# Specify the display color of a mesh object in Maya

## `palettePort`
This command creates an array of color cells. It could be used to store some colors
you want to manage during your working session.

* `dimensions(dim)`, set the dimensions of the array.
* `editable(ed)`, if true then the user can change the current color.
* `rgbValue(rgb)`, set a color for a given cell, using RGB format. On query return
the color of the current cell.
* `setCurCell(scc)`, set the current cell in the array to the given index. Return
the current cell when queried.

## `colorIndex`
The index specifies a color index in the color palette. The r, g and b values
(between 0-1) specify the RGB values (or the HSV values if the -hsv flag is used)
for the color.


## Reference
1. http://zurbrigg.com/maya-scripts/display-color-override
