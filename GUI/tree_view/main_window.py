# -*- coding: utf-8 -*-

import sys
import json

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from ui_treeview import Ui_MainWindow
from dialog import FileDailog

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.data = None
        self.tests = None
        self.model = QtGui.QStandardItemModel(self)
        self.simpleButton.setVisible(False)
        # self.suiteButton.setEnabled(False)
        # self.suiteButton.clicked.connect(self.suite2)
        self.actionRead_configuration.triggered.connect(self.read_config)
        self.detailButton.clicked.connect(self.show_details)
        self.simpleButton.clicked.connect(self.show_simplicity)

    def _init_suite(self):
        if self.tests is None or not len(self.tests):
            return
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Item', 'Expected', 'Status', 'Actual'])
        for key, val in ((k, v) for k, v in self.tests.items()):
            item = QtGui.QStandardItem(key)
            item.setEditable(False)
            self.model.appendRow(item)
            row = self.model.indexFromItem(item).row()
            item = QtGui.QStandardItem(val)
            item.setEditable(False)
            self.model.setItem(row, 2, item)
            self.treeView.setModel(self.model)
            for c in range(0, 4):
                self.treeView.resizeColumnToContents(c)

    def show_simplicity(self):
        self.simpleButton.setVisible(False)
        self.detailButton.setVisible(True)
        self._init_suite()

    # def suite2(self):
    def show_details(self):
        self.simpleButton.setVisible(True)
        self.detailButton.setVisible(False)
        self.model.clear()
        # self._init_suite()
        self.model.setHorizontalHeaderLabels(['Item', 'Expected', 'Status', 'Actual'])
        with open('../../maya_script/suite_reports.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        def _fill_data(parent, data):
            if isinstance(data, dict):
                for k, v in data.items():
                    item = QtGui.QStandardItem(k)
                    item.setEditable(False)
                    parent.appendRow(item)
                    row = self.model.indexFromItem(item).row()
                    actual = str(v) if not isinstance(v, list) and not isinstance(v, dict) else '...'
                    if hasattr(parent, 'setItem'):
                        parent.setItem(row, 3, QtGui.QStandardItem(actual))
                    else:
                        parent.setChild(row, 3, QtGui.QStandardItem(actual))
                    if actual == '...':
                        _fill_data(item, v)
            elif isinstance(data, list):
                for d in data:
                    if isinstance(d, list) or isinstance(d, dict):
                        _fill_data(parent, d)
                    else:
                        item = QtGui.QStandardItem(str(d))
                        item.setEditable(False)
                        parent.appendRow(item)

        _fill_data(self.model, self.data)
        for c in range(0, 4):
            self.treeView.resizeColumnToContents(c)

    def suite(self):
        self.model.setHorizontalHeaderLabels(['Item', 'Expected', 'Status', 'Actual'])
        with open('../../maya_script/suite_reports.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        for k, v in self.data.items():
            item = QtGui.QStandardItem(k)
            self.model.appendRow(item)
            row = self.model.indexFromItem(item).row()
            actual = str(v) if not isinstance(v, list) else '...'
            self.model.setItem(row, 3, QtGui.QStandardItem(actual))

        self.treeView.setModel(self.model)
        # selectionModel() can't return an valid value unless call it after setModel.
        self.treeView.selectionModel().selectionChanged.connect(self.expand)
        for c in range(0, 4):
            self.treeView.resizeColumnToContents(c)

    def expand(self):
        index = self.treeView.selectionModel().currentIndex()
        parent = self.model.itemFromIndex(index)
        text = parent.text()
        if isinstance(self.data[text], list):
            for d in self.data[text]:
                for k, v in d.items():
                    item = QtGui.QStandardItem(k)
                    parent.appendRow(item)
                    row = self.model.indexFromItem(item).row()
                    actual = str(v) if not isinstance(v, list) else '...'
                    parent.setChild(row, 3, QtGui.QStandardItem(actual))

    def read_config(self):
        dialog = FileDailog()
        path = dialog.selectedFiles()[0] if dialog.exec_() else None
        if path is not None:
            with open(path, 'r', encoding='utf-8') as f:
                self.tests = json.load(f)
        self._init_suite()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
