# -*- coding: utf-8 -*-
import re

import pymel.core as pm

def checkShaderNames(prototypes=[], *args, **kwargs):
    shaders = pm.ls(materials=True)
    shaders.remove('particleCloud1')
    shaders.remove('lambert1')

    if len(shaders):
        for prototype in prototypes:
            prototype = prototype[0]
            prototype = prototype.replace('<SHADER>', '.*?').replace('#', '\d')
            prototype = re.compile(prototype)
            map(lambda s : re.match(prototype, s.name()) is None or shaders.remove(s), shaders[:])

    return [s.name() for s in shaders]
