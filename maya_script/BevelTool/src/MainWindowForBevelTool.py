# -*- coding: utf-8 -*-
import copy

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from pyside2uic import compileUi
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from pysideuic import compileUi
    from PySide import __version__
    from shiboken import wrapInstance

import maya.OpenMayaUI as apiUI

import bevelTool
reload(bevelTool)
import ui_MainWindowForBevelTool
reload(ui_MainWindowForBevelTool)
import options
reload(options)



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class OptionDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(OptionDelegate, self).__init__(parent)
        self.font = QFont('OldEnglish', 10, QFont.Bold)


    def createEditor(self, parent, option, index):
        row = index.row()
        opt = index.model().item(row, 0).text()
        if opt in options.BOOLOPTIONS:
            editor = QComboBox(parent)
            editor.addItems(('True', 'False'))
            editor.setFont(self.font)
        elif 'mitering' == opt:
            editor = QComboBox(parent)
            editor.addItems(('Auto, 0', 'Uniform, 1', 'Patch, 2', 'Radial, 3', 'None, 4'))
            editor.setFont(self.font)
        elif 'miterAlong' == opt:
            editor = QComboBox(parent)
            editor.addItems(('Auto, 0', 'Center, 1', 'Edge, 2', 'Hard Edge, 3'))
            editor.setFont(self.font)
        else:
            editor = QLineEdit(parent)

        return editor


    def setEditorData(self, editor, index):
        row = index.row()
        opt = index.model().item(row, 0).text()
        data = index.model().data(index, Qt.EditRole)
        if opt in options.BOOLOPTIONS:
            data == 'True' or editor.setCurrentIndex(1)
            data == 'False' or editor.setCurrentIndex(0)
        elif 'mitering' == opt or 'miterAlong' == opt:
            editor.setCurrentIndex(int(data))
        else:
            editor.setText(data)


    def setModelData(self, editor, model, index):
        row = index.row()
        opt = index.model().item(row, 0).text()
        if opt in options.BOOLOPTIONS:
            data = editor.currentText()
        elif 'mitering' == opt or 'miterAlong' == opt:
            data = editor.currentIndex()
        else:
            data = editor.text()

        model.setData(index, str(data), Qt.EditRole)


    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)



class MainWindowForBevelTool(QMainWindow, ui_MainWindowForBevelTool.Ui_MainWindowForBevelTool):
    def __init__(self, parent=None):
        super(MainWindowForBevelTool, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.dataModelInOptionTableView = QStandardItemModel(self.optionTableView)
        self.optionTableView.setModel(self.dataModelInOptionTableView)
        self.selectionModelInOptionTableView = QItemSelectionModel(self.dataModelInOptionTableView, self.optionTableView)
        self.optionTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.optionTableView.setSelectionModel(self.selectionModelInOptionTableView)
        self.optionDelegate = OptionDelegate(self)
        self.optionTableView.setItemDelegate(self.optionDelegate)
        self.optionActionGroup = QActionGroup(self)
        self.optionActionGroup.addAction(self.simpleOptionsAction)
        self.optionActionGroup.addAction(self.fullOptionsAction)
        self.simpleOptionsAction.setChecked(True)

        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.bevelOptions = copy.copy(options.bevelOptions)
        self.resultPolyBevels = []

        self.displayBevelOptions()

        self.bevelButton.clicked.connect(self.bevel)
        self.optionActionGroup.triggered.connect(self.alterBevelOption)
        self.optionDelegate.closeEditor.connect(self.editOption)


    def displayBevelOptions(self, opts=options.SIMPLEOPTIONS):
        col = 0
        self.dataModelInOptionTableView.clear()
        for header in ('Bevel Option', 'Value'):
            item = QStandardItem(header)
            item.setFont(self.font)
            self.dataModelInOptionTableView.setHorizontalHeaderItem(col, item)
            col += 1

        for option in opts:
            item =  QStandardItem(option)
            item.setEditable(False)
            item.setFont(self.font)
            self.dataModelInOptionTableView.appendRow(item)
            row = self.dataModelInOptionTableView.indexFromItem(item).row()

            value = options.bevelOptions[option]
            item = QStandardItem(str(value))
            item.setFont(self.font)
            self.dataModelInOptionTableView.setItem(row, 1, item)

        self.optionTableView.resizeColumnsToContents()


    def alterBevelOption(self):
        self.simpleOptionsAction.isChecked() or self.displayBevelOptions(options.FULLOPTIONS)
        self.fullOptionsAction.isChecked() or self.displayBevelOptions(options.SIMPLEOPTIONS)


    def bevel(self):
        self.resultPolyBevels = bevelTool.bevelOnHardEdges(**self.bevelOptions)


    def _editAttribute(self, option, value):
        for bevelNode in self.resultPolyBevels:
            if 'fraction' == option:
                bevelNode[0].fraction.set(value)
            elif 'offsetAsFraction' == option:
                bevelNode[0].offsetAsFraction(value)
            elif 'autoFit' == option:
                bevelNode[0].autoFit.set(value)
            elif 'depth' == option:
                bevelNode[0].depth.set(value)
            elif 'mitering' == option:
                bevelNode[0].mitering.set(value)
            elif 'miterAlong' == option:
                bevelNode[0].miterAlong.set(value)
            elif 'chamfer' == option:
                bevelNode[0].chamfer.set(value)
            elif 'segments' == option:
                bevelNode[0].segments.set(value)
            elif 'worldSpace' == option:
                bevelNode[0].worldSpace.set(value)
            elif 'smoothingAngle' == option:
                bevelNode[0].smoothingAngle.set(value)
            elif 'subdivideNgons' == option:
                bevelNode[0].subdivideNgons.set(value)
            elif 'mergeVertices' == option:
                bevelNode[0].mergeVertices.set(value)
            elif 'mergeVertexTolerance' == option:
                bevelNode[0].mergeVertexTolerance.set(value)
            elif 'miteringAngle' == option:
                bevelNode[0].miteringAngle.set(value)
            elif 'angleTolerance' == option:
                bevelNode[0].angleTolerance.set(value)
            elif 'forceParallel' == option:
                bevelNode[0].forceParallel.set(value)


    def editOption(self, editor, hint):
        row = self.selectionModelInOptionTableView.currentIndex().row()
        option = self.dataModelInOptionTableView.item(row, 0).text()
        if option in options.BOOLOPTIONS:
            value = True if 'True' == editor.currentText() else False
        elif 'mitering' == option or 'miterAlong' == option:
            value = editor.currentIndex()
        else:
            value = float(editor.text())

        self.bevelOptions[option] = value
        not len(self.resultPolyBevels) or self._editAttribute(option, value)



def run():
    window = MainWindowForBevelTool(getMayaWindow())
    window.show()


if __name__ == '__main__':
    run()
