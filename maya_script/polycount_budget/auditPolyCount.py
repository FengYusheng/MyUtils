# -*- coding: utf-8 -*-

import sys
import os
import csv
import json
from collections import deque

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide import __version__
    from shiboken import wrapInstance

import pymel.core as pm

sys.path.insert(0, os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
from ui_auditMainWindow import Ui_AuditMainWindow
sys.path.remove(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))

MAYA_VERION = pm.mel.eval('getApplicationVersionAsFloat();')


class DashboardRender(QWidget):
    def __init__(self, parent):
        super(DashboardRender, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAutoFillBackground(True)
        self.parent = parent
        self.selectedAssetPolyCount = 0
        self.selectedAssetLODMessage = ''


    def moveHand(self, count=0):
        self.selectedAssetLODMessage = ''
        if len(self.parent.data):
            self.selectedAssetPolyCount = count
            fmt = '{0} : {1} {2}'
            self.selectedAssetLODMessage = fmt.format(self.parent.data[0][0], self.selectedAssetPolyCount, self.parent.data[0][2]) if count else ''
            for record in self.parent.data:
                if record[1] <= self.selectedAssetPolyCount:
                    self.selectedAssetLODMessage = fmt.format(record[0], self.selectedAssetPolyCount, record[2])

            if self.selectedAssetPolyCount >= self.parent.data[-1][1]:
                self.selectedAssetLODMessage = fmt.format('Overspending', self.selectedAssetPolyCount, self.parent[-1][2])

            self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.black)
        line = QLine(self.width()/4, 0, self.width()/4+20, 0)
        longLine = QLine(self.width()/4, 0, self.width()/4+30, 0)
        startAngle = -240.0
        endAngle = 60.0
        intervalAngle = 5.0
        angle = startAngle
        hand = QPolygon([
            QPoint(0, 2),
            QPoint(0, -2),
            QPoint(self.width()/4-5, 0)
        ])

        recordCount = len(self.parent.data)
        if recordCount:
            # Paint the dial
            count = 0
            overspending = int(self.parent.data[-1][1]) * 1.2
            step = int(overspending / (endAngle - startAngle) * intervalAngle)
            while angle <= endAngle:
                painter.save()
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.translate(self.width()/2, self.height()/2)
                painter.rotate(angle)
                pen = QPen(Qt.green) if count <= self.parent.data[-1][1] else QPen(Qt.red)
                painter.setPen(pen)

                if not angle % int(intervalAngle * 5):
                    painter.drawLine(longLine)
                    painter.translate(self.width()/4-20, 0)
                    painter.rotate(0-angle)
                    painter.setPen(Qt.white)
                    coordinate = (-20, 0) if angle >= -60.0 else (0, 0)
                    painter.drawText(coordinate[0], coordinate[1], str(round(count/1000.0, 1))+'K')
                else:
                    painter.drawLine(line)

                painter.restore()
                angle += intervalAngle
                count += step

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.translate(self.width()/2, self.height()/2)
            # selectedAssetPolyCount / overspending == angle / (endAngle - startAngle)
            angle = int(self.selectedAssetPolyCount / overspending * (endAngle - startAngle) + startAngle)
            painter.rotate(angle)
            painter.setPen(QPen(Qt.white, 1))
            painter.drawConvexPolygon(hand)
            painter.restore()

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.translate(self.width()/2-40, self.height()/2+60)
            painter.setPen(Qt.white)
            self.selectedAssetPolyCount <= self.parent.data[-1][1] or painter.setPen(Qt.red)
            painter.drawText(0, 0, self.selectedAssetLODMessage)
            painter.restore()

            painter.save()
            painter.translate(0, 15)
            painter.setPen(Qt.white)
            offset = 0
            for record in self.parent.data:
                painter.drawText(0, offset, record[0]+' : '+str(record[1]))
                offset += 20
            painter.restore()
        else:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.translate(self.width()/2, self.height()/2)
            painter.setPen(QPen(Qt.darkGray, 14))
            painter.drawText(0, 0, 'Import budget data.')
            painter.restore()



