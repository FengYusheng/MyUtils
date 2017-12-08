# -*- coding: utf-8 -*-
import json
import csv
import os

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

import pymel.core as pm
import maya.OpenMayaUI as apiUI

import loadArtistUI
loadArtistUI.loadUIForArtist()
import ui_MainWindowForArtist
reload(ui_MainWindowForArtist)
import ui_ChooseLocationDialog
reload(ui_ChooseLocationDialog)
import checkers.CheckAsset as CheckAsset
import GlobalInArtist



def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QWidget)



class ProgressBarDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ProgressBarDelegate, self).__init__(parent)
        self.progress = 0
        self.min = 0
        self.max = 0


    def setProgress(self, progress):
        self.progress = progress


    def paint(self, painter, option, index):
        if 1 == index.column():
            progressBarOption = QStyleOptionProgressBar()
            progressBarOption.rect = option.rect
            progressBarOption.minimum = 0
            progressBarOption.maximum = 100
            progressBarOption.progress = self.progress
            progressBarOption.text = '{0}%'.format(self.progress)
            progressBarOption.textVisible = True
            QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBarOption, painter)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)



class ChooseLocationDialog(QDialog, ui_ChooseLocationDialog.Ui_ChooseLocationDialog):
    def __init__(self, parent=None):
        super(ChooseLocationDialog, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.applyButton.setDefault(True)
        self.applyButton.setEnabled(False)

        self.parent = parent
        self.location = None

        self.closeButton.clicked.connect(self.quit)
        self.applyButton.clicked.connect(self.applyLocation)
        self.chooseLocationButton.clicked.connect(self.choose)


    def choose(self):
        self.applyButton.setEnabled(False)
        destination = pm.fileDialog2(cap='Open', ds=2, fm=3, okc='Open')
        if destination is not None:
            self.locationLineEdit.setText(destination[0])
            self.applyButton.setEnabled(True)
            self.location = destination[0]


    def quit(self):
        self.reject()


    def applyLocation(self):
        self.parent.setLocation(self.location)
        self.accept()


class MainWindowForArtist(QMainWindow, ui_MainWindowForArtist.Ui_MainWindowForArtist):
    TIPTAB = 0
    DETAILTAB = 1

    def __init__(self, parent=None):
        super(MainWindowForArtist, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dataModelInCheckerTableView = QStandardItemModel(self.checkerTableView)
        self.checkerTableView.setModel(self.dataModelInCheckerTableView)
        self.selectionModelIncheckerTableView = QItemSelectionModel(self.dataModelInCheckerTableView, self.checkerTableView)
        self.checkerTableView.setSelectionModel(self.selectionModelIncheckerTableView)
        self.checkerTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.checkerTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.checkerTableView.mousePressEvent = self._mousePressEventInCheckerTableView
        self.progressBarDelegateInCheckerTableView = ProgressBarDelegate(self)
        self.checkerTableView.setItemDelegate(self.progressBarDelegateInCheckerTableView)
        self.dataModelInDetailTableView = QStandardItemModel(self.detailTableView)
        self.detailTableView.setModel(self.dataModelInDetailTableView)
        self.selectionModelInDetailTableView = QItemSelectionModel(self.dataModelInDetailTableView, self.detailTableView)
        self.detailTableView.setSelectionModel(self.selectionModelInDetailTableView)
        self.dataModelInResultTreeView = QStandardItemModel(self.resultTreeView)
        self.resultTreeView.setModel(self.dataModelInResultTreeView)
        self.selectionModelInResultTreeView = QItemSelectionModel(self.dataModelInResultTreeView, self.resultTreeView)
        self.resultTreeView.setSelectionModel(self.selectionModelInResultTreeView)
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(self.checkerTableView)
        self.splitter.addWidget(self.messageTabWidget)
        self.horizontalLayout.addWidget(self.splitter)
        self.splitter2 = QSplitter(self)
        self.splitter2.setOrientation(Qt.Vertical)
        self.splitter2.addWidget(self.splitter)
        self.splitter2.addWidget(self.displayTabWidget)
        self.verticalLayout.addWidget(self.splitter2)

        self.data = {}
        self.result = None
        self.parent = parent
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.brush = QBrush(Qt.GlobalColor.darkGray)

        self.projectComboBox.currentIndexChanged.connect(self.changeProject)
        self.selectionModelIncheckerTableView.selectionChanged.connect(self.configuration)
        self.checkButton.clicked.connect(self.checkAsset)


    def _initializeProjectList(self):
        self.projectComboBox.clear()
        self.projectComboBox.addItems(self.projects())


    def _initializeCheckerList(self):
        project = self.projectComboBox.currentText()
        self.dataModelInCheckerTableView.clear()
        col = 0
        for header in ('Checker', 'State'):
            item = QStandardItem(header)
            item.setFont(self.font)
            self.dataModelInCheckerTableView.setHorizontalHeaderItem(col, item)
            col += 1

        for checker in self.checkers(project):
            item = QStandardItem(checker)
            item.setEditable(False)
            item.setCheckable(True)
            item.setFont(self.font)
            item.setBackground(self.brush)
            self.dataModelInCheckerTableView.appendRow(item)
            row = self.dataModelInCheckerTableView.indexFromItem(item).row()

            item = QStandardItem('not start')
            item.setEditable(False)
            item.setFont(self.font)
            self.dataModelInCheckerTableView.setItem(row, 1, item)

        self.checkerTableView.resizeColumnsToContents()


    def _initializeData(self):
        def _initializeProjects():
            for root, subdirs, filenames in os.walk(self.location()):
                self.setProjects(subdirs)
                break

        def _initializeCheckers():
            location = self.location()
            for project in self.projects():
                s = location + '/' + project + '/checkers.csv'
                if os.access(s, os.F_OK):
                    with open(s, 'rb') as csvfile:
                        reader = csv.reader(csvfile, dialect=csv.excel)
                        self.setCheckers(project, [i[0].decode('utf-8') for i in reader])

        def _initializeTips():
            location = self.location()
            for project in self.projects():
                checkers = self.checkers(project)
                s = location + '/' + project + '/tip'
                if os.access(s, os.F_OK):
                    for tip in os.walk(s).next()[2]:
                        if tip.rpartition('.')[0] in checkers:
                            with open(s+'/'+tip, 'r') as f:
                                self.setTip(project, tip.rpartition('.')[0], f.read().decode('utf-8').strip())

        def _initializeDetails():
            location = self.location()
            for project in self.projects():
                checkers = self.checkers(project)
                s = location + '/' + project + '/detail'
                if os.access(s, os.F_OK):
                    for detail in os.walk(s).next()[2]:
                        if detail.rpartition('.')[0] in checkers and detail.rpartition('.')[0] in GlobalInArtist.detail:
                            with open(s+'/'+detail, 'rb') as csvfile:
                                reader = csv.reader(csvfile, dialect=csv.excel)
                                self.setDetail(project, detail.rpartition('.')[0], [i for i in reader])

        _initializeProjects()
        _initializeCheckers()
        _initializeTips()
        _initializeDetails()
        self._initializeProjectList()
        self._initializeCheckerList()


    def _mousePressEventInCheckerTableView(self, event):
        self.selectionModelIncheckerTableView.clearSelection()
        QTableView.mousePressEvent(self.checkerTableView, event)


    def _displayTip(self, project, checker):
        self.tipTextBrower.setFontPointSize(12.0)
        self.tipTextBrower.setText(self.tip(project, checker))


    def _displayPolyCountDetail(self, project):
        self.dataModelInDetailTableView.clear()
        col = 0
        for header in ('LOD', 'Tris/Verts', 'Budget'):
            item = QStandardItem(header)
            item.setFont(self.font)
            self.dataModelInDetailTableView.setHorizontalHeaderItem(col, item)
            col += 1

        row = 0
        for level, polygon, budget in self.detail(project, 'check poly count'):
            item = QStandardItem(level.decode('utf-8'))
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInDetailTableView.appendRow(item)

            item = QStandardItem(polygon.decode('utf-8'))
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInDetailTableView.setItem(row, 1, item)

            item= QStandardItem(budget.decode('utf-8'))
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInDetailTableView.setItem(row, 2, item)

            row += 1

        self.detailTableView.resizeColumnsToContents()


    def _displayShaderNamesDetails(self, project):
        self.dataModelInDetailTableView.clear()
        for i in self.detail(project, 'check shader names'):
            item = QStandardItem(i[0].decode('utf-8'))
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInDetailTableView.appendRow(item)

        self.detailTableView.resizeColumnsToContents()


    def _displayDetail(self, project, checker):
        self.dataModelInDetailTableView.clear()
        if checker in GlobalInArtist.detail:
            if 'check poly count' == checker:
                self._displayPolyCountDetail(project)
            elif 'check shader names' == checker:
                self._displayShaderNamesDetails(project)


    def _displayPolyCountResult(self, project):
        def _lod(lods, polycount):
            level = 'Overspend'
            _lods = lods[:]
            _lods.insert(0, ('LOD_1', lods[0][1], lods[0][2]*1.2))
            for lod in _lods:
                if polycount <= lod[2]:
                    level = lod[0]

            return level

        def _displayPolyCountGroupByAsset(lods, hierarchy, parent=None):
            if parent is not None:
                polygon = 'Verts' if lods[0][1] == 'Vertex' else 'Tris'
                for root in hierarchy.keys():
                    item = QStandardItem(root)
                    item.setFont(self.font)
                    item.setEditable(False)
                    parent.appendRow(item)
                    row = self.dataModelInResultTreeView.indexFromItem(item).row()
                    _parent = item

                    item = QStandardItem(polygon)
                    item.setFont(self.font)
                    item.setEditable(False)
                    parent.setChild(row, 1, item)

                    polycount = hierarchy[root][polygon]
                    item = QStandardItem(str(polycount))
                    item.setFont(self.font)
                    item.setEditable(False)
                    parent.setChild(row, 2, item)

                    level = _lod(lods, polycount)
                    item = QStandardItem(level)
                    item.setFont(self.font)
                    item.setEditable(False)
                    parent.setChild(row, 3, item)

                    _displayPolyCountGroupByAsset(lods, hierarchy[root]['children'], _parent)

        index = 0
        parent = None
        checker = 'check poly count'
        lods = [(lod[0].decode('utf-8'), lod[1].decode('utf-8'), float(lod[2].decode('utf-8').rpartition('K')[0])*1000.0) for lod in self.detail(project, checker)]
        self.dataModelInResultTreeView.clear()
        if checker in self.result:
            for header in ('Asset', 'Tris/Verts', 'Poly Count', 'LOD'):
                item = QStandardItem(header)
                item.setFont(self.font)
                self.dataModelInResultTreeView.setHorizontalHeaderItem(index, item)
                index += 1

            scene = pm.system.sceneName()
            scene = scene.rpartition('/')[2].rpartition('.')[0] if scene else 'Untitled'
            item = QStandardItem(scene)
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInResultTreeView.appendRow(item)
            parent = item

            polygon = 'Verts' if lods[0][1] == 'Vertex' else 'Tris'
            item = QStandardItem(polygon)
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInResultTreeView.setItem(0, 1, item)

            polycount = self.result[checker][polygon]
            item = QStandardItem(str(polycount))
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInResultTreeView.setItem(0, 2, item)

            level = _lod(lods, polycount)
            item = QStandardItem(level)
            item.setFont(self.font)
            item.setEditable(False)
            self.dataModelInResultTreeView.setItem(0, 3, item)

            _displayPolyCountGroupByAsset(lods, self.result[checker]['hierarchy'], parent)
            map(lambda i : self.resultTreeView.resizeColumnToContents(i), range(index))


    def _displayCommonResult(self, project, checker):
        self.dataModelInResultTreeView.clear()
        if checker in self.result:
            item = QStandardItem(checker)
            item.setFont(self.font)
            self.dataModelInResultTreeView.setHorizontalHeaderItem(0, item)
            for i in self.result[checker]:
                item = QStandardItem(i)
                item.setFont(self.font)
                item.setEditable(False)
                self.dataModelInResultTreeView.appendRow(item)
            self.resultTreeView.resizeColumnToContents(0)


    def _displayNGonsResult(self, project, checker):
        parent = None
        self.dataModelInResultTreeView.clear()
        if checker in self.result:
            item = QStandardItem(checker)
            item.setFont(self.font)
            self.dataModelInResultTreeView.setHorizontalHeaderItem(0, item)
            for k, v in self.result[checker].items():
                item = QStandardItem(k)
                item.setFont(self.font)
                item.setEditable(False)
                self.dataModelInResultTreeView.appendRow(item)
                parent = item
                row = 0
                for i in v:
                    item = QStandardItem(i)
                    item.setFont(self.font)
                    item.setEditable(False)
                    parent.setChild(row, item)
                    row += 1
            self.resultTreeView.resizeColumnToContents(0)


    def _displayResult(self, project, checker):
        if self.result is not None:
            if 'check poly count' == checker:
                self._displayPolyCountResult(project)
            elif 'check n-gons' == checker           \
            or 'check lamina faces' == checker       \
            or 'check overlapping vertices' == checker:
                self._displayNGonsResult(project, checker)
            else:
                self._displayCommonResult(project, checker)


    def setLocation(self, location):
        self.data['location'] = location
        self._initializeData()


    def location(self):
        return self.data.setdefault('location', '')


    def setProjects(self, projects):
        self.data['projects'] = projects
        self.data['projects'].append('Change location')


    def projects(self):
        return self.data.setdefault('projects', ['Change location',])


    def setCheckers(self, project, checkers):
        self.data.setdefault('checkers', {})
        self.data['checkers'][project] = checkers


    def checkers(self, project):
        self.data.setdefault('checkers', {})
        return self.data['checkers'].setdefault(project, [])


    def setTip(self, project, checker, tip):
        self.data.setdefault('tip', {})
        self.data['tip'].setdefault(project, {})
        self.data['tip'][project][checker] = tip


    def tip(self, project, checker):
        self.data.setdefault('tip', {})
        self.data['tip'].setdefault(project, {})
        return self.data['tip'][project].setdefault(checker, '')


    def setDetail(self, project, checker, detail):
        self.data.setdefault('detail', {})
        self.data['detail'].setdefault(project, {})
        self.data['detail'][project][checker] = detail


    def detail(self, project, checker):
        self.data.setdefault('detail', {})
        self.data['detail'].setdefault(project, {})
        return self.data['detail'][project].setdefault(checker, [])


    def quit(self):
        self.close()


    def changeProject(self):
        project = self.projectComboBox.currentText()
        self.result = None
        if project != 'Change location':
            self._initializeCheckerList()
        else:
            self.dataModelInCheckerTableView.clear()
            QDialog.Accepted == ChooseLocationDialog(self).exec_() or self.projectComboBox.setCurrentIndex(0)


    def configuration(self):
        # print self.selectionModelIncheckerTableView.hasSelection()
        # The selection mode is SingleSelection, diselect the selectned item first, then select the new item.
        if self.selectionModelIncheckerTableView.hasSelection():
            project = self.projectComboBox.currentText()
            index = self.selectionModelIncheckerTableView.selectedRows()[0]
            checker = self.dataModelInCheckerTableView.itemFromIndex(index).text()
            self._displayTip(project, checker)
            self._displayDetail(project, checker)
            self.result is None or self._displayResult(project, checker)
        else:
            self.tipTextBrower.clear()
            self.dataModelInDetailTableView.clear()
            self.dataModelInResultTreeView.clear()


    def checkAsset(self):
        activeCheckers = []
        self.result = None
        for row in range(self.dataModelInCheckerTableView.rowCount()):
            index = self.dataModelInCheckerTableView.index(row, 0)
            item = self.dataModelInCheckerTableView.itemFromIndex(index)
            item.checkState() == Qt.Unchecked or activeCheckers.append(item.text())

        if len(activeCheckers):
            project = self.projectComboBox.currentText()
            details = {checker : self.detail(project, checker) for checker in activeCheckers if checker in GlobalInArtist.detail}
            self.result = CheckAsset.checkAsset(activeCheckers, **details)


if __name__ == '__main__':
    window = MainWindowForArtist(getMayaWindow())
    window.show()
    QDialog.Accepted == ChooseLocationDialog(window).exec_() or window.quit()
