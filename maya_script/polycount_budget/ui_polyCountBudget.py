# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\polycount_budget\Qt\UI\polyCountBudget.ui'
#
# Created: Sat Oct 14 10:25:38 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_polyCountBudget(object):
    def setupUi(self, polyCountBudget):
        polyCountBudget.setObjectName("polyCountBudget")
        polyCountBudget.resize(690, 440)
        self.horizontalLayout_5 = QtGui.QHBoxLayout(polyCountBudget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.polyCountBudgetGroupBox = QtGui.QGroupBox(polyCountBudget)
        self.polyCountBudgetGroupBox.setFlat(False)
        self.polyCountBudgetGroupBox.setCheckable(False)
        self.polyCountBudgetGroupBox.setObjectName("polyCountBudgetGroupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.polyCountBudgetGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.triangleRadio = QtGui.QRadioButton(self.polyCountBudgetGroupBox)
        self.triangleRadio.setChecked(True)
        self.triangleRadio.setObjectName("triangleRadio")
        self.horizontalLayout_6.addWidget(self.triangleRadio)
        self.vertexRadio = QtGui.QRadioButton(self.polyCountBudgetGroupBox)
        self.vertexRadio.setObjectName("vertexRadio")
        self.horizontalLayout_6.addWidget(self.vertexRadio)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fromLabel = QtGui.QLabel(self.polyCountBudgetGroupBox)
        self.fromLabel.setTextFormat(QtCore.Qt.RichText)
        self.fromLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fromLabel.setObjectName("fromLabel")
        self.horizontalLayout.addWidget(self.fromLabel)
        self.startBudgetSpinBox = QtGui.QSpinBox(self.polyCountBudgetGroupBox)
        self.startBudgetSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.startBudgetSpinBox.setSuffix("")
        self.startBudgetSpinBox.setMaximum(9999999)
        self.startBudgetSpinBox.setObjectName("startBudgetSpinBox")
        self.horizontalLayout.addWidget(self.startBudgetSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.polyCountBudgetGroupBox)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.endBudgetSpinBox = QtGui.QSpinBox(self.polyCountBudgetGroupBox)
        self.endBudgetSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.endBudgetSpinBox.setSuffix("")
        self.endBudgetSpinBox.setPrefix("")
        self.endBudgetSpinBox.setMaximum(9999999)
        self.endBudgetSpinBox.setObjectName("endBudgetSpinBox")
        self.horizontalLayout_3.addWidget(self.endBudgetSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tagLabel = QtGui.QLabel(self.polyCountBudgetGroupBox)
        self.tagLabel.setTextFormat(QtCore.Qt.RichText)
        self.tagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagLabel.setObjectName("tagLabel")
        self.horizontalLayout_2.addWidget(self.tagLabel)
        self.tagComboBox = QtGui.QComboBox(self.polyCountBudgetGroupBox)
        self.tagComboBox.setObjectName("tagComboBox")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.tagComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.tagComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addButton = QtGui.QPushButton(self.polyCountBudgetGroupBox)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_4.addWidget(self.addButton)
        self.resetButton = QtGui.QPushButton(self.polyCountBudgetGroupBox)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_4.addWidget(self.resetButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addWidget(self.polyCountBudgetGroupBox)
        self.budgetGroupBox = QtGui.QGroupBox(polyCountBudget)
        self.budgetGroupBox.setObjectName("budgetGroupBox")
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.budgetGroupBox)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.budgetTableView = QtGui.QTableView(self.budgetGroupBox)
        self.budgetTableView.setGridStyle(QtCore.Qt.DashLine)
        self.budgetTableView.setSortingEnabled(True)
        self.budgetTableView.setObjectName("budgetTableView")
        self.horizontalLayout_7.addWidget(self.budgetTableView)
        self.horizontalLayout_5.addWidget(self.budgetGroupBox)

        self.retranslateUi(polyCountBudget)
        QtCore.QMetaObject.connectSlotsByName(polyCountBudget)

    def retranslateUi(self, polyCountBudget):
        polyCountBudget.setWindowTitle(QtGui.QApplication.translate("polyCountBudget", "Poly Count Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountBudgetGroupBox.setTitle(QtGui.QApplication.translate("polyCountBudget", "Enter Poly Count", None, QtGui.QApplication.UnicodeUTF8))
        self.triangleRadio.setText(QtGui.QApplication.translate("polyCountBudget", "Triangle", None, QtGui.QApplication.UnicodeUTF8))
        self.vertexRadio.setText(QtGui.QApplication.translate("polyCountBudget", "Vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.fromLabel.setText(QtGui.QApplication.translate("polyCountBudget", "<html><head/><body><p><span style=\" font-weight:600;\">From:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("polyCountBudget", "<html><head/><body><p><span style=\" font-weight:600;\">TO</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tagLabel.setText(QtGui.QApplication.translate("polyCountBudget", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Tag: </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tagComboBox.setItemText(0, QtGui.QApplication.translate("polyCountBudget", "Extremely low", None, QtGui.QApplication.UnicodeUTF8))
        self.tagComboBox.setItemText(1, QtGui.QApplication.translate("polyCountBudget", "Low", None, QtGui.QApplication.UnicodeUTF8))
        self.tagComboBox.setItemText(2, QtGui.QApplication.translate("polyCountBudget", "Medium", None, QtGui.QApplication.UnicodeUTF8))
        self.tagComboBox.setItemText(3, QtGui.QApplication.translate("polyCountBudget", "High", None, QtGui.QApplication.UnicodeUTF8))
        self.tagComboBox.setItemText(4, QtGui.QApplication.translate("polyCountBudget", "Very high", None, QtGui.QApplication.UnicodeUTF8))
        self.tagComboBox.setItemText(5, QtGui.QApplication.translate("polyCountBudget", "Extremely high", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("polyCountBudget", "Add Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("polyCountBudget", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.budgetGroupBox.setTitle(QtGui.QApplication.translate("polyCountBudget", "Budget", None, QtGui.QApplication.UnicodeUTF8))

