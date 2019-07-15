# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:02:23 2019

@author: GELab
"""

import pickle
import os 
import cv2 as cv 
import matplotlib.pyplot as plt
import collections as col
from ImgObjClass import Item,Img
import DatabaseOps
import captureImages
import time 
from datetime import datetime
import re
import label
import glob
import take_picture


def capture_save_by_frame(saveFolder,Label,capFrames = 200,camNum=0):
    
    
    print('Make sure to remove all other objects except the one you want to train')
    
    vidCap = cv.VideoCapture(camNum) ## from camera
    
    time.sleep(5)
    
    createdFileNameList = []
    
    capturedFrames = 0
    while capturedFrames <= capFrames:
        
    
        
        print('picture number : ',capturedFrames)
        time.sleep(1)
        ret_val, img = vidCap.read()
        

        
        img = cv.flip(img, 1)
        
        boolTakePic = take_picture.take_picture(img)
        print("picture taken ",boolTakePic)
#            img = cv.resize(img, (300, 300)) 
#        uniqueID = int(time.mktime(datetime.now().timetuple()))
        
        
        if boolTakePic == True:
            
            capturedFrames +=1
            uniqueID = re.sub('(?:\W+)','_',str(datetime.now()))
            fileName = Label + "_" + uniqueID+'.jpg'
            
            createdFileNameList.append(os.path.join(saveFolder,fileName))
            
            
            cv.imwrite(os.path.join(saveFolder,fileName),img)
        

    cv.destroyAllWindows()  
    
    print('all done')
    
    return createdFileNameList
    

if __name__ == '__main__':

    Label = 'marshmallow' ### to be passed from cmd line args
    saveFolder = './imageCaptures/images'
    
    
    
    fileListCreated = capture_save_by_frame(saveFolder = saveFolder,
                                            Label = Label,capFrames = 20,camNum=1)
    
    

    
    
    
#    fileListCreated = [saveFolder+'/'+fileName for fileName in fileListCreated]
    
    fileListCreated = glob.glob('./imageCaptures/images/marshmallow*')
    
    imgObjList = label.label_imgs(fileListCreated, Label)
    
    ##db update
    DatabaseOps.dbInsertWrapper(imgObjList)
    
    







