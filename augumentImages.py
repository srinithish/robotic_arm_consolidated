# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:31:07 2019

@author: GELab
"""

import Augmentor

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



saveFolder = './imageCaptures/objImages'
dictOfImgAndObjs = pickle.load(open('./Data/AllObjectLevelData.pkl','rb'))



for fileName,imgArray in zip(dictOfImgAndObjs['FileNames'],dictOfImgAndObjs['X']):
    uniqueID = re.sub('(?:\W+)','_',str(datetime.now()))
    
    
    cv.imwrite(os.path.join(saveFolder,uniqueID+'_'+fileName),imgArray)
    
    

p = Augmentor.Pipeline(saveFolder)

p.rotate90(probability=0.5)
p.rotate270(probability=0.5)
p.flip_left_right(probability=0.5)
p.flip_top_bottom(probability=0.5)
p.random_distortion(probability=0.5, grid_width=28, grid_height=28, magnitude=1)
p.shear(probability = 0.5,max_shear_left = 10,max_shear_right = 10)

p.sample(100)
