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



class ControlDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ControlDelegate, self).__init__(parent)
        self.parent = parent
        self.col = 0
        self.row = 0
        self.model = None
        self.editor = None
        self.isLeftButton = False
        self.initialPos = None
        self.oldValue = None
        self.MWBevelSetName = None


    def _mousePressEventInDelegate(self, event):
        self.initialPos = (event.x(), event.y())
        self.isLeftButton = True if event.button() & Qt.LeftButton else False
        super(type(self.editor), self.editor).mousePressEvent(event)


    def _mouseMoveEventInDelegate(self, event):
        if self.isLeftButton:
            posDelta = event.x() - self.initialPos[0]

            if options.TREEVIEWHEADERS['Fraction'] == self.col:
                valuePerPixel = 0.001
                valueStep = 2
                newValue = posDelta * valuePerPixel * valueStep + self.editorValue
                if newValue > 1.0:
                    newValue = 1.0
                elif newValue < 0.0:
                    newValue = 0.0

                bevelTool.setMWBevelOption(self.MWBevelSetName, 'Fraction', newValue)
                self.editor.setText(str(newValue))

            elif options.TREEVIEWHEADERS['Segments'] == self.col:
                valuePerPixel = 0.05
                newValue = int(posDelta * valuePerPixel + self.editorValue)
                if newValue > 12:
                    newValue = 12
                elif newValue < 1:
                    newValue = 1

                bevelTool.setMWBevelOption(self.MWBevelSetName, 'Segments', newValue)
                self.editor.setText(str(newValue))

        super(type(self.editor), self.editor).mouseMoveEvent(event)


    def _mouseReleaseEventInDelegate(self, event):
        self.isLeftButton = False
        super(type(self.editor), self.editor).mouseReleaseEvent(event)


    def _setMitering(self):
        value = self.editor.currentIndex()
        bevelTool.setMWBevelOption(self.MWBevelSetName, 'Mitering', value)
        self.model.item(self.row, options.TREEVIEWHEADERS['Miter Along']).setEditable(True)

        # Mitering is "None".
        value == 4 and self.model.item(self.row, options.TREEVIEWHEADERS['Miter Along']).setEditable(False)


    def _setMiterAlong(self):
        value = self.editor.currentIndex()
        bevelTool.setMWBevelOption(self.MWBevelSetName, 'Miter Along', value)


    def _setChamfer(self):
        value = self.editor.currentIndex()
        bevelTool.setMWBevelOption(self.MWBevelSetName, 'Chamfer', value)


    def createEditor(self, parent, option, index):
        col = index.column()
        row = index.row()
        editor = None

        if options.TREEVIEWHEADERS['Fraction'] == col \
            or options.TREEVIEWHEADERS['Segments'] == col:

            editor = QLineEdit(parent)
            editor.mousePressEvent = self._mousePressEventInDelegate
            editor.mouseMoveEvent = self._mouseMoveEventInDelegate
            editor.mouseReleaseEvent = self._mouseReleaseEventInDelegate

        elif options.TREEVIEWHEADERS['Mitering'] == col:
            editor = QComboBox(parent)
            editor.addItems(options.MITERING)
            editor.currentIndexChanged.connect(self._setMitering)

        elif options.TREEVIEWHEADERS['Miter Along'] == col:
            editor = QComboBox(parent)
            editor.addItems(options.MITERALONG)
            editor.currentIndexChanged.connect(self._setMiterAlong)

        elif options.TREEVIEWHEADERS['Chamfer'] == col:
            editor = QComboBox(parent)
            editor.addItems(options.CHAMFER)
            editor.currentIndexChanged.connect(self._setChamfer)

        self.MWBevelSetName = index.model().item(row, 0).text().strip()
        self.editor = editor
        self.col = col
        self.row = row
        self.model = index.model()
        return editor


    def setEditorData(self, editor, index):
        col = index.column()
        if options.TREEVIEWHEADERS['Fraction'] == col:
            data = index.model().data(index, Qt.EditRole)
            self.oldValue = round(float(data), 3)
            editor.setText(data)

        elif options.TREEVIEWHEADERS['Segments'] == col:
            data = index.model().data(index, Qt.EditRole)
            self.oldValue = int(data)
            editor.setText(data)

        elif options.TREEVIEWHEADERS['Mitering'] == col:
            mitering = bevelTool.MWBevelOption(self.MWBevelSetName, 'Mitering')
            editor.setCurrentIndex(mitering)

        elif options.TREEVIEWHEADERS['Miter Along'] == col:
            miterAlong = bevelTool.MWBevelOption(self.MWBevelSetName, 'Miter Along')
            editor.setCurrentIndex(miterAlong)

        elif options.TREEVIEWHEADERS['Chamfer'] == col:
            chamfer = bevelTool.MWBevelOption(self.MWBevelSetName, 'Chamfer')
            editor.setCurrentIndex(chamfer)


    def setModelData(self, editor, model, index):
        col = index.column()
        if options.TREEVIEWHEADERS['Fraction'] == col:
            try:
                value = round(float(editor.text()), 3)
            except ValueError as e:
                value = self.oldValue

            if value > 1.0:
                value = 1.0
            elif value < 0.0:
                value = 0.0

            bevelTool.setMWBevelOption(self.MWBevelSetName, 'Fraction', value)

        elif options.TREEVIEWHEADERS['Segments'] == col:
            try:
                value = int(editor.text())
            except ValueError as e:
                value = self.oldValue

            if value > 12:
                value = 12
            elif value < 1:
                value = 1

            bevelTool.setMWBevelOption(self.MWBevelSetName, 'Segments', value)

        elif options.TREEVIEWHEADERS['Mitering'] == col:
            value = editor.currentIndex()
            bevelTool.setMWBevelOption(self.MWBevelSetName, 'Mitering', value)
            value = options.MITERING[value]

        elif options.TREEVIEWHEADERS['Miter Along'] == col:
            value = editor.currentIndex()
            bevelTool.setMWBevelOption(self.MWBevelSetName, 'Miter Along', value)
            value = options.MITERALONG[value]

        elif options.TREEVIEWHEADERS['Chamfer'] == col:
            value = editor.currentIndex()
            bevelTool.setMWBevelOption(self.MWBevelSetName, 'Chamfer', value)
            value = options.CHAMFER[value]

        model.setData(index, str(value), Qt.EditRole)


    def updateEditorGeometry(self, editor, option, index):
        option.rect.setHeight(option.rect.height()*1.4)
        editor.setGeometry(option.rect)



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
        self.controlDelegate = ControlDelegate(self)
        self.bevelSetTreeView.setItemDelegate(self.controlDelegate)
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


    def _activeSelectionListchangedCallback(self, clientData=None):
        """
        The Mesh is in drawOverredeAttributes dict.       Selection Type is edge.                  Description.                            Operation
             False                                             True                  Select a new mesh, its seleciton type is edge.          Active.

             False                                             False                 Select a new mesh, but its selection type isn't         Restore.
                                                                                     edge.

             True                                              True                  The artist can bevel this mesh now.                     Bevel.

             True                                              False                 The artis switches the selection type of the            Restore.
                                                                                     mesh beveling directly.
        """
        def _runCallback():
            if (not utils.isInDrawOverrideAttributesDict()) and utils.isSelectionTypeEdge():
                utils.activeBevel()
                self.createBevelSetButton.setEnabled(True)
                self.addButton.setEnabled(True)
                self.removeButton.setEnabled(True)
                self.statusbar.showMessage('Edit "{0}"'.format(options.drawOverredeAttributes['mesh']))

            elif (not utils.isInDrawOverrideAttributesDict()) and (not utils.isSelectionTypeEdge()):
                utils.restoreDrawOverrideAttributes('Select a new mesh')
                self.createBevelSetButton.setEnabled(False)
                self.addButton.setEnabled(False)
                self.removeButton.setEnabled(False)
                self.statusbar.clearMessage()

            elif utils.isInDrawOverrideAttributesDict() and utils.isSelectionTypeEdge():
                self.statusbar.showMessage('Edit "{0}"'.format(options.drawOverredeAttributes['mesh']))

            elif utils.isInDrawOverrideAttributesDict() and (not utils.isSelectionTypeEdge()):
                utils.restoreDrawOverrideAttributes("Selection type isn't edge.")
                self.createBevelSetButton.setEnabled(False)
                self.addButton.setEnabled(False)
                self.removeButton.setEnabled(False)
                self.statusbar.clearMessage()

        options.runActiveSelecitonListCallback and _runCallback()


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
            success = False

        elif not utils.isInDrawOverrideAttributesDict():
            success = False

        elif not utils.isSelectionTypeEdge():
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
            self.statusbar.clearMessage()

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
