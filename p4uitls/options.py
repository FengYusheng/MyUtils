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

    p4p_option_group = parser.add_argument_group('P4P options', 'These options are used to start a p4p process.')
    p4p_option_group.add_argument('-p', '--p4port')

    return vars(parser.parse_args())
