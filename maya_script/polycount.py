# -*- coding: utf-8 -*-

import os
import sys
import json
from collections import deque

import pymel.core as pm

"""
https://www.highend3d.com/maya/script/polyscatter-spread-objects-across-a-surface-for-maya
"""


def printHierarchy(hierarchy={}):
    print json.dumps(hierarchy, indent=4, encoding='utf-8', sort_keys=True)


def _createtContainerNode():
    return {'container':'', 'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0, 'children':{}, 'parent':'None'}


def _buildHierarchy(scenePolyCount, stack, shape):
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

        currentContainer['container'] = containerName
        currentContainer['parent']    = parent['container'] if parent else parent
        currentContainer['Verts']     += shape['Verts']
        currentContainer['Edges']     += shape['Edges']
        currentContainer['Faces']     += shape['Faces']
        currentContainer['UVs']       += shape['UVs']
        currentContainer['Tris']      += shape['Tris']
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
    print(polyCount)


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
    scenePolyCount = {'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0, 'hierarchy':{}}
    Verts = Edges = Faces = UVs = Tris = 0
    if pm.system.sceneName():
        for shape in pm.ls(type='mesh', noIntermediate=True):
            instanceCount = len(shape.getAllPaths())
            Verts = shape.numVertices()                                                    * instanceCount
            Edges = shape.numEdges()                                                       * instanceCount
            Faces = shape.numFaces()                                                       * instanceCount
            UVs   = shape.numUVs()                                                         * instanceCount
            Tris  = int(pm.mel.eval('polyEvaluate -triangle {0}'.format(shape.name()))[0]) * instanceCount

            scenePolyCount['Verts'] += Verts
            scenePolyCount['Edges'] += Edges
            scenePolyCount['Faces'] += Faces
            scenePolyCount['UVs']   += UVs
            scenePolyCount['Tris']  += Tris

            container = pm.container(shape, query=True, findContainer=shape.name())
            if container is not None:
                containerStack = getContainerStackUsingPymel(container)
                _buildHierarchy(scenePolyCount, containerStack, {'container':container.name(), 'Verts':Verts, 'Edges':Edges, 'Faces':Faces, 'UVs':UVs, 'Tris':Tris})

    return scenePolyCount



if __name__ == '__main__':
    scenePolyCount = getPoyCountGroupByContainerUsingPymel2()
    printHierarchy(scenePolyCount)
