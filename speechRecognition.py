#Python 2.x program for Speech Recognition 
  
import speech_recognition as sr 
import re
  
#enter the name of usb microphone that you found 
#using lsusb 
#the following name is only used as an example 
mic_name = "Microphone (Realtek Audio)"
#Sample rate is how often values are recorded 
sample_rate = 48000
#Chunk is like a buffer. It stores 2048 samples (bytes of data) 
#here.  
#it is advisable to use powers of 2 such as 1024 or 2048 
chunk_size = 2048
#Initialize the recognizer 
r = sr.Recognizer() 
  
#generate a list of all audio cards/microphones 
mic_list = sr.Microphone.list_microphone_names() 
  
#the following loop aims to set the device ID of the mic that 
#we specifically want to use to avoid ambiguity. 
for i, microphone_name in enumerate(mic_list): 
    if microphone_name == mic_name: 
        device_id = i 
  
#use the microphone as source for input. Here, we also specify  
#which device ID to specifically look for incase the microphone  
#is not working, an error will pop up saying "device_id undefined" 
        
        
def parseSpokenText(possibleObjs):
    
    
    dictOfMapping = {'pepper': 'serrano','carrot': 'carrot', 'marshmallow':'marshmallow','':None}
    
    with sr.Microphone(sample_rate = sample_rate,  
                            chunk_size = chunk_size) as source:
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source) 
        print("Say Something")
        #listens for the user's input 
        
        
        recognisedObj = ''
        
        try: 
            audio = r.listen(source,timeout= 6) 
            text = r.recognize_google(audio) 
            print ("you said: " ,text)
#            m = re.match("(?:Hello|Hey).*(?:robot|bot).*(?:get|give).*me (.*)", 
#                         text,re.IGNORECASE)   
            
            m = re.match(".*(carrot|pepper|marshmallow).*", 
                         text,re.IGNORECASE)
            
            
            if m.group(1) in possibleObjs:
                print ("Object is " ,m.group(1))
                recognisedObj  = m.group(1)
                
            
        #error occurs when google could not understand what was said 
          
#        except sr.UnknownValueError as e: 
#            print("Google Speech Recognition could not understand audio") 
#            
#        
#        except sr.WaitTimeoutError:
#            print("Google Speech Recognition timeout error") 
#            
#            
#        
#        except sr.RequestError as e: 
#            print("Could not request results from Google\
#                                     Speech Recognition service {}".format(e)) 
        
        except Exception as e :
        
            print(e)
#            
        finally:
            
            return dictOfMapping[recognisedObj]
        
            
if __name__ == '__main__' :
    
    print(parseSpokenText(['carrot','pepper','marshmallow']))
         


