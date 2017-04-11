# -*- coding: utf-8 -*-

import pymel.core as pm

def smartExtract():
    transforms = pm.ls(selection=True)
    if 0 == len(transforms):
        print("You need to select an object first.")
        return

    for node in transforms:
        node_type = repr(node)
        if 'nt.Transform' in node_type:
            pm.polyChipOff(node)[0].setKeepFacesTogether(val=False)
            pieces = pm.polySeparate(node)
            pm.delete(pieces[0])

    pm.delete(ch=True)

if __name__ == '__main__':
    smartExtract()
