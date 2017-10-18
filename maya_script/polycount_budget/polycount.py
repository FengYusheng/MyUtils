# -*- coding: utf-8 -*-

import os
import sys
import json
from collections import deque
from collections import namedtuple

import pymel.core as pm
import maya.api.OpenMaya as om # Python API 2.0

"""
https://www.highend3d.com/maya/script/polyscatter-spread-objects-across-a-surface-for-maya
"""


def printHierarchy(hierarchy={}):
    print json.dumps(hierarchy, indent=4, encoding='utf-8', sort_keys=True)


def savePolyCountGroupByContainer(hierarchy={}):
    _ = pm.system.sceneName().rpartition('.')[0] + '.json'
    with open(_, 'w') as desination:
        json.dump(hierarchy, desination, encoding='utf-8', indent=4)


def _createtContainerNode():
    return {'container':'', 'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0, 'surface area':0, 'children':{}, 'parent':'None'}


def _buildHierarchy(scenePolyCount, stack, **shape):
    root             = None
    parent           = None
    currentContainer = None
    for containerName in stack:
        if root is None:
            containerName in scenePolyCount['hierarchy'].keys() or scenePolyCount['hierarchy'].setdefault(containerName, _createtContainerNode())
            currentContainer = scenePolyCount['hierarchy'][containerName]
            root = containerName
        else:
            containerName in parent['children'].keys() or parent['children'].setdefault(containerName, _createtContainerNode())
            currentContainer = parent['children'][containerName]

        currentContainer['container']    = containerName
        currentContainer['parent']       = parent['container'] if parent else parent
        currentContainer['Verts']        += shape['Verts']
        currentContainer['Edges']        += shape['Edges']
        currentContainer['Faces']        += shape['Faces']
        currentContainer['UVs']          += shape['UVs']
        currentContainer['Tris']         += shape['Tris']
        currentContainer['surface area'] += shape['surface area']

        parent = currentContainer


def getPolyCountUsingPymel():
    polyCount = {}
    Verts = Edges = Faces = UVs = Tris = 0
    if pm.system.sceneName():
        for shape in pm.ls(type='mesh', noIntermediate=True):
            instanceCount = len(shape.getAllPaths())
            Verts += shape.numVertices()                                             * instanceCount
            Edges += shape.numEdges()                                                * instanceCount
            Faces += shape.numFaces()                                                * instanceCount
            UVs   += shape.numUVs()                                                  * instanceCount
            Tris  += int(pm.mel.eval('polyEvaluate -triangle {0}'.format(shape))[0]) * instanceCount

    polyCount['Verts'] = Verts
    polyCount['Edges'] = Edges
    polyCount['Faces'] = Faces
    polyCount['UVs']   = UVs
    polyCount['Tris']  = Tris

    return polyCount


def getContainerStackUsingPymel(container=None):
    '''
    Container path
    '''
    container_stack = deque()
    while isinstance(container, pm.nt.Container) \
          or isinstance(container, pm.nt.DagContainer):
               container_stack.appendleft(container.name())
               parent = pm.container(container, query=True, parentContainer=True)
               container = parent[0] if parent else None
               if container is not None:
                   pm.mel.eval('select -r {0}'.format(container))
                   container = pm.ls(selection=True)[0]

    pm.select(cl=True)
    return container_stack


def getPoyCountGroupByContainerUsingPymel2():
    scenePolyCount = {'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0, 'surface area':0, 'hierarchy':{}}
    Verts = Edges = Faces = UVs = Tris = 0
    if pm.system.sceneName():
        for shape in pm.ls(type='mesh', noIntermediate=True):
            instanceCount = len(shape.getAllPaths())
            Verts         = shape.numVertices()                                                    * instanceCount
            Edges         = shape.numEdges()                                                       * instanceCount
            Faces         = shape.numFaces()                                                       * instanceCount
            UVs           = shape.numUVs()                                                         * instanceCount
            Tris          = int(pm.mel.eval('polyEvaluate -triangle {0}'.format(shape.name()))[0]) * instanceCount
            surfaceArea   = pm.polyEvaluate(shape, wa=True)

            scenePolyCount['Verts']        += Verts
            scenePolyCount['Edges']        += Edges
            scenePolyCount['Faces']        += Faces
            scenePolyCount['UVs']          += UVs
            scenePolyCount['Tris']         += Tris
            scenePolyCount['surface area'] += int(surfaceArea)

            container = pm.container(shape, query=True, findContainer=shape.name())
            if container is not None:
                containerStack = getContainerStackUsingPymel(container)
                _buildHierarchy(scenePolyCount, containerStack, **{'container':container.name(), 'Verts':Verts, 'Edges':Edges, 'Faces':Faces, 'UVs':UVs, 'Tris':Tris, 'surface area': int(surfaceArea)})

    return scenePolyCount


def getModelingSurfaceAreaUsingPymel():
    surfaceArea = 0
    if pm.system.sceneName():
        surfaceArea = sum((pm.polyEvaluate(shape, wa=True) for shape in pm.ls(type='mesh', noIntermediate=True)))
        surfaceArea = int(surfaceArea)

    return surfaceArea


def getPolyCountGroupByContainer():
    scenePolyCount = getPoyCountGroupByContainerUsingPymel2()
    savePolyCountGroupByContainer(scenePolyCount)


def maya_useNewAPI():
    """ Use Maya Python API 2.0 """
    pass


def getPolyCountUsingMayaAPI():
    """ Use Maya Python API 2.0 """
    meshIterator = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    meshNodeFn   = om.MFnMesh()
    # fmt = '{0} : {1}'
    Verts = Edges = Faces = Tris = UVs = 0
    polyCountTuple = namedtuple('polyCountTuple', ['Verts', 'Edges', 'Faces', 'Tris', 'UVs'])
    while not meshIterator.isDone():
        meshNode = meshIterator.currentItem()
        meshNodeFn.setObject(meshNode)

        if not meshNodeFn.isIntermediateObject:
            # om.MFnDagNode.instanceCount() documentation says: If indirect is True then the instancing of ancestor
            # nodes further up the DAG path is included, otherwise only the immediate instancing of this node is counted.
            # Here I choice True because om.MFnDagNode.isInstanced(indirect=True)
            # print fmt.format(meshNodeFn.name(), meshNodeFn.instanceCount(True))
            instanceNumber  = meshNodeFn.instanceCount(True)
            Verts          += meshNodeFn.numVertices
            Edges          += meshNodeFn.numEdges
            Faces          += meshNodeFn.numPolygons
            UVs            += meshNodeFn.numUVs()
            Tris           += sum(meshNodeFn.getTriangles()[0])

        meshIterator.next()

    return polyCountTuple(Verts, Edges, Faces, Tris, UVs)


def getPolyCountByDagPathUsingMayaAPI():
    meshIterator   = om.MItDag(om.MItDag.kDepthFirst, om.MItDag.kMesh)
    meshFn         = om.MFnMesh()
    polyCountTuple = namedtuple('polyCountTuple', ['Verts', 'Edges', 'Faces', 'Tris', 'UVs'])
    Verts = Edges = Faces = Tris = UVs = 0
    while not meshIterator.isDone():
        meshNode = meshIterator.currentItem()
        meshFn.setObject(meshNode)
        instanceNumber = meshIterator.getPath().instanceNumber()

        Verts += meshFn.numVertices            * instanceNumber
        Edges += meshFn.numEdges               * instanceNumber
        Faces += meshFn.numPolygons            * instanceNumber
        UVs   += meshFn.numUVs()               * instanceNumber
        Tris  += int(meshFn.getTriangles()[0]) * instanceNumber

        meshIterator.next()

    return polyCountTuple(Verts, Edges, Faces, Tris, UVs)



if __name__ == '__main__':
    # scenePolyCount = getPoyCountGroupByContainerUsingPymel2()
    # printHierarchy(scenePolyCount)
    # savePolyCountGroupByContainer(scenePolyCount)
    print getPolyCountUsingMayaAPI()
