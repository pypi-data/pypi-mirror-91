# -*- coding: utf-8 -*-
"""
The :mod:`neurotic.gui.standalone` module implements the main window of the
app.

.. autoclass:: MainWindow
"""

import os
import gc
import platform
import requests
import subprocess
import pkg_resources
import warnings
from packaging import version

import quantities as pq
import neo
from ephyviewer import QT, QT_MODE

from .. import __version__, _elephant_tools, global_config, global_config_file, default_log_level, log_file, gdrive_downloader
from ..datasets import MetadataSelector, load_dataset
from ..datasets.metadata import _selector_labels
from ..gui.config import EphyviewerConfigurator, available_themes, available_ui_scales

import logging
logger = logging.getLogger(__name__)

# suppress warning that gdrive token file does not exist
warnings.filterwarnings('ignore', message='Cannot access .*', module='oauth2client')


def open_path_with_default_program(path):
    """
    Open a directory or file with its default program.
    """

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def open_url(url):
    """
    Open a URL in a browser.
    """

    QT.QDesktopServices.openUrl(QT.QUrl(url))

def get_versioned_docs_url():
    """
    Get the URL for the docs that best fits the package version.
    """

    url = 'https://neurotic.readthedocs.io/en/'
    if version.parse(__version__).is_devrelease:
        url += 'latest'
    else:
        url += version.parse(__version__).base_version
    return url

