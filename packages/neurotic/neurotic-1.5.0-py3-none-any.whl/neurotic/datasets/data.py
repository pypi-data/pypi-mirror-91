# -*- coding: utf-8 -*-
"""
The :mod:`neurotic.datasets.data` module implements a function for loading a
dataset from selected metadata.

.. autofunction:: load_dataset
"""

import datetime
import inspect
from packaging import version
import numpy as np
import pandas as pd
import quantities as pq
import neo

from ..datasets.metadata import _abs_path
from .. import _elephant_tools

import logging
logger = logging.getLogger(__name__)


def load_dataset(metadata, blk=None, lazy=False, signal_group_mode='split-all', filter_events_from_epochs=False):
    """
    Load a dataset.

    ``metadata`` may be a :class:`MetadataSelector
    <neurotic.datasets.metadata.MetadataSelector>` or a simple dictionary
    containing the appropriate data.

    The ``data_file`` in ``metadata`` is read into a Neo :class:`Block
    <neo.core.Block>` using an automatically detected :mod:`neo.io` class
    if ``lazy=False`` or a :mod:`neo.rawio` class if ``lazy=True``. If
    ``data_file`` is unspecified, an empty Neo Block is created instead. If a
    Neo Block is passed as ``blk``, ``data_file`` is ignored.

    Epochs and events loaded from ``annotations_file`` and
    ``epoch_encoder_file`` and spike trains loaded from ``tridesclous_file``
    are added to the Neo Block.

    If ``lazy=False``, parameters given in ``metadata`` are used to apply
    filters to the signals, to detect spikes using amplitude discriminators, to
    calculate smoothed firing rates from spike trains, to detect bursts of
    spikes, and to calculate the rectified area under the curve (RAUC) for each
    signal.
    """

    if blk is None:
        if metadata.get('data_file', None) is not None:
            # read in the electrophysiology data
            blk = _read_data_file(metadata, lazy, signal_group_mode)
        else:
            # create an empty Block
            blk = neo.Block()
            seg = neo.Segment()
            blk.segments.append(seg)
    else:
        # a Block was provided
        if not isinstance(blk, neo.Block):
            raise TypeError('blk must be a neo.Block')

    # update the real-world start time of the data if provided
    if metadata.get('rec_datetime', None) is not None:
        if isinstance(metadata['rec_datetime'], datetime.datetime):
            blk.rec_datetime = metadata['rec_datetime']
        else:
            logger.warning('Ignoring rec_datetime because it is not a properly formatted datetime: {}'.format(metadata['rec_datetime']))

    # apply filters to signals if not using lazy loading of signals
    if not lazy:
        blk = _apply_filters(metadata, blk)

    # copy events into epochs and vice versa
    epochs_from_events = [neo.Epoch(name=ev.name, times=ev.times, labels=ev.labels, durations=np.zeros_like(ev.times)) for ev in blk.segments[0].events]
    events_from_epochs = [neo.Event(name=ep.name, times=ep.times, labels=ep.labels) for ep in blk.segments[0].epochs]
    if not filter_events_from_epochs:
        blk.segments[0].epochs += epochs_from_events
    blk.segments[0].events += events_from_epochs

    # read in annotations
    annotations_dataframe = _read_annotations_file(metadata)
    blk.segments[0].epochs += _create_neo_epochs_from_dataframe(annotations_dataframe, metadata, _abs_path(metadata, 'annotations_file'), filter_events_from_epochs)
    blk.segments[0].events += _create_neo_events_from_dataframe(annotations_dataframe, metadata, _abs_path(metadata, 'annotations_file'))

    # read in epoch encoder file
    epoch_encoder_dataframe = _read_epoch_encoder_file(metadata)
    blk.segments[0].epochs += _create_neo_epochs_from_dataframe(epoch_encoder_dataframe, metadata, _abs_path(metadata, 'epoch_encoder_file'), filter_events_from_epochs)
    blk.segments[0].events += _create_neo_events_from_dataframe(epoch_encoder_dataframe, metadata, _abs_path(metadata, 'epoch_encoder_file'))

    # classify spikes by amplitude if not using lazy loading of signals
    if not lazy:
        blk.segments[0].spiketrains += _run_amplitude_discriminators(metadata, blk)

    # read in spikes identified by spike sorting using tridesclous
    spikes_dataframe = _read_spikes_file(metadata, blk)
    if spikes_dataframe is not None:
        if blk.segments[0].analogsignals:
            t_start = blk.segments[0].analogsignals[0].t_start                 # assuming all AnalogSignals start at the same time
            t_stop = blk.segments[0].analogsignals[0].t_stop                   # assuming all AnalogSignals start at the same time
            sampling_period = blk.segments[0].analogsignals[0].sampling_period # assuming all AnalogSignals have the same sampling rate
            blk.segments[0].spiketrains += _create_neo_spike_trains_from_dataframe(spikes_dataframe, metadata, t_start, t_stop, sampling_period)
        else:
            logger.warning('Ignoring tridesclous_file because the sampling rate and start time could not be inferred from analog signals')

    # calculate smoothed firing rates from spike trains if not using lazy
    # loading of signals
    if not lazy:
        blk = _compute_firing_rates(metadata, blk)

    # identify bursts from spike trains if not using lazy loading of signals
    if not lazy:
        blk.segments[0].epochs += _run_burst_detectors(metadata, blk)

    # alphabetize epoch and event channels by name
    blk.segments[0].epochs.sort(key=lambda ep: ep.name or '')
    blk.segments[0].events.sort(key=lambda ev: ev.name or '')

    # compute rectified area under the curve (RAUC) for each signal if not
    # using lazy loading of signals
    if not lazy and metadata.get('rauc_bin_duration', None) is not None:
        for sig in blk.segments[0].analogsignals:
            rauc_sig = _elephant_tools.rauc(
                signal=sig,
                baseline=metadata.get('rauc_baseline', None),
                bin_duration=metadata['rauc_bin_duration']*pq.s,
            )
            rauc_sig.name = sig.name + ' RAUC'
            sig.annotate(
                rauc_sig=rauc_sig,
                rauc_baseline=metadata.get('rauc_baseline', None),
                rauc_bin_duration=metadata['rauc_bin_duration']*pq.s,
            )

    return blk

