# -*- coding: utf-8 -*-
"""
Tests for Neo IO features
"""

import pkg_resources
import tempfile
import shutil
import gc
import unittest

import neurotic

import logging
logger = logging.getLogger(__name__)


class NeoIOUnitTest(unittest.TestCase):

    def setUp(self):
        self.file = pkg_resources.resource_filename(
            'neurotic.tests', 'metadata-for-tests.yml')

        # make a copy of the metadata file in a temp directory
        self.temp_dir = tempfile.TemporaryDirectory(prefix='neurotic-')
        self.temp_file = shutil.copy(self.file, self.temp_dir.name)

    def tearDown(self):
        # clean up references to proxy objects which keep files locked
        gc.collect()

        # remove the temp directory
        self.temp_dir.cleanup()

    def test_missing_data_file(self):
        """Test error is raised when data file is not found locally"""
        dataset = 'video-jumps-unset'
        metadata = neurotic.MetadataSelector(file=self.temp_file,
                                             initial_selection=dataset)
        # intentionally skipping downloading data file

        with self.assertRaises(FileNotFoundError):
            blk = neurotic.load_dataset(metadata=metadata, lazy=True)

    def test_missing_extension_error(self):
        """Test error is raised when file extension and io_class are missing"""
        dataset = 'missing-extension-without-io_class'
        metadata = neurotic.MetadataSelector(file=self.temp_file,
                                             initial_selection=dataset)
        metadata.download('data_file')

        with self.assertRaisesRegex(IOError, 'Could not find an appropriate neo.io class .*'):
            blk = neurotic.load_dataset(metadata=metadata, lazy=True)

    def test_missing_extension_io_class(self):
        """Test io_class works for data file with missing extension"""
        dataset = 'missing-extension-with-io_class'
        metadata = neurotic.MetadataSelector(file=self.temp_file,
                                             initial_selection=dataset)
        metadata.download('data_file')

        blk = neurotic.load_dataset(metadata=metadata, lazy=True)
        assert(blk)

    def test_plain_text_axograph(self):
        """Test reading a plain text AXGT file using io_class and io_args"""
        dataset = 'plain-text-axograph'
        metadata = neurotic.MetadataSelector(file=self.temp_file,
                                             initial_selection=dataset)
        metadata.download('data_file')

        blk = neurotic.load_dataset(metadata=metadata, lazy=False)
        assert(blk)

    def test_matlab(self):
        """Test reading a MATLAB file"""
        dataset = 'matlab example'
        metadata = neurotic.MetadataSelector(file=self.temp_file,
                                             initial_selection=dataset)
        metadata.download('data_file')

        blk = neurotic.load_dataset(metadata=metadata, lazy=False)
        assert(blk)

if __name__ == '__main__':
    unittest.main()
