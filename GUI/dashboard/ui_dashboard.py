# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt/UI/dashboard.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DashboardMainWindow(object):
    def setupUi(self, DashboardMainWindow):
        DashboardMainWindow.setObjectName("DashboardMainWindow")
        DashboardMainWindow.resize(755, 569)
        self.centralwidget = QtWidgets.QWidget(DashboardMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        DashboardMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DashboardMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 755, 28))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        DashboardMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DashboardMainWindow)
        self.statusbar.setObjectName("statusbar")
        DashboardMainWindow.setStatusBar(self.statusbar)
        self.budgetDock = QtWidgets.QDockWidget(DashboardMainWindow)
        self.budgetDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.budgetDock.setObjectName("budgetDock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.budgetTableView = QtWidgets.QTableView(self.dockWidgetContents_2)
        self.budgetTableView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.budgetTableView.setObjectName("budgetTableView")
        self.gridLayout.addWidget(self.budgetTableView, 0, 0, 1, 1)
        self.budgetDock.setWidget(self.dockWidgetContents_2)
        DashboardMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.budgetDock)
        self.sliderDock = QtWidgets.QDockWidget(DashboardMainWindow)
        self.sliderDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.sliderDock.setObjectName("sliderDock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.polyCountSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.polyCountSlider.setOrientation(QtCore.Qt.Vertical)
        self.polyCountSlider.setObjectName("polyCountSlider")
        self.gridLayout_2.addWidget(self.polyCountSlider, 0, 0, 1, 1)
        self.sliderDock.setWidget(self.dockWidgetContents)
        DashboardMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.sliderDock)
        self.importDataAction = QtWidgets.QAction(DashboardMainWindow)
        self.importDataAction.setObjectName("importDataAction")
        self.menuEdit.addAction(self.importDataAction)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(DashboardMainWindow)
        QtCore.QMetaObject.connectSlotsByName(DashboardMainWindow)

    def retranslateUi(self, DashboardMainWindow):
        _translate = QtCore.QCoreApplication.translate
        DashboardMainWindow.setWindowTitle(_translate("DashboardMainWindow", "Dash Board"))
        self.menuEdit.setTitle(_translate("DashboardMainWindow", "Edit"))
        self.menuView.setTitle(_translate("DashboardMainWindow", "View"))
        self.budgetDock.setWindowTitle(_translate("DashboardMainWindow", "Budget"))
        self.sliderDock.setWindowTitle(_translate("DashboardMainWindow", "Control Poly Count "))
        self.importDataAction.setText(_translate("DashboardMainWindow", "Import Data"))