def _get_io(metadata):
    """
    Return a :mod:`neo.io` object for reading the ``data_file`` in
    ``metadata``. An appropriate :mod:`neo.io` class is typically determined
    automatically from the file extension, but this can be overridden with the
    optional ``io_class`` metadata parameter. Arbitrary arguments can be passed
    to the :mod:`neo.io` class using the optional ``io_args`` metadata
    parameter.
    """

    # prepare arguments for instantiating a Neo IO class
    if metadata.get('io_args', None) is not None:
        io_args = metadata['io_args'].copy()
        if 'sampling_rate' in io_args:
            # AsciiSignalIO's sampling_rate must be a Quantity
            io_args['sampling_rate'] *= pq.Hz
    else:
        io_args = {}

    if metadata.get('io_class', None) is None:
        try:
            # detect the class automatically using the file extension
            io = neo.io.get_io(_abs_path(metadata, 'data_file'), **io_args)
        except IOError as e:
            if len(e.args) > 0 and type(e.args[0]) is str and e.args[0].startswith('File extension'):
                # provide a useful error message when format detection fails
                raise IOError("Could not find an appropriate neo.io class " \
                              f"for data_file \"{metadata['data_file']}\". " \
                              "Try specifying one in your metadata using " \
                              "the io_class parameter.")
            else:
                # something else has gone wrong, like the file not being found
                raise e

    else:
        # use a user-specified class
        io_list = [io.__name__ for io in neo.io.iolist]
        if metadata['io_class'] not in io_list:
            raise ValueError(f"specified io_class \"{metadata['io_class']}\" was not found in neo.io.iolist: {io_list}")
        io_class_index = io_list.index(metadata['io_class'])
        io_class = neo.io.iolist[io_class_index]
        io = io_class(_abs_path(metadata, 'data_file'), **io_args)

    return io

