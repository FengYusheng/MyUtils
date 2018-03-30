# -*- coding: utf-8 -*-
from collections import Counter
import copy
import functools

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
        len(bevelSetNode) > 0 and pm.lockNode(bevelSetNode, lock=False)


    def __exit__(self, type, value, trackback):
        bevelSetNode = pm.ls(self.bevelSetName, type='objectSet')
        len(bevelSetNode) > 0 and pm.lockNode(bevelSetNode, lock=True)



def isSelectionTypeVertexFace():
    mesh = pm.ls(hilite=True, dag=True, ni=True, type='mesh')
    ret = len(mesh) > 0 and pm.selectType(q=True, pvf=True)
    if ret:
        for m in mesh:
            options.isVertexFace += Counter({m.name() : 1})

    return ret



def switchSelectionTypeToVf(item):
    pm.mel.eval('HideManipulators')
    if pm.selectMode(q=True, object=True):
        pm.selectType(ocm=True, alc=False)
        pm.selectType(ocm=True, pvf=True)
        pm.selectType(pvf=True)
        pm.hilite(item)
    else:
        pm.selectType(alc=False)
        pm.selectType(pvf=True)
        pm.selectMode(q=True, preset=True) and pm.hilite(item)

    try:
        pm.mel.eval('exists dR_selTypeChanged') and pm.mel.eval('dR_selTypeChanged("edge")')
    except pm.MelError:
        pass



def switchSelectionTypeToEdge(item):
    '''
    :Reference:
        doMenuComponentSelection in C:/Program Files/Autodesk/Maya2017/scripts/others/dagMenuProc.mel
    '''
    def _switchSelectionTypeToEdge():
        pm.mel.eval('HideManipulators')
        if pm.selectMode(q=True, object=True):
            pm.selectType(ocm=True, alc=False)
            pm.selectType(ocm=True, edge=True)
            pm.selectType(edge=True)
            pm.hilite(item)
        else:
            pm.selectType(alc=False)
            pm.selectType(edge=True)
            pm.selectMode(q=True, preset=True) and pm.hilite(item)

        try:
            pm.mel.eval('exists dR_selTypeChanged') and pm.mel.eval('dR_selTypeChanged("edge")')
        except pm.MelError:
            pass

    name = item.name() if not isinstance(item, str) else item
    if pm.mel.eval('exists doMenuComponentSelection'):
        try:
            pm.mel.eval('doMenuComponentSelection("{0}", "edge")'.format(name))
        except pm.MelError:
            pass
    else:
        _switchSelectionTypeToEdge()



def numBevelSet():
    bevelSets = []
    if options.drawOverredeAttributes['mesh'] != ' ':
        bevelSets = [s.name() for s in pm.listSets(object=options.drawOverredeAttributes['mesh']) if len(s.name().partition('MWBevelSet')[1])]
        bevelSets += [s.name() for m in options.drawOverredeAttributes['ioMesh queue'] for s in pm.listSets(object=m) if len(s.name().partition('MWBevelSet')[1])] if isinstance(options.drawOverredeAttributes['ioMesh queue'], list) else []

    return len(bevelSets), bevelSets



def MWBevelSets():
    return [i.name() for i in pm.ls(type='objectSet') if i.name().startswith('MWBevelSet')]



def bevelSetMembers(bevelSetName):
    bevelSetNode = pm.ls(bevelSetName, type='objectSet')
    return pm.ls(bevelSetNode[0].flattened(), flatten=True) if bevelSetNode else []



def isBevelSetBeveled(bevelSetName):
    return len(bevelSetMembers(bevelSetName))



def clearBevelSet(bevelSetName):
    bevelNode = pm.ls(bevelSetName, type='objectSet')
    members = bevelSetMembers(bevelSetName)
    members = pm.filterExpand(members, sm=32, ex=True) if len(members) else []
    with UnlockBevelSet(bevelSetName):
        len(members) and len(bevelNode) and bevelNode[0].removeMembers(members)



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



def disconnectFromMWBevelSet(MWBevelSetName, meshTransform):
    bevelSet = pm.ls(MWBevelSetName, type='objectSet')
    meshTransformNode = pm.ls(meshTransform)
    if len(bevelSet) and len(meshTransformNode):
        with UnlockBevelSet(MWBevelSetName):
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



