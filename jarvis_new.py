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
        responses = intents[intent]['responses']
        response = random.choice(responses)
        speak(response)

    else:
        speak("AI Assistant: Sorry, I'm not sure how to respond to that. Try Again!")
