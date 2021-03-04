from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np

class spotDetector: 
    def __init__(self):
        self.allSpots=[]
        self.getAllSpots()
        print(self.allSpots)

    def getAllSpots(self):
        self.allSpots.append(Polygon([(515,338),(535, 372),(578, 365),(555, 330)]))
        #self.allSpots.append(Polygon([(),(),(),()]))
        #self.allSpots.append(Polygon([(),(),(),()]))
        #self.allSpots.append(Polygon([(),(),(),()]))
        #self.allSpots.append(Polygon([(),(),(),()]))

    def returnSpots(self):
        return self.allSpots