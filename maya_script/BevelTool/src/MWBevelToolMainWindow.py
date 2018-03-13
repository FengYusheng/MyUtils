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
import ui_MWChooseDialog
reload(options)
reload(utils)
reload(bevelTool)
reload(ui_MWBevelToolMainWindow)
reload(ui_MWChooseDialog)



def getMayaWindow():
    # TODO: pm.lsUI(windows=True)
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class MWChooseDialog(QDialog, ui_MWChooseDialog.Ui_MWChooseDialog):
    def __init__(self, parent, *args):
        super(MWChooseDialog, self).__init__(parent)
        self.parent = parent
        self.args = args
        self.mesh = options.drawOverredeAttributes['mesh']

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.args[0] == 'createBevelSet' and self.textEdit.setHtml(
            "<b>{0} is already in {1}. Do you want to move it into a new bevel set?<b/>"\
            .format(self.mesh, self.args[1])
        )

        self.args[0] == 'addEdgesIntoBevelSet' and self.textEdit.setHtml(
            "<b>{0} is already in {1}, Do you want to move it into {2}?</b>"\
            .format(self.mesh, self.args[1], self.args[2])
        )

        self.yesButton.clicked.connect(self.move)
        self.noButton.clicked.connect(self.maintain)
        self.remeberCheckBox.stateChanged.connect(lambda : self.remeberCheckBox.isChecked() or self.parent.chooseAction.setChecked(True))


    def move(self):
        self.remeberCheckBox.isChecked() and self.parent.moveAction.setChecked(True)
        self.accept()


    def maintain(self):
        self.remeberCheckBox.isChecked() and self.parent.maintainAction.setChecked(True)
        self.reject()



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
        self.bevelSetActionGroup = QActionGroup(self)
        self.bevelSetActionGroup.addAction(self.moveAction)
        self.bevelSetActionGroup.addAction(self.maintainAction)
        self.bevelSetActionGroup.addAction(self.chooseAction)

        self.createBevelSetButton.clicked.connect(self.createBevelSet)
        self.addButton.clicked.connect(self.addEdgesIntoBevelSet)
        self.removeButton.clicked.connect(self.removeEdgesFromBevelSet)
        self.deleteButton.clicked.connect(self.deleteBevelSet)
        self.displayOverrideAction.triggered.connect(self.displayOverrideAttributes)

        self.updateBevelSetTreeView()
        # TODO: Validate the Maya scene: 1. turn construction history on


    def _mousePressEventInBevelSetLable(self, event):
        isVisible = not self.bevelSetGroupBox.isVisible()
        self.bevelSetGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelSetLabel, event)


    def _mousePressEventInBevelSetTreeView(self, event):
        self.selectionModelInBevelSetTreeView.clearSelection()
        super(QTreeView, self.bevelSetTreeView).mousePressEvent(event)


    def _restore(self, operation=None):
        utils.restoreDrawOverrideAttributes(operation)
        self.createBevelSetButton.setEnabled(False)
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        # self.statusbar.clearMessage()


    def _activeSelectionListchangedCallback(self, clientData=None):
        '''
        In drawOverredeAttributes Dict   Selection Type is Edge                  Description                                         Operation
               False                            True                      Select a new mesh and its selection type is edge.           Active.
               False                            False                     Select a new mesh but its selection type isn't edge.        Restore.
               True                             True                             -                                                Prepare to bevel mesh.
               True                             False                     Switch the selection type of the mesh beveling.         Just disable buttons.
        '''
        if (not utils.isIndrawOverredeAttributes()) and utils.isSelectionTypeEdge():
            utils.activeBevel()
            self.createBevelSetButton.setEnabled(True)
            self.addButton.setEnabled(True)
            self.removeButton.setEnabled(True)
            self.statusbar.showMessage('Prepare to bevel {0}'.format(options.drawOverredeAttributes['mesh']))
        elif (not utils.isIndrawOverredeAttributes()) and (not utils.isSelectionTypeEdge()):
            self.statusbar.showMessage('Restore {0} when you select another object'.format(options.drawOverredeAttributes['mesh']))
            self._restore('Restore {0} when you select another object'.format(options.drawOverredeAttributes['mesh']))
        elif utils.isIndrawOverredeAttributes() and utils.isSelectionTypeEdge():
            self.statusbar.showMessage('Prepare to bevel {0}'.format(options.drawOverredeAttributes['mesh']))
        elif utils.isIndrawOverredeAttributes() and (not utils.isSelectionTypeEdge()):
            self.statusbar.showMessage("{0} isn't in edge selection type.".format(options.drawOverredeAttributes['mesh']))
            options.drawOverredeAttributes['restore'] == True and self._restore("Restore {0} when it isn't in edge selection type.")



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


    def _run(self, func, *args):
        '''
        1. drawOverredeAttributes is empty.
        2. Active selection list is changed.
        3. Selection mode is changed.
        4. The mesh has been in another bevel set.
        '''
        success = True
        force = QDialog.Rejected
        mesh = options.drawOverredeAttributes['mesh']
        num, MWBevelSetName = utils.numBevelSet()
        if options.drawOverredeAttributes['mesh'] == ' ':
            self._restore()
            success = False
        elif not utils.isSelectionTypeEdge():
            self.statusbar.showMessage('Selection mode is changed.')
            self._restore('Selecton mode is changed.')
            success = False
        elif func.__name__ == 'createBevelSet' and num > 0:
            self.statusbar.showMessage('{0} is already in {1}'.format(mesh, MWBevelSetName[0]))
            if self.moveAction.isChecked():
                force = QDialog.Accepted
            elif self.maintainAction.isChecked():
                force = QDialog.Rejected
            else:
                force = MWChooseDialog(self, 'createBevelSet', MWBevelSetName[0]).exec_()

            success = force == QDialog.Accepted
            success and utils.force(MWBevelSetName[0])
        elif func.__name__ == 'addEdgesIntoBevelSet' and num > 0 and args[0] != MWBevelSetName[0]:
            self.statusbar.showMessage('{0} is already in {1}'.format(mesh, MWBevelSetName[0]))
            if self.moveAction.isChecked():
                force = QDialog.Accepted
            elif self.maintainAction.isChecked():
                force = QDialog.Rejected
            else:
                force = MWChooseDialog(self, 'addEdgesIntoBevelSet', MWBevelSetName[0], args[0]).exec_()

            success = force == QDialog.Accepted
            success and utils.force(MWBevelSetName[0], args[0])
        else:
            func(*args)

        return success


    def createBevelSet(self):
        self._run(utils.createBevelSet) and self.updateBevelSetTreeView()


    def addEdgesIntoBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            MWBevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            self._run(utils.addEdgesIntoBevelSet, MWBevelSetName) and self.updateBevelSetTreeView()


    def removeEdgesFromBevelSet(self):
        self._run(utils.removeEdgesFromBevelSet) and self.updateBevelSetTreeView()


    def deleteBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            MWBevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            utils.deleteBevelSet(MWBevelSetName)
            self.updateBevelSetTreeView()


    def displayOverrideAttributes(self):
        print(options.drawOverredeAttributes)



def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
