# Sets and Partitions in Maya
## Sets
A set is a collection of *objects of components.* Any item you can select can be
in a set. The set exists as a separate node. *Unlike groups, sets do not alter the
hierarchy of the scene.* They are always saved at the scene level, and can't be part
of an object, group, or hierarchy.

There are two different types of custom sets: sets and quick select sets. Both of
them can contain selected objects, components, or groups, but a quick select set
can't be added to a partition.

Sets are useful for the following:
* Simplifying the selection of objects or components that you regularly select,
have difficulty selecting in the view panel, or are nested in hierarchies so they're
difficult to access easily.
* Assigning objects to shading groups for rendering.
* Moving objects from one layer to another.
* Adjusting deformer, skin, and flexor deformation.
* Adjusting the weight of cluster, cluster flexor, and skin points.
* Working with shading groups.

## Partitions
A partition is a collection of related sets. Maya creates partitions to keep character
sets, shading groups, skin point sets, and exclusive deformers from having overlapping
members.

## Reference
> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-B1DE4646-E52B-4611-87B6-E741F25E284B
