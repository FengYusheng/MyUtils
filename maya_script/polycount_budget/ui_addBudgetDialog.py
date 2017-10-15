# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\polycount_budget\Qt\UI\addBudgetDialog.ui'
#
# Created: Sat Oct 14 10:25:39 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addBudgetDialog(object):
    def setupUi(self, addBudgetDialog):
        addBudgetDialog.setObjectName("addBudgetDialog")
        addBudgetDialog.resize(348, 397)
        self.gridLayout = QtGui.QGridLayout(addBudgetDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.triRadio = QtGui.QRadioButton(addBudgetDialog)
        self.triRadio.setChecked(True)
        self.triRadio.setObjectName("triRadio")
        self.gridLayout.addWidget(self.triRadio, 0, 0, 1, 1)
        self.vertRadio = QtGui.QRadioButton(addBudgetDialog)
        self.vertRadio.setObjectName("vertRadio")
        self.gridLayout.addWidget(self.vertRadio, 0, 1, 1, 1)
        self.polyCountLabel = QtGui.QLabel(addBudgetDialog)
        self.polyCountLabel.setTextFormat(QtCore.Qt.RichText)
        self.polyCountLabel.setObjectName("polyCountLabel")
        self.gridLayout.addWidget(self.polyCountLabel, 1, 0, 1, 1)
        self.polyCountSpinBox = QtGui.QDoubleSpinBox(addBudgetDialog)
        self.polyCountSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.polyCountSpinBox.setDecimals(1)
        self.polyCountSpinBox.setMaximum(1000.0)
        self.polyCountSpinBox.setObjectName("polyCountSpinBox")
        self.gridLayout.addWidget(self.polyCountSpinBox, 1, 1, 1, 1)
        self.LODLabel = QtGui.QLabel(addBudgetDialog)
        self.LODLabel.setTextFormat(QtCore.Qt.RichText)
        self.LODLabel.setObjectName("LODLabel")
        self.gridLayout.addWidget(self.LODLabel, 2, 0, 1, 1)
        self.lodComboBox = QtGui.QComboBox(addBudgetDialog)
        self.lodComboBox.setEditable(True)
        self.lodComboBox.setObjectName("lodComboBox")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.gridLayout.addWidget(self.lodComboBox, 2, 1, 1, 1)
        self.colorLabel = QtGui.QLabel(addBudgetDialog)
        self.colorLabel.setTextFormat(QtCore.Qt.RichText)
        self.colorLabel.setObjectName("colorLabel")
        self.gridLayout.addWidget(self.colorLabel, 3, 0, 1, 1)
        self.colorComboBox = QtGui.QComboBox(addBudgetDialog)
        self.colorComboBox.setObjectName("colorComboBox")
        self.gridLayout.addWidget(self.colorComboBox, 3, 1, 1, 1)
        self.line = QtGui.QFrame(addBudgetDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)
        self.addButton = QtGui.QPushButton(addBudgetDialog)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 5, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(addBudgetDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 5, 1, 1, 1)

        self.retranslateUi(addBudgetDialog)
        QtCore.QMetaObject.connectSlotsByName(addBudgetDialog)

    def retranslateUi(self, addBudgetDialog):
        addBudgetDialog.setWindowTitle(QtGui.QApplication.translate("addBudgetDialog", "Set Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.triRadio.setText(QtGui.QApplication.translate("addBudgetDialog", "Triangle", None, QtGui.QApplication.UnicodeUTF8))
        self.vertRadio.setText(QtGui.QApplication.translate("addBudgetDialog", "Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountLabel.setText(QtGui.QApplication.translate("addBudgetDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Poly Count</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountSpinBox.setSuffix(QtGui.QApplication.translate("addBudgetDialog", "K", None, QtGui.QApplication.UnicodeUTF8))
        self.LODLabel.setText(QtGui.QApplication.translate("addBudgetDialog", "<html><head/><body><p><span style=\" font-weight:600;\">LOD</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lodComboBox.setItemText(0, QtGui.QApplication.translate("addBudgetDialog", "Extremely Low", None, QtGui.QApplication.UnicodeUTF8))
        self.lodComboBox.setItemText(1, QtGui.QApplication.translate("addBudgetDialog", "Low", None, QtGui.QApplication.UnicodeUTF8))
        self.lodComboBox.setItemText(2, QtGui.QApplication.translate("addBudgetDialog", "Medium", None, QtGui.QApplication.UnicodeUTF8))
        self.lodComboBox.setItemText(3, QtGui.QApplication.translate("addBudgetDialog", "High", None, QtGui.QApplication.UnicodeUTF8))
        self.lodComboBox.setItemText(4, QtGui.QApplication.translate("addBudgetDialog", "Very High", None, QtGui.QApplication.UnicodeUTF8))
        self.lodComboBox.setItemText(5, QtGui.QApplication.translate("addBudgetDialog", "Extremely High", None, QtGui.QApplication.UnicodeUTF8))
        self.colorLabel.setText(QtGui.QApplication.translate("addBudgetDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Color</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("addBudgetDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("addBudgetDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

