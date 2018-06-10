#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

if __package__ is None and not hasattr(sys, 'frozen'):
    import os
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import MWP4ProxyGuider

if __name__ == '__main__':
    MWP4ProxyGuider.main()
