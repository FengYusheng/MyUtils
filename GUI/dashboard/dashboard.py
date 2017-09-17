# -*- coding: utf-8 -*-

import sys
import csv
import os
import math
from collections import deque

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui_dashboard import Ui_DashboardMainWindow


start_angle = -90


class RenderDashboard(QWidget):
    def __init__(self, parent=None):
        super(RenderDashboard, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAutoFillBackground(True)
        self.parent = parent


    def paintEvent(self, event):
        # Init the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.black)
        painter.translate(self.width()/2, self.height()/2)
        line = QLine(180, 0, 200, 0)
        pointer = QPolygon([
            QPoint(-2, 0),
            QPoint(2, 0),
            QPoint(0, -170)
        ])

        recordCount = len(self.parent.data)
        if recordCount:
            _, budget = self.parent.data[recordCount-1]
            currentCount = self.parent.polyCountSlider.value()
            overspending = int(budget) + 5000
            step = int(overspending / 300 * 5)

            # Paint the marks
            painter.rotate(start_angle)
            angle = start_angle
            count = 0
            while angle <= 210:
                if step * count <= budget:
                    painter.setPen(QPen(Qt.green))
                else:
                    painter.setPen(QPen(Qt.red))
                painter.drawLine(line)

                if not angle % 25:
                    painter.save()
                    painter.setPen(QPen(Qt.white))
                    painter.drawLine(line)
                    painter.translate(150, 0)
                    painter.rotate(0-angle)

                    if angle > 45:
                        painter.drawText(-20, 0, str(step*count/1000)+'K')
                    else:
                        painter.drawText(0, 0, str(step*count/1000)+'K')

                    painter.restore()

                painter.rotate(5)
                angle += 5
                count += 1

            painter.rotate(0-angle)

            # Paint the pointer.
            painter.save()
            angle = int(currentCount / overspending * 300)
            painter.rotate(angle)
            painter.setPen(QPen(QBrush(Qt.cyan), 1))
            painter.drawConvexPolygon(pointer)
            painter.restore()

            # Display current poly count and level
            painter.save()
            painter.translate(250, 0)
            painter.setPen(QPen(QBrush(Qt.cyan), 5))
            painter.drawText(0, 0, str(currentCount))
            painter.restore()
        else:
            # Paint tips
            painter.save()
            painter.setPen(QPen(QBrush(Qt.gray), 15))
            painter.drawText(0, 0, 'Import your budget.')
            painter.restore()


class DashboardMainWindow(QMainWindow, Ui_DashboardMainWindow):
    def __init__(self, parent=None):
        super(DashboardMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dashboardRender = RenderDashboard(self)
        self.setCentralWidget(self.dashboardRender)
        self.model = QStandardItemModel(self)
        self.budgetTableView.setModel(self.model)
        self.menuView.addAction(self.budgetDock.toggleViewAction())
        self.menuView.addAction(self.sliderDock.toggleViewAction())
        self.polyCountSlider.setMinimum(0)
        self.polyCountSlider.setMaximum(0)
        self.polyCountSlider.setSingleStep(100)
        self.font = QFont("Monospace", 10, QFont.Bold)
        self.data = deque()

        self.importDataAction.triggered.connect(self.importData)
        self.polyCountSlider.valueChanged.connect(self.displayCurrentPolyCount)


    def importData(self):
        if os.access('data.csv', os.F_OK):
            self.model.clear()
            index = 0
            for header in ('Level', 'From', 'To'):
                item = QStandardItem(header)
                item.setFont(self.font)
                item.setEditable(False)
                self.model.setHorizontalHeaderItem(index, item)
                index += 1

            with open('data.csv', newline='') as csvfile:
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

                    self.data.append((record[0], int(record[2])))

                self.budgetTableView.resizeColumnsToContents()
                self.polyCountSlider.setMaximum(self.data[-1][1]+5000)
                self.dashboardRender.update()


    def displayCurrentPolyCount(self):
        self.dashboardRender.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DashboardMainWindow()
    window.show()
    sys.exit(app.exec_())
