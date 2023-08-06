# -*- coding: utf-8 -*-
"""
The :mod:`neurotic.datasets.download` module implements a general purpose
download function that handles connecting to remote servers, performing
authentication, and downloading files with progress reporting. The function
handles various errors and will automatically reprompt the user for login
credentials if a bad user name or password is given.

The module installs an :class:`urllib.request.HTTPBasicAuthHandler` and a
:class:`neurotic.datasets.ftpauth.FTPBasicAuthHandler` at import time.

.. autofunction:: download
"""

import os
import shutil
import urllib
from getpass import getpass
import numpy as np
from tqdm.auto import tqdm

from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from .. import global_config
from ..datasets.ftpauth import FTPBasicAuthHandler
from ..datasets.gdrive import GoogleDriveDownloader

import logging
logger = logging.getLogger(__name__)


# install HTTP and FTP authentication handlers, the latter of which also adds
# reliable file size retrieval before downloading
_max_bad_login_attempts = 3
_http_auth_handler = HTTPBasicAuthHandler(HTTPPasswordMgrWithDefaultRealm())
_ftp_auth_handler = FTPBasicAuthHandler()
_opener = urllib.request.build_opener(_http_auth_handler, _ftp_auth_handler)
urllib.request.install_opener(_opener)

gdrive_downloader = GoogleDriveDownloader(
    client_secret_file=global_config['gdrive']['client_secret_file'],
    tokens_file=global_config['gdrive']['tokens_file'],
    save_tokens=global_config['gdrive']['save_tokens'],
)


def download(url, local_file, overwrite_existing=False, show_progress=True, bytes_per_chunk=1024*8):
    """
    Download a file.
    """
    if urllib.parse.urlparse(url).scheme == 'gdrive':
        return gdrive_downloader.download(url, local_file, show_progress=show_progress, bytes_per_chunk=1024*1024*5)

    if not overwrite_existing and os.path.exists(local_file):
        logger.info(f'Skipping {os.path.basename(local_file)} (already exists)')
        return

    error = None
    error_code = None

    logger.info(f'Downloading {os.path.basename(local_file)}')
    try:
        _download_with_progress_bar(url, local_file, show_progress=show_progress, bytes_per_chunk=bytes_per_chunk)

    except urllib.error.HTTPError as e:

        error = e
        error_code = e.code

    except urllib.error.URLError as e:

        error = e

        if isinstance(e.reason, str):

            # special cases for ftp errors
            if e.reason.startswith('ftp error: error_perm('):
                reason = e.reason[23:-2]
                error_code = int(reason[:3])
            elif e.reason.startswith('ftp error: TimeoutError('):
                reason = e.reason[24:-2]
                error_code = int(reason[:5])
            else:
                error_code = -1

        else:

            error_code = e.reason.errno

    finally:

        if error_code is not None:

            if error_code == 404:
                # not found
                logger.error(f'Skipping {os.path.basename(local_file)} (not found on server)')
                raise error

            elif error_code == 550:
                # no such file or folder, or permission denied
                logger.error(f'Skipping {os.path.basename(local_file)} (not found on server, or user is unauthorized)')
                raise error

            elif error_code == 10060:
                # timeout
                hostname = urllib.parse.urlparse(url).hostname
                logger.error(f'Skipping {os.path.basename(local_file)} (timed out when connecting to {hostname})')
                raise error

            elif error_code == 11001:
                # could not reach server or resolve hostname
                hostname = urllib.parse.urlparse(url).hostname
                logger.error(f'Skipping {os.path.basename(local_file)} (cannot connect to {hostname})')
                raise error

            else:
                logger.error(f'Encountered a problem: {error}')
                raise error


