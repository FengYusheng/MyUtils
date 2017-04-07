# -*- coding: utf-8 -*-

import pymel.core as pm

def xAxisMirrorDup():
    transforms = pm.ls(selection=True)
    if len(transforms) > 0:
        group1 = pm.group(transforms, name='group1')
        group1.setPivots(pm.dt.Vector([0.0, 0.0, 0.0]), worldSpace=True)
        group2 = pm.duplicate('group1', name='group2')[0]
        scaleX, scaleY, scaleZ = group2.getScale()
        group2.setScale((0-scaleX, scaleY, scaleZ))
    else:
        print('You need to select objects first.')

if __name__ == '__main__':
    xAxisMirrorDup()
