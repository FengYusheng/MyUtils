# -*- coding: utf-8 -*-

checkers = [
    'check n-gons',
    'check lamina faces',
    'check transformations',
    'check overlapping vertices',
    'check external files',
    'check shader names',
    'check poly count'
]

detail = [
    'check shader names',
    'check poly count'
]

whatsThis = {
    'check n-gons' : 'No g-gons should exist.',
    'check lamina faces' : 'No lamina faces should exist.',
    'check transformations' : 'Pivot should be at ZERO, and all the transformations should be frozen.',
    'check overlapping vertices' : 'No overlapping vertices should exist.',
    'check external files' : 'All the files your Maya asset reference should be under the correct path.',
    'check shader names' : 'Check whether or not the shader names meet the requirement.',
    'check poly count' : 'Set your poly count budget and LOD.'
}
