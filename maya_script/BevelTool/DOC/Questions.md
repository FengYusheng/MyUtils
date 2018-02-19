## Qt

### Event handlers
Are these handlers static methods?

    `def _mousePressEventInBevelOptionslabel(self, event):
        isVisible = not self.bevelOptionsGroupBox.isVisible()
        self.bevelOptionsGroupBox.setVisible(isVisible)
        QLabel.mousePressEvent(self.bevelOptionsLabel, event)`


### List widgets in tree QTreeView

     `def paint(self, painter, option, index):
         parentIndex = self.parent.dataModelInControlPanelTreeView.parent(index)
         if parentIndex.row() >= 0:
             bevelsetPanel = MWBevelToolPanels.MWBevelSetPanel(self.parent)
             groupBoxOption = QStyleOptionGroupBox()
             groupBoxOption.activeSubControls = QStyle.SC_All
             self.parent.toolbarGroupBox.initStyleOption(groupBoxOption)
             groupBoxOption.rect = option.rect
             groupBoxOption.rect.setHeight(bevelsetPanel.height())
             groupBoxOption.styleObject = bevelsetPanel
             QApplication.style().drawComplexControl(QStyle.CC_GroupBox, groupBoxOption, painter, bevelsetPanel)
         else:
             QStyledItemDelegate.paint(self, painter, option, index)`


## Python

### `Super()`


## Maya Command

1. `maya.cmds.displayRGBColor`, this command changes or queries the display color
for anything in the application that allows the user to set its color.

2. Get Maya main window in Maya python api 2.0.

3. `print pm.optionVar['polySoftEdge']`

4. Edit undo list.

## Private work
1. Reverse link list: reverse the bevel nodes of a mesh in Maya.
