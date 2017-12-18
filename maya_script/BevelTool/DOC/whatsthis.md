## soft edges definition
An edge is the place where two different colors, textures or values
meet. Edges may be characterized in a variety of ways. Soft edges blend
together, making it difficult to distinguish where texture/color/value
stops and another begins.
[[1]](http://www.creativeglossary.com/art-mediums/soft-edges.html).

1. [Hard Edges and Soft Edges](https://www.thoughtco.com/hard-edges-and-soft-edges-2577590)

2. [maya的软硬边](http://hkcgart.com/zhidao/detail/id/899777.html)

## `polyBevel` options

## Selecting

### Selection Mode
>http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-E3DBC099-2E93-47F3-B7FA-A219DB72B4A7


## mel2py

## How do I import mel procedure?

## Crease
>http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-DEB060F9-A4B1-4F73-8B4D-B18A13D0E54B

The higher the crease value, the sharper the crease.

Maya offers two methods to crease edges and vertices on a polygon mesh:
1. The Crease Tool.

    `polyCrease`

    The crease values range between 0 and 7. 7 indicates the component is
    fully creased.

2. The Crease Set Editor.

*You must select one method to use throughout your workflow, as the methods can't
be used interchangeably on the same components.*

### What's the meaning of a crease value?
A crease value of 2 means that the base level and first level edges are
fully creased, but finer level edges are not creased at all.

The crease values are used by the smoothing algorithm.
> polyCrease command reference

A creaseSet is a special kind of set that contains the edges and vertices
that share the same subdivision surface creasing value. A crease level is
used with subdivision surfaces. The value is the maximum subd level that  
the edge or vertex is creased before it starts smoothing.
> creaseSet node reference

### Subdivision Surface.
