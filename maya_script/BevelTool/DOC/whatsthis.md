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

*You must select one method to use throughout your workflow, as the methods
can't be used interchangeably on the same components.*

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

*Subdivision surfaces* have the slowest performance of the three smoothing
methods. Subdivision surfaces are largely unsupported in pipelines outside
of Maya, so you need to convert them to polygons or NURBS before exporting
to these pipelines.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-4D290125-7A5C-47D9-A698-00449056F089

## Commands support undo

`MayaUndoChunk` in "C:\\Program Files\\Autodesk\\Maya2017\\Python\\Lib\\site-packages\\maya\\app\\general\\creaseSetEditor.py"


## What is a partition node?
This node defines a collection of objectSet nodes which are exclusive of each
other with respect to membership. That is, no member of an objectSet which is
in a partition will also be a member of another objectSet if that objectSet is
also in the same partition.

The renderPartition defines the collection of shading groups which define which
objects should be rendered. If an object or part of an object is not in a shading
group, it will not be rendered.

> partition node reference

### What is a objectSet?
This node defines a logical collection of objects, object components, and node
attributes. Sets are used to which parts of an object to deform. Sets are used
to define which objects should have the same shading properties and are called
shading groups or renderable sets. Anything that can be selected using `select`
command can be added to an ojectSet. An objetSet is created and edited using the
`sets` command.

Objects may be connected to a partition. Mutual exclusivity is maintained by the
`sets` and `partition` commands. The shading groups are connected to the renderPartition.

> objectSet node reference

A set is a logical  grouping of an arbitrary collection of objects, attributes,
or components of objects. Sets are dependency nodes. Connections from objects
to a set define membership in the set.

**Sets are used throughout Maya in a multitude of ways. They are used to define
an association of material properties to objects, to define an association of lights
to objects, to define a bookmark or named collection of objects, to define a character,
and to define the components to be deformed by some deformation operation.**

Sets can be connected to **any number of partitions.** A partition is a node which
enforces mutual exclusivity among the sets in the partition.

Sets can be associated color which is only of use when creating vertex sets. The
color can be one of the eight user defined colors defined in the color preferences.
This color can be used, for example to distinguish which vertices are being deformed
by a particular deformation.

> `set` command reference

## What're the meaning of "subdivide the mesh" and subdivision level?
`polySmooth`, this command works on polygon objects or faces.

### What is an edge hardness?
I guess it is helpful:
> polySoftEdge node reference

### What is preview division level(smoothLevel attribute in a mesh node)?
