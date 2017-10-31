# -*- coding: utf-8 -*-

import os
import re
import sys
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

from MayaTools.check_scene.load_ui import loadCreateCheckerUI
loadCreateCheckerUI()
from MayaTools.check_scene.create_checker.ui_pm_main import Ui_PM_View
from MayaTools.check_scene.create_checker.ui_details_window import Ui_DetailsWindow
from MayaTools.check_scene.create_checker.dialog import (DeleteDialog, DetailsDialog, ChooseDialog)
import MayaTools.check_scene.create_checker.details_widgets as details_widgets
reload(details_widgets)


suite = set([
    'check overlapping vertices',
    'check n-gons',
    'check lamina faces',
    'check shader names',
    'check external file path',
    'check transformations',
    'check intermediate node',
    'check poly count'
])

g_editable_templete = {
    "check transformations"       : "no",
    "check overlapping vertices"  : "no",
    "check n-gons"                : "no",
    "check lamina faces"          : "no",
    "check intermediate node"     : "no",
    "check poly count"            : "yes",
    "check shader names"          : "yes",
    "check external file path"    : "no"
}

g_details_templete = {
    "check overlapping vertices"  : 0,
    "check n-gons"                : 0,
    "check lamina faces"          : 0,
    "check transformations"       : 0,
    "check shader names"          : [],
    "check external file path"    : 0,
    "check intermediate node"     : 0,
    "check poly count"            : {
        "Verts"                   : "0",
        "Edges"                   : "0",
        "Faces"                   : "0",
        "Tris"                    : "0",
        "UVs"                     : "0"
    }
}

g_whatsthis_templete = {
    "check transformations"       : "Find the transform nodes whose transformations aren't frozen and their pivots aren't centered.",
    "check overlapping vertices"  : "Find overlapping vetices.",
    "check n-gons"                : "Find n-gons(faces with more than 4 sides).",
    "check lamina faces"          : "Find lamina faces(faces sharing all edges).",
    "check intermediate node"     : "Find intermediate mesh nodes.",
    "check shader names"          : "Determine if shaders are nameed correctly.",
    "check external file path"    : "Find the file nodes which are outside the current maya work directory.",
    "check poly count"            : "Check poly count, just like `Disply->Heads Up Display->Poly Count`."
}


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)


class DetailsWindow(QMainWindow, Ui_DetailsWindow):
    def __init__(self, parent=None, suite=None, project=None, project_dir=None):
        super(DetailsWindow, self).__init__(parent)
        self.data = {}
        self.data['test'] = list(suite)
        self.data['details'] = {}
        self.template = None
        self.project = project
        self.project_dir = project_dir
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.model = QStandardItemModel(self)
        self.projectList.setModel(self.model)
        self.projectListSelectionModel = self.projectList.selectionModel()
        self.setWindowTitle(self.project_dir+u'/'+self.project)

        self.read_suite()

        self.projectListSelectionModel.selectionChanged.connect(self.setDetails)
        self.previousButton.clicked.connect(self.previous)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.quite)


    def read_suite(self):
        if self.data['test'] is not None and self.project is not None:
            font = QFont('OldEnglish', 10, QFont.Bold)
            for i in (QStandardItem(item) for item in self.data['test']):
                i.setFont(font)
                i.setEditable(False)
                self.model.appendRow(i)

            if 'New project' == self.project:
                template = os.path.dirname(os.path.realpath(os.path.abspath(__file__))) + '\\templete.json'
            else:
                template = self.project_dir + u'\\' + self.project + u'.json'

            with open(template, 'r') as t:
                self.template = json.load(t, encoding='utf-8')

            self.data[u'editable'] = {k : self.template[u'editable'].setdefault(k, g_editable_templete[k]) for k in self.data[u'test']}
            self.data[u'details'] = {k : self.template[u'details'].setdefault(k, g_details_templete[k]) for k in self.data[u'test']}
            self.data[u'whatsThis'] = {k : self.template[u'whatsThis'].setdefault(k, g_whatsthis_templete[k]) for k in self.data[u'test']}


    def quite(self):
        self.close()


    def save(self):
        destination = pm.fileDialog2(cap='Save As',
                                     ds=2,
                                     fm=0,
                                     dir=self.project_dir,
                                     ff='All JSON Files (*.json)',
                                     okc='Save')

        if destination is not None:
            with open(destination[0], 'w') as d:
                json.dump(self.data, d, encoding='utf-8', indent=4)

            self.setWindowTitle(destination[0])


    def previous(self):
        self.quite()
        mayaWindow = getMayaWindow()
        main_window = MainWindow(mayaWindow, self.project_dir)
        main_window.show()

    def setDetails(self):
        index = self.projectListSelectionModel.currentIndex()
        item = self.model.itemFromIndex(index).text()

        if u'check shader names' == item:
            details_widgets.checkShaderNameWidget(self)
        elif u'check lamina faces' == item:
            details_widgets.checkLaminaFacesWidget(self)
        elif u'check poly count' == item:
            details_widgets.checkPolyCountWidget(self)
        elif u'check intermediate node' == item:
            details_widgets.checkIntermediateNodeWidget(self)
        elif u'check external file path' == item:
            details_widgets.checkExternalFilePathWidget(self)
        elif u'check n-gons' == item:
            details_widgets.checkNgonsWidget(self)
        elif u'check overlapping vertices' == item:
            details_widgets.checkOverlappingVerticesWidget(self)
        elif u'check transformations' == item:
            details_widgets.checkTransformationsWidget(self)


