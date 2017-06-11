# -*- coding: utf-8 -*-

import sys
import json

import pymel.core as pm
from PySide.QtGui import *
from PySide.QtCore import *
from shiboken import wrapInstance

try:
    from UIMainWindow import Ui_MainWindow
except ImportError:
    sys.path.insert(0, 'E:\develop\MyUtils\maya_script\polyCount')
    from UIMainWindow import Ui_MainWindow
    sys.path.remove('E:\develop\MyUtils\maya_script\polyCount')

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.datas = None
        self.maya_dir = pm.system.sceneName().dirname()
        self.setupUi(self)
        self.model = QStandardItemModel(self)
        self.read_datas()

    def read_datas(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Item', 'Expected', 'Actual', 'Status'])
        self.treeView.setModel(self.model)
        report = self.maya_dir + '/report.json'
        with open(report, 'r') as report:
            self.datas = json.load(report, encoding='utf-8')
        for k, v in self.datas.items():
            parent = self.model
            item = QStandardItem(k)
            item.setEditable(False)
            parent.appendRow(item)
            if isinstance(v, dict):
                parent = item
                for k1, v1 in v.items():
                    if 'transforms' == k1:
                        item = QStandardItem(k1)
                        item.setEditable(False)
                        parent.appendRow(item)
                        parent = item
                        for t in v1:
                            item = QStandardItem(t)
                            item.setEditable(False)
                            parent.appendRow(item)
                    else:
                        item = QStandardItem(k1)
                        item.setEditable(False)
                        parent.appendRow(item)
                        row = self.model.indexFromItem(item).row()
                        item = QStandardItem(str(v1))
                        item.setEditable(False)
                        parent.setChild(row, 2, item)
            else:
                row = self.model.indexFromItem(item).row()
                item = QStandardItem(str(v))
                item.setEditable(False)
                parent.setItem(row, 2, item)

            for c in range(0, 4):
                self.treeView.resizeColumnToContents(c)

if __name__ == '__main__':
    window = MainWindow()
    window.show()
