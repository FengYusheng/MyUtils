# -*- coding: utf-8 -*-
import copy

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

import maya.OpenMayaUI as apiUI

import ui_MainWindowForBevelTool
reload(ui_MainWindowForBevelTool)
import Panel
reload(Panel)
import options



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)




class MainWindowForBevelTool(QMainWindow, ui_MainWindowForBevelTool.Ui_MainWindowForBevelTool):
    def __init__(self, parent=None):
        super(MainWindowForBevelTool, self).__init__(parent)
        self._bevelNodes = None
        self._bevelOptions = copy.copy(options.bevelOptions)

        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.setCentralWidget(Panel.SimpleOptionsWidget(self))
        self.bevelActionGroup = QActionGroup(self)
        self.bevelActionGroup.addAction(self.simpleBevelOptionsAction)
        self.bevelActionGroup.addAction(self.fullBevelOptionsAction)
        self.simpleBevelOptionsAction.setChecked(True)

        self.bevelActionGroup.triggered.connect(self.alterPanel)


    def setBevelNodes(self, nodes):
        self._bevelNodes = copy.copy(nodes)


    def bevelNodes(self):
        return self._bevelNodes


    def bevelOptions(self):
        return self._bevelOptions


    def editBevelOption(self, option, value):
        self._bevelOptions[option] = value
        for _bevelNode in self._bevelNodes:
            if 'fraction' == option:
                _bevelNode[0].fraction.set(value)
            elif 'offsetAsFraction' == option:
                _bevelNode[0].offsetAsFraction.set(value)
            elif 'autoFit' == option:
                _bevelNode[0].autoFit.set(value)
            elif 'depth' == option:
                _bevelNode[0].depth.set(value)
            elif 'mitering' == option:
                _bevelNode[0].mitering.set(value)
            elif 'miterAlong' == option:
                _bevelNode[0].miterAlong.set(value)
            elif 'chamfer' == option:
                _bevelNode[0].chamfer.set(value)
            elif 'segments' == option:
                _bevelNode[0].segments.set(value)
            elif 'worldSpace' == option:
                _bevelNode[0].worldSpace.set(value)
            elif 'smoothingAngle' == option:
                _bevelNode[0].smoothingAngle.set(value)
            elif 'subdivideNgons' == option:
                _bevelNode[0].subdivideNgons.set(value)
            elif 'mergeVertices' == option:
                _bevelNode[0].mergeVertices.set(value)
            elif 'mergeVertexTolerance' == option:
                _bevelNode[0].mergeVertexTolerance.set(value)
            elif 'miteringAngle' == option:
                _bevelNode[0].miteringAngle.set(value)
            elif 'angleTolerance' == option:
                _bevelNode[0].angleTolerance.set(value)
            elif 'forceParallel' == option:
                _bevelNode[0].forceParallel.set(value)


    def alterPanel(self):
        if self.simpleBevelOptionsAction.isChecked():
            self.setCentralWidget(Panel.SimpleOptionsWidget(self))
        elif self.fullBevelOptionsAction.isChecked():
            self.setCentralWidget(Panel.OptionTableViewWidget(self))



def run():
    window = MainWindowForBevelTool(getMayaWindow())
    window.show()


if __name__ == '__main__':
    run()
