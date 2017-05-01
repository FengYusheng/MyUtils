# -*- coding: utf-8 -*-

import sys
import pymel.core as pm



# print node[1].rx.get()
# print node[1].ry.get()
# print node[1].rz.get()


# pm.mel.eval(u'nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 1; objectMoveCommand;')
def normalChecker():
    pm.mel.eval(u'polyPlane -n normalChecker -w 1 -h 1 -sx 10 -sy 10 -ax 0 1 0 -cuv 2 -ch 1;')
    checker = pm.ls(regex='normalChecker')
    if len(checker) > 1:
        print(u'An object called nomralChecker has existed.')
        return None

    checker = checker[0]
    faces = checker.f[1:]
    for face in faces:
        pm.delete(face)

    pm.xform(cpc=True)
    return checker

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


if __name__ == '__main__':
    flipped_face = []
    nodes = pm.ls(selection=True)
    checker = normalChecker()
    if checker is None:
        sys.exit()

    checker_normal = checker.f[0].getNormal(space='transform').normal()

    for node in nodes:
        tmp = getConnectedVertices(node)
        tmp = getVerticesPositions(node, tmp)
        for face in tmp:
            checker.vtx[1].setPosition(face[1][0], space='world')
            checker.vtx[3].setPosition(face[1][1], space='world')
            checker.vtx[2].setPosition(face[1][2], space='world')
            checker.vtx[0].setPosition(face[1][3], space='world')
            pm.xform(cpc=True)

            # face_normal = face[0].getNormal().normal()
            face_normal = checker.f[0].getNormal(space='transform').normal()

            if checker_normal.cotan(face_normal) < 0:
                flipped_face.append(face[0])

    pm.select(flipped_face)
