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
import Global



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)


class DetailsWindowForPM(QMainWindow, ui_DetailsWindowForPM.Ui_DetailsMainWindowForPm):
    TIPTAB = 0
    DETAILTAB = 1
    CHECKTAB = 2

    def __init__(self, parent=None, **data):
        super(DetailsWindowForPM, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.font =  QFont('OldEnglish', 10, QFont.Bold)
        self.modelInCheckerListView = QStandardItemModel(self.checkerListView)
        self.selectionModelInCheckerListView = QItemSelectionModel(self.modelInCheckerListView, self.checkerListView)
        self.checkerListView.setModel(self.modelInCheckerListView)
        self.checkerListView.setSelectionModel(self.selectionModelInCheckerListView)
        self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.TIPTAB, False)
        self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.DETAILTAB, False)
        self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.CHECKTAB, False)
        self.checkerListView.mousePressEvent = self._mousePressEventInCheckerListView


        self.data = data
        self.parent = parent
        self.project = self.currentProject()
        self.checkToolDir = os.path.normpath(os.path.split(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))[0])

        self._initCheckerList()
        self._initTabData()

        self.finishButton.clicked.connect(self.quit)
        self.applyButton.clicked.connect(self.save)
        self.prevButton.clicked.connect(self.gotoPreviousWindow)
        self.selectionModelInCheckerListView.selectionChanged.connect(self.configureTab)
        self.tipTextBrower.textChanged.connect(self.setTip)
        self.tipTextBrower.currentCharFormatChanged.connect(self.initTipFormat)


    def _initCheckerList(self):
        for i in self.checkers():
            item = QStandardItem(i)
            item.setFont(self.font)
            item.setEditable(False)
            self.modelInCheckerListView.appendRow(item)


    def _initTabData(self):
        self.data.setdefault('tip', {})
        self.data.setdefault('detail', {})


    def _mousePressEventInCheckerListView(self, event):
        self.selectionModelInCheckerListView.clearSelection()
        QListView.mousePressEvent(self.checkerListView, event)


    def currentProject(self):
        index = self.data['project']
        return self.data['projects'][index]


    def checkers(self):
        self.data.setdefault('checkers', {})
        return self.data['checkers'].setdefault(self.project, [])


    def setTip(self):
        index = self.selectionModelInCheckerListView.currentIndex()
        checker = self.modelInCheckerListView.itemFromIndex(index).text()
        self.data['tip'][checker] = self.tipTextBrower.toPlainText().strip()


    def tip(self, checker):
        return self.data['tip'].setdefault(checker, '')


    def quit(self):
        self.close()


    def gotoPreviousWindow(self):
        parent = self.parent
        data = self.data
        self.quit()
        MainWindowForPM.MainWindowForPM(parent, **data).show()


    def initTipFormat(self):
        self.tipTextBrower.setFontPointSize(12.0)


    def configureTab(self):
        def _configureTipTab(checker):
            self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.TIPTAB, True)
            self.tipTextBrower.setFontPointSize(12.0)
            self.tipTextBrower.setPlaceholderText(
                'You can edit your own tip message about "{0}" '.format(checker)\
                +'to tell your members what this item does.'
            )
            self.tipTextBrower.setPlainText(self.tip(checker))


        def _configureDetailTab(checker):
            checker not in Global.detail or self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.DETAILTAB, True)
            if 'check shader names' == checker:
                self.scrollAreaInDetailTab.setWidget(DetailTabWidgets.CheckShaderNamesWidget(self))
            elif 'check poly count' == checker:
                self.scrollAreaInDetailTab.setWidget(DetailTabWidgets.CheckPolyCountWidget(self))


        self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.TIPTAB, False)
        self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.DETAILTAB, False)
        self.checkerTabWidget.setTabEnabled(DetailsWindowForPM.CHECKTAB, False)
        self.statusbar.clearMessage()
        if self.selectionModelInCheckerListView.hasSelection():
            index = self.selectionModelInCheckerListView.currentIndex()
            checker = str(self.modelInCheckerListView.itemFromIndex(index).text())
            _configureTipTab(checker)
            _configureDetailTab(checker)

            self.statusbar.showMessage(Global.whatsThis[checker])


    def detail(self, checker):
        return self.data['detail'].setdefault(checker, [])


    def setDetail(self, checker, args=[]):
        self.data['detail'].setdefault(checker, [])
        self.data['detail'][checker] = args


    def save(self):
        if 'New project' ==  self.project:
            pass
        else:
            pass
        # Save selected items.
        destination = self.checkToolDir + '/temporary'
        if len(self.data['checkItems']):
            with open(destination+'/selected checkers.csv', 'wb') as csvfile:
                writer = csv.writer(csvfile, dialect=csv.excel)
                writer.writerows([[i] for i in self.data['checkItems']])

        # Save tips.
        destination = self.checkToolDir + '/temporary/tip'
        if len(self.data['tip']):
            for key, tip in self.data['tip'].items():
                with open(destination+'/'+key+'.txt', 'w') as tipfile:
                    tipfile.write(tip.encode('utf-8'))

        # Save detail configuration.
        destination = self.checkToolDir + '/temporary/detail'
        for key, detail in self.data['detail'].items():
            with open(destination+'/'+key+'.csv', 'wb') as csvfile:
                writer = csv.writer(csvfile, dialect=csv.excel)
                writer.writerows([[i] for i in detail])



if __name__ == '__main__':
    window = DetailsWindowForPM({})
    window.show()
