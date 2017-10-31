# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\check_scene\Qt\UI\create_checker\delete.ui'
#
# Created: Tue Oct 31 14:42:33 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_deletePojectDailog(object):
    def setupUi(self, deletePojectDailog):
        deletePojectDailog.setObjectName("deletePojectDailog")
        deletePojectDailog.resize(176, 83)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(deletePojectDailog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.project_la = QtWidgets.QLabel(deletePojectDailog)
        self.project_la.setText("")
        self.project_la.setObjectName("project_la")
        self.verticalLayout.addWidget(self.project_la)
        self.path_la = QtWidgets.QLabel(deletePojectDailog)
        self.path_la.setText("")
        self.path_la.setObjectName("path_la")
        self.verticalLayout.addWidget(self.path_la)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_button = QtWidgets.QPushButton(deletePojectDailog)
        self.yes_button.setObjectName("yes_button")
        self.horizontalLayout.addWidget(self.yes_button)
        self.no_button = QtWidgets.QPushButton(deletePojectDailog)
        self.no_button.setObjectName("no_button")
        self.horizontalLayout.addWidget(self.no_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(deletePojectDailog)
        QtCore.QMetaObject.connectSlotsByName(deletePojectDailog)

    def retranslateUi(self, deletePojectDailog):
        deletePojectDailog.setWindowTitle(QtWidgets.QApplication.translate("deletePojectDailog", "Dialog", None, -1))
        self.yes_button.setText(QtWidgets.QApplication.translate("deletePojectDailog", "Yes", None, -1))
        self.no_button.setText(QtWidgets.QApplication.translate("deletePojectDailog", "No", None, -1))

