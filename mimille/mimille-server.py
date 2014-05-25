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

def event_loop(configuration):
    socket_path = os.path.normpath(configuration.['socket_directory'] 'mimille.socket'):
    if os.path.exists( socket_path ):
          os.remove( socket_path )
    server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
    server.bind(socket_path)
    server.listen(5)
    while True:
        connection, address = server.accept()
        while True: 
            data = connection.recv( 512 )
            if not data:
                break
            else:
                print data
                break

if __name__ == "__main__":
    configuration = get_configuration(get_configuration_filename('mimille'))
    session = get_session(configuration)
    torrents = initialize_torrents(configuration,session)
    event_loop(configuration)

