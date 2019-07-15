# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:29:22 2019

@author: GELab
"""

import vlc
import makeInference
import cv2
import matplotlib.pyplot as plt
import os 
from gtts import gTTS 
from playsound import playsound


vidCapHandle = makeInference.initVidCap(camNum=1)
testImg = makeInference.getFrame(vidCapHandle,mirror=True)
cv2.imwrite('test.jpg',testImg)



arr = plt.imread("./test.jpg")
plt.imshow(arr)

plt.figure()


vidCapHandle.release()

dominantHSV = [112.84615384615384, 64.23076923076923, 171.30769230769232]
#[111.0, 131.7, 114.8]

# The text that you want to convert to audio 
mytext = 'Got it getting you the object'
  
# Language in which you want to convert 
language = 'en'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=mytext, lang=language, slow=False) 
# Saving the converted audio in a mp3 file named 
# welcome  
file = "welcome.mp3"


myobj.save("welcome.mp3")
 
playsound("welcome.mp3",block = False)

