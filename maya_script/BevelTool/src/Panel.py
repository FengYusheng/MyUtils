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

import ui_OptionTableViewWidget
reload(ui_OptionTableViewWidget)
import ui_SimpleOptionsWidget
reload(ui_SimpleOptionsWidget)
import options
reload(options)
import bevelTool
reload(bevelTool)



class DelegateInOptionTableView(QStyledItemDelegate):
    def __init__(self, parent):
        super(DelegateInOptionTableView, self).__init__(parent)
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




class OptionTableViewWidget(QWidget, ui_OptionTableViewWidget.Ui_optionTableViewWidiget):
    def __init__(self, parent):
        super(OptionTableViewWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.dataModelInOptionTableView = QStandardItemModel(self.optionTableView)
        self.optionTableView.setModel(self.dataModelInOptionTableView)
        self.selectionModelInOptionTableView = QItemSelectionModel(self.dataModelInOptionTableView, self.optionTableView)
        self.optionTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.optionTableView.setSelectionModel(self.selectionModelInOptionTableView)
        self.delegate = DelegateInOptionTableView(self)
        self.optionTableView.setItemDelegate(self.delegate)

        self.parent = parent
        self.bevelOptions = self.parent.bevelOptions()
        self.font = QFont('OldEnglish', 10, QFont.Bold)

        self._displayOptionsInTableView()

        self.bevelButton.clicked.connect(self.bevel)
        self.delegate.closeEditor.connect(self.editOption)


    def _displayOptionsInTableView(self, opts=options.FULLOPTIONS):
        _ = 0
        self.dataModelInOptionTableView.clear()
        for header in ('Bevel Opiton', 'Value'):
            item = QStandardItem(header)
            item.setFont(self.font)
            self.dataModelInOptionTableView.setHorizontalHeaderItem(_, item)
            _ += 1

        for option in opts:
            item = QStandardItem(option)
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInOptionTableView.appendRow(item)
            _ = self.dataModelInOptionTableView.indexFromItem(item).row()

            item = QStandardItem(str(self.bevelOptions[option]))
            item.setFont(self.font)
            self.dataModelInOptionTableView.setItem(_, 1, item)

        self.optionTableView.resizeColumnsToContents()


    def bevel(self):
        bevelNodes = bevelTool.bevelOnHardEdges(**self.bevelOptions)
        self.parent.setBevelNodes(bevelNodes)


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
        self.parent.editBevelOption(option, value)




class SimpleOptionsWidget(QWidget, ui_SimpleOptionsWidget.Ui_simpleOptionsWidget):
    def __init__(self, parent):
        super(SimpleOptionsWidget, self).__init__(parent)
        self.parent = parent
        self.bevelOptions = self.parent.bevelOptions()

        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(self.optionGroupBox)
        self.splitter.addWidget(self.helpTabWidget)
        self.gridLayout_3.addWidget(self.splitter)
        self.helpTabWidget.setVisible(False)

        self.fractionDoubleSpinBox.valueChanged.connect(self.editFractionBySpinBox)
        self.fractionSlider.valueChanged.connect(self.editFractionBySlider)
        self.segmentsSpinBox.valueChanged.connect(self.editSegmentsBySpinBox)
        self.segmentsSlider.valueChanged.connect(self.editSegmentsBySlider)
        self.miteringComboBox.currentIndexChanged.connect(self.editMitering)
        self.miterAlongComboBox.currentIndexChanged.connect(self.editMiteringAlong)
        self.bevelButton.clicked.connect(self.bevel)


    def editFractionBySpinBox(self, value):
        if self.fractionSlider.value() != (int(value*1000)):
            self.fractionSlider.setValue(int(value*1000))
            self.bevelOptions['fraction'] = value
            self.parent.editBevelOption('fraction', value)


    def editFractionBySlider(self, value):
        if self.fractionDoubleSpinBox.value() != (value/1000.0):
            self.fractionDoubleSpinBox.setValue(value/1000.0)
            self.bevelOptions['fraction'] = value
            self.parent.editBevelOption('fraction', value/1000.0)


    def editSegmentsBySpinBox(self, value):
        if self.segmentsSlider.value() != value:
            self.segmentsSlider.setValue(value)
            self.bevelOptions['segments'] = value
            self.parent.editBevelOption('segments', value)


    def editSegmentsBySlider(self, value):
        if self.segmentsSpinBox.value() != value:
            self.segmentsSpinBox.setValue(value)
            self.bevelOptions['segments'] = value
            self.parent.editBevelOption('segments', value)


    def editMitering(self, index):
        self.bevelOptions['mitering'] = index
        self.parent.editBevelOption('mitering', index)


    def editMiteringAlong(self, index):
        self.bevelOptions['miterAlong'] = index
        self.parent.editBevelOption('miterAlong', index)



    def bevel(self):
        bevelNodes = bevelTool.bevelOnHardEdges(**self.bevelOptions)
        self.parent.setBevelNodes(bevelNodes)
