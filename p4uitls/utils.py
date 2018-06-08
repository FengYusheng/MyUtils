#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import ctypes.util

globalSettings = {
    'encoding' : 'utf-8'
}


class MWP4ProxyGuiderException(Exception):
    """Base exception for MWP4ProxyGuider."""
    pass


class InvalidPlatformException(MWP4ProxyGuiderException):
    def __init__(self, exc_info=None):
        super(InvalidPlatformException, self).__init__()
        sys.exc_info = exc_info


class InvalideUserException(MWP4ProxyGuiderException):
    def __init__(self, exc_info=None):
        super(InvalideUserException, self).__init__()
        sys.exc_info = exc_info


def setProcessTitle(title):
    libc = ctypes.util.find_library('c')
    if libc is not None:
        try:
            libc = ctypes.cdll.LoadLibrary(libc)
        except OSError as e:
            return
        except TypeError as e:
            return

        titleBytes = title.encode(globalSettings['encoding'])
        buf = ctypes.create_string_buffer(len(titleBytes))
        buf.value = titleBytes

        try:
            libc.prctl(15, buf, 0, 0, 0)
        except AttributeError as e:
            return
