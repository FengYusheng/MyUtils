# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\MWCheckTool/Qt/UI/GUIforPM/deleteProjectDialog.ui'
#
# Created: Fri Dec 01 17:29:29 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_deleteProjectDialog(object):
    def setupUi(self, deleteProjectDialog):
        deleteProjectDialog.setObjectName("deleteProjectDialog")
        deleteProjectDialog.resize(492, 123)
        self.gridLayout = QtWidgets.QGridLayout(deleteProjectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.projectLabel = QtWidgets.QLabel(deleteProjectDialog)
        self.projectLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.projectLabel.setObjectName("projectLabel")
        self.gridLayout.addWidget(self.projectLabel, 0, 0, 1, 2)
        self.applyButton = QtWidgets.QPushButton(deleteProjectDialog)
        self.applyButton.setDefault(True)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout.addWidget(self.applyButton, 1, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(deleteProjectDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 1, 1, 1, 1)

        self.retranslateUi(deleteProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(deleteProjectDialog)

    def retranslateUi(self, deleteProjectDialog):
        deleteProjectDialog.setWindowTitle(QtWidgets.QApplication.translate("deleteProjectDialog", "Dialog", None, -1))
        self.projectLabel.setText(QtWidgets.QApplication.translate("deleteProjectDialog", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Delete project:</span></p></body></html>", None, -1))
        self.applyButton.setText(QtWidgets.QApplication.translate("deleteProjectDialog", "Apply", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("deleteProjectDialog", "Cancle", None, -1))

