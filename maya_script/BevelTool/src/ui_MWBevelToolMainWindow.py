# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/MWBevelToolMainWindow.ui'
#
# Created: Mon Jan 15 18:11:44 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MWBevelToolMainWindow(object):
    def setupUi(self, MWBevelToolMainWindow):
        MWBevelToolMainWindow.setObjectName("MWBevelToolMainWindow")
        MWBevelToolMainWindow.resize(865, 742)
        self.centralwidget = QtWidgets.QWidget(MWBevelToolMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.toolbarGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.toolbarGroupBox.setTitle("")
        self.toolbarGroupBox.setFlat(True)
        self.toolbarGroupBox.setCheckable(False)
        self.toolbarGroupBox.setObjectName("toolbarGroupBox")
        self.treeView = QtWidgets.QTreeView(self.splitter)
        self.treeView.setObjectName("treeView")
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        MWBevelToolMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MWBevelToolMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 865, 21))
        self.menubar.setObjectName("menubar")
        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        self.viewMenu = QtWidgets.QMenu(self.menubar)
        self.viewMenu.setObjectName("viewMenu")
        MWBevelToolMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MWBevelToolMainWindow)
        self.statusbar.setObjectName("statusbar")
        MWBevelToolMainWindow.setStatusBar(self.statusbar)
        self.controlDock = QtWidgets.QDockWidget(MWBevelToolMainWindow)
        self.controlDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.controlDock.setObjectName("controlDock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setObjectName("gridLayout")
        self.controlPanelTreeView = QtWidgets.QTreeView(self.dockWidgetContents_2)
        self.controlPanelTreeView.setIndentation(20)
        self.controlPanelTreeView.setAnimated(False)
        self.controlPanelTreeView.setWordWrap(True)
        self.controlPanelTreeView.setHeaderHidden(True)
        self.controlPanelTreeView.setObjectName("controlPanelTreeView")
        self.gridLayout.addWidget(self.controlPanelTreeView, 0, 0, 1, 1)
        self.controlDock.setWidget(self.dockWidgetContents_2)
        MWBevelToolMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.controlDock)
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.viewMenu.menuAction())

        self.retranslateUi(MWBevelToolMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MWBevelToolMainWindow)

    def retranslateUi(self, MWBevelToolMainWindow):
        MWBevelToolMainWindow.setWindowTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Mindwalk Bevel Tool", None, -1))
        self.editMenu.setTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Edit", None, -1))
        self.viewMenu.setTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "View", None, -1))
        self.controlDock.setWindowTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Control Panel", None, -1))

