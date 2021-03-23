from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np
import config as cfg 
import mysql.connector

HOST = cfg.db['host']
PORT = cfg.db['port']
DATABASE = cfg.db['database']
USER = cfg.db['user']
PASSWORD = cfg.db['password']

class spotDetector: 
    def __init__(self):
        self.allSpots=[]
        # self.convert = 1
        self.convert = 1.5
        self.getAllSpots()
        print(self.allSpots)
        

    def getAllSpots(self):
        sql = Sql()
        coordinates = sql.get_coordinates()
        for row in coordinates:
            number1 = row[0].split(',')
            number2 = row[1].split(',')
            number3 = row[2].split(',')
            number4 = row[3].split(',')
            self.allSpots.append(Polygon([(int(number1[0])*self.convert, int(number1[1])*self.convert),(int(number2[0])*self.convert, int(number2[1])*self.convert),
            (int(number3[0])*self.convert, int(number3[1])*self.convert),(int(number4[0])*self.convert, int(number4[1])*self.convert)]))
        # coordinates_1 = sql.get_coordinates(1)
        # coordinates_2 = sql.get_coordinates(2)
        # coordinates_3 = sql.get_coordinates(3)
        # coordinates_4 = sql.get_coordinates(4)
        # coord1_x1 = coordinates_1[0].split(',')
        # coord1_y1 = coordinates_1[1].split(',')
        # coord1_x2 = coordinates_1[2].split(',')
        # coord1_y2 = coordinates_1[3].split(',')

        # coord2_x1 = coordinates_2[0].split(',')
        # coord2_y1 = coordinates_2[1].split(',')
        # coord2_x2 = coordinates_2[2].split(',')
        # coord2_y2 = coordinates_2[3].split(',')

        # coord3_x1 = coordinates_3[0].split(',')
        # coord3_y1 = coordinates_3[1].split(',')
        # coord3_x2 = coordinates_3[2].split(',')
        # coord3_y2 = coordinates_3[3].split(',')

        # coord4_x1 = coordinates_4[0].split(',')
        # coord4_y1 = coordinates_4[1].split(',')
        # coord4_x2 = coordinates_4[2].split(',')
        # coord4_y2 = coordinates_4[3].split(',')
        
       
        # self.allSpots.append(Polygon([(int(coord1_x1[0])*self.convert,int(coord1_x1[1])*self.convert),(int(coord1_y1[0])*self.convert, int(coord1_y1[1])*self.convert),(int(coord1_x2[0])*self.convert, int(coord1_x2[1])*self.convert),(int(coord1_y2[1])*self.convert, int(coord1_y2[1])*self.convert)]))
        # self.allSpots.append(Polygon([(int(coord1_x1[1])*self.convert, 461*self.convert),(672*self.convert, 511*self.convert),(721*self.convert, 503*self.convert),(689*self.convert, 451*self.convert)]))
        # self.allSpots.append(Polygon([(949*self.convert, 459*self.convert),(1000*self.convert, 510*self.convert),(1047*self.convert, 500*self.convert),(991*self.convert, 450*self.convert)]))
        # self.allSpots.append(Polygon([(771 *self.convert, 489*self.convert),(812*self.convert, 543*self.convert),(862*self.convert, 534*self.convert),(815*self.convert, 479*self.convert)]))   
        #self.allSpots.append(Polygon([(),(),(),()]))

    def returnSpots(self):
        return self.allSpots

class Sql:
        
    def connected(self):
        return self.cnx.is_connected()
    
    def connect(self):
        self.cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    
    def disconnect(self):
        self.cnx.close()
    
    def get_coordinates(self):
        self.connect()
        cursor = self.cnx.cursor()

        query = ("SELECT * from Coordinates ")
        coordinates = []
        cursor.execute(query,)
        for row in cursor:
            coordinates.append(row)
        
        cursor.close()
        self.cnx.commit()
        self.disconnect()

        return coordinates

sql = Sql()
coordinates = sql.get_coordinates()
for row in coordinates:
    number1 = row[0].split(',')
    number2 = row[1].split(',')
    number3 = row[2].split(',')
    number4 = row[3].split(',')
    
    print(int(number1[0]), int(number1[1]))
