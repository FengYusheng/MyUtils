# -*- coding: utf-8 -*-
import os
import re

try:
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2 import __version__ as pyside_version
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance


class ListViewInDetailTabWidget(QListView):
    prototypeEdited = Signal(str, int)

    def __init__(self, parent):
        super(ListViewInDetailTabeWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.dataModel = QStandardItemModel(self)
        self.setModel(self.dataModel)
        self.selectionModel = QItemSelectionModel(self.dataModel, self)
        self.setSelectionModel(self.selectionModel)

        self.dataModel.itemChanged.connect(self.editPrototype)


    def addItems(self, prototypes):
        for p in prototypes:
            item = QStandardItem(p)
            item.setFont(self.font)
            self.dataModel.appendRow(item)


    def clearItems(self):
        self.dataModel.clear()


    def editPrototype(self, item):
        row = self.dataModel.indexFromItem(item).row()
        text = item.text()
        len(text) or self.dataModel.removeRow(row)
        self.prototypeEdited.emit(text, row)



class TableViewInDetailTabWidget(QTableView):
    def __init__(self, parent):
        super(TableViewInDetailTabWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.dataModel = QStandardItemModel(self)
        self.setModel(self.dataModel)
        self.selectionModel = QItemSelectionModel(self.dataModel, self)
        self.setSelectionModel(self.selectionModel)


    def addLODs(self, lods):
        self.dataModel.clear()
        index = 0
        for h in ('LOD', 'Budget', 'Tris/Verts'):
            item = QStandardItem(h)
            item.setFont(self.font)
            self.dataModel.setHorizontalHeaderItem(index, item)
            index += 1

        self.resizeColumnsToContents()



class CheckPolyCountWidget(QWidget):
    def __init__(self, parent):
        super(CheckPolyCountWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.parent = parent

        self.vertLayout = QVBoxLayout(self)
        self.itemLabel = QLabel(self)
        self.itemLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
        self.itemLabel.setTextFormat(Qt.RichText)
        self.itemLabel.setText('<b><span style="font-size:10pt">Check Poly Count</span></b>')
        self.vertLayout.addWidget(self.itemLabel)

        self.limitLabel = QLabel(self)
        self.limitLabel.setText('Budget type')
        self.limitComboBox = QComboBox(self)
        self.limitComboBox.addItem('Vertex budget')
        self.limitComboBox.addItem('Triangle budget')
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.limitLabel)
        horiLayout.addWidget(self.limitComboBox)
        self.vertLayout.addLayout(horiLayout)

        self.lodLabel = QLabel(self)
        self.lodLabel.setText('Number of LOD levels')
        self.lodComboBox = QComboBox(self)
        self.lodComboBox.addItems([str(i) for i in range(1, 10)])
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.lodLabel)
        horiLayout.addWidget(self.lodComboBox)
        self.vertLayout.addLayout(horiLayout)

        self.lodTableView = TableViewInDetailTabWidget(self)
        self.vertLayout.addWidget(self.lodTableView)

        self.lodTableView.addLODs(self.parent.data['detail'].setdefault('check poly count', []))


    def _initBudgetType(self):
        if len(self.parent.data['detail'].setdefault('check poly count', [])):
            self.lodComboBox.setCurrentIndex(0)
            # self.parent.data['detail']['check poly count'][0]




class CheckShaderNamesWidget(QWidget):
    def __init__(self, parent):
        super(CheckShaderNamesWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.parent = parent

        self.vertLayout = QVBoxLayout(self)
        self.itemLabel = QLabel(self)
        self.itemLabel.setTextFormat(Qt.RichText)
        self.itemLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
        self.itemLabel.setText('<b><span style="font-size:10pt">Check Shader Names</span></b>')
        self.vertLayout.addWidget(self.itemLabel)

        self.easyRadioButton = QRadioButton('Easy', self)
        self.easyRadioButton.setChecked(True)
        self.reRadioButton = QRadioButton('Regular Expression', self)
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.easyRadioButton)
        self.buttonGroup.addButton(self.reRadioButton)
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.easyRadioButton)
        horiLayout.addWidget(self.reRadioButton)
        self.vertLayout.addLayout(horiLayout)

        self.prefixLineEdit = QLineEdit(self)
        self.prefixLabel = QLabel(self)
        self.prefixLabel.setTextFormat(Qt.RichText)
        self.prefixLabel.setText('<b><span style="font-size:8pt">prefix: </span></b>')
        self.postfixLabel = QLabel(self)
        self.postfixLabel.setTextFormat(Qt.RichText)
        self.postfixLabel.setText('<b><span style="font-size:8pt">postfix: </span></b>')
        self.postfixLineEdit = QLineEdit(self)
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.prefixLabel)
        horiLayout.addWidget(self.prefixLineEdit)
        horiLayout.addWidget(self.postfixLabel)
        horiLayout.addWidget(self.postfixLineEdit)
        self.vertLayout.addLayout(horiLayout)

        self.addButton = QPushButton(self)
        self.addButton.setText('Add Prefix and Postfix')
        self.resetButton = QPushButton(self)
        self.resetButton.setText('Reset')
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.addButton)
        horiLayout.addWidget(self.resetButton)
        self.vertLayout.addLayout(horiLayout)

        self.previewLabel = QLabel(self)
        self.previewLabel.setTextFormat(Qt.RichText)
        self.previewLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
        self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')
        self.vertLayout.addWidget(self.previewLabel)

        self.prototypeList = ListViewInDetailTabWidget(self)
        self.prototypeList.addItems(self.parent.data['detail'].setdefault('check shader names', []))
        self.vertLayout.addWidget(self.prototypeList)

        self.buttonGroup.buttonClicked.connect(self.switchMode)
        self.prefixLineEdit.textEdited.connect(self.previewNamePrototype)
        self.postfixLineEdit.textEdited.connect(self.previewNamePrototype)
        self.resetButton.clicked.connect(self.reset)
        self.addButton.clicked.connect(self.addPrototype)
        self.prototypeList.prototypeEdited.connect(self.editPrototype)


    def switchMode(self):
        self.prototypeList.clearItems()
        self.parent.data['detail']['check shader names'] = []
        if self.reRadioButton.isChecked():
            self.prefixLineEdit.setEnabled(False)
            self.prefixLineEdit.clear()
            self.postfixLineEdit.setEnabled(False)
            self.postfixLineEdit.clear()
            self.addButton.setEnabled(False)
            self.resetButton.setEnabled(False)
            self.previewLabel.setText('<b><span style="font-size:10pt">Enter your regular expression:</span></b>')
        else:
            self.prefixLineEdit.setEnabled(True)
            self.postfixLineEdit.setEnabled(True)
            self.addButton.setEnabled(True)
            self.resetButton.setEnabled(True)
            self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')


    def previewNamePrototype(self):
        text = 'Preview: ' + self.prefixLineEdit.text() + '&#60;SHADER&#62;' + self.postfixLineEdit.text()
        self.previewLabel.setText('<b><span style="font-size:10pt">{0}</span></b>'.format(text))


    def reset(self):
        self.prefixLineEdit.clear()
        self.postfixLineEdit.clear()
        self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')
        self.prototypeList.clearItems()
        self.parent.data['detail']['check shader names'] = []


    def addPrototype(self):
        prototype = self.prefixLineEdit.text() + u'<SHADER>' + self.postfixLineEdit.text()
        if prototype not in self.parent.data['detail']['check shader names']:
            self.prototypeList.addItems([prototype,])
            self.parent.data['detail']['check shader names'].append(prototype)
            self.prefixLineEdit.clear()
            self.postfixLineEdit.clear()
            self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')


    def editPrototype(self, text, row):
        if len(text):
            self.parent.data['detail']['check shader names'][row] = text
        else:
            del self.parent.data['detail']['check shader names'][row]
