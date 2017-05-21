# -*- coding: utf-8 -*-

import sys
import json
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from ui_treeview import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.data = None
        self.model = QtGui.QStandardItemModel(self)
        self.suiteButton.clicked.connect(self.suite2)

    def suite2(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Item', 'Status', 'Expected', 'Actual'])
        with open('../../maya_script/suite_reports.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        def _fill_data(parent, data):
            if isinstance(data, dict):
                for k, v in data.items():
                    item = QtGui.QStandardItem(k)
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
                        parent.appendRow(item)

        _fill_data(self.model, self.data)
        self.treeView.setModel(self.model)
        for c in range(0, 4):
            self.treeView.resizeColumnToContents(c)

    def suite(self):
        self.model.setHorizontalHeaderLabels(['Item', 'Status', 'Expected', 'Actual'])
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
