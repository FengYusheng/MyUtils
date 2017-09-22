# -*- coding: utf-8 -*-

import os
import sys
import json
from collections import deque

import pymel.core as pm

"""
https://www.highend3d.com/maya/script/polyscatter-spread-objects-across-a-surface-for-maya
"""



ZERO = {'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0, 'children':{}}


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


def getPoyCountGroupByContainerUsingPymel():
    polyCount = {}
    Verts = Edges = Faces = UVs = Tris = 0
    if pm.system.sceneName():
        for shape in pm.ls(type='mesh', noIntermediate=True):
            instanceCount = len(shape.getAllPaths())
            container = pm.container(shape, query=True, findContainer=shape.name())
            print getContainerStackUsingPymel(container)
            if container is not None:
                container = container.name()
                polyCount.setdefault(container, {'Verts':0, 'Edges':0, 'Faces':0, 'UVs':0, 'Tris':0})
                polyCount[container]['Verts'] += shape.numVertices()                                             * instanceCount
                polyCount[container]['Edges'] += shape.numEdges()                                                * instanceCount
                polyCount[container]['Faces'] += shape.numFaces()                                                * instanceCount
                polyCount[container]['UVs']   += shape.numUVs()                                                  * instanceCount
                polyCount[container]['Tris']  += int(pm.mel.eval('polyEvaluate -triangle {0}'.format(shape))[0]) * instanceCount

            Verts += shape.numVertices()                                             * instanceCount
            Edges += shape.numEdges()                                                * instanceCount
            Faces += shape.numFaces()                                                * instanceCount
            UVs   += shape.numUVs()                                                  * instanceCount
            Tris  += int(pm.mel.eval('polyEvaluate -triangle {0}'.format(shape))[0]) * instanceCount

    return polyCount


def getContainerStackUsingPymel(container=None):
    container_stack = deque()
    while isinstance(container, pm.nt.Container) \
          or isinstance(container, pm.nt.DagContainer):
               container_stack.appendleft(container)
               parent = pm.container(container, query=True, parentContainer=True)
               container = parent[0] if parent else None
               if container is not None:
                   pm.mel.eval('select -r {0}'.format(container))
                   container = pm.ls(selection=True)[0]

    pm.select(cl=True)
    return container_stack


def buildContanierHierarchyFromStack(container_stack):
    container_hierarchy = {}
    if len(container_stack):
        for container in container_stack:
            container_hierarchy.setdefault(container.name(), ZERO)
    else:
        print('buildContanierHierarchyFromStack')



if __name__ == '__main__':
    polyCount = getPoyCountGroupByContainerUsingPymel()
