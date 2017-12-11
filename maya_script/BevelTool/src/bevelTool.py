# -*- coding: utf-8 -*-

import pymel.core as pm

import options
reload(options)

def bevelOnHardEdges(*args, **kwargs):
    objects = [i for i in pm.ls(sl=True) if isinstance(i, pm.nt.DagNode) and hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]
    if objects:
        dups = pm.duplicate(objects, st=True, rr=True) if not kwargs['instance'] else pm.instance(objects, st=True)
        pm.move(25.0, 0.0, 0.0, dups, r=True)
        # Select all the hard edges.
        pm.polySelectConstraint(disable=True, m=3, t=0x8000, sm=1)
        hardEdges = pm.ls(sl=True)
        pm.polySelectConstraint(disable=True)

        # polyBevel3 -fraction 0.5 -offsetAsFraction 1 -autoFit 1 -depth 1 \
        # -mitering 0 -miterAlong 0 -chamfer 1 -segments 1 -worldSpace 1 \
        # -smoothingAngle 30 -subdivideNgons 1 -mergeVertices 1 -mergeVertexTolerance 0.0001 \
        # -miteringAngle 180 -angleTolerance 180 -ch 1 pCube3;
        # http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-A1C5EC72-AD48-4A7D-8577-1823B3832E14
        #  C:\Program Files\Autodesk\Maya2018\scripts\others\performBevelOrChamfer.mel

        not hardEdges or map(lambda _ : pm.polyBevel3(
            _,
            fraction=kwargs['fraction'],
            offsetAsFraction=kwargs['offsetAsFraction'],
            autoFit=kwargs['autoFit'],
            depth=kwargs['depth'],
            mitering=kwargs['mitering'],
            miterAlong=kwargs['miterAlong'],
            chamfer=kwargs['chamfer'],
            segments=kwargs['segments'],
            worldSpace=kwargs['worldSpace'],
            smoothingAngle=kwargs['smoothingAngle'],
            subdivideNgons=kwargs['subdivideNgons'],
            mergeVertices=kwargs['mergeVertices'],
            mergeVertexTolerance=kwargs['mergeVertexTolerance'],
            miteringAngle=kwargs['miteringAngle'],
            angleTolerance=kwargs['angleTolerance'],
            forceParallel=kwargs['forceParallel'],
            ch=kwargs['ch']
        ), dups)

        pm.select(dups, r=True)



if __name__ == '__main__':
    bevelOnHardEdges()
