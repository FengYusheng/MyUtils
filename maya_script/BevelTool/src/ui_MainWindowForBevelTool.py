# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/MainWindowForBevelTool.ui'
#
# Created: Fri Feb 02 14:56:34 2018
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
        MainWindowForBevelTool.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowForBevelTool)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 654, 23))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindowForBevelTool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowForBevelTool)
        self.statusbar.setObjectName("statusbar")
        MainWindowForBevelTool.setStatusBar(self.statusbar)
        self.simpleBevelOptionsAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.simpleBevelOptionsAction.setCheckable(True)
        self.simpleBevelOptionsAction.setChecked(False)
        self.simpleBevelOptionsAction.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.simpleBevelOptionsAction.setObjectName("simpleBevelOptionsAction")
        self.fullBevelOptionsAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.fullBevelOptionsAction.setCheckable(True)
        self.fullBevelOptionsAction.setObjectName("fullBevelOptionsAction")
        self.hardEdgesAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.hardEdgesAction.setObjectName("hardEdgesAction")
        self.bevelSetEditorAction = QtWidgets.QAction(MainWindowForBevelTool)
        self.bevelSetEditorAction.setCheckable(True)
        self.bevelSetEditorAction.setObjectName("bevelSetEditorAction")
        self.menuEdit.addAction(self.simpleBevelOptionsAction)
        self.menuEdit.addAction(self.fullBevelOptionsAction)
        self.menuEdit.addAction(self.bevelSetEditorAction)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindowForBevelTool)
        QtCore.QMetaObject.connectSlotsByName(MainWindowForBevelTool)

    def retranslateUi(self, MainWindowForBevelTool):
        MainWindowForBevelTool.setWindowTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "MainWindow", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Edit", None, -1))
        self.simpleBevelOptionsAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Simple bevel options", None, -1))
        self.fullBevelOptionsAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Full bevel options", None, -1))
        self.hardEdgesAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Hard edges", None, -1))
        self.bevelSetEditorAction.setText(QtWidgets.QApplication.translate("MainWindowForBevelTool", "Bevel set editor", None, -1))

