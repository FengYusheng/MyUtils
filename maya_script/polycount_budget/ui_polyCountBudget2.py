# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\polycount_budget\Qt\UI\polyCountBudget2.ui'
#
# Created: Sat Oct 14 10:25:38 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_polyCountBudgetMainWindow(object):
    def setupUi(self, polyCountBudgetMainWindow):
        polyCountBudgetMainWindow.setObjectName("polyCountBudgetMainWindow")
        polyCountBudgetMainWindow.resize(675, 652)
        polyCountBudgetMainWindow.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)
        self.centralwidget = QtGui.QWidget(polyCountBudgetMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.budgetGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.budgetGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.budgetGroupBox.setObjectName("budgetGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.budgetGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.trisRadioButton = QtGui.QRadioButton(self.budgetGroupBox)
        self.trisRadioButton.setChecked(True)
        self.trisRadioButton.setObjectName("trisRadioButton")
        self.gridLayout.addWidget(self.trisRadioButton, 0, 0, 1, 2)
        self.vertsRadioButton = QtGui.QRadioButton(self.budgetGroupBox)
        self.vertsRadioButton.setObjectName("vertsRadioButton")
        self.gridLayout.addWidget(self.vertsRadioButton, 0, 2, 1, 1)
        self.lodCheckBox = QtGui.QCheckBox(self.budgetGroupBox)
        self.lodCheckBox.setObjectName("lodCheckBox")
        self.gridLayout.addWidget(self.lodCheckBox, 0, 3, 1, 1)
        self.extremelyLowLabel = QtGui.QLabel(self.budgetGroupBox)
        self.extremelyLowLabel.setTextFormat(QtCore.Qt.RichText)
        self.extremelyLowLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.extremelyLowLabel.setObjectName("extremelyLowLabel")
        self.gridLayout.addWidget(self.extremelyLowLabel, 1, 0, 1, 2)
        self.extremelyLowSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.extremelyLowSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.extremelyLowSpinBox.setMaximum(100000)
        self.extremelyLowSpinBox.setObjectName("extremelyLowSpinBox")
        self.gridLayout.addWidget(self.extremelyLowSpinBox, 1, 2, 1, 1)
        self.extremleyLowSlider = QtGui.QSlider(self.budgetGroupBox)
        self.extremleyLowSlider.setMaximum(100000)
        self.extremleyLowSlider.setOrientation(QtCore.Qt.Horizontal)
        self.extremleyLowSlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.extremleyLowSlider.setObjectName("extremleyLowSlider")
        self.gridLayout.addWidget(self.extremleyLowSlider, 1, 3, 1, 1)
        self.lowLabel = QtGui.QLabel(self.budgetGroupBox)
        self.lowLabel.setTextFormat(QtCore.Qt.RichText)
        self.lowLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lowLabel.setObjectName("lowLabel")
        self.gridLayout.addWidget(self.lowLabel, 2, 0, 1, 1)
        self.lowSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.lowSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.lowSpinBox.setMaximum(100000)
        self.lowSpinBox.setObjectName("lowSpinBox")
        self.gridLayout.addWidget(self.lowSpinBox, 2, 2, 1, 1)
        self.lowSlider = QtGui.QSlider(self.budgetGroupBox)
        self.lowSlider.setMaximum(100000)
        self.lowSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lowSlider.setObjectName("lowSlider")
        self.gridLayout.addWidget(self.lowSlider, 2, 3, 1, 1)
        self.mediumLabel = QtGui.QLabel(self.budgetGroupBox)
        self.mediumLabel.setTextFormat(QtCore.Qt.RichText)
        self.mediumLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mediumLabel.setObjectName("mediumLabel")
        self.gridLayout.addWidget(self.mediumLabel, 3, 0, 1, 1)
        self.mediumSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.mediumSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.mediumSpinBox.setMaximum(100000)
        self.mediumSpinBox.setObjectName("mediumSpinBox")
        self.gridLayout.addWidget(self.mediumSpinBox, 3, 2, 1, 1)
        self.mediumSlider = QtGui.QSlider(self.budgetGroupBox)
        self.mediumSlider.setMaximum(100000)
        self.mediumSlider.setOrientation(QtCore.Qt.Horizontal)
        self.mediumSlider.setObjectName("mediumSlider")
        self.gridLayout.addWidget(self.mediumSlider, 3, 3, 1, 1)
        self.highLabel = QtGui.QLabel(self.budgetGroupBox)
        self.highLabel.setTextFormat(QtCore.Qt.RichText)
        self.highLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.highLabel.setObjectName("highLabel")
        self.gridLayout.addWidget(self.highLabel, 4, 0, 1, 1)
        self.highSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.highSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.highSpinBox.setMaximum(100000)
        self.highSpinBox.setObjectName("highSpinBox")
        self.gridLayout.addWidget(self.highSpinBox, 4, 2, 1, 1)
        self.highSlider = QtGui.QSlider(self.budgetGroupBox)
        self.highSlider.setMaximum(100000)
        self.highSlider.setOrientation(QtCore.Qt.Horizontal)
        self.highSlider.setObjectName("highSlider")
        self.gridLayout.addWidget(self.highSlider, 4, 3, 1, 1)
        self.veryHighLabel = QtGui.QLabel(self.budgetGroupBox)
        self.veryHighLabel.setTextFormat(QtCore.Qt.RichText)
        self.veryHighLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.veryHighLabel.setObjectName("veryHighLabel")
        self.gridLayout.addWidget(self.veryHighLabel, 5, 0, 1, 1)
        self.veryHighSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.veryHighSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.veryHighSpinBox.setMaximum(100000)
        self.veryHighSpinBox.setObjectName("veryHighSpinBox")
        self.gridLayout.addWidget(self.veryHighSpinBox, 5, 2, 1, 1)
        self.veryHighSlider = QtGui.QSlider(self.budgetGroupBox)
        self.veryHighSlider.setMaximum(100000)
        self.veryHighSlider.setOrientation(QtCore.Qt.Horizontal)
        self.veryHighSlider.setObjectName("veryHighSlider")
        self.gridLayout.addWidget(self.veryHighSlider, 5, 3, 1, 1)
        self.extremelyHighLabel = QtGui.QLabel(self.budgetGroupBox)
        self.extremelyHighLabel.setTextFormat(QtCore.Qt.RichText)
        self.extremelyHighLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.extremelyHighLabel.setObjectName("extremelyHighLabel")
        self.gridLayout.addWidget(self.extremelyHighLabel, 6, 0, 1, 2)
        self.extremelyHighSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.extremelyHighSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.extremelyHighSpinBox.setMaximum(100000)
        self.extremelyHighSpinBox.setObjectName("extremelyHighSpinBox")
        self.gridLayout.addWidget(self.extremelyHighSpinBox, 6, 2, 1, 1)
        self.extremelyHighSlider = QtGui.QSlider(self.budgetGroupBox)
        self.extremelyHighSlider.setMaximum(100000)
        self.extremelyHighSlider.setOrientation(QtCore.Qt.Horizontal)
        self.extremelyHighSlider.setObjectName("extremelyHighSlider")
        self.gridLayout.addWidget(self.extremelyHighSlider, 6, 3, 1, 1)
        self.line = QtGui.QFrame(self.budgetGroupBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 7, 0, 1, 4)
        self.label = QtGui.QLabel(self.budgetGroupBox)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 8, 0, 1, 1)
        self.budgetSlider = QtGui.QSlider(self.budgetGroupBox)
        self.budgetSlider.setMaximum(100000)
        self.budgetSlider.setOrientation(QtCore.Qt.Horizontal)
        self.budgetSlider.setObjectName("budgetSlider")
        self.gridLayout.addWidget(self.budgetSlider, 8, 3, 1, 1)
        self.budgetSpinBox = QtGui.QSpinBox(self.budgetGroupBox)
        self.budgetSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.budgetSpinBox.setMaximum(100000)
        self.budgetSpinBox.setObjectName("budgetSpinBox")
        self.gridLayout.addWidget(self.budgetSpinBox, 8, 2, 1, 1)
        self.gridLayout_2.addWidget(self.budgetGroupBox, 0, 0, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.resetButton = QtGui.QPushButton(self.centralwidget)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout.addWidget(self.resetButton)
        self.closeButton = QtGui.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        polyCountBudgetMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(polyCountBudgetMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 675, 21))
        self.menubar.setObjectName("menubar")
        self.menuReset = QtGui.QMenu(self.menubar)
        self.menuReset.setObjectName("menuReset")
        polyCountBudgetMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(polyCountBudgetMainWindow)
        self.statusbar.setObjectName("statusbar")
        polyCountBudgetMainWindow.setStatusBar(self.statusbar)
        self.resetAction = QtGui.QAction(polyCountBudgetMainWindow)
        self.resetAction.setObjectName("resetAction")
        self.auditAction = QtGui.QAction(polyCountBudgetMainWindow)
        self.auditAction.setObjectName("auditAction")
        self.menuReset.addAction(self.resetAction)
        self.menuReset.addAction(self.auditAction)
        self.menubar.addAction(self.menuReset.menuAction())

        self.retranslateUi(polyCountBudgetMainWindow)
        QtCore.QMetaObject.connectSlotsByName(polyCountBudgetMainWindow)

    def retranslateUi(self, polyCountBudgetMainWindow):
        polyCountBudgetMainWindow.setWindowTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Poly Count Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.budgetGroupBox.setTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Enter Your Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.trisRadioButton.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Triangle Count", None, QtGui.QApplication.UnicodeUTF8))
        self.vertsRadioButton.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Vertex Count", None, QtGui.QApplication.UnicodeUTF8))
        self.lodCheckBox.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Set LOD", None, QtGui.QApplication.UnicodeUTF8))
        self.extremelyLowLabel.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Extremely Low</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lowLabel.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Low</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.mediumLabel.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Medium</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.highLabel.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">High</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.veryHighLabel.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Very High</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.extremelyHighLabel.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Extremely High</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Budget</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.menuReset.setTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.resetAction.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.auditAction.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Audit your asset", None, QtGui.QApplication.UnicodeUTF8))

