# -*- coding: utf-8 -*-

import pymel.core as pm


def bevelOnHardEdges(**kwargs):
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


if __name__ == '__main__':
    bevelOnHardEdges()
