# -*- coding: utf-8 -*-
import pymel.core as pm

import utils
reload(utils)
import options



def MWBevelOption(bevelSetName, bevelOption):
    value = ''
    polyBevel3Node = pm.ls('MWBevel_'+bevelSetName, type='polyBevel3')
    if len(polyBevel3Node):
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
    if len(polyBevel3Node):
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



def getInputComponent(bevelNodeName):
    bevelNode = pm.ls(bevelNodeName, type='polyBevel3')
    print bevelNode[0].inputComponents.get()



def bevelOnSelectedBevelSet(bevelSetName, *args, **kwargs):
    members = utils.bevelSetMembers(bevelSetName)
    if len(members):
        meshObject = utils.getMeshObject(members)
        bevelSet = pm.ls(bevelSetName, type='objectSet')
        bevelOptions = kwargs

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
            bevelSet[0].rename(bevelNode[0].name().partition('MWBevel_')[2])

        utils.disconnectFromMWBevelSet(bevelSet[0].name(), meshObject)
        utils.lockBevelSet(bevelSet, True)



def bevelSelectedEdges(*args, **kwargs):
    edgeIndices, mesh, MWBevelSetName = args
    bevelOptions = kwargs
    MWBevelName = MWBevelSetName + '_Bevel_' + mesh
    MWBevelNode = pm.ls(MWBevelName, type='polyBevel3')
    mesh = pm.ls(mesh,type='mesh')
    edges = [mesh[0].e[i] for i in edgeIndices]
    0 == len(MWBevelNode) or pm.delete(MWBevelNode)
    MWBevelNode = pm.polyBevel3(
        edges,
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

    MWBevelNode[0].rename(MWBevelName)



if __name__ == '__main__':
    getInputComponent('polyBevel1')
    getInputComponent('polyBevel2')
