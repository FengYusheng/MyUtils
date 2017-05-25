# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from ui_new_save import Ui_new_save
from ui_save_dialog import Ui_save_dialog


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
        self.name_le.setText(self.parent.current_project)
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
