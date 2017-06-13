# -*- coding: utf-8 -*-

import sys
import json

import pymel.core as pm

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance

try:
    from UIMainWindow import Ui_MainWindow
except ImportError:
    sys.path.insert(0, 'D:\source\opensource\FeelUOwn\MyUtils\maya_script\polyCount')
    from UIMainWindow import Ui_MainWindow
    sys.path.remove('D:\source\opensource\FeelUOwn\MyUtils\maya_script\polyCount')

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.vertices = 0
        self.edges = 0
        self.faces = 0
        self.UVs =0
        self.datas = None
        self.maya_dir = pm.system.sceneName().dirname()
        self.setupUi(self)
        self.model = QStandardItemModel(self)
        self.treeView.setModel(self.model)
        self.selection = self.treeView.selectionModel()
        self.selection.currentChanged.connect(self.select)
        self.actionReset.triggered.connect(self.reset)
        self.read_datas2()

    def read_datas2(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Geometries'])
        report = self.maya_dir + '/report.json'
        with open(report, 'r') as report:
            self.datas = json.load(report, encoding='utf-8')
        for k, v in self.datas.items():
            if isinstance(v, dict):
                parent = self.model
                item = QStandardItem(k)
                item.setEditable(False)
                parent.appendRow(item)
                for t in v['transforms']:
                    parent = item
                    item = QStandardItem(t)
                    item.setEditable(False)
                    parent.appendRow(item)


    def read_datas(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Item', 'Expected', 'Actual', 'Status'])
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

    def select(self):
        index = self.selection.currentIndex()
        item = self.model.itemFromIndex(index)
        geometry = item.text()
        if geometry.startswith('nt.Mesh'):
            self.vertices += int(self.datas[geometry]['vertices'])
            self.vertices_le.setText(str(self.vertices))
            self.edges += int(self.datas[geometry]['edges'])
            self.edges_le.setText(str(self.edges))
            self.faces += int(self.datas[geometry]['faces'])
            self.faces_le.setText(str(self.faces))
            self.UVs += int(self.datas[geometry]['UVs'])
            self.uv_le.setText(str(self.UVs))
            geometry = eval('pm.' + geometry)
            pm.select(geometry, tgl=True)

    def reset(self):
        self.vertices = 0
        self.edges = 0
        self.faces = 0
        self.UVs = 0
        self.vertices_le.clear()
        self.edges_le.clear()
        self.faces_le.clear()
        self.uv_le.clear()
        pm.select(cl=True)

if __name__ == '__main__':
    window = MainWindow()
    window.show()
