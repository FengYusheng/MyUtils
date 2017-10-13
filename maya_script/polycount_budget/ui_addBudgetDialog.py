# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\Draft\polycount_budget\Qt\UI\addBudgetDialog.ui'
#
# Created: Wed Oct 11 10:34:16 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_addBudgetDialog(object):
    def setupUi(self, addBudgetDialog):
        addBudgetDialog.setObjectName("addBudgetDialog")
        addBudgetDialog.resize(348, 397)
        self.gridLayout = QtWidgets.QGridLayout(addBudgetDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.triRadio = QtWidgets.QRadioButton(addBudgetDialog)
        self.triRadio.setChecked(True)
        self.triRadio.setObjectName("triRadio")
        self.gridLayout.addWidget(self.triRadio, 0, 0, 1, 1)
        self.vertRadio = QtWidgets.QRadioButton(addBudgetDialog)
        self.vertRadio.setObjectName("vertRadio")
        self.gridLayout.addWidget(self.vertRadio, 0, 1, 1, 1)
        self.polyCountLabel = QtWidgets.QLabel(addBudgetDialog)
        self.polyCountLabel.setTextFormat(QtCore.Qt.RichText)
        self.polyCountLabel.setObjectName("polyCountLabel")
        self.gridLayout.addWidget(self.polyCountLabel, 1, 0, 1, 1)
        self.polyCountSpinBox = QtWidgets.QDoubleSpinBox(addBudgetDialog)
        self.polyCountSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.polyCountSpinBox.setDecimals(1)
        self.polyCountSpinBox.setMaximum(1000.0)
        self.polyCountSpinBox.setObjectName("polyCountSpinBox")
        self.gridLayout.addWidget(self.polyCountSpinBox, 1, 1, 1, 1)
        self.LODLabel = QtWidgets.QLabel(addBudgetDialog)
        self.LODLabel.setTextFormat(QtCore.Qt.RichText)
        self.LODLabel.setObjectName("LODLabel")
        self.gridLayout.addWidget(self.LODLabel, 2, 0, 1, 1)
        self.lodComboBox = QtWidgets.QComboBox(addBudgetDialog)
        self.lodComboBox.setEditable(True)
        self.lodComboBox.setObjectName("lodComboBox")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.lodComboBox.addItem("")
        self.gridLayout.addWidget(self.lodComboBox, 2, 1, 1, 1)
        self.colorLabel = QtWidgets.QLabel(addBudgetDialog)
        self.colorLabel.setTextFormat(QtCore.Qt.RichText)
        self.colorLabel.setObjectName("colorLabel")
        self.gridLayout.addWidget(self.colorLabel, 3, 0, 1, 1)
        self.colorComboBox = QtWidgets.QComboBox(addBudgetDialog)
        self.colorComboBox.setObjectName("colorComboBox")
        self.gridLayout.addWidget(self.colorComboBox, 3, 1, 1, 1)
        self.line = QtWidgets.QFrame(addBudgetDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)
        self.addButton = QtWidgets.QPushButton(addBudgetDialog)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 5, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(addBudgetDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 5, 1, 1, 1)

        self.retranslateUi(addBudgetDialog)
        QtCore.QMetaObject.connectSlotsByName(addBudgetDialog)

    def retranslateUi(self, addBudgetDialog):
        addBudgetDialog.setWindowTitle(QtWidgets.QApplication.translate("addBudgetDialog", "Set Budget", None, -1))
        self.triRadio.setText(QtWidgets.QApplication.translate("addBudgetDialog", "Triangle", None, -1))
        self.vertRadio.setText(QtWidgets.QApplication.translate("addBudgetDialog", "Vertex", None, -1))
        self.polyCountLabel.setText(QtWidgets.QApplication.translate("addBudgetDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Poly Count</span></p></body></html>", None, -1))
        self.polyCountSpinBox.setSuffix(QtWidgets.QApplication.translate("addBudgetDialog", "K", None, -1))
        self.LODLabel.setText(QtWidgets.QApplication.translate("addBudgetDialog", "<html><head/><body><p><span style=\" font-weight:600;\">LOD</span></p></body></html>", None, -1))
        self.lodComboBox.setItemText(0, QtWidgets.QApplication.translate("addBudgetDialog", "Extremely Low", None, -1))
        self.lodComboBox.setItemText(1, QtWidgets.QApplication.translate("addBudgetDialog", "Low", None, -1))
        self.lodComboBox.setItemText(2, QtWidgets.QApplication.translate("addBudgetDialog", "Medium", None, -1))
        self.lodComboBox.setItemText(3, QtWidgets.QApplication.translate("addBudgetDialog", "High", None, -1))
        self.lodComboBox.setItemText(4, QtWidgets.QApplication.translate("addBudgetDialog", "Very High", None, -1))
        self.lodComboBox.setItemText(5, QtWidgets.QApplication.translate("addBudgetDialog", "Extremely High", None, -1))
        self.colorLabel.setText(QtWidgets.QApplication.translate("addBudgetDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Color</span></p></body></html>", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("addBudgetDialog", "Add", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("addBudgetDialog", "Cancel", None, -1))

