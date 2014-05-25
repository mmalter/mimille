#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
import os

def get_configuration_path(appname):
    """Return the configuration file path."""
    if os.name == 'posix' or os.name == 'mac':
        return '/etc/'+appname
    elif os.name == 'nt':
        return ("%s\%s" % (os.environ["APPDATA"], appname))
    else:
        raise UnsupportedOSError(os.name)

setup(name='mtorrent',
	version='0.1',
    description='A bittorrent client following a client/server architecture',
    author='Michaël Malter',
    author_email='dev@michaelmalter.fr',
    url='https://github.com/mmalter/mtorrent', 
    data_files=[(get_configuration_path('mtorrent'),['mtorrent'])]
	)
