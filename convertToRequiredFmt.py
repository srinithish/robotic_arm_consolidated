# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:12:00 2019

@author: GELab
"""

import pascal_voc_writer as xmlWriter
import pickle
import os 
import cv2 
import matplotlib.pyplot as plt
import collections as col
from ImgObjClass import Item,Img
import DatabaseOps




# Writer(path, width, height)






    
def getObjectsArrayAndLables(imgObject,classMappingDict,dirpath = './imageCaptures/images/'):
    listOfObjArr = []
    listOfLabels = []
    listOfIntLabel = []
    
    
    inpfile = dirpath+image.name
    imgArray = cv2.imread(inpfile)
    
    for obj in imgObject.objects:
    
        
        croppedImageOfObj = imgArray[obj.ymin:obj.ymax,obj.xmin:obj.xmax]
        resizedImg = cv2.resize(croppedImageOfObj,(28,28))
        
        listOfObjArr.append(resizedImg)
        listOfLabels.append(obj.label)
        listOfIntLabel.append(classMappingDict[obj.label])
        
        
    return listOfObjArr,listOfLabels,listOfIntLabel
    





if __name__ == '__main__':
    

   #for image in AllImgs:
    #    for obj in image.objects:
    #    
    #        temp = obj.xmin 
    #        obj.xmin = obj.xmax
    #        obj.xmax = temp
    #        
    #        
    #pickle.dump(AllImgs, open('./Data/AllCucumber.pickle','wb'))

###generate x and y
    
    
    dictOfImgAndObjs = col.defaultdict(list)
    conn = DatabaseOps.getConnection('ObjectsDB')
    
    
    unqLabels = DatabaseOps.getUniqueLabels(conn,'IMAGE_INFO')
    
    CLS_MAPPING_DICT = {strLabel:index for index,strLabel in enumerate(unqLabels)}
    
    pickle.dump(CLS_MAPPING_DICT,open('./Data/CLS_MAP_DICT.pkl','wb'))
    
    AllImgs = DatabaseOps.fetchImgObjs(conn,'IMAGE_INFO') ##table and connection
    
 
    
    for image in AllImgs:
        
        
    #    imageNameNoExt = os.path.splitext(os.path.basename(image.name))[0]
        try:
            dictOfImgAndObjs['FileNames'].append(image.name)
            dictOfImgAndObjs['X'].extend(getObjectsArrayAndLables(image,CLS_MAPPING_DICT)[0]) ## all x
            dictOfImgAndObjs['Label'].extend(getObjectsArrayAndLables(image,CLS_MAPPING_DICT)[1]) ##all labels
            dictOfImgAndObjs['Y'].extend(getObjectsArrayAndLables(image,CLS_MAPPING_DICT)[2])
        except Exception as ex:
            
            print('exception', ex, 'in ', image.name)
    
    pickle.dump(dictOfImgAndObjs,open('./Data/AllObjectLevelData.pkl','wb'))
    
    conn.commit()
    conn.close()