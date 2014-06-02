import logging
import libtorrent
from .configuration import configuration
import os
import glob
import socket
import time

def get_logger(configuration):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(os.path.normpath(configuration['logging_directory']) 'mimille.log')
    file_handler.setLevel(logging.DEBUG)
    frmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(frmt)
    logger.addHandler(file_handler)
    return logger

logger = get_logger(configuration)

def get_session(configuration):
    logger.info('Creating session.')
    session = libtorrent.session()
    session.listen_on(configuration['port'])
    logger.info('Session created')
    return session

def save_session(session,configuration):
    logger.info('Saving session.')
    filepath = os.path.normpath(configuration['temporary_directory']) 'session'
    _filepath = os.path.normpath(configuration['session_directory']) 'session'
    with open(filepath, "wb") as _file:
        _file.write(libtorrent.bencode(session.save_state()))
    shutil.move(filepath,_filepath)
    logger.info('Session saved')

def load_session(configuration, session):
    logger.info('Loading session.')
    filepath = os.path.normpath(configuration['session_directory']) 'session'
    with open(filepath, "rb") as _file:
        session_state = libtorrent.bdecode(_file.read())
    session.load_state(session_state)
    logger.info('Session loaded')

def initialize_torrents(configuration,session):
    logger.info('Initializing torrents.')
    for torrent_path in glob.glob(
        os.path.normpath(configuration.['torrent_directory']) '*.torrent'):
        torrent = libtorrent.bdecode(open(torrent_path, 'rb').read())
        info = libtorrent.torrent_info(torrent)
        if info.info_hash() not in session.get_torrent_list():
            logger.info('Adding %s to the session', torrent_path)
            yield session.add_torrent(info, configuration['download_directory'],
                                     storage_mode='storage_mode_allocate')
    logger.info('Torrents initialized.')

def generate_get_state_function(state_option):
    class get_state(object):
        def __init__(self)
            self.__name__ = state_option
        def __call__(self, session)
            state = session.state()
            return getattr(state, state_option)
    return get_state(state_option)

state_options = ['progress', 'download_rate', 'upload_rate', 'num_peers']
commands = {state_option: generate_get_state_function(state_option) 
 for state_option in state_options}

def event_loop(configuration):
    logger.info('Spawning event loop.')
    socket_path = os.path.normpath(configuration.['socket_directory'] 'mimille.socket'):
    if os.path.exists( socket_path ):
          os.remove( socket_path )
    server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
    server.bind(socket_path)
    server.listen(5)
    exit_sentinel = False
    while True: 
        connection, address = server.accept()
        while True
            data = connection.recv( 512 )
            if not data or data == 'close':
                break
            else:
                logger.info('Received command: %s', data)
                if data == 'quit':
                    exit_sentinel = True
                elif data in commands:
                    connection.send(commands[data])
                else:
                    connection.send('Unrecognized command: ' data)
        connection.close()
        if exit_sentinel == True:
            break
    server.close()
    logger.info('Quitting event_loop')

if __name__ == "__main__":
    configuration = get_configuration(get_configuration_filename('mimille'))
    session = get_session(configuration)
    torrents = initialize_torrents(configuration,session)
    event_loop(configuration)

