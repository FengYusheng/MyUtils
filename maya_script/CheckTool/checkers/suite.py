# -*- coding: utf-8 -*-

import time
import json
import sys
import os
import re

import pymel.core as pm
import maya.api.OpenMaya as OpenMaya


def maya_useNewAPI():
    pass


class Checkers(object):
    def __init__(self, suite):
        """
        @param {dict} suite
        """
        def _getGeometries():
            shapes = pm.ls(type='mesh')
            self.data['geometries'] = {repr(shape) : {} for shape in shapes}
            for shape in shapes:
                transforms = shape.getAllParents()
                self.data['geometries'][repr(shape)]['transforms'] = [repr(t) for t in transforms if t.getShape()]

        self.data = {}
        self.data['report'] = {}
        self.suite = suite
        self.scene = pm.system.sceneName()
        self.maya_dir = None if '' == self.scene else self.scene.dirname()
        _getGeometries()


    def centerAndFreeze(self):
        """
        Set all polygons' pivots to (0, 0, 0) in world space and
        freeze all polygons' transformations.
        """
        center = pm.dt.Point([0, 0, 0])
        geometries = self.data['geometries'].values()
        # polygons = [t for g in geometries for t in g['transforms']]
        for p in (t for g in geometries for t in g['transforms']):
            p = eval('pm.' + p)
            p.setPivots(center, worldSpace=True)
            pm.makeIdentity(p, apply=True,      \
                               translate=1,     \
                               rotate=1,        \
                               scale=1,         \
                               normal=0,        \
                               preserveNormals=1)


    def checkTransformations(self):
        cameras = pm.listCameras()
        cameras = cameras if cameras else []
        transforms = pm.ls(type='transform')
        transforms = [t for t in transforms if t not in cameras] if transforms else []
        center = pm.dt.Vector([0.0, 0.0, 0.0])
        self.data['report']['check transformations'] = []
        with pm.uitypes.MainProgressBar(minValue=0, maxValue=len(transforms), interruptable=False) as bar:
            bar.setStatus('Check Transformations.')
            for t in transforms:
                bar.step(1)
                pivots = t.getPivots(worldSpace=True)
                tx = t.tx.get()
                ty = t.ty.get()
                tz = t.tz.get()
                rx = t.rx.get()
                ry = t.ry.get()
                rz = t.rz.get()
                sx = t.sx.get()
                sy = t.sy.get()
                sz = t.sz.get()

                if pivots[0] != center \
                or pivots[1] != center \
                or tx != 0.0           \
                or ty != 0.0           \
                or rx != 0.0           \
                or ry != 0.0           \
                or rz != 0.0           \
                or sx != 0.0           \
                or sy != 0.0           \
                or sz != 0.0:

                    t.name() in self.data['report']['check transformations'] \
                    or self.data['report']['check transformations'].append(t.name())


    def checkIntermediateNode(self):
        """Check whether intermediate mesh nodes exist."""
        shapes = [eval('pm.'+s) for s in self.data['geometries'].keys()]
        with pm.uitypes.MainProgressBar(minValue=0, maxValue=2, interruptable=False) as bar:
            bar.setStatus('Check Intermediate Node.')
            bar.step(1)
            self.data['report']['check intermediate node'] = [s.name() for s in shapes if s.isIntermediate()]
            bar.step(1)


    def checkPolyCount(self):
        """
        Check the poly count(Verts, Edges, Faces, Tris, UVs).

        Note:
            The default option of 'heads up->poly count' is 'Smooth Mesh Preview'.
            So the counts aren't the actual numbers of polygons which you see in maya scene.
            Select the option 'Cage' to make 'heads up' display the actual counts.

        Reference:
            http://help.autodesk.com/view/MAYAUL/2017/CHS/?guid=__files_GUID_0B85C721_C3C6_47D7_9D85_4F27B787ABB6_htm
        """
        Verts = Edges = Faces = Tris = UVs = 0
        dagIterator = OpenMaya.MItDag(
            OpenMaya.MItDag.kDepthFirst,
            OpenMaya.MFn.kMesh
        )

        while (not dagIterator.isDone()):
            dagObject = dagIterator.currentItem()
            instances = dagIterator.getPath().instanceNumber() + 1
            meshFn = OpenMaya.MFnMesh(dagObject)

            Verts += meshFn.numVertices            * instances
            Edges += meshFn.numEdges               * instances
            Faces += meshFn.numPolygons            * instances
            UVs   += meshFn.numUVs()               * instances
            Tris  += sum(meshFn.getTriangles()[0]) * instances

            dagIterator.next()

        expected = int(self.suite['details']['check poly count'][0])
        if expected and Verts > expected:
            self.data['report']['check poly count'][0] = str(Verts)

        expected = int(self.suite['details']['check poly count'][1])
        if expected and Edges > expected:
            self.data['report']['check poly count'][1] = str(Edges)

        expected = int(self.suite['details']['check poly count'][2])
        if expected and Faces > expected:
            self.data['report']['check poly count'][2] = str(Faces)

        expected = int(self.suite['details']['check poly count'][3])
        if expected and Tris > expected:
            self.data['report']['check poly count'][3] = str(Tris)

        expected = int(self.suite['details']['check poly count'][4])
        if expected and UVs > expected:
            self.data['report']['check poly count'][4] = str(UVs)


    def checkPolyCount2(self):
        """
        Check the poly count(Verts, Edges, Faces, Tris, UVs). This function also
        detects the intermediate nodes.
        """
        if len(self.data['geometries']):
            shapes = [eval('pm.'+s) for s in self.data['geometries'].keys()]
            Verts = Edges = Faces = Tris = UVs = 0
            self.data['report']['check poly count'] = {}
            with pm.uitypes.MainProgressBar(minValue=0, maxValue=len(shapes), interruptable=False) as bar:
                bar.setStatus('Check Poly Count.')
                for s in shapes:
                    bar.step(1)
                    if s.isIntermediate():
                        continue

                    instance_number = len(s.getAllPaths())
                    Verts += s.numVertices() * instance_number
                    Edges += s.numEdges() * instance_number
                    Faces += s.numFaces() * instance_number
                    UVs   += s.numUVs() * instance_number
                    Tris  += int(pm.mel.eval('polyEvaluate -triangle {0}'.format(s))[0]) * instance_number

            expected = int(self.suite['details']['check poly count']['Verts'])
            if expected and Verts > expected:
                self.data['report']['check poly count']['Verts'] = str(Verts)

            expected = int(self.suite['details']['check poly count']['Edges'])
            if expected and Edges > expected:
                self.data['report']['check poly count']['Edges'] = str(Edges)

            expected = int(self.suite['details']['check poly count']['Faces'])
            if expected and Faces > expected:
                self.data['report']['check poly count']['Faces'] = str(Faces)

            expected = int(self.suite['details']['check poly count']['Tris'])
            if expected and Tris > expected:
                self.data['report']['check poly count']['Tris'] = str(Tris)

            expected = int(self.suite['details']['check poly count']['UVs'])
            if expected and UVs > expected:
                self.data['report']['check poly count']['UVs'] = str(UVs)


    def checkNGons(self):
        """
        Find n-gons(faces with more than 4 sides). This function refers to maya script, polyCleanupArgList.mel.
        """
        self.data['report']['check n-gons'] = []
        if len(self.data['geometries']):
            shapes = [eval('pm.'+s) for s in self.data['geometries'].keys()]
            with pm.uitypes.MainProgressBar(minValue=0, maxValue=2, interruptable=False) as bar:
                bar.setStatus('Check N-gons.')
                bar.step(1)
                pm.select(shapes, r=True)
                pm.polySelectConstraint(disable=True, m=3, t=8, sz=3)
                ngons = pm.ls(sl=True)
                pm.polySelectConstraint(disable=True)
                pm.select(cl=True)
                bar.step(1)

            self.data['report']['check n-gons'] = [n.name() for n in ngons] if ngons else []


    def checkLaminaFaces(self):
        """
        Find Lamina faces(faces sharing all edges). This function refers to maya script, polyCleanupArgList.mel.
        """
        self.data['report']['check lamina faces'] = []
        if len(self.data['geometries']):
            shapes = [eval('pm.'+s) for s in self.data['geometries'].keys()]
            with pm.uitypes.MainProgressBar(minValue=0, maxValue=2, interruptable=False) as bar:
                bar.setStatus('Check Lamina Faces.')
                bar.step(1)
                pm.select(shapes, r=True)
                pm.polySelectConstraint(disable=True, m=3, t=8, tp=2)
                laminas = pm.ls(sl=True)
                pm.polySelectConstraint(disable=True)
                pm.select(cl=True)
                bar.step(1)

            self.data['report']['check lamina faces'] = [l.name() for l in laminas] if laminas else []


    def checkOverlappingVertices(self):
        """
        Find overlapping vertices.

        Steps:
            1. Find vertices on zero length edges(whose length is less than 0.01).
            2. Find vertices on zero area faces(whose area is less than 0.01).
        """
        self.data['report']['check overlapping vertices'] = []
        if len(self.data['geometries']):
            overlappingVertices = set()
            shapes = [eval('pm.'+s) for s in self.data['geometries'].keys()]

            # Find vertices on zero length edges.
            pm.select(shapes, r=True)
            pm.polySelectConstraint(disable=True, m=3, t=0x8000, l=True, lb=(0.0, 0.01))
            zeroEdges = pm.ls(sl=True)
            pm.polySelectConstraint(disable=True)
            pm.select(cl=True)
            overlappingVertices.update(set(pm.polyListComponentConversion(zeroEdges, toVertex=True)))

            # Find vertices on zero area faces.
            pm.select(shapes, r=True)
            pm.polySelectConstraint(disable=True, m=3, t=8, ga=True, gab=(0.0, 0.01))
            zeroFaces = pm.ls(sl=True)
            pm.polySelectConstraint(disable=True)
            pm.select(cl=True)
            overlappingVertices.update(set(pm.polyListComponentConversion(zeroFaces, toVertex=True)))

            self.data['report']['check overlapping vertices'] = [v.name() for v in overlappingVertices]


    def checkOverlappingVertices2(self):
        """ Find overlapping vertices."""
        self.data['report']['check overlapping vertices'] = []
        if len(self.data['geometries']):
            shapes = [eval('pm.'+s) for s in self.data['geometries'].keys()]
            with pm.uitypes.MainProgressBar(minValue=0, maxValue=len(shapes), interruptable=False) as bar:
                bar.setStatus('Check Overlapping Vertices.')
                for shape in shapes:
                    bar.step(1)
                    verts = set(shape.vtx)
                    while verts:
                        vert = verts.pop()
                        position = vert.getPosition()
                        pm.select(shape, r=True)
                        pm.polySelectConstraint(disable=True, m=3, t=1, d=1, db=(0.0, 0.01), dp=position)
                        _overlappingVerts = pm.ls(sl=True)
                        verts.difference_update(set(_overlappingVerts))
                        _overlappingVerts = [v.name() for v in _overlappingVerts]
                        pm.polySelectConstraint(disable=True)
                        not len(_overlappingVerts) > 1 or self.data['report']['check overlapping vertices'].append(_overlappingVerts)


    def checkShaderNames(self):
        """ Check the shaders name. """
        shaders = pm.ls(materials=True)
        shaders.remove('particleCloud1')
        shaders.remove('lambert1')
        self.data['report']['check shader names'] = []

        if len(shaders):
            with pm.uitypes.MainProgressBar(minValue=0, maxValue=len(shaders), interruptable=False) as bar:
                bar.setStatus('Check Shader Names.')
                for pattern in self.suite['details']['check shader names']:
                    bar.step(1)
                    pattern = pattern.replace('<SHADER>', '.*?').replace('#', '\d')
                    pattern = re.compile(pattern)
                    map(lambda s : re.match(pattern, s.name()) is None or shaders.remove(s), shaders[:])

            self.data['report']['check shader names'] = [s.name() for s in shaders]


    def checkExternalfilePath(self):
        """Check all the external files which aren't in the specified folder."""
        files = pm.ls(type='file')
        files = files if files else []
        self.data['report']['check external file path'] = []
        with pm.uitypes.MainProgressBar(minValue=0, maxValue=len(files), interruptable=False) as bar:
            bar.setStatus('Check External File Path.')
            for f in files[:]:
                bar.step(1)
                file_path = f.fileTextureName.get().rpartition('/')[0]
                self.maya_dir not in file_path or files.remove(f)

        self.data['report']['check external file path'] = [f.name() + ' : ' + f.fileTextureName.get() for f in files]


    def save_report(self):
        if self.maya_dir is not None:
            path = self.maya_dir + '/report.json'
            with open(path, 'w') as report:
                json.dump(self.data['report'], report, indent=4, encoding='utf-8')
                self.data['report'] = {}
        else:
            pm.system.warning('Save your scene !')


    def run(self):
        if 'check transformations' in self.suite['test']:
            self.checkTransformations()

        if 'check intermediate node' in self.suite['test']:
            self.checkIntermediateNode()

        if 'check n-gons' in self.suite['test']:
            self.checkNGons()

        if 'check lamina faces' in self.suite['test']:
            self.checkLaminaFaces()

        if 'check shader names' in self.suite['test']:
            self.checkShaderNames()

        if 'check external file path' in self.suite['test']:
            self.checkExternalfilePath()

        if 'check poly count' in self.suite['test']:
            self.checkPolyCount2()

        if 'check overlapping vertices' in self.suite['test']:
            self.checkOverlappingVertices2()

        if len(self.data['report']):
            self.save_report()
