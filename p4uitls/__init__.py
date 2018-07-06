#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys
import time
import logging
import platform
import getpass

import P4

from utils import (
    globalSettings,
    setProcessTitle,
    InvalidPlatformException,
    InvalideUserException,
    KeyboardInterruption,
    DeployP4Proxy,
    PreloadProxyCache,
    LackBinaryFiles,
    PortOccupiedException,
    RunCommandFailed
)

import options


def initialize():
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
    initialize()
    setProcessTitle('MW-P4Proxy-Guider')

    opts, parser = options.parseOptions3()
    opts = options.readConf(opts)
    print(opts)

    with DeployP4Proxy(opts) as dp:
        dp.createProject()
        dp.copyToolsIntoProject()
        dp.installPreloader()
        dp.startProxy()
        dp.createP4Workspace()


def main(argv=None):
    try:
        _realMain(argv)
    except InvalidPlatformException as e:
        sys.exit('ERROR: run this tool in a linux system.')
    except InvalideUserException as e:
        sys.exit('ERROR: "{0}" is not a perforce user'.format(globalSettings['LOGINNAME']))
    except KeyboardInterruption as e:
        sys.exit('\n\n# WARNING: User interrupt the program from keyboard.')
    except LackBinaryFiles as e:
        sys.exit(e)
    except P4.P4Exception as e:
        sys.exit(e)
    except PortOccupiedException as e:
        sys.exit(e)
    except RunCommandFailed as e:
        sys.exit(e)


__all__ = [
    'main'
]
