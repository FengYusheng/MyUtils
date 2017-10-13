# -*- coding: utf-8 -*-

import sys
import csv
import os

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


MAYA_VERION = pm.mel.eval('getApplicationVersionAsFloat();')


class DashboardRender(QWidget):
    def __init__(self, data=[], parent=None):
        super(DashboardRender, self).__init__(parent)
        self.parent = parent
        self.data = data
        self.startAngle = -240.0
        self.endAngle = 60.0
        self.intervalAngle = 5.0
        self.selectedAssetPolyCount = 0
        self.selectedAssetLODMessage = ''
        self.painter = QPainter(self)

        self.setAutoFillBackground(True)


    def _paintTipMessage(self, painter):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width()/2, self.height()/2)
        painter.setPen(QPen(Qt.darkGray, 14))
        painter.drawText(0, 0, 'Enter your budget in the "Set Budget" table.')
        painter.restore()


    def _paintDashBoard(self, painter):
        def _getPenColor(count):
            color = Qt.red
            for t1, budget, t2, colorTuple in self.data:
                if (count * 1.0) <= (float(budget) * 1000):
                    color = colorTuple[1]
                    break

            return color

        count = 0
        angle = self.startAngle
        line = QLine(self.width()/4, 0, self.width()/4+20, 0)
        longLine = QLine(self.width()/4, 0, self.width()/4+30, 0)
        hand = QPolygon([
            QPoint(0, 2),
            QPoint(0, -2),
            QPoint(self.width()/4-5, 0)
        ])

        # Paint the dial
        overspending = float(self.data[-1][1])*1000 * 1.1
        step = int(overspending / (self.endAngle - self.startAngle) * self.intervalAngle)
        while angle <= self.endAngle:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.translate(self.width()/2, self.height()/2)
            painter.rotate(angle)
            penColor = _getPenColor(count)
            painter.setPen(QPen(penColor))

            if not angle % int(self.intervalAngle * 5):
                painter.drawLine(longLine)
                painter.translate(self.width()/4-20, 0)
                painter.rotate(0-angle)
                painter.setPen(Qt.white)
                coordinate = (-20, 0) if angle >= -60.0 else (0, 0)
                number = str(round(count/1000.0, 1))+'K' if count/1000 else str(count)
                painter.drawText(coordinate[0], coordinate[1], number)
            else:
                painter.drawLine(line)

            painter.restore()
            angle += self.intervalAngle
            count += step

        # Paint the hand.
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width()/2, self.height()/2)
        # selectedAssetPolyCount / overspending == angle / (endAngle - startAngle)
        self.selectedAssetPolyCount = overspending if self.selectedAssetPolyCount > overspending else self.selectedAssetPolyCount
        angle = int(self.selectedAssetPolyCount / overspending * (self.endAngle - self.startAngle) + self.startAngle)
        painter.rotate(angle)
        painter.setPen(QPen(Qt.white, 1))
        painter.drawConvexPolygon(hand)
        painter.restore()

        # Paint the selected asset message
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width()/2-40, self.height()/2+60)
        painter.setPen(Qt.white)
        self.selectedAssetPolyCount <= self.data[-1][1] or painter.setPen(Qt.red)
        painter.drawText(0, 0, self.selectedAssetLODMessage)
        painter.restore()

        # Paint the budget table
        painter.save()
        painter.translate(0, 15)
        painter.setPen(Qt.white)
        offset = 0
        for record in self.data:
            painter.drawText(0, offset, record[0]+' : '+record[1]+'K')
            offset += 20
        painter.restore()


    def moveHand(self, count=0):
        self.selectedAssetLODMessage = ''
        if len(self.data):
            self.selectedAssetPolyCount = count
            fmt = '{0} : {1} {2}'
            self.selectedAssetLODMessage = fmt.format(self.data[0][0], self.selectedAssetPolyCount, self.data[0][2]) if count else ''
            for record in self.data:
                if int((float(record[1]) * 1000)) >= self.selectedAssetPolyCount:
                    self.selectedAssetLODMessage = fmt.format(record[0], self.selectedAssetPolyCount, record[2])
                    break

            if self.selectedAssetPolyCount >= int(float(self.data[-1][1]) * 1000):
                self.selectedAssetLODMessage = fmt.format('Overspending', self.selectedAssetPolyCount, self.data[-1][2])

            self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.black)

        if len(self.data):
            self._paintDashBoard(painter)
        else:
            self._paintTipMessage(painter)
