# -*- coding: utf-8 -*-
import copy
import functools

import pymel.core as pm

import utils
reload(utils)
import options



def disableActiveSelectionListCallbackDecorator():
    def decorate(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            options.disableCallback.append(func.__name__)
            func(*args, **kwargs)
            options.disableCallback.pop()

        return decorator
    return decorate




def MWBevelOption(MWBevelSetName, bevelOption):
    value = ''
    polyBevel3Node = [i for i in pm.ls(type='polyBevel3') if i.name().startswith(MWBevelSetName+'_Bevel_')]
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



def getBevelOptionsFromBevelSet(MWBevelSetName):
    bevelOptions = copy.copy(options.bevelOptions)
    MWBevelNode = [i for i in pm.ls(type='polyBevel3') if i.name().startswith(MWBevelSetName+'_Bevel_')]
    if len(MWBevelNode):
        bevelOptions['fraction'] = MWBevelNode[0].fraction.get()
        bevelOptions['segments'] = MWBevelNode[0].segments.get()
        bevelOptions['mitering'] = MWBevelNode[0].mitering.get()
        bevelOptions['miterAlong'] = MWBevelNode[0].miterAlong.get()
        bevelOptions['chamfer'] = MWBevelNode[0].chamfer.get()

    return bevelOptions



def setMWBevelOption(MWBevelSetName, bevelOption, value):
    for MWBevelNode in (i for i in pm.ls(type='polyBevel3') if i.name().startswith(MWBevelSetName+'_Bevel_')):
        if 'Fraction' == bevelOption:
            MWBevelNode.fraction.set(value)
        elif 'Segments' == bevelOption:
            MWBevelNode.segments.set(value)
        elif 'Mitering' == bevelOption:
            MWBevelNode.mitering.set(value)
        elif 'Miter Along' == bevelOption:
            MWBevelNode.miterAlong.set(value)
        elif 'Chamfer' == bevelOption:
            MWBevelNode.chamfer.set(value)



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


@disableActiveSelectionListCallbackDecorator()
def bevelSelectedEdges(*args, **kwargs):
    edgeIndices, mesh, MWBevelSetName = args
    edgeIndices = list(set(edgeIndices))
    bevelOptions = kwargs
    MWBevelName = MWBevelSetName + '_Bevel_' + mesh
    MWBevelNode = list(set([i for i in pm.listConnections(mesh, type='polyBevel3') if i.name().startswith('MWBevelSet')]))
    mesh = pm.ls(mesh,type='mesh')
    edges = list([mesh[0].e[i] for i in edgeIndices])
    len(MWBevelNode) > 0 and pm.delete(MWBevelNode)

    pm.select(cl=True) # Clear the active selection list in case both intermediate and origin mesh are selected.

    if len(edges):
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
