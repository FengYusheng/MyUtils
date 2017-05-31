# -*- coding: utf-8 -*-

import os
import sys
import json
import configparser

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from ui_new_save import Ui_new_save
from ui_save_dialog import Ui_save_dialog
from delete_project_dialog import Ui_deletePojectDailog
from ui_details_dialog import Ui_details_dialog


class NewSaveDialog(QtWidgets.QDialog, Ui_new_save):
    # A signal need to be defined on class level
    # https://stackoverflow.com/questions/37630233/pyqt5-signal-pyqtsignal-no-method-connect
    saved = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(NewSaveDialog, self).__init__(parent)
        self.parent = parent # details dialog
        self.main_window = self.parent.parent # main window
        self.setupUi(self)
        self.cancel_buttion.clicked.connect(self.closeDialog)
        self.save_buttion.clicked.connect(self.saveConfig)
        self.saved.connect(self.save_slot)

    def closeDialog(self):
        self.close()

    def saveConfig(self):
        current_project = self.name_le.text()
        if len(current_project) > 0 \
        and not current_project.isspace() \
        and current_project != 'New project':
            self.saved.emit(current_project)
            self.closeDialog()

    def save_slot(self, project):
        project_name = project + '.ini'
        current_project = self.main_window.project_combo.currentText()
        self.parent.setWindowTitle(project)
        config = configparser.ConfigParser()
        config['TEST SUITE'] = {}
        for s in self.main_window.selected:
            config['TEST SUITE'][s] = 'on'
        with open(project_name, 'w', encoding='utf-8') as f:
            config.write(f)
        if current_project != project:
            self.main_window.project_combo.insertItem(0, project)
            self.main_window.project_combo.setCurrentIndex(0)

        project_name = project + '.json'
        with open(project_name, 'w', encoding='utf-8') as f:
            json.dump(self.parent.details, f, indent=4)

class SaveDialog(QtWidgets.QDialog, Ui_save_dialog):
    saved = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(SaveDialog, self).__init__(parent)
        self.parent = parent # details dialog
        self.main_window = self.parent.parent # main window
        self.setupUi(self)
        self.name_le.setText(self.main_window.project_combo.currentText())
        self.no_button.clicked.connect((self.closeDialog))
        self.yes_button.clicked.connect((self.saveConfig))
        self.saved.connect(self.save_slot)

    def closeDialog(self):
        self.close()

    def saveConfig(self):
        current_project = self.name_le.text()
        if len(current_project) > 0 \
        and not current_project.isspace() \
        and current_project != 'New project':
            self.saved.emit(current_project)
            self.closeDialog()

    def save_slot(self, project):
        project_name = project + '.ini'
        current_project = self.main_window.project_combo.currentText()
        self.parent.setWindowTitle(project)
        config = configparser.ConfigParser()
        config['TEST SUITE'] = {}
        for s in self.main_window.selected:
            config['TEST SUITE'][s] = 'on'
        with open(project_name, 'w', encoding='utf-8') as f:
            config.write(f)
        if current_project != project:
            self.main_window.project_combo.insertItem(0, project)
            self.main_window.project_combo.setCurrentIndex(0)

        project_name = project + '.json'
        with open(project_name, 'w', encoding='utf-8') as f:
            json.dump(self.parent.details, f, indent=4)

class DeleteDialog(QtWidgets.QDialog, Ui_deletePojectDailog):
    def __init__(self, parent=None):
        super(DeleteDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.project = self.parent.project_combo.currentText()
        self.project_la.setText(
            'Delete configuration "{0}" ?'\
            .format(self.project)
        )

        config = os.path.realpath(os.path.abspath(self.project+'.ini'))
        self.path_la.setText('File path: {0}'.format(config))
        self.setWindowTitle(
            'Delete "{0}" ?'\
            .format(self.project)
        )

        self.yes_button.clicked.connect(self.delete)
        self.no_button.clicked.connect(self.cancel)

    def delete(self):
        config = os.path.realpath(os.path.abspath(self.project+'.ini'))
        not os.access(config, os.F_OK) or os.remove(config)
        details = os.path.realpath(os.path.abspath(self.project+'.json'))
        not os.access(details, os.F_OK) or os.remove(details)
        self.parent.reset()
        self.parent.project_combo.removeItem(
            self.parent.project_combo.currentIndex()
        )

        self.parent.project_combo.setCurrentIndex(
            self.parent.project_combo.count()-1
        )

        self.close()

    def cancel(self):
        self.close()

class DetailsDialog(QtWidgets.QDialog, Ui_details_dialog):
    def __init__(self, parent=None):
        super(DetailsDialog, self).__init__(parent)
        self.setupUi(self)
        self.row = 0
        self.details = {}
        self.parent = parent
        self.project = self.parent.project_combo.currentText()
        self.setWindowTitle(self.project)
        self.model = QtGui.QStandardItemModel()
        self.details_table.setModel(self.model)
        self.cancel_button.clicked.connect(self.closeDialog)
        self.reset_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save)
        self._init_table()

    def _init_table(self, reset=False):
        details = self.project + '.json'
        details = os.path.realpath(os.path.abspath(details))
        details = details if os.access(details, os.F_OK) and not reset else os.path.realpath(os.path.abspath('templete.json'))
        with open(details, 'r', encoding='utf-8') as f:
            templete = json.load(f)

        self.row = 0
        self.model.setHorizontalHeaderLabels(['Tile', 'Expected'])
        for t in self.parent.selected:
            if 'shader name' == t:
                item = QtGui.QStandardItem('shader name suffix')
                item.setEditable(False)
                self.model.setItem(self.row, 0, item)
                item = QtGui.QStandardItem(templete['shader name suffix'])
                self.model.setItem(self.row, 1, item)
                self.row += 1
                item = QtGui.QStandardItem('shader name prefix')
                item.setEditable(False)
                self.model.setItem(self.row, 0, item)
                item = QtGui.QStandardItem(templete['shader name prefix'])
                self.model.setItem(self.row, 1, item)
                self.row += 1
            else:
                item = QtGui.QStandardItem(t)
                item.setEditable(False)
                self.model.setItem(self.row, 0, item)
                item = QtGui.QStandardItem(templete[t])
                not '(Uneditable)' in templete[t] or item.setEditable(False)
                self.model.setItem(self.row, 1, item)
                self.row += 1

        self.details_table.resizeColumnsToContents()
        self.details_table.resizeRowsToContents()

    def closeDialog(self):
        self.close()

    def reset(self):
        self.model.clear()
        self._init_table(reset=True)

    def save(self):
        path = self.project + '.json'
        path = os.path.realpath(os.path.abspath(path))
        self.details = {self.model.item(row, 0).text() : self.model.item(row, 1).text() for row in range(0, self.row)}
        self.project = self.parent.project_combo.currentText()
        dialog = NewSaveDialog(self) if self.project == 'New project' else SaveDialog(self)
        dialog.exec_()
