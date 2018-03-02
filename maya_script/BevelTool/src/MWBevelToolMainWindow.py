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
import ui_MWBevelToolMainWindow
reload(options)
reload(utils)
reload(ui_MWBevelToolMainWindow)



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class MWBevelToolMainWindow(QMainWindow, ui_MWBevelToolMainWindow.Ui_MWBevelToolMainWindow):
    def __init__(self, parent=None):
        super(MWBevelToolMainWindow, self).__init__(parent)
        self.registeredMayaCallbacks = []

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.bevelSetLabel.mousePressEvent = self._mousePressEventInBevelSetLable
        self.viewMenu.addAction(self.controlPanelDock.toggleViewAction())
        self.dataModelInBevelSetTreeView = QStandardItemModel(self.bevelSetTreeView)
        self.bevelSetTreeView.setModel(self.dataModelInBevelSetTreeView)
        self.selectionModelInBevelSetTreeView = QItemSelectionModel(self.dataModelInBevelSetTreeView, self.bevelSetTreeView)
        self.bevelSetTreeView.setSelectionModel(self.selectionModelInBevelSetTreeView)
        self.completeButton.setEnabled(False)
        self.createBevelSetButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

        self.startButton.clicked.connect(self.startBevel)
        self.completeButton.clicked.connect(self.completeBevel)
        self.createBevelSetButton.clicked.connect(self.createBevelSet)
        self.addButton.clicked.connect(self.addEdgesIntoBevelSet)


    def _mousePressEventInBevelSetLable(self, event):
        isVisible = not self.bevelSetGroupBox.isVisible()
        self.bevelSetGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelSetLabel, event)


    def _restore(self):
        utils.restoreDrawOverrideAttributes()
        options.drawOverredeAttributes.clear()
        self.startButton.setEnabled(True)
        self.completeButton.setEnabled(False)
        self.createBevelSetButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.statusbar.clearMessage()


    def _activeSelectionListchangedCallback(self, clientData=None):
        not utils.isActiveSelectionListChanged() or self._restore()


    def showEvent(self, event):
        cb = om.MModelMessage.addCallback(om.MModelMessage.kActiveListModified, self._activeSelectionListchangedCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))
        super(MWBevelToolMainWindow, self).showEvent(event)


    def hideEvent(self, event):
        self.registeredMayaCallbacks = []
        utils.restoreDrawOverrideAttributes()
        super(MWBevelToolMainWindow, self).hideEvent(event)


    def startBevel(self):
        if utils.activeBevel():
            self.startButton.setEnabled(False)
            self.completeButton.setEnabled(True)
            self.createBevelSetButton.setEnabled(True)
            self.addButton.setEnabled(True)
            self.removeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            self.statusbar.showMessage('Start to Bevel "{0}"'.format(options.drawOverredeAttributes['mesh']))


    def completeBevel(self):
        self.startButton.setEnabled(True)
        self.completeButton.setEnabled(False)
        self.createBevelSetButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.deleteButton.setEnabled(False)


    def createBevelSet(self):
        if not utils.isSelectionModechanged():
            num, bevelSets = utils.numBevelSet()
            if 0 == num:
                utils.createBevelSet()
            else:
                self.statusbar.showMessage('"{0}" is already in bevel set "{1}"'.format(options.drawOverredeAttributes['mesh'], bevelSets))
        else:
            self._restore()
            self.statusbar.showMessage(
                'MW Bevel Tool only works in edge seletion mode, click "Start" button to edit the selected object.'
                )


    def addEdgesIntoBevelSet(self):
        if not utils.isSelectionModechanged():
            num, bevelSets = utils.numBevelSet()
            if 0 == num:
                print('add')
            else:
                self.statusbar.showMessage('"{0}" is already in bevel set "{1}"'.format(options.drawOverredeAttributes['mesh'], bevelSets))
        else:
            self._restore()
            self.statusbar.showMessage(
                'MW Bevel Tool only works in edge seletion mode, click "Start" button to edit the selected object.'
                )



def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
