# -*- coding: utf-8 -*-
import pymel.core as pm


class MayaUndoChuck():
    """
    Reference:
        `MayaUndoChunk` in "C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py"
    """
    def __init__(self, name):
        self.name = name


    def __enter__(self):
        pm.system.undoInfo(openChunk=True, chunkName=self.name)


    def __exit__(self, type, value, trackback):
        pm.system.undoInfo(closeChunk=True)



def switchSelectionModeToEdge(item):
    '''
    Reference:
        doMenuComponentSelection in C:/Program Files/Autodesk/Maya2017/scripts/others/dagMenuProc.mel
    '''
    pm.mel.eval('HideManipulators')
    if pm.selectMode(q=True, object=True):
        pm.selectType(ocm=True, alc=False)
        pm.selectType(ocm=True, edge=True)
        pm.selectType(edge=True)
        pm.hilite(item)
    else:
        pm.selectType(alc=False)
        pm.selectType(edge=True)
        not pm.selectMode(q=True, preset=True) or pm.hilite(item)

    try:
        not pm.mel.eval('exists dR_selTypeChanged') or pm.mel.eval('dR_selTypeChanged("edge")')
    except pm.MelError:
        pass


def selectedMeshTransformNodes():
    '''
    A shape node may have more than one transform node as its parent node, use
    `i for i in pm.ls(sl=True) if isinstance(i, pm.nt.DagNode) and hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)`
    to get mesh transform nodes

    Reference:
        http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__Nodes_index_html

        Reference: getSelectedMeshComponents() in C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py
    '''
    # meshTransformNodes = []
    # for mesh in pm.ls(dag=True, sl=True, noIntermediate=True, type='mesh'):
    #     transformNode = pm.listRelatives(mesh, parent=True, path=True)[0]
    #     not isinstance(transformNode, pm.nt.Transform) or meshTransformNodes.append(transformNode)

    return [i for i in pm.ls(sl=True) if isinstance(i, pm.nt.DagNode) and hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]


def createSet(name='BevelSet#'):
    pass



if __name__ == '__main__':
    # item = pm.ls(sl=True)[0]
    # switchSelectionModeToEdge(item)
    selectedMeshTransformNodes()
