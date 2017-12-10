# -*- coding: utf-8 -*-
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

import bevelTool
import ui_MainWindowForBevelTool
reload(ui_MainWindowForBevelTool)


class MainWindowForBevelTool(QMainWindow, ui_MainWindowForBevelTool.Ui_MainWindowForBevelTool):
    def __init__(self, parent=None):
        super(MainWindowForBevelTool, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.dataModelInOptionTableView = QStandardItemModel(self.optionTableView)
        self.optionTableView.setModel(self.dataModelInOptionTableView)
        self.selectionModelInOptionTableView = QItemSelectionModel(self.dataModelInOptionTableView, self.optionTableView)
        self.optionTableView.setSelection(self.selectionModelInOptionTableView)

        self._insertDefaultOptions()


    def _insertDefaultOptions():
        pass



if __name__ == '__main__':
    window = MainWindowForBevelTool()
    window.show()
