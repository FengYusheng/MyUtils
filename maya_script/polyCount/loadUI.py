# -*- coding: utf-8 -*-

import os

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance
    from pysideuic import compileUi
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
    from pyside2uic import compileUi

cwd = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
destination = cwd + '\UIMainWindow.py'
source = cwd + '\Qt\main_window.ui'
with open(destination, 'w') as dest:
    compileUi(source, dest, False, 4, False)
