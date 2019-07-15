# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 08:18:50 2019

@author: GELab
"""


import makeInference
import track
import cv2 as cv

import os 
import numpy as np
import collections as col
import localize
import matplotlib.pyplot as plt
import track

import arduinoToPythonComm
import time
import voiceFeedback

def pixelsToCoords(armCenterPx, objCenterPx):
    
    """
    armCenterPx : tuple of (pX,pY)
    objCenterPx : tuple of (pX,pY)
    """
    
    scale = 400/170; ## mm per pixel
    
    armCenterPx = np.array(armCenterPx)
    objCenterPx = np.array(objCenterPx)
    
    movementReqInPx = armCenterPx - objCenterPx
    movementReqInCords = scale*movementReqInPx
    
    
    
    return [1,-1]*movementReqInCords




def adjustToRequiredPos(vidCapHandle,robotObj,objPixelPos):
    
    ### trap and completely achieve the robot at the required position
#    scaleX = 400/170
    scaleX = 1040/425
    
#    scaleY = 400/250
    scaleY = 1220/470
    
    
    pixelTolerance = 5
    
    while True:
        
        gripPixelPosns = []
        for i in range(5):
            frame = makeInference.getFrame(vidCapHandle,mirror=True)
            gripPixelPos = track.getCenterOfGripper(frame)
            gripPixelPosns.append(gripPixelPos)
        
        
        
        avgGripPixelPos = np.mean(gripPixelPosns, axis=0)
        
        print('avg pixel grip pos : ' ,avgGripPixelPos)
        
        pixelDiff = objPixelPos - avgGripPixelPos
        
        pixelDiff = [-1,1]*pixelDiff ## actual movement required
        
        print(np.abs(pixelDiff)<pixelTolerance)
        
        
        
        newCords,newAngles = robotObj.getPosition()
        
        
        if np.all(np.abs(pixelDiff)<pixelTolerance): ##pixel tolerance of the centers
            
            break
        
        
        
        
        ### adjust x
        
        
        if np.abs(pixelDiff[0])>pixelTolerance: ## check x
            
            
#            newCords = newCords[:2] + [2,0]*np.sign(pixelDiff)
            newCords = newCords[:2] + [scaleX/3,0]*pixelDiff## change x
            robotObj.reachPosWithoutApp(newCords[0]  ,newCords[1],50)
            ##update cords
            
        ### adjust y
        
        if np.abs(pixelDiff[1])>pixelTolerance: ## check y
            
            
#            newCords = newCords[:2] + [0,2]*np.sign(pixelDiff) #change y
            newCords = newCords[:2] + [0,scaleY/3]*pixelDiff## change x
            robotObj.reachPosWithoutApp(newCords[0]  ,newCords[1],50)
        
        
def performActionWrapper(vidCapHandle,myRobot,requiredPosInPx,robotCenter = (320,450)):
    
    
    
    
    myRobot.resetToHome()
    
    coords = pixelsToCoords(robotCenter,requiredPosInPx)
    myRobot.reachPosWithoutApp(coords[0]  ,coords[1],100) ## reach approx position
    
    
    
     
        
    adjustToRequiredPos(vidCapHandle,myRobot,requiredPosInPx)
    
    
    
    curCords,angles = myRobot.getPosition()
    myRobot.reachPosWithoutApp(curCords[0]  ,curCords[1],-35)
    myRobot.hold(70)
    ##ateempt twice
    myRobot.hold(70)
    myRobot.reachPosWithoutApp(curCords[0]  ,curCords[1],200)
    
    time.sleep(3)
    
    myRobot.reachPosWithoutApp(curCords[0]  ,curCords[1],-35)
    myRobot.hold(20)
    
    myRobot.reachPosWithoutApp(curCords[0]  ,curCords[1],200)
    
    myRobot.resetToHome()
    time.sleep(3)
    pass
    
def pickAndDropInDroneAction(vidCapHandle,myRobot,requiredPosInPx,dronePositionInPx,robotCenter = (325,450)):
    
    
    myRobot.resetToHome()
    
    coords = pixelsToCoords(robotCenter,requiredPosInPx)
    myRobot.reachPosWithoutApp(coords[0]  ,coords[1],70) ## reach approx position
    
    
    
     
    
    adjustToRequiredPos(vidCapHandle,myRobot,requiredPosInPx)
    
    
    
    curCords,angles = myRobot.getPosition()
    myRobot.reachPosWithoutApp(curCords[0]  ,curCords[1],-30)
    myRobot.hold(70)
    myRobot.hold(70)
    _,_ = myRobot.getPosition()
    
    myRobot.reachPosWithoutApp(curCords[0]  ,curCords[1],200)
    
    
    
    voiceFeedback.playClip('./audioCaptures/locatedObj.mp3')
    ### got to drone and drop it
#    adjustToRequiredPos(vidCapHandle,myRobot,dronePositionInPx)
    curCords,angles = myRobot.getPosition()
    myRobot.reachPosWithoutApp(-200  ,-150,180) ##150
    
    myRobot.hold(20) ## release
    
#    myRobot.reachPosWithoutApp(-200  ,-150,180)
    
    myRobot.resetToHome()
    
    voiceFeedback.playClip('./audioCaptures/droneTakeoff.mp3')
    time.sleep(3)
    
    
    pass



def makeCoffee(myRobot):
    
    #        150,-350,200,0
#    myRobot.resetToHome()
    print(myRobot.reachPosWithApp(-100,-375,50,0))
    pass




if __name__ == '__main__':
    
    
    ## test with vid cap
#    requiredPosInPx = (232,336)
#    vidCapHandle = makeInference.initVidCap(camNum=1)
#    myRobot = arduinoToPythonComm.robot_arm()
#    myRobot.switchOn()
#    performActionWrapper(vidCapHandle,myRobot,requiredPosInPx)
#    
#    vidCapHandle.release()
    
    
    
    
    ### test general
    
    myRobot = arduinoToPythonComm.robot_arm()
    myRobot.switchOn()
#    makeCoffee(myRobot)
    
    myRobot.reachPosWithApp(-100,-375,50,0)
    myRobot.hold(70)
    
    myRobot.reachPosWithApp(-100,-375,200,0)
    for i in range(200,70,-10):
        myRobot.reachPosWithApp(-100,-375,i,0)
    myRobot.hold(10)
    
    
    myRobot.closeSerial()
    