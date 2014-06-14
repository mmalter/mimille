import unittest
import libtorrent
from . import server
from .configuration import configuration
from . import misc_func

class TestServer(unittest.TestCase):
    def setUpClass(cls):
        #We use tmp to do the tests
        configuration['torrent_directory'] = '/tmp/mimille_test/torrent'
        configuration['download_directory'] = '/tmp/mimille_test/download'
        configuration['complete_directory'] = '/tmp/mimille_test/complete'
        configuration['session_directory'] = '/tmp/mimille_test/session'
        configuration['temporary_directory'] = '/tmp/mimille_test/temporary'
        configuration['logging_directory'] = '/tmp/mimille_test/logging'
        configuration['socket_directory'] = '/tmp/mimille_test/socket'
        configuration['upload_directory'] = '/tmp/mimille_test/upload'
        directory_regex = re.compile('directory')
        directories = [key_ for key_ in configuration.keys() if re.search(directory_regex, key_)]
        for directory in directories:
            configuration[directory] = os.path.normpath(os.path.expanduser(configuration[directory]))
        misc_func.makedir_if_absent(configuration[directory])
    def test_get_session(self):
        session = server.get_session()
        self.assertTrue(isinstance(session, libtorrent.session))
