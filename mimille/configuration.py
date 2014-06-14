import configobj
import validate
import os
import re

def get_configuration_filename(appname):
    """Return the configuration file path."""
    if os.name == 'posix':
        if os.path.isfile(os.environ["HOME"]+'/.'+appname):
            return os.environ["HOME"]+'/.'+appname
        elif os.path.isfile('/etc/'+appname):
            return '/etc/'+appname
        else:
            raise FileNotFoundError('No configuration file found.')
    elif os.name == 'mac':
        if os.path.isfile("%s/Library/Application Support/%s" % (os.environ["HOME"], appname)):
            return ("%s/Library/Application Support/%s" % (os.environ["HOME"], appname))
        elif os.path.isfile('/etc/'+appname):
            return '/etc/'+appname
        else:
            raise FileNotFoundError('No configuration file found.')
    elif os.name == 'nt':
        return ("%s\%s" % (os.environ["APPDATA"], appname))
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
    logging_directory = string()
    socket_directory = string()
    upload_download_ratio = int()"""
    configuration = configobj.ConfigObj(configuration_filename,
                                        configspec=_configspec.split('\n'))
    validator = validate.Validator()
    configuration.validate(validator, copy=True)
    configuration = configuration.dict()
    directory_regex = re.compile('directory')
    directories = [key_ if re.search(directory_regex, key_) for key_ in configuration.keys()]
    for directory in directories:
        configuration[directory] = os.path.normpath(os.path.expanduser(configuration[directory]))
    return configuration

configuration = get_configuration(get_configuration_filename('mimille'))

