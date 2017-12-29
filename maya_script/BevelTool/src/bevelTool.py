# -*- coding: utf-8 -*-

import pymel.core as pm

import utils
reload(utils)
import options



def bevelOnHardEdges(*args, **kwargs):
    duplications = []
    resultPolyBevelNodes = []
    meshTransformNodes = [i for i in pm.ls(sl=True) if isinstance(i, pm.nt.DagNode) and hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]
    with utils.MayaUndoChuck('bevelOnHardEdges'):
        for meshTransform in meshTransformNodes:
            dup = pm.duplicate(meshTransform, st=True, rr=True)[0]
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



def bevelOnSelectedEdges(*args, **kwargs):
    selectedMeshEdges = pm.filterExpand(sm=32, ex=True)
    if selectedMeshEdges:
        with utils.MayaUndoChuck('bevelOnSelectedEdges'):
            bevelNode = pm.polyBevel3(
                selectedMeshEdges,
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

            bevelNode[0].setName('bevelOnSelectedEdges#')



if __name__ == '__main__':
    # bevelOnHardEdges()
    bevelOnSelectedEdges(**options.bevelOptions)
