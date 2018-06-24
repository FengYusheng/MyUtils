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

def parseOptions():
    columns = shutil.get_terminal_size(fallback=(80, 24)).columns
    max_width = columns if columns else 80
    max_help_position = 80

    kwargs = {
        'prog' : 'MWP4ProxyGuider',

        'usage' : '%(prog)s [OPTIONS]',

        'description' : '''This program guides you to deploy a P4P service on this machine.''',

        'formatter_class' : argparse.RawDescriptionHelpFormatter,

        'argument_default' : argparse.SUPPRESS,

        'conflict_handler' : 'resolve'
    }

    parser = argparse.ArgumentParser(**kwargs)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

    p4p_option_group = parser.add_argument_group('P4P options', 'These options are used to start a p4p process.')

    p4p_option_group.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='port', type=str, dest='p4port')

    p4p_option_group.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached.', metavar='root', type=str, dest='p4cache')

    p4p_option_group.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file', metavar='logfile', type=str, dest='p4log')

    p4p_option_group.add_argument('-t', '--p4target', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='port', type=str, dest='p4target')

    p4_option_group = parser.add_argument_group('p4 preloading options', 'These options are used to preload the cache directory for optimal initial performance.')

    return vars(parser.parse_args())


def parseOptionsSubCommand():
    kwargs = {
        'prog' : 'MWP4ProxyGuider',

        'description' : '''This program guides you to deploy a P4P service on this machine.''',

        'formatter_class' : argparse.RawDescriptionHelpFormatter,

        'argument_default' : argparse.SUPPRESS,

        'conflict_handler' : 'resolve'
    }

    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

    global_group = parser.add_argument_group('Global options')
    # global_group.add_argument('-P', '--project', action='store', help='Specify your project name, all the things will be in PROJECT directory.', metavar='PROJECT_NAME', type=str, dest='project')
    # global_group.add_argument('-t', '--target-p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='TARGET_P4PORT', type=str, dest='target_p4port')
    # global_group.add_argument('-u', '--target-p4user', action='store', help='Specify your Perforce user name.', metavar='P4USER_NAME', type=str, dest='target_p4user')
    # global_group.add_argument('-p', '--target-p4port', action='store', help='Specify your Perforce password.', metavar='P4PASSWORD', type=str, dest='target_p4passwd')

    global_group.add_argument('project', action='store', help='Specify your project name, all the things will be in $HOME/PROJECT directory.', metavar='PROJECT_NAME', type=str)
    global_group.add_argument('target_p4port', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='TARGET_P4PORT', type=str)
    global_group.add_argument('target_p4user', action='store', help='Specify your Perforce user name.', metavar='P4USER_NAME', type=str)
    global_group.add_argument('target_p4passwd', action='store', help='Specify your Perforce password.', metavar='P4PASSWORD', type=str)

    # global_group.add_argument('-c', '--clean', action='store_true', help='Clean your last configuration.', dest='clean')

    subparsers = parser.add_subparsers(title='Mindwalk P4Proxy Guider Commands')

    # Deploy and start a Perforce proxy service
    p4proxy_parser = subparsers.add_parser('p4p', help='This command deploys and starts a Perforce proxy service on this machine.', description='"%(prog)s" deploys and starts a Perforce proxy service on this machine.')

    p4proxy_parser.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='PORT', type=str, dest='proxy_p4port')

    p4proxy_parser.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached. Default is P4PCACHE, or the directory from which p4p is started if P4PCACHE is not set.', metavar='ROOT_DIR', type=str, dest='proxy_p4cache')

    p4proxy_parser.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file. Default is P4LOG, or the directory from which p4p is started if P4LOG is not set. ', metavar='LOGFILE', type=str, dest='proxy_p4log')

    # p4proxy_parser.add_argument('-t', '--p4target', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='PORT', type=str, dest='proxy_p4target')

    # p4proxy_parser.add_argument('-P', '--p4passwd', action='store', help='Specify your Perforce user password.', metavar='PASSWORD', type=str, dest='p4_password')

    # Preload the cache directory.
    preload_parser = subparsers.add_parser('preload', help='This command is used to preload the cache directory for optimal initial performance.', description='"%(prog)s" is used to preload the cache directory for optimal initial performance.')

    preload_parser.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P is listening for requests from Perforce applications.', metavar='PORT', type=str, dest='proxy_p4port')

    # preload_parser.add_argument('-u', '--p4user', action='store', help='Specify your Perforce user name.', metavar='P4USER NAME', type=str, dest='preload_p4user')

    # preload_parser.add_argument('-P', '-p4passwd', action='store', help='Specify current Perforce user password.', metavar='PASSWORD', type=str, dest='preload_p4passwd')

    preload_parser.add_argument('-c', '--p4client', action='store', help='Specify your client workspace', metavar='P4CLIENT', type=str, dest='preload_p4client')

    # TODO: argparse.FileType seems better.
    preload_parser.add_argument('-d', '--p4Depot', action='store', help='Add the depot paths which you want to sync.', metavar='DEPOT', type=argparse.FileType('r', encoding=globalSettings['encoding']), dest='preload_p4depots')

    return vars(parser.parse_args()), parser


