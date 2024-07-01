import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()
news_api = os.getenv("NEWS_API_KEY")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
   tts = gTTS(text)
   tts.save('temp.mp3')

   pygame.mixer.init()

   pygame.mixer.music.load('temp.mp3')

   pygame.mixer.music.play()

   while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

   pygame.mixer.music.unload()

   os.remove("temp.mp3")

def processCommand(c):
   if "open google" in c.lower():
      webbrowser.open("https://google.com")
   elif "open facebook" in c.lower():
      webbrowser.open("https://facebook.com")
   elif "open twitter" in c.lower():
      webbrowser.open("https://twitter.com")
   elif "open linkedin" in c.lower():
      webbrowser.open("https://linkedin.com")
   elif "open youtube" in c.lower():
      webbrowser.open("https://youtube.com")
   elif c.lower().startswith("play"):
      song = c.lower().split(" ")[1]
      link = musicLibrary.music[song]
      webbrowser.open(link)

   elif "news" in c.lower():
      r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}")
      if r.status_code == 200:
         data = r.json()
         articles = data.get('articles', [])
         for article in articles:
            speak(article['title'])

   else:
       pass
      

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    # obtain audio from the microphone
    while True:
        r = sr.Recognizer()
        # recognize speech using Google
        print("Recognizing...")
        try:
          with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=2, phrase_time_limit=1)
          word = r.recognize_google(audio)
          if(word.lower() == "jarvis"):
             speak("Ya")
             with sr.Microphone() as source:
                print("Jarvis Active...")
                audio = r.listen(source)
                command = r.recognize_google(audio)

                processCommand(command)
                

        except Exception as e:
            print("Error; {0}".format(e))