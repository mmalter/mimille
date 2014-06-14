#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
from mimille import version
import os

def get_configuration_path(appname):
    """Return the configuration file path."""
    if os.name == 'posix' or os.name == 'mac':
        return '/etc/'+appname
    elif os.name == 'nt':
        return ("%s\%s" % (os.environ["APPDATA"], appname))
    else:
        raise UnsupportedOSError(os.name)

setup(name='mimille',
    version=version.version,
    description='A bittorrent client following a client/server architecture',
    author='Michaël Malter',
    author_email='dev@michaelmalter.fr',
    url='https://github.com/mmalter/mimille', 
    packages = ['mimille'],
    data_files=[
        (get_configuration_path('mimille'),['mimille']),
        ('/usr/local/bin',['mimille/server.py']),
        ('/etc/systemd/system',['os_specific/mimille.service'])]
	)

with open('/etc/systemd/system/mimille.service'):
        os.chmod('/etc/systemd/system/mimille.service', 0o755)

with open('/usr/local/bin/mimille_server.py'):
        os.chmod('/usr/local/bin/mimille_server.py', 0o755)
