# -*- coding: utf-8 -*-

import sys
import os

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide import __version__
    from shiboken import wrapInstance

import pymel.core as pm

sys.path.insert(0, os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
import ui_polyCountBudget as ui_budget
sys.path.remove(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))

MAYA_VERION = int(pm.mel.eval('getApplicationVersionAsFloat();'))


class PolyCountBudget(QWidget, ui_budget.Ui_polyCountBudget):
    def __init__(self, parent=None):
        super(PolyCountBudget, self).__init__(parent)
        self.budget = []
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.addButton.setEnabled(False)
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.model = QStandardItemModel(self)
        self.budgetTableView.setModel(self.model)


        self.startBudgetSpinBox.valueChanged.connect(self.isAddButtonActivated)
        self.endBudgetSpinBox.valueChanged.connect(self.isAddButtonActivated)
        self.addButton.clicked.connect(self.addBudget)

        self.initBudgetTable()


    def initBudgetTable(self):
        index = 0
        for i in ('LOD', 'From', 'To'):
            item = QStandardItem(i)
            item.setFont(self.font)
            self.model.setHorizontalHeaderItem(index, item)
            index += 1

        for i in ('Extremely low', 'low', 'Medium', 'High', 'Very high', 'Extremely high'):
            item = QStandardItem(i)
            item.setFont(self.font)
            self.model.appendRow(item)
            row = self.model.indexFromItem(item).row()
            item = QStandardItem('0')
            item.setFont(self.font)
            self.model.setItem(row, 1, item)
            item = QStandardItem('0')
            item.setFont(self.font)
            self.model.setItem(row, 2, item)

            self.budget.append((index, i, 0, 0))

        # self.budgetTableView.resizeColumnsToContents()


    def isAddButtonActivated(self):
        fromValue = self.startBudgetSpinBox.value()
        toValue = self.endBudgetSpinBox.value()
        if fromValue < toValue:
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)


    def addBudget(self):
        fromValue = str(self.startBudgetSpinBox.value())
        toValue = str(self.endBudgetSpinBox.value())
        tag = self.tagComboBox.currentText()
        # index = 0

        # self.model.clear()



if __name__ == '__main__':
    budget_widget = PolyCountBudget()
    budget_widget.show()
