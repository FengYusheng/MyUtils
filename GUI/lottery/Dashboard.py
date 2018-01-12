# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Utils

class Dashboard(QWidget):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAutoFillBackground(True)

        self.parent = parent
        self.pen = QPen(QBrush(Qt.darkGray), 3, Qt.SolidLine, Qt.RoundCap, Qt.BevelJoin)
        self.font = QFont()
        # https://stackoverflow.com/questions/17819698/how-to-change-fontsize-on-drawtext#17819878
        self.font.setPointSize(20)
        self.text = '你的名字！'
        self.playerGenerator = self.parent.playerGenerator()


    def setText(self):
        # https://stackoverflow.com/questions/1756096/understanding-generators-in-python
        self.text = next(self.playerGenerator).strip()
        self.update()


    def showPrizewinners(self, winners):
        self.text = list(winners)
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.white)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width()*3/7, self.height()/2)
        painter.setPen(self.pen)
        painter.setFont(self.font)

        if isinstance(self.text, str):
            painter.drawText(0, 0, self.text)
        elif isinstance(self.text, list):
            length = len(self.text)
            h = 0 - int(length/2)*self.font.pointSize()
            painter.save()
            painter.translate(0, h)

            for index, winner in enumerate(self.text):
                height = index * self.font.pointSize() * 1.5
                painter.drawText(0, height, winner)

            painter.restore()
            
        painter.restore()


    def paintMatrixCodeRain(self):
        pass


    def currentPlayer(self):
        return self.text