def isInDrawOverrideAttributesDict():
    """
    Problem: more than one objects are in edge selection type.
    Solve: unhilite the other objects?
    """
    mesh = pm.ls(dag=True, hilite=True, type='mesh', ni=True)
    mesh = pm.ls(dag=True, os=True, type='mesh', ni=True) if len(mesh) == 0 else mesh
    return len(mesh) > 0 and mesh[0].name() in (options.drawOverredeAttributes['mesh'], options.drawOverredeAttributes['ioMesh'])



def isSelectionTypeEdge():
    return len(pm.ls(dag=True, hilite=True, type='mesh')) > 0 and pm.selectType(q=True, edge=True)



def lockBevelSet(bevelSetName, isLocked=True):
    bevelSet = pm.ls(bevelSetName, type='objectSet')
    len(bevelSet) and pm.lockNode(bevelSet, lock=isLocked)



def disableSelectionEventCallback():
    def decorate(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            options.disableIntermediate.append(func.__name__)
            ret = func(*args, **kwargs)
            options.disableIntermediate.pop()
            return ret
        return decorator
    return decorate



def saveDrawOverrideAttributes(originMesh):
    options.drawOverredeAttributes['mesh'] = originMesh.name()
    options.drawOverredeAttributes['originMesh overrideEnabled'] = originMesh.overrideEnabled.get()
    options.drawOverredeAttributes['originMesh overrideDisplayType'] = originMesh.overrideDisplayType.get()

    ioMesh = pm.ls(dag=True, hilite=True, io=True)
    if len(ioMesh):
        options.drawOverredeAttributes['ioMesh queue'] = [s.name() for s in ioMesh]
        options.drawOverredeAttributes['ioMesh'] = ioMesh[-1].name()
        options.drawOverredeAttributes['ioMesh overrideEnabled'] = ioMesh[-1].overrideEnabled.get()
        options.drawOverredeAttributes['ioMesh overrideDisplayType'] = ioMesh[-1].overrideDisplayType.get()
        options.drawOverredeAttributes['ioMesh overrideTexturing'] = ioMesh[-1].overrideTexturing.get()
        options.drawOverredeAttributes['ioMesh allowTopologyMod'] = ioMesh[-1].allowTopologyMod.get()



@disableSelectionEventCallback()
def restoreDrawOverrideAttributes(operation=None):
    def _restore():
        if len(ioMesh):
            ioMesh[0].overrideTexturing.set(options.drawOverredeAttributes['ioMesh overrideTexturing'])
            ioMesh[0].overrideDisplayType.set(options.drawOverredeAttributes['ioMesh overrideDisplayType'])
            ioMesh[0].overrideEnabled.set(options.drawOverredeAttributes['ioMesh overrideEnabled'])
            ioMesh[0].allowTopologyMod.set(options.drawOverredeAttributes['ioMesh allowTopologyMod'])

            # The selected components of the intermediate are still in active selection list
            # when you turn the intermediate flag on. Clearing active selection list seems good.
            ioMesh[0].intermediateObject.set(True)

        if len(mesh):
            mesh[0].overrideDisplayType.set(options.drawOverredeAttributes['originMesh overrideDisplayType'])
            mesh[0].overrideEnabled.set(options.drawOverredeAttributes['originMesh overrideEnabled'])

            # The selected components of the intermediate are still in active selection list
            # when you turn the intermediate flag on. So clear active selection list here.
            pm.select(cl=True)

    ioMesh = pm.ls(options.drawOverredeAttributes['ioMesh'], type='mesh')
    mesh = pm.ls(options.drawOverredeAttributes['mesh'], type='mesh')

    if operation is None:
        _restore()
    else:
        with MayaUndoChuck(operation):
            _restore()

    options.drawOverredeAttributes.clear()


@disableSelectionEventCallback()
def displayIOMesh(meshTrans, operation=None):
    def _displayIOMesh():
        if len(ioMesh):
            originMesh[0].overrideEnabled.get() or originMesh[0].overrideEnabled.set(True)

            # Reference.
            originMesh[0].overrideDisplayType.set(2)

            # displaySmoothness isn't undoable.
            pm.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)

            # Edit the latest intermediate object attributes.
            ioMesh[-1].intermediateObject.set(False)
            ioMesh[-1].overrideEnabled.set(True)

            # Normal.
            ioMesh[-1].overrideDisplayType.set(0)

            ioMesh[-1].overrideTexturing.set(False)
            ioMesh[-1].allowTopologyMod.set(False)

            pm.select(ioMesh[-1], r=True)
            switchSelectionTypeToEdge(ioMesh[-1])

            # The display of intermediate is defective if the selection type of origin mesh is vertex face
            # _origin = options.drawOverredeAttributes['mesh']
            # if options.isVertexFace[_origin] > 0:
            #     switchSelectionTypeToVf(options.drawOverredeAttributes['ioMesh'])
            #     switchSelectionTypeToEdge(options.drawOverredeAttributes['ioMesh'])
            #     del options.isVertexFace[_origin]
        else:
            switchSelectionTypeToEdge(meshTrans)

    def _deleteHistory():
        modifiers = [i for i in pm.listConnections(originMesh[0], type='polyModifier') if not isinstance(i, pm.nt.PolyBevel3)]
        (len(modifiers) > 0 or len(pm.ls(dag=True, hilite=True, io=True)) == 0) and pm.delete(meshTrans, ch=True)

    restoreDrawOverrideAttributes()

    originMesh = pm.listRelatives(meshTrans, shapes=True, ni=True)

    _deleteHistory()

    ioMesh = pm.ls(dag=True, hilite=True, io=True)
    saveDrawOverrideAttributes(originMesh[0])

    if operation is not None:
        with MayaUndoChuck(operation):
            _displayIOMesh()
    else:
        _displayIOMesh()



