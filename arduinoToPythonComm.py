# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:09:12 2019

@author: GELab
"""

import serial
import time
# "COM11" is the port that your Arduino board is connected.set it to port that your are using        
import re

import numpy as np

class robot_arm():
    
    def __init__(self,com = "COM21" ):
        
        try:
            
            self.ser = serial.Serial(com, 9600,timeout= 5)
        
        except Exception as e :
            
            print(e)
    
    
    def switchOn(self):
        self.ser.write("Power_On".encode('utf-8'))
        return self.ser.readline()
        
    def getPosition(self):
        
        self.ser.write("Get_Position".encode('utf-8'))
        
        
        retString = self.ser.readline() 
        asStr = retString.decode('ASCII')
        
        m = re.match("isSwitchedOn : (.*) The current cords are: (.*) and angles are (.*)", asStr)
        
        
        coords = np.float16(m.group(2).split(';'))
        angles = np.float16(m.group(3).split(';'))
        
        return coords,angles
        
    
    def reachPosWithoutApp(self,x,y,z):
        
        self.ser.write("POS_WithoutApp,{},{},{}".format(x,y,z).encode('utf-8'))
        
        
        
        return self.ser.readline()
        
        
    def reachPosWithApp(self,x,y,z,appAngle):
#        150,-350,200,0
        self.ser.write("POS_WithApp,{},{},{},{}".format(x,y,z,appAngle).encode('utf-8'))
        return self.ser.readline()


    def hold(self,angle):
        self.ser.write("Hold,{}".format(angle).encode('utf-8'))
        return self.ser.readline()

    
    
    def resetToHome(self):
#        a0 = 0, a1 = 90 , a2 = 0 , a3 = 0, a4 =0, a5 = 20;    
        self.ser.write("SetAngles,{},{},{},{},{},{}".format(0,90,0,0,0,10).encode('utf-8'))
        return self.ser.readline()
        
    def switchOff(self):
        
        self.ser.write("Power_Off".encode('utf-8'))
        self.ser.readline()
        
        
    def closeSerial(self):
        self.ser.close()
        


if __name__ == '__main__':
    
    myRobot = robot_arm()
    myRobot.switchOn()
    myRobot.resetToHome()
    myRobot.reachPosWithoutApp(142  ,-277,0)
    
    a,b = myRobot.getPosition()
    
    for i in range(5):
        myRobot.hold(72)
        
        myRobot.hold(20)
        
        myRobot.hold(72)
    
  
    myRobot.closeSerial()
#    myRobot.resetToHome()
  
    
#    myRobot.closeSerial()




