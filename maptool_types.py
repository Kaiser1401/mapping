import numpy as np
from scipy.spatial import kdtree

class pointFile:
    def __init__(self,path,group=""):
        self.group = group
        self.path=path

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (self.path)

class utmPoint:
    def __init__(self,x,y,z,group = ""):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.group = group

    def assign(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    def min(self,other):
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)
        self.z = min(self.z, other.z)

    def max(self,other):
        self.x = max(self.x, other.x)
        self.y = max(self.y, other.y)
        self.z = max(self.z, other.z)

    def __sub__(self, other):
        return utmPoint(self.x-other.x,self.y-other.y,self.z-other.z)

    def __add__(self, other):
        return utmPoint(self.x+other.x,self.y+other.y,self.z+other.z)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ("%f %f %f" % (self.x, self.y, self.z))



class HoleFixer:
    def __init__(self,points):
        self.points = points
        self.tree = kdtree(points)

    def getTree(self):
        return self.tree

    def getEdgePoints(self,range=1.0,minDistFromMean=0.35,minNeighbourCount = 6):
        edgePoints = []


        # maybe change to query_ball_tree
        for point in self.points:
            neighbours = self.tree.query_ball_point(point,range)
            if len(neighbours) <= minNeighbourCount:
                continue

            mean = np.mean(neighbours, axis=0)
            print (mean)
            dist = np.linalg.norm(point - mean)
            print (dist)
            if dist > minDistFromMean:
                edgePoints.append(point)

        return edgePoints

    def getPatchPoints(self,edgePoints,range=1.6,minDist=2.0,pointSpacing=0.7):
        patchPoints = []
        # maybe change to query_ball_tree
        for point in edgePoints:
            neighbours = self.tree.query_ball_point(point, range)
            #find highest
            highest_z_idx=neighbours.argmax(axis=0)[2]
            highestPoint = neighbours[highest_z_idx]