def activeBevel():
    transforms = pm.ls(dag=True, hilite=True, transforms=True)
    hasSelection = len(transforms) > 0
    hasSelection and displayIOMesh(transforms[-1], 'Start to bevel {0}.'.format(transforms[-1].name()))
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
            len(intersection) > 0 and objectSet.removeMembers(intersection)



def addEdgesIntoBevelSet(MWBevelSetName, edges=None):
    mesh = options.drawOverredeAttributes['ioMesh'] if options.drawOverredeAttributes['ioMesh'] != ' ' else options.drawOverredeAttributes['mesh']
    meshTrans = pm.ls(options.drawOverredeAttributes['mesh'])[0].getTransform()
    MWBevelSet = pm.ls(MWBevelSetName, type='objectSet')
    edges = pm.filterExpand(edges, sm=32, ex=True) if edges is not None else pm.filterExpand(sm=32, ex=True)
    _, bevelSetName = numBevelSet()

    if edges is not None:
        edges += [e.name() for e in bevelSetMembers(MWBevelSetName) if e.name().rpartition('.e')[0] == mesh]
        indices = [int(e.rpartition('[')[2].rpartition(']')[0]) for e in pm.ls(edges, flatten=True)]
        bevelOptions = bevelTool.getBevelOptionsFromBevelSet(MWBevelSetName)
        with MayaUndoChuck('Add edges {0} into {1}.'.format(edges, MWBevelSetName)):
            pm.lockNode(MWBevelSet[0], lock=False)
            bevelTool.bevelSelectedEdges(*(indices, options.drawOverredeAttributes['mesh'], MWBevelSetName), **bevelOptions)

            if options.drawOverredeAttributes['ioMesh'] == ' ':
                disconnectFromMWBevelSet(MWBevelSetName, options.drawOverredeAttributes['mesh'])
            else:
                disconnectFromMWBevelSet(MWBevelSetName, options.drawOverredeAttributes['ioMesh'])

            displayIOMesh(meshTrans)
            mesh = options.drawOverredeAttributes['ioMesh'] if options.drawOverredeAttributes['ioMesh'] != ' ' else options.drawOverredeAttributes['mesh']
            mesh = pm.ls(mesh, type='mesh')
            edges = [mesh[0].e[i] for i in indices]
            _addMembersIntoBevelSet(MWBevelSetName, edges)
            pm.lockNode(MWBevelSet[0], lock=True)



