# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\CheckTool/Qt/UI/GUIforPM/DetailsWindowForPM.ui'
#
# Created: Sat Dec  9 11:11:32 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DetailsMainWindowForPm(object):
    def setupUi(self, DetailsMainWindowForPm):
        DetailsMainWindowForPm.setObjectName("DetailsMainWindowForPm")
        DetailsMainWindowForPm.resize(854, 725)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DetailsMainWindowForPm.sizePolicy().hasHeightForWidth())
        DetailsMainWindowForPm.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(DetailsMainWindowForPm)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkerListView = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkerListView.sizePolicy().hasHeightForWidth())
        self.checkerListView.setSizePolicy(sizePolicy)
        self.checkerListView.setResizeMode(QtWidgets.QListView.Adjust)
        self.checkerListView.setObjectName("checkerListView")
        self.horizontalLayout.addWidget(self.checkerListView)
        self.checkerTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.checkerTabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.checkerTabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.checkerTabWidget.setMovable(False)
        self.checkerTabWidget.setTabBarAutoHide(True)
        self.checkerTabWidget.setObjectName("checkerTabWidget")
        self.tipTab = QtWidgets.QWidget()
        self.tipTab.setObjectName("tipTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tipTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tipTextBrower = QtWidgets.QTextBrowser(self.tipTab)
        self.tipTextBrower.setReadOnly(False)
        self.tipTextBrower.setObjectName("tipTextBrower")
        self.gridLayout_2.addWidget(self.tipTextBrower, 0, 0, 1, 1)
        self.checkerTabWidget.addTab(self.tipTab, "")
        self.detailTab = QtWidgets.QWidget()
        self.detailTab.setObjectName("detailTab")
        self.gridLayout = QtWidgets.QGridLayout(self.detailTab)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollAreaInDetailTab = QtWidgets.QScrollArea(self.detailTab)
        self.scrollAreaInDetailTab.setWidgetResizable(True)
        self.scrollAreaInDetailTab.setObjectName("scrollAreaInDetailTab")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaInDetailTab.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollAreaInDetailTab, 0, 0, 1, 1)
        self.checkerTabWidget.addTab(self.detailTab, "")
        self.checkTab = QtWidgets.QWidget()
        self.checkTab.setObjectName("checkTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.checkTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollAreaInCheckTab = QtWidgets.QScrollArea(self.checkTab)
        self.scrollAreaInCheckTab.setWidgetResizable(True)
        self.scrollAreaInCheckTab.setObjectName("scrollAreaInCheckTab")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaInCheckTab.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.addWidget(self.scrollAreaInCheckTab, 0, 0, 1, 1)
        self.checkerTabWidget.addTab(self.checkTab, "")
        self.horizontalLayout.addWidget(self.checkerTabWidget)
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prevButton = QtWidgets.QPushButton(self.centralwidget)
        self.prevButton.setObjectName("prevButton")
        self.horizontalLayout_2.addWidget(self.prevButton)
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout_2.addWidget(self.applyButton)
        self.finishButton = QtWidgets.QPushButton(self.centralwidget)
        self.finishButton.setObjectName("finishButton")
        self.horizontalLayout_2.addWidget(self.finishButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        DetailsMainWindowForPm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DetailsMainWindowForPm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 854, 23))
        self.menubar.setObjectName("menubar")
        DetailsMainWindowForPm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DetailsMainWindowForPm)
        self.statusbar.setObjectName("statusbar")
        DetailsMainWindowForPm.setStatusBar(self.statusbar)

        self.retranslateUi(DetailsMainWindowForPm)
        self.checkerTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DetailsMainWindowForPm)

    def retranslateUi(self, DetailsMainWindowForPm):
        DetailsMainWindowForPm.setWindowTitle(QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Configure Check Tool for project: ", None, -1))
        self.tipTextBrower.setHtml(QtWidgets.QApplication.translate("DetailsMainWindowForPm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:12pt;\"><br /></p></body></html>", None, -1))
        self.checkerTabWidget.setTabText(self.checkerTabWidget.indexOf(self.tipTab), QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Tip", None, -1))
        self.checkerTabWidget.setTabText(self.checkerTabWidget.indexOf(self.detailTab), QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Detail", None, -1))
        self.checkerTabWidget.setTabText(self.checkerTabWidget.indexOf(self.checkTab), QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Check Now", None, -1))
        self.prevButton.setText(QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Previous", None, -1))
        self.applyButton.setText(QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Apply", None, -1))
        self.finishButton.setText(QtWidgets.QApplication.translate("DetailsMainWindowForPm", "Finish", None, -1))