def _download_with_progress_bar(url, local_file, show_progress=True, bytes_per_chunk=1024*8):
    """
    Authenticate if necessary, then download while showing a progress bar.
    """

    auth_needed =  _auth_needed(url)
    if auth_needed:
        authenticated = _authenticate(url)

    if not auth_needed or (auth_needed and authenticated):

        # determine where to temporarily save the file during download
        temp_file = local_file + '.part'
        logger.debug(f'Temporarily downloading to {temp_file}')

        # create the containing directory if necessary
        if not os.path.exists(os.path.dirname(local_file)):
            os.makedirs(os.path.dirname(local_file))

        try:
            with urllib.request.urlopen(urllib.parse.quote(url, safe='/:')) as dist:
                with open(temp_file, 'wb') as f:
                    if show_progress:
                        if 'Content-Length' in dist.headers:
                            # knowing the file size allows progress to be displayed
                            file_size_in_bytes = int(dist.headers['Content-Length'])
                            num_chunks = int(np.ceil(file_size_in_bytes/bytes_per_chunk))
                            total = num_chunks*bytes_per_chunk
                        else:
                            # progress can't be displayed, but other stats can be
                            total = None
                        pbar = tqdm(total=total, unit='B', unit_scale=True)
                    while True:
                        chunk = dist.read(bytes_per_chunk)
                        if chunk:
                            f.write(chunk)
                            if show_progress:
                                pbar.update(bytes_per_chunk)
                        else:
                            break
                    if show_progress:
                        pbar.close()

        except:
            # the download is likely incomplete, so delete the temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)

            # raise the exception so that it can be handled elsewhere
            raise

        else:
            # download completed, so move the temp file to the final location
            shutil.move(temp_file, local_file)


def _auth_needed(url):
    """
    Determine whether authentication is needed by attempting to make a
    connection.
    """

    # escape spaces and other unsafe characters
    url = urllib.parse.quote(url, safe='/:')

    error = None
    error_code = None

    try:
        # try to connect
        with urllib.request.urlopen(url) as dist:
            # if connection was successful, additional auth is not needed
            return False

    except urllib.error.HTTPError as e:

        error = e
        error_code = e.code

    except urllib.error.URLError as e:

        error = e

        if isinstance(e.reason, str):

            # special cases for ftp errors
            if e.reason.startswith('ftp error: error_perm('):
                reason = e.reason[23:-2]
                error_code = int(reason[:3])
            else:
                raise

        else:

            error_code = e.reason.errno

    finally:

        if error_code is not None:

            if error_code in [401, 530, 553]:
                # unauthorized
                return True

            else:
                raise error


def _authenticate(url):
    """
    Perform HTTP or FTP authentication.
    """

    # escape spaces and other unsafe characters
    url = urllib.parse.quote(url, safe='/:')

    bad_login_attempts = 0
    while True:

        error = None
        error_code = None

        try:
            # try to connect
            with urllib.request.urlopen(url) as dist:
                # if connection was successful, authentication is done
                return True

        except urllib.error.HTTPError as e:

            error = e
            error_code = e.code

        except urllib.error.URLError as e:

            error = e

            if isinstance(e.reason, str):

                # special cases for ftp errors
                if e.reason.startswith('ftp error: error_perm('):
                    reason = e.reason[23:-2]
                    error_code = int(reason[:3])
                else:
                    raise

            else:

                error_code = e.reason.errno

        finally:

            if error_code is not None:

                if error_code == 401:
                    # unauthorized -- will try to authenticate with http handler
                    handler = _http_auth_handler

                elif error_code in [530, 553]:
                    # unauthorized -- will try to authenticate with ftp handler
                    handler = _ftp_auth_handler

                else:
                    raise error

        if bad_login_attempts >= _max_bad_login_attempts:
            logger.error('Unauthorized: Aborting login')
            return False
        else:
            if bad_login_attempts == 0:
                logger.info('Authentication required')
            else:
                logger.warning(f'Failed login ({bad_login_attempts} of '
                      f'{_max_bad_login_attempts}): Bad login credentials, or '
                      f'else user {user} does not have permission to access '
                      f'{url}')
            bad_login_attempts += 1

            netloc = urllib.parse.urlparse(url).netloc
            host, port = urllib.parse.splitport(netloc)
            user = input(f'User name on {host}: ')
            if not user:
                logger.error('No user given, aborting login')
                return False
            passwd = getpass('Password: ')
            handler.add_password(None, netloc, user, passwd)
