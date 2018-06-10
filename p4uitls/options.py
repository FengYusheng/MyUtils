#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import shutil
import argparse
import getpass

from version import __version__


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

    # root_dir, required
    # log_dir, default:root_dir/log
    # port, required
    # project_port, required
    # p4_remote, required

    p4p_option_group.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='port', type=str, dest='p4port')

    p4p_option_group.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached.', metavar='root', type=str, dest='p4cache')

    p4p_option_group.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file', metavar='logfile', type=str, dest='p4log')

    p4p_option_group.add_argument('-t', '--p4target', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='port', type=str, dest='p4target')

    p4_option_group = parser.add_argument_group('p4 preloading options', 'These options are used to preload the cache directory for optimal initial performance.')

    return vars(parser.parse_args())


def parseOptionsSubCommand():
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

    parser.add_argument('--Project', action='store', help='Specify your project name, all the things will be in PROJECT directory.', required=True, type=str, dest='project', metavar='PROJECT')

    subparsers = parser.add_subparsers(title='Mindwalk P4Proxy Guider Commands')

    # Deploy and start a Perforce proxy service
    p4proxy_parser = subparsers.add_parser('p4p', help='This command deploys and starts a Perforce proxy service on this machine.', description='"%(prog)s" deploys and starts a Perforce proxy service on this machine.')

    p4proxy_parser.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='PORT', type=str, dest='proxy_p4port')

    p4proxy_parser.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached.', metavar='ROOT_DIR', type=str, dest='proxy_p4cache')

    p4proxy_parser.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file.', metavar='LOGFILE', type=str, dest='proxy_p4log')

    p4proxy_parser.add_argument('-t', '--p4target', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='PORT', type=str, dest='proxy_p4target')

    # Preload the cache directory.
    preload_parser = subparsers.add_parser('p4', help='This command is used to preload the cache directory for optimal initial performance.', description='"%(prog)s" is used to preload the cache directory for optimal initial performance.')

    preload_parser.add_argument('-p', '--p4port', action='store', help='Specify the the port of target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='PORT', type=str, dest='preload_p4port')

    preload_parser.add_argument('-u', '--p4user', action='store', help='Specify your Perforce user name.', metavar='P4USER NAME', type=str, dest='preload_p4user')

    preload_parser.add_argument('-P', '-p4passwd', action='store', help='Specify current Perforce user password.', metavar='PASSWORD', type=str, dest='preload_p4passwd')

    preload_parser.add_argument('-c', '--p4client', action='store', help='Specify your client workspace', metavar='P4CLIENT', type=str, dest='preload_p4client')

    # TODO: argparse.FileType seems better.
    preload_parser.add_argument('-d', '--p4Depot', action='append', help='Add the depot paths which you want to sync.', metavar='DEPOT', nargs='+', type=str, dest='preload_p4depots', default=[])

    return vars(parser.parse_args()), parser


# TODO: Validate the configuration.
# TODO: Catch the keyboard interrupt.
def parseProxyOptions(opts):
    print('Deloying a Perforce proxy service.')
    print('-'*50)

    if opts['proxy_p4port'] is None:
        opts['proxy_p4port'] = input('Enter the port which P4P will listen for p4 requests: ')
    g_proxy_conf['proxy_p4port'] = opts['proxy_p4port']

    if opts['proxy_p4cache'] is None:
        opts['proxy_p4cache'] = input('Enter the directory name where revisions are cached: ')
    g_proxy_conf['proxy_p4cache'] = opts['proxy_p4cache']

    if opts['proxy_p4log'] is None:
        opts['proxy_p4log'] = input('Enter the location of the log file: ')
    g_proxy_conf['proxy_p4log'] = opts['proxy_p4log']

    if opts['proxy_p4target'] is None:
        opts['proxy_p4target'] = input('Specify the port of the target Perforce server: ')
    g_proxy_conf['proxy_p4target'] = opts['proxy_p4target']

    print(g_proxy_conf)


def parsePreloadOptions(opts):
    print('Preloading the cache directory for optimal initial performance.')
    print('-'*50)

    if opts['preload_p4port'] is None:
        opts['preload_p4port'] = input('Specify the port of target Perforce server: ')
    g_preload_conf['preload_p4port'] = opts['preload_p4port']

    if opts['preload_p4user'] is None:
        opts['preload_p4user'] = input('Enter your Perforce user name: ')
    g_preload_conf['preload_p4user'] = opts['preload_p4user']

    if opts['preload_p4passwd'] is None:
        opts['preload_p4passwd'] = getpass.getpass()
        # opts['preload_p4passwd'] = input('Enter your Perforce password: ')
    g_preload_conf['preload_p4passwd'] = opts['preload_p4passwd']

    if opts['preload_p4client'] is None:
        opts['preload_p4client'] = input('Specify your workspace: ')
    g_preload_conf['preload_p4client'] = opts['preload_p4client']

    if len(opts['preload_p4depots']) == 0:
        pass
    g_preload_conf['preload_p4depots'] = opts['preload_p4depots']

    print(g_preload_conf)
