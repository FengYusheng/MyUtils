# -*- coding: utf-8 -*-
import json

import pymel.core as pm

import polycount
import checkShader



def printCheckResult(result={}):
    print json.dumps(result, indent=4, encoding='utf-8', sort_keys=True)


def saveCheckReuslt(result={}):
    if pm.system.sceneName():
        _ = pm.system.sceneName().rpartition('.')[0] + '.json'
        with open(_, 'w') as destination:
            json.dump(result, destination, indent=4, encoding='utf-8')


def checkAsset(checkers=[], **kwargs):
    result = {}
    if 'check transformations' in checkers:
        pass

    if 'check n-gons' in checkers:
        pass

    if 'check lamina faces' in checkers:
        pass

    if 'check overlapping vertices' in checkers:
        pass

    if 'check external files' in checkers:
        pass

    if 'check shader names' in checkers:
        result['check shader names'] = checkShader.checkShaderNames(kwargs['check shader names'])

    if 'check poly count' in checkers:
        result['check poly count'] = polycount.getPoyCountGroupByContainerUsingPymel2()

    saveCheckReuslt(result)
    printCheckResult(result)

    return result
