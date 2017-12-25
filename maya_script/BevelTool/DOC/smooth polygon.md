# Smooth Methods
## Smooth a mesh by adding new polygon
`Mesh->Smooth` modifies the polygon mesh by adding new polygons and smoothing out
vertices and their connected edges.

The maximum division level is 5.

`polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 1 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 pCylinder1;`

Smooth out: make something smooth by the removal of lines and creases.

>http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-C4442D89-990B-4302-AF60-E21FCA22D4F3

**When to use**
1. when the final model is complete and ready to be sent down the pipeline.
2. When you absolutely require the versatility of working with the highres mesh.

**Limitation**
Add divisions to the mesh, increasing the polyon count.

## Smooth Mesh Preview
Smooth Mesh Preview lets you quickly and easyly see how your mesh will appear when
smoothed.

If you render a mesh while Smooth Mesh Preview is enabled, it will apprear in its
original un-smoothed state in the final image. If you want the mesh to appear in
a smoothed way in a rendering, see "Convert a smooth mesh preview to polygons"
and "Subdiv Proxy Options".

Smooth Mesh Preview use the OpenSubdiv Catmull-clark subdivision method.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-4863E5AE-0EA0-4596-B1AE-10C19603838E

`displaySmoothness` in "C:/Program Files/Autodesk/Maya2017/scripts/others/setDisplaySmoothness.mel"

### Preview a smoothed mesh
Press Page Up or Page Down to change the level of smoothing/subdivision that occurs
on the smoothed preview.

Alternatively, you can go to the Attribute Editor for any mesh's polyShape node
and turn on Smooth Mesh Preview in the Smooth Mesh section.

The range of "division level(smoothing/subdivision level)" is from 0 to 4.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-BF4C21CB-C149-449F-925D-5456B1D96EB7

### Convert a smooth mesh preview to polygons
Maya copies the Smooth Mesh Preview attributes to a new polySmooth node.

>http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-C27982A5-9F7E-45FF-B362-A3DE7129EE13

### Display subdivisions on a smooth mesh preview
Displaying subdivisions can help pinpoint exactly what a mesh will look like at
varying degrees of smoothness.

Dotted lines represent subdivisions.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-AC93F593-1578-4237-AB65-CA90615A627E

**When to use**
1. In most cases you will want use a smooth mesh preview to see the effects of
a smooth operation.

2. When you want to make changes to a smooth mesh by modifying its less complicated
un-smoothed counterpart.

**Limitation**
1. Can't be smoothed linearly.
2. Coomplicated mirror setup.
3. Can't colide with particles

## Subdiv Proxy
The Subdiv Proxy method smooths the selected mesh by adding polygons and placing the
original non-smoothed mesh(the proxy).

Unlike the smoothed preview, the subdiv proxy version of the mesh is fully renderable
an can be skinned and weighted for animation. A subdiv proxy also lets you work
with meshed in a mirrored fashion. You can modify the original mesh on one half
of an object and see the changes reflected on the opposite, smoothed half of the model.

By default, subdiv proxy uses the OpenSubdiv Catmull-Clark subdivision method.

*When you render the model, both the proxy and smoothed mesh will appear.*

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-196DCBDA-4A3D-4D48-904F-D38D8267E07E

Command:

    SmoothProxy;
    performSmoothProxy 0;
    duplicate -rc  pCube1 ;

### Create a subdiv proxy
Unlike `Mesh->Smooth`, you can't use subdiv proxy on specific faces.

You can use Edit Mesh->Bevel on the proxy mesh to control the shape fo the smooth
mesh at a corner.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-DBB39F66-FC4B-4577-94DF-2BA0D61AFDBD

### Control the visibility of the subdiv proxy
To control the proxy and the smoothed mesh visibility using Layer Editor, turn on
the following options:
  * Subdiv Proxy In Layer
  * Smooth Mesh In Layer

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-500DD142-1F88-4D83-9EC3-7ED58B4D19C1

### Mirror a polygonal mesh with subdiv proxy
> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-16C8CED5-8776-40E2-85B1-0A2D22EC2A31

### Best practices for subdiv proxy meshes
* In most cases you should only edit the proxy mesh.
* You can move the proxy mesh, but don't rotate the proxy mesh.
* `Mesh->Combine` and `Mesh->Booleans` can't be performed on a proxy mesh. These
operations create new surfaces and can break the connection between the proxy and
smooth meshes.
* Keep the proxy and smooth meshes connected througout an animation.
* Keep "Subdivision Level" low while modeling, and then increase it just before
rendering. `setAttr polySmoothFaceX.divisions Y;`

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-5CFE8D1C-6C28-4562-9A25-EBEE5397D673

### Troubleshoot subdiv proxy
This part tells you how to edit the smoothed mesh directly.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-8D112D65-3F31-4793-B3DD-47F4BEADFDDB

### Creasse components on a sbudiv proxy
`Mesh->Smooth Proxy->Crease Tool`

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-2D66DED7-FF91-442E-B22E-BC1F08603609

**When to use**
1. When you need to perform a linear smooth.
2. When you want to want to see the effect of particle collision on your smoothed
object, prior to smoothing.
3. If you want to perform a mirrored smooth(though this can be recreated in a smooth
  mesh preview with a few extra steps).

