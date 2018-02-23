# Intermediate Node
http://discourse.techart.online/t/maya-missing-geo/2358


## Command
    setAttr "pCubeShape1.overrideEnabled" 1;
    setAttr "pCubeShape1.overrideDisplayType" 2;
    setAttr "polySurfaceShape1.intermediateObject" 0;
    setAttr "polySurfaceShape1.overrideEnabled" 1;
    setAttr "polySurfaceShape1.overrideTexturing" 0;
    select -add polySurfaceShape1.e[7] ;
    select -r polySurfaceShape1.e[6] ;
    polyBevel3 -fraction 0.5 -offsetAsFraction 1 -autoFit 1 -depth 1 -mitering 0 -miterAlong 0 -chamfer 1 -segments 1 -worldSpace 1 -smoothingAngle 30 -subdivideNgons 1 -mergeVertices 1 -mergeVertexTolerance 0.0001 -miteringAngle 180 -angleTolerance 180 -ch 1 polySurfaceShape1.e[6];
    // polyBevel2 //
    setAttr "polySurfaceShape1.intermediateObject" 1;
    select -cl  ;
    setAttr "polySurfaceShape2.intermediateObject" 0;
    disconnectAttr polyBevel1.output pCubeShape1.inMesh;
    // Disconnect polyBevel1.output from pCubeShape1.inMesh. //
    disconnectAttr polyBevel2.output polyBevel1.inputPolymesh;
    // Disconnect polyBevel2.output from polyBevel1.inputPolymesh. //
    connectAttr -f polyBevel2.output pCubeShape1.inMesh;
    // Connected polyBevel2.output to pCubeShape1.inMesh. //
    connectAttr -f polyBevel1.output polyBevel2.inputPolymesh;
    // Connected polyBevel1.output to polyBevel2.inputPolymesh. //
    // Warning: Can't perform polyBevel2 on selection //
    connectAttr -f polySurfaceShape2.outMesh polyBevel1.inputPolymesh;
    // Connected polySurfaceShape2.outMesh to polyBevel1.inputPolymesh. //
    setAttr "polySurfaceShape2.intermediateObject" 1;
    setAttr "pCubeShape1.overrideEnabled" 0;


## Construction history
As you work in Maya, most of your actions create nodes in **construction
history** of the objects you work on. At each point in your work, the current
 scene is the result of all the nodes you've created so far.

Construction history is part of the dependency graph in Maya. While  
construction history refers to the *history* of actions that created the
scene, the entire dependency graph refers to all *connections(input and
output)* between nodes.

Some common uses of the construction history:
1. Edit the transform attributes of a node in the attribute editor or channel box.
2. Change dependency relationships between node attributes in the Hypergraph or Node Editor.
3. Make some nodes inactive while you focus on editing others.
4. Delete all or part of the construction history of an object or an animation to **bake** it in the current state. Doing so can reduce a scene's recalculation time and file size, but it can also change object appearance by simplifying a sequence of operations.
