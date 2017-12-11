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
        else:
            editor = QDoubleSpinBox(parent)
            editor.setMaximum(1000.0)
            editor.setMinimum(0.0)
            editor.setDecimals(1.0)

        return editor


    def setEditorData(self, editor, index):
        data = index.model().data(index, Qt.EditRole)
        if isinstance(editor, QComboBox):
            data == 'True' or editor.setCurrentIndex(1)
            data == 'False' or editor.setCurrentIndex(0)
        else:
            editor.setValue(float(data))


    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            data = editor.currentText()
        else:
            editor.interpretText()
            data = str(editor.value())

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
        bevelTool.bevelOnHardEdges(**self.bevelOptions)


    def editOption(self, editor, hint):
        row = self.selectionModelInOptionTableView.currentIndex().row()
        option = self.dataModelInOptionTableView.item(row, 0).text()
        if isinstance(editor, QComboBox):
            value = True if 'True' == editor.currentText() else False
        else:
            editor.interpretText()
            value = editor.value()

        self.bevelOptions[option] = value



if __name__ == '__main__':
    window = MainWindowForBevelTool(getMayaWindow())
    window.show()
