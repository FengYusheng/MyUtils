# -*- coding: utf-8 -*-
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
        super(ListViewInDetailTabWidget, self).__init__(parent)
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



class DelegateInLODTableView(QStyledItemDelegate):
    budgetEdited = Signal(QModelIndex, str)

    def __init__(self, parent):
        super(DelegateInLODTableView, self).__init__(parent)


    def createEditor(self, parent, option, index):
        col = index.column()
        editor = None
        if col == 2:
            editor = QDoubleSpinBox(parent)
            editor.setMaximum(1000.0)
            editor.setMinimum(0.0)
            editor.setDecimals(1.0)
            editor.setSuffix('K')

        return editor


    def setEditorData(self, editor, index):
        col = index.column()
        if col == 2:
            valueInModel = index.model().data(index, Qt.EditRole).partition('K')[0]
            editor.setValue(float(valueInModel))


    def setModelData(self, editor, model, index):
        col = index.column()
        if col == 2:
            editor.interpretText()
            value = str(editor.value()) + 'K'
            model.setData(index, value, Qt.EditRole)
            self.budgetEdited.emit(index, value)


    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)



class LODTableViewInDetailTabWidget(QTableView):
    budgetEdited = Signal(QModelIndex, str)

    def __init__(self, parent):
        super(LODTableViewInDetailTabWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.dataModel = QStandardItemModel(self)
        self.setModel(self.dataModel)
        self.selectionModel = QItemSelectionModel(self.dataModel, self)
        self.setSelectionModel(self.selectionModel)
        self.budgetDelegate = DelegateInLODTableView(self)
        self.setItemDelegate(self.budgetDelegate)

        self.budgetDelegate.budgetEdited.connect(self.setBudget)


    def setLODs(self, lods):
        self.dataModel.clear()
        index = 0
        for h in ('LOD', 'Tris/Verts', 'Budget'):
            item = QStandardItem(h)
            item.setFont(self.font)
            self.dataModel.setHorizontalHeaderItem(index, item)
            index += 1

        row = 0
        # lods: [['LOD_1', 'Vertex', '0.0K'],]
        for level, component, budget in lods:
            item = QStandardItem(level)
            item.setFont(self.font)
            self.dataModel.appendRow(item)

            item = QStandardItem(component)
            item.setFont(self.font)
            self.dataModel.setItem(row, 1, item)

            item = QStandardItem(budget)
            item.setFont(self.font)
            self.dataModel.setItem(row, 2, item)

            row += 1

        self.resizeColumnsToContents()


    def setBudget(self, index, budget):
        self.budgetEdited.emit(index, budget)



class CheckPolyCountWidget(QWidget):
    CHECKER = 'check poly count'

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

        self.typeLabel = QLabel(self)
        self.typeLabel.setText('Budget type')
        self.typeComboBox = QComboBox(self)
        self.typeComboBox.addItem('Vertex')
        self.typeComboBox.addItem('Triangle')
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.typeLabel)
        horiLayout.addWidget(self.typeComboBox)
        self.vertLayout.addLayout(horiLayout)

        self.lodLabel = QLabel(self)
        self.lodLabel.setText('Number of LOD levels')
        self.lodComboBox = QComboBox(self)
        self.lodComboBox.addItems([str(i) for i in range(1, 10)])
        horiLayout = QHBoxLayout(self)
        horiLayout.addWidget(self.lodLabel)
        horiLayout.addWidget(self.lodComboBox)
        self.vertLayout.addLayout(horiLayout)

        self.lodTableView = LODTableViewInDetailTabWidget(self)
        self.vertLayout.addWidget(self.lodTableView)

        self._initialize()

        self.typeComboBox.currentIndexChanged.connect(self.setBudgetType)
        self.lodComboBox.currentIndexChanged.connect(self.setLODCount)
        self.lodTableView.budgetEdited.connect(self.setBudget)


    def _initialize(self):
        data = self.parent.detail('check poly count')
        if len(data):
            self.lodComboBox.setCurrentIndex(len(data)-1)
            self.typeComboBox.setCurrentIndex(0)
            data[0][1] == 'Vertex' or self.typeComboBox.setCurrentIndex(1)
            self.lodTableView.setLODs(data)
        else:
            self.lodComboBox.setCurrentIndex(0)
            self.typeComboBox.setCurrentIndex(0)
            data = self._initializeLODs()['Vertex'][:1]
            self.parent.setDetail('check poly count', data)
            self.lodTableView.setLODs(data)


    def _initializeLODs(self):
        return {
            'Vertex'   : [['LOD_{0}'.format(i), 'Vertex', '0.0K'] for i in range(1, 10)],
            'Triangle' : [['LOD_{0}'.format(i), 'Triangle', '0.0K'] for i in range(1, 10)]
        }


    def setBudgetType(self):
        budgetType = self.typeComboBox.currentText()
        count = int(self.lodComboBox.currentText())
        data = self.parent.detail('check poly count')
        for lod in data:
            lod[1] = budgetType
        self.lodTableView.setLODs(data[0:count])


    def setLODCount(self):
        count = int(self.lodComboBox.currentText())
        budgetType = self.typeComboBox.currentText()
        data = self.parent.detail('check poly count')
        existing = len(data)
        if count > existing:
            data = data + self._initializeLODs()[budgetType][existing:count]
            self.lodTableView.setLODs(data)
        else:
            self.lodTableView.setLODs(data[0:count])
            data = data[0:count]

        self.parent.setDetail('check poly count', data)


    def setBudget(self, index, budget):
        row = index.row()
        col = index.column()
        data = self.parent.detail('check poly count')
        data[row][col] = budget
        self.parent.setDetail('check poly count', data)



