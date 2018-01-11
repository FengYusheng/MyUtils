# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Qt\UI\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        self.viewMenu = QtWidgets.QMenu(self.menubar)
        self.viewMenu.setObjectName("viewMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.controlPanelDock = QtWidgets.QDockWidget(MainWindow)
        self.controlPanelDock.setFloating(True)
        self.controlPanelDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.controlPanelDock.setObjectName("controlPanelDock")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.controlPanelDock.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.controlPanelDock)
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.viewMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lottery"))
        self.editMenu.setTitle(_translate("MainWindow", "Edit"))
        self.viewMenu.setTitle(_translate("MainWindow", "View"))
        self.controlPanelDock.setWindowTitle(_translate("MainWindow", "Control panel"))

