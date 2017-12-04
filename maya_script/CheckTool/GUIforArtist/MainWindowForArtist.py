# -*- coding: utf-8 -*-
import json
import csv
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
import maya.OpenMayaUI as apiUI

import loadArtistUI
loadArtistUI.loadUIForArtist()
import ui_MainWindowForArtist
reload(ui_MainWindowForArtist)
import ui_ChooseLocationDialog
reload(ui_ChooseLocationDialog)
import checkers.CheckAsset
import GlobalInArtist



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class ChooseLocationDialog(QDialog, ui_ChooseLocationDialog.Ui_ChooseLocationDialog):
    def __init__(self, parent=None):
        super(ChooseLocationDialog, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.applyButton.setDefault(True)
        self.applyButton.setEnabled(False)

        self.parent = parent
        self.location = None

        self.closeButton.clicked.connect(self.quit)
        self.applyButton.clicked.connect(self.applyLocation)
        self.chooseLocationButton.clicked.connect(self.choose)


    def choose(self):
        self.applyButton.setEnabled(False)
        destination = pm.fileDialog2(cap='Open', ds=2, fm=3, okc='Open')
        if destination is not None:
            self.locationLineEdit.setText(destination[0])
            self.applyButton.setEnabled(True)
            self.location = destination[0]


    def quit(self):
        self.reject()


    def applyLocation(self):
        self.parent.setLocation(self.location)
        self.accept()


class MainWindowForArtist(QMainWindow, ui_MainWindowForArtist.Ui_MainWindowForArtist):
    def __init__(self, parent=None):
        super(MainWindowForArtist, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dataModelInCheckerListView = QStandardItemModel(self.checkerListView)
        self.checkerListView.setModel(self.dataModelInCheckerListView)
        self.selectionModelIncheckerListView = QItemSelectionModel(self.dataModelInCheckerListView, self.checkerListView)
        self.checkerListView.setSelectionModel(self.selectionModelIncheckerListView)
        self.checkerListView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.checkerListView.mousePressEvent = self._mousePressEventInCheckerListView

        self.data = {}
        self.parent = parent
        self.font = QFont('OldEnglish', 10, QFont.Bold)


    def _initializeProjectList(self):
        self.projectComboBox.clear()
        self.projectComboBox.addItems(self.projects())


    def _initializeCheckerList(self):
        self.dataModelInCheckerListView.clear()
        header = QStandardItem('Checker')
        header.setFont(self.font)
        project = self.projectComboBox.currentText()
        self.dataModelInCheckerListView.setHorizontalHeaderItem(0, header)
        for checker in self.checkers(project):
            item = QStandardItem(checker)
            item.setEditable(False)
            item.setFont(self.font)
            self.dataModelInCheckerListView.appendRow(item)


    def _initializeData(self):
        def _initializeProjects():
            for root, subdirs, filenames in os.walk(self.location()):
                self.setProjects(subdirs)
                break

        def _initializeCheckers():
            location = self.location()
            for project in self.projects():
                s = location + '/' + project + '/checkers.csv'
                if os.access(s, os.F_OK):
                    with open(s, 'rb') as csvfile:
                        reader = csv.reader(csvfile, dialect=csv.excel)
                        self.setCheckers(project, [i[0].decode('utf-8') for i in reader])

        def _initializeTips():
            location = self.location()
            for project in self.projects():
                checkers = self.checkers(project)
                s = location + '/' + project + '/tip'
                if os.access(s, os.F_OK):
                    for tip in os.walk(s).next()[2]:
                        if tip.rpartition('.')[0] in checkers:
                            with open(s+'/'+tip, 'r') as f:
                                self.setTip(project, tip.rpartition('.')[0], f.read().decode('utf-8').strip())

        def _initializeDetails():
            location = self.location()
            for project in self.projects():
                checkers = self.checkers(project)
                s = location + '/' + project + '/detail'
                if os.access(s, os.F_OK):
                    for detail in os.walk(s).next()[2]:
                        if detail.rpartition('.')[0] in checkers and detail.rpartition('.')[0] in GlobalInArtist.detail:
                            with open(s+'/'+detail, 'rb') as csvfile:
                                reader = csv.reader(csvfile, dialect=csv.excel)
                                self.setDetail(project, detail.rpartition('.')[0], [i for i in reader])

        _initializeProjects()
        _initializeCheckers()
        _initializeTips()
        _initializeDetails()
        self._initializeProjectList()
        self._initializeCheckerList()


    def _mousePressEventInCheckerListView(self, event):
        self.selectionModelIncheckerListView.clearSelection()
        QListView.mousePressEvent(self.checkerListView, event)


    def setLocation(self, location):
        self.data['location'] = location
        self._initializeData()


    def location(self):
        return self.data.setdefault('location', '')


    def setProjects(self, projects):
        self.data['projects'] = projects
        self.data['projects'].append('Change location')


    def projects(self):
        return self.data.setdefault('projects', ['Change location',])


    def setCheckers(self, project, checkers):
        self.data.setdefault('checkers', {})
        self.data['checkers'][project] = checkers


    def checkers(self, project):
        self.data.setdefault('checkers', {})
        return self.data['checkers'].setdefault(project, [])


    def setTip(self, project, checker, tip):
        self.data.setdefault('tip', {})
        self.data['tip'].setdefault(project, {})
        self.data['tip'][project][checker] = tip


    def tip(self, project, checker):
        self.data.setdefault('tip', {})
        self.data['tip'].setdefault(project, {})
        return self.data['tip'][project].setdefault(checker, '')


    def setDetail(self, project, checker, detail):
        self.data.setdefault('detail', {})
        self.data['detail'].setdefault(project, {})
        self.data['detail'][project][checker] = detail


    def detail(self, project, checker):
        self.data.setdefault('detail', {})
        self.data['detail'].setdefault(project, {})
        return self.data['detail'][project].setdefault(checker, [])


    def quit(self):
        self.close()


if __name__ == '__main__':
    window = MainWindowForArtist(getMayaWindow())
    window.show()
    QDialog.Accepted == ChooseLocationDialog(window).exec_() or window.quit()