class CheckShaderNamesWidget(QWidget):
    CHECKER = 'check shader names'

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
        self.prototypeList.addItems([i[0] for i in self.parent.detail('check shader names') if len(i)])
        self.vertLayout.addWidget(self.prototypeList)

        self.regularEditor = QTextEdit(self)
        self.regularEditor.setPlaceholderText('Enter regular expression.')
        self.regularEditor.setVisible(False)
        self.regularEditor.setFontPointSize(10.0)
        self.vertLayout.addWidget(self.regularEditor)

        self.buttonGroup.buttonClicked.connect(self.switchMode)
        self.prefixLineEdit.textEdited.connect(self.previewNamePrototype)
        self.postfixLineEdit.textEdited.connect(self.previewNamePrototype)
        self.resetButton.clicked.connect(self.reset)
        self.addButton.clicked.connect(self.addPrototype)
        self.prototypeList.prototypeEdited.connect(self.editPrototype)
        self.regularEditor.currentCharFormatChanged.connect(lambda x:self.regularEditor.setFontPointSize(10.0))
        self.regularEditor.textChanged.connect(self.editPrototypeInRegularMode)


    def switchMode(self):
        if self.reRadioButton.isChecked():
            self.prefixLineEdit.setEnabled(False)
            self.prefixLineEdit.clear()
            self.postfixLineEdit.setEnabled(False)
            self.postfixLineEdit.clear()
            self.addButton.setEnabled(False)
            self.resetButton.setEnabled(False)
            self.previewLabel.setText('<b><span style="font-size:10pt">Enter your regular expression:</span></b>')
            self.prototypeList.setVisible(False)
            self.regularEditor.setVisible(True)
            self.regularEditor.setPlainText('\n'.join([i[0] for i in self.parent.detail('check shader names') if len(i)]))
        else:
            self.prefixLineEdit.setEnabled(True)
            self.postfixLineEdit.setEnabled(True)
            self.addButton.setEnabled(True)
            self.resetButton.setEnabled(True)
            self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')
            self.prototypeList.setVisible(True)
            self.regularEditor.setVisible(False)
            self.prototypeList.clearItems()
            self.prototypeList.addItems([i[0] for i in self.parent.detail('check shader names') if len(i)])


    def previewNamePrototype(self):
        text = 'Preview: ' + self.prefixLineEdit.text() + '&#60;SHADER&#62;' + self.postfixLineEdit.text()
        self.previewLabel.setText('<b><span style="font-size:10pt">{0}</span></b>'.format(text))


    def reset(self):
        self.prefixLineEdit.clear()
        self.postfixLineEdit.clear()
        self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')
        self.prototypeList.clearItems()
        self.parent.setDetail('check shader names', [])


    def addPrototype(self):
        if len(self.prefixLineEdit.text()) or len(self.postfixLineEdit.text()):
            prototype = self.prefixLineEdit.text() + u'<SHADER>' + self.postfixLineEdit.text()
            data = self.parent.detail('check shader names')
            if prototype not in data:
                self.prototypeList.addItems([prototype,])
                data.append([prototype,])
                self.parent.setDetail('check shader names', data)
                self.prefixLineEdit.clear()
                self.postfixLineEdit.clear()
                self.previewLabel.setText('<b><span style="font-size:10pt">Preview</span></b>')


    def editPrototype(self, text, row):
        data = self.parent.detail('check shader names')
        if len(text):
            data[row][0] = text
        else:
            del data[row]

        self.parent.setDetail('check shader names', data)


    def editPrototypeInRegularMode(self):
        self.parent.setDetail('check shader names', [[i] for i in self.regularEditor.toPlainText().strip().split('\n')])
