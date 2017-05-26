# -*- coding: utf-8 -*-

import os
import sys
import json

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
        self.parent = parent
        self.setupUi(self)
        self.cancel_buttion.clicked.connect(self.closeDialog)
        self.save_buttion.clicked.connect(self.saveConfig)
        self.saved.connect(self.parent.save_slot)

    def closeDialog(self):
        self.close()

    def saveConfig(self):
        current_project = self.name_le.text()
        if len(current_project) > 0 and not current_project.isspace():
            self.saved.emit(current_project)
            self.closeDialog()

class SaveDialog(QtWidgets.QDialog, Ui_save_dialog):
    saved = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(SaveDialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.name_le.setText(self.parent.project_combo.currentText())
        self.no_button.clicked.connect((self.closeDialog))
        self.yes_button.clicked.connect((self.saveConfig))
        self.saved.connect(self.parent.save_slot)

    def closeDialog(self):
        self.close()

    def saveConfig(self):
        current_project = self.name_le.text()
        if len(current_project) > 0 and not current_project.isspace():
            self.saved.emit(current_project)
            self.closeDialog()

class DeleteDialog(QtWidgets.QDialog, Ui_deletePojectDailog):
    def __init__(self, file_path, parent=None):
        super(DeleteDialog, self).__init__(parent)
        self.setupUi(self)
        self.file_path = file_path
        self.parent = parent
        self.project_la.setText(
            'Delete configuration "{0}" ?'\
            .format(self.file_path.split('\\')[-1].split('.')[0])
        )

        self.path_la.setText('File path: {0}'.format(self.file_path))
        self.setWindowTitle(
            'Delete "{0}" ?'\
            .format(self.file_path.split('\\')[-1].split('.')[0])
        )

        self.yes_button.clicked.connect(self.delete)
        self.no_button.clicked.connect(self.cancel)

    def delete(self):
        os.remove(self.file_path)
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
        self.parent = parent
        self.project = self.parent.project_combo.currentText()
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Tile', 'Expected'])
        self.details_table.setModel(self.model)
        self.cancel_button.clicked.connect(self.closeDialog)
        self.reset_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save)

        def _init_title():
            with open('D:\\source\opensource\\FeelUOwn\\MyUtils\\GUI\\list_view\\templete.json', 'r', encoding='utf-8') as f:
                templete = json.load(f)
            for t in parent.selected:
                print(templete[t])

        _init_title()
        self.details_table.resizeColumnsToContents()

    def closeDialog(self):
        self.close()

    def reset(self):
        print('reset')

    def save(self):
        print('save')
