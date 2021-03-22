from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np

class spotDetector: 
    def __init__(self):
        self.allSpots=[]
        self.convert = 1
        #self.convert = 1.5
        self.getAllSpots()
        print(self.allSpots)
        

    def getAllSpots(self):
        self.allSpots.append(Polygon([(515*self.convert,338*self.convert),(535*self.convert, 372*self.convert),(578*self.convert, 365*self.convert),(555*self.convert, 330*self.convert)]))
        self.allSpots.append(Polygon([(639*self.convert, 461*self.convert),(672*self.convert, 511*self.convert),(721*self.convert, 503*self.convert),(689*self.convert, 451*self.convert)]))
        self.allSpots.append(Polygon([(949*self.convert, 459*self.convert),(1000*self.convert, 510*self.convert),(1047*self.convert, 500*self.convert),(991*self.convert, 450*self.convert)]))
        self.allSpots.append(Polygon([(771 *self.convert, 489*self.convert),(812*self.convert, 543*self.convert),(862*self.convert, 534*self.convert),(815*self.convert, 479*self.convert)]))   
        #self.allSpots.append(Polygon([(),(),(),()]))

    def returnSpots(self):
        return self.allSpots