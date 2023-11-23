import pyttsx3
import speech_recognition as sr

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

def MainExecution(query):
    query = query.lower()
    if "hello" in query:
        speak('Hi sir, welcome back!')

    elif "bye" in query:
        speak('Nice to see you...')

while True:
    query = speechrecognition()
    MainExecution(query)
