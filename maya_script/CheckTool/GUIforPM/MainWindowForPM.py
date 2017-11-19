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
import ui_LocationDialog
reload(ui_LocationDialog)
import Global


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class LocationDialog(QDialog, ui_LocationDialog.Ui_locationDialog):
    def __init__(self, parent=None):
        super(LocationDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.okButton.setDefault(True)
        self.okButton.setEnabled(False)

        self.parent = parent
        self.location = None

        self.chooseButton.clicked.connect(self.choose)
        self.cancelButton.clicked.connect(self.quit)
        self.okButton.clicked.connect(self.setLocation)

    def choose(self):
        destination = pm.fileDialog2(cap='Open', ds=2, fm=3, okc='Open')
        if destination is not None:
            self.locationLinediet.setText(destination[0])
            self.location = destination[0]
            not self.location or self.okButton.setEnabled(True)


    def quit(self):
        self.reject()


    def setLocation(self):
        self.parent.setLocation(self.location)
        self.accept()



class MainWindowForPM(QMainWindow, ui_MainWindowForPM.Ui_MainWindowForPM):
    locationChanged = Signal()


    def __init__(self, parent=None, **data):
        super(MainWindowForPM, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.modelInCheckerListView = QStandardItemModel(self.checkerListView)
        self.checkerListView.setModel(self.modelInCheckerListView)
        self.selectionModelInCheckerListView = QItemSelectionModel(self.modelInCheckerListView, self.checkerListView)
        self.checkerListView.setSelectionModel(self.selectionModelInCheckerListView)
        self.checkerListView.mouseDoubleClickEvent = self._mouseDoubleClickEventInCheckerListView
        self.checkerListView.mousePressEvent = self._mousePressEventInCheckerListView
        self.modelInSelectedCheckerListView = QStandardItemModel(self.selectedCheckerListView)
        self.selectedCheckerListView.setModel(self.modelInSelectedCheckerListView)
        self.selectionModelInSelectedCheckerListView = QItemSelectionModel(self.modelInSelectedCheckerListView, self.selectedCheckerListView)
        self.selectedCheckerListView.setSelectionModel(self.selectionModelInSelectedCheckerListView)
        self.selectedCheckerListView.mouseDoubleClickEvent = self._mouseDoubleClickEventInSelectedCheckerListView
        self.selectedCheckerListView.mousePressEvent = self._mousePressEventInSelectedCheckerListView
        self.nextButton.setEnabled(False)

        self.data = data
        self.parent = parent
        self.checkToolDir = os.path.normpath(os.path.split(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))[0])
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.brushForSelected = QBrush(Qt.GlobalColor.darkCyan)
        self.brushForUnselected = QBrush(Qt.NoBrush)

        self.initialize()

        self.projectCombo.currentIndexChanged.connect(self.setCurrentProjectIndex)
        self.addButton.clicked.connect(self.addChecker)
        self.removeButtion.clicked.connect(self.removeChecker)
        self.cancelButton.clicked.connect(self.quit)
        self.nextButton.clicked.connect(self.goToDetailWindow)
        self.resetButton.clicked.connect(self.reset)
        self.selectionModelInCheckerListView.selectionChanged.connect(self.showWhatsThis)
        self.locationChanged.connect(self.initialize)


    def _initCheckerList(self):
        project = self.projectCombo.currentText()
        self.modelInCheckerListView.clear()
        for checker in Global.checkers:
            item = QStandardItem(checker.strip())
            item.setFont(self.font)
            item.setEditable(False)
            item.setBackground(self.brushForUnselected)
            checker not in self.checkers(project) or item.setBackground(self.brushForSelected)
            self.modelInCheckerListView.appendRow(item)


    def _initProjectList(self):
        self.projectCombo.clear()
        for root, subdirs, filenames in os.walk(self.location()):
            self.setProjects(subdirs)
            self.projectCombo.addItems(self.projects())
            for p in subdirs:
                path = root + p + '/checkers.csv'
                if os.access(path, os.F_OK):
                    with open(path, 'wb') as csvfile:
                        self.setCheckers(p, [i for i in csv.reader(csvfile, dialect=csv.excel)])

            break

        self.projectCombo.setCurrentIndex(self.currentProjectIndex())


    def _initSelectedCheckerList(self):
        project = self.projectCombo.currentText()
        self.modelInSelectedCheckerListView.clear()
        for i in self.checkers(project):
            item = QStandardItem(i)
            item.setEditable(False)
            item.setFont(self.font)
            self.modelInSelectedCheckerListView.appendRow(item)


    def _setNextButtonState(self):
        project = self.projectCombo.currentText()
        self.nextButton.setEnabled(False)
        not len(self.checkers(project)) or self.nextButton.setEnabled(True)


    def _updateBothCheckerListViews(self):
        self._initSelectedCheckerList()
        self._initCheckerList()


    def _mouseDoubleClickEventInCheckerListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.addChecker()
        QListView.mouseDoubleClickEvent(self.checkerListView, event)


    def _mousePressEventInCheckerListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.checkerListView.clearSelection()
        QListView.mousePressEvent(self.checkerListView, event)


    def _mouseDoubleClickEventInSelectedCheckerListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.removeChecker()
        QListView.mouseDoubleClickEvent(self.selectedCheckerListView, event)


    def _mousePressEventInSelectedCheckerListView(self, event):
        button = event.button()
        Qt.LeftButton != button or self.selectedCheckerListView.clearSelection()
        QListView.mousePressEvent(self.selectedCheckerListView, event)


    def setLocation(self, location):
        self.data.clear()
        self.data['location'] = location
        self.locationChanged.emit()


    def location(self):
        return self.data.setdefault('location', '')


    def projects(self):
        return self.data.setdefault('projects', [])


    def setProjects(self, projects):
        self.data['projects'] = projects
        self.data['projects'].append('New project')
        self.data['projects'].append('Change location')


    def setCurrentProjectIndex(self):
        project = self.projectCombo.currentText()
        if 'Change location' == project:
            QDialog.Accepted == LocationDialog(self).exec_() or self.projectCombo.setCurrentIndex(0)
        else:
            index = self.projectCombo.currentIndex()
            index = index if index > -1 else 0
            self.data['project'] = index


    def currentProjectIndex(self):
        return self.data.setdefault('project', 0)


    def checkers(self, project):
        self.data.setdefault('checkers', {})
        return self.data['checkers'].setdefault(project, [])


    def setCheckers(self, project, checkers):
        self.data.setdefault('checkers', {})
        self.data['checkers'][project] = checkers


    def addChecker(self):
        if self.selectionModelInCheckerListView.hasSelection():
            project = self.projectCombo.currentText()
            index = self.selectionModelInCheckerListView.currentIndex()
            text = self.modelInCheckerListView.itemFromIndex(index).text()
            text in self.checkers(project) or self.data['checkers'][project].append(text)
            self._updateBothCheckerListViews()
            self._setNextButtonState()


    def removeChecker(self):
        if self.selectionModelInSelectedCheckerListView.hasSelection():
            project = self.projectCombo.currentText()
            index = self.selectionModelInSelectedCheckerListView.currentIndex()
            text = self.modelInSelectedCheckerListView.itemFromIndex(index).text()
            self.checkers(project).remove(text)
            self._updateBothCheckerListViews()
            self._setNextButtonState()


    def initialize(self):
        self._initProjectList()
        self._initSelectedCheckerList()
        self._initCheckerList()
        self._setNextButtonState()


    def reset(self):
        project = self.projectCombo.currentText()
        self.setCheckers(project, [])
        self._initSelectedCheckerList()
        self._initCheckerList()
        self._setNextButtonState()


    def quit(self):
        self.close()


    def showWhatsThis(self):
        self.statusbar.clearMessage()
        if self.selectionModelInCheckerListView.hasSelection():
            index = self.selectionModelInCheckerListView.currentIndex()
            key = str(self.modelInCheckerListView.itemFromIndex(index).text())
            whatsThis = key + ': ' + Global.whatsThis[key]
            self.statusbar.showMessage(whatsThis)


    def goToDetailWindow(self):
        '''
        https://stackoverflow.com/questions/3868928/passing-variables-between-modules
        '''
        data = self.data
        parent = self.parent
        self.quit()
        detailsWindow = DetailsWindowForPM.DetailsWindowForPM(parent, **data)
        detailsWindow.show()



if __name__ == '__main__':
    window =  MainWindowForPM(parent=getMayaWindow())
    window.show()
    if QDialog.Rejected == LocationDialog(window).exec_():
        window.quit()