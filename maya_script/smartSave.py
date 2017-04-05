# -*- coding: utf-8 -*-

import os
import re

import pymel.core as pm

scene = pm.system.sceneName()
file_name = scene.basename().split('.')[0]
file_path = scene.dirname()
file_type = scene.getTypeName()[0]

pattern = re.compile(r'_(\d{3})', re.U)
result = re.search(pattern, file_name)
if 0 == len(file_name):
    print('new save')
elif result is None:
    file_name = file_name + u'_001'
else:
    save_count = int(result.group(1))
    save_count += 1

    def _format_save_count(save_count):
        suffix = unicode(save_count)
        if save_count < 100 and save_count >= 10:
            suffix = u'0' + suffix
        elif save_count < 10 and save_count >= 1:
            suffix = u'00' + suffix

        return suffix

    suffix = _format_save_count(save_count)
    file_name = file_name.partition('_')[0]
    file_name = file_name + '_' + suffix

def cleanHistory():
    pm.delete(ch=True)

file_name = file_path + '/' + file_name
pm.system.saveAs(file_name, type=file_type)