def _read_data_file(metadata, lazy=False, signal_group_mode='split-all'):
    """
    Read in the ``data_file`` given in ``metadata`` using a :mod:`neo.io`
    class. Lazy-loading is used for signals if both ``lazy=True`` and the data
    file type is supported by a :mod:`neo.rawio` class; otherwise, signals are
    fully loaded. Lazy-loading is never used for epochs, events, and spike
    trains contained in the data file; these are always fully loaded. Returns a
    Neo :class:`Block <neo.core.Block>`.
    """

    # get a Neo IO object appropriate for the data file type
    io = _get_io(metadata)

    # force lazy=False if lazy is not supported by the reader class
    if lazy and not io.support_lazy:
        lazy = False
        logger.info(f'NOTE: Not reading signals in lazy mode because Neo\'s {io.__class__.__name__} reader does not support it.')

    if 'signal_group_mode' in inspect.signature(io.read_block).parameters.keys():
        # - signal_group_mode='split-all' is the default because this ensures
        #   every channel gets its own AnalogSignal, which is important for
        #   indexing in EphyviewerConfigurator
        blk = io.read_block(lazy=lazy, signal_group_mode=signal_group_mode)
    else:
        # some IOs do not have signal_group_mode
        blk = io.read_block(lazy=lazy)

    if lazy and isinstance(io, neo.rawio.baserawio.BaseRawIO):
        # store the rawio for use with AnalogSignalFromNeoRawIOSource
        blk.rawio = io

    # load all objects except analog signals
    if lazy:

        if version.parse(neo.__version__) >= version.parse('0.8.0'):  # Neo >= 0.8.0 has proxy objects with load method

            for i in range(len(blk.segments[0].epochs)):
                epoch = blk.segments[0].epochs[i]
                if hasattr(epoch, 'load'):
                    blk.segments[0].epochs[i] = epoch.load()

            for i in range(len(blk.segments[0].events)):
                event = blk.segments[0].events[i]
                if hasattr(event, 'load'):
                    blk.segments[0].events[i] = event.load()

            for i in range(len(blk.segments[0].spiketrains)):
                spiketrain = blk.segments[0].spiketrains[i]
                if hasattr(spiketrain, 'load'):
                    blk.segments[0].spiketrains[i] = spiketrain.load()

        else:  # Neo < 0.8.0 does not have proxy objects

            neorawioclass = neo.rawio.get_rawio_class(_abs_path(metadata, 'data_file'))
            if neorawioclass is not None:
                neorawio = neorawioclass(_abs_path(metadata, 'data_file'))
                neorawio.parse_header()

                for i in range(len(blk.segments[0].epochs)):
                    epoch = blk.segments[0].epochs[i]
                    channel_index = next((i for i, chan in enumerate(neorawio.header['event_channels']) if chan['name'] == epoch.name and chan['type'] == b'epoch'), None)
                    if channel_index is not None:
                        ep_raw_times, ep_raw_durations, ep_labels = neorawio.get_event_timestamps(event_channel_index=channel_index)
                        ep_times = neorawio.rescale_event_timestamp(ep_raw_times, dtype='float64')
                        ep_durations = neorawio.rescale_epoch_duration(ep_raw_durations, dtype='float64')
                        ep = neo.Epoch(times=ep_times*pq.s, durations=ep_durations*pq.s, labels=ep_labels, name=epoch.name)
                        blk.segments[0].epochs[i] = ep

                for i in range(len(blk.segments[0].events)):
                    event = blk.segments[0].events[i]
                    channel_index = next((i for i, chan in enumerate(neorawio.header['event_channels']) if chan['name'] == event.name and chan['type'] == b'event'), None)
                    if channel_index is not None:
                        ev_raw_times, _, ev_labels = neorawio.get_event_timestamps(event_channel_index=channel_index)
                        ev_times = neorawio.rescale_event_timestamp(ev_raw_times, dtype='float64')
                        ev = neo.Event(times=ev_times*pq.s, labels=ev_labels, name=event.name)
                        blk.segments[0].events[i] = ev

                for i in range(len(blk.segments[0].spiketrains)):
                    spiketrain = blk.segments[0].spiketrains[i]
                    channel_index = next((i for i, chan in enumerate(neorawio.header['unit_channels']) if chan['name'] == spiketrain.name), None)
                    if channel_index is not None:
                        st_raw_times = neorawio.get_spike_timestamps(unit_index=channel_index)
                        st_times = neorawio.rescale_spike_timestamp(st_raw_times, dtype='float64')
                        st = neo.SpikeTrain(times=st_times*pq.s, name=st.name)
                        blk.segments[0].spiketrains[i] = st

    # convert byte labels to Unicode strings
    for epoch in blk.segments[0].epochs:
        epoch.labels = epoch.labels.astype('U')

    for event in blk.segments[0].events:
        event.labels = event.labels.astype('U')

    return blk

