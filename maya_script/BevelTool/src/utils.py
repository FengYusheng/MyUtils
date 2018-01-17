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



def createPartition(objectSetNode, name='MWBevelPartition'):
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
        MWBevelPartition.addMember(objectSetNode)
        # pm.partition(objectSetNode, add=MWBevelPartition)
    else:
        MWBevelPartition = pm.partition(objectSetNode, name=name)

    return MWBevelPartition



def getObjectSetsContainingEdgesUsingAPI2(edges=None):
    '''
    :Reference:
        getCreaseSetsContainingItems in  C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py

        http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__files_GUID_0B85C721_C3C6_47D7_9D85_4F27B787ABB6_htm
    '''
    setsContainingEdges = set()
    processedMeshNodeHandles = set()
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
                # Filter to not re-iterate over both the transform and the shape if both are in the selection list
                dagPathMeshNodeHandle = HashableMobjectHandle(dagPath.extendToShape().node())
                if (not component.isNull()) or (dagPathMeshNodeHandle not in processedMeshNodeHandles):
                    processedMeshNodeHandles.add(dagPathMeshNodeHandle)

                    # Process mesh and mesh components.
                    meshFn.setObject(dagPath)
                    connectedSets, connectedSetMembers = meshFn.getConnectedSetsAndMembers(dagPath.instanceNumber(), False)
                    for iConnectedSets in range(len(connectedSets)):
                        setFn.setObject(connectedSets[iConnectedSets])
                        if setFn.name().startswith('MWBevelSet'):
                            memberList = om.MSelectionList()
                            not len(connectedSetMembers) or memberList.add((dagPath, connectedSetMembers[iConnectedSets]))

                            # NOTE: om.MSelectionList.intersect()
                            if (not component.isNull()) and (component.apiTypeStr == 'kMeshEdgeComponent'):
                                selectionListToRemoveItems = om.MSelectionList(memberList)
                                selectionListToRemoveItems.merge(dagPath, component, om.MSelectionList.kRemoveFromList)
                                selectionListToRemoveItems.isEmpty() or  memberList.merge(selectionListToRemoveItems, om.MSelectionList.kRemoveFromList)

                            memberList.isEmpty() or setsContainingEdges.add(setFn.name())

        selectionListIterator.next()

    return setsContainingEdges



def createBevelSet(edges=None):
    '''
    :Reference:
        `CreateSet;`
        `performCreateSet false;`
        performCreateSet in C:/Program Files/Autodesk/Maya2018/scripts/others/performCreateSet.mel
    '''
    if edges is None:
        edges = pm.filterExpand(sm=32, ex=True)
    else:
        edges = pm.filterExpand(edges, sm=32, ex=True)

    pm.select(cl=True)
    MWBevelSet = None
    meshNode = getMeshObject(edges) if edges else []
    if edges and len(meshNode):
        name = meshNode[0].name() + 'MWBevelSet#'
        MWBevelSet = pm.sets(name=name)
        MWBevelPartition = createPartition(MWBevelSet)
        # pm.sets(*edges, forceElement=MWBevelSet)
        MWBevelSet.forceElement(edges)

        # forceElement doesn't always work.
        objestSetsContainingEdges = getObjectSetsContainingEdgesUsingAPI2(edges)
        objestSetsContainingEdges.discard(MWBevelSet.name())
        for objectSet in objestSetsContainingEdges:
            objectSet = pm.ls(objectSet, type='objectSet')[0]
            intersection = MWBevelSet.getIntersection(objectSet)
            not len(intersection) or objectSet.removeMembers(intersection)

    return MWBevelSet



def flattenEdges(edges):
    return pm.ls(edges, flatten=True)



def MWBevelSets():
    return [i for i in pm.ls(type='objectSet') if len(i.name().partition('MWBevelSet')[1])]



def bevelSetMembers(bevelSetName):
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    return pm.ls(bevelSetNode[0].flattened(), flatten=True) if bevelSetNode else []



def addMembersIntoBevelSet(bevelSetName, edges=None):
    # TODO: Only the edges belong to the same mesh can be added.
    edges = edges if edges is not None else pm.filterExpand(sm=32, ex=True)
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    if len(bevelSetNode) and (edges is not None):
        bevelSetNode[0].forceElement(edges)
        # forceElement doesn't always work.
        edges = edges if isinstance(edges[0], unicode) else [e.name() for e in edges]
        objestSetsContainingEdges = getObjectSetsContainingEdgesUsingAPI2(edges)
        objestSetsContainingEdges.discard(bevelSetNode[0].name())
        for objectSet in objestSetsContainingEdges:
            objectSet = pm.ls(objectSet, type='objectSet')[0]
            intersection = bevelSetNode[0].getIntersection(objectSet)
            not len(intersection) or objectSet.removeMembers(intersection)

    return bevelSetNode



