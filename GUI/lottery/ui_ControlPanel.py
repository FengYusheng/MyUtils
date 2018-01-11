# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Qt\UI\ControlPanel.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ControlPanelWidge(object):
    def setupUi(self, ControlPanelWidge):
        ControlPanelWidge.setObjectName("ControlPanelWidge")
        ControlPanelWidge.resize(628, 425)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ControlPanelWidge)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(ControlPanelWidge)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.playerPathLabel = QtWidgets.QLabel(self.widget)
        self.playerPathLabel.setObjectName("playerPathLabel")
        self.gridLayout.addWidget(self.playerPathLabel, 0, 0, 1, 1)
        self.playerPathLineEdit = QtWidgets.QLineEdit(self.widget)
        self.playerPathLineEdit.setObjectName("playerPathLineEdit")
        self.gridLayout.addWidget(self.playerPathLineEdit, 0, 1, 1, 1)
        self.openButton = QtWidgets.QPushButton(self.widget)
        self.openButton.setObjectName("openButton")
        self.gridLayout.addWidget(self.openButton, 0, 2, 1, 1)
        self.playerNumberLabel = QtWidgets.QLabel(self.widget)
        self.playerNumberLabel.setObjectName("playerNumberLabel")
        self.gridLayout.addWidget(self.playerNumberLabel, 1, 0, 1, 1)
        self.playerNumberSpinBox = QtWidgets.QSpinBox(self.widget)
        self.playerNumberSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.playerNumberSpinBox.setMinimum(1)
        self.playerNumberSpinBox.setMaximum(300)
        self.playerNumberSpinBox.setObjectName("playerNumberSpinBox")
        self.gridLayout.addWidget(self.playerNumberSpinBox, 1, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QFrame(self.widget1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.startButton = QtWidgets.QPushButton(self.widget1)
        self.startButton.setObjectName("startButton")
        self.verticalLayout.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.widget1)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout.addWidget(self.stopButton)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(ControlPanelWidge)
        QtCore.QMetaObject.connectSlotsByName(ControlPanelWidge)

    def retranslateUi(self, ControlPanelWidge):
        _translate = QtCore.QCoreApplication.translate
        ControlPanelWidge.setWindowTitle(_translate("ControlPanelWidge", "Form"))
        self.playerPathLabel.setText(_translate("ControlPanelWidge", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Player path:</span></p></body></html>"))
        self.openButton.setText(_translate("ControlPanelWidge", "Open"))
        self.playerNumberLabel.setText(_translate("ControlPanelWidge", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Player number:</span></p></body></html>"))
        self.startButton.setText(_translate("ControlPanelWidge", "Start"))
        self.stopButton.setText(_translate("ControlPanelWidge", "Pause"))

