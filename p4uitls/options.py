#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import shutil
import argparse

from version import __version__


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

    p4p_option_group.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='port', nargs=1, type=str, dest='p4port')

    p4p_option_group.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached.', metavar='root', nargs=1, type=str, dest='p4cache')

    p4p_option_group.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file', metavar='logfile', nargs=1, type=str, dest='p4log')

    p4p_option_group.add_argument('-t', '--p4target', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='port', nargs=1, type=str, dest='p4target')

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

    subparsers = parser.add_subparsers(title='Mindwalk P4Proxy Guider Commands')

    # Deploy and start a Perforce proxy service
    p4proxy_parser = subparsers.add_parser('p4p', help='This command deploys and starts a Perforce proxy service on this machine.', description='"%(prog)s" deploys and starts a Perforce proxy service on this machine.')

    p4proxy_parser.add_argument('-p', '--p4port', action='store', help='Specify the port on which P4P will listen for requests from Perforce applications.', metavar='PORT', nargs=1, type=str, dest='proxy_p4port')

    p4proxy_parser.add_argument('-r', '--p4cache', action='store', help='Specify the directory where revisions are cached.', metavar='ROOT_DIR', nargs=1, type=str, dest='proxy_p4cache')

    p4proxy_parser.add_argument('-L', '--p4log', action='store', help='Specify the location of the log file.', metavar='LOGFILE', nargs=1, type=str, dest='proxy_p4log')

    p4proxy_parser.add_argument('-t', '--p4target', action='store', help='Specify the port of the target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='PORT', nargs=1, type=str, dest='proxy_p4target')

    # Preload the cache directory.
    preload_parser = subparsers.add_parser('p4', help='This command is used to preload the cache directory for optimal initial performance.', description='"%(prog)s" is used to preload the cache directory for optimal initial performance.')

    preload_parser.add_argument('-p', '--p4port', action='store', help='Specify the the port of target Perforce server (that is, the Perforce server for which P4P acts as a proxy).', metavar='PORT', nargs='?', type=str, dest='preload_p4port', default='P4PORT')

    preload_parser.add_argument('-u', '--p4user', action='store', help='Specify your Perforce user name.', metavar='P4USER NAME', nargs='?', type=str, dest='preload_p4user', default='P4USER')

    preload_parser.add_argument('-P', '-p4passwd', action='store', help='Specify current Perforce user password.', metavar='PASSWORD', nargs=1, type=str, dest='preload_p4passwd')

    preload_parser.add_argument('-c', '--p4client', action='store', help='Specify your client workspace', metavar='P4CLIENT', nargs=1, type=str, dest='preload_p4client')

    preload_parser.add_argument('-d', '--p4Depot', action='append', help='Add the depot paths which you want to sync.', metavar='DEPOT', nargs='+', type=str, dest='preload_p4depots')

    return vars(parser.parse_args()), parser
