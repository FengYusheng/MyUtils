# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from ui_pm_view import Ui_PM_View

suite = set([
    'Overlapping ertices',
    'N-gons counts',
    'Overlapping faces',
    'Shader name',
    'Texture file path',
    'Pivot and transform'
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

        self.saveButton.clicked.connect(self.save)
        self.cancelButtion.clicked.connect(self.quit)
        self.addButton.clicked.connect(self.add)
        self.removeButtion.clicked.connect(self.remove)
        self.testList.selectionModel().selectionChanged.connect(self.currentItemToAdd)
        self.selectedList.selectionModel().currentChanged.connect(self.currentItemToRemove)

    def add(self):
        if self.text_to_add is None or self.text_to_add in self.selected:
            return
        item = QtGui.QStandardItem(self.text_to_add)
        item.setEditable(False)
        self.selected_model.appendRow(item)
        self.selected.add(self.text_to_add)


    def remove(self):
        if self.index_to_remove is None:
            return
        text = self.selected_model.itemFromIndex(self.index_to_remove).text()
        self.selected_model.removeRow(self.index_to_remove.row())
        self.selected.remove(text)
        self.index_to_remove = self.selectedList.selectionModel().currentIndex()
        if self.index_to_remove.row() < 0:
            self.index_to_remove = None

    def currentItemToAdd(self):
        index = self.testList.selectionModel().currentIndex()
        item = self.test_model.itemFromIndex(index)
        self.text_to_add = item.text()

    def currentItemToRemove(self):
        self.index_to_remove = self.selectedList.selectionModel().currentIndex()

    def quit(self):
        QtWidgets.QApplication.quit()

    def save(self):
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