**Limitation**
Increase polygon count

## Smooth by averaging distance between vertices
The Average Vertices(`Edit Mesh->Average Vertices`) command smooths your mesh while
*maintaining its polygon count*. It averages the  values of existing vertices to produce
a smoother surface without modifying the current topology.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-7DA6670A-625B-4734-864F-16821910D062

`polyAverageVertex -i 10 -ch 1 pCube1;`

Move the selected vertices of a polygonal object to round its shape. Translate
, move, rotate or scale vertices.

> `polyAverageVertex` command reference

**When to use**
1. When under a strict poly count restriction.
2. When you want to massage an area with a lot of spikes or dips.

**Limitation**
Less versatility since only existing vertices can be used.

## Subdivision Surface
A subdivision surface lets subdivide *specific regions of a mesh*, giving you the
ability to finely *tune or smooth certain areas without changing the entire mesh*.

Subdivision surfaces only insert control points where you need them instead of uniformly
across the entire mesh.

Subdivision surfaces are largely unsupported in pipelines outside of Maya, so you
need to convert them to polygons or NURBS , `Modify->Convert Subdiv to Polygons`
or `Modify->Convert Subdiv to NURBS`.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-4D290125-7A5C-47D9-A698-00449056F089

**When to use**
1. When modeling objects are not going to be rigged.
2. When modeling with the intention of converting to NURBS.

**Limitation**
1. Slowest performance.
2. No external pipeline support.

# OpenSubdiv
As a professional standard in the animation industry, OpenSubdiv is implemented
in a variety of software packages, improving interoperability by producing the
same results when models are transferred between applications.

In Maya, OpenSubdiv is the default subdivision method when you preview a smoothed
mesh, smooth a mesh using `Mesh->Smooth`, or create a subdiv proxy.

OpenSubdiv is an improved alternative to the legacy May Catmull-Clark subdivision
method.

Two OpenSubdiv subdivision methods:
1. OpenSubdiv Catmull-Clark Uniform: Applies a uniform refinement scheme to the faces
of a mesh. *The entire mesh receives the same leve of subdivision*.

2. OpenSubdiv Catmull-Clark Adaptive: Applies a progressive refinement scheme to
irregular parts of your mesh. Adaptive subdivision only refines the mesh topology
where additional detail is needed. Adaptive subdivision lets increase the smoothness
of your mesh without increasing its subdivision level.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-909B2D5F-D031-4372-B2D7-7D8BCCBE3183

## Preview a smoothed mesh with OpenSubdiv
*Edit global preferences in `Preference Editor`.* In the Attribute Editor, select
the polyShape tab, open the Smooth Mesh panel, and then disable the Use global
subdivision method option. you can set the Subdivision Method on a per-object overriding
the global preference.

> OpenSubdiv Controls: http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-FF35F773-1FC0-4EBA-A64C-6199375F489A#GUID-FF35F773-1FC0-4EBA-A64C-6199375F489A__SECTION_AEC2592F09DA47ACBB9901F1310E01E9

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-909B2D5F-D031-4372-B2D7-7D8BCCBE3183

## OpenSubdiv limitations
### OpenSubdiv General limitations
OpenSubdiv doesn't support.

### OpenSubdiv Catmull-Clark Adaptive limitations
* Depth of field.
* Use Default Material.
* Depth peeling.
* Plug-in shader implemented with MPxShaderOverrride.

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-FD9DCF96-6914-4BB4-A665-A817A4DE2521

# polySmooth Node
These attributes can be found under the Smooth Mesh section on the polyShape node for the mesh.

## Subdivision Algorithm
1. Maya Catmull-Clark
2. OpenSubdiv Catmull-Clark
3. OpenSubdiv Catmull-Clark Adaptive

## Subdivision Levels
### Preview Division Levels
Control the number of times the original version of the mesh is subdivided. The
slider range is between 0 and 4, but you can input values higher than 4 in the text
field.

> *Smooth Mesh Render*: http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-86E8A2A3-2685-4230-9097-D6F2EE880910

## OpenSubdiv Controls
### Vertex Boundary
Control how boundary edges and corner vertices are interpolated.
1. Sharp edges and corners.
2. Sharp edges.

### UV Boundary Smoothing
Control how smoothing is applied to boundary UVs.

1. None, UVs aren't smoothed.
2. Preserve edges and corners, edges and corners remain sharp after smoothing.
3. Preserve edges, only edges remain sharp after smoothing.
4. Maya Catmull-Clark, smooth face-varying data(UVs and colors sets) near vertices
that aren't on a discontinuous boundary.

### Crease Method
Control how creases are smoothed during subdivision.

`polySmooth` opiton, osdCreaseMethod

> polySmooth command reference

1. Normal, no smoothing is applied to creases.
2. Chaikin, this method improves the appearance of *multi-edge creases with different
edge weights.*

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-FF35F773-1FC0-4EBA-A64C-6199375F489A#GUID-FF35F773-1FC0-4EBA-A64C-6199375F489A__SECTION_AEC2592F09DA47ACBB9901F1310E01E9

# Options
## Smooth Options

> http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-4D094DC4-9027-4422-9083-6C9D2FE4036E
