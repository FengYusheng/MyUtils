# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\Draft\polycount_budget\Qt\UI\polyCountBudget3.ui'
#
# Created: Wed Oct 11 10:34:16 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_polyCountBudgetMainWindow(object):
    def setupUi(self, polyCountBudgetMainWindow):
        polyCountBudgetMainWindow.setObjectName("polyCountBudgetMainWindow")
        polyCountBudgetMainWindow.resize(965, 789)
        self.centralwidget = QtWidgets.QWidget(polyCountBudgetMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        polyCountBudgetMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(polyCountBudgetMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 965, 21))
        self.menubar.setObjectName("menubar")
        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        self.viewMenu = QtWidgets.QMenu(self.menubar)
        self.viewMenu.setObjectName("viewMenu")
        polyCountBudgetMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(polyCountBudgetMainWindow)
        self.statusbar.setObjectName("statusbar")
        polyCountBudgetMainWindow.setStatusBar(self.statusbar)
        self.budgetDock = QtWidgets.QDockWidget(polyCountBudgetMainWindow)
        self.budgetDock.setObjectName("budgetDock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.polyCountTab = QtWidgets.QTabWidget(self.dockWidgetContents)
        self.polyCountTab.setObjectName("polyCountTab")
        self.setBudgetTab = QtWidgets.QWidget()
        self.setBudgetTab.setObjectName("setBudgetTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.setBudgetTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.setBudgetTableView = QtWidgets.QTableView(self.setBudgetTab)
        self.setBudgetTableView.setObjectName("setBudgetTableView")
        self.gridLayout_2.addWidget(self.setBudgetTableView, 0, 0, 1, 1)
        self.polyCountTab.addTab(self.setBudgetTab, "")
        self.polycontInScene = QtWidgets.QWidget()
        self.polycontInScene.setObjectName("polycontInScene")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.polycontInScene)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.polycountTreeView = QtWidgets.QTreeView(self.polycontInScene)
        self.polycountTreeView.setObjectName("polycountTreeView")
        self.gridLayout_3.addWidget(self.polycountTreeView, 0, 0, 1, 1)
        self.polyCountTab.addTab(self.polycontInScene, "")
        self.gridLayout.addWidget(self.polyCountTab, 0, 0, 1, 1)
        self.budgetDock.setWidget(self.dockWidgetContents)
        polyCountBudgetMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.budgetDock)
        self.resetAction = QtWidgets.QAction(polyCountBudgetMainWindow)
        self.resetAction.setObjectName("resetAction")
        self.editMenu.addAction(self.resetAction)
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.viewMenu.menuAction())

        self.retranslateUi(polyCountBudgetMainWindow)
        self.polyCountTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(polyCountBudgetMainWindow)

    def retranslateUi(self, polyCountBudgetMainWindow):
        polyCountBudgetMainWindow.setWindowTitle(QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "Set Your Polycount Budget", None, -1))
        self.editMenu.setTitle(QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "Edit", None, -1))
        self.viewMenu.setTitle(QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "View", None, -1))
        self.budgetDock.setWindowTitle(QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "Poly Count Budget", None, -1))
        self.polyCountTab.setTabText(self.polyCountTab.indexOf(self.setBudgetTab), QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "Set Budget", None, -1))
        self.polyCountTab.setTabText(self.polyCountTab.indexOf(self.polycontInScene), QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "Polycont in Scene", None, -1))
        self.resetAction.setText(QtWidgets.QApplication.translate("polyCountBudgetMainWindow", "Reset", None, -1))

