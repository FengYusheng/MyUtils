# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Qt\UI\ControlPanel.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_controlPanelWidget(object):
    def setupUi(self, controlPanelWidget):
        controlPanelWidget.setObjectName("controlPanelWidget")
        controlPanelWidget.resize(494, 343)
        self.verticalLayout = QtWidgets.QVBoxLayout(controlPanelWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.filePathLabel = QtWidgets.QLabel(controlPanelWidget)
        self.filePathLabel.setObjectName("filePathLabel")
        self.gridLayout.addWidget(self.filePathLabel, 0, 0, 1, 1)
        self.filePathLineEdit = QtWidgets.QLineEdit(controlPanelWidget)
        self.filePathLineEdit.setObjectName("filePathLineEdit")
        self.gridLayout.addWidget(self.filePathLineEdit, 0, 1, 1, 1)
        self.openFileButton = QtWidgets.QPushButton(controlPanelWidget)
        self.openFileButton.setObjectName("openFileButton")
        self.gridLayout.addWidget(self.openFileButton, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(controlPanelWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startButton = QtWidgets.QPushButton(controlPanelWidget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_2.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(controlPanelWidget)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(controlPanelWidget)
        QtCore.QMetaObject.connectSlotsByName(controlPanelWidget)

    def retranslateUi(self, controlPanelWidget):
        _translate = QtCore.QCoreApplication.translate
        controlPanelWidget.setWindowTitle(_translate("controlPanelWidget", "Form"))
        self.filePathLabel.setText(_translate("controlPanelWidget", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Player path:</span></p></body></html>"))
        self.openFileButton.setText(_translate("controlPanelWidget", "Open "))
        self.startButton.setText(_translate("controlPanelWidget", "Start"))
        self.stopButton.setText(_translate("controlPanelWidget", "Stop"))

