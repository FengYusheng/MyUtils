# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\check_scene\Qt\UI\create_checker\details_window.ui'
#
# Created: Tue Oct 31 14:42:33 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DetailsWindow(object):
    def setupUi(self, DetailsWindow):
        DetailsWindow.setObjectName("DetailsWindow")
        DetailsWindow.resize(790, 596)
        self.centralwidget = QtWidgets.QWidget(DetailsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.suiteLabel = QtWidgets.QLabel(self.centralwidget)
        self.suiteLabel.setObjectName("suiteLabel")
        self.verticalLayout.addWidget(self.suiteLabel)
        self.projectList = QtWidgets.QListView(self.centralwidget)
        self.projectList.setObjectName("projectList")
        self.verticalLayout.addWidget(self.projectList)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.detailsLabel = QtWidgets.QLabel(self.centralwidget)
        self.detailsLabel.setObjectName("detailsLabel")
        self.verticalLayout_2.addWidget(self.detailsLabel)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Panel)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 378, 472))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.previousButton = QtWidgets.QPushButton(self.centralwidget)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout.addWidget(self.previousButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        DetailsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DetailsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 21))
        self.menubar.setObjectName("menubar")
        DetailsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DetailsWindow)
        self.statusbar.setObjectName("statusbar")
        DetailsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DetailsWindow)
        QtCore.QMetaObject.connectSlotsByName(DetailsWindow)

    def retranslateUi(self, DetailsWindow):
        DetailsWindow.setWindowTitle(QtWidgets.QApplication.translate("DetailsWindow", "Set Details", None, -1))
        self.suiteLabel.setText(QtWidgets.QApplication.translate("DetailsWindow", "Suite:", None, -1))
        self.detailsLabel.setText(QtWidgets.QApplication.translate("DetailsWindow", "Details", None, -1))
        self.previousButton.setText(QtWidgets.QApplication.translate("DetailsWindow", "Previous", None, -1))
        self.saveButton.setText(QtWidgets.QApplication.translate("DetailsWindow", "Save", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("DetailsWindow", "Cancel", None, -1))

