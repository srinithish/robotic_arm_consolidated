# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:30:11 2019

@author: GELab
"""

import numpy as np




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
    
    return -movementReqInCords
    
    

if __name__ == '__main__':
    pixelsToCoords((294,444),(324,280))  
    