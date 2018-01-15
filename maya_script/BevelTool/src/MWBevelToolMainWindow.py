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

import ui_MWBevelToolMainWindow
reload(ui_MWBevelToolMainWindow)



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class ControlPanelDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ControlPanelDelegate, self).__init__(parent)



class MWBevelToolMainWindow(QMainWindow, ui_MWBevelToolMainWindow.Ui_MWBevelToolMainWindow):
    def __init__(self, parent=None):
        super(MWBevelToolMainWindow, self).__init__(parent)

        self.itemFont = QFont('OldEnglish', 10, QFont.Bold)
        self.itemBrush = QBrush(Qt.GlobalColor.darkGray, Qt.SolidPattern)

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dataModelInControlPanelTreeView = QStandardItemModel(self.controlDock)
        self.controlPanelTreeView.setModel(self.dataModelInControlPanelTreeView)
        self.selectionModelInControlPanelTreeView = QItemSelectionModel(self.dataModelInControlPanelTreeView, self.controlDock)
        self.controlPanelTreeView.setSelectionModel(self.selectionModelInControlPanelTreeView)
        self.controlPanelTreeView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.controlPanelTreeView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self._initializeControlPanel()


    def _initializeControlPanel(self):
        self.dataModelInControlPanelTreeView.clear()
        item = QStandardItem('Bevel Set')
        item.setFont(self.itemFont)
        item.setEditable(False)
        item.setBackground(self.itemBrush)
        self.dataModelInControlPanelTreeView.appendRow(item)
        parent = item

        item = QStandardItem('Children')
        item.setFont(self.itemFont)
        item.setEditable(False)
        parent.setChild(0, item)


        self.controlPanelTreeView.resizeColumnToContents(0)




def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