def _read_annotations_file(metadata):
    """
    Read in epochs and events from the ``annotations_file`` in ``metadata`` and
    return a dataframe.
    """

    if metadata.get('annotations_file', None) is None:

        return None

    else:

        # data types for each column in the file
        dtypes = {
            'Start (s)': float,
            'End (s)':   float,
            'Type':      str,
            'Label':     str,
        }

        # parse the file and create a dataframe
        df = pd.read_csv(_abs_path(metadata, 'annotations_file'), dtype = dtypes)

        # increment row labels by 2 so they match the source file
        # which is 1-indexed and has a header
        df.index += 2

        # discard entries with missing or negative start times
        bad_start = df['Start (s)'].isnull() | (df['Start (s)'] < 0)
        if bad_start.any():
            logger.warning('These rows will be discarded because their Start '
                           'times are missing or negative:\n'
                           f'{df[bad_start]}')
            df = df[~bad_start]

        # discard entries with end time preceding start time
        bad_end = df['End (s)'] < df['Start (s)']
        if bad_end.any():
            logger.warning('These rows will be discarded because their End '
                           'times precede their Start times:\n'
                           f'{df[bad_end]}')
            df = df[~bad_end]

        # compute durations
        df.insert(
            column = 'Duration (s)',
            value = df['End (s)'] - df['Start (s)'],
            loc = 2, # insert after 'End (s)'
        )

        # replace some NaNs
        df.fillna({
            'Duration (s)': 0,
            'Type': 'Other',
            'Label': '',
        }, inplace = True)

        # sort entries by time
        df.sort_values([
            'Start (s)',
            'Duration (s)',
        ], inplace = True)

        # return the dataframe
        return df

def _read_epoch_encoder_file(metadata):
    """
    Read in epochs from the ``epoch_encoder_file`` in ``metadata`` and return a
    dataframe.
    """

    if metadata.get('epoch_encoder_file', None) is None:

        return None

    else:

        # data types for each column in the file
        dtypes = {
            'Start (s)': float,
            'End (s)':   float,
            'Type':      str,
        }

        # parse the file and create a dataframe
        df = pd.read_csv(_abs_path(metadata, 'epoch_encoder_file'), dtype = dtypes)

        # increment row labels by 2 so they match the source file
        # which is 1-indexed and has a header
        df.index += 2

        # discard entries with missing or negative start times
        bad_start = df['Start (s)'].isnull() | (df['Start (s)'] < 0)
        if bad_start.any():
            logger.warning('These rows will be discarded because their Start '
                           'times are missing or negative:\n'
                           f'{df[bad_start]}')
            df = df[~bad_start]

        # discard entries with end time preceding start time
        bad_end = df['End (s)'] < df['Start (s)']
        if bad_end.any():
            logger.warning('These rows will be discarded because their End '
                           'times precede their Start times:\n'
                           f'{df[bad_end]}')
            df = df[~bad_end]

        # compute durations
        df.insert(
            column = 'Duration (s)',
            value = df['End (s)'] - df['Start (s)'],
            loc = 2, # insert after 'End (s)'
        )

        # replace some NaNs
        df.fillna({
            'Duration (s)': 0,
            'Type': 'Other',
        }, inplace = True)

        # sort entries by time
        df.sort_values([
            'Start (s)',
            'Duration (s)',
        ], inplace = True)

        # add 'Label' column to indicate where these epochs came from
        df.insert(
            column = 'Label',
            value = '(from epoch encoder file)',
            loc = 4, # insert after 'Type'
        )

        # return the dataframe
        return df

def _read_spikes_file(metadata, blk):
    """
    Read in spikes identified by spike sorting with tridesclous and return a
    dataframe.
    """

    if metadata.get('tridesclous_file', None) is None or metadata.get('tridesclous_channels', None) is None:

        return None

    else:

        # parse the file and create a dataframe
        df = pd.read_csv(_abs_path(metadata, 'tridesclous_file'), names = ['index', 'label'])

        # drop clusters with negative labels
        df = df[df['label'] >= 0]

        if metadata.get('tridesclous_merge', None):
            # merge some clusters and drop all others
            new_labels = []
            for clusters_to_merge in metadata['tridesclous_merge']:
                new_label = clusters_to_merge[0]
                new_labels.append(new_label)
                df.loc[df['label'].isin(clusters_to_merge), 'label'] = new_label
            df = df[df['label'].isin(new_labels)]

        # return the dataframe
        return df

