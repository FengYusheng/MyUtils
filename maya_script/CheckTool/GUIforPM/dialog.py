# -*- coding: utf-8 -*-

import os
import sys
import json

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

import pymel.core as pm

from MayaTools.check_scene.create_checker.ui_new_save_dialog import Ui_new_save
from MayaTools.check_scene.create_checker.ui_save_dialog import Ui_save_dialog
from MayaTools.check_scene.create_checker.ui_delete_dialog import Ui_deletePojectDailog
from MayaTools.check_scene.create_checker.ui_details_dialog import Ui_details_dialog
from MayaTools.check_scene.create_checker.ui_choose_dialog import Ui_chooseDialog


g_current_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))


class NewSaveDialog(QDialog, Ui_new_save):
    # A signal need to be defined on class level
    # https://stackoverflow.com/questions/37630233/pyqt5-signal-pyqtsignal-no-method-connect
    saved = Signal(str)
    def __init__(self, parent=None):
        super(NewSaveDialog, self).__init__(parent)
        self.parent = parent # details dialog
        self.main_window = self.parent.parent # main window
        self.setAttribute(Qt.WA_DeleteOnClose, True)
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
        test_data = {}
        project_name = os.path.dirname(g_current_dir) + '\\project\\' + project + '.json'
        current_project = self.main_window.project_combo.currentText()
        self.parent.setWindowTitle(project)
        # test_data['test'] = {s : 'on' for s in self.main_window.selected}
        test_data['test'] = list(self.main_window.selected)
        test_data['details'] = self.parent.details
        test_data['editable'] = g_editable_templete
        with open(project_name, 'w') as f:
            json.dump(test_data, f, indent=4, encoding='utf-8')

        if current_project != project:
            self.main_window.project_combo.insertItem(0, project)
            self.main_window.project_combo.setCurrentIndex(0)

class SaveDialog(QDialog, Ui_save_dialog):
    saved = Signal(str)
    def __init__(self, parent=None):
        super(SaveDialog, self).__init__(parent)
        self.parent = parent # details dialog
        self.main_window = self.parent.parent # main window
        self.setAttribute(Qt.WA_DeleteOnClose, True)
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
        test_data = {}
        project_name = os.path.dirname(g_current_dir) + '\\project\\' + project + '.json'
        current_project = self.main_window.project_combo.currentText()
        self.parent.setWindowTitle(project)
        # test_data['test'] = {s : 'on' for s in self.main_window.selected}
        test_data['test'] = list(self.main_window.selected)
        test_data['details'] = self.parent.details
        test_data['editable'] = g_editable_templete
        with open(project_name, 'w') as f:
            json.dump(test_data, f, indent=4, encoding='utf-8')

        if current_project != project:
            self.main_window.project_combo.insertItem(0, project)
            self.main_window.project_combo.setCurrentIndex(0)


