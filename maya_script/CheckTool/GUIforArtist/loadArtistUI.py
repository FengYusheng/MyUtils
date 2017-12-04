# -*- coding: utf-8 -*-
import sys
import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from pyside2uic import compileUi
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from pysideuic import compileUi
    from PySide import __version__
    from shiboken import wrapInstance

import pymel.core as pm

MAYA_VERSION = int(pm.mel.eval('getApplicationVersionAsFloat();'))

def loadUIForArtist():
    checkToolDir = os.path.normpath(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
    checkToolDir = os.path.split(checkToolDir)[0]

    destination = checkToolDir + '/GUIforArtist' + '/ui_MainWindowForArtist.py'
    source = checkToolDir + '/Qt/UI/GUIforArtist' + '/MainWindowForArtist.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = checkToolDir + '/GUIforArtist' + '/ui_ChooseLocationDialog.py'
    source = checkToolDir + '/Qt/UI/GUIforArtist' + '/ChooseLocationDialog.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)



if __name__ == '__main__':
    loadUIForArtist()
