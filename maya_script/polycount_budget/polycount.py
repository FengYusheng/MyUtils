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
    meshIterator = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    meshNodeFn   = om.MFnMesh()
    Verts = Edges = Faces = Tris = UVs = 0
    polyCountTuple = namedtuple('polyCountTuple', ['Verts', 'Edges', 'Faces', 'Tris', 'UVs'])
    while not meshIterator.isDone():
        meshNode = meshIterator.currentItem()
        meshNodeFn.setObject(meshNode)

        if not meshNodeFn.isIntermediateObject:
            # om.MFnDagNode.instanceCount() documentation says: If indirect is True then the instancing of ancestor
            # nodes further up the DAG path is included, otherwise only the immediate instancing of this node is counted.
            # Here I choice True because om.MFnDagNode.isInstanced(indirect=True)
            instanceNumber  = meshNodeFn.instanceCount(True)

            # This kind of iterator doesn't need instance number.
            Verts          += meshNodeFn.numVertices
            Edges          += meshNodeFn.numEdges
            Faces          += meshNodeFn.numPolygons
            UVs            += meshNodeFn.numUVs()
            Tris           += sum(meshNodeFn.getTriangles()[0])

        meshIterator.next()

    return polyCountTuple(Verts, Edges, Faces, Tris, UVs)


def getContainerStacksUsingMayaAPI():
    def _getPolyCountInContainer(containerNodeFn):
        containerData = _createtContainerNode()
        meshNodeFn = om.MFnMesh()
        containerData['container'] = containerNodeFn.name()
        for _ in (node for node in containerNodeFn.getMembers() if node.hasFn(om.MFn.kMesh)):
            meshNodeFn.setObject(_)
            if not meshNodeFn.isIntermediateObject:
                containerData['Verts'] += meshNodeFn.numVertices
                containerData['Edges'] += meshNodeFn.numEdges
                containerData['Faces'] += meshNodeFn.numPolygons
                containerData['UVs']   += meshNodeFn.numUVs()
                containerData['Tris']  += sum(meshNodeFn.getTriangles()[0])

        return containerData


    def _getDagContainers(containerNodeFn):
        dagNodeFn = om.MFnDagNode()
        dagContainers = deque()
        dagContainers.append(containerNodeFn.name())
        for _ in (node for node in containerNodeFn.getMembers() if node.hasFn(om.MFn.kDagContainer)):
            dagNodeFn.setObject(_)
            dagContainers.append(dagNodeFn.name())

        return dagContainers


    containerNodeIterator = om.MItDependencyNodes(om.MFn.kContainer)
    containerNodeFn = om.MFnContainerNode()
    meshNodeFn = om.MFnMesh()
    containerStacks = []
    dagContainersInContainers = []
    while not containerNodeIterator.isDone():
        stack = deque()
        containerNodeFn.setObject(containerNodeIterator.thisNode())
        dagContainersInContainers.append(_getDagContainers(containerNodeFn))
        stack.append(_getPolyCountInContainer(containerNodeFn))
        parent = containerNodeFn.getParentContainer()
        while not parent.isNull():
            containerNodeFn.setObject(parent)
            stack.append(_getPolyCountInContainer(containerNodeFn))
            parent = containerNodeFn.getParentContainer()

        containerStacks.append(stack)
        containerNodeIterator.next()

    return containerStacks, dagContainersInContainers


