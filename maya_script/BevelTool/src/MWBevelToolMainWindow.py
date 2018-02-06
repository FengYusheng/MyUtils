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

import maya.OpenMayaUI as apiUI # Python api 1.0
import maya.api.OpenMaya as om # Python api 2.0

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



class ControlDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ControlDelegate, self).__init__(parent)
        self.parent = parent
        self.col = 0
        self.row = 0
        self.model = None
        self.editor = None
        self.bevelSetName = None
        self.isLeftButtonPressed = False
        self.initialPos = None
        self.editorValue = None


    def _mousePressEventInDelegate(self, event):
        self.initialPos = (event.x(), event.y())
        self.isLeftButtonPressed = True if event.button() & Qt.LeftButton else False
        super(type(self.editor), self.editor).mousePressEvent(event)


    def _mouseMoveEventInDelegate(self, event):
        if self.isLeftButtonPressed:
            posDelta = event.x() - self.initialPos[0]
            if 1 == self.col:
                maxValue = 1.0
                minValue = 0.0
                valuePerPixel = 0.001
                valueStep = 2
                newValue = posDelta * valuePerPixel * valueStep + self.editorValue
                if newValue > maxValue:
                    newValue = maxValue
                elif newValue < minValue:
                    newValue = minValue

                bevelTool.setMWBevelOption(self.bevelSetName, 'Fraction', newValue)
                self.editor.setText(str(newValue))
            elif 2 == self.col:
                maxValue = 12
                minValue = 1
                valuePerPixel = 0.05
                newValue = int(posDelta * valuePerPixel + self.editorValue)
                if newValue > maxValue:
                    newValue = maxValue
                elif newValue < minValue:
                    newValue = minValue

                bevelTool.setMWBevelOption(self.bevelSetName, 'Segments', newValue)
                self.editor.setText(str(newValue))

        super(type(self.editor), self.editor).mouseMoveEvent(event)


    def _mouseReleaseEventInDelegate(self, event):
        self.isLeftButtonPressed = False
        super(type(self.editor), self.editor).mouseReleaseEvent(event)


    def _setMitering(self):
        value = self.editor.currentIndex()
        bevelTool.setMWBevelOption(self.bevelSetName, 'Mitering', value)
        self.model.item(self.row, 4).setEditable(True)
        value != 4 or self.model.item(self.row, 4).setEditable(False)


    def _setMiterAlong(self):
        value = self.editor.currentIndex()
        bevelTool.setMWBevelOption(self.bevelSetName, 'Miter Along', value)


    def _setChamfer(self):
        value = self.editor.currentIndex()
        bevelTool.setMWBevelOption(self.bevelSetName, 'Chamfer', value)


    def createEditor(self, parent, opiton, index):
        col = index.column()
        row = index.row()
        editor = None
        if 1 == col or 2 == col:
            editor = QLineEdit(parent)
            editor.mousePressEvent = self._mousePressEventInDelegate
            editor.mouseMoveEvent = self._mouseMoveEventInDelegate
            editor.mouseReleaseEvent = self._mouseReleaseEventInDelegate
        elif 3 == col:
            editor = QComboBox(parent)
            editor.addItems(options.MITERING)
            editor.currentIndexChanged.connect(self._setMitering)
        elif 4 == col:
            editor = QComboBox(parent)
            editor.addItems(options.MITERALONG)
            editor.currentIndexChanged.connect(self._setMiterAlong)
        elif 5 == col:
            editor = QComboBox(parent)
            editor.addItems(options.CHAMFER)
            editor.currentIndexChanged.connect(self._setChamfer)

        self.bevelSetName = index.model().item(row, 0).text().strip()
        self.editor = editor
        self.col = col
        self.row = row
        self.model = index.model()
        return editor


    def setEditorData(self, editor, index):
        col = index.column()
        if 1 == col:
            data = index.model().data(index, Qt.EditRole)
            self.editorValue = round(float(data),3)
            editor.setText(data)
        elif 2 == col:
            data = index.model().data(index, Qt.EditRole)
            self.editorValue = int(data)
            editor.setText(data)
        elif 3 == col:
            mitering = bevelTool.MWBevelOption(self.bevelSetName, 'Mitering')
            editor.setCurrentIndex(mitering)
        elif 4 == col:
            miterAlong = bevelTool.MWBevelOption(self.bevelSetName, 'Miter Along')
            editor.setCurrentIndex(miterAlong)
        elif 5 == col:
            chamfer = bevelTool.MWBevelOption(self.bevelSetName, 'Chamfer')
            editor.setCurrentIndex(chamfer)


    def setModelData(self, editor, model, index):
        col = index.column()
        if 1 == col:
            try:
                value = round(float(editor.text()), 3)
            except ValueError as e:
                value = self.editorValue

            if value > 1.0:
                value = 1.0
            elif value < 0.0:
                value = 0.0

            bevelTool.setMWBevelOption(self.bevelSetName, 'Fraction', value)
        elif 2 == col:
            try:
                value = int(editor.text())
            except ValueError as e:
                value = self.editorValue

            if value > 12:
                value = 12
            elif value < 1:
                value = 1

            bevelTool.setMWBevelOption(self.bevelSetName, 'Segments', value)
        elif 3 == col:
            value = editor.currentIndex()
            bevelTool.setMWBevelOption(self.bevelSetName, 'Mitering', value)
            value = options.MITERING[value]
        elif 4 == col:
            value = editor.currentIndex()
            bevelTool.setMWBevelOption(self.bevelSetName, 'Miter Along', value)
            value = options.MITERALONG[value]
        elif 5 == col:
            value = editor.currentIndex()
            bevelTool.setMWBevelOption(self.bevelSetName, 'Chamfer', value)
            value = options.CHAMFER[value]

        model.setData(index, str(value), Qt.EditRole)


    def updateEditorGeometry(self, editor, option, index):
        option.rect.setHeight(option.rect.height()*1.4)
        editor.setGeometry(option.rect)



