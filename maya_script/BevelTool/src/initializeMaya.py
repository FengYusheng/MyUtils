# -*- coding: utf-8 -*-
import sys
import os

def inilialize():
    toolDir = os.path.normpath(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
    toolDir = os.path.split(toolDir)[0]
    path = toolDir + '/src'
    sys.path.insert(0, path)


if __name__ == '__main__':
    inilialize()
