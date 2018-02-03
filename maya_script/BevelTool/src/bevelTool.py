# -*- coding: utf-8 -*-
import copy

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



def bevelOnSelectedEdges( *args, **kwargs):
    dupMeshTransform = None
    edges, bevelSetName = args
    selectedMeshEdges = edges if len(edges) else pm.filterExpand(sm=32, ex=True)

    # Duplicate the mesh node.
    originMesh = pm.ls(selectedMeshEdges[0].name().partition('.')[0], type='mesh')[0]
    dupMeshTransform = utils.duplicateMeshTransform(bevelSetName)
    if len(dupMeshTransform):
        edgeIndices = utils.selectedEdgeindices(selectedMeshEdges)
        edges = [dupMeshTransform[0].e[i] for i in edgeIndices]

    if len(edges):
        with utils.MayaUndoChuck('bevelOnSelectedEdges'):
            bevelNode = pm.polyBevel3(
                edges,
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

            bevelNode[0].setName('MWBevelOn'+bevelSetName+'#')

    return dupMeshTransform



def MWBevelOption(bevelSetName, bevelOption):
    value = ''
    polyBevel3Node = pm.ls('MWBevel_'+bevelSetName, type='polyBevel3')
    if 'Fraction' == bevelOption:
        value = polyBevel3Node[0].fraction.get()
    elif 'Input Components' == bevelOption:
        value = polyBevel3Node[0].inputComponents.get() # Result: [u'e[0:39]', u'e[56]']
    elif 'Segments' == bevelOption:
        value = polyBevel3Node[0].segments.get()
    elif 'Mitering' == bevelOption:
        value = polyBevel3Node[0].mitering.get()
    elif 'Miter Along' == bevelOption:
        value = polyBevel3Node[0].miterAlong.get()
    elif 'Chamfer' == bevelOption:
        value = polyBevel3Node[0].chamfer.get()

    return value



def setMWBevelOption(bevelSetName, bevelOption, value):
    polyBevel3Node = pm.ls('MWBevel_'+bevelSetName, type='polyBevel3')
    if 'Fraction' == bevelOption:
        polyBevel3Node[0].fraction.set(value)
    elif 'Segments' == bevelOption:
        polyBevel3Node[0].segments.set(value)
    elif 'Mitering' == bevelOption:
        polyBevel3Node[0].mitering.set(value)
    elif 'Miter Along' == bevelOption:
        polyBevel3Node[0].miterAlong.set(value)
    elif 'Chamfer' == bevelOption:
        polyBevel3Node[0].chamfer.set(value)



def bevelMembers(bevelSetName):
    polyBevel3Info = []
    _bevelSetName = bevelSetName
    meshName = _bevelSetName.rpartition('MWBevelSet_')[0]
    num = int(bevelSetName.rpartition('MWBevelSet_')[2])
    polyBevel3Node = pm.ls('MWBevel_'+_bevelSetName, type='polyBevel3')
    while len(polyBevel3Node):
        edgeIndices = MWBevelOption(_bevelSetName, 'Input Components')
        members = [pm.ls(meshName+'.'+e)[0] for e in edgeIndices]
        bevelOptions = [MWBevelOption(_bevelSetName, i) for i in options.SIMPLEOPTIONS]
        polyBevel3Info.append({'Bevel':_bevelSetName, 'members':members, 'options':bevelOptions})

        num += 1
        _bevelSetName = meshName + 'MWBevelSet_' + str(num)
        polyBevel3Node = pm.ls('MWBevel_'+_bevelSetName, type='polyBevel3')

    return polyBevel3Info





def bevelOnSelectedBevelSet(bevelSetName, *args, **kwargs):
    members = utils.bevelSetMembers(bevelSetName)
    if len(members):
        meshObject = utils.getMeshObject(members)
        bevelOptions = kwargs

        with utils.MayaUndoChuck('MWBevel'):
            bevelNode = pm.polyBevel3(
                members,
                fraction=bevelOptions['fraction'],
                offsetAsFraction=bevelOptions['offsetAsFraction'],
                autoFit=bevelOptions['autoFit'],
                depth=bevelOptions['depth'],
                mitering=bevelOptions['mitering'],
                miterAlong=bevelOptions['miterAlong'],
                chamfer=bevelOptions['chamfer'],
                segments=bevelOptions['segments'],
                worldSpace=bevelOptions['worldSpace'],
                smoothingAngle=bevelOptions['smoothingAngle'],
                subdivideNgons=bevelOptions['subdivideNgons'],
                mergeVertices=bevelOptions['mergeVertices'],
                mergeVertexTolerance=bevelOptions['mergeVertexTolerance'],
                miteringAngle=bevelOptions['miteringAngle'],
                angleTolerance=bevelOptions['angleTolerance'],
                forceParallel=bevelOptions['forceParallel'],
                ch=bevelOptions['ch']
            )

            if bevelSetName.rpartition('_')[1] == '_':
                bevelNode[0].setName('MWBevel_'+bevelSetName)
            else:
                bevelNode[0].setName('MWBevel_'+bevelSetName+'_#')
                pm.ls(bevelSetName, type='objectSet')[0].rename(bevelNode[0].name().partition('MWBevel_')[2])



if __name__ == '__main__':
    bevelMembers('pCylinderShape1MWBevelSet_1')
