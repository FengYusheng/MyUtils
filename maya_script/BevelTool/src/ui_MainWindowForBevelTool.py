# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MayaTools\BevelTool/src/Qt/UI/MainWindowForBevelTool.ui'
#
# Created: Mon Dec 11 11:59:40 2017
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 654, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindowForBevelTool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowForBevelTool)
        self.statusbar.setObjectName("statusbar")
        MainWindowForBevelTool.setStatusBar(self.statusbar)
        self.simpleOptionsAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.simpleOptionsAction.setCheckable(True)
        self.simpleOptionsAction.setChecked(False)
        self.simpleOptionsAction.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.simpleOptionsAction.setObjectName("simpleOptionsAction")
        self.fullOptionsAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.fullOptionsAction.setCheckable(True)
        self.fullOptionsAction.setObjectName("fullOptionsAction")
        self.hardEdgesAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.hardEdgesAction.setObjectName("hardEdgesAction")
        self.menuEdit.addAction(self.simpleOptionsAction)
        self.menuEdit.addAction(self.fullOptionsAction)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindowForBevelTool)
        QtCore.QMetaObject.connectSlotsByName(MainWindowForBevelTool)

    def retranslateUi(self, MainWindowForBevelTool):
        MainWindowForBevelTool.setWindowTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "MainWindow", None, -1))
        self.bevelButton.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Bevel", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Edit", None, -1))
        self.simpleOptionsAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Simple options", None, -1))
        self.fullOptionsAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Full options", None, -1))
        self.hardEdgesAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Hard edges", None, -1))

