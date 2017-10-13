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

MAYA_VERION = int(pm.mel.eval('getApplicationVersionAsFloat();'))


def loadBudgetUI():
    ui_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__))) + '\Qt\UI'
    desination = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

    source = ui_dir + '\polyCountBudget.ui'
    py_file = desination + '\ui_polyCountBudget.py'
    with open(py_file, 'w') as pyfile:
        compileUi(source, pyfile, False, 4, False)

    source = ui_dir + '\polyCountBudget2.ui'
    py_file = desination + '\ui_polyCountBudget2.py'
    with open(py_file, 'w') as pyfile:
        compileUi(source, pyfile, False, 4, False)

    source = ui_dir + '\\auditMainWindow.ui'
    py_file = desination + '\ui_auditMainWindow.py'
    with open(py_file, 'w') as pyfile:
        compileUi(source, pyfile, False, 4, False)

    source = ui_dir + '\polyCountBudget3.ui'
    py_file = desination + '\ui_polyCountBudget3.py'
    with open(py_file, 'w') as pyfile:
        compileUi(source, pyfile, False, 4, False)

    source = ui_dir + '\\addBudgetDialog.ui'
    py_file = desination + '\ui_addBudgetDialog.py'
    with open(py_file, 'w') as pyfile:
        compileUi(source, pyfile, False, 4, False)


if __name__ == '__main__':
    loadBudgetUI()
