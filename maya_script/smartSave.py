# -*- coding: utf-8 -*-

import os
import re
import pymel.core as pm

def smartSave():
    scene = pm.system.sceneName()
    scene_path = scene.dirname()
    file_name = scene.basename().split('.')[0]
    file_type = scene.getTypeName()[0]

    pattern = re.compile(r'_(\d{3})', re.U)
    result = re.search(pattern, file_name)

    if 0 == len(file_name):
        print('You need to save your scene first.')
    elif result is None:
        file_name = file_name + u'_001'
        file_name = scene_path + '\\' + file_name
        pm.system.saveAs(file_name, type=file_type)
    else:
        def _format_save_count(save_count):
            suffix = unicode(save_count)
            if save_count < 100 and save_count >= 10:
                suffix = u'0' + suffix
            elif save_count <= 9 and save_count >= 1:
                suffix = u'00' + suffix
            return suffix
        save_count = result.group(1)
        file_prefix = file_name.partition(save_count)[0]
        save_count = int(save_count) + 1
        save_count = _format_save_count(save_count)
        file_name = scene_path + '\\' + file_prefix + save_count
        pm.system.saveAs(file_name, type=file_type)

if __name__ == '__main__':
    smartSave()
