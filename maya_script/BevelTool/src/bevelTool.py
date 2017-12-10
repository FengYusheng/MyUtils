# -*- coding: utf-8 -*-

import pymel.core as pm


def bevelOnHardEdges(*args, **kwargs):
    objects = pm.ls(sl=True)
    mesh = [obj.getShape() for obj in objects] if objects else None
    if mesh:
        # Select all the hard edges.
        pm.polySelectConstraint(disable=True, m=3, t=0x8000, sm=1)
        hardEdges = pm.ls(sl=True)
        pm.polySelectConstraint(disable=True)
        # Bevel:
        # polyBevel3 -fraction 0.5 -offsetAsFraction 1 -autoFit 1 -depth 1 \
        # -mitering 0 -miterAlong 0 -chamfer 1 -segments 1 -worldSpace 1 \
        # -smoothingAngle 30 -subdivideNgons 1 -mergeVertices 1 -mergeVertexTolerance 0.0001 \
        # -miteringAngle 180 -angleTolerance 180 -ch 1 pCube3;
        # http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-A1C5EC72-AD48-4A7D-8577-1823B3832E14
        #  C:\Program Files\Autodesk\Maya2018\scripts\others\performBevelOrChamfer.mel
        not hardEdges or pm.polyBevel3(
            objects,
            fraction=0.5,
            offsetAsFraction=True,
            autoFit=True,
            depth=1,
            mitering=0,
            miterAlong=0,
            chamfer=False,
            segments=1,
            worldSpace=True,
            smoothingAngle=30,
            subdivideNgons=True,
            mergeVertices=True,
            mergeVertexTolerance=0.0001,
            miteringAngle=180,
            angleTolerance=180,
            forceParallel=True,
            ch=True
        )


if __name__ == '__main__':
    bevelOnHardEdges()
