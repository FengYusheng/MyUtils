# -*- coding: utf-8 -*-
import pymel.core as pm



def checkTransformations():
    result = set()
    cameras = pm.listCameras()
    cameras = cameras if cameras else []
    transforms = pm.ls(type='transform')
    transforms = [t for t in transforms if t not in cameras] if transforms else []
    center = pm.dt.Vector([0.0, 0.0, 0.0])
    for t in transforms:
        pivots = t.getPivots(worldSpace=True)
        tx = t.tx.get()
        ty = t.ty.get()
        tz = t.tz.get()
        rx = t.rx.get()
        ry = t.ry.get()
        rz = t.rz.get()
        sx = t.sx.get()
        sy = t.sy.get()
        sz = t.sz.get()

        if pivots[0] != center \
        or pivots[1] != center \
        or tx != 0.0           \
        or ty != 0.0           \
        or tz != 0.0           \
        or rx != 0.0           \
        or rz != 0.0           \
        or sx != 0.0           \
        or sy != 0.0           \
        or sz != 0.0:

            result.add(t.name())

    return list(result)


def checkNGons():
    result = {}
    shapes = pm.ls(type='mesh')
    pm.select(shapes, r=True)
    pm.polySelectConstraint(disable=True, m=3, t=8, sz=3)
    ngons = pm.ls(sl=True)
    pm.polySelectConstraint(disable=True)
    pm.select(cl=True)
    for n in ngons:
        k = n.name().rpartition('.')[0]
        result.setdefault(k, []).append(n.name())

    return result


def checkLaminaFaces():
    result = {}
    shapes = pm.ls(type='mesh')
    pm.select(shapes, r=True)
    pm.polySelectConstraint(disable=True, m=3, t=8, tp=2)
    laminas = pm.ls(sl=True)
    pm.polySelectConstraint(disable=True)
    pm.select(cl=True)
    for l in laminas:
        k = l.name().rpartition('.')[0]
        result.setdefault(k, []).append(l.name())

    return result


def checkOverlappingVertices():
    result = {}
    shapes = pm.ls(type='mesh')
    for shape in shapes:
        verts = set(shape.vtx)
        while verts:
            vert = verts.pop()
            position = vert.getPosition()
            pm.select(shape, r=True)
            pm.polySelectConstraint(disable=True, m=3, t=1, d=1, db=(0.0, 0.01), dp=position)
            _overlappingVerts = pm.ls(sl=True)
            verts.difference_update(set(_overlappingVerts))
            _overlappingVerts = [v.name() for v in _overlappingVerts]
            pm.polySelectConstraint(disable=True)
            not len(_overlappingVerts) > 1 or result.setdefault(shape.name(), []).append(reduce(lambda x,y:x+', '+y, _overlappingVerts))

    return result


def checkExternalfilePath():
    files = pm.ls(type='file')
    files = files if files else []
    scenePath = pm.system.sceneName()
    scenePath = None if '' == scenePath else scenePath.dirname()
    for f in files[:]:
        path = f.fileTextureName.get().rpartition('/')[0]
        scenePath not in path or files.remove(f)

    return [f.name()+' : '+f.fileTextureName.get() for f in files]
