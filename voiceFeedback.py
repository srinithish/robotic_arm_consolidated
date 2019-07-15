# -*- coding: utf-8 -*-


from gtts import gTTS 
from playsound import playsound




def generateAudioClip(text,filepath):
    
    
    language = 'en'
  

    myobj = gTTS(text=text, lang=language, slow=False) 
    myobj.save(filepath)
    
    
    pass
    
    
def playClip(filepath):
    
    playsound(filepath,block = True)
    
    pass


if __name__ == '__main__':
    
    generateAudioClip('Got it, getting you the object requested','./audioCaptures/gotIt.mp3')
    generateAudioClip('Located the object','./audioCaptures/locatedObj.mp3')
    generateAudioClip('The drone may now take off','./audioCaptures/droneTakeoff.mp3')
    generateAudioClip('Sorry didnt get that.Can you say the once again','./audioCaptures/didntGetThat.mp3')
    generateAudioClip('Hello rich, racist, Juan Huerta! Good day!','./audioCaptures/Juan.mp3')
    
    
    
    
    
    
    
    
    