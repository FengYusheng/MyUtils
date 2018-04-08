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
        self.remeberCheckBox.setVisible(False)
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
        self.remeberCheckBox.stateChanged.connect(self.force)


    def move(self):
        self.remeberCheckBox.isChecked() and self.parent.moveAction.setChecked(True)
        self.accept()


    def maintain(self):
        self.remeberCheckBox.isChecked() and self.parent.maintainAction.setChecked(True)
        self.reject()


    def force(self):
        if self.remeberCheckBox.isChecked():
            self.parent.forceAction.setChecked(True)
        else:
            self.parent.forceAction.setChecked(False)



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
                newValue = posDelta * valuePerPixel * valueStep + self.oldValue
                if newValue > 1.0:
                    newValue = 1.0
                elif newValue < 0.0:
                    newValue = 0.0

                bevelTool.setMWBevelOption(self.MWBevelSetName, 'Fraction', newValue)
                self.editor.setText(str(newValue))

            elif options.TREEVIEWHEADERS['Segments'] == self.col:
                valuePerPixel = 0.05
                newValue = int(posDelta * valuePerPixel + self.oldValue)
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
        self.highlightBrush = QBrush(Qt.GlobalColor.darkMagenta)

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.viewMenu.addAction(self.bevelToolbar.toggleViewAction())
        self.viewMenu.addAction(self.selectionToolbar.toggleViewAction())
        self.dataModelInBevelSetTreeView = QStandardItemModel(self.bevelSetTreeView)
        self.bevelSetTreeView.setModel(self.dataModelInBevelSetTreeView)
        self.selectionModelInBevelSetTreeView = QItemSelectionModel(self.dataModelInBevelSetTreeView, self.bevelSetTreeView)
        self.bevelSetTreeView.setSelectionModel(self.selectionModelInBevelSetTreeView)
        self.bevelSetTreeView.mousePressEvent = self._mousePressEventInBevelSetTreeView
        self.controlDelegate = ControlDelegate(self)
        self.bevelSetTreeView.setItemDelegate(self.controlDelegate)
        self.newAction.setIcon(QIcon(':/newLayerSelected.png'))
        self.addAction.setIcon(QIcon(':/trackAdd.png'))
        self.removeAction.setIcon(QIcon(':/trackRemove.png'))
        self.selectMemberAction.setIcon(QIcon(':/subdivMirror.png'))
        self.deleteAction.setIcon(QIcon(':/smallTrash.png'))
        self.displaySmoothnessPreviewAction.setIcon(QIcon(':/Smooth.png'))
        self.bevelToolbar.addAction(self.newAction)
        self.bevelToolbar.addAction(self.addAction)
        self.bevelToolbar.addAction(self.removeAction)
        self.bevelToolbar.addAction(self.selectMemberAction)
        self.bevelToolbar.addAction(self.deleteAction)
        self.bevelToolbar.addAction(self.displaySmoothnessPreviewAction)
        self.selectHardEdgeAction.setIcon(QIcon(':/polyHardEdge.png'))
        self.selectSoftEdgeAction.setIcon(QIcon(':/polySoftEdge.png'))
        self.selectionToolbar.addAction(self.selectHardEdgeAction)
        self.selectionToolbar.addAction(self.selectSoftEdgeAction)
        self.selectionToolbar.addWidget(self.smoothingAngleCheckBox)
        self.selectionToolbar.addWidget(self.smoothingAngleSpinBox)
        self.selectionToolbar.addWidget(self.smoothingAngleSlider)
        self.displayOverrideAction.setVisible(False)
        self.selectionConstraintDock.setVisible(False)
        self.forceAction.setVisible(False)

        self.displayOverrideAction.triggered.connect(self.displayOverrideAttributes)
        self.smoothingAngleCheckBox.stateChanged.connect(self.toggleSmoothingAngle)
        self.selectSoftEdgesButton.clicked.connect(self.selectSoftEdges)
        self.selectHardEdgesButton.clicked.connect(self.selectHardEdges)

        self.newAction.triggered.connect(self.createBevelSet)
        self.addAction.triggered.connect(self.addEdgesIntoBevelSet)
        self.removeAction.triggered.connect(self.removeEdgesFromBevelSet)
        self.selectMemberAction.triggered.connect(self.selectMembers)
        self.deleteAction.triggered.connect(self.deleteBevelSet)
        self.displaySmoothnessPreviewAction.triggered.connect(self.displaySmoothnessPreview)
        self.selectHardEdgeAction.triggered.connect(self.selectHardEdges)
        self.selectSoftEdgeAction.triggered.connect(self.selectSoftEdges)
        self.smoothingAngleSlider.valueChanged.connect(self.smoothingAngleFromSliderToSpinBox)
        self.smoothingAngleSpinBox.valueChanged.connect(self.smoothingAngleFromSpinBoxToSlider)

        self.updateBevelSetTreeView()


    def _mousePressEventInBevelSetTreeView(self, event):
        self.selectionModelInBevelSetTreeView.clearSelection()
        super(QTreeView, self.bevelSetTreeView).mousePressEvent(event)


    def _selectionChangedCallback(self, clientData=None):
        """
        The Mesh is in drawOverredeAttributes dict.       Selection Type is edge.                  Description.                            Operation
             False                                             True                  Select a new mesh, its seleciton type is edge.          Active.

             False                                             False                 Select a new mesh, but its selection type isn't         Restore.
                                                                                     edge.

             True                                              True                  The artist can bevel this mesh now.                     Bevel.

             True                                              False                 The artist switches the selection type of the            Restore.
                                                                                     mesh beveling directly. Handling this case in
                                                                                     _selectionTypeChangedCallback seems better
                                                                                     because active selection list isn't changed.

        TODO: add log
        """
        def _activeIntermdiate():
            # TODO: self.statusbar.showMessage("IN {0}. EDGE {1}".format(utils.isInDrawOverrideAttributesDict(), utils.isSelectionTypeEdge()))
            # print("IN: {0}".format(utils.isInDrawOverrideAttributesDict()))
            # print("EDGE: {0}".format(utils.isSelectionTypeEdge()))
            if (not utils.isInDrawOverrideAttributesDict()) and utils.isSelectionTypeEdge():
                utils.activeBevel()
                self.newAction.setEnabled(True)
                self.addAction.setEnabled(True)
                self.removeAction.setEnabled(True)
                self.displaySmoothnessPreviewAction.setEnabled(True)
                self.statusbar.showMessage('Edit "{0}"'.format(options.drawOverredeAttributes['mesh']))

            elif (not utils.isInDrawOverrideAttributesDict()) and (not utils.isSelectionTypeEdge()):
                utils.restoreDrawOverrideAttributes('Select a new mesh')
                self.newAction.setEnabled(False)
                self.addAction.setEnabled(False)
                self.removeAction.setEnabled(False)
                self.displaySmoothnessPreviewAction.setEnabled(False)
                self.statusbar.clearMessage()

            elif utils.isInDrawOverrideAttributesDict() and utils.isSelectionTypeEdge():
                self.statusbar.showMessage('Edit "{0}"'.format(options.drawOverredeAttributes['mesh']))

            elif utils.isInDrawOverrideAttributesDict() and (not utils.isSelectionTypeEdge()):
                utils.restoreDrawOverrideAttributes("Selection type isn't edge.")
                self.newAction.setEnabled(False)
                self.addAction.setEnabled(False)
                self.removeAction.setEnabled(False)
                self.displaySmoothnessPreviewAction.setEnabled(False)
                self.statusbar.clearMessage()

        len(options.disableIntermediate) == 0 and _activeIntermdiate()
        self.updateBevelSetTreeView()
        # print('selction changed')


    def _selectionTypeChangedCallback(self, clientData=None):
        def _runCallback():
            if options.drawOverredeAttributes['ioMesh'] != ' ' and (not utils.isSelectionTypeEdge()):
                #This restoration doesn't seem to appear in undo list.
                utils.restoreDrawOverrideAttributes('type')
                self.newAction.setEnabled(False)
                self.addAction.setEnabled(False)
                self.removeAction.setEnabled(False)
                self.displaySmoothnessPreviewAction.setEnabled(False)
            elif utils.isSelectionTypeEdge() and (not utils.isInDrawOverrideAttributesDict()):
                utils.activeBevel()
                self.newAction.setEnabled(True)
                self.addAction.setEnabled(True)
                self.removeAction.setEnabled(True)
                self.displaySmoothnessPreviewAction.setEnabled(False)

        options.drawOverredeAttributes['ioMesh'] == ' ' and utils.isSelectionTypeVertexFace()
        len(options.disableIntermediate) == 0 and _runCallback()
        # print('type changed')


    def _beforeSceneUpdateCallback(self, clientData=None):
        self.setEnabled(False)


    def _sceneUpdateCallback(self, clientDate=None):
        self.setEnabled(True)
        self.updateBevelSetTreeView()


    def _selectionPreferenceChangedCallback(self, clientData=None):
        if options.drawOverredeAttributes['ioMesh'] != ' ' and not(utils.isSelectionTypeEdge()):
            # This restoration doesn't seem to appear in undo list.
            utils.restoreDrawOverrideAttributes()
            self.newAction.setEnabled(False)
            self.addAction.setEnabled(False)
            self.removeAction.setEnabled(False)
            self.displaySmoothnessPreviewAction.setEnabled(False)


    def showEvent(self, event):
        cb = om.MEventMessage.addEventCallback('SelectPreferenceChanged', self._selectionPreferenceChangedCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MEventMessage.addEventCallback('SelectionChanged', self._selectionChangedCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MEventMessage.addEventCallback('SelectTypeChanged', self._selectionTypeChangedCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeNew, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeImport, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterImport, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeOpen, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeReference, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterReference, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeRemoveReference, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterRemoveReference, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeImportReference, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterImportReference, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeLoadReference, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterLoadReference, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeUnloadReference, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterUnloadReference, self._sceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        cb = om.MSceneMessage.addCallback(om.MSceneMessage.kMayaExiting, self._beforeSceneUpdateCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))

        utils.turnConstructionHistoryOn()
        super(MWBevelToolMainWindow, self).showEvent(event)


    def hideEvent(self, event):
        self.registeredMayaCallbacks = []
        utils.restoreDrawOverrideAttributes("Restore before exiting.")
        super(MWBevelToolMainWindow, self).hideEvent(event)


    def updateBevelSetTreeView(self):
        self.dataModelInBevelSetTreeView.clear()
        selectedMWBevelSets = utils.selectedMWBevelSets()[0]

        for header, col in options.TREEVIEWHEADERS.items():
            item = QStandardItem(header)
            item.setFont(self.headerFont)
            self.dataModelInBevelSetTreeView.setHorizontalHeaderItem(col, item)

        for MWBevelSetName in utils.MWBevelSets():
            item = QStandardItem(MWBevelSetName+' '*4)
            item.setFont(self.itemFont)
            item.setEditable(False)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.appendRow(item)
            row = self.dataModelInBevelSetTreeView.indexFromItem(item).row()

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Fraction')
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Fraction'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Segments')
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Segments'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Mitering')
            item = QStandardItem(options.MITERING[value])
            item.setFont(self.itemFont)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Mitering'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Miter Along')
            item = QStandardItem(options.MITERALONG[value])
            item.setFont(self.itemFont)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Miter Along'], item)

            value = bevelTool.MWBevelOption(MWBevelSetName, 'Chamfer')
            item = QStandardItem(options.CHAMFER[value])
            item.setFont(self.itemFont)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Chamfer'], item)

            value = len(utils.bevelSetMembers(MWBevelSetName))
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            item.setEditable(False)
            MWBevelSetName in selectedMWBevelSets and item.setBackground(self.highlightBrush)
            self.dataModelInBevelSetTreeView.setItem(row, options.TREEVIEWHEADERS['Members'], item)

        map(lambda col:self.bevelSetTreeView.resizeColumnToContents(col), range(len(options.TREEVIEWHEADERS)))


    def _run(self, func, *args):
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
            force = QDialog.Accepted if self.forceAction.isChecked() else MWChooseDialog(self, 'createBevelSet', MWBevelSetName[0]).exec_()
            success = force == QDialog.Accepted
            success and utils.force(MWBevelSetName[0])

        elif func.__name__ == 'addEdgesIntoBevelSet' and num > 0 and args[0] != MWBevelSetName[0]:
            self.statusbar.showMessage('{0} is already in {1}'.format(mesh, MWBevelSetName[0]))
            force = QDialog.Accepted if self.forceAction.isChecked() else MWChooseDialog(self, 'addEdgesIntoBevelSet', MWBevelSetName[0], args[0]).exec_()
            success = force == QDialog.Accepted
            success and utils.force(MWBevelSetName[0], args[0])

        else:
            utils.delConstructionHistory()
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


    def selectMembers(self):
        utils.selectMWBevelSetMembers()


    def deleteBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            MWBevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            utils.deleteBevelSet(MWBevelSetName)
            self.updateBevelSetTreeView()


    def selectHardEdges(self):
        angle = self.smoothingAngleSpinBox.value()
        self.smoothingAngleCheckBox.isChecked() and utils.setSmoothingAngle(angle)
        if utils.selectHardEdges() == 1:
            self.newAction.setEnabled(True)
            self.addAction.setEnabled(True)
            self.removeAction.setEnabled(True)
            self.displaySmoothnessPreviewAction.setEnabled(True)
            self.statusbar.showMessage('Edit {0}.'.format(options.drawOverredeAttributes['mesh']))
        else:
            self.statusbar.showMessage('Select an object per time.')


    def selectSoftEdges(self):
        angle = self.smoothingAngleSpinBox.value()
        self.smoothingAngleCheckBox.isChecked() and utils.setSmoothingAngle(angle)
        if utils.selectSoftEdges() == 1:
            self.newAction.setEnabled(True)
            self.addAction.setEnabled(True)
            self.removeAction.setEnabled(True)
            self.displaySmoothnessPreviewAction.setEnabled(True)
            self.statusbar.showMessage('Edit {0}'.format(options.drawOverredeAttributes['mesh']))
        else:
            self.statusbar.showMessage('Select an object per time.')


    def toggleSmoothingAngle(self, state):
        if Qt.Checked == state:
            self.smoothingAngleSlider.setEnabled(True)
            self.smoothingAngleSpinBox.setEnabled(True)
        else:
            self.smoothingAngleSlider.setEnabled(False)
            self.smoothingAngleSpinBox.setEnabled(False)


    def smoothingAngleFromSliderToSpinBox(self, value):
        v = round((value/10000.0), 4)
        self.smoothingAngleSpinBox.value() == v or self.smoothingAngleSpinBox.setValue(v)



    def smoothingAngleFromSpinBoxToSlider(self, value):
        v = value * 10000
        self.smoothingAngleSlider.value() == v or self.smoothingAngleSlider.setValue(v)


    def displaySmoothnessPreview(self):
        options.displaySmoothnessPreview = True if self.displaySmoothnessPreviewAction.isChecked() else False
        utils.displayOriginInSmoothnessPreview()


    def displayOverrideAttributes(self):
        print(options.drawOverredeAttributes)
        print(options.isVertexFace)
        print(options.disableIntermediate)



def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
