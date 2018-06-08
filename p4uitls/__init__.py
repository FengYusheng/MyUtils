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
    if globalSettings['LOGINNAME'] != 'fengyusheng': # perforce
        raise InvalideUserException(sys.exc_info())



def _realMain(argv=None):
    _initialize()
    setProcessTitle('MW-P4Proxy-Guider')
    options.parseOptions()


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
