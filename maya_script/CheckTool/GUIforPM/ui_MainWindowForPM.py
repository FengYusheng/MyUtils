# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\CheckTool/Qt/UI/GUIforPM/MainWindowForPM.ui'
#
# Created: Sat Dec  9 11:11:32 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindowForPM(object):
    def setupUi(self, MainWindowForPM):
        MainWindowForPM.setObjectName("MainWindowForPM")
        MainWindowForPM.resize(841, 779)
        self.centralwidget = QtWidgets.QWidget(MainWindowForPM)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.test_label = QtWidgets.QLabel(self.centralwidget)
        self.test_label.setObjectName("test_label")
        self.verticalLayout.addWidget(self.test_label)
        self.checkerListView = QtWidgets.QListView(self.centralwidget)
        self.checkerListView.setObjectName("checkerListView")
        self.verticalLayout.addWidget(self.checkerListView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.verticalLayout_3.addWidget(self.addButton)
        self.removeButtion = QtWidgets.QPushButton(self.centralwidget)
        self.removeButtion.setObjectName("removeButtion")
        self.verticalLayout_3.addWidget(self.removeButtion)
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setObjectName("resetButton")
        self.verticalLayout_3.addWidget(self.resetButton)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.projectLabel = QtWidgets.QLabel(self.centralwidget)
        self.projectLabel.setObjectName("projectLabel")
        self.horizontalLayout_2.addWidget(self.projectLabel)
        self.projectCombo = QtWidgets.QComboBox(self.centralwidget)
        self.projectCombo.setObjectName("projectCombo")
        self.projectCombo.addItem("")
        self.projectCombo.addItem("")
        self.horizontalLayout_2.addWidget(self.projectCombo)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.selectedCheckerListView = QtWidgets.QListView(self.centralwidget)
        self.selectedCheckerListView.setObjectName("selectedCheckerListView")
        self.verticalLayout_2.addWidget(self.selectedCheckerListView)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        MainWindowForPM.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowForPM)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 841, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindowForPM.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowForPM)
        self.statusbar.setObjectName("statusbar")
        MainWindowForPM.setStatusBar(self.statusbar)
        self.actionReset = QtWidgets.QAction(MainWindowForPM)
        self.actionReset.setObjectName("actionReset")
        self.actionSave_as = QtWidgets.QAction(MainWindowForPM)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionDelete = QtWidgets.QAction(MainWindowForPM)
        self.actionDelete.setObjectName("actionDelete")
        self.actionChoose = QtWidgets.QAction(MainWindowForPM)
        self.actionChoose.setObjectName("actionChoose")
        self.menuEdit.addAction(self.actionReset)
        self.menuEdit.addAction(self.actionChoose)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindowForPM)
        QtCore.QMetaObject.connectSlotsByName(MainWindowForPM)

    def retranslateUi(self, MainWindowForPM):
        MainWindowForPM.setWindowTitle(QtWidgets.QApplication.translate("MainWindowForPM", "Configure Check Tool for Project:", None, -1))
        self.test_label.setText(QtWidgets.QApplication.translate("MainWindowForPM", "<html><head/><body><p><span style=\" font-weight:600;\">Select your check item:</span></p></body></html>", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Add", None, -1))
        self.removeButtion.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Remove", None, -1))
        self.resetButton.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Reset", None, -1))
        self.projectLabel.setText(QtWidgets.QApplication.translate("MainWindowForPM", "<html><head/><body><p><span style=\" font-weight:600;\">Project:</span></p></body></html>", None, -1))
        self.projectCombo.setItemText(0, QtWidgets.QApplication.translate("MainWindowForPM", "New project", None, -1))
        self.projectCombo.setItemText(1, QtWidgets.QApplication.translate("MainWindowForPM", "Change location", None, -1))
        self.deleteButton.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Delete", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Cancel", None, -1))
        self.nextButton.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Next", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindowForPM", "Edit", None, -1))
        self.actionReset.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Reset", None, -1))
        self.actionSave_as.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Save as...", None, -1))
        self.actionDelete.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Delete", None, -1))
        self.actionChoose.setText(QtWidgets.QApplication.translate("MainWindowForPM", "Set Project Directory...", None, -1))

