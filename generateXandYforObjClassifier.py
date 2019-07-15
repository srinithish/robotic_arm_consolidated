# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:19:56 2019

@author: AI Lab
"""

import os 
import glob
import cv2
import pickle
import collections as col


classMappingDict = {'apple':0,'cucumber':1,'carrot':2} ## add more labels as needed

def generateXandY(folderPath,classMappingDict):
    
    
    listOfFiles = sorted(glob.glob(folderPath +"*.jpg"))
    

    dictOfXandY = col.defaultdict(list)
    
    for inpfile in listOfFiles:
        
        baseFileName = os.path.basename(inpfile)
        basefileName_noext,extension = os.path.splitext(baseFileName)
        
        Label,frameNum = basefileName_noext.split('_')
        imgArray = cv2.imread(inpfile)
        
        dictOfXandY['fileName'].append(baseFileName)
        dictOfXandY['X'].append(imgArray)
        dictOfXandY['Labels'].append(Label)
        dictOfXandY['Y'].append(classMappingDict[Label])
    
    return dictOfXandY
        
dictOfXandY = generateXandY('./imageCaptures/',classMappingDict)



def pickleObj(obj,outputFile):
    with open(outputFile, 'wb') as f:
        pickle.dump(obj, f)
        f.close()


pickleObj(dictOfXandY,'./pickledXandY/All_test.pkl')

dictOfXandY['X'][0].shape
