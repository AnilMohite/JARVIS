import pyttsx3
import speech_recognition as sr
import random
import warnings
warnings.simplefilter('ignore')

def speak(text):
    engine = pyttsx3.init()
    voice_id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    engine.setProperty('voice', voice_id)
    print(f"==> Jarvis AI : {text}")   
    print("") 
    engine.say(text=text)
    engine.runAndWait()

def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        r.pause_threshold = 1
        audio = r.listen(source,0,8)

        try:
            print('Recognizing....')
            query = r.recognize_google(audio, language='en')   
            print("")         
            print(f"==> Anil : {query}")
            return query.lower()
        except:
            return ""

def mainExecution(query):
    Query = str(query).lower()

    if "hello" in Query:
        speak("Hi Anil, Welcome Back!")
    
    elif "bye" in Query:
        speak("Nice to meet you bro, Have a nice day!")

    elif "time" in Query:
        from datetime import datetime
        time = datetime.now().strftime("%I:%M %p")
        speak(f"The time now is  : {time}")

print("")
print("==> Jarvis AI: Hello! How can I assist you?")
print("")
while True:
    # query = str(input("Enter Query: "))
    query = speechrecognition()
    mainExecution(query)