def _create_neo_epochs_from_dataframe(dataframe, metadata, file_origin, filter_events_from_epochs=False):
    """
    Convert the contents of a dataframe into Neo :class:`Epochs
    <neo.core.Epoch>`.
    """

    epochs_list = []

    if dataframe is not None:

        if filter_events_from_epochs:
            # keep only rows with a positive duration
            dataframe = dataframe[dataframe['Duration (s)'] > 0]

        # group epochs by type
        for type_name, df in dataframe.groupby('Type'):

            # create a Neo Epoch for each type
            epoch = neo.Epoch(
                name = type_name,
                file_origin = file_origin,
                times = df['Start (s)'].values * pq.s,
                durations = df['Duration (s)'].values * pq.s,
                labels = df['Label'].values,
            )

            epochs_list.append(epoch)

    # return the list of Neo Epochs
    return epochs_list

def _create_neo_events_from_dataframe(dataframe, metadata, file_origin):
    """
    Convert the contents of a dataframe into Neo :class:`Events
    <neo.core.Event>`.
    """

    events_list = []

    if dataframe is not None:

        # group events by type
        for type_name, df in dataframe.groupby('Type'):

            # create a Neo Event for each type
            event = neo.Event(
                name = type_name,
                file_origin = file_origin,
                times = df['Start (s)'].values * pq.s,
                labels = df['Label'].values,
            )

            events_list.append(event)

    # return the list of Neo Events
    return events_list

def _create_neo_spike_trains_from_dataframe(dataframe, metadata, t_start, t_stop, sampling_period):
    """
    Convert the contents of a dataframe into Neo :class:`SpikeTrains
    <neo.core.SpikeTrain>`.
    """

    spiketrain_list = []

    if dataframe is not None:

        # group spikes by cluster label
        for spike_label, df in dataframe.groupby('label'):

            # look up the channels that this unit was found on
            channels = metadata['tridesclous_channels'][spike_label]

            # create a Neo SpikeTrain for each cluster label
            st = neo.SpikeTrain(
                name = str(spike_label),
                file_origin = _abs_path(metadata, 'tridesclous_file'),
                times = t_start + sampling_period * df['index'].values,
                t_start = t_start,
                t_stop = t_stop,
            )

            st.annotate(
                channels=channels,
                amplitude=None,
            )

            spiketrain_list.append(st)

    return spiketrain_list

def _apply_filters(metadata, blk):
    """
    Apply filters specified in ``metadata`` to the signals in ``blk``.
    """

    if metadata.get('filters', None) is not None:

        signalNameToIndex = {sig.name:i for i, sig in enumerate(blk.segments[0].analogsignals)}

        for sig_filter in metadata['filters']:

            index = signalNameToIndex.get(sig_filter['channel'], None)
            if index is None:

                logger.warning('Skipping filter with channel name {} because channel was not found!'.format(sig_filter['channel']))

            else:

                high = sig_filter.get('highpass', None)
                low  = sig_filter.get('lowpass',  None)
                if high:
                    high *= pq.Hz
                if low:
                    low  *= pq.Hz
                blk.segments[0].analogsignals[index] = _elephant_tools.butter(
                    signal = blk.segments[0].analogsignals[index],
                    highpass_freq = high,
                    lowpass_freq  = low,
                )

    return blk

def _run_amplitude_discriminators(metadata, blk):
    """
    Run all amplitude discriminators for spike detection given in ``metadata``
    on the signals in ``blk``.
    """

    spiketrain_list = []

    if metadata.get('amplitude_discriminators', None) is not None:

        signalNameToIndex = {sig.name:i for i, sig in enumerate(blk.segments[0].analogsignals)}
        epochs = blk.segments[0].epochs

        # classify spikes by amplitude
        for discriminator in metadata['amplitude_discriminators']:

            index = signalNameToIndex.get(discriminator['channel'], None)
            if index is None:

                logger.warning('Skipping amplitude discriminator with channel name {} because channel was not found!'.format(discriminator['channel']))

            else:

                sig = blk.segments[0].analogsignals[index]
                st = _detect_spikes(sig, discriminator, epochs)
                spiketrain_list.append(st)

    return spiketrain_list


