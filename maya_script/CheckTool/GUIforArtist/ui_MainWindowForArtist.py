# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\MWCheckTool/Qt/UI/GUIforArtist/MainWindowForArtist.ui'
#
# Created: Thu Dec 07 18:14:48 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindowForArtist(object):
    def setupUi(self, MainWindowForArtist):
        MainWindowForArtist.setObjectName("MainWindowForArtist")
        MainWindowForArtist.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindowForArtist)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setObjectName("checkButton")
        self.horizontalLayout_2.addWidget(self.checkButton)
        self.projectComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.projectComboBox.setObjectName("projectComboBox")
        self.projectComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.projectComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkerTableView = QtWidgets.QTableView(self.centralwidget)
        self.checkerTableView.setObjectName("checkerTableView")
        self.horizontalLayout.addWidget(self.checkerTableView)
        self.messageTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.messageTabWidget.setObjectName("messageTabWidget")
        self.tipTab = QtWidgets.QWidget()
        self.tipTab.setObjectName("tipTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tipTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tipTextBrower = QtWidgets.QTextBrowser(self.tipTab)
        self.tipTextBrower.setObjectName("tipTextBrower")
        self.gridLayout_3.addWidget(self.tipTextBrower, 0, 0, 1, 1)
        self.messageTabWidget.addTab(self.tipTab, "")
        self.detailTab = QtWidgets.QWidget()
        self.detailTab.setObjectName("detailTab")
        self.gridLayout = QtWidgets.QGridLayout(self.detailTab)
        self.gridLayout.setObjectName("gridLayout")
        self.detailTableView = QtWidgets.QTableView(self.detailTab)
        self.detailTableView.setObjectName("detailTableView")
        self.gridLayout.addWidget(self.detailTableView, 0, 0, 1, 1)
        self.messageTabWidget.addTab(self.detailTab, "")
        self.horizontalLayout.addWidget(self.messageTabWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.displayTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.displayTabWidget.setObjectName("displayTabWidget")
        self.resultTab = QtWidgets.QWidget()
        self.resultTab.setObjectName("resultTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.resultTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.resultTreeView = QtWidgets.QTreeView(self.resultTab)
        self.resultTreeView.setObjectName("resultTreeView")
        self.gridLayout_2.addWidget(self.resultTreeView, 0, 0, 1, 1)
        self.displayTabWidget.addTab(self.resultTab, "")
        self.displayTab = QtWidgets.QWidget()
        self.displayTab.setObjectName("displayTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.displayTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.outputTextBrower = QtWidgets.QTextBrowser(self.displayTab)
        self.outputTextBrower.setObjectName("outputTextBrower")
        self.gridLayout_4.addWidget(self.outputTextBrower, 0, 0, 1, 1)
        self.displayTabWidget.addTab(self.displayTab, "")
        self.verticalLayout.addWidget(self.displayTabWidget)
        MainWindowForArtist.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowForArtist)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindowForArtist.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowForArtist)
        self.statusbar.setObjectName("statusbar")
        MainWindowForArtist.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowForArtist)
        self.messageTabWidget.setCurrentIndex(0)
        self.displayTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindowForArtist)

    def retranslateUi(self, MainWindowForArtist):
        MainWindowForArtist.setWindowTitle(QtWidgets.QApplication.translate("MainWindowForArtist", "Check Your Asset: ", None, -1))
        self.checkButton.setText(QtWidgets.QApplication.translate("MainWindowForArtist", "Check Asset", None, -1))
        self.projectComboBox.setItemText(0, QtWidgets.QApplication.translate("MainWindowForArtist", "Change location", None, -1))
        self.messageTabWidget.setTabText(self.messageTabWidget.indexOf(self.tipTab), QtWidgets.QApplication.translate("MainWindowForArtist", "Tip", None, -1))
        self.messageTabWidget.setTabText(self.messageTabWidget.indexOf(self.detailTab), QtWidgets.QApplication.translate("MainWindowForArtist", "Detail", None, -1))
        self.displayTabWidget.setTabText(self.displayTabWidget.indexOf(self.resultTab), QtWidgets.QApplication.translate("MainWindowForArtist", "Result", None, -1))
        self.displayTabWidget.setTabText(self.displayTabWidget.indexOf(self.displayTab), QtWidgets.QApplication.translate("MainWindowForArtist", "Display", None, -1))