class AuditPolyCount(QMainWindow, Ui_AuditMainWindow):
    def __init__(self, parent=None):
        super(AuditPolyCount, self).__init__(parent)
        self.data = deque()
        self.scene = None
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.menuView.addAction(self.budgetDock.toggleViewAction())
        self.menuView.addAction(self.polyCountDock.toggleViewAction())
        self.font = QFont('OldEnglish', 10, QFont.Bold)
        self.model = QStandardItemModel(self.budgetTabelView)
        self.budgetTabelView.setModel(self.model)
        self.budgetTabelView.mouseDoubleClickEvent = self._mouseDoubleClickEventInBudgetTableView
        self.polyCountModel = QStandardItemModel(self.polyCountTreeView)
        self.polyCountTreeView.setModel(self.polyCountModel)
        self.polyCountSelectionModel = QItemSelectionModel(self.polyCountModel, self.polyCountTreeView)
        self.polyCountTreeView.setSelectionModel(self.polyCountSelectionModel)
        self.polyCountTreeView.mousePressEvent = self._mousePressEventInTreeView
        self.polyCountTreeView.mouseDoubleClickEvent = self._mouseDoubleClickEventInTreeView
        self.dashboard = DashboardRender(self)
        self.setCentralWidget(self.dashboard)

        self.importBudgetAction.triggered.connect(self.readBudget)
        self.polyCountAction.triggered.connect(self.getPolyCount)
        self.polyCountSelectionModel.selectionChanged.connect(self.selectMayaObjectFromView)


    def readBudget(self):
        '''
        TODO: visualize the budget.
             https://stackoverflow.com/questions/23395056/how-to-draw-a-linear-gradient-arc-with-qt-qpainter

             http://doc.qt.io/qt-5/qtwidgets-itemviews-chart-example.html
        '''
        current_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
        budget_path = pm.fileDialog2(cap='Open', ds=2, fm=1, dir=current_dir, okc='Open', ff='All CSV Files (*.csv)')
        if budget_path is not None:
            self.model.clear()
            self.data.clear()

            index = 0
            for header in ('LOD', 'From', 'TO', 'Tris/Verts'):
                item = QStandardItem(header)
                item.setFont(self.font)
                item.setEditable(False)
                self.model.setHorizontalHeaderItem(index, item)
                index += 1

            with open(budget_path[0], 'rb') as csvfile:
                reader = csv.reader(csvfile, dialect=csv.excel)
                for record in reader:
                    item = QStandardItem(record[0])
                    item.setFont(self.font)
                    item.setEditable(False)
                    self.model.appendRow(item)
                    row = self.model.indexFromItem(item).row()

                    item = QStandardItem(record[1])
                    item.setFont(self.font)
                    item.setEditable(False)
                    self.model.setItem(row, 1, item)

                    item = QStandardItem(record[2])
                    item.setFont(self.font)
                    item.setEditable(False)
                    self.model.setItem(row, 2, item)

                    item = QStandardItem(record[3])
                    item.setFont(self.font)
                    item.setEditable(False)
                    self.model.setItem(row, 3, item)

                    self.data.append((record[0], int(record[2]), record[3]))

                self.budgetTabelView.resizeColumnsToContents()
                self.dashboard.update()


    def _displayPolyCountInTreeView(self, polyCount):
        # Display total poly count first
        self.scene = pm.system.sceneName().rpartition('/')[2].partition('.')[0]
        item = QStandardItem(self.scene)
        item.setFont(self.font)
        item.setEditable(False)
        self.polyCountModel.appendRow(item)
        parent = item

        item = QStandardItem(str(polyCount['Tris']))
        item.setFont(self.font)
        item.setEditable(False)
        self.polyCountModel.setItem(0, 1, item)

        item = QStandardItem(str(polyCount['Verts']))
        item.setFont(self.font)
        item.setEditable(False)
        self.polyCountModel.setItem(0, 2, item)

        # Display the poly count of each asset.
        self._displayPolyCountGroupByAsset(polyCount['hierarchy'], parent)


    def _displayPolyCountGroupByAsset(self, hierarchy, parent=None):
        if parent is not None:
            for root in hierarchy.keys():
                item = QStandardItem(root)
                item.setFont(self.font)
                item.setEditable(False)
                parent.appendRow(item)
                row = self.polyCountModel.indexFromItem(item).row()
                parent2 = item

                item = QStandardItem(str(hierarchy[root]['Tris']))
                item.setFont(self.font)
                item.setEditable(False)
                parent.setChild(row, 1, item)

                item = QStandardItem(str(hierarchy[root]['Verts']))
                item.setFont(self.font)
                item.setEditable(False)
                parent.setChild(row, 2, item)

                self._displayPolyCountGroupByAsset(hierarchy[root]['children'], parent2)


    def getPolyCount(self):
        scene_path = pm.system.sceneName().dirname()
        path = pm.fileDialog2(cap='Open', ds=2, fm=1, dir=scene_path, okc='Open', ff='All Json Files (*.json)')
        if path is not None:
            with open(path[0], 'r') as source:
                polyCount = json.load(source, encoding='utf-8')

            # Tree view header
            index = 0
            self.polyCountModel.clear()
            for header in ('Asset', 'Tris', 'Verts'):
                item = QStandardItem(header)
                item.setFont(self.font)
                item.setEditable(False)
                self.polyCountModel.setHorizontalHeaderItem(index, item)
                index += 1

            self._displayPolyCountInTreeView(polyCount)

            self.polyCountTreeView.resizeColumnToContents(0)
            self.polyCountTreeView.resizeColumnToContents(1)
            self.polyCountTreeView.resizeColumnToContents(2)


    def _selectTransformsFromContainer(self, container=None):
        if isinstance(container, pm.nt.Container):
            transforms = []
            queue = deque(container.getNodeList())
            while len(queue):
                node = queue.popleft()
                if isinstance(node, pm.nt.Transform):
                    transforms.append(node)
                elif isinstance(node, pm.nt.Container):
                    queue.extend(node.getNodeList())

            not len(transforms) or pm.select(transforms, r=True)


    def selectMayaObjectFromView(self):
        '''
        Various approaches to select objects in Maya.
        '''
        self.dashboard.moveHand(0)
        if self.polyCountSelectionModel.hasSelection():
            index = self.polyCountSelectionModel.selectedRows()[0]
            text = self.polyCountModel.itemFromIndex(index).text()

            index = self.polyCountSelectionModel.selectedRows(1)[0]
            count = int(self.polyCountModel.itemFromIndex(index).text())
            self.dashboard.moveHand(count)

            if self.scene == text:
                # Select all polygon geometries.
                transforms = pm.listTransforms(type='mesh')
                pm.select(transforms, r=True)
            else:
                # Select individual asset.
                node = pm.ls(text)[0]
                not isinstance(node, pm.nt.DagContainer) or pm.select(node, r=True)
                not isinstance(node, pm.nt.Container) or self._selectTransformsFromContainer(node)


    def _mousePressEventInTreeView(self, event):
        '''
        https://stackoverflow.com/questions/2761284/is-it-possible-to-deselect-in-a-qtreeview-by-clicking-off-an-item
        '''
        self.polyCountTreeView.clearSelection()
        QTreeView.mousePressEvent(self.polyCountTreeView, event)


    def _mouseDoubleClickEventInTreeView(self, event):
        self.getPolyCount()
        QTreeView.mouseDoubleClickEvent(self.polyCountTreeView, event)


    def _mouseDoubleClickEventInBudgetTableView(self, event):
        self.readBudget()
        QTableView.mouseDoubleClickEvent(self.budgetTabelView, event)


if __name__ == '__main__':
    window = AuditPolyCount()
    window.show()
