# -*- coding: utf-8 -*-
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


def loadBevelToolUI():
    bevelToolDir = os.path.normpath(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
    bevelToolDir = os.path.split(bevelToolDir)[0]

    destination = bevelToolDir + '/src/ui_MainWindowForBevelTool.py'
    source = bevelToolDir + '/src/Qt/UI/MainWindowForBevelTool.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = bevelToolDir + '/src/ui_OptionTableViewWidget.py'
    source = bevelToolDir + '/src/Qt/UI/OptionTableViewWidget.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = bevelToolDir + '/src/ui_SimpleOptionsWidget.py'
    source = bevelToolDir + '/src/Qt/UI/SimpleOptionsWidget.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = bevelToolDir + '/src/ui_BevelSetEditorWidget.py'
    source = bevelToolDir + '/src/Qt/UI/BevelSetEditorWidget.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)

    destination = bevelToolDir + '/src/ui_MWBevelToolMainWindow.py'
    source = bevelToolDir + '/src/Qt/UI/MWBevelToolMainWindow_io.ui'
    with open(destination, 'w') as f:
        compileUi(source, f, False, 4, False)



if __name__ == '__main__':
    loadBevelToolUI()
