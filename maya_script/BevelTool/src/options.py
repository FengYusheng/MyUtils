# -*- coding: utf-8 -*-
from collections import (defaultdict, OrderedDict, deque)

"""
polyBevel3 -fraction 0.5 -offsetAsFraction 1 -autoFit 1 -depth 1 -mitering 0
            -miterAlong 0 -chamfer 0 -segments 1 -worldSpace 1 -smoothingAngle 30
            -subdivideNgons 1 -mergeVertices 1 -mergeVertexTolerance 0.0001
            3-miteringAngle 180 -angleTolerance 180 -ch 1 pCylinder2.e[0:39];
"""


bevelOptions = {
    'fraction'             : 0.5,
    'offsetAsFraction'     : True,
    'autoFit'              : True,
    'depth'                : 1,
    'mitering'             : 0,
    'miterAlong'           : 0,
    'chamfer'              : False,
    'segments'             : 1,
    'worldSpace'           : True,
    'smoothingAngle'       : 30,
    'subdivideNgons'       : True,
    'mergeVertices'        : True,
    'mergeVertexTolerance' : 0.0001,
    'miteringAngle'        : 180,
    'angleTolerance'       : 180,
    'forceParallel'        : True,
    'ch'                   : True,
    'instance'             : False
}


BOOLOPTIONS = ('offsetAsFraction', 'autoFit', 'chamfer', 'worldSpace', 'subdivideNgons', 'mergeVertices', 'forceParallel', 'ch')


SIMPLEOPTIONS = (
    'Fraction',
    'Segments',
    'Mitering' ,
    'Miter Along',
    'Chamfer'
)


FULLOPTIONS = (
    'fraction',
    'offsetAsFraction',
    'autoFit',
    'depth',
    'mitering',
    'miterAlong',
    'chamfer',
    'segments',
    'worldSpace',
    'smoothingAngle',
    'subdivideNgons',
    'mergeVertices',
    'mergeVertexTolerance',
    'miteringAngle',
    'angleTolerance',
    'forceParallel',
    'ch'
)


MITERING = ('Auto', 'Uniform', 'Patch', 'Radial', 'None')
MITERALONG = ('Auto', 'Center', 'Edge', 'Hard Edge')
CHAMFER = ('off', 'on')

TREEVIEWHEADERS = OrderedDict(
    sorted(
        {
            'Bevel Set'   : 0,
            'Fraction'    : 1,
            'Segments'    : 2,
            'Mitering'    : 3,
            'Miter Along' : 4,
            'Chamfer'     : 5
        }.items(),

        key = lambda t : t[1]
    )
)


drawOverredeAttributes = defaultdict(lambda: ' ')

disableSelectionCallback = deque()

isVertexFace = deque()
