# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.api.OpenMaya as om



class HashableMobjectHandle(om.MObjectHandle):
    """
    :Reference:
        HashableMObjectHandle in C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py
    """
    def __init__(self, object):
        super(HashableMobjectHandle, self).__init__(object)


    def __hash__(self):
        return self.hashCode()



class MayaUndoChuck():
    """
    :Reference:
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
    :Reference:
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

    :Reference:
        http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__Nodes_index_html

        Reference: getSelectedMeshComponents() in C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py
    '''
    # meshTransformNodes = []
    # for mesh in pm.ls(dag=True, sl=True, noIntermediate=True, type='mesh'):
    #     transformNode = pm.listRelatives(mesh, parent=True, path=True)[0]
    #     not isinstance(transformNode, pm.nt.Transform) or meshTransformNodes.append(transformNode)

    return [i for i in pm.ls(sl=True) if isinstance(i, pm.nt.DagNode) and hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]



def createPartition(name='MWBevelPartition'):
    '''
    :Refernce:
        `CreatePartition;`
        `performCreatePartition false;`
        performCreatePartition in C:/Program Files/Autodesk/Maya2018/scripts/others/performCreatePartition.mel

        getCreaseSetPartition in C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py
    '''
    MWBevelPartition = pm.ls(name, type='partition')
    if MWBevelPartition:
        MWBevelPartition = MWBevelPartition[0]
    else:
        MWBevelPartition = pm.partition(name=name)

    return MWBevelPartition



def getBevelSetsContainingEdgesUsingAPI2(edges=None):
    '''
    :Reference:
        getCreaseSetsContainingItems in  C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py

        http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__files_GUID_0B85C721_C3C6_47D7_9D85_4F27B787ABB6_htm
    '''
    setsContainingEdges = set()
    processedTransformNodeHandles = set()
    meshFn = om.MFnMesh()
    setFn = om.MFnSet()

    if edges is not None:
        selectionList = om.MSelectionList()
        map(lambda e:selectionList.add(e), edges)
    else:
        selectionList = om.MGlobal.getActiveSelectionList()

    selectionListIterator = om.MItSelectionList(selectionList)
    while not selectionListIterator.isDone():
        if selectionListIterator.itemType() == om.MItSelectionList.kDagSelectionItem:
            dagPath, component = selectionListIterator.getComponent()
            if dagPath.hasFn(om.MFn.kMesh):
                # meshFn.setObject(dagPath)
                # print(meshFn.name())
                # print(component.apiTypeStr) # kMeshEdgeComponent

                # Filter to not re-iterate over both the transform and the shape if both are in the selection list
                dagPathTransformNodeHandle = HashableMobjectHandle(dagPath.transform())
                if (not component.isNull()) or (dagPathTransformNodeHandle not in processedTransformNodeHandles):
                    processedTransformNodeHandles.add(dagPathTransformNodeHandle)

                    # Process mesh and mesh components.
                    meshFn.setObject(dagPath)
                    connectedSets, connectedSetMembers = meshFn.getConnectedSetsAndMembers(dagPath.instanceNumber(), False)
                    for iConnectedSets in range(len(connectedSets)):
                        setFn.setObject(connectedSets[iConnectedSets])
                        if setFn.name().startswith('MWBevelSet'):
                            memberList = om.MSelectionList()
                            connectedSetMembers.isNull() or memberList.add(dagPath, connectedSetMembers[iConnectedSets])

                            # NOTE: om.MSelectionList.intersect()
                            if (not component.isNull()) and (component.apiTypeStr == 'kMeshEdgeComponent'):
                                selectionListToRemoveItems = om.MSelectionList(memberList)
                                selectionListToRemoveItems.merge(dagPath, component, om.MSelectionList.kRemoveFromList)
                                selectionListToRemoveItems.isEmpty() or  memberList.merge(selectionListToRemoveItems, om.MSelectionList.kRemoveFromList)

                            memberList.isEmpty() or setsContainingEdges.add(setFn.name())

        selectionListIterator.next()

    return setsContainingEdges



def createBevelSet(name='MWBevelSet#', edges=None):
    '''
    :Reference:
        `CreateSet;`
        `performCreateSet false;`
        performCreateSet in C:/Program Files/Autodesk/Maya2018/scripts/others/performCreateSet.mel
    '''
    MWBevelPartition = createPartition()
    newMWBevelSet = pm.sets(name=name)
    # newBevelSet = pm.sets(name=name, edges=True)
    pm.partition(newMWBevelSet, add=MWBevelPartition)

    edges is not None or pm.select(edges, r=True)
    selectedEdges = pm.filterExpand(sm=32, ex=True)
    not len(selectedEdges) or pm.sets(selectedEdges, forceElement=newMWBevelSet)

    # `forceElement` doesn't always work.
    if len(selectedEdges):
        pass



if __name__ == '__main__':
    # item = pm.ls(sl=True)[0]
    # switchSelectionModeToEdge(item)
    # selectedMeshTransformNodes()
    getBevelSetsContainingEdgesUsingAPI2()
