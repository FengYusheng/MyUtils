# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/OptionTableViewWidget.ui'
#
# Created: Fri Mar 09 16:47:28 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_optionTableViewWidiget(object):
    def setupUi(self, optionTableViewWidiget):
        optionTableViewWidiget.setObjectName("optionTableViewWidiget")
        optionTableViewWidiget.resize(531, 348)
        self.verticalLayout = QtWidgets.QVBoxLayout(optionTableViewWidiget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bevelButton = QtWidgets.QPushButton(optionTableViewWidiget)
        self.bevelButton.setObjectName("bevelButton")
        self.verticalLayout.addWidget(self.bevelButton)
        self.optionTableView = QtWidgets.QTableView(optionTableViewWidiget)
        self.optionTableView.setObjectName("optionTableView")
        self.verticalLayout.addWidget(self.optionTableView)

        self.retranslateUi(optionTableViewWidiget)
        QtCore.QMetaObject.connectSlotsByName(optionTableViewWidiget)

    def retranslateUi(self, optionTableViewWidiget):
        optionTableViewWidiget.setWindowTitle(QtWidgets.QApplication.translate("optionTableViewWidiget", "Form", None, -1))
        self.bevelButton.setText(QtWidgets.QApplication.translate("optionTableViewWidiget", "Bevel", None, -1))