def removeEdgesFromBevelSet(edges=None):
    edges = pm.filterExpand(edges, sm=32, ex=True) if edges is not None else pm.filterExpand(sm=32, ex=True)
    mesh = options.drawOverredeAttributes['ioMesh'] if options.drawOverredeAttributes['ioMesh'] != ' ' else options.drawOverredeAttributes['mesh']
    meshTrans = pm.ls(mesh, type='mesh')[0].getTransform()
    _, MWBevelSetName = numBevelSet()

    if len(MWBevelSetName) and (edges is not None):
        membersIndices = set([int(e.name().rpartition('[')[2].rpartition(']')[0]) for e in bevelSetMembers(MWBevelSetName[0]) if e.name().rpartition('.e')[0] == mesh])
        selectedIndices = set([int(e.name().rpartition('[')[2].rpartition(']')[0]) for e in pm.ls(edges, flatten=True)])
        membersIndices.difference_update(selectedIndices)
        indices = list(membersIndices)
        bevelOptions = bevelTool.getBevelOptionsFromBevelSet(MWBevelSetName[0])
        MWBevelSet = pm.ls(MWBevelSetName[0], type='objectSet')

        with MayaUndoChuck('Remove edges {0} from {1}'.format(edges, MWBevelSetName[0])):
            pm.lockNode(MWBevelSet[0], lock=False)
            bevelTool.bevelSelectedEdges(*(indices, options.drawOverredeAttributes['mesh'], MWBevelSetName[0]), **bevelOptions)
            if options.drawOverredeAttributes['ioMesh'] == ' ':
                disconnectFromMWBevelSet(MWBevelSetName[0], options.drawOverredeAttributes['mesh'])
            else:
                disconnectFromMWBevelSet(MWBevelSetName[0], options.drawOverredeAttributes['ioMesh'])

            displayIOMesh(meshTrans)
            mesh = options.drawOverredeAttributes['ioMesh'] if options.drawOverredeAttributes['ioMesh'] != ' ' else options.drawOverredeAttributes['mesh']
            mesh = pm.ls(mesh, type='mesh')
            edges = [mesh[0].e[i] for i in indices]
            _addMembersIntoBevelSet(MWBevelSetName[0], edges)
            pm.lockNode(MWBevelSet[0], lock=True)



def deleteBevelSet(MWBevelSetName):
    MWBevelSet = pm.ls(MWBevelSetName, type='objectSet')
    if len(MWBevelSet):
        MWBevelNodes = [i for i in pm.ls(type='polyBevel3') if i.name().startswith(MWBevelSetName+'_Bevel_')]
        with MayaUndoChuck('Delete {0}.'.format(MWBevelSetName)):
            len(MWBevelNodes) > 0 and pm.delete(MWBevelNodes)
            pm.lockNode(MWBevelSet, lock=False)
            restoreDrawOverrideAttributes()
            pm.delete(MWBevelSet)



@disableSelectionEventCallback()
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
            MWBevelSetName = MWBevelSet.name()
            bevelTool.bevelSelectedEdges(*(edgeIndices, options.drawOverredeAttributes['mesh'], MWBevelSetName), **copy.copy(options.bevelOptions))
            pm.createNode('polyBevel3', name=MWBevelSetName+'_Bevel_Node', shared=True, skipSelect=True)

            # The objectSet is locked automatically when it has no connection.
            # You can still add members into it.
            if options.drawOverredeAttributes['ioMesh'] == ' ':
                disconnectFromMWBevelSet(MWBevelSetName, options.drawOverredeAttributes['mesh'])
            else:
                disconnectFromMWBevelSet(MWBevelSetName, options.drawOverredeAttributes['ioMesh'])

            displayIOMesh(meshTrans)
            _addMembersIntoBevelSet(MWBevelSetName, edges)
            pm.lockNode(MWBevelSet, lock=True)



def force(oldMWBevelSetName, newMWBevelSetName=None, edges=None, *args):
    mesh = options.drawOverredeAttributes['ioMesh'] if options.drawOverredeAttributes['ioMesh'] != ' ' else options.drawOverredeAttributes['mesh']
    edges = pm.filterExpand(edges, sm=32, ex=True) if edges is not None else pm.filterExpand(sm=32, ex=True)
    members = [e.name() for e in bevelSetMembers(oldMWBevelSetName) if e.name().rpartition('.e')[0] == mesh]
    edges = members + edges if edges is not None else members
    newMWBevelSetName is None and createBevelSet(edges)
    newMWBevelSetName is not None and addEdgesIntoBevelSet(newMWBevelSetName, edges)



@disableSelectionEventCallback()
def selectMembersInBevelSet(bevelSetName):
    members = bevelSetMembers(bevelSetName)



