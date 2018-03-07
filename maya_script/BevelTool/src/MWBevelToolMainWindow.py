# -*- coding: utf-8 -*-
# This version bevels the selected mesh object with the assistance of its intermediate objects.
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

import maya.OpenMayaUI as apiUI # Python api 1.0
import maya.api.OpenMaya as om # Python api 2.0

import options
import utils
import bevelTool
import ui_MWBevelToolMainWindow
reload(options)
reload(utils)
reload(bevelTool)
reload(ui_MWBevelToolMainWindow)



def getMayaWindow():
    # TODO: pm.lsUI(windows=True)
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class MWBevelToolMainWindow(QMainWindow, ui_MWBevelToolMainWindow.Ui_MWBevelToolMainWindow):
    def __init__(self, parent=None):
        super(MWBevelToolMainWindow, self).__init__(parent)
        self.registeredMayaCallbacks = []
        self.headerFont = QFont('OldEnglish', 10, QFont.Bold)
        self.itemFont = QFont('OldEnglish', 10)

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.bevelSetLabel.mousePressEvent = self._mousePressEventInBevelSetLable
        self.viewMenu.addAction(self.controlPanelDock.toggleViewAction())
        self.dataModelInBevelSetTreeView = QStandardItemModel(self.bevelSetTreeView)
        self.bevelSetTreeView.setModel(self.dataModelInBevelSetTreeView)
        self.selectionModelInBevelSetTreeView = QItemSelectionModel(self.dataModelInBevelSetTreeView, self.bevelSetTreeView)
        self.bevelSetTreeView.setSelectionModel(self.selectionModelInBevelSetTreeView)
        self.bevelSetTreeView.mousePressEvent = self._mousePressEventInBevelSetTreeView
        self.bevelSetTreeView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bevelSetTreeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.createBevelSetButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)

        self.startButton.clicked.connect(self.startBevel)
        self.createBevelSetButton.clicked.connect(self.createBevelSet)
        self.addButton.clicked.connect(self.addEdgesIntoBevelSet)
        self.removeButton.clicked.connect(self.removeEdgesFromBevelSet)
        self.deleteButton.clicked.connect(self.deleteBevelSet)
        self.displayDrawOverrideAttrAction.triggered.connect(self.displayDrawOverrideAttr)

        self.updateBevelSetTreeView()


    def _mousePressEventInBevelSetLable(self, event):
        isVisible = not self.bevelSetGroupBox.isVisible()
        self.bevelSetGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelSetLabel, event)


    def _mousePressEventInBevelSetTreeView(self, event):
        self.selectionModelInBevelSetTreeView.clearSelection()
        super(QTreeView, self.bevelSetTreeView).mousePressEvent(event)


    def _restore(self, operation):
        utils.restoreDrawOverrideAttributes(operation)
        self.startButton.setEnabled(True)
        self.createBevelSetButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.statusbar.clearMessage()


    def _activeSelectionListchangedCallback(self, clientData=None):
        utils.isActiveSelectionListChanged() and self._restore('Restore because active selection list is changed.')


    def showEvent(self, event):
        cb = om.MModelMessage.addCallback(om.MModelMessage.kActiveListModified, self._activeSelectionListchangedCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))
        super(MWBevelToolMainWindow, self).showEvent(event)


    def hideEvent(self, event):
        self.registeredMayaCallbacks = []
        utils.restoreDrawOverrideAttributes("Restore before exiting.")
        super(MWBevelToolMainWindow, self).hideEvent(event)


    def updateBevelSetTreeView(self):
        self.dataModelInBevelSetTreeView.clear()
        for header, col in options.TREEVIEWHEADERS.items():
            item = QStandardItem(header)
            item.setFont(self.headerFont)
            self.dataModelInBevelSetTreeView.setHorizontalHeaderItem(col, item)

        for MWBevelSetName in utils.MWBevelSets():
            item = QStandardItem(MWBevelSetName+' '*4)
            item.setFont(self.itemFont)
            item.setEditable(False)
            self.dataModelInBevelSetTreeView.appendRow(item)
            row = self.dataModelInBevelSetTreeView.indexFromItem(item).row()

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Fraction')
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Fraction'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Segments')
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Segments'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Mitering')
            item = QStandardItem(options.MITERING[value])
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Mitering'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Miter Along')
            item = QStandardItem(options.MITERALONG[value])
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Miter Along'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Chamfer')
            item = QStandardItem(options.CHAMFER[value])
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Chamfer'], item)

        map(lambda col:self.bevelSetTreeView.resizeColumnToContents(col), range(len(options.TREEVIEWHEADERS)))


    def _validateConditionForFunc(self, func):
        '''
        1. Active selection list is changed.
        2. Selection mode is changed.
        3. The mesh has been in another bevel set.
        '''
        utils.isActiveSelectionListChanged()
        utils.isSelectionModechanged()
        utils.numBevelSet()


    def startBevel(self):
        if utils.activeBevel():
            self.startButton.setEnabled(False)
            self.createBevelSetButton.setEnabled(True)
            self.addButton.setEnabled(True)
            self.removeButton.setEnabled(True)
            self.statusbar.showMessage('Start to Bevel "{0}"'.format(options.drawOverredeAttributes['mesh']))


    def createBevelSet(self):
        if not utils.isSelectionModechanged():
            num, bevelSets = utils.numBevelSet()
            if 0 == num:
                utils.createBevelSet()
                self.updateBevelSetTreeView()
            else:
                self.statusbar.showMessage('"{0}" is already in bevel set "{1}"'.format(options.drawOverredeAttributes['mesh'], bevelSets))
        else:
            self._restore('Restore because selection mode is changed.')
            self.statusbar.showMessage(
                'MW Bevel Tool only works in edge seletion mode, click "Start" button to edit the selected object.'
                )


    def addEdgesIntoBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            MWBevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()

            # TODO: if self._checkActiveSelectionList(utils.addEdgesIntoBevelSet)
            if not utils.isSelectionModechanged():
                utils.addEdgesIntoBevelSet(MWBevelSetName)
                self.updateBevelSetTreeView()
            else:
                self._restore('Restore because selection mode is changed.')
                self.statusbar.showMessage(
                    'MW Bevel Tool only works in edge seletion mode, click "Start" button to edit the selected object.'
                    )


    def removeEdgesFromBevelSet(self):
        utils.removeEdgesFromBevelSet()


    def deleteBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            MWBevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            utils.deleteBevelSet(MWBevelSetName)
            self.updateBevelSetTreeView()


    def displayDrawOverrideAttr(self):
        print(options.drawOverredeAttributes)



def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
