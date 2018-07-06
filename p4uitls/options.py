#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import shutil
import argparse
import getpass

from version import __version__
from utils import (
    globalSettings,
    KeyboardInterruption
)


g_proxy_conf = {}

g_preload_conf = {}


def parseOptions3():
    kwargs = {
        'prog' : 'MWP4ProxyGuider',

        'description' : '''This program guides you to deploy a P4P service on this machine.''',

        'formatter_class' : argparse.RawDescriptionHelpFormatter,

        'argument_default' : argparse.SUPPRESS,

        'conflict_handler' : 'resolve'
    }

    parser = argparse.ArgumentParser(**kwargs)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

    parser.add_argument('-p', '--project', action='store', help='Specify your project name, all the things will be in $HOME/PROJECT directory.', metavar='PROJECT_NAME', type=str, dest='project', default=None)

    parser.add_argument('-t', '--target-port', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='TARGET_P4PORT', type=str, dest='target_p4port', default=None)

    parser.add_argument('-u', '--p4user', action='store', help='Specify your Perforce user name.', metavar='P4USER_NAME', type=str, dest='target_p4user', default=None)

    parser.add_argument('-P', '--p4passwd', action='store', help='Specify your Perforce password.', metavar='P4PASSWORD', type=str, dest='target_p4passwd', default=None)

    parser.add_argument('-p', '--proxy-port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='PORT', type=str, dest='proxy_p4port', default=None)

    parser.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached. Default is P4PCACHE, or the directory from which p4p is started if P4PCACHE is not set.', metavar='ROOT_DIR', type=str, dest='proxy_p4cache', default=None)

    parser.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file. Default is P4LOG, or the directory from which p4p is started if P4LOG is not set. ', metavar='LOGFILE', type=str, dest='proxy_p4log', default=None)

    parser.add_argument('-c', '--p4client', action='store', help='Specify your client workspace', metavar='P4CLIENT', type=str, dest='preload_p4client', default=None)

    parser.add_argument('-d', '--p4Depot', action='store', help='Add the depot paths which you want to sync.', metavar='DEPOT', type=argparse.FileType('r', encoding=globalSettings['encoding']), dest='preload_p4depots', required=True)

    return vars(parser.parse_args()), parser


def readConf(opts):
    print('Deloying a Perforce proxy service.')
    print('-'*50)

    if opts['project'] is None:
        try:
            opts['project'] = input('Enter your project name: ')
            while opts['project'] == '':
                opts['project'] = input('Enter your project name: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['project'] = opts['project'].strip()

    if opts['target_p4port'] is None:
        try:
            opts['target_p4port'] = input("Enter the target Perforce server's port: ")
            while opts['target_p4port'] == '':
                opts['target_p4port'] = input("Enter the target Perforce server's port: ")
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['target_p4port'] = opts['target_p4port'].strip()

    if opts['target_p4user'] is None:
        try:
            opts['target_p4user'] = input('Enter your Perforce user name: ')
            while opts['target_p4user'] == '':
                opts['target_p4user'] = input('Enter your Perforce user name: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['target_p4user'] = opts['target_p4user']

    if opts['target_p4passwd'] is None:
        try:
            opts['target_p4passwd'] = input('Enter your Perforce password: ')
            while opts['target_p4passwd'] == '':
                opts['target_p4passwd'] = input('Enter your Perforce password: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['target_p4passwd'] = opts['target_p4passwd'].strip()

    if opts['proxy_p4port'] is None:
        try:
            opts['proxy_p4port'] = input('Enter the port on which P4P will listen: ')
            while opts['proxy_p4port'] == '':
                opts['proxy_p4port'] = input('Enter the port on which P4P will listen: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4port'] = opts['proxy_p4port'].strip()

    if opts['proxy_p4cache'] is None:
        try:
            opts['proxy_p4cache'] = input('Enter the directory where revisions are cached [{0}]: '.format(g_proxy_conf['project']+'/cache'))

            if opts['proxy_p4cache'] == '':
                opts['proxy_p4cache'] = 'cache'

        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4cache'] = opts['proxy_p4cache'].strip()

    if opts['proxy_p4log'] is None:
        try:
            opts['proxy_p4log'] = input('Enter the location of your P4P log file [{0}]: '.format(g_proxy_conf['project']+'/log'))

            if opts['proxy_p4log'] == '':
                opts['proxy_p4log'] = 'log'

        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['proxy_p4log'] = opts['proxy_p4log'].strip()

    if opts['preload_p4client'] is None:
        try:
            opts['preload_p4client'] = input('Specify your client workspace [{0}/{0}_{1}_workspace]: '.format(g_proxy_conf['project'], g_proxy_conf['proxy_p4port']))

            if opts['preload_p4client'] == '':
                opts['preload_p4client'] = g_proxy_conf['project'] + '_' + g_proxy_conf['proxy_p4port'] + '_workspace'

        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['preload_p4client'] = opts['preload_p4client'].strip()

    if opts['preload_p4depots'] is not None:
        g_proxy_conf['preload_p4depots'] = list(set([i.strip() for i in opts['preload_p4depots']]))
    else:
        i = 1
        opts['preload_p4depots'] = []

        print('Enter the depots which you want to cache, type "Q" to quit: ')

        try:
            depot = input('[{0}]: '.format(i))
        except (IOError , EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        while depot != 'Q':
            opts['preload_p4depots'].append(depot)
            i += 1

            try:
                depot = input('[{0}]: '.format(i))
            except (IOError, EOFError, KeyboardInterrupt) as e:
                raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['preload_p4depots'] = list(set(opts['preload_p4depots']))

    return g_proxy_conf


def saveConf(opts, dest):
    pass


def validateProxyOpts(opts):
    return True


def validatePreloadOpts(opts):
    return True