# TODO: Validate the configuration.
def parseProxyOptions(opts):
    print('Deloying a Perforce proxy service.')
    print('-'*50)

    g_proxy_conf['project'] = opts['project']
    g_proxy_conf['target_p4port'] = opts['target_p4port']
    g_proxy_conf['target_p4user'] = opts['target_p4user']
    g_proxy_conf['target_p4passwd'] = opts['target_p4passwd']

    if opts['proxy_p4port'] is None:
        try:
            opts['proxy_p4port'] = input('Enter the port on which P4P is listening for requests from Perforce applications: ')
            while opts['proxy_p4port'] == '':
                opts['proxy_p4port'] = input('Enter the port on which P4P is listening for requests from Perforce applications: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4port'] = opts['proxy_p4port']

    if opts['proxy_p4cache'] is None:
        try:
            opts['proxy_p4cache'] = input('Enter the directory name where revisions are cached [{0}]: '.format(opts['project']+'/cache'))
            if opts['proxy_p4cache'] == '':
                opts['proxy_p4cache'] = 'cache'
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4cache'] = opts['proxy_p4cache']

    if opts['proxy_p4log'] is None:
        try:
            opts['proxy_p4log'] = input('Enter the location of the log file [{0}]: '.format(opts['project']+'/log'))
            if opts['proxy_p4log'] == '':
                opts['proxy_p4log'] = 'log'
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4log'] = opts['proxy_p4log']

    # print(g_proxy_conf)
    return g_proxy_conf


def parsePreloadOptions(opts):
    print('Preloading the cache directory for optimal initial performance.')
    print('-'*50)

    g_preload_conf['project'] = opts['project']
    g_preload_conf['target_p4port'] = opts['target_p4port']
    g_preload_conf['target_p4user'] = opts['target_p4user']
    g_preload_conf['target_p4passwd'] = opts['target_p4passwd']

    if opts['proxy_p4port'] is None:
        try:
            opts['proxy_p4port'] = input('Perforce proxy port: ')
            while opts['proxy_p4port'] == '':
                opts['proxy_p4port'] = input('Perforce proxy port: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_preload_conf['proxy_p4port'] = opts['proxy_p4port']

    if opts['preload_p4client'] is None:
        try:
            opts['preload_p4client'] = input('Specify your workspace [{0}/{0}_{1}_workspace]: '.format(opts['project'], opts['proxy_p4port']))
            if opts['preload_p4client'] == '':
                opts['preload_p4client'] = opts['project'] + '_' + opts['proxy_p4port'] + '_workspace'
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_preload_conf['preload_p4client'] = opts['preload_p4client']

    if opts['preload_p4depots'] is not None:
        g_preload_conf['preload_p4depots'] = list(set([i.strip() for i in opts['preload_p4depots']]))
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

        g_preload_conf['preload_p4depots'] = list(set(opts['preload_p4depots']))

    # print(g_preload_conf)
    return g_preload_conf


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

    g_proxy_conf['project'] = opts['project']

    if opts['target_p4port'] is None:
        try:
            opts['target_p4port'] = input("Enter the target Perforce server's port: ")
            while opts['target_p4port'] == '':
                opts['target_p4port'] = input("Enter the target Perforce server's port: ")
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['target_p4port'] = opts['target_p4port']

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
            opts['target_p4passwd'] = getpass.getpass('Enter your Perforce password: ')
            while opts['target_p4passwd'] == '':
                opts['target_p4passwd'] = getpass.getpass('Enter your Perforce password: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['target_p4passwd'] = opts['target_p4passwd']

    if opts['proxy_p4port'] is None:
        try:
            opts['proxy_p4port'] = input('Enter the port on which P4P will listen: ')
            while opts['proxy_p4port'] == '':
                opts['proxy_p4port'] = input('Enter the port on which P4P will listen: ')
        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4port'] = opts['proxy_p4port']

    if opts['proxy_p4cache'] is None:
        try:
            opts['proxy_p4cache'] = input('Enter the directory where revisions are cached [{0}]: '.format(g_proxy_conf['project']+'/cache'))

            if opts['proxy_p4cache'] == '':
                opts['proxy_p4cache'] = 'cache'

        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

    g_proxy_conf['proxy_p4cache'] = opts['proxy_p4cache']

    if opts['proxy_p4log'] is None:
        try:
            opts['proxy_p4log'] = input('Enter the location of your P4P log file [{0}]: '.format(g_proxy_conf['project']+'/log'))

            if opts['proxy_p4log'] == '':
                opts['proxy_p4log'] = 'log'

        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['proxy_p4log'] = opts['proxy_p4log']

    if opts['preload_p4client'] is None:
        try:
            opts['preload_p4client'] = input('Specify your client workspace [{0}/{0}_{1}_workspace]: '.format(g_proxy_conf['project'], g_proxy_conf['proxy_p4port']))

            if opts['preload_p4client'] == '':
                opts['preload_p4client'] = g_proxy_conf['project'] + '_' + g_proxy_conf['proxy_p4port'] + '_workspace'

        except (IOError, EOFError, KeyboardInterrupt) as e:
            raise KeyboardInterruption(sys.exc_info())

        g_proxy_conf['preload_p4client'] = opts['preload_p4client']

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
