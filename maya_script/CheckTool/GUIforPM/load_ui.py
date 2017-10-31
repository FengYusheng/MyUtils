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

def loadCreateCheckerUI():
    check_scene_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    create_checker_dir = check_scene_dir + '\create_checker'

    destination = create_checker_dir + '\ui_pm_main.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\pm_main.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = create_checker_dir + '\ui_details_dialog.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\details_dialog.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = create_checker_dir + '\ui_delete_dialog.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\delete.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = create_checker_dir + '\ui_new_save_dialog.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\\new_save_dialog.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = create_checker_dir + '\ui_save_dialog.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\save_dialog.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = create_checker_dir + '\ui_details_window.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\details_window.ui' if MAYA_VERSION >= 2017 else \
            check_scene_dir + '\Qt\UI\create_checker' + '\details_window_qt4.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = create_checker_dir + '\ui_choose_dialog.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\choose_dialog.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

def loadCheckUI():
    check_scene_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    check_dir = check_scene_dir + '\check'

    destination = check_dir + '\ui_main_window.py'
    source = check_scene_dir + '\Qt\UI\check' + '\main_window.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = check_dir + '\ui_choose_dialog.py'
    source = check_scene_dir + '\Qt\UI\create_checker' + '\choose_dialog.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)


if __name__ == '__main__':
    loadCreateCheckerUI()
    loadCheckUI()
