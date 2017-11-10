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
import DetailTabWidgets
reload(DetailTabWidgets)



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)


class DetailsWindowForPM(QMainWindow, ui_DetailsWindowForPM.Ui_DetailsMainWindowForPm):
    TIPTAB = 0
    DETAILTAB = 1
    CHECKTAB = 2

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
        self._initWhatsThisMessage()
        self._initTabData()

        self.finishButton.clicked.connect(self.quit)
        self.prevButton.clicked.connect(self.gotoPreviousWindow)
        self.selectionModelInCheckItemsListView.selectionChanged.connect(self.configureCheckItem)
        self.tipTextBrower.textChanged.connect(self.getTip)
        self.tipTextBrower.currentCharFormatChanged.connect(self.initTipFormat)


    def _initCheckItemsList(self):
        for i in self.data['checkItems']:
            item = QStandardItem(i)
            item.setFont(self.font)
            item.setEditable(False)
            self.modelInCheckItemsListView.appendRow(item)


    def _initWhatsThisMessage(self):
        self.data['whatsthis'] = {}
        tipDir = self.checkToolDir + '/projects/no mans land/tip/'
        whatsThisDir = self.checkToolDir + '/projects/no mans land/whatsThis'
        path = tipDir if os.access(tipDir, os.F_OK) else whatsThisDir
        for fileName in (f for t1, t2, files in os.walk(path) for f in files):
            with open(path+'/'+fileName, 'r') as f:
                key = fileName.rpartition('.')[0]
                self.data['whatsthis'][key] = key + ': ' + f.read().strip()


    def _initTabData(self):
        self.itemTabWidget.setTabEnabled(DetailsWindowForPM.DETAILTAB, False)
        path = self.checkToolDir + '/projects/no mans land'
        self.data['detail'] = {f.rpartition('.')[0]:[] for f in os.listdir(path) if f.endswith('.csv')}

        self.data.setdefault('tip', {})

    def quit(self):
        self.close()


    def gotoPreviousWindow(self):
        self.quit()
        MainWindowForPM.MainWindowForPM(self.data, self.parent).show()


    def getTip(self):
        index = self.selectionModelInCheckItemsListView.currentIndex()
        item = str(self.modelInCheckItemsListView.itemFromIndex(index).text())
        self.data['tip'][item] = self.tipTextBrower.toPlainText().strip()


    def initTipFormat(self):
        self.tipTextBrower.setFontPointSize(12.0)


    def configureCheckItem(self):
        def _configureTipTab(item):
            self.tipTextBrower.setFontPointSize(12.0)
            self.tipTextBrower.setPlaceholderText(
                'You can edit your own tip message about "{0}" '.format(item)\
                +'to tell your members what this item does.'
            )
            self.tipTextBrower.setPlainText(self.data['tip'].setdefault(item, ''))


        def _configureDetailTab(item):
            self.itemTabWidget.setTabEnabled(DetailsWindowForPM.DETAILTAB, False)
            item not in self.data['detail'].keys() or self.itemTabWidget.setTabEnabled(DetailsWindowForPM.DETAILTAB, True)
            if 'check shader names' == item:
                self.scrollAreaInDetailTab.setWidget(DetailTabWidgets.CheckShaderNamesWidget(self))
            elif 'check poly count' == item:
                self.scrollAreaInDetailTab.setWidget(DetailTabWidgets.CheckPolyCountWidget(self))


        index = self.selectionModelInCheckItemsListView.currentIndex()
        item = str(self.modelInCheckItemsListView.itemFromIndex(index).text())
        _configureTipTab(item)
        _configureDetailTab(item)

        self.statusbar.showMessage(self.data['whatsthis'][item])



if __name__ == '__main__':
    window = DetailsWindowForPM({})
    window.show()
