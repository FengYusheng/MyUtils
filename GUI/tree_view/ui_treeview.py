# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tree_view.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 593)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.suiteButton = QtWidgets.QPushButton(self.centralwidget)
        self.suiteButton.setObjectName("suiteButton")
        self.horizontalLayout.addWidget(self.suiteButton)
        self.detailButton = QtWidgets.QPushButton(self.centralwidget)
        self.detailButton.setObjectName("detailButton")
        self.horizontalLayout.addWidget(self.detailButton)
        self.simpleButton = QtWidgets.QPushButton(self.centralwidget)
        self.simpleButton.setObjectName("simpleButton")
        self.horizontalLayout.addWidget(self.simpleButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menusuite = QtWidgets.QMenu(self.menubar)
        self.menusuite.setObjectName("menusuite")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRead_configuration = QtWidgets.QAction(MainWindow)
        self.actionRead_configuration.setObjectName("actionRead_configuration")
        self.menuHelp.addAction(self.actionRead_configuration)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menusuite.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.suiteButton.setText(_translate("MainWindow", "Suite"))
        self.detailButton.setText(_translate("MainWindow", "Detail"))
        self.simpleButton.setText(_translate("MainWindow", "Simple"))
        self.menuHelp.setTitle(_translate("MainWindow", "edit"))
        self.menusuite.setTitle(_translate("MainWindow", "suite"))
        self.menuhelp.setTitle(_translate("MainWindow", "help"))
        self.actionRead_configuration.setText(_translate("MainWindow", "Read configuration"))