class MainWindow(QT.QMainWindow):
    """
    The main window of the app.
    """

    request_download = QT.pyqtSignal()
    request_load_dataset = QT.pyqtSignal()
    request_gdrive_authorization = QT.pyqtSignal()
    request_check_for_updates = QT.pyqtSignal(bool)

    def __init__(self, file=None, initial_selection=None, lazy=True, theme='light', ui_scale='medium', support_increased_line_width=False, show_datetime=False):
        """
        Initialize a new MainWindow.
        """

        QT.QMainWindow.__init__(self)

        self.setWindowIcon(QT.QIcon(':/neurotic-logo-150.png'))

        self.setWindowTitle('neurotic')
        self.resize(600, 300)
        self.statusBar()

        # lazy loading using Neo RawIO
        self.lazy = lazy

        if theme not in available_themes:
            logger.error(f'theme "{theme}" is unrecognized')
            raise ValueError(f'theme "{theme}" is unrecognized')
        self.theme = theme

        if ui_scale not in available_ui_scales:
            logger.error(f'ui scale "{ui_scale}" is unrecognized')
            raise ValueError(f'ui scale "{ui_scale}" is unrecognized')
        self.ui_scale = ui_scale
        self.default_font_size = QT.QFont().pointSize()

        # support_increased_line_width=True eliminates the extremely poor
        # performance associated with TraceViewer's line_width > 1.0, but it
        # also degrades overall performance somewhat and uses a mode of
        # pyqtgraph that is reportedly unstable
        self.support_increased_line_width = support_increased_line_width

        # show_datetime=True will display the real-world date and time next to
        # the in-file time, but this may be inaccurate for several reasons,
        # e.g. if data acquisition was paused and continued after some delay or
        # if an AxoGraph chart was not started immediately after creation
        self.show_datetime = show_datetime

        # windows are appended to this list so that they persist after the
        # function that spawned them returns
        self.windows = []

        # metadata selector
        self.metadata_selector = _MetadataSelectorQt(self)

        # loading label
        self.loading_label = QT.QLabel('Launching, please wait...')
        self.loading_label.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Sunken)
        self.loading_label.setAlignment(QT.Qt.AlignCenter)

        # gdrive auth flow label
        self.gdrive_auth_label = QT.QLabel('Continue Google Drive authorization\nin your web browser')
        self.gdrive_auth_label.setFrameStyle(QT.QFrame.Panel | QT.QFrame.Sunken)
        self.gdrive_auth_label.setAlignment(QT.Qt.AlignCenter)

        # initially stack the metadata selector above the loading label
        self.stacked_layout = QT.QStackedLayout()
        self.stacked_layout.addWidget(self.metadata_selector)  # index 0
        self.stacked_layout.addWidget(self.loading_label)      # index 1
        self.stacked_layout.addWidget(self.gdrive_auth_label)  # index 2
        central_widget = QT.QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

        # create a worker thread for network activity (e.g., downloading data)
        self.network_thread = QT.QThread()
        self.network_worker = _NetworkWorker(self)
        self.network_worker.moveToThread(self.network_thread)

        # set up the network thread to perform data downloads
        self.request_download.connect(self.network_worker.download)
        self.network_worker.download_finished.connect(self.on_download_finished)

        # set up the network thread to perform checks for updates
        self.request_check_for_updates.connect(self.network_worker.get_latest_release_number)
        self.network_worker.version_check_finished.connect(self.on_version_check_finished)

        # set up the network thread to run the Google Drive authorization flow
        self.request_gdrive_authorization.connect(self.network_worker.authorize_gdrive)
        self.network_worker.gdrive_authorization_finished.connect(self.on_gdrive_authorization_finished)

        # create a worker thread for loading datasets
        self.load_dataset_thread = QT.QThread()
        self.load_dataset_worker = _LoadDatasetWorker(self)
        self.load_dataset_worker.moveToThread(self.load_dataset_thread)
        self.request_load_dataset.connect(self.load_dataset_worker.load_dataset)
        self.load_dataset_worker.load_dataset_finished.connect(self.on_load_dataset_finished)
        self.load_dataset_worker.show_status_msg.connect(self.statusBar().showMessage)
        self.blk = None

        # construct the menus
        self.create_menus()

        # open metadata file
        if file:
            # try the user-specified file
            self.metadata_selector.file = file
            self.metadata_selector.load()
        if self.metadata_selector.all_metadata is None:
            # use an example metadata file if the user-specified file failed to
            # load or one was not provided
            self.metadata_selector.file = pkg_resources.resource_filename('neurotic', 'example/metadata.yml')
            self.metadata_selector.load()

        # select a dataset if the user provided one
        if initial_selection:
            try:
                self.metadata_selector.setCurrentRow(list(self.metadata_selector.all_metadata).index(initial_selection))
            except (TypeError, ValueError) as e:
                logger.error(f'Bad dataset key, will ignore: {e}')
                self.statusBar().showMessage('ERROR: Bad dataset key, will '
                                             'ignore', msecs=5000)

    def showEvent(self, event):
        """
        Executed when the window is shown.
        """
        QT.QMainWindow.showEvent(self, event)

        if global_config['app']['auto_check_for_updates']:
            self.check_for_updates(show_new_only=True)

    def create_menus(self):
        """
        Construct the menus of the app.
        """

        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)  # disable for macOS, see GH-239

        file_menu = self.menu_bar.addMenu(self.tr('&File'))

        do_open_metadata = file_menu.addAction('&Open metadata')
        do_open_metadata.setShortcut('Ctrl+O')
        do_open_metadata.setStatusTip('Open a YAML file containing dataset '
                                      'configurations')
        do_open_metadata.triggered.connect(self.open_metadata)

        do_edit_metadata = file_menu.addAction('&Edit metadata')
        do_edit_metadata.setStatusTip('Tip: Remember to reload metadata after '
                                      'saving changes')
        do_edit_metadata.setShortcut('Ctrl+E')
        do_edit_metadata.triggered.connect(self.edit_metadata)

        do_reload_metadata = file_menu.addAction('&Reload metadata')
        do_reload_metadata.setStatusTip('Reload the metadata file that is '
                                        'currently open (use after making '
                                        'changes)')
        do_reload_metadata.setShortcut('Ctrl+R')
        do_reload_metadata.triggered.connect(self.metadata_selector.load)

        file_menu.addSeparator()

        self.do_download_data = file_menu.addAction('&Download data')
        self.do_download_data.setShortcut('Ctrl+D')
        self.do_download_data.triggered.connect(self.download_files)

        do_open_directory = file_menu.addAction('Open data &folder')
        do_open_directory.setShortcut('Ctrl+F')
        do_open_directory.triggered.connect(self.open_directory)

        self.do_launch = file_menu.addAction('&Launch')
        self.do_launch.setShortcut('Return')
        self.do_launch.triggered.connect(self.start_launch)

        options_menu = self.menu_bar.addMenu(self.tr('&Options'))

        do_toggle_lazy = options_menu.addAction('&Fast loading')
        do_toggle_lazy.setStatusTip('Reduces load time and memory usage, disables expensive features like spike detection')
        do_toggle_lazy.setCheckable(True)
        do_toggle_lazy.setChecked(self.lazy)
        do_toggle_lazy.triggered.connect(self.toggle_lazy)

        do_toggle_show_datetime = options_menu.addAction('&Display date and time')
        do_toggle_show_datetime.setStatusTip('May be inaccurate for some data files unless manually set with rec_datetime')
        do_toggle_show_datetime.setCheckable(True)
        do_toggle_show_datetime.setChecked(self.show_datetime)
        do_toggle_show_datetime.triggered.connect(self.toggle_show_datetime)

        options_menu.addSeparator()

        do_view_global_config_file = options_menu.addAction('View global &config file')
        do_view_global_config_file.triggered.connect(self.view_global_config_file)

        appearance_menu = self.menu_bar.addMenu(self.tr('&Appearance'))

        ui_scale_group = QT.QActionGroup(appearance_menu)
        ui_scale_actions = {}
        for size in available_ui_scales:
            ui_scale_actions[size] = appearance_menu.addAction(f'&{size.capitalize()} scale')
            ui_scale_actions[size].setCheckable(True)
            ui_scale_actions[size].triggered.connect(lambda checked, size=size: self.set_ui_scale(size))
            ui_scale_group.addAction(ui_scale_actions[size])
        ui_scale_actions[self.ui_scale].setChecked(True)
        self.set_ui_scale(self.ui_scale)  # adjust the UI scale now

        appearance_menu.addSeparator()

        theme_group = QT.QActionGroup(appearance_menu)
        theme_actions = {}
        for theme in available_themes:
            theme_actions[theme] = appearance_menu.addAction(f'&{theme.capitalize()} theme')
            theme_actions[theme].setCheckable(True)
            theme_actions[theme].triggered.connect(lambda checked, theme=theme: self.set_theme(theme))
            theme_group.addAction(theme_actions[theme])
        theme_actions[self.theme].setChecked(True)

        appearance_menu.addSeparator()

        do_toggle_support_increased_line_width = appearance_menu.addAction('&Thick traces')
        do_toggle_support_increased_line_width.setStatusTip('Thickens signal traces at the cost of reduced performance')
        do_toggle_support_increased_line_width.setCheckable(True)
        do_toggle_support_increased_line_width.setChecked(self.support_increased_line_width)
        do_toggle_support_increased_line_width.triggered.connect(self.toggle_support_increased_line_width)

        help_menu = self.menu_bar.addMenu(self.tr('&Help'))

        self.do_toggle_debug_logging = help_menu.addAction('Show and log &debug messages')
        self.do_toggle_debug_logging.setCheckable(True)
        self.do_toggle_debug_logging.setChecked(logger.parent.level == logging.DEBUG)
        self.do_toggle_debug_logging.triggered.connect(self.toggle_debug_logging)

        do_view_log_file = help_menu.addAction('View &log file')
        do_view_log_file.triggered.connect(self.view_log_file)

        do_open_issues = help_menu.addAction('Report issues')
        do_open_issues.triggered.connect(lambda: open_url('https://github.com/jpgill86/neurotic/issues'))

        help_menu.addSeparator()

        do_open_gdrive_creds_dir = help_menu.addAction('Open Google Drive credentials directory')
        do_open_gdrive_creds_dir.triggered.connect(self.open_gdrive_creds_dir)

        self.do_authorize_gdrive = help_menu.addAction('Request Google Drive authorization now')
        self.do_authorize_gdrive.triggered.connect(self.authorize_gdrive)

        do_deauthorize_gdrive = help_menu.addAction('Purge Google Drive authorization token')
        do_deauthorize_gdrive.triggered.connect(self.deauthorize_gdrive)

        help_menu.addSeparator()

        do_check_for_updates = help_menu.addAction('Check for updates')
        do_check_for_updates.triggered.connect(self.check_for_updates)

        do_open_update_docs = help_menu.addAction('How to update')
        do_open_update_docs.triggered.connect(lambda: open_url('https://neurotic.readthedocs.io/en/latest/update.html'))

        do_open_release_notes = help_menu.addAction('Release notes')
        do_open_release_notes.triggered.connect(lambda: open_url('https://neurotic.readthedocs.io/en/latest/releasenotes.html'))

        help_menu.addSeparator()

        do_open_docs = help_menu.addAction('Documentation')
        do_open_docs.triggered.connect(lambda: open_url(get_versioned_docs_url()))

        do_open_ui_guide = help_menu.addAction('User interface guide')
        do_open_ui_guide.triggered.connect(lambda: open_url('https://ephyviewer.readthedocs.io/en/latest/interface.html'))

        do_show_about = help_menu.addAction('&About neurotic')
        do_show_about.triggered.connect(self.show_about)

    def open_metadata(self):
        """
        Open and load a metadata file.
        """

        file, _ = QT.QFileDialog.getOpenFileName(
            parent=self,
            caption='Open metadata',
            directory=None,
            filter='YAML files (*.yml *.yaml)')

        if file:
            self.metadata_selector.file = file
            self.metadata_selector.load()

    def edit_metadata(self):
        """
        Open the metadata file in an editor.
        """

        try:
            open_path_with_default_program(self.metadata_selector.file)

            title = 'Reload metadata?'
            text = 'The metadata file must be reloaded if you made changes. ' \
                   'Do you want to reload now?'
            button = QT.QMessageBox.question(self, title, text,
                                             defaultButton=QT.QMessageBox.Yes)
            if button == QT.QMessageBox.Yes:
                self.metadata_selector.load()

        except FileNotFoundError as e:

            logger.error(f'The metadata file was not found: {e}')
            self.statusBar().showMessage('ERROR: The metadata file could not '
                                         'be found', msecs=5000)

    def download_files(self):
        """
        Download all files for the selected dataset in a separate thread.
        """

        self.network_thread.start()
        self.request_download.emit()
        self.do_download_data.setText('&Download in progress!')
        self.do_download_data.setEnabled(False)
        self.statusBar().showMessage('Starting downloads (see console window)',
                                     msecs=5000)

    def on_download_finished(self, success):
        """
        Cleanup network thread and reload the metadata list content to update
        file indicators.
        """

        self.network_thread.quit()
        self.metadata_selector.load()
        self.do_download_data.setText('&Download data')
        self.do_download_data.setEnabled(True)

        if success:
            self.statusBar().showMessage('Downloads complete', msecs=5000)
        else:
            self.statusBar().showMessage('ERROR: Download failed (see console '
                                         'for details)', msecs=5000)

    def open_directory(self):
        """
        Open the directory of the selected dataset in Win Explorer / Mac
        Finder.
        """

        try:
            open_path_with_default_program(self.metadata_selector['data_dir'])
        except FileNotFoundError as e:
            logger.error('The directory for the selected dataset was not '
                         'found locally, perhaps because it does not exist '
                         f'yet: {e}')
            self.statusBar().showMessage('ERROR: Folder not found locally '
                                         '(need to download?)', msecs=5000)

    def start_launch(self):
        """
        Load data for the selected dataset in a separate thread.
        """

        self.menu_bar.setEnabled(False)
        self.metadata_selector.setEnabled(False)
        self.stacked_layout.setCurrentIndex(1)  # show loading label
        self.load_dataset_thread.start()
        self.request_load_dataset.emit()

    def on_load_dataset_finished(self):
        """
        Launch the ephyviewer window after loading the dataset.
        """

        self.load_dataset_thread.quit()

        try:

            if self.blk is None:
                pass

            elif not isinstance(self.blk, neo.Block):
                raise ValueError('blk must be a Neo Block but instead is '
                                 f'{self.blk}')

            else:
                metadata = self.metadata_selector.selected_metadata
                ephyviewer_config = EphyviewerConfigurator(metadata, self.blk, self.lazy)
                ephyviewer_config.show_all()

                win = ephyviewer_config.create_ephyviewer_window(theme=self.theme, ui_scale=self.ui_scale, support_increased_line_width=self.support_increased_line_width, show_datetime=self.show_datetime)
                self.windows.append(win)
                win.destroyed.connect(lambda qobject, i=len(self.windows)-1: self.free_resources(i))
                win.show()

        except FileNotFoundError as e:

            logger.error('Some files were not found locally and may need to '
                         f'be downloaded: {e}')
            self.statusBar().showMessage('ERROR: Launch failed because some '
                                         'files are missing (need to '
                                         'download?)', msecs=5000)

        except Exception:

            logger.exception('Encountered a fatal error. Traceback will be '
                             'written to log file.')
            self.statusBar().showMessage('ERROR: Launch failed (see console '
                                         'for details)', msecs=5000)

        finally:

            self.menu_bar.setEnabled(True)
            self.metadata_selector.setEnabled(True)
            self.stacked_layout.setCurrentIndex(0)  # show metadata selector

    def view_global_config_file(self):
        """
        Open the global config file in an editor.
        """

        try:
            open_path_with_default_program(global_config_file)
        except FileNotFoundError as e:
            logger.error(f'The global config file was not found: {e}')
            self.statusBar().showMessage('ERROR: The global config file could '
                                         'not be found', msecs=5000)
            return

    def toggle_debug_logging(self, checked):
        """
        Toggle log filtering level between its original level and debug mode
        """
        if checked:
            logger.parent.setLevel(logging.DEBUG)
            logger.debug('Debug messages enabled')

            # lower the threshold for PyAV messages printed to the console from
            # critical to warning
            logging.getLogger('libav').setLevel(logging.WARNING)

        else:
            logger.debug('Disabling debug messages')
            logger.parent.setLevel(default_log_level)

            # raise the threshold for PyAV messages printed to the console from
            # warning to critical
            logging.getLogger('libav').setLevel(logging.CRITICAL)

    def view_log_file(self):
        """
        Open the log file in an editor.
        """

        try:
            open_path_with_default_program(log_file)
        except FileNotFoundError as e:
            logger.error(f'The log file was not found: {e}')
            self.statusBar().showMessage('ERROR: The log file could not be '
                                         'found', msecs=5000)

    def open_gdrive_creds_dir(self):
        """
        Open the Google Drive credentials directory.
        """

        gdrive_creds_dir = os.path.dirname(global_config['gdrive']['client_secret_file'])
        try:
            open_path_with_default_program(gdrive_creds_dir)
        except FileNotFoundError as e:
            logger.error(f'Could not open Google Drive credentials directory: '
                         f'{e}')
            self.statusBar().showMessage('ERROR: Could not open Google Drive '
                                         'credentials directory', msecs=5000)

    def authorize_gdrive(self):
        """
        Trigger the Google Drive authorization flow if necessary.
        """
        if gdrive_downloader.is_authorized() or os.path.exists(global_config['gdrive']['tokens_file']):
            # already authorized
            logger.info('Already authorized to access Google Drive for '
                        f'{gdrive_downloader.GetUserEmail()}')
            self.statusBar().showMessage('Google Drive authorization already '
                                         'complete for '
                                         f'{gdrive_downloader.GetUserEmail()}',
                                         msecs=5000)

        elif not os.path.exists(global_config['gdrive']['client_secret_file']):
            # missing client secret file
            logger.error('Google Drive authorization could not begin due to '
                         'missing client secret file')
            self.statusBar().showMessage('ERROR: Missing client secret file',
                                         msecs=5000)

        else:
            title = 'Continue with authorization?'
            text = 'Completing this process will allow <i>neurotic</i> to ' \
                   'download files from your Google Drive. A web browser ' \
                   'will open so that you can log into your Google account ' \
                   'and accept the request for permissions. You will not be ' \
                   'able to use <i>neurotic</i> until this process finishes.' \
                   '<br/><br/>Do you want to continue?'
            button = QT.QMessageBox.question(self, title, text,
                                             defaultButton=QT.QMessageBox.Yes)
            if button == QT.QMessageBox.Yes:
                self.menu_bar.setEnabled(False)
                self.metadata_selector.setEnabled(False)
                self.stacked_layout.setCurrentIndex(2)  # show gdrive auth label
                self.network_thread.start()
                self.request_gdrive_authorization.emit()

    def on_gdrive_authorization_finished(self, success):
        """
        Cleanup network thread and display success or failute of Google Drive
        authorization flow.
        """
        self.network_thread.quit()
        if success:
            self.statusBar().showMessage('Authorization successful',
                                         msecs=5000)
        else:
            self.statusBar().showMessage('ERROR: Authorization failed '
                                         '(see console for details)',
                                         msecs=5000)
        self.menu_bar.setEnabled(True)
        self.metadata_selector.setEnabled(True)
        self.stacked_layout.setCurrentIndex(0)  # show metadata selector

    def deauthorize_gdrive(self):
        """
        Forget Google Drive access tokens and delete the token file.
        """
        gdrive_downloader.deauthorize()
        logger.info(f'Purged Google Drive authorization token')
        self.statusBar().showMessage('Purged Google Drive authorization token',
                                     msecs=5000)

    def check_for_updates(self, *args, show_new_only=False):
        """
        Check for new releases in a separate thread.
        """

        self.network_thread.start()
        self.request_check_for_updates.emit(show_new_only)

    def on_version_check_finished(self, latest_release, show_new_only):
        """
        Cleanup network thread and display a dialog window showing the state of
        available updates.
        """
        self.network_thread.quit()

        urls = {}
        urls['globalconfig'] = 'https://neurotic.readthedocs.io/en/latest/globalconfig.html'
        urls['releases'] = 'https://github.com/jpgill86/neurotic/releases'
        urls['updating'] = 'https://neurotic.readthedocs.io/en/latest/update.html'

        if latest_release:
            if version.parse(latest_release) > version.parse(__version__):
                text = f"""
                <h2>A new version is available</h2>

                <p><table>
                <tr><td>Installed version:</td>  <td>{__version__}</td></tr>
                <tr><td>Latest version:</td>     <td>{latest_release}</td></tr>
                </table></p>

                <p><a href='{urls['updating']}'>How do I update <i>neurotic</i>?</a></p>

                <p>Automatically check for updates at launch: {'Yes' if global_config['app']['auto_check_for_updates'] else 'No'}<br/>
                <a href='{urls['globalconfig']}'>Learn how to change this</a></p>
                """
                title = 'Check for updates'
                return QT.QMessageBox.about(self, title, text)

            elif not show_new_only:
                # display up to date
                text = f"""
                <h2>neurotic is up to date</h2>

                <p><table>
                <tr><td>Installed version:</td>  <td>{__version__}</td></tr>
                <tr><td>Latest version:</td>     <td>{latest_release}</td></tr>
                </table></p>

                <p>Automatically check for updates at launch: {'Yes' if global_config['app']['auto_check_for_updates'] else 'No'}<br/>
                <a href='{urls['globalconfig']}'>Learn how to change this</a></p>
                """
                title = 'Check for updates'
                return QT.QMessageBox.about(self, title, text)

        elif not show_new_only:
            # display failure message
            text = f"""
            <h2>Could not detect latest version</h2>

            <p><table>
            <tr><td>Installed version:</td>  <td>{__version__}</td></tr>
            <tr><td>Latest version:</td>     <td>unknown</td></tr>
            </table></p>

            <p><a href='{urls['releases']}'>Check for latest version manually</a></p>

            <p><a href='{urls['updating']}'>How do I update <i>neurotic</i>?</a></p>

            <p>Automatically check for updates at launch: {'Yes' if global_config['app']['auto_check_for_updates'] else 'No'}<br/>
            <a href='{urls['globalconfig']}'>Learn how to change this</a></p>
            """
            title = 'Check for updates'
            return QT.QMessageBox.about(self, title, text)

    def show_about(self):
        """
        Display the "About neurotic" message box.
        """

        import platform
        import ephyviewer
        import numpy
        import pyqtgraph
        try:
            pyqt_version = QT.PYQT_VERSION_STR
        except AttributeError:
            pyqt_version = 'unknown'

        title = 'About neurotic'

        urls = {}
        urls['GitHub'] = 'https://github.com/jpgill86/neurotic'
        urls['GitHub user'] = 'https://github.com/jpgill86'
        urls['PyPI'] = 'https://pypi.org/project/neurotic'

        gdrive_creds_dir = os.path.dirname(global_config['gdrive']['client_secret_file'])

        text = f"""
        <h2><i>neurotic</i> {__version__}</h2>

        <p><b>NEUROscience Tool for Interactive Characterization</b></p>

        <p><i>Curate, visualize, annotate, and share <br/>
        your behavioral ephys data using Python</i></p>

        <p>Author: Jeffrey Gill (<a href='{urls['GitHub user']}'>@jpgill86</a>)</p>

        <p>Websites: <a href='{urls['GitHub']}'>GitHub</a>
                   | <a href='{urls['PyPI']}'>PyPI</a></p>

        <p>Installed dependencies:</p>
        <table width='80%' align='center'>
        <tr><td>ephyviewer</td>         <td>{ephyviewer.__version__}</td></tr>
        <tr><td>neo</td>                <td>{neo.__version__}</td></tr>
        <tr><td>numpy</td>              <td>{numpy.__version__}</td></tr>
        <tr><td>{QT_MODE.lower()}</td>  <td>{pyqt_version}</td></tr>
        <tr><td>pyqtgraph</td>          <td>{pyqtgraph.__version__}</td></tr>
        <tr><td>python</td>             <td>{platform.python_version()}</td></tr>
        </table>

        <p>Install path: <code>{os.path.dirname(os.path.dirname(__file__))}</code></p>

        <p>Google Drive credentials directory: <code>{gdrive_creds_dir}</code></p>
        """

        QT.QMessageBox.about(self, title, text)

    def toggle_lazy(self, checked):
        self.lazy = checked

    def toggle_show_datetime(self, checked):
        self.show_datetime = checked

    def set_ui_scale(self, size):
        self.ui_scale = size

        font_size = {
            'tiny':   self.default_font_size-4,
            'small':  self.default_font_size-2,
            'medium': self.default_font_size,
            'large':  self.default_font_size+4,
            'huge':   self.default_font_size+8,
        }

        font = self.font()
        font.setPointSize(font_size[size])
        self.setFont(font)

        font = self.loading_label.font()
        font.setPointSize(font_size[size]+4)
        self.loading_label.setFont(font)

        font = self.gdrive_auth_label.font()
        font.setPointSize(font_size[size]+4)
        self.gdrive_auth_label.setFont(font)

    def set_theme(self, theme):
        self.theme = theme

    def toggle_support_increased_line_width(self, checked):
        self.support_increased_line_width = checked

    def free_resources(self, i):
        """
        Run garbage collection to unlock files and free memory for the closed
        window with index ``i``.

        Data files opened by Neo in lazy mode remain locked for as long as the
        RawIO objects pointing to them exist in memory. Normally such objects
        would be automatically garbage collected when they go out of scope,
        i.e., when the window that created them is closed. However, due to an
        issue in Neo, circular references to these objects are always created,
        so they persist even after the window is closed. This function performs
        a manual garbage collection after a window has been closed to clean up
        any lingering Neo objects that keep files locked. For more info about
        the issue, see https://github.com/NeuralEnsemble/python-neo/issues/684.
        """

        # first remove the last remaining references to the closed window and
        # Neo Block
        self.windows[i] = None
        self.blk = None

        # run garbage collection
        gc.collect()


