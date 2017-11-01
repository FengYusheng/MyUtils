# -*- coding: utf-8 -*-
import os
import re
import sys
import csv
import json

import maya.OpenMayaUI as apiUI
import pymel.core as pm

try:
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2 import __version__ as pyside_version
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

import load_ui
load_ui.loadUIForPM()
import ui_MainWindowForPM
reload(ui_MainWindowForPM)


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class MainWindowForPM(QMainWindow, ui_MainWindowForPM.Ui_MainWindowForPM):
    def __init__(self, parent=None):
        super(MainWindowForPM, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)

        self.checkToolDir = os.path.normcase(os.path.split(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))[0])
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.brushForSelected = QBrush(Qt.GlobalColor.darkCyan)
        self.brushForUnselected = QBrush(Qt.NoBrush)
        self.modelInCheckItemsListView = QStandardItemModel(self.checkItemsListView)
        self.checkItemsListView.setModel(self.modelInCheckItemsListView)
        self.selectionModelInCheckItemsListView = QItemSelectionModel(self.modelInCheckItemsListView, self.checkItemsListView)
        self.checkItemsListView.setSelectionModel(self.selectionModelInCheckItemsListView)
        self.modelInSelectedCheckItemsListView = QStandardItemModel(self.selectedCheckItemsListView)
        self.selectedCheckItemsListView.setModel(self.modelInSelectedCheckItemsListView)
        self.selectionModelInSelectedCheckItemsListView = QItemSelectionModel(self.modelInSelectedCheckItemsListView, self.selectedCheckItemsListView)
        self.selectedCheckItemsListView.setSelectionModel(self.selectionModelInSelectedCheckItemsListView)

        self.selectedCheckItems = []

        self._initProjectList()
        self._initCheckItemsList()

        self.addButton.clicked.connect(self.addCheckItems)
        self.removeButtion.clicked.connect(self.removeCheckItems)
        self.cancelButton.clicked.connect(self.quit)


    def _initProjectList(self):
        dataDir = self.checkToolDir + '/projects'
        self.projectCombo.clear()
        for top, subdirs, filenames in os.walk(dataDir):
            self.projects = subdirs
            break

        self.projectCombo.addItems(self.projects)


    def _initCheckItemsList(self):
        path = self.checkToolDir + '/projects/no mans land/checkItems.csv'
        if os.access(path, os.F_OK):
            self.modelInCheckItemsListView.clear()
            with open(path, 'rb') as csvfile:
                reader = csv.reader(csvfile, dialect=csv.excel)
                for item, _ in reader:
                    item = QStandardItem(item)
                    item.setFont(self.font)
                    item.setBackground(self.brushForUnselected)
                    str(item.text()) not in self.selectedCheckItems or item.setBackground(self.brushForSelected)
                    item.setEditable(False)
                    self.modelInCheckItemsListView.appendRow(item)


    def _initSelectedCheckItemsList(self):
        self.modelInSelectedCheckItemsListView.clear()
        if len(self.selectedCheckItems):
            for i in self.selectedCheckItems:
                item = QStandardItem(i)
                item.setEditable(False)
                item.setFont(self.font)
                self.modelInSelectedCheckItemsListView.appendRow(item)


    def _updateBothCheckItemsListViews(self):
        self._initSelectedCheckItemsList()
        self._initCheckItemsList()


    def addCheckItems(self):
        if self.selectionModelInCheckItemsListView.hasSelection():
            index = self.selectionModelInCheckItemsListView.currentIndex()
            text = self.modelInCheckItemsListView.itemFromIndex(index).text()
            str(text) in self.selectedCheckItems or self.selectedCheckItems.append(str(text))
            self._updateBothCheckItemsListViews()


    def removeCheckItems(self):
        if self.selectionModelInSelectedCheckItemsListView.hasSelection():
            index = self.selectionModelInSelectedCheckItemsListView.currentIndex()
            text = self.modelInSelectedCheckItemsListView.itemFromIndex(index).text()
            self.selectedCheckItems.remove(str(text))
            self._updateBothCheckItemsListViews()


    def quit(self):
        self.close()




if __name__ == '__main__':
    window =  MainWindowForPM(getMayaWindow())
    window.show()
