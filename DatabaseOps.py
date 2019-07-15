# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:35:25 2019

@author: GELab
"""


###one thread do the follwing :

### need to first signal the data not being present
### then need to take pictures and save it in the folder with labels
### generate pickle with required format with convertToRequired and juans code
## restore the partial model and train before making an inference

###another thread keep inferencing
### merge thread when  training is done

import sqlite3
from datetime import datetime
import pickle
from ImgObjClass import Item,Img



def imgObjReverseDBConvertor(ImgObjStr):
    return pickle.loads(ImgObjStr)

sqlite3.register_adapter(Img, imgObjReverseDBConvertor)

###time functions


def getTimeObjFrmStr(timestampString):
    
    return datetime.strptime(timestampString, '%Y-%m-%d %H:%M:%S.%f')
    


def getConnection(database):
    conn = sqlite3.connect('./Database/'+database+'.db')
       
    return conn








# Insert a row of data
def insertIntoTable(conn,imageObj):
    
    queryStr = 'INSERT INTO IMAGE_INFO \
    (file_name,image_obj,obj_label,added_at_timestamp,used_by_model) \
    VALUES (?,?,?,?,?)' 
    
    
    
    if len(imageObj.objects) != 0: ## if there are no objects dont store
        
        
        fileName = imageObj.name
        
        pickledImgObj = pickle.dumps(imageObj)
        
        Label = imageObj.objects[0].label
        
        timestamp = str(datetime.now())
        
        used_by_model = ''
    
        values = (fileName,pickledImgObj,Label,timestamp,used_by_model)
    
    
    try :
    
        conn.execute(queryStr,values)
    
    except Exception as e:
        
        
        print(e, imageObj.name)
    
    
    
    return True




def fetchImgObjs(conn,fromTable):
    
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('select * from '+ fromTable)
    rows = cursor.fetchall()
    
    ImgObjects = [pickle.loads(row['image_obj']) for row in rows]
    
    
    
    return ImgObjects

def getUniqueLabels(conn,fromTable):
    
    cursor = conn.execute('select distinct obj_label from '+ fromTable)
    rows = cursor.fetchall()
    reqFormat = [tup[0] for tup in rows]
    return reqFormat
    
def dbInsertWrapper(imgObjList):
    
    conn = getConnection('ObjectsDB')
    
    
    for img in imgObjList:
        
        insertIntoTable(conn,img)
    
    
    
    # Save (commit) the changes
    conn.commit()
    
    conn.close()
    
    return True

if __name__ == '__main__':
    
    
    """
    # Create table
    conn.execute('''CREATE TABLE IMAGE_INFO
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 
                 file_name text UNIQUE,
                 image_obj blob, 
                 obj_label text, 
                 added_at_timestamp text, 
                 used_by_model text)''')
    


"""
    


    conn = getConnection('ObjectsDB')
    conn.execute("delete from IMAGE_INFO where obj_label like '%robot_arm%'")    

    
#    getUniqueLabels(conn,'IMAGE_INFO')

    AllImgs = pickle.load(open('./Data/AllCarrot.pickle','rb'))
    
    for img in AllImgs:
        
        insertIntoTable(conn,img)
    
    
    
    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    pass