class _MetadataSelectorQt(MetadataSelector, QT.QListWidget):
    """
    A QListWidget that displays the state of a MetadataSelector.
    """

    def __init__(self, mainwindow):
        """
        Initialize a new _MetadataSelectorQt.
        """

        MetadataSelector.__init__(self)
        QT.QListWidget.__init__(self, parent=mainwindow)

        self.mainwindow = mainwindow

        self.setSelectionMode(QT.QListWidget.SingleSelection)

        font = self.font()
        font.setFamily('Courier')
        self.setFont(font)

        self.currentRowChanged.connect(self._on_select)
        self.itemDoubleClicked.connect(self.mainwindow.start_launch)

    def _on_select(self, currentRow):
        """
        Update the MetadataSelector's selection after changing the
        QListWidget's selection.
        """

        if currentRow >= 0:
            self._selection = list(self.all_metadata)[currentRow]
        else:
            self._selection = None

    def load(self):
        """
        Load or reload the metadata file and populate the QListWidget.
        """

        # remember the current selection
        old_selection = self._selection

        try:
            MetadataSelector.load(self)
        except Exception as e:
            logger.error(f'Bad metadata file\n{e}')
            self.mainwindow.statusBar().showMessage('ERROR: Bad metadata file '
                                                    '(see console for '
                                                    'details)', msecs=5000)

        if self.all_metadata is not None:

            # clear and repopulate the list,
            # which triggers the selection to change
            self.clear()
            for label in _selector_labels(self.all_metadata):
                QT.QListWidgetItem(label, self)

            if old_selection in self.all_metadata:
                # reselect the original selection if it still exists
                self.setCurrentRow(list(self.all_metadata).index(old_selection))
            else:
                # otherwise select the first item
                self.setCurrentRow(0)


