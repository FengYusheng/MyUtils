# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myLittleTimer.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myLitteTimer(object):
    def setupUi(self, myLitteTimer):
        myLitteTimer.setObjectName("myLitteTimer")
        myLitteTimer.resize(607, 388)
        self.centralwidget = QtWidgets.QWidget(myLitteTimer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeEdit.setTimeSpec(QtCore.Qt.LocalTime)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.verticalLayout.addWidget(self.dateTimeEdit)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        myLitteTimer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(myLitteTimer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 607, 28))
        self.menubar.setObjectName("menubar")
        myLitteTimer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(myLitteTimer)
        self.statusbar.setObjectName("statusbar")
        myLitteTimer.setStatusBar(self.statusbar)

        self.retranslateUi(myLitteTimer)
        QtCore.QMetaObject.connectSlotsByName(myLitteTimer)

    def retranslateUi(self, myLitteTimer):
        _translate = QtCore.QCoreApplication.translate
        myLitteTimer.setWindowTitle(_translate("myLitteTimer", "MainWindow"))

