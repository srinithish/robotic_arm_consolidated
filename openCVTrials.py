# -*- coding: utf-8 -*-
"""
Created on Mon May 20 15:54:35 2019

@author: GELab
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import imutils
img = cv2.imread('./imageCaptures/AllTrails_2.jpg',0)
edges = cv2.Canny(img,100,200)
edges = cv2.GaussianBlur(edges,(7,7),0)
#plt.subplot(121),plt.imshow(img,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.imshow(edges)
plt.figure()


img = cv2.imread('./imageCaptures/AllTrails_3.jpg',0)
equ = cv2.equalizeHist(img)
#res = np.hstack((img,equ)) #stacking images side-by-side
edges = cv2.Canny(equ,100,200)
plt.imshow(edges)


lookUpTable = np.empty((1,256), np.uint8)
for i in range(256):
    lookUpTable[0,i] = np.clip(pow(i / 255.0, 0.4) * 255.0, 0, 255)
res = cv2.LUT(img, lookUpTable)
edges = cv2.Canny(equ,100,200)
plt.imshow(edges)



kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

fgmask = fgbg.apply(img)
fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
plt.imshow(fgmask)



img = cv2.imread('./imageCaptures/images/apple_1.jpg',0)
BgmImg1 = cv2.imread('./imageCaptures/EmptyTable_1.jpg',0)
BgmImg2 = cv2.imread('./imageCaptures/EmptyTable_2.jpg',0)
BgmImg3 = cv2.imread('./imageCaptures/EmptyTable_3.jpg',0)

BgmImg = np.mean( np.array([ BgmImg1, BgmImg2,BgmImg3 ]), axis=0 )
highlight = np.abs(img.astype(np.int)-BgmImg.astype(np.int))

np.median(highlight)

highlight[highlight > 20] =255
highlight[highlight < 20 ] = 0

highlight= highlight.astype(np.uint8)

cv2.imshow('dsfg',highlight)
plt.imshow(highlight,cmap = 'gray')

plt.close()

highlight.dtype
highlight.astype(np.uint8)
equ = cv2.equalizeHist(highlight)
#res = np.hstack((img,equ)) #stacking images side-by-side
edges = cv2.Canny(equ,100,200)
plt.imshow(edges)







BgmImg1 = cv2.imread('./imageCaptures/EmptyTable_1.jpg')
img = cv2.imread('./imageCaptures/AllTrails_2.jpg',0)
gray = cv2.cvtColor(BgmImg1, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)

frameDelta = cv2.absdiff(img, gray)
thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('sdf',thresh)
thresh = cv2.dilate(thresh, None, iterations=2)
cv2.imshow('sdf',thresh)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