class _NetworkWorker(QT.QObject):
    """
    A thread worker for for network activity (e.g., downloading data)
    """

    download_finished = QT.pyqtSignal(bool)
    gdrive_authorization_finished = QT.pyqtSignal(bool)
    version_check_finished = QT.pyqtSignal(str, bool)

    def __init__(self, mainwindow):
        """
        Initialize a new _NetworkWorker.
        """

        QT.QObject.__init__(self)

        self.mainwindow = mainwindow

    def download(self):
        """
        Download all files and emit a signal when complete.
        """

        success = False
        try:
            self.mainwindow.metadata_selector.download_all_data_files()
            success = True
        except:
            pass
        finally:
            self.download_finished.emit(success)

    def authorize_gdrive(self):
        success = False
        try:
            logger.info('Initiating Google Drive authorization flow')
            gdrive_downloader.authorize()
            success = True
            logger.info('Authorization successful')
        except Exception as e:
            logger.error(f'Problem during authorization: {e}')
        finally:
            self.gdrive_authorization_finished.emit(success)

    def get_latest_release_number(self, show_new_only):
        """
        Query GitHub for the version number of the latest release and emit a
        signal when complete.
        """

        latest_release = None
        try:
            # query GitHub for the latest release
            logger.debug('Checking for new release versions of neurotic')
            url = 'https://api.github.com/repos/jpgill86/neurotic/releases/latest'
            r = requests.get(url)
            latest_release = r.json()['tag_name']
            logger.debug(f'Found latest release version: {latest_release}')
        except Exception as e:
            # something went wrong with the query
            logger.error(f'Query for latest release version failed: {e}')
        finally:
            self.version_check_finished.emit(latest_release, show_new_only)


class _LoadDatasetWorker(QT.QObject):
    """
    A thread worker for loading data sets.
    """

    load_dataset_finished = QT.pyqtSignal()
    show_status_msg = QT.pyqtSignal(str, int)

    def __init__(self, mainwindow):
        """
        Initialize a new _LoadDatasetWorker.
        """

        QT.QObject.__init__(self)

        self.mainwindow = mainwindow

    def load_dataset(self):
        """
        Load the selected dataset.
        """

        metadata = self.mainwindow.metadata_selector.selected_metadata
        lazy = self.mainwindow.lazy

        try:

            self.mainwindow.blk = load_dataset(metadata, lazy=lazy)

        except FileNotFoundError as e:

            logger.error('Some files were not found locally and may need to '
                         f'be downloaded: {e}')
            self.show_status_msg.emit('ERROR: Launch failed because some '
                                      'files are missing (need to download?)',
                                      5000)
            self.mainwindow.blk = None

        except Exception:

            logger.exception('Encountered a fatal error. Traceback will be '
                             'written to log file.')
            self.show_status_msg.emit('ERROR: Launch failed (see console for '
                                      'details)', 5000)
            self.mainwindow.blk = None

        finally:

            self.load_dataset_finished.emit()
