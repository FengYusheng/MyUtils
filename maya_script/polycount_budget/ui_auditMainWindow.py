# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\polycount_budget\Qt\UI\auditMainWindow.ui'
#
# Created: Sat Oct 14 10:25:38 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AuditMainWindow(object):
    def setupUi(self, AuditMainWindow):
        AuditMainWindow.setObjectName("AuditMainWindow")
        AuditMainWindow.resize(1093, 830)
        self.centralwidget = QtGui.QWidget(AuditMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.sceneTreeView = QtGui.QTreeView(self.centralwidget)
        self.sceneTreeView.setObjectName("sceneTreeView")
        self.gridLayout_3.addWidget(self.sceneTreeView, 0, 0, 1, 1)
        AuditMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AuditMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        AuditMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AuditMainWindow)
        self.statusbar.setObjectName("statusbar")
        AuditMainWindow.setStatusBar(self.statusbar)
        self.budgetDock = QtGui.QDockWidget(AuditMainWindow)
        self.budgetDock.setMinimumSize(QtCore.QSize(89, 111))
        self.budgetDock.setFloating(False)
        self.budgetDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.budgetDock.setObjectName("budgetDock")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.budgetTabelView = QtGui.QTableView(self.dockWidgetContents)
        self.budgetTabelView.setFrameShadow(QtGui.QFrame.Plain)
        self.budgetTabelView.setObjectName("budgetTabelView")
        self.gridLayout.addWidget(self.budgetTabelView, 0, 0, 1, 1)
        self.budgetDock.setWidget(self.dockWidgetContents)
        AuditMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.budgetDock)
        self.polyCountDock = QtGui.QDockWidget(AuditMainWindow)
        self.polyCountDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.polyCountDock.setObjectName("polyCountDock")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.polyCountTreeView = QtGui.QTreeView(self.dockWidgetContents_2)
        self.polyCountTreeView.setMouseTracking(False)
        self.polyCountTreeView.setAlternatingRowColors(True)
        self.polyCountTreeView.setObjectName("polyCountTreeView")
        self.gridLayout_2.addWidget(self.polyCountTreeView, 0, 0, 1, 1)
        self.polyCountDock.setWidget(self.dockWidgetContents_2)
        AuditMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.polyCountDock)
        self.resetAction = QtGui.QAction(AuditMainWindow)
        self.resetAction.setObjectName("resetAction")
        self.budgetAction = QtGui.QAction(AuditMainWindow)
        self.budgetAction.setObjectName("budgetAction")
        self.importBudgetAction = QtGui.QAction(AuditMainWindow)
        self.importBudgetAction.setObjectName("importBudgetAction")
        self.polyCountAction = QtGui.QAction(AuditMainWindow)
        self.polyCountAction.setObjectName("polyCountAction")
        self.menuEdit.addAction(self.resetAction)
        self.menuEdit.addAction(self.budgetAction)
        self.menuEdit.addAction(self.importBudgetAction)
        self.menuEdit.addAction(self.polyCountAction)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(AuditMainWindow)
        QtCore.QMetaObject.connectSlotsByName(AuditMainWindow)

    def retranslateUi(self, AuditMainWindow):
        AuditMainWindow.setWindowTitle(QtGui.QApplication.translate("AuditMainWindow", "Audit your asset", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("AuditMainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("AuditMainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.budgetDock.setWindowTitle(QtGui.QApplication.translate("AuditMainWindow", "Budget and LOD", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountDock.setWindowTitle(QtGui.QApplication.translate("AuditMainWindow", "Poly Count in Current Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.resetAction.setText(QtGui.QApplication.translate("AuditMainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.budgetAction.setText(QtGui.QApplication.translate("AuditMainWindow", "Enter your budget", None, QtGui.QApplication.UnicodeUTF8))
        self.importBudgetAction.setText(QtGui.QApplication.translate("AuditMainWindow", "Import Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountAction.setText(QtGui.QApplication.translate("AuditMainWindow", "Poly Count", None, QtGui.QApplication.UnicodeUTF8))