class MainWindow(QMainWindow, Ui_PM_View):
    def __init__(self, parent=None, project_dir=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.project_dir = project_dir
        self.test_model = QStandardItemModel(self)
        self.selected_model = QStandardItemModel(self)
        self.selectedList.setModel(self.selected_model)
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.brushForSelected = QBrush(Qt.GlobalColor.darkCyan)
        self.brushForUnselected = QBrush(Qt.NoBrush)
        for i in (QStandardItem(s) for s in suite):
            i.setFont(self.font)
            i.setEditable(False)
            self.test_model.appendRow(i)
        self.testList.setModel(self.test_model)
        self.selected = set()
        self.item_to_add = None # item text
        self.index_to_remove = None # item index
        self.nextButton.setEnabled(False)
        self.nextButton.clicked.connect(self.next)
        self.cancelButton.clicked.connect(self.quit)
        self.addButton.clicked.connect(self.add)
        self.removeButtion.clicked.connect(self.remove)
        self.resetButton.clicked.connect(self.reset)
        self.deleteButton.clicked.connect(self.delete)
        # pyside can no longer connect to an arbitary virtual method
        # https://groups.google.com/forum/#!topic/pyside-dev/JEyTfhbFoOg
        self.testList_selection = self.testList.selectionModel()
        self.testList_selection.selectionChanged.connect(self.currentItemToAdd)
        self.selectedlist_selection = self.selectedList.selectionModel()
        self.selectedlist_selection.currentChanged.connect(self.currentItemToRemove)
        self.actionReset.triggered.connect(self.reset)
        self.actionChoose.triggered.connect(self.choose)
        self.project_combo.currentIndexChanged.connect(self.read_suite)
        self.initProjectList()


    def _indicateSelectedTestItem(self):
        for i in xrange(self.test_model.rowCount()):
            item = self.test_model.item(i)
            item.setBackground(self.brushForUnselected)
            not item.text() in self.selected or item.setBackground(self.brushForSelected)


    def initProjectList(self):
        self.project_combo.clear()
        self.project_combo.addItem(u'New project')
        if self.project_dir is not None:
            self.setWindowTitle(self.project_dir)
            pattern = re.compile(r'([\w\d]+)\.json')
            files = ' '.join(os.listdir(self.project_dir))
            ret = re.findall(pattern, files)
            ret is None or self.project_combo.insertItems(0, ret)
            self.read_suite()


    def read_suite(self):
        current_project = self.project_combo.currentText() if self.project_combo.currentText() else u'New project'
        self.selected_model.clear()
        self.selected.clear()
        if current_project != 'New project':
            self.nextButton.setEnabled(True)
            project = self.project_dir + u'\\' + current_project + u'.json'
            with open(project, 'r') as f:
                suite = json.load(f, encoding='utf-8')
            self.selected = set(suite['test'])
            for i in self.selected:
                item = QStandardItem(i)
                item.setFont(self.font)
                item.setEditable(False)
                self.selected_model.appendRow(item)
        else:
            self.nextButton.setEnabled(False)

        self._indicateSelectedTestItem()


    def add(self):
        if self.text_to_add is None or self.text_to_add in self.selected:
            return
        item = QStandardItem(self.text_to_add)
        item.setFont(self.font)
        item.setEditable(False)
        self.selected_model.appendRow(item)
        self.selected.add(self.text_to_add)
        self.nextButton.setEnabled(True)
        self._indicateSelectedTestItem()


    def remove(self):
        if self.index_to_remove is None:
            return
        text = self.selected_model.itemFromIndex(self.index_to_remove).text()
        self.selected_model.removeRow(self.index_to_remove.row())
        self.selected.remove(text)
        self.index_to_remove = self.selectedList.selectionModel().currentIndex()
        if self.index_to_remove.row() < 0:
            self.index_to_remove = None
            self.nextButton.setEnabled(False)

        self._indicateSelectedTestItem()


    def currentItemToAdd(self):
        index = self.testList.selectionModel().currentIndex()
        item = self.test_model.itemFromIndex(index)
        self.text_to_add = item.text()


    def currentItemToRemove(self):
        self.index_to_remove = self.selectedList.selectionModel().currentIndex()


    def quit(self):
        self.close()


    def delete(self):
        project = self.project_combo.currentText()
        if 'New project' == project:
            self.reset()
        else:
            project = self.project_dir + '\\' + project + '.json'
            if os.access(project, os.F_OK):
                dialog = DeleteDialog(self)
                dialog.exec_()


    def reset(self):
        self.selected_model.clear()
        self.selected.clear()
        self.nextButton.setEnabled(False)
        self._indicateSelectedTestItem()


    def next(self):
        self.quit()
        mayaWindow = getMayaWindow()
        project = self.project_combo.currentText()
        details_window = DetailsWindow(mayaWindow, self.selected, project, self.project_dir)
        details_window.show()


    def choose(self):
        destination = pm.fileDialog2(cap='Open',
                                     ds=2,
                                     fm=3,
                                     okc='Open',
                                     hne=False)

        if destination is not None:
            self.project_dir = destination[0]
            self.setWindowTitle(destination[0])
            self.initProjectList()



def main():
    mayaWindow = getMayaWindow()
    window = MainWindow(parent=mayaWindow)
    window.show()
    ret = ChooseDialog(window).exec_()
    if QDialog.Rejected == ret:
        window.quit()
