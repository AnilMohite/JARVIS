import pyttsx3
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import nltk
from sklearn.model_selection import train_test_split
import json
import warnings
warnings.simplefilter('ignore')
import random
import webbrowser
import os
import smtplib
import wikipedia

# first download nltk requied data 
# nltk.download("punkt")

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

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

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
    
    elif 'open youtube' in query:
        speak("opening youtube...")
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        speak("opening google...")
        webbrowser.open("google.com")

    elif 'open stack overflow' in query:
        speak("opening stackoverflow...")
        webbrowser.open("stackoverflow.com") 

    elif "open cmd" in query:
        speak("opening cmd...")
        os.system('start cmd')

    elif "email" in query:
        try:            
            speak("Whom to send? Email Please?")
            to = speechrecognition() 
            to = to.replace(" ","").strip()
            # to = "mohiteanil22@gmail.com"   
            speak("What should I say?")
            content = speechrecognition() 
            sendEmail(to, content)
            print(f"To : {to}, Email Content : {content}")
            speak("Email has been sent! with")
        except Exception as e:
            print(e)
            speak("Sorry my friend Anil bhai. I am not able to send this email") 

    if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
    

# print("")
# print("==> Jarvis AI: Hello! How can I assist you?")
# print("")
# while True:
#     # query = str(input("Enter Query: "))
#     query = speechrecognition()
#     mainExecution(query)

# training data 
with open('./training_data.json','r') as f:
    intents = json.load(f)

training_data = []
labels = []

for intent , data in intents.items():
    for pattern in data['patterns']:
        training_data.append(pattern.lower())
        labels.append(intent)

Vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize,stop_words="english",max_df=0.8,min_df=1)
X_train = Vectorizer.fit_transform(training_data)
X_train,X_test,Y_train,Y_test = train_test_split(X_train,labels,test_size=0.4,random_state=42,stratify=labels)

model = SVC(kernel='linear', probability=True, C=1.0)
model.fit(X_train, Y_train)

predictions = model.predict(X_test)

def predict_intent(user_input):
    user_input = user_input.lower()
    input_vector = Vectorizer.transform([user_input])
    intent = model.predict(input_vector)[0]
    return intent

print("AI Assistant: Hello! How can I assist you?")
while True:
    user_input = speechrecognition()
    if user_input.lower() == 'exit':
        print("AI Assistant: Goodbye!")
        break

    intent = predict_intent(user_input)
    if intent in intents:
        if intent == "open":
            mainExecution(user_input)
        else:
            responses = intents[intent]['responses']
            response = random.choice(responses)
            speak(response)

    else:
        speak("AI Assistant: Sorry, I'm not sure how to respond to that. Try Again!")
