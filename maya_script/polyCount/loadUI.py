# -*- coding: utf-8 -*-

import os

from PySide.QtCore import *
from PySide.QtGui import *
from shiboken import wrapInstance
from pysideuic import compileUi

cwd = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
destination = cwd + '\UIMainWindow.py'
source = cwd + '\Qt\main_window.ui'
with open(destination, 'w') as dest:
    compileUi(source, dest, False, 4, False)
