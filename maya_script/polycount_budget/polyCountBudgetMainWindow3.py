# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
from collections import deque

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
import maya.OpenMayaUI as apiUI

sys.path.insert(0, os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
from ui_polyCountBudget3 import Ui_polyCountBudgetMainWindow
from ui_addBudgetDialog import Ui_addBudgetDialog
from visualization import DashboardRender
import polycount
sys.path.remove(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))


MAYA_VERION = pm.mel.eval('getApplicationVersionAsFloat();')


gColorTuple = (
    ('color 1', QColor('#99e600')),
    ('color 2', QColor('#99cc00')),
    ('color 3', QColor('#99b300')),
    ('color 4', QColor('#9f991a')),
    ('color 5', QColor('#a48033')),
    ('color 6', QColor('#a9664d')),
    ('color 7', QColor('#ae4d66')),
    ('color 8', QColor('#b33380')),
    ('color 9', QColor('#a64086')),
    ('color 10', QColor('#994d8d')),
    ('color 11', QColor('#8d5a93')),
    ('color 12', QColor('#806699')),
    ('color 13', QColor('#8073a6')),
    ('color 14', QColor('#8080b3')),
    ('color 15', QColor(Qt.cyan)),
    ('color 16', QColor(Qt.darkCyan)),
    ('color 17', QColor(Qt.magenta)),
    ('color 18', QColor(Qt.darkMagenta)),
    ('color 19', QColor(Qt.green)),
    ('color 20', QColor(Qt.darkGreen)),
    ('color 21', QColor(Qt.yellow)),
    ('color 22', QColor(Qt.darkYellow)),
    ('color 23', QColor(Qt.blue)),
    ('color 24', QColor(Qt.darkBlue)),
)


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class DelegateInBudgetTableView(QStyledItemDelegate):
    def __init__(self, data=[], parent=None):
        # Items in table view must be editable.
        super(DelegateInBudgetTableView, self).__init__(parent)
        self.data = data
        self.parent = parent


    def createEditor(self, parent, option, index):
        col = index.column()
        row = index.row()
        # print parent.objectName()
        if col == 1:
            editor = QDoubleSpinBox(parent)
            editor.setMaximum(1000.0)
            editor.setMinimum(0)
            editor.setDecimals(1)
            row == 0 or editor.setMinimum(self.data[row-2][1])
            editor.setSuffix('K')
            editor.setFrame(False)

        return editor


    def setEditorData(self, editor, index):
        col = index.column()
        row = index.row()
        if col == 1:
            valueInModel = index.model().data(index, Qt.EditRole).partition('K')[0]
            editor.setValue(float(valueInModel))


    def setModelData(self, editor, model, index):
        col = index.column()
        row = index.row()
        if col == 1:
            editor.interpretText()
            value = editor.value()
            model.setData(index, str(value)+'K', Qt.EditRole)



    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)



class AddBudgetDialog(QDialog, Ui_addBudgetDialog):
    def __init__(self, parent):
        super(AddBudgetDialog, self).__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.triRadio.setEnabled(False)
        self.vertRadio.setEnabled(False)
        len(self.parent.budgetList) or self.triRadio.setEnabled(True)
        len(self.parent.budgetList) or self.vertRadio.setEnabled(True)
        self.addButton.setDefault(True)
        self.addButton.setEnabled(False)

        self._initColorComboBox()
        self._initPolyCountSpinBox()

        self.cancelButton.clicked.connect(self.cancelDialog)
        self.addButton.clicked.connect(self.addBudget)
        self.polyCountSpinBox.valueChanged.connect(self.activeAddButton)


    def _initColorComboBox(self):
        for name, color in gColorTuple:
            self.colorComboBox.addItem(name)
            index = int(name.partition(' ')[2]) - 1
            self.colorComboBox.setItemData(index, color, Qt.DecorationRole)


    def _initPolyCountSpinBox(self):
        self.polyCountSpinBox.setMinimum(0.0)
        not len(self.parent.budgetList) or self.polyCountSpinBox.setMinimum(float(self.parent.budgetList[-1][1]))


    def cancelDialog(self):
        self.reject()


    def activeAddButton(self):
        minimum = self.polyCountSpinBox.minimum()
        self.addButton.setEnabled(False)
        self.polyCountSpinBox.value() <= minimum or self.addButton.setEnabled(True)


    def addBudget(self):
        polyCount = str(self.polyCountSpinBox.value())
        lod = self.lodComboBox.currentText()
        primitive = 'Tris' if self.triRadio.isChecked() else 'Verts'
        colorIndex = self.colorComboBox.currentIndex()
        (len(self.parent.budgetList) and polyCount == self.parent.budgetList[-1][1]) or self.parent.budgetList.append((lod, polyCount, primitive, gColorTuple[colorIndex]))
        self._initPolyCountSpinBox()
        self.accept()



