import libtorrent
import configobj
import validate
import os
import glob
import socket
import time

#Use asyncio to communicate

def get_filename(appname):
    """Return the configuration file path."""
    if os.name == 'posix':
        if os.path.isfile(os.environ["HOME"]+'/.'+appname):
            return os.environ["HOME"]+'/.'+appname
        elif os.path.isfile('/etc/'+appname):
            return '/etc/'+appname
        else:
            raise FileNotFoundError('No configuration file found.')
    elif os.name == 'mac':
        return ("%s/Library/Application Support/%s" % (os.environ["HOME"], appname))
    elif os.name == 'nt':
        return ("%s\Application Data\%s" % (os.environ["HOMEPATH"], appname))
    else:
        raise UnsupportedOSError(os.name)

def get_configuration(configuration_filename):
    _configspec = """
    port = integer()
    torrent_directory = string()
    download_directory = string()
    complete_directory = string()
    session_directory = string()
    temporary_directory = string()
    socket_directory = string()
    upload_download_ratio = int()"""
    configuration = configobj.ConfigObj(configuration_filename,
                                        configspec=_configspec.split('\n'))
    validator = validate.Validator()
    configuration.validate(validator, copy=True)
    return configuration.dict()

def get_session(configuration):
    session = libtorrent.session()
    session.listen_on(configuration['port'])
    return session

def save_session(session,configuration):
    filepath = os.path.normpath(configuration['temporary_directory']) 'session'
    _filepath = os.path.normpath(configuration['session_directory']) 'session'
    with open(filepath, "wb") as _file:
        _file.write(libtorrent.bencode(session.save_state()))
    shutil.move(filepath,_filepath)

def load_session(configuration, session):
    filepath = os.path.normpath(configuration['session_directory']) 'session'
    with open(filepath, "rb") as _file:
        session_state = libtorrent.bdecode(_file.read())
    session.load_state(session_state)

def initialize_torrents(configuration,session):
    for torrent_path in glob.glob(
        os.path.normpath(configuration.['torrent_directory']) '*.torrent'):
        torrent = libtorrent.bdecode(open(torrent_path, 'rb').read())
        info = libtorrent.torrent_info(torrent)
        if info.info_hash() not in session.get_torrent_list():
            yield session.add_torrent(info, configuration['download_directory'],
                                     storage_mode='storage_mode_allocate')

def event_loop(configuration):
    socket_path = os.path.normpath(configuration.['socket_directory'] '.socket'):
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
    configuration = get_configuration(get_configuration_filename('mtorrent'))
    session = get_session(configuration)
    torrents = initialize_torrents(configuration,session)
    event_loop(configuration)

