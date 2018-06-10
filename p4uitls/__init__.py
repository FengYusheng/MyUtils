#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys
import time
import logging
import platform
import getpass

from utils import (
    globalSettings,
    setProcessTitle,
    InvalidPlatformException,
    InvalideUserException
)

import options


def _initialize():
    '''Initialize the running environment.'''

    globalSettings['platform'] = sys.platform
    if globalSettings['platform'] == 'linux':
        globalSettings['encoding'] = sys.getfilesystemencoding()
    else:
        raise InvalidPlatformException(sys.exc_info())

    globalSettings['Python'] = platform.python_version_tuple()[0]
    if globalSettings['Python'] != '3':
        print('WARNING: Suggset to run this tool with Python3.')

    globalSettings['LOGINNAME'] = getpass.getuser()
    if globalSettings['LOGINNAME'] != 'skywalker': # perforce
        raise InvalideUserException(sys.exc_info())



def _realMain(argv=None):
    _initialize()
    setProcessTitle('MW-P4Proxy-Guider')

    opts, parser = options.parseOptionsSubCommand()
    print(opts)

    # Analyze the options.
    len(opts.keys()) == 0 and parser.print_help()

    #TODO: Deploy a P4P service.
    if list(opts.keys())[0].startswith('proxy_'):
        print(type(opts.keys()))

    #TODO: Preload.
    if list(opts.keys())[0].startswith('preload_'):
        print(opts.keys())


def main(argv=None):
    try:
        _realMain(argv)
    except InvalidPlatformException as e:
        sys.exit('ERROR: run this tool in a linux system.')
    except InvalideUserException as e:
        sys.exit('ERROR: "{0}" is not a perforce user'.format(globalSettings['LOGINNAME']))


__all__ = [
    'main'
]
