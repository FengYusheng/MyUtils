# -*- coding: utf-8 -*-

import os
import re
import sys
import configparser

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from ui_pm_view import Ui_PM_View
from dialog import (NewSaveDialog, SaveDialog)

suite = set([
    'overlapping vertices',
    'n-gons counts',
    'overlapping faces',
    'shader name',
    'texture file path',
    'pivot and transform'
])

class MainWindow(QtWidgets.QMainWindow, Ui_PM_View):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.test_model = QtGui.QStandardItemModel(self)
        self.selected_model = QtGui.QStandardItemModel(self)
        self.selectedList.setModel(self.selected_model)
        items = [QtGui.QStandardItem(s) for s in suite]
        for i in items:
            i.setEditable(False)
            self.test_model.appendRow(i)
        self.testList.setModel(self.test_model)
        self.selected = set()
        self.item_to_add = None # item text
        self.index_to_remove = None # item index
        self.isChanged = False
        self.current_project = 'New project'

        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.quit)
        self.addButton.clicked.connect(self.add)
        self.removeButtion.clicked.connect(self.remove)
        self.testList.selectionModel().selectionChanged.connect(self.currentItemToAdd)
        self.selectedList.selectionModel().currentChanged.connect(self.currentItemToRemove)
        self.actionReset.triggered.connect(self.reset)
        self.project_combo.currentTextChanged.connect(self.read_config)

        self._init_project_list()

    def _init_project_list(self):
        pattern = re.compile(r'([\w\d]+)\.ini')
        files = ' '.join(os.listdir())
        ret = re.findall(pattern, files)
        if ret is not None:
            self.project_combo.insertItems(0, ret)
        self.current_project = self.project_combo.currentText()
        self.read_config()

    def read_config(self):
        self.current_project = self.project_combo.currentText()
        self.selected_model.clear()
        self.selected.clear()
        if self.current_project != 'New project':
            project = self.current_project + '.ini'
            config = configparser.ConfigParser()
            config.read(project, encoding='utf-8')
            self.selected = set(i for i in config['TEST SUITE'])
            for i in self.selected:
                item = QtGui.QStandardItem(i)
                item.setEditable(False)
                self.selected_model.appendRow(item)

    def add(self):
        if self.text_to_add is None or self.text_to_add in self.selected:
            return
        item = QtGui.QStandardItem(self.text_to_add)
        item.setEditable(False)
        self.selected_model.appendRow(item)
        self.selected.add(self.text_to_add)
        self.isChanged = True


    def remove(self):
        if self.index_to_remove is None:
            return
        text = self.selected_model.itemFromIndex(self.index_to_remove).text()
        self.selected_model.removeRow(self.index_to_remove.row())
        self.selected.remove(text)
        self.index_to_remove = self.selectedList.selectionModel().currentIndex()
        if self.index_to_remove.row() < 0:
            self.index_to_remove = None
        self.isChanged = True

    def currentItemToAdd(self):
        index = self.testList.selectionModel().currentIndex()
        item = self.test_model.itemFromIndex(index)
        self.text_to_add = item.text()

    def currentItemToRemove(self):
        self.index_to_remove = self.selectedList.selectionModel().currentIndex()

    def quit(self):
        QtWidgets.QApplication.quit()

    def save(self):
        if self.isChanged is True and len(self.selected) > 0:
            dialog = NewSaveDialog(self) if self.current_project == 'New project' else SaveDialog(self)
            dialog.exec_()

    def delete(self):
        pass

    def save_slot(self, project):
        project_name = project + '.ini'
        config = configparser.ConfigParser()
        config['TEST SUITE'] = {}
        for s in self.selected:
            config['TEST SUITE'][s] = 'on'
        with open(project_name, 'w', encoding='utf-8') as f:
            config.write(f)
        self.isChanged = False
        if self.current_project != project:
            self.project_combo.insertItem(0, project)
            self.project_combo.setCurrentIndex(0)
        self.current_project = project

    def reset(self):
        self.selected_model.clear()
        self.selected.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
