# Smoothing Angle

## `polySoftEdge` Node
An edge is hard if the angle between two owning facets is **sharper(larger)**
 than the smoothing angle. An edge is soft if the angle between two owning
 facets is flatter(smaller) than the smoothing angle.

 Smoothing angle. An angle value greater than "angle", means that the edges
 are *rendered hard*; otherwise, they are *rendered soft*.

> http://download.autodesk.com/us/maya/2011help/CommandsPython/polySoftEdge.html

## Smoothing angle in bevel option
Lets you specify whether you want the beveled edges to be hard or soft when
shaded. If you want the beveled edges to be soft, set the **Smoothing Angle**
 to a high value(180). If you want the beveled edges to be hard, set the
 **Smoothing Angle** to a low value(0).
 In general, if the angle between two shared edges is greater than the value
 specified by the Smoothing Angle attribute, the beveled edge will be shaded
 to appear hard.

> https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2015/ENU/Maya/files/GUID-40E32F44-1EB9-4DC6-8EE4-6A013EEC626F-htm.html

## `polySoftEdge` command

## `polyOptions` command
Change the global display polygonal attributes.

## Command Refernce

    PolygonSoftenHarden;
    performPolySoftEdge 0;
    polyPerformAction "polySoftEdge -a 30" e 0;
    // polyPerformAction "polySoftEdge -a 30" e 0 //
    whatIs PolygonSoftenHarden;
    // Result: Run Time Command //
    whatIs performPolySoftEdge;
    // Result: Mel procedure found in: C:/Program Files/Autodesk/Maya2018/scripts/others/performPolySoftEdge.mel //
    optionVar -query polySoftEdge;
    // Result: 30 //

`nodeType`, this command returns a string which identifies the given node's type.
