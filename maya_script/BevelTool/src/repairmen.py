# -*- coding: utf-8 -*-
import functools

import pymel.core as pm
from pymel.all import mayautils

import utils
import options



def disableSelecitonEventCallback(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        options.disableIntermediate.append(func.__name__)
        ret = func(*args, **kwargs)
        options.disableIntermediate.pop()
        return ret
    return decorator



def runOnLater(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        mayautils.executeDeferred(func, *args, **kwargs)
    return decorator



@disableSelecitonEventCallback
def repairman():
    origin = options.drawOverredeAttributes['mesh']
    intermediate = options.drawOverredeAttributes['ioMesh']

    if intermediate != ' ':
        meshTrans = utils.getTransform(origin)
        # unhilite operation doesn't trigger any selection callback.
        # TODO: it seems that unhilite operation works only in deferred mode.
        pm.hilite(meshTrans, u=True)
        if options.isVertexFace[origin]:
            MWBevelSetName = [i.name() for i in pm.listSets(object=intermediate) if i.name().startswith('MWBevelSet')]
            members = [i for i in utils.bevelSetMembers(MWBevelSetName[0]) if i.name().rpartition('.e')[0] == intermediate ]
            indices = [int(i.name().rpartition('[')[2].rpartition(']')[0]) for i in members]
            mesh = pm.ls(origin, type='mesh')[0]
            edges = [mesh.e[i] for i in indices]
            utils.removeEdgesFromBevelSet(members)
            utils.restoreDrawOverrideAttributes()
            pm.delete(meshTrans, ch=True)
            utils.displayIOMesh(meshTrans)
            utils.addEdgesIntoBevelSet(MWBevelSetName[0], edges)
            del options.isVertexFace[origin]



@disableSelecitonEventCallback
def repairman2():
    activeMesh = (options.drawOverredeAttributes['mesh'], options.drawOverredeAttributes['ioMesh'])
    inactiveTransforms = [utils.getTransform(m) for m in pm.ls(dag=True, hilite=True, ni=True, type='mesh') if m.name() not in activeMesh]
    if activeMesh[0] !=' ' \
        and len(inactiveTransforms) > 0 \
        and utils.isSelectionTypeEdge():

        pm.hilite(inactiveTransforms, u=True)
        pm.warning("You are editing {0}. If you want to edite another object, left click it first.".format(activeMesh[0]))



@runOnLater
def repairman3():
    if options.drawOverredeAttributes['ioMesh'] != ' ':
        meshTrans = getTransform(options.drawOverredeAttributes['mesh'])
        pm.hilite(meshTrans, u=True)
