# -*- coding: utf-8 -*-

from collections import Counter
import pymel.core as pm

def getConnectedVertices(node):
    """Get all the vertices of a face

    Reference:
        # pymel bug: https://github.com/LumaPictures/pymel/issues/367
        # for face in faces:
        #     a = face.connectedVertices()

    Param:
        pm.Transform

    Return:
        list: vertices indices of a face
    """
    if not isinstance(node, pm.nt.Transform):
        print(u'You must pass a pm.nt.Transform')
        return None

    return [(face,face.getVertices()) for face in node.f]

def getVerticesPositions(node, indices = []):
    if 0 == len(indices) \
        or not isinstance(node, pm.nt.Transform):
        print(u'indices - list, node - pm.nt.Transform')
        return None

    return [(a[0],[node.vtx[b].getPosition(space='world') for b in a[1]]) for a in indices]

def getUVs(node, indices = []):
    if 0 == len(indices) \
        or not isinstance(node, pm.nt.Transform):
        print(u'indices - list, node - pm.nt.Transform')
        return None

    return [(a[0],[a[0].getUV(b) for b in a[1]]) for a in indices]

def findInvertedFaceNormal():
    objects = pm.ls(selection=True)
    if 0 == len(objects):
        print(u'You must select an object first.')
        return False

    connectedVertices = []
    for node in objects:
        if not isinstance(node, pm.nt.Transform):
            continue

        tmp = getConnectedVertices(node)
        tmp = getVerticesPositions(node, tmp)
        for face in tmp:
            # print face
            u = face[1][1] - face[1][0]
            v = face[1][3] - face[1][0]
            normal1 = u.cross(v).normal()

            face_normal = face[0].getNormal(space='world').normal()
            print repr(normal1), repr(face_normal)
            print normal1.isEquivalent(face_normal, tol=0.01)
            #  3
            #4    2
            #  1
            # After reverse:
            #  3
            #2   4
            #  1
            # 对于四边形面 normal 是(face[1][0] -face[1][1]).cross(face[1][0] - face[1][2])
            # reverse_normal是(face[1][0] - face[1][3]).cross(face[1][0] - face[1][3])
            # 对于三角形面 normal 是(face[1][0] - face[1][1]).cross(face[1][0] - face[1][2])
            # reverse_normal是(face[1][0] - face[1][2]).cross(face[1][0] - face[1][1])

    # print pm.ls('volumeLight1')
    return True

if __name__ == '__main__':
    findInvertedFaceNormal()
