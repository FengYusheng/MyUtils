# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\Draft\polycount_budget\Qt\UI\polyCountBudget.ui'
#
# Created: Wed Oct 11 10:34:15 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_polyCountBudget(object):
    def setupUi(self, polyCountBudget):
        polyCountBudget.setObjectName("polyCountBudget")
        polyCountBudget.resize(690, 440)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(polyCountBudget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.polyCountBudgetGroupBox = QtWidgets.QGroupBox(polyCountBudget)
        self.polyCountBudgetGroupBox.setFlat(False)
        self.polyCountBudgetGroupBox.setCheckable(False)
        self.polyCountBudgetGroupBox.setObjectName("polyCountBudgetGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.polyCountBudgetGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.triangleRadio = QtWidgets.QRadioButton(self.polyCountBudgetGroupBox)
        self.triangleRadio.setChecked(True)
        self.triangleRadio.setObjectName("triangleRadio")
        self.horizontalLayout_6.addWidget(self.triangleRadio)
        self.vertexRadio = QtWidgets.QRadioButton(self.polyCountBudgetGroupBox)
        self.vertexRadio.setObjectName("vertexRadio")
        self.horizontalLayout_6.addWidget(self.vertexRadio)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fromLabel = QtWidgets.QLabel(self.polyCountBudgetGroupBox)
        self.fromLabel.setTextFormat(QtCore.Qt.RichText)
        self.fromLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fromLabel.setObjectName("fromLabel")
        self.horizontalLayout.addWidget(self.fromLabel)
        self.startBudgetSpinBox = QtWidgets.QSpinBox(self.polyCountBudgetGroupBox)
        self.startBudgetSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.startBudgetSpinBox.setSuffix("")
        self.startBudgetSpinBox.setMaximum(9999999)
        self.startBudgetSpinBox.setObjectName("startBudgetSpinBox")
        self.horizontalLayout.addWidget(self.startBudgetSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.polyCountBudgetGroupBox)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.endBudgetSpinBox = QtWidgets.QSpinBox(self.polyCountBudgetGroupBox)
        self.endBudgetSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.endBudgetSpinBox.setSuffix("")
        self.endBudgetSpinBox.setPrefix("")
        self.endBudgetSpinBox.setMaximum(9999999)
        self.endBudgetSpinBox.setObjectName("endBudgetSpinBox")
        self.horizontalLayout_3.addWidget(self.endBudgetSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tagLabel = QtWidgets.QLabel(self.polyCountBudgetGroupBox)
        self.tagLabel.setTextFormat(QtCore.Qt.RichText)
        self.tagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagLabel.setObjectName("tagLabel")
        self.horizontalLayout_2.addWidget(self.tagLabel)
        self.tagComboBox = QtWidgets.QComboBox(self.polyCountBudgetGroupBox)
        self.tagComboBox.setObjectName("tagComboBox")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.tagComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addButton = QtWidgets.QPushButton(self.polyCountBudgetGroupBox)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_4.addWidget(self.addButton)
        self.resetButton = QtWidgets.QPushButton(self.polyCountBudgetGroupBox)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_4.addWidget(self.resetButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addWidget(self.polyCountBudgetGroupBox)
        self.budgetGroupBox = QtWidgets.QGroupBox(polyCountBudget)
        self.budgetGroupBox.setObjectName("budgetGroupBox")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.budgetGroupBox)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.budgetTableView = QtWidgets.QTableView(self.budgetGroupBox)
        self.budgetTableView.setGridStyle(QtCore.Qt.DashLine)
        self.budgetTableView.setSortingEnabled(True)
        self.budgetTableView.setObjectName("budgetTableView")
        self.horizontalLayout_7.addWidget(self.budgetTableView)
        self.horizontalLayout_5.addWidget(self.budgetGroupBox)

        self.retranslateUi(polyCountBudget)
        QtCore.QMetaObject.connectSlotsByName(polyCountBudget)

    def retranslateUi(self, polyCountBudget):
        polyCountBudget.setWindowTitle(QtWidgets.QApplication.translate("polyCountBudget", "Poly Count Budget", None, -1))
        self.polyCountBudgetGroupBox.setTitle(QtWidgets.QApplication.translate("polyCountBudget", "Enter Poly Count", None, -1))
        self.triangleRadio.setText(QtWidgets.QApplication.translate("polyCountBudget", "Triangle", None, -1))
        self.vertexRadio.setText(QtWidgets.QApplication.translate("polyCountBudget", "Vertex", None, -1))
        self.fromLabel.setText(QtWidgets.QApplication.translate("polyCountBudget", "<html><head/><body><p><span style=\" font-weight:600;\">From:</span></p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("polyCountBudget", "<html><head/><body><p><span style=\" font-weight:600;\">TO</span></p></body></html>", None, -1))
        self.tagLabel.setText(QtWidgets.QApplication.translate("polyCountBudget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Tag: </span></p></body></html>", None, -1))
        self.tagComboBox.setItemText(0, QtWidgets.QApplication.translate("polyCountBudget", "Extremely low", None, -1))
        self.tagComboBox.setItemText(1, QtWidgets.QApplication.translate("polyCountBudget", "Low", None, -1))
        self.tagComboBox.setItemText(2, QtWidgets.QApplication.translate("polyCountBudget", "Medium", None, -1))
        self.tagComboBox.setItemText(3, QtWidgets.QApplication.translate("polyCountBudget", "High", None, -1))
        self.tagComboBox.setItemText(4, QtWidgets.QApplication.translate("polyCountBudget", "Very high", None, -1))
        self.tagComboBox.setItemText(5, QtWidgets.QApplication.translate("polyCountBudget", "Extremely high", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("polyCountBudget", "Add Budget", None, -1))
        self.resetButton.setText(QtWidgets.QApplication.translate("polyCountBudget", "Reset", None, -1))
        self.budgetGroupBox.setTitle(QtWidgets.QApplication.translate("polyCountBudget", "Budget", None, -1))

