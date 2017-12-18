# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt/UI/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.controlDock = QtWidgets.QDockWidget(MainWindow)
        self.controlDock.setObjectName("controlDock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.startButton = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.startButton.setObjectName("startButton")
        self.verticalLayout.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout.addWidget(self.stopButton)
        self.controlDock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.controlDock)
        self.menubar.addAction(self.editMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lottery"))
        self.editMenu.setTitle(_translate("MainWindow", "Edit"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))

