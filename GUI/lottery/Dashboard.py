# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Dashboard(QWidget):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAutoFillBackground(True)

        self.pen = QPen(QBrush(Qt.darkGray), 3, Qt.SolidLine, Qt.RoundCap, Qt.BevelJoin)
        self.font = QFont()
        # https://stackoverflow.com/questions/17819698/how-to-change-fontsize-on-drawtext#17819878
        self.font.setPointSize(20)
        self.text = '你的名字！'


    def setText(self, text):
        self.text = text
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

        painter.drawText(0, 0, self.text)
        painter.restore()
