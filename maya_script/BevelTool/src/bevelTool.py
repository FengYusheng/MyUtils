# -*- coding: utf-8 -*-

import pymel.core as pm

import utils


def bevelOnHardEdges(*args, **kwargs):
    duplications = []
    resultPolyBevelNodes = []
    # TODO: call filterExpand to get mesh dag nodes. Or
    # All selected mesh meshShapes
    # maya.cmds.ls(dag=True, sl=True, noIntermediate=True, type='mesh')
    # maya.cmds.ls(items, dag=True, noIntermediate=True, type='mesh')
    # Reference: getSelectedMeshComponents() in C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py
    # maya.cmds.objectType(mesh, isAType='transform') in C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py:463
    polygons = [i for i in pm.ls(sl=True) if isinstance(i, pm.nt.DagNode) and hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]
    for polygon in polygons:
        dup = pm.duplicate(polygon, st=True, rr=True)[0]
        duplications.append(dup)
        pm.move(25.0, 0.0, 0.0, dup, r=True)
        if pm.mel.eval('exists doMenuComponentSelection'):
            try:
                pm.mel.eval('doMenuComponentSelection("{0}", "edge")'.format(dup.name()))
            except pm.MelError:
                pass
        else:
            utils.switchSelectionModeToEdge(dup)

        pm.select(dup.e, r=True)
        pm.polySelectConstraint(disable=True, m=2, t=0x8000, sm=1)
        hardEdges = pm.ls(sl=True)
        not len(hardEdges) or resultPolyBevelNodes.append(
            pm.polyBevel3(
                hardEdges,
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
            )
        )

    pm.polySelectConstraint(disable=True)
    pm.select(duplications, r=True)
    return resultPolyBevelNodes


if __name__ == '__main__':
    bevelOnHardEdges()
