# -*- coding: utf-8 -*-

import os
import csv

import pymel.core as pm



def findInconsistentFaceNormal():
    inconsistentFaceNormals = []
    for mesh in pm.ls(type='mesh', noIntermediate=True):
        duplicatedMesh = pm.duplicate(mesh.name(), rr=True)[0]
        pm.polySoftEdge(duplicatedMesh, a=180, ch=False)
        for vert in duplicatedMesh.getShape().vtx:
            normals = vert.getNormals()
            if len([n for n in normals[1:] if n != normals[0]]):
                inconsistentFaceNormals.append((mesh.name(), vert.connectedFaces().name()))
                break

        pm.delete(duplicatedMesh)

    return inconsistentFaceNormals


if __name__ == '__main__':
    print findInconsistentFaceNormal()