def removeMembersFromBevelSet(bevelSetName, edges=None):
    edges = edges if edges is not None else pm.filterExpand(sm=32, ex=True)
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    if len(bevelSetNode) and (edges is not None):
        edges = [e for e in edges if e in bevelSetNode[0]]
        not len(edges) or bevelSetNode[0].removeMembers(edges)

    return bevelSetNode



def selectedEdgeindices(edges=[]):
    edges = edges if edges else pm.filterExpand(sm=32, ex=True)
    return [int(e.name().partition('[')[2].partition(']')[0]) for e in pm.ls(edges, flatten=True)]



def getMeshObject(edges=[]):
    """
    :param:
        edges, unicode list
    """
    meshObject = list(set(e.partition('.')[0] for e in edges))
    print(meshObject)

    if len(meshObject) > 1:
        pm.warning('More than one objects are selected.')
    elif 0 == len(meshObject):
        pm.warning('You need select several mesh edges.')

    return pm.ls(meshObject) if len(meshObject) == 1 else []



def disconnectFromMWBevelSet(bevelSetName, meshTransform):
    bevelSet = pm.ls(bevelSetName, type='objectSet')
    meshTransformNode = pm.ls(meshTransform)
    if len(bevelSet) and len(meshTransformNode):
        meshNode = meshTransformNode[0].getShape() if isinstance(meshTransformNode[0], pm.nt.Transform) else meshTransformNode[0]

        meshAttr = None
        bevelSetAttr = bevelSet[0].name() + '.memberWireframeColor'
        for destinationAttr in pm.connectionInfo(bevelSetAttr, dfs=True):
            if destinationAttr.startswith(meshNode.name()):
                meshAttr = destinationAttr.rpartition('.')[0]
                pm.disconnectAttr(bevelSetAttr, destinationAttr)
                break

        if meshAttr is not None:
            for destinationAttr in pm.connectionInfo(meshAttr, dfs=True):
                if destinationAttr.startswith(bevelSet[0].name()):
                    pm.disconnectAttr(meshAttr, destinationAttr)
                    break



def duplicateMeshTransform(bevelSetName):
    _duplicatedMeshTransform = []
    members = bevelSetMembers(bevelSetName)
    meshObject = getMeshObject(members)
    _duplicatedMeshTransform = pm.ls(meshObject[0].name()+'DupTrans', type='transform')
    if not len(_duplicatedMeshTransform):
        # TODO: Undo duplicate.
        _duplicatedMeshTransform = pm.duplicate(meshObject[0], name=meshObject[0].name()+'DupTrans', st=True, rr=True)
        disconnectFromMWBevelSet(bevelSetName, _duplicatedMeshTransform)
        pm.move(25.0, 0.0, 0.0, _duplicatedMeshTransform, r=True)

    return _duplicatedMeshTransform



def deletePolyBevelNodeInBevelSet(bevelSetName):
    _duplicatedMeshTransform = pm.ls(bevelSetName+'DuplicationTransform', type='transform')
    if len(_duplicatedMeshTransform):
        if len(bevelSetMembers(bevelSetName)):
            polyBevel3Node = pm.listConnections(_duplicatedMeshTransform[0].getShape(), type='polyBevel3')
            polyBevel3Node = [bevel for bevel in polyBevel3Node if bevel.name().startswith('MWBevelOnSelectedEdges')]
            not len(polyBevel3Node) or pm.delete(polyBevel3Node)
        else:
            # NOTE: Why does it delete the empty objectSet at the same time?
            pm.delete(_duplicatedMeshTransform)



def deleteBevelSet(bevelSetName):
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    # TODO: Undo delete.
    if len(bevelSetNode):
        # Delete the duplicated mesh transform.
        _duplicatedMeshTransform = pm.ls(bevelSetName+'DuplicationTransform', type='transform')
        not len(_duplicatedMeshTransform) or pm.delete(_duplicatedMeshTransform)
        pm.delete(bevelSetNode[0])



def selectMembersInBevelSet(bevelSetName):
    # TODO: Undo select?
    members = bevelSetMembers(bevelSetName)
    if len(members):
        meshNode = pm.ls(members[0].name().partition('.')[0], type='mesh')
        pm.select(meshNode, r=True)
        switchSelectionModeToEdge(meshNode[0])
        pm.select(members, r=True)



def navigateBevelSet():
    # TODO: Undo navigate?
    pass



if __name__ == '__main__':
    # item = pm.ls(sl=True)[0]
    # switchSelectionModeToEdge(item)
    # selectedMeshTransformNodes()
    # getObjectSetsContainingEdgesUsingAPI2()
    createBevelSet()
    # print(MWBevelSets())
    # print(polyBevel3NodeInBevelSet('MWBevelSet1'))
    # disconnectFromMWBevelSet('MWBevelSet1', 'pCube3')
    # removeMembersFromBevelSet('MWBevelSet1')
    # deleteBevelSet('MWBevelSet1')
    # selectMembersInBevelSet('MWBevelSet1')
