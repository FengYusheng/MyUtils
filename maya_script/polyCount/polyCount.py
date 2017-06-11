# -*- coding: utf-8 -*-

import os
import json

import pymel.core as pm

class PolyGeometries(object):
    def __init__(self):
        self.scene_name = pm.system.sceneName()
        self.work_dir = self.scene_name.dirname()
        self.UVs = 0
        self.vertices = 0
        self.faces = 0
        self.edges = 0
        self.triangles = 0
        self.geometris = None
        self.datas = {
            'totalVertices' : 0,
            'totalEdges' : 0,
            'totalFaces' : 0,
            'totalUVs' : 0
        }

    def getPolyCount(self):
        self.geometris = pm.ls(type='mesh')
        for shape in self.geometris:
            transforms = shape.getAllParents()
            transforms = [repr(t) for t in transforms if t.getShape()]
            count = len(transforms)
            shape_name = repr(shape)
            self.datas[shape_name] = {}
            self.datas[shape_name]['vertices'] = shape.numVertices() * count
            self.datas[shape_name]['edges'] = shape.numEdges() * count
            self.datas[shape_name]['faces'] = shape.numFaces() * count
            self.datas[shape_name]['UVs'] = shape.numUVs() * count
            self.datas[shape_name]['transforms'] = transforms
            self.datas['totalVertices'] += self.datas[shape_name]['vertices']
            self.datas['totalEdges'] += self.datas[shape_name]['edges']
            self.datas['totalFaces'] += self.datas[shape_name]['faces']
            self.datas['totalUVs'] += self.datas[shape_name]['UVs']

    def savePolyCount(self):
        path = self.work_dir + '/report.json'
        with open(path, 'w') as report:
            json.dump(self.datas, report, indent=4, encoding='utf-8')


if __name__ == '__main__':
    poly = PolyGeometries()
    poly.getPolyCount()
    poly.savePolyCount()
