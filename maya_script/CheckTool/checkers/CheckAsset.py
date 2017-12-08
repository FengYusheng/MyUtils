# -*- coding: utf-8 -*-
import json

import pymel.core as pm

import polycount
import checkShader
import checkMesh
reload(checkMesh)



def printCheckResult(result={}):
    print json.dumps(result, indent=4, encoding='utf-8', sort_keys=True)


def saveCheckReuslt(result={}):
    if pm.system.sceneName():
        _ = pm.system.sceneName().rpartition('.')[0] + '.json'
        with open(_, 'w') as destination:
            json.dump(result, destination, indent=4, encoding='utf-8')


def checkAsset(checkers=[], progressCallback=None, **kwargs):
    result = {}
    if 'check transformations' in checkers:
        result['check transformations'] = checkMesh.checkTransformations(progressCallback)

    if 'check n-gons' in checkers:
        result['check n-gons'] = checkMesh.checkNGons(progressCallback)

    if 'check lamina faces' in checkers:
        result['check lamina faces'] = checkMesh.checkLaminaFaces(progressCallback)

    if 'check overlapping vertices' in checkers:
        result['check overlapping vertices'] = checkMesh.checkOverlappingVertices(progressCallback)

    if 'check external files' in checkers:
        result['check external files'] = checkMesh.checkExternalfilePath(progressCallback)

    if 'check shader names' in checkers:
        result['check shader names'] = checkShader.checkShaderNames(kwargs['check shader names'], progressCallback)

    if 'check poly count' in checkers:
        result['check poly count'] = polycount.getPoyCountGroupByContainerUsingPymel2(progressCallback)

    saveCheckReuslt(result)
    printCheckResult(result)

    return result
