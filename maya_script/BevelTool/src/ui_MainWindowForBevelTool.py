# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\BevelTool/src/Qt/UI/MainWindowForBevelTool.ui'
#
# Created: Sun Dec 10 21:20:02 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindowForBevelTool(object):
    def setupUi(self, MainWindowForBevelTool):
        MainWindowForBevelTool.setObjectName("MainWindowForBevelTool")
        MainWindowForBevelTool.resize(654, 477)
        self.centralwidget = QtWidgets.QWidget(MainWindowForBevelTool)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.bevelButton = QtWidgets.QPushButton(self.centralwidget)
        self.bevelButton.setObjectName("bevelButton")
        self.gridLayout.addWidget(self.bevelButton, 0, 0, 1, 1)
        self.optionTableView = QtWidgets.QTableView(self.centralwidget)
        self.optionTableView.setObjectName("optionTableView")
        self.gridLayout.addWidget(self.optionTableView, 1, 0, 1, 1)
        MainWindowForBevelTool.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowForBevelTool)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 654, 23))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSelectConstraint = QtWidgets.QMenu(self.menubar)
        self.menuSelectConstraint.setObjectName("menuSelectConstraint")
        MainWindowForBevelTool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowForBevelTool)
        self.statusbar.setObjectName("statusbar")
        MainWindowForBevelTool.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSelectConstraint.menuAction())

        self.retranslateUi(MainWindowForBevelTool)
        QtCore.QMetaObject.connectSlotsByName(MainWindowForBevelTool)

    def retranslateUi(self, MainWindowForBevelTool):
        MainWindowForBevelTool.setWindowTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "MainWindow", None, -1))
        self.bevelButton.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Bevel", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Edit", None, -1))
        self.menuSelectConstraint.setTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "SelectConstraint", None, -1))

