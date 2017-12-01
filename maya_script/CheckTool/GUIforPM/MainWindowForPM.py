# -*- coding: utf-8 -*-
import os
import re
import sys
import csv
import copy

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
import ui_DeletePorjectDialog
reload(ui_DeletePorjectDialog)
import Global


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class LocationDialog(QDialog, ui_LocationDialog.Ui_locationDialog):
    def __init__(self, parent):
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



class DeleteProjectDialog(QDialog, ui_DeletePorjectDialog.Ui_deleteProjectDialog):
    def __init__(self, parent):
        super(DeleteProjectDialog, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.parent = parent

        self._initializeProjectName()

        self.cancelButton.clicked.connect(self.quit)
        self.applyButton.clicked.connect(self.deleteProject)


    def _initializeProjectName(self):
        index = self.parent.currentProjectIndex()
        project = self.parent.projects()[index]
        self.projectLabel.setText('<b><span style="font-size:10pt">Delete project: "{0}"</span></b>'.format(project))


    def quit(self):
        self.reject()


    def deleteProject(self):
        location = self.parent.location()
        index = self.parent.currentProjectIndex()
        project = self.parent.projects()[index]
        projectPath = location + '/' + project
        if os.access(projectPath, os.F_OK):
            for root, subdirs, filenames in os.walk(projectPath, topdown=False):
                for name in filenames:
                    path = os.path.normpath(os.path.join(root, name))
                    not os.access(path, os.F_OK) or os.remove(path)

                for name in subdirs:
                    path = os.path.normpath(os.path.join(root, name))
                    not os.access(path, os.F_OK) or os.rmdir(path)

            os.rmdir(projectPath)

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
        self.deleteButton.setEnabled(False)

        self.data = data
        self.parent = parent
        self.checkToolDir = os.path.normpath(os.path.split(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))[0])
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.brushForSelected = QBrush(Qt.GlobalColor.darkCyan)
        self.brushForUnselected = QBrush(Qt.NoBrush)

        self.initializeData()

        self.projectCombo.currentIndexChanged.connect(self.setCurrentProjectIndex)
        self.addButton.clicked.connect(self.addChecker)
        self.removeButtion.clicked.connect(self.removeChecker)
        self.cancelButton.clicked.connect(self.quit)
        self.nextButton.clicked.connect(self.goToDetailWindow)
        self.resetButton.clicked.connect(self.reset)
        self.deleteButton.clicked.connect(self.deleteProject)
        self.selectionModelInCheckerListView.selectionChanged.connect(self.showWhatsThis)
        self.locationChanged.connect(self.initializeData)


    def _initializeCheckerList(self):
        project = self.projectCombo.currentText()
        self.modelInCheckerListView.clear()
        for checker in Global.checkers:
            item = QStandardItem(checker.strip())
            item.setFont(self.font)
            item.setEditable(False)
            item.setBackground(self.brushForUnselected)
            checker not in self.checkers(project) or item.setBackground(self.brushForSelected)
            self.modelInCheckerListView.appendRow(item)


    def _initializeProjectList(self):
        self.projectCombo.clear()
        self.projectCombo.addItems(self.projects())
        self.projectCombo.setCurrentIndex(self.currentProjectIndex())


    def _initializeSelectedCheckerList(self):
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
        self._initializeSelectedCheckerList()
        self._initializeCheckerList()


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


    def _configurationChanged(self):
        temporary = {}
        self.data['temporary'] = None
        project = self.projectCombo.currentText()
        if project != 'New project' and temporary.setdefault('project', None) != project:
            checkers = self.checkers(project)
            temporary['project'] = project
            temporary['checkers'] = checkers
            temporary['tip'] = {}
            temporary['detail'] = {}
            for i in checkers:
                temporary['tip'][i] = self.tip(project, i)
                temporary['detail'][i] = self.detail(project, i)
            self.data['temporary'] = temporary


    def setLocation(self, location):
        self.data.clear()
        self.data['location'] = location
        self.locationChanged.emit()


    def location(self):
        return self.data.setdefault('location', '')


    def projects(self):
        return self.data.setdefault('projects', ['New project', 'Change location'])


    def setProjects(self, projects):
        self.data['projects'] = projects
        self.data['projects'].append('New project')
        self.data['projects'].append('Change location')


    def setCurrentProjectIndex(self):
        self._configurationChanged()
        self.deleteButton.setEnabled(False)
        project = self.projectCombo.currentText()
        ('New project' == project or 'Change location' == project) or self.deleteButton.setEnabled(True)
        if 'Change location' == project:
            QDialog.Accepted == LocationDialog(self).exec_() or self.projectCombo.setCurrentIndex(0)
        else:
            index = self.projectCombo.currentIndex()
            self.data['project'] = index if index > -1 else 0

        self._initializeCheckerList()
        self._initializeSelectedCheckerList()
        self._setNextButtonState()


    def currentProjectIndex(self):
        return self.data.setdefault('project', 0)


    def checkers(self, project):
        '''
        https://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep
        '''
        self.data.setdefault('checkers', {})
        return copy.deepcopy(self.data['checkers'].setdefault(project, []))


    def setCheckers(self, project, checkers):
        self._configurationChanged()
        self.data.setdefault('checkers', {})
        self.data['checkers'][project] = checkers


    def tip(self, project, checker):
        self.data.setdefault('tip', {})
        self.data['tip'].setdefault(project, {})
        return copy.deepcopy(self.data['tip'][project].setdefault(checker, ''))


    def setTip(self, project, checker, tip):
        self.data.setdefault('tip', {})
        self.data['tip'].setdefault(project, {})
        self.data['tip'][project][checker] = tip


    def detail(self, project, checker):
        self.data.setdefault('detail', {})
        self.data['detail'].setdefault(project, {})
        return copy.deepcopy(self.data['detail'][project].setdefault(checker, []))


    def setDetail(self, project, checker, detail):
        self.data.setdefault('detail', {})
        self.data['detail'].setdefault(project, {})
        self.data['detail'][project][checker] = detail


    def addChecker(self):
        if self.selectionModelInCheckerListView.hasSelection():
            project = self.projectCombo.currentText()
            index = self.selectionModelInCheckerListView.currentIndex()
            text = self.modelInCheckerListView.itemFromIndex(index).text()
            checkers = self.checkers(project)
            text in checkers or checkers.append(text)
            self.setCheckers(project, checkers)
            self._updateBothCheckerListViews()
            self._setNextButtonState()


    def removeChecker(self):
        if self.selectionModelInSelectedCheckerListView.hasSelection():
            project = self.projectCombo.currentText()
            index = self.selectionModelInSelectedCheckerListView.currentIndex()
            text = self.modelInSelectedCheckerListView.itemFromIndex(index).text()
            checkers = self.checkers(project)
            checkers.remove(text)
            self.setCheckers(project, checkers)
            self._updateBothCheckerListViews()
            self._setNextButtonState()


    def initializeData(self):
        def _initializeProjects():
            for root, subdirs, filenames in os.walk(self.location()):
                self.setProjects(subdirs)
                break

        def _initializeCheckers():
            location = self.location()
            for project in self.projects():
                source = location + '/' + project + '/checkers.csv'
                if os.access(source, os.F_OK):
                    with open(source, 'rb') as csvfile:
                        reader = csv.reader(csvfile, dialect=csv.excel)
                        self.setCheckers(project, [i[0].decode('utf-8') for i in reader])

        def _initializeTips():
            location = self.location()
            for project in self.projects():
                checkers = self.checkers(project)
                source = location+'/'+project+'/tip'
                if os.access(source, os.F_OK):
                    for tip in os.walk(source).next()[2]:
                        if tip.rpartition('.')[0] in checkers:
                            with open(source+'/'+tip, 'r') as f:
                                self.setTip(project, tip.rpartition('.')[0], f.read().strip())

        def _initializeDetails():
            location = self.location()
            for project in self.projects():
                checkers = self.checkers(project)
                source = location+'/'+project+'/detail'
                if os.access(source, os.F_OK):
                    for detail in os.walk(source).next()[2]:
                        if detail.rpartition('.')[0] in checkers and detail.rpartition('.')[0] in Global.detail:
                            with open(source+'/'+detail, 'rb') as csvfile:
                                reader = csv.reader(csvfile, dialect=csv.excel)
                                self.setDetail(project, detail.rpartition('.')[0], [i for i in reader])

        if not len(self.data.setdefault('projects', [])):
            _initializeProjects()
            _initializeCheckers()
            _initializeTips()
            _initializeDetails()

        self._configurationChanged()
        self._initializeProjectList()
        self._initializeCheckerList()
        self._initializeSelectedCheckerList()
        self._setNextButtonState()


    def reset(self):
        location = self.location()
        self.data.clear()
        self.setLocation(location)


    def quit(self):
        self.close()


    def deleteProject(self):
        'New project' == self.projectCombo.currentText() or DeleteProjectDialog(self).exec_()
        self.reset()


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
