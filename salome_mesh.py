#
# This file is generated automatically by SALOME v8.3.0 with dump python functionality
# Modified by: Mehdi Paak
#

from __future__ import print_function
import os
import sys
import salome

salome.salome_init()
theStudy = salome.myStudy


with open('mesh_data.txt','r') as mshdata:
    GeomFile = mshdata.readline().strip('\n')
    wrkdir = mshdata.readline().strip('\n')
    seg_a = int(mshdata.readline())
    seg_b = int(mshdata.readline())

MeshFile = os.path.join(wrkdir,'mesh.med')
#print(GeomFile)
#print(MeshFile)
#print("aa = ", seg_a)
#print("bb = ", seg_b)

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

plate_iges_1 = geompy.ImportIGES(GeomFile)

edge_x0 = geompy.CreateGroup(plate_iges_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_x0, [3])
edge_x1 = geompy.CreateGroup(plate_iges_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_x1, [8])
edge_y0 = geompy.CreateGroup(plate_iges_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_y0, [10])
edge_y1 = geompy.CreateGroup(plate_iges_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(edge_y1, [6])

#TODO: find edge list and add instead of explicit edge index
border =  geompy.CreateGroup(plate_iges_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(border, [3,6,8,10])

face_1 = geompy.CreateGroup(plate_iges_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(face_1, [1])

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( plate_iges_1, 'plate.iges_1' )
geompy.addToStudyInFather( plate_iges_1, edge_x0, 'edge_x0' )
geompy.addToStudyInFather( plate_iges_1, edge_x1, 'edge_x1' )
geompy.addToStudyInFather( plate_iges_1, edge_y0, 'edge_y0' )
geompy.addToStudyInFather( plate_iges_1, edge_y1, 'edge_y1' )
geompy.addToStudyInFather( plate_iges_1, face_1, 'face_1' )
geompy.addToStudyInFather( plate_iges_1, border, 'border' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(plate_iges_1)
Regular_1D = Mesh_1.Segment()
Number_of_Segments_1 = Regular_1D.NumberOfSegments(seg_b,None,[])
Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
Regular_1D_1 = Mesh_1.Segment(geom=edge_x0)
status = Mesh_1.AddHypothesis(Number_of_Segments_1,edge_x0)
Propagation_of_1D_Hyp = Regular_1D_1.Propagation()
Regular_1D_2 = Mesh_1.Segment(geom=edge_y0)
Number_of_Segments_2 = Regular_1D_2.NumberOfSegments(seg_a,None,[])
status = Mesh_1.AddHypothesis(Propagation_of_1D_Hyp,edge_y0)
isDone = Mesh_1.Compute()
edge_x0_1 = Mesh_1.GroupOnGeom(edge_x0,'edge_x0',SMESH.NODE)
edge_x1_1 = Mesh_1.GroupOnGeom(edge_x1,'edge_x1',SMESH.NODE)
edge_y0_1 = Mesh_1.GroupOnGeom(edge_y0,'edge_y0',SMESH.NODE)
edge_y1_1 = Mesh_1.GroupOnGeom(edge_y1,'edge_y1',SMESH.NODE)
border_1 = Mesh_1.GroupOnGeom(border,'border',SMESH.NODE)
face_1_1 = Mesh_1.GroupOnGeom(face_1,'face_1',SMESH.FACE)
fac_nde = Mesh_1.GroupOnGeom(face_1,'fac_nde',SMESH.NODE)

smesh.SetName(Mesh_1, 'Mesh_1')

try:
  Mesh_1.ExportMED(MeshFile, 0, SMESH.MED_V2_2, 1, None ,1)
  pass
except:
  print('ExportToMEDX() failed. Invalid file name?')

