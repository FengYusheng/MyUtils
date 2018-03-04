# -*- coding: utf-8 -*-
from collections import defaultdict
import copy

import pymel.core as pm
import maya.api.OpenMaya as om # Python api 2.0

import options
import bevelTool
reload(bevelTool)



class MCallBackIdWrapper(object):
    """
    :Refernce:
        MCallbackIdWrapper in C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py
    """
    def __init__(self, callbackId):
        super(MCallBackIdWrapper, self).__init__()
        self.callbackId = callbackId


    def __del__(self):
        om.MMessage.removeCallback(self.callbackId)


    def __repr__(self):
        return 'MCallBackIdWrapper(%r)'%self.callbackId



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
    :TODO: flush undo?
    :Reference:
        `MayaUndoChunk` in "C:\Program Files\Autodesk\Maya2017\Python\Lib\site-packages\maya\app\general\creaseSetEditor.py"
    """
    def __init__(self, name):
        self.name = name


    def __enter__(self):
        pm.system.undoInfo(openChunk=True, chunkName=self.name)


    def __exit__(self, type, value, trackback):
        pm.system.undoInfo(closeChunk=True)



class UnlockBevelSet(object):
    def __init__(self, bevelSetName):
        super(UnlockBevelSet, self).__init__()
        self.bevelSetName = bevelSetName


    def __enter__(self):
        bevelSetNode = pm.ls(self.bevelSetName, type='objectSet')
        not len(bevelSetNode) or pm.lockNode(bevelSetNode, lock=False)


    def __exit__(self, type, value, trackback):
        bevelSetNode = pm.ls(self.bevelSetName, type='objectSet')
        not len(bevelSetNode) or pm.lockNode(bevelSetNode, lock=True)



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



def numBevelSet():
    bevelSets = []
    if options.drawOverredeAttributes['mesh'] != ' ':
        bevelSets = [s.name() for s in pm.listSets(object=options.drawOverredeAttributes['mesh']) if len(s.name().partition('MWBevelSet')[1])]
        bevelSets += [s.name() for m in options.drawOverredeAttributes['ioMesh queue'] for s in pm.listSets(object=m) if len(s.name().partition('MWBevelSet')[1])] if isinstance(options.drawOverredeAttributes['ioMesh queue'], list) else []

    return len(bevelSets), bevelSets



def flattenEdges(edges):
    return pm.ls(edges, flatten=True)



def MWBevelSets():
    return [i for i in pm.ls(type='objectSet') if len(i.name().rpartition('MWBevelSet_')[1])]



def MWBevelSetExists(bevelSetName):
    return len(pm.ls(bevelSetName, type='objectSet'))



def bevelSetMembers(bevelSetName):
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    return pm.ls(bevelSetNode[0].flattened(), flatten=True) if bevelSetNode else []



def isBevelSetBeveled(bevelSetName):
    return len(bevelSetMembers(bevelSetName))



def removeMembersFromBevelSet(bevelSetName, edges=None):
    edges = pm.filterExpand(edges, sm=32, ex=True) if edges is not None else pm.filterExpand(sm=32, ex=True)
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    if len(bevelSetNode) and (edges is not None):
        edges = [e for e in edges if e in bevelSetNode[0]]
        with UnlockBevelSet(bevelSetName):
            not len(edges) or bevelSetNode[0].removeMembers(edges)



def clearBevelSet(bevelSetName):
    bevelNode = pm.ls(bevelSetName, type='objectSet')
    members = bevelSetMembers(bevelSetName)
    members = pm.filterExpand(members, sm=32, ex=True) if len(members) else []
    with UnlockBevelSet(bevelSetName):
        not (len(members) and len(bevelNode)) or bevelNode[0].removeMembers(members)



def selectedEdgeindices(edges=[]):
    edges = edges if edges else pm.filterExpand(sm=32, ex=True)
    return [int(e.name().partition('[')[2].partition(']')[0]) for e in pm.ls(edges, flatten=True)]



def getMeshObject(edges=[]):
    """
    :param:
        edges, results of pm.filterExpand command, e.g.[u'pCylinder1.e[54]'] or pm.MeshEdge list.
    """
    dagObject = list(set(e.partition('.')[0] for e in edges))

    if len(dagObject) > 1:
        pm.warning('More than one objects are selected.')
    elif 0 == len(dagObject):
        pm.warning('You need select several mesh edges.')
    else:
        dagObject = pm.ls(dagObject)
        dagObject = dagObject if isinstance(dagObject[0], pm.nt.Mesh) else pm.listRelatives(dagObject[0], shapes=True, ni=True)

    return dagObject if len(dagObject) == 1 else []



def disconnectFromMWBevelSet(bevelSetName, meshTransform):
    bevelSet = pm.ls(bevelSetName, type='objectSet')
    meshTransformNode = pm.ls(meshTransform)
    if len(bevelSet) and len(meshTransformNode):
        with UnlockBevelSet(bevelSetName):
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



def deletePolyBevelNodeInBevelSet(bevelSetName):
    # NOTE: Why does it delete the empty objectSet at the same time?
    # If you find something wierd, clean up the maya folder YOUR DOCUMENT\maya\VERSION\.
    polyBevel3Node = pm.ls('MWBevel_'+bevelSetName, type='polyBevel3')
    not len(polyBevel3Node) or pm.delete(polyBevel3Node)



def deleteBevelSet(bevelSetName):
    _bevelSetName = bevelSetName
    deleteBevelNodeStack = []
    num = int(bevelSetName.rpartition('_')[2])
    meshName = bevelSetName.rpartition('MWBevelSet_')[0]
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    while len(bevelSetNode):
        with UnlockBevelSet(_bevelSetName):
            len(bevelSetMembers(_bevelSetName)) or deleteBevelNodeStack.append(_bevelSetName)
            pm.delete(bevelSetNode)
            num += 1
            _bevelSetName = meshName + 'MWBevelSet_' + str(num)
            bevelSetNode = pm.ls(_bevelSetName, type='objectSet')

    map(lambda name:deletePolyBevelNodeInBevelSet(name), deleteBevelNodeStack[::-1]) # Delete polyBevel3 node in reversed order.



def selectMembersInBevelSet(bevelSetName):
    # TODO: Undo select?
    members = bevelSetMembers(bevelSetName)
    if len(members):
        meshNode = pm.ls(members[0].name().partition('.')[0], type='mesh')
        pm.select(meshNode, r=True)
        switchSelectionModeToEdge(meshNode[0])
        pm.select(members, r=True)



def selectHardEdges():
    meshTrans = [i for i in pm.ls(dag=True, sl=True, noIntermediate=True) if hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]
    if not len(meshTrans):
        edges = [e for e in pm.ls(sl=True, noIntermediate=True) if isinstance(e, pm.MeshEdge)]
        meshTrans = getMeshObject(edges) if len(edges) else []

    if len(meshTrans):
        # Switch selection mode to edge.
        if pm.mel.eval('exists doMenuComponentSelection'):
            try:
                pm.mel.eval('doMenuComponentSelection("{0}", "edge")'.format(meshTrans[0].name()))
            except pm.MelError:
                pass
        else:
            switchSelectionModeToEdge(meshTrans[0])

        pm.select(meshTrans[0].e, r=True)
        pm.polySelectConstraint(disable=True, m=2, t=0x8000, sm=1)
        pm.polySelectConstraint(disable=True)



def selectSoftEdges():
    meshTrans = [i for i in pm.ls(dag=True, sl=True, noIntermediate=True) if hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]
    if not len(meshTrans):
        edges = [e for e in pm.ls(sl=True, noIntermediate=True) if isinstance(e, pm.MeshEdge)]
        meshTrans = getMeshObject(edges) if len(edges) else []

    if len(meshTrans):
        # Switch selection mode to edge.
        if pm.mel.eval('exists doMenuComponentSelection'):
            try:
                pm.mel.eval('doMenuComponentSelection("{0}", "edge")'.format(meshTrans[0].name()))
            except pm.MelError:
                pass
        else:
            switchSelectionModeToEdge(meshTrans[0])

        pm.select(meshTrans[0].e, r=True)
        pm.polySelectConstraint(disable=True, m=2, t=0x8000, sm=2)
        pm.polySelectConstraint(disable=True)



def setSmoothingAngle(angle):
    meshTrans = [i for i in pm.ls(dag=True, sl=True, noIntermediate=True) if hasattr(i, 'getShape') and isinstance(i.getShape(), pm.nt.Mesh)]
    if not len(meshTrans):
        edges = [e for e in pm.ls(sl=True, noIntermediate=True) if isinstance(e, pm.MeshEdge)]
        meshTrans = getMeshObject(edges) if len(edges) else []

    if len(meshTrans) == 1:
        meshObject = meshTrans[0].getShape() if isinstance(meshTrans[0], pm.nt.Transform) else meshTrans[0]
        polySoftEdgeName = 'MWPolySoftEdge_' + meshObject.name()
        MWPolySoftEdgeNodes = [i for i in pm.listConnections(meshObject, type='polySoftEdge') if i.name().startswith('MWPolySoftEdge_')]

        # TODO: Delete the polySoftEdge nodes?
        polySoftEdgeNodes = list(set([i for i in pm.listConnections(meshObject, type='polySoftEdge')]) - set(MWPolySoftEdgeNodes))
        not len(polySoftEdgeNodes) or pm.delete(polySoftEdgeNodes)

        if len(MWPolySoftEdgeNodes):
            MWPolySoftEdgeNodes[0].setAngle(angle)
        else:
            pm.polySoftEdge(a=angle)[0].setName(polySoftEdgeName)
    else:
        pm.warning('Select one mesh transform object.')



def isActiveSelectionListChanged():
    edges = pm.filterExpand(sm=32, ex=True)
    mesh = getMeshObject(edges) if edges is not None else pm.ls(dag=True, os=True, type='mesh', ni=True) # original mesh
    return len(mesh) > 0 and (options.drawOverredeAttributes['mesh'] != ' ' or options.drawOverredeAttributes['ioMesh'] != ' ') and mesh[0].name() not in (options.drawOverredeAttributes['mesh'], options.drawOverredeAttributes['ioMesh'])



def isSelectionModechanged():
    return not (len(pm.ls(hilite=True)) > 0 and pm.selectType(q=True, edge=True))



def finishBevel():
    for bevelSet in MWBevelSets():
        lockBevelSet(bevelSet.name(), False)
        pm.delete(bevelSet)



def lockBevelSet(bevelSetName, isLocked=True):
    bevelSet = pm.ls(bevelSetName, type='objectSet')
    not len(bevelSet) or pm.lockNode(bevelSet, lock=isLocked)



def enableUndo(enable=True):
    pm.undoInfo(state=enable)



def saveDrawOverrideAttributes(originMesh):
    options.drawOverredeAttributes['mesh'] = originMesh.name()
    options.drawOverredeAttributes['originMesh overrideEnabled'] = originMesh.overrideEnabled.get()
    options.drawOverredeAttributes['originMesh overrideDisplayType'] = originMesh.overrideDisplayType.get()

    ioMesh = pm.ls(dag=True, os=True, io=True)
    if len(ioMesh):
        options.drawOverredeAttributes['ioMesh queue'] = [s.name() for s in ioMesh]
        options.drawOverredeAttributes['ioMesh'] = ioMesh[-1].name()
        options.drawOverredeAttributes['ioMesh overrideEnabled'] = ioMesh[-1].overrideEnabled.get()
        options.drawOverredeAttributes['ioMesh overrideDisplayType'] = ioMesh[-1].overrideDisplayType.get()
        options.drawOverredeAttributes['ioMesh overrideTexturing'] = ioMesh[-1].overrideTexturing.get()



def restoreDrawOverrideAttributes():
    ioMesh = pm.ls(options.drawOverredeAttributes['ioMesh'], type='mesh')
    if len(ioMesh):
        ioMesh[0].overrideTexturing.set(options.drawOverredeAttributes['ioMesh overrideTexturing'])
        ioMesh[0].overrideDisplayType.set(options.drawOverredeAttributes['ioMesh overrideDisplayType'])
        ioMesh[0].overrideEnabled.set(options.drawOverredeAttributes['ioMesh overrideEnabled'])
        ioMesh[0].intermediateObject.set(True)

    mesh = pm.ls(options.drawOverredeAttributes['mesh'], type='mesh')
    if len(mesh):
        mesh[0].overrideDisplayType.set(options.drawOverredeAttributes['originMesh overrideDisplayType'])
        mesh[0].overrideEnabled.set(options.drawOverredeAttributes['originMesh overrideEnabled'])

    options.drawOverredeAttributes.clear()



def displayIOMesh(meshTrans, operation=None):
    def _displayIOMeshe(originMesh, ioMesh):
        if len(ioMesh):
            originMesh[0].overrideEnabled.get() or originMesh[0].overrideEnabled.set(True)
            originMesh[0].overrideDisplayType.set(2) # Reference.
            pm.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3) # displaySmoothness isn't undoable.

            # Edit the latest intermediate object attributes.
            ioMesh[-1].intermediateObject.set(False)
            ioMesh[-1].overrideEnabled.set(True)
            ioMesh[-1].overrideDisplayType.set(0) # Normal.
            ioMesh[-1].overrideTexturing.set(False)
            pm.select(ioMesh[-1], r=True)
            switchSelectionModeToEdge(ioMesh[-1])
        else:
            switchSelectionModeToEdge(meshTrans)

    originMesh = pm.listRelatives(meshTrans, shapes=True, ni=True)
    pm.select(meshTrans, r=True) # I can't select the intermediate object if I select the origin mesh directly hear.
    ioMesh = pm.ls(dag=True, os=True, io=True)
    restoreDrawOverrideAttributes()
    saveDrawOverrideAttributes(originMesh[0])
    if operation is not None:
        with MayaUndoChuck(operation):
            _displayIOMeshe(originMesh, ioMesh)
    else:
        _displayIOMeshe(originMesh, ioMesh)



def activeBevel():
    editingMeshTrans = ''
    transforms = pm.ls(dag=True, os=True, transforms=True)
    hasSelection = len(transforms) > 0
    not hasSelection or displayIOMesh(transforms[-1], 'Start to MW bevel.')
    return hasSelection



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
                        if len(setFn.name().partition('MWBevelSet')[1]):
                            memberList = om.MSelectionList()
                            not len(connectedSetMembers) or memberList.add((dagPath, connectedSetMembers[iConnectedSets]))

                            # NOTE: om.MSelectionList.intersect()
                            if (not component.isNull()) and (component.apiTypeStr == 'kMeshEdgeComponent'):
                                selectionListToRemoveItems = om.MSelectionList(memberList)
                                selectionListToRemoveItems.merge(dagPath, component, om.MSelectionList.kRemoveFromList)
                                selectionListToRemoveItems.isEmpty() or memberList.merge(selectionListToRemoveItems, om.MSelectionList.kRemoveFromList)

                            memberList.isEmpty() or setsContainingEdges.add(setFn.name())

        selectionListIterator.next()

    return setsContainingEdges



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



def _addMembersIntoBevelSet(bevelSetName, edges=None):
    origin, intermediate = options.drawOverredeAttributes['mesh'], options.drawOverredeAttributes['ioMesh']
    edges = pm.filterExpand(edges, sm=32, ex=True) if edges is not None else pm.filterExpand(sm=32, ex=True)
    MWBevelSet = pm.ls(bevelSetName, type='objectSet')
    if len(MWBevelSet) and (edges is not None):
        indices = [int(e.name().rpartition('[')[2].rpartition(']')[0]) for e in pm.ls(edges, flatten=True)]
        mesh = pm.ls(intermediate, type='mesh') if intermediate != ' ' else pm.ls(origin, type='mesh')
        edges = [mesh[0].e[i] for i in indices]
        MWBevelSet[0].forceElement(edges)
        objectSetsContainingEdges = getObjectSetsContainingEdgesUsingAPI2([e.name() for e in edges])
        objectSetsContainingEdges.discard(MWBevelSet[0].name())
        for objectSet in objectSetsContainingEdges:
            objectSet = pm.ls(objectSet, type='objectSet')[0]
            intersection = MWBevelSet[0].getIntersection(objectSet)
            not len(intersection) or objectSet.removeMembers(intersection)



def addEdgesIntoBevelSet(MWBevelSetName, edges=None):
    pass



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

    if edges is not None:
        originMesh = pm.ls(options.drawOverredeAttributes['mesh'])
        meshTrans = originMesh[0].getTransform()
        edgeIndices = [int(e.name().partition('[')[2].partition(']')[0]) for e in pm.ls(edges, flatten=True)]
        with MayaUndoChuck('Create a MW bevel set.'):
            pm.select(cl=True)
            MWBevelSet = pm.sets(name='MWBevelSet#')
            MWBevelPartition = createPartition(MWBevelSet)
            MWBevelSet.forceElement(edges)

            objectSetsContainingEdges = getObjectSetsContainingEdgesUsingAPI2(edges)
            objectSetsContainingEdges.discard(MWBevelSet.name())
            for objectSet in objectSetsContainingEdges:
                objectSet = pm.ls(objectSet, type='objectSet')[0]
                intersection = MWBevelSet.getIntersection(objectSet)
                not len(intersection) or objectSet.removeMembers(intersection)

            MWBevelSetName = MWBevelSet.name()
            bevelTool.bevelSelectedEdges(*(edgeIndices, options.drawOverredeAttributes['mesh'], MWBevelSetName), **copy.copy(options.bevelOptions))

            if options.drawOverredeAttributes['ioMesh'] == ' ':
                disconnectFromMWBevelSet(MWBevelSetName, options.drawOverredeAttributes['mesh'])
            else:
                disconnectFromMWBevelSet(MWBevelSetName, options.drawOverredeAttributes['ioMesh'])

            displayIOMesh(meshTrans)
            addMembersIntoBevelSet(MWBevelSetName, edges)



if __name__ == '__main__':
    addMembersIntoBevelSet('MWBevelSet1')