def _detect_spikes(sig, discriminator, epochs):
    """
    Detect spikes in the amplitude window given by ``discriminator`` and
    optionally filter them by coincidence with epochs of a given name.
    """

    assert sig.name == discriminator['channel'], 'sig name "{}" does not match amplitude discriminator channel "{}"'.format(sig.name, discriminator['channel'])

    min_threshold = min(discriminator['amplitude'])
    max_threshold = max(discriminator['amplitude'])
    spike_type = discriminator.get('type', None)
    if spike_type == 'peak':
        sign = 'above'
    elif spike_type == 'trough':
        sign = 'below'
    elif spike_type is None:
        # infer type from thresholds
        if min_threshold >= 0 and max_threshold > 0:
            spike_type = 'peak'
            sign = 'above'
        elif min_threshold < 0 and max_threshold <= 0:
            spike_type = 'trough'
            sign = 'below'
        else:
            raise ValueError('automatic spike type inference for amplitude discriminator is possible only with two nonnegative thresholds (type=peak) or two nonpositive thresholds (type=trough); otherwise, type must be given explicitly: {}'.format(discriminator))
    else:
        raise ValueError('amplitude discriminator type must be "peak", "trough", or unspecified: {}'.format(discriminator))

    spikes_crossing_min = _elephant_tools.peak_detection(sig, pq.Quantity(min_threshold, discriminator['units']), sign, 'raw')
    spikes_crossing_max = _elephant_tools.peak_detection(sig, pq.Quantity(max_threshold, discriminator['units']), sign, 'raw')
    if spike_type == 'peak':
        spikes_between_min_and_max = np.setdiff1d(spikes_crossing_min, spikes_crossing_max)
    elif spike_type == 'trough':
        spikes_between_min_and_max = np.setdiff1d(spikes_crossing_max, spikes_crossing_min)
    else:
        raise ValueError('type should be "peak" or "trough": {}'.format(spike_type))

    st = neo.SpikeTrain(
        name = discriminator['name'],
        times = spikes_between_min_and_max * pq.s,
        t_start = sig.t_start,
        t_stop  = sig.t_stop,
    )

    st.annotate(
        channels=[discriminator['channel']],
        amplitude=pq.Quantity(discriminator['amplitude'], discriminator['units']),
        type=spike_type,
    )

    if 'epoch' in discriminator:

        time_masks = []
        if isinstance(discriminator['epoch'], str):
            # search for matching epochs
            ep = next((ep for ep in epochs if ep.name == discriminator['epoch']), None)
            if ep is not None:
                # select spike times that fall within each epoch
                for t_start, duration in zip(ep.times, ep.durations):
                    t_stop = t_start + duration
                    time_masks.append((t_start <= st) & (st < t_stop))
            else:
                # no matching epochs found
                time_masks.append([False] * len(st))
        else:
            # may eventually implement lists of ordered pairs, but
            # for now raise an error
            raise ValueError('amplitude discriminator epoch could not be handled: {}'.format(discriminator['epoch']))

        # select the subset of spikes that fall within the epoch
        # windows
        st = st[np.any(time_masks, axis=0)]

        st.annotate(epoch=discriminator['epoch'])

    return st

def _run_burst_detectors(metadata, blk):
    """
    Run all burst detectors given in ``metadata`` on the spike trains in
    ``blk``.
    """

    burst_list = []

    if metadata.get('burst_detectors', None) is not None:

        spikeTrainNameToIndex = {st.name:i for i, st in enumerate(blk.segments[0].spiketrains)}

        # detect bursts of spikes using frequency thresholds
        for detector in metadata['burst_detectors']:

            index = spikeTrainNameToIndex.get(detector['spiketrain'], None)
            if index is None:

                logger.warning("Skipping burst detector for spike train named "
                      f"\"{detector['spiketrain']}\" because spike train was "
                      "not found!")

            else:

                st = blk.segments[0].spiketrains[index]
                start_freq, stop_freq = detector['thresholds']*pq.Hz
                burst = _find_bursts(st, start_freq, stop_freq)
                burst.name = detector.get('name', detector['spiketrain'] + ' burst')
                burst_list.append(burst)

    return burst_list

