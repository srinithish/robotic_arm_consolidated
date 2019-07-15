# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:34:42 2019

@author: AI Lab
"""

import cv2 as cv

import os 

import time 
class camOpertations():
    
    def __init__(self):
        
        pass
    
    
    def capture_save_by_frame(self,saveFolder,Label,capFrames = 200,camNum=0,startFrom = 0):
        
        vidCap = cv.VideoCapture(camNum) ## from camera
        
        
        
        for frameNum in range(capFrames):
            
            
            
            print('3 seconds for a picture',frameNum)
            time.sleep(3)
            ret_val, img = vidCap.read()
            print("picture taken")
            
            img = cv.flip(img, 1)
#            img = cv.resize(img, (300, 300)) 
            fileName = Label + "_" + str(startFrom+frameNum)+'.jpg'
            
            
            
            
            
            
            cv.imwrite(os.path.join(saveFolder,fileName),img)
            

        cv.destroyAllWindows()  
        
        print('all done')
        

    def show_cam(self,mirror=False,camNum=0):
        vidCap = cv.VideoCapture(camNum)
#        print(vidCap.get(cv.CAP_PROP_FPS))
        scale  = 50
        while True:
            ret_val, img = vidCap.read()
            if mirror: 
                img = cv.flip(img, 1)
                
                
                
            #get the webcam size
            height, width, channels = img.shape

            #prepare the crop
            centerX,centerY=int(height/2),int(width/2)
            radiusX,radiusY= int(scale*height/100),int(scale*width/100)

            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY

            cropped = img[minX:maxX, minY:maxY]
            resized_cropped = cv.resize(cropped, (width, height)) 
                
                
                
            cv.imshow('Reading Cam', resized_cropped)
            if cv.waitKey(1) == 27: 
                break  # esc to quit
                

                
        cv.destroyAllWindows()
        vidCap.release()    
    
    
 
    
    

    

if __name__ == '__main__':

    camOps = camOpertations()
    camOps.capture_save_by_frame(saveFolder = './imageCaptures',
                                 Label = 'TestImgsAll',capFrames = 5,camNum=1,startFrom=5)
#
#    camOps.show_cam(camNum = 1 )

