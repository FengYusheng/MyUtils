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

import MainWindowForPM
reload(MainWindowForPM)
import ui_DetailsWindowForPM
reload(ui_DetailsWindowForPM)



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)


class DetailsWindowForPM(QMainWindow, ui_DetailsWindowForPM.Ui_DetailsMainWindowForPm):
    def __init__(self, data, parent=None):
        super(DetailsWindowForPM, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)

        self.font =  QFont('OldEnglish', 10, QFont.Bold)
        self.modelInCheckItemsListView = QStandardItemModel(self.checkItemsListView)
        self.selectionModelInCheckItemsListView = QItemSelectionModel(self.modelInCheckItemsListView, self.checkItemsListView)
        self.checkItemsListView.setModel(self.modelInCheckItemsListView)
        self.checkItemsListView.setSelectionModel(self.selectionModelInCheckItemsListView)

        self.data = data
        self.parent = parent
        self.checkToolDir = os.path.normpath(os.path.split(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))[0])

        self._initCheckItemsList()
        self._initTipMessage()

        self.cancelButton.clicked.connect(self.quit)
        self.prevButton.clicked.connect(self.gotoPreviousWindow)


    def _initCheckItemsList(self):
        for i in self.data['checkItems']:
            item = QStandardItem(i)
            item.setFont(self.font)
            item.setEditable(False)
            self.modelInCheckItemsListView.appendRow(item)


    def _initTipMessage(self):
        self.data['tip'] = {}
        tipDir = self.checkToolDir + '/projects/no mans land/tip/'
        whatsThisDir = self.checkToolDir + '/projects/no mans land/whatsThis'
        path = tipDir if os.access(tipDir, os.F_OK) else whatsThisDir
        for fileName in (f for t1, t2, files in os.walk(path) for f in files):
            with open(path+'/'+fileName, 'r') as f:
                key = fileName.rpartition('.')[0]
                self.data['tip'][key] = f.read().strip()


    def quit(self):
        self.close()


    def gotoPreviousWindow(self):
        self.quit()
        MainWindowForPM.MainWindowForPM(self.data, self.parent).show()


    def configureCheckItem(self):
        pass



if __name__ == '__main__':
    window = DetailsWindowForPM({})
    window.show()
