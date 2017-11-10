# -*- coding: utf-8 -*-
import os
import re
import sys
import csv

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
import DetailsWindowForPM
reload(DetailsWindowForPM)
import ui_MainWindowForPM
reload(ui_MainWindowForPM)


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class MainWindowForPM(QMainWindow, ui_MainWindowForPM.Ui_MainWindowForPM):
    def __init__(self, data={}, parent=None):
        super(MainWindowForPM, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)

        self.modelInCheckItemsListView = QStandardItemModel(self.checkItemsListView)
        self.checkItemsListView.setModel(self.modelInCheckItemsListView)
        self.selectionModelInCheckItemsListView = QItemSelectionModel(self.modelInCheckItemsListView, self.checkItemsListView)
        self.checkItemsListView.setSelectionModel(self.selectionModelInCheckItemsListView)
        self.checkItemsListView.mouseDoubleClickEvent = self._mouseDoubleClickEventInCheckItemsListView
        self.checkItemsListView.mousePressEvent = self._mousePressEventInCheckItemsListView
        self.modelInSelectedCheckItemsListView = QStandardItemModel(self.selectedCheckItemsListView)
        self.selectedCheckItemsListView.setModel(self.modelInSelectedCheckItemsListView)
        self.selectionModelInSelectedCheckItemsListView = QItemSelectionModel(self.modelInSelectedCheckItemsListView, self.selectedCheckItemsListView)
        self.selectedCheckItemsListView.setSelectionModel(self.selectionModelInSelectedCheckItemsListView)
        self.selectedCheckItemsListView.mouseDoubleClickEvent = self._mouseDoubleClickEventInSelectedCheckItemsListView
        self.selectedCheckItemsListView.mousePressEvent = self._mousePressEventInSelectedCheckItemsListView

        self.data = data
        self.parent = parent
        self.whatsThisMessage = {}
        self.checkToolDir = os.path.normpath(os.path.split(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))[0])
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.brushForSelected = QBrush(Qt.GlobalColor.darkCyan)
        self.brushForUnselected = QBrush(Qt.NoBrush)

        self._initProjectList()
        self._initCheckItemsList()
        self._initSelectedCheckItemsList()
        self._initWhatsThisMessage()
        self._setNextButtonState()

        self.addButton.clicked.connect(self.addCheckItems)
        self.removeButtion.clicked.connect(self.removeCheckItems)
        self.cancelButton.clicked.connect(self.quit)
        self.nextButton.clicked.connect(self.goToDetailWindow)
        self.selectionModelInCheckItemsListView.selectionChanged.connect(self.displayWhatsThis)


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
                    item = QStandardItem(item.strip())
                    item.setFont(self.font)
                    item.setBackground(self.brushForUnselected)
                    str(item.text()) not in self.data.setdefault('checkItems', []) or item.setBackground(self.brushForSelected)
                    item.setEditable(False)
                    self.modelInCheckItemsListView.appendRow(item)


    def _initSelectedCheckItemsList(self):
        self.modelInSelectedCheckItemsListView.clear()
        if len(self.data.setdefault('checkItems', [])):
            for i in self.data['checkItems']:
                item = QStandardItem(i)
                item.setEditable(False)
                item.setFont(self.font)
                self.modelInSelectedCheckItemsListView.appendRow(item)


    def _initWhatsThisMessage(self):
        whatsThisDir = self.checkToolDir + '/projects/no mans land/whatsThis/'
        for fileName in (f for t1, t2, files in os.walk(whatsThisDir) for f in files):
            with open(whatsThisDir+'/'+fileName, 'r') as whatsThisFile:
                key = fileName.rpartition('.')[0]
                self.whatsThisMessage.setdefault(key, whatsThisFile.read().strip())


    def _setNextButtonState(self):
        self.nextButton.setEnabled(False)
        not len(self.data.setdefault('checkItems', [])) or self.nextButton.setEnabled(True)


    def _updateBothCheckItemsListViews(self):
        self._initSelectedCheckItemsList()
        self._initCheckItemsList()


    def _mouseDoubleClickEventInCheckItemsListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.addCheckItems()
        QListView.mouseDoubleClickEvent(self.checkItemsListView, event)


    def _mousePressEventInCheckItemsListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.checkItemsListView.clearSelection()
        QListView.mousePressEvent(self.checkItemsListView, event)


    def _mouseDoubleClickEventInSelectedCheckItemsListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.removeCheckItems()
        QListView.mouseDoubleClickEvent(self.selectedCheckItemsListView, event)


    def _mousePressEventInSelectedCheckItemsListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.selectedCheckItemsListView.clearSelection()
        QListView.mousePressEvent(self.selectedCheckItemsListView, event)


    def addCheckItems(self):
        if self.selectionModelInCheckItemsListView.hasSelection():
            index = self.selectionModelInCheckItemsListView.currentIndex()
            text = self.modelInCheckItemsListView.itemFromIndex(index).text()
            str(text) in self.data.setdefault('checkItems', []) or self.data['checkItems'].append(str(text))
            self._updateBothCheckItemsListViews()
            self._setNextButtonState()


    def removeCheckItems(self):
        if self.selectionModelInSelectedCheckItemsListView.hasSelection():
            index = self.selectionModelInSelectedCheckItemsListView.currentIndex()
            text = self.modelInSelectedCheckItemsListView.itemFromIndex(index).text()
            self.data['checkItems'].remove(str(text))
            self._updateBothCheckItemsListViews()
            self._setNextButtonState()


    def quit(self):
        self.close()


    def displayWhatsThis(self):
        self.statusbar.clearMessage()
        if self.selectionModelInCheckItemsListView.hasSelection():
            index = self.selectionModelInCheckItemsListView.currentIndex()
            key = str(self.modelInCheckItemsListView.itemFromIndex(index).text())
            whatsThis = key + ': ' + self.whatsThisMessage.setdefault(key, '')
            self.statusbar.showMessage(whatsThis)


    def goToDetailWindow(self):
        '''
        https://stackoverflow.com/questions/3868928/passing-variables-between-modules
        '''
        self.quit()
        detailsWindow = DetailsWindowForPM.DetailsWindowForPM(self.data, self.parent)
        detailsWindow.show()

if __name__ == '__main__':
    window =  MainWindowForPM(parent=getMayaWindow())
    window.show()