class MWBevelToolMainWindow(QMainWindow, ui_MWBevelToolMainWindow.Ui_MWBevelToolMainWindow):
    HEADERSINBEVELSETTREEVIEW = ('Bevel Set', 'Fraction', 'Segments', 'Mitering', 'Miter Along', 'Chamfer')
    def __init__(self, parent=None):
        super(MWBevelToolMainWindow, self).__init__(parent)

        self.headerFont = QFont('OldEnglish', 10, QFont.Bold)
        self.itemFont = QFont('OldEnglish', 10)
        self.itemEditedBrush = QBrush(Qt.GlobalColor.blue)
        self.bevelSetMinorBrush = QBrush(Qt.GlobalColor.darkGray)
        self.bevelOptions = copy.copy(options.bevelOptions)
        self.isMouseLeftButtonClicked = False
        self.registeredMayaCallbacks = []
        self.polyBevel3Info = []

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.bevelSetLabel.mousePressEvent = self._mousePressEventInBevelSetLabel
        self.bevelLabel.mousePressEvent = self._mousePressEventInBevelLabel
        self.selectionLabel.mousePressEvent = self._mousePressEventInSelectionLabel
        self.bevelSetTreeView.mousePressEvent = self._mousePressEventInBevelSetTreeView
        self.bevelSetTreeView.showEvent = self._showEventInBevelSetTreeView
        self.bevelSetTreeView.hideEvent = self._hideEventInBevelSetTreeView
        self.dataModelInBevelSetTreeView = QStandardItemModel(self.bevelSetTreeView)
        self.bevelSetTreeView.setModel(self.dataModelInBevelSetTreeView)
        self.selectionModelInBevelSetTreeView = QItemSelectionModel(self.dataModelInBevelSetTreeView, self.bevelSetTreeView)
        self.bevelSetTreeView.setSelectionModel(self.selectionModelInBevelSetTreeView)
        self.controlDelegate = ControlDelegate(self)
        self.bevelSetTreeView.setItemDelegate(self.controlDelegate)
        self.viewMenu.addAction(self.controlDock.toggleViewAction())
        self.toolbarGroupBox.setVisible(False)

        self.updateBevelSetTreeView()

        self.newBevelSetButton.clicked.connect(self.createNewBevelSet)
        self.addMemberButton.clicked.connect(self.addEdgesIntoBevelSet)
        self.removeMemberButton.clicked.connect(self.removeEdgesFromBevelSet)
        self.deleteBevelSetbutton.clicked.connect(self.deleteBevelSet)
        self.selectMembersButton.clicked.connect(self.selectEdgesInBevelSet)
        self.selectHardEdgesButton.clicked.connect(self.selectHardEdges)
        self.selectSoftEdgesButton.clicked.connect(self.selectSoftEdges)
        self.smoothingAngleCheckBox.stateChanged.connect(self.toggleSmoothingAngle)
        self.smoothingAngleSlider.valueChanged.connect(self.smoothingAngleFromSliderToSpinBox)
        self.smoothingAngleSpinBox.valueChanged.connect(self.smoothingAngleFromSpinBoxToSlider)
        self.memberButton.clicked.connect(self.showMembers)
        self.bevelButton.clicked.connect(self.backToBevelState)
        self.finishBevelButton.clicked.connect(self.finishBevel)
        self.finishBevelAction.triggered.connect(self.finishBevel)
        self.selectionModelInBevelSetTreeView.selectionChanged.connect(self.activeControlButtons)


    def _mousePressEventInBevelSetLabel(self, event):
        isVisible = not self.bevelSetGroupBox.isVisible()
        self.bevelSetGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelSetLabel, event)


    def _mousePressEventInBevelLabel(self, event):
        isVisible = not self.bevelGroupBox.isVisible()
        self.bevelGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelLabel, event)


    def _mousePressEventInSelectionLabel(self, event):
        isVisible = not self.selectionGroupBox.isVisible()
        self.selectionGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.selectionLabel, event)


    def _mousePressEventInBevelSetTreeView(self, event):
        self.selectionModelInBevelSetTreeView.clearSelection()
        QTreeView.mousePressEvent(self.bevelSetTreeView, event)


    def _activeSelectionListchangedCallback(self, clientData=None):
        self.selectionModelInBevelSetTreeView.clearSelection()
        bevelSet = utils.navigateBevelSetFromActiveSelectionList(clientData)
        if len(bevelSet) == 1:
            item = self.dataModelInBevelSetTreeView.findItems(bevelSet[0]+' '*4, Qt.MatchFixedString|Qt.MatchCaseSensitive, 0)
            if len(item):
                index = self.dataModelInBevelSetTreeView.indexFromItem(item[0])
                self.selectionModelInBevelSetTreeView.select(index, QItemSelectionModel.ClearAndSelect|QItemSelectionModel.Rows)
        elif len(bevelSet) > 1:
            self.statusbar.showMessage(status.INFO['Bevel set'])


    def _removeBevelSetCallback(self, dgNode, clientData=None):
        self.updateBevelSetTreeView()


    def _beforeSceneUpdateCallback(self, clientData=None):
        self.setEnabled(False)


    def _sceneUpdateCallback(self, clientData=None):
        self.setEnabled(True)
        self.updateBevelSetTreeView()


    def _showEventInBevelSetTreeView(self, event):
        cb = om.MModelMessage.addCallback(om.MModelMessage.kActiveListModified, self._activeSelectionListchangedCallback, None)
        self.registeredMayaCallbacks.append(utils.MCallBackIdWrapper(cb))
        cb = om.MDGMessage.addNodeRemovedCallback(self._removeBevelSetCallback, 'objectSet', None)
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
        QTreeView.showEvent(self.bevelSetTreeView, event)


    def _hideEventInBevelSetTreeView(self, event):
        self.registeredMayaCallbacks = []
        self.backToBevelState()
        QTreeView.hideEvent(self.bevelSetTreeView, event)


    def _editItemBrush(self, bevelSetName):
        item = self.dataModelInBevelSetTreeView.findItems(bevelSetName+' '*4, Qt.MatchFixedString|Qt.MatchCaseSensitive, 0)
        len(item) != 1 or item[0].setBackground(self.itemEditedBrush)


    def updateBevelSetTreeView(self):
        self.dataModelInBevelSetTreeView.clear()
        for col, header in enumerate(self.HEADERSINBEVELSETTREEVIEW):
            item = QStandardItem(header)
            item.setFont(self.headerFont)
            self.dataModelInBevelSetTreeView.setHorizontalHeaderItem(col, item)

        for bevelset in utils.MWBevelSets():
            item = QStandardItem(bevelset.name()+' '*4)
            item.setFont(self.itemFont)
            item.setEditable(False)
            self.dataModelInBevelSetTreeView.appendRow(item)
            row = self.dataModelInBevelSetTreeView.indexFromItem(item).row()
            index = self.dataModelInBevelSetTreeView.indexFromItem(item)

            value = bevelTool.MWBevelOption(bevelset.name(), 'Fraction')
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, 1, item)

            value = bevelTool.MWBevelOption(bevelset.name(), 'Segments')
            item = QStandardItem(str(value))
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, 2, item)

            mitering = bevelTool.MWBevelOption(bevelset.name(), 'Mitering')
            item = QStandardItem(options.MITERING[mitering])
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, 3, item)

            value = bevelTool.MWBevelOption(bevelset.name(), 'Miter Along')
            item = QStandardItem(options.MITERALONG[value])
            item.setFont(self.itemFont)
            mitering != 4 or item.setEditable(False)
            self.dataModelInBevelSetTreeView.setItem(row, 4, item)

            value = bevelTool.MWBevelOption(bevelset.name(), 'Chamfer')
            item = QStandardItem(options.CHAMFER[value])
            item.setFont(self.itemFont)
            self.dataModelInBevelSetTreeView.setItem(row, 5, item)

        map(lambda col:self.bevelSetTreeView.resizeColumnToContents(col), range(len(self.HEADERSINBEVELSETTREEVIEW)))


    def createNewBevelSet(self):
        with utils.MayaUndoChuck('Create a bevel set.'):
            newBevelSet = utils.createBevelSet()
            if newBevelSet is not None:
                self.bevelOnMWBevelSet(newBevelSet.name())
                self.updateBevelSetTreeView()
                self.statusbar.clearMessage()
            else:
                self.statusbar.showMessage(status.WARNING['New bevel set'])


    def bevelOnMWBevelSet(self, bevelSetName):
        members = utils.bevelSetMembers(bevelSetName)
        not len(members) or bevelTool.bevelOnSelectedBevelSet(bevelSetName, **self.bevelOptions)


    def _redoBevel(self, bevelSetName):
        utils.deletePolyBevelNodeInBevelSet(bevelSetName)
        self.bevelOnMWBevelSet(bevelSetName)
        map(lambda i:utils.deleteBevelSet(i['Bevel']), self.polyBevel3Info[1:])
        self.polyBevel3Info = []


    def addEdgesIntoBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            with utils.MayaUndoChuck('Add members.'):
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
            if len(utils.bevelSetMembers(bevelSetName)):
                self._redoBevel(bevelSetName)
            else:
                utils.deleteBevelSet(bevelSetName)
            self.updateBevelSetTreeView()
        else:
            self.statusbar.showMessage(status.WARNING['Select bevelset'])


    def selectEdgesInBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            utils.selectMembersInBevelSet(bevelSetName)
            self.statusbar.clearMessage()
        else:
            self.statusbar.showMessage(status.WARNING['Select bevelset'])


    def deleteBevelSet(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            utils.deleteBevelSet(bevelSetName)
            self.updateBevelSetTreeView()


    def selectHardEdges(self):
        angle = self.smoothingAngleSpinBox.value()
        not self.smoothingAngleCheckBox.isChecked() or utils.setSmoothingAngle(angle)
        utils.selectHardEdges()


    def selectSoftEdges(self):
        angle = self.smoothingAngleSpinBox.value()
        not self.smoothingAngleCheckBox.isChecked() or utils.setSmoothingAngle(angle)
        utils.selectSoftEdges()


    def toggleSmoothingAngle(self, state):
        if Qt.Checked == state:
            self.smoothingAngleSlider.setEnabled(True)
            self.smoothingAngleSpinBox.setEnabled(True)
        else:
            self.smoothingAngleSlider.setEnabled(False)
            self.smoothingAngleSpinBox.setEnabled(False)


    def smoothingAngleFromSpinBoxToSlider(self, value):
        _value = value * 10000
        self.smoothingAngleSlider.value() == _value or self.smoothingAngleSlider.setValue(_value)


    def smoothingAngleFromSliderToSpinBox(self, value):
        _value = round((value/10000.0), 4)
        self.smoothingAngleSpinBox.value() == _value or self.smoothingAngleSpinBox.setValue(_value)


    def showMembers(self):
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            self.backToBevelState()
            self.polyBevel3Info = bevelTool.bevelMembers(bevelSetName)
            map(lambda info:utils.deletePolyBevelNodeInBevelSet(info['Bevel']), self.polyBevel3Info[::-1])
            # Clear the bevel set. The bevel set may contain some edges after deleting the polyBevel3 node.
            map(lambda info:utils.clearBevelSet(info['Bevel']), self.polyBevel3Info)
            utils.addMembersIntoBevelSet(bevelSetName, self.polyBevel3Info[0]['members'])
            utils.selectMembersInBevelSet(bevelSetName)
            self._editItemBrush(bevelSetName)


    def backToBevelState(self):
        for bevelInfo in self.polyBevel3Info:
            bevelOptions = copy.copy(options.bevelOptions)
            bevelOptions['fraction'] = bevelInfo['options'][0]
            bevelOptions['segments'] = bevelInfo['options'][1]
            bevelOptions['mitering'] = bevelInfo['options'][2]
            bevelOptions['miterAlong'] = bevelInfo['options'][3]
            bevelOptions['chamfer'] = 0 if bevelInfo['options'][4] == False else 1
            utils.addMembersIntoBevelSet(bevelInfo['Bevel'], bevelInfo['members'])
            bevelTool.bevelOnSelectedBevelSet(bevelInfo['Bevel'], **bevelOptions)

        self.updateBevelSetTreeView()
        self.polyBevel3Info = []


    def activeControlButtons(self):
        self.newBevelSetButton.setEnabled(True)
        self.memberButton.setEnabled(False)
        self.bevelButton.setEnabled(False)
        self.addMemberButton.setEnabled(False)
        self.removeMemberButton.setEnabled(False)
        self.deleteBevelSetbutton.setEnabled(False)
        self.selectMembersButton.setEnabled(False)
        if self.selectionModelInBevelSetTreeView.hasSelection():
            index = self.selectionModelInBevelSetTreeView.selectedRows()[0]
            bevelSetName = self.dataModelInBevelSetTreeView.itemFromIndex(index).text().strip()
            _member = utils.bevelSetMembers(bevelSetName)
            len(_member) or self.memberButton.setEnabled(True)
            not len(_member) or self.newBevelSetButton.setEnabled(False)
            not len(_member) or self.bevelButton.setEnabled(True)
            not len(_member) or self.addMemberButton.setEnabled(True)
            not len(_member) or self.removeMemberButton.setEnabled(True)
            not len(_member) or self.selectMembersButton.setEnabled(True)
            self.deleteBevelSetbutton.setEnabled(True)


    def finishBevel(self):
        utils.finishBevel()
        self.updateBevelSetTreeView()



def run():
    window = MWBevelToolMainWindow(getMayaWindow())
    window.show()



if __name__ == '__main__':
    run()