def _find_bursts(st, start_freq, stop_freq):
    """
    Find every period of time during which the instantaneous firing frequency
    (IFF) of the Neo :class:`SpikeTrain <neo.core.SpikeTrain>` ``st`` meets the
    criteria for bursting. Return the set of bursts as a Neo :class:`Epoch
    <neo.core.Epoch>`, with ``array_annotations['spikes']`` listing the number
    of spikes contained in each burst.

    A burst is defined as a period beginning when the IFF exceeds
    ``start_freq`` and ending when the IFF subsequently drops below the
    ``stop_freq``. Note that in general ``stop_freq`` should not exceed
    ``start_freq``, since otherwise bursts may not be detected.
    """

    isi = _elephant_tools.isi(st).rescale('s')
    iff = 1/isi

    start_mask = iff > start_freq
    stop_mask = iff < stop_freq

    times = []
    durations = []
    n_spikes = []
    scan_index = -1
    while scan_index < iff.size:
        start_index = None
        stop_index = None

        start_mask_indexes = np.where(start_mask)[0]
        start_mask_indexes = start_mask_indexes[start_mask_indexes > scan_index]
        if start_mask_indexes.size == 0:
            break

        start_index = start_mask_indexes[0] # first time that iff rises above start threshold

        stop_mask_indexes = np.where(stop_mask)[0]
        stop_mask_indexes = stop_mask_indexes[stop_mask_indexes > start_index]
        if stop_mask_indexes.size > 0:
            stop_index = stop_mask_indexes[0] # first time after start that iff drops below stop theshold
        else:
            stop_index = -1 # end of spike train (include all spikes after start)

        times.append(st[start_index].rescale('s').magnitude)
        durations.append((st[stop_index] - st[start_index]).rescale('s').magnitude)
        n_spikes.append(stop_index-start_index+1 if stop_index > 0 else st.size-start_index)

        if stop_index == -1:
            break
        else:
            scan_index = stop_index

    bursts = neo.Epoch(
        times = times*pq.s,
        durations = durations*pq.s,
        labels = [''] * len(times),
        array_annotations = {'spikes': n_spikes},
    )

    return bursts

def _compute_firing_rates(metadata, blk):
    """
    Compute instantaneous firing rates using parameters given in ``metadata``
    on spike trains in ``blk``.

    The elephant package's :func:`instantaneous_rate
    <elephant.statistics.instantaneous_rate>` function is used for calculating
    firing rates. The :mod:`kernel <elephant.kernels>` classes from the
    elephant package, as well as :class:`CausalAlphaKernel
    <neurotic._elephant_tools.CausalAlphaKernel>`, may be used. The function
    and kernel classes are sourced from :mod:`neurotic._elephant_tools`, rather
    than the elephant package itself, to avoid having elephant as a package
    dependency.
    """

    if metadata.get('firing_rates', None) is not None:

        t_start = blk.segments[0].t_start
        t_stop = blk.segments[0].t_stop
        sampling_period = blk.segments[0].analogsignals[0].sampling_period

        for firing_rate in metadata['firing_rates']:

            spiketrain = next((st for st in blk.segments[0].spiketrains if st.name == firing_rate['name']), None)
            if spiketrain is None:

                logger.warning('Skipping firing rate computation with name {} because spike train was not found!'.format(firing_rate['name']))

            else:

                kernel_cls = getattr(_elephant_tools, firing_rate['kernel'], None)

                if kernel_cls is None or not issubclass(kernel_cls, _elephant_tools.Kernel):

                    logger.warning('Skipping firing rate computation with name {} because kernel "{}" was not found!'.format(firing_rate['name'], firing_rate['kernel']))

                else:

                    kernel = kernel_cls(firing_rate['sigma']*pq.s)
                    firing_rate_sig = _elephant_tools.instantaneous_rate(
                        spiketrain=spiketrain,
                        sampling_period=sampling_period,
                        kernel=kernel,
                        t_start=t_start,
                        t_stop=t_stop,
                    )
                    firing_rate_sig.t_start = firing_rate_sig.t_start.rescale('s')
                    firing_rate_sig.name = firing_rate['name']
                    firing_rate_sig.annotations['t_stop'] = firing_rate_sig.annotations['t_stop'].rescale('s')
                    spiketrain.annotate(
                        firing_rate_sig=firing_rate_sig,
                        firing_rate_kernel=firing_rate['kernel'],
                        firing_rate_sigma=firing_rate['sigma']*pq.s,
                    )

    return blk
