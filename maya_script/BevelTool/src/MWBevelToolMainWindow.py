# -*- coding: utf-8 -*-
import copy

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from pyside2uic import compileUi
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from pysideuic import compileUi
    from PySide import __version__
    from shiboken import wrapInstance

import maya.OpenMayaUI as apiUI

import ui_MWBevelToolMainWindow
reload(ui_MWBevelToolMainWindow)
import utils
reload(utils)
import bevelTool
reload(bevelTool)
import status
reload(status)
import options
reload(options)



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class ControlPanelDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ControlPanelDelegate, self).__init__(parent)
        self.parent = parent

    # def createEditor(self, parent, option, index):
    #     item = self.parent.dataModelInControlPanelTreeView.itemFromIndex(index)
    #     editor = MWBevelToolPanels.MWBevelSetPanel(self.parent)
    #     return editor
    #
    #
    # def setEditorData(self, editor, index):
    #     pass
    #
    #
    # def setModelData(self, editor, model, index):
    #     pass
    #
    #
    # def updateEditorGeometry(self, editor, option, index):
    #     _rect = option.rect
    #     _rect.setHeight(editor.height())
    #     editor.setGeometry(_rect)

    def paint(self, painter, option, index):
        parentIndex = self.parent.dataModelInControlPanelTreeView.parent(index)
        if parentIndex.row() >= 0:
            bevelsetPanel = MWBevelToolPanels.MWBevelSetPanel(self.parent)
            groupBoxOption = QStyleOptionGroupBox()
            groupBoxOption.activeSubControls = QStyle.SC_All
            self.parent.toolbarGroupBox.initStyleOption(groupBoxOption)
            groupBoxOption.rect = option.rect
            groupBoxOption.rect.setHeight(bevelsetPanel.height())
            groupBoxOption.styleObject = bevelsetPanel
            QApplication.style().drawComplexControl(QStyle.CC_GroupBox, groupBoxOption, painter, bevelsetPanel)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)



class MWBevelToolMainWindow(QMainWindow, ui_MWBevelToolMainWindow.Ui_MWBevelToolMainWindow):
    HEADERSINBEVELSETTREEVIEW = ('Bevel Set', 'Members')
    def __init__(self, parent=None):
        super(MWBevelToolMainWindow, self).__init__(parent)

        self.headerFont = QFont('OldEnglish', 10, QFont.Bold)
        self.itemFont = QFont('OldEnglish', 10)
        self.bevelOptions = copy.copy(options.bevelOptions)

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.bevelSetLabel.mousePressEvent = self._mousePressEventInBevelSetLabel
        self.selectionLabel.mousePressEvent = self._mousePressEventInSelectionLabel
        self.bevelOptionsLabel.mousePressEvent = self._mousePressEventInBevelOptionslabel
        self.bevelLabel.mousePressEvent = self._mousePressEventInBevelLabel
        self.bevelSetTreeView.mousePressEvent = self._mousePressEventInBevelSetTreeView
        self.dataModelInBevelSetTreeView = QStandardItemModel(self.bevelSetTreeView)
        self.bevelSetTreeView.setModel(self.dataModelInBevelSetTreeView)
        self.selectionModelInBevelSetTreeView = QItemSelectionModel(self.dataModelInBevelSetTreeView, self.bevelSetTreeView)
        self.bevelSetTreeView.setSelectionModel(self.selectionModelInBevelSetTreeView)

        self.updateBevelSetTreeView()

        self.newBevelSetButton.clicked.connect(self.createNewBevelSet)
        self.addMemberButton.clicked.connect(self.addEdgesIntoBevelSet)
        self.removeMemberButton.clicked.connect(self.removeEdgesFromBevelSet)


    def _mousePressEventInBevelSetLabel(self, event):
        isVisible = not self.bevelSetGroupBox.isVisible()
        self.bevelSetGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelSetLabel, event)


    def _mousePressEventInSelectionLabel(self, event):
        isVisible = not self.selectionGroupBox.isVisible()
        self.selectionGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.selectionLabel, event)


    def _mousePressEventInBevelOptionslabel(self, event):
        isVisible = not self.bevelOptionsGroupBox.isVisible()
        self.bevelOptionsGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelOptionsLabel, event)


    def _mousePressEventInBevelLabel(self, event):
        isVisible = not self.bevelGroupBox.isVisible()
        self.bevelGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelLabel, event)


    def _mousePressEventInBevelSetTreeView(self, event):
        self.selectionModelInBevelSetTreeView.clearSelection()
        QTreeView.mousePressEvent(self.bevelSetTreeView, event)


    def updateBevelSetTreeView(self):
        self.dataModelInBevelSetTreeView.clear()
        for col, header in enumerate(self.HEADERSINBEVELSETTREEVIEW):
            item = QStandardItem(header)
            item.setFont(self.headerFont)
            self.dataModelInBevelSetTreeView.setHorizontalHeaderItem(col, item)

        for bevelset in utils.MWBevelSets():
            item = QStandardItem(bevelset.name()+' '*10)
            item.setFont(self.itemFont)
            item.setEditable(False)
            self.dataModelInBevelSetTreeView.appendRow(item)
            row = self.dataModelInBevelSetTreeView.indexFromItem(item).row()
            index = self.dataModelInBevelSetTreeView.indexFromItem(item)

            item = QStandardItem(str(len(utils.bevelSetMembers(bevelset.name()))))
            item.setEditable(False)
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, 1, item)

            self.selectionModelInBevelSetTreeView.select(index, QItemSelectionModel.ToggleCurrent|QItemSelectionModel.Rows)

        map(lambda col:self.bevelSetTreeView.resizeColumnToContents(col), range(len(self.HEADERSINBEVELSETTREEVIEW)))


    def createNewBevelSet(self):
        newBevelSet = utils.createBevelSet()
        if newBevelSet is not None:
            self.bevelOnMWBevelSet(newBevelSet.name())
            self.updateBevelSetTreeView()
            self.statusbar.clearMessage()
        else:
            self.statusbar.showMessage(status.WARNING['New bevel set'])


    def bevelOnMWBevelSet(self, bevelSetName):
        members = utils.bevelSetMembers(bevelSetName)
        if len(members):
            bevelTool.bevelOnSelectedEdges(*(members, bevelSetName), **self.bevelOptions)
            utils.addMembersIntoBevelSet(bevelSetName, members)


    def _redoBevel(self, bevelSetName):
        utils.deletePolyBevelNodeInBevelSet(bevelSetName)
        self.bevelOnMWBevelSet(bevelSetName)


    def addEdgesIntoBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            if utils.addMembersIntoBevelSet(bevelSetName):
                self._redoBevel(bevelSetName)
                self.updateBevelSetTreeView()
            else:
                self.statusbar.showMessage(status.WARNING['Add member error'].format(bevelSetName))
        else:
            self.statusbar.showMessage(status.WARNING['Select bevelset'])


    def removeEdgesFromBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            utils.removeMembersFromBevelSet(bevelSetName)
            self._redoBevel(bevelSetName)
            self.updateBevelSetTreeView()
        else:
            self.statusbar.showMessage(status.WARNING['Select bevelset'])



def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