def getDagContainerStacksUsingMayaAPI():
    # TODO: om.MFn.kContainerBase indicates the object either a container or a dagContainer.
    def _getPolyCountInDagContainer(node):
        meshFn = om.MFnMesh()
        dagNodeFn = om.MFnDagNode(node)
        containerData = _createtContainerNode()
        containerData['container'] = dagNodeFn.name()
        if node.hasFn(om.MFn.kMesh):
            meshFn.setObject(node)
            if not meshFn.isIntermediateObject:
                containerData['Verts'] = meshFn.numVertices
                containerData['Edges'] = meshFn.numEdges
                containerData['Faces'] = meshFn.numPolygons
                containerData['UVs']   = meshFn.numUVs()
                containerData['Tris']  = sum(meshFn.getTriangles()[0])

        return containerData


    def _addPolyCountIntoDagContainer(meshNodeData, dagContainer):
        dagContainer['Verts'] += meshNodeData['Verts']
        dagContainer['Edges'] += meshNodeData['Edges']
        dagContainer['Faces'] += meshNodeData['Faces']
        dagContainer['Tris']  += meshNodeData['Tris']
        dagContainer['UVs']   += meshNodeData['UVs']

    # MItDependencyNodes may miss some mesh nodes in the scene.
    # meshIterator = om.MItDependencyNodes(om.MFn.kMesh)
    meshIterator = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    dagNodeFn = om.MFnDagNode()
    dagContainerStacks = []
    while not meshIterator.isDone():
        stack = deque()
        path = dagNodeFn.setObject(meshIterator.currentItem()).getPath()
        meshNodeData = _getPolyCountInDagContainer(path.node())
        path.pop()
        while path.length():
            node = path.node()
            not node.hasFn(om.MFn.kDagContainer) or stack.append(_getPolyCountInDagContainer(node))
            path.pop()

        if len(stack):
            _addPolyCountIntoDagContainer(meshNodeData, stack[0])
            dagContainerStacks.append(stack)

        meshIterator.next()

    return dagContainerStacks


def _buildHierarchyUsingMayaAPI(containerStacks=[]):
    scenePolyCount = {'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0, 'surface area':0, 'hierarchy':{}}
    meshNodeFn = om.MFnMesh()
    if len(containerStacks):
        for stack in containerStacks:
            root    = None
            parent  = None
            #containerStacks[0]: ['street']
            #containerStacks[1]: ['Geometry_CNT', 'street']
            #containerStacks[2]: ['road_CNT', 'Geometry_CNT, 'street']
            #So only stack[0] isn't in the hierarchy in each loop.
            newCome = stack[0]
            for container in reversed(stack):
                containerName = container['container']

                if root is None:
                    containerName in scenePolyCount['hierarchy'].keys() or scenePolyCount['hierarchy'].setdefault(containerName, _createtContainerNode())
                    root = containerName
                    currentContainer = scenePolyCount['hierarchy'][root]
                else:
                    containerName in parent['children'].keys() or parent['children'].setdefault(containerName, _createtContainerNode())
                    currentContainer = parent['children'][containerName]

                currentContainer['Verts'] += newCome['Verts']
                currentContainer['Edges'] += newCome['Edges']
                currentContainer['Faces'] += newCome['Faces']
                currentContainer['Tris']  += newCome['Tris']
                currentContainer['UVs']   += newCome['UVs']

                parent = currentContainer

    return scenePolyCount


def getPolyCountGroupByContainerUsingMayaAPI():
    # Get polycount from container nodes.
    def _mergeTwoContainerStacks(dagContainersInContainers, dagContainerStacks, containerStacks):
        for dagContainerStack in dagContainerStacks:
            for container in dagContainersInContainers:
                if dagContainerStack[-1]['container'] in container:
                    containerHead = _createtContainerNode()
                    containerHead['container'] = container[0]
                    dagContainerStack.append(containerHead)
                    break

        return containerStacks + dagContainerStacks


    containerStacks, dagContainersInContainers = getContainerStacksUsingMayaAPI()
    dagContainerStacks = getDagContainerStacksUsingMayaAPI()
    totalStacks = _mergeTwoContainerStacks(dagContainersInContainers, dagContainerStacks, containerStacks)
    polyCountInScene = _buildHierarchyUsingMayaAPI(totalStacks)

    return polyCountInScene



if __name__ == '__main__':
    ret = getPolyCountGroupByContainerUsingMayaAPI()
    printHierarchy(ret)