class DeleteDialog(QDialog, Ui_deletePojectDailog):
    def __init__(self, parent=None):
        super(DeleteDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.parent = parent
        self.project = self.parent.project_combo.currentText()
        self.project_la.setText(
            'Delete configuration "{0}" ?'\
            .format(self.project)
        )

        project = os.path.dirname(g_current_dir) + '\\project\\' + self.project + '.json'
        self.path_la.setText('File path: {0}'.format(project))
        self.setWindowTitle(
            'Delete "{0}" ?'\
            .format(self.project)
        )

        self.yes_button.clicked.connect(self.delete)
        self.no_button.clicked.connect(self.cancel)

    def delete(self):
        project = os.path.dirname(g_current_dir) + '\\project\\' + self.project + '.json'
        os.remove(project)
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

class DetailsDialog(QDialog, Ui_details_dialog):
    def __init__(self, parent=None):
        super(DetailsDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.row = 0
        self.details = {}
        self.parent = parent
        self.project = self.parent.project_combo.currentText()
        self.setWindowTitle(self.project)
        self.model = QStandardItemModel()
        self.details_table.setModel(self.model)
        self.cancel_button.clicked.connect(self.closeDialog)
        self.reset_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save)
        self.init_table()

    def init_table(self, reset=False):
        project = os.path.dirname(g_current_dir) + '\\project\\' + self.project + '.json'
        templete = g_current_dir + '\\templete.json'
        project = project if os.access(project, os.F_OK) and not reset else templete
        with open(project, 'r') as f:
            templete = json.load(f, encoding='utf-8')

        self.row = 0
        self.model.setHorizontalHeaderLabels(['Tile', 'Expected'])
        brush = QBrush(Qt.GlobalColor.darkGray)
        for t in self.parent.selected:
            if 'shader name' == t:
                item = QStandardItem('shader name suffix')
                item.setEditable(False)
                self.model.setItem(self.row, 0, item)
                if 'shader name suffix' in templete['details']:
                    item = QStandardItem(templete['details']['shader name suffix'])
                else:
                    item = QStandardItem(g_details_templete['shader name suffix'])
                self.model.setItem(self.row, 1, item)
                self.row += 1
                item = QStandardItem('shader name prefix')
                item.setEditable(False)
                self.model.setItem(self.row, 0, item)
                if 'shader name prefix' in templete['details']:
                    item = QStandardItem(templete['details']['shader name prefix'])
                else:
                    item = QStandardItem(g_details_templete['shader name prefix'])
                self.model.setItem(self.row, 1, item)
                self.row += 1
            else:
                if t in templete['details']:
                    item = QStandardItem(t)
                    item.setEditable(False)
                    'yes' == templete['editable'][t] or item.setBackground(brush)
                    self.model.setItem(self.row, 0, item)
                    item = QStandardItem(templete['details'][t])
                    # not '(Uneditable)' in templete['details'][t] or item.setEditable(False)
                    if 'no' == templete['editable'][t] :
                        item.setEditable(False)
                        item.setBackground(brush)
                    self.model.setItem(self.row, 1, item)
                    self.row += 1
                else:
                    item = QStandardItem(t)
                    item.setEditable(False)
                    'yes' == g_editable_templete[t] or item.setBackground(brush)
                    self.model.setItem(self.row, 0, item)
                    item = QStandardItem(g_details_templete[t])
                    # not '(Uneditable)' in templete['details'][t] or item.setEditable(False)
                    if 'no' == g_editable_templete[t] :
                        item.setEditable(False)
                        item.setBackground(brush)
                    self.model.setItem(self.row, 1, item)
                    self.row += 1

        self.details_table.resizeColumnsToContents()
        self.details_table.resizeRowsToContents()

    def closeDialog(self):
        self.close()

    def reset(self):
        self.model.clear()
        self.init_table(reset=True)

    def save(self):
        self.details = {self.model.item(row, 0).text() : self.model.item(row, 1).text() for row in range(0, self.row)}
        self.project = self.parent.project_combo.currentText()
        dialog = NewSaveDialog(self) if self.project == 'New project' else SaveDialog(self)
        dialog.exec_()
        self.closeDialog()


class ChooseDialog(QDialog, Ui_chooseDialog):
    def __init__(self, parent):
        super(ChooseDialog, self).__init__(parent)
        self.project_dir = None
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.okbutton.setDefault(True)
        self.okbutton.setEnabled(False)

        self.cancelButton.clicked.connect(self.quite)
        self.chooseButton.clicked.connect(self.choose)
        self.okbutton.clicked.connect(self.setProject)

    def setProject(self):
        self.parent.project_dir = self.project_dir
        self.parent.setWindowTitle(self.project_dir)
        self.parent.initProjectList()
        self.accept()

    def quite(self):
        self.reject()

    def choose(self):
        destination = pm.fileDialog2(cap='Open',
                                     ds=2,
                                     fm=3,
                                     okc='Open')

        if destination is not None:
            self.chooseLineEdit.setText(destination[0])
            self.project_dir = destination[0]
            not self.project_dir or self.okbutton.setEnabled(True)