class PolyCountBudgetMainWindow(QMainWindow, Ui_polyCountBudgetMainWindow):
    def __init__(self, parent=None):
        super(PolyCountBudgetMainWindow, self).__init__(parent)
        self.budgetList = deque()
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.budgetModelInSetBudgetTableView = QStandardItemModel(self.setBudgetTableView)
        self.setBudgetTableView.setModel(self.budgetModelInSetBudgetTableView)
        self.selectionModelInTableView = QItemSelectionModel(self.budgetModelInSetBudgetTableView, self.setBudgetTableView)
        self.setBudgetTableView.setSelectionModel(self.selectionModelInTableView)
        self.delegateInBudgetTableView = DelegateInBudgetTableView(self.budgetList, self.setBudgetTableView)
        self.setBudgetTableView.setItemDelegate(self.delegateInBudgetTableView)
        self.modelInPolycountTreeView = QStandardItemModel(self.polycountTreeView)
        self.polycountTreeView.setModel(self.modelInPolycountTreeView)
        self.selectionModelInTreeView = QItemSelectionModel(self.modelInPolycountTreeView, self.polycountTreeView)
        self.polycountTreeView.setSelectionModel(self.selectionModelInTreeView)
        self.viewMenu.addAction(self.budgetDock.toggleViewAction())
        self.dashboard = DashboardRender(self.budgetList, self)
        self.setCentralWidget(self.dashboard)
        self.setBudgetTableView.mouseDoubleClickEvent = self._mouseDoubleClickEventInSetBudgetTableView
        self.polycountTreeView.mouseDoubleClickEvent  = self._mouseDoubleClickEventInPolycountTreeView
        self.polycountTreeView.mousePressEvent        = self._mousePressEventInTreeView

        self._displayBudget()

        self.resetAction.triggered.connect(self.resetBudget)
        self.selectionModelInTreeView.selectionChanged.connect(self.selectMayaObjectFromView)


    def _displayBudget(self):
        self.budgetModelInSetBudgetTableView.clear()
        index = 0
        for col in ('LOD', 'Budget', 'Tris/Verts', 'Color'):
            item = QStandardItem(col)
            item.setFont(self.font)
            # item.setEditable(False)
            self.budgetModelInSetBudgetTableView.setHorizontalHeaderItem(index, item)
            index += 1

        for lod, budget, primitiveType, color in self.budgetList:
            item = QStandardItem(lod)
            item.setFont(self.font)
            # item.setEditable(False)
            self.budgetModelInSetBudgetTableView.appendRow(item)
            row = self.budgetModelInSetBudgetTableView.indexFromItem(item).row()

            item = QStandardItem(budget+'K')
            item.setFont(self.font)
            # item.setEditable(False)
            self.budgetModelInSetBudgetTableView.setItem(row, 1, item)

            item = QStandardItem(primitiveType)
            item.setFont(self.font)
            # item.setEditable(False)
            self.budgetModelInSetBudgetTableView.setItem(row, 2, item)

            item = QStandardItem(color[0])
            item.setFont(self.font)
            # item.setEditable(False)
            item.setData(color[1], Qt.DecorationRole)
            self.budgetModelInSetBudgetTableView.setItem(row, 3, item)

        self.setBudgetTableView.resizeColumnsToContents()
        self.dashboard.moveHand(0)
        self.dashboard.update()


    def _mouseDoubleClickEventInSetBudgetTableView(self, event):
        button = event.button()
        if button == Qt.LeftButton:
            if self.selectionModelInTableView.hasSelection():
                row = self.selectionModelInTableView.currentIndex().row()
                # TODO: Add delegate, interactive with the user.
            else:
                ret = AddBudgetDialog(self).exec_()
                ret == QDialog.Rejected or self._displayBudget()

        QTableView.mouseDoubleClickEvent(self.setBudgetTableView, event)


    def resetBudget(self):
        self.budgetList.clear()
        self.budgetModelInSetBudgetTableView.clear()
        self.dashboard.update()


    def _displayPolyCountGroupByAsset(self, hierarchy, parent=None):
        if parent is not None:
            for root in hierarchy.keys():
                item = QStandardItem(root)
                item.setFont(self.font)
                item.setEditable(False)
                parent.appendRow(item)
                row = self.modelInPolycountTreeView.indexFromItem(item).row()
                parent2 = item

                item = QStandardItem(str(hierarchy[root]['Tris']))
                item.setFont(self.font)
                item.setEditable(False)
                parent.setChild(row, 1, item)

                item = QStandardItem(str(hierarchy[root]['Verts']))
                item.setFont(self.font)
                item.setEditable(False)
                parent.setChild(row, 2, item)

                self._displayPolyCountGroupByAsset(hierarchy[root]['children'], parent2)


    def _displayPolyCountInTreeView(self, polyCount):
        # Display total poly count first
        self.scene = pm.system.sceneName().rpartition('/')[2].partition('.')[0]
        item = QStandardItem(self.scene)
        item.setFont(self.font)
        item.setEditable(False)
        self.modelInPolycountTreeView.appendRow(item)
        parent = item

        item = QStandardItem(str(polyCount['Tris']))
        item.setFont(self.font)
        item.setEditable(False)
        self.modelInPolycountTreeView.setItem(0, 1, item)

        item = QStandardItem(str(polyCount['Verts']))
        item.setFont(self.font)
        item.setEditable(False)
        self.modelInPolycountTreeView.setItem(0, 2, item)

        # Display the poly count of each asset.
        self._displayPolyCountGroupByAsset(polyCount['hierarchy'], parent)


    def _mouseDoubleClickEventInPolycountTreeView(self, event):
        polycount.getPolyCountGroupByContainer()
        scene_path = pm.system.sceneName().dirname()
        path = pm.fileDialog2(cap='Open', ds=2, fm=1, dir=scene_path, okc='Open', ff='All Json Files (*.json)')
        if path is not None:
            with open(path[0], 'r') as source:
                polyCount = json.load(source, encoding='utf-8')

            index = 0
            self.modelInPolycountTreeView.clear()
            for header in ('Asset', 'Tris', 'Verts'):
                item = QStandardItem(header)
                item.setFont(self.font)
                item.setEditable(False)
                self.modelInPolycountTreeView.setHorizontalHeaderItem(index, item)
                index += 1

            self._displayPolyCountInTreeView(polyCount)

            self.polycountTreeView.resizeColumnToContents(0)
            self.polycountTreeView.resizeColumnToContents(1)
            self.polycountTreeView.resizeColumnToContents(2)

        QTreeView.mouseDoubleClickEvent(self.polycountTreeView, event)


    def _selectTransformsFromContainer(self, container=None):
        if isinstance(container, pm.nt.Container):
            transforms = []
            queue = deque(container.getNodeList())
            while len(queue):
                node = queue.popleft()
                if isinstance(node, pm.nt.Transform):
                    transforms.append(node)
                elif isinstance(node, pm.nt.Container):
                    queue.extend(node.getNodeList())

            not len(transforms) or pm.select(transforms, r=True)


    def selectMayaObjectFromView(self):
        self.dashboard.moveHand(0)
        if self.selectionModelInTreeView.hasSelection():
            index = self.selectionModelInTreeView.selectedRows()[0]
            text = self.modelInPolycountTreeView.itemFromIndex(index).text()

            index = self.selectionModelInTreeView.selectedRows(1)[0]
            count = int(self.modelInPolycountTreeView.itemFromIndex(index).text())
            self.dashboard.moveHand(count)

            if self.scene == text:
                # Select all polygon geometries.
                transforms = pm.listTransforms(type='mesh')
                pm.select(transforms, r=True)
            else:
                # Select individual asset.
                node = pm.ls(text)[0]
                not isinstance(node, pm.nt.DagContainer) or pm.select(node, r=True)
                not isinstance(node, pm.nt.Container) or self._selectTransformsFromContainer(node)


    def _mousePressEventInTreeView(self, event):
        '''
        https://stackoverflow.com/questions/2761284/is-it-possible-to-deselect-in-a-qtreeview-by-clicking-off-an-item
        '''
        self.polycountTreeView.clearSelection()
        QTreeView.mousePressEvent(self.polycountTreeView, event)



if __name__ == '__main__':
    window = PolyCountBudgetMainWindow()
    window.show()
