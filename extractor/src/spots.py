from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

class spotDetector: 
    def __init__(self):
        allSpots=[]
        getAllSpots()
        print(allSpots)

    def getAllSpots(self):
        self.allSpots.append(Polygon([(),(),(),()]))
        self.allSpots.append(Polygon([(),(),(),()]))
        self.allSpots.append(Polygon([(),(),(),()]))
        self.allSpots.append(Polygon([(),(),(),()]))
        self.allSpots.append(Polygon([(),(),(),()]))

    def returnSpots(self):
        return self.allSpots