@disableSelectionEventCallback()
def selectHardEdges():
    mesh = pm.ls(dag=True, os=True, ni=True, type='mesh')
    mesh = pm.ls(dag=True, hilite=True, ni=True, type='mesh') if len(mesh) == 0 else mesh
    if len(mesh) == 1:
        switchSelectionTypeToEdge(mesh[0].getTransform())
        activeBevel()

        if options.drawOverredeAttributes['ioMesh'] != ' ':
            mesh = pm.ls(options.drawOverredeAttributes['ioMesh'], type='mesh')
        else:
            mesh = pm.ls(options.drawOverredeAttributes['mesh'], type='mesh')

        pm.select(mesh[0].e, r=True)
        pm.polySelectConstraint(disable=True, m=2, t=0x8000, sm=1)
        pm.polySelectConstraint(disable=True)
    else:
        pm.warning('Select an object per time.')

    return len(mesh)



@disableSelectionEventCallback()
def selectSoftEdges():
    mesh = pm.ls(dag=True, os=True, ni=True, type='mesh')
    mesh = pm.ls(dag=True, hilite=True, ni=True, type='mesh') if len(mesh) == 0 else mesh
    if len(mesh) == 1:
        switchSelectionTypeToEdge(mesh[0].getTransform())
        activeBevel()

        if options.drawOverredeAttributes['ioMesh'] != ' ':
            mesh = pm.ls(options.drawOverredeAttributes['ioMesh'], type='mesh')
        else:
            mesh = pm.ls(options.drawOverredeAttributes['mesh'], type='mesh')

        pm.select(mesh[0].e, r=True)
        pm.polySelectConstraint(disable=True, m=2, t=0x8000, sm=2)
        pm.polySelectConstraint(disable=True)
    else:
        pm.warning('Select an object per time.')

    return len(mesh)



@disableSelectionEventCallback()
def setSmoothingAngle(angle):
    if options.drawOverredeAttributes['mesh'] == ' ':
        mesh = pm.ls(dag=True, os=True, ni=True, type='mesh')
    else:
        mesh = pm.ls(options.drawOverredeAttributes['mesh'], type='mesh')
        restoreDrawOverrideAttributes()

    if len(mesh) == 1:
        polySoftEdgeName = 'MWPolySoftEdge_' + mesh[0].name()
        MWPolySoftEdgeNodes = [i for i in pm.listConnections(mesh[0], type='polySoftEdge') if i.name().startswith('MWPolySoftEdge_')]

        # Delete the polySoftEdge nodes?
        polySoftEdgeNodes = list(set([i for i in pm.listConnections(mesh[0], type='polySoftEdge')]) - set(MWPolySoftEdgeNodes))
        len(polySoftEdgeNodes) == 0 or pm.delete(polySoftEdgeNodes)

        pm.select(mesh[0].getTransform(), r=True)

        if len(MWPolySoftEdgeNodes):
            MWPolySoftEdgeNodes[0].setAngle(angle)
        else:
            pm.polySoftEdge(a=angle)[0].setName(polySoftEdgeName)

        # Delete construction history because the origin mesh is changed.
        pm.delete(mesh[0].getTransform(), ch=True)

    else:
        pm.warning('Select an object per time.')



def selectedMWBevelSets():
    mesh = pm.ls(dag=True, os=True, io=True, type='mesh')
    mesh = pm.ls(dag=True, hilite=True, ni=True, type='mesh') if len(mesh) == 0 else mesh
    MWBevelSets = [s for m in mesh for s in pm.listSets(object=m.name()) if s.startswith('MWBevelSet')] if len(mesh) else []
    return MWBevelSets, len(mesh)



@disableSelectionEventCallback()
def delConstructionHistory():
    """
    Solve problem: modify the origin mesh shape when it's in edge selection type.

    Delete the construction history if the origin mesh is modified.
    """
    if options.drawOverredeAttributes['mesh'] != ' ':
        mesh = pm.ls(options.drawOverredeAttributes['mesh'], type='mesh')
        modifiers = [i for i in pm.listConnections(mesh[0], type='polyModifier') if not i.name().startswith('MWBevelSet')]
        edges = pm.filterExpand(sm=32, ex=True)

        if len(modifiers):
            with MayaUndoChuck('Delete ch when origin mesh is modified.'):
                restoreDrawOverrideAttributes()
                pm.delete(mesh[0].getTransform(), ch=True)
                displayIOMesh(mesh[0].getTransform())
                pm.select(edges, r=True)



if __name__ == '__main__':
    selectedMWBevelSets()
