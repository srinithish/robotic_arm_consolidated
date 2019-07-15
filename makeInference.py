# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:34:35 2019

@author: AI Lab
"""

import cv2 as cv

import os 
import numpy as np
import collections as col
import localize
import matplotlib.pyplot as plt
import track
import makeInference
import arduinoToPythonComm
import time
def enumerateObjects(Label,classMappingDict):
    
    reverseMappingDict = {value:key for key,value in classMappingDict.items()}
    enumeratedObjs = col.Counter(Label)
    enumeratedObjs ={reverseMappingDict[key]:value for  key,value in enumeratedObjs.items() if value != 0}
    
    
    return enumeratedObjs

def initVidCap(camNum=0):
    vidCapHandle = cv.VideoCapture(camNum)
    return vidCapHandle
    
    
def getFrame(vidCapHandle,mirror=False):
    ret_val, img = vidCapHandle.read()
    if mirror: 
        img = cv.flip(img, 1)
        
    return img

def showFrame(img,text):
    
    
    font                   = cv.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (250,200)
    fontScale              = 0.5
    fontColor              = (255,255,255)
    lineType               = 2
    
    
    
    cv.putText(img,str(text), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    cv.imshow('LiveFeed', img)
    
    pass





def getObjectsFromTestImg(imgArray):
    
    
    
    ##takes in orginal img array 

    (objects, rectangles) = localize.localize(imgArray)
    
    
    
    listOfObjArr = []
    
    filteredObjs = []
    filteredRects = []
    
    for obj,rect in zip(objects,rectangles):
    
        
        croppedImageOfObj = imgArray[obj.ymin:obj.ymax,obj.xmin:obj.xmax]
        
        if  croppedImageOfObj.size != 0:
            resizedImg = cv.resize(croppedImageOfObj,(28,28))
            
            listOfObjArr.append(resizedImg)
            filteredObjs.append(obj)
            filteredRects.append(rect)
        
    return listOfObjArr,filteredObjs,filteredRects



def putTextWrap(imgArray,text,location):
    
    
    ##location (width,height)
    
    font                   = cv.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = location
    fontScale              = 0.5
    fontColor              = (255,255,255)
    lineType               = 2
    
    
    
    cv.putText(imgArray,str(text), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    return imgArray
    
    

def drawBoxesAndText(imgArray,objects,rectangles,Labels,probs,classMappingdict):
    
    
    ##need to send cropped image here
    
    reverseMappingDict = {value:key for key,value in classMappingdict.items()}
    
    LabelsAsStr  = [reverseMappingDict[i] for i in Labels]
    
    for obj,Label,prob in zip(objects,LabelsAsStr,probs):
    
        
       centerY = (obj.ymin+obj.ymax)//2
       centerX = (obj.xmin+obj.xmax)//2
       
       center = (centerX,centerY)
       
       if prob < 0.8:
           Label = 'Unknown'
       
       text = Label + ' '+ str(round(prob*100,1))
       putTextWrap(imgArray,text,center)
        
    for r in rectangles:
    
        cv.drawContours(imgArray, [r], -1, (0, 255, 0), 2)
    
    
    
    return imgArray
    
    

def getCenters(imgArray,objects,rectangles,Labels,probs,classMappingdict):
    
    
    reverseMappingDict = {value:key for key,value in classMappingdict.items()}
    
    LabelsAsStr  = [reverseMappingDict[i] for i in Labels]
    
    
    LabelAndCenters = {}
    
    
    for obj,Label,prob in zip(objects,LabelsAsStr,probs):
    
        
       centerY = (obj.ymin+obj.ymax)//2
       centerX = (obj.xmin+obj.xmax)//2
       
       center = (centerX,centerY)
       
       if prob < 0.8:
           Label = 'Unknown'
       
        
        
       LabelAndCenters[Label] = center
       
       
    
    
    return LabelAndCenters






    

    
    



    
    


if __name__ == '__main__':
    
    vidCapHandle = makeInference.initVidCap(camNum=1)
    
    myRobot = arduinoToPythonComm.robot_arm()
    myRobot.switchOn()
    myRobot.resetToHome()
    requiredPosInPx = (232,336)
    coords = pixelsToCoords((298,448),requiredPosInPx)
    myRobot.reachPosWithoutApp(coords[0]  ,coords[1],50)
    
    
    
     
        
    adjustToRequiredPos(vidCapHandle,myRobot,requiredPosInPx)
    
    vidCapHandle.release()
    
    cords,angles = myRobot.getPosition()
    myRobot.reachPosWithoutApp(cords[0]  ,cords[1],-40)
    myRobot.hold(70)
    myRobot.reachPosWithoutApp(cords[0]  ,cords[1],200)
    