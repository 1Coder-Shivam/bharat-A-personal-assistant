import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import cv2
import pywhatkit
import smtplib
import sys
import time
import requests
import pyjokes
import json
import subprocess
from googlesearch import *
import wolframalpha

try:
    app = wolframalpha.Client("6KJ7LY-67LVA9RAGQ")
except Exception:
    print("Some Features are not work")


# sapi5-Microsoft developed speech API.Helps in synthesis and recognition of voice.
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')  # to grab the list of available voices.
# print(voices[1].id)
# voice[1].id = Male voice, voice[0].id = Female voice
engine.setProperty('voice', voices[1].id)


def speak(audio):  # speak function to convert our text to speech
    engine.say(audio)
    engine.runAndWait()


def wishMe():  # this function will make our BHARAT wish us according to current time.
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning sir!")
        print("Good Morning sir!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon sir!")
        print("Good Afternoon sir!")

    else:
        speak("Good Evening sir!")
        print("Good Evening sir!")

    speak("I am BHAARAT. Please tell how may I help you?")
    print("I am BHAARAT. Please tell how may I help you?")


def takeCommand():  # It takes microphone input from the user and returns string output

    # this requires PyAudio because it uses the Microphone class import speech_recognition
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # seconds of non-speaking audio before a phrase is considered complete
        r.pause_threshold = 1
        r.energy_threshold = 4000  # minimum audio energy to consider for recording
        # use the default microphone as the audio source
        audio = r.listen(source)

        try:
            # it recognize what user said and print it.
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:  # In case computer doesn't understand what user said.
            # print(e)
            print("Say that again please...")
            return "None"
        return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('skm1910.shivam@gmail.com', '8112939821')
    server.sendmail('skm1910.shivam@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while 1:

        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(result)
            speak(result)

        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            time.sleep(5)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Sir, What should I search on google")
            gg = takeCommand().lower()
            webbrowser.open(f"{gg}")

        elif 'open stack overflow' in query:
            webbrowser.open("www.stackoverflow.com")

        elif 'play' in query:
            song = query.replace('play', '')
            speak('playing' + song)
            pywhatkit.playonyt(song)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(strTime)

        elif 'date' in query:
            strTime = datetime.datetime.now().strftime("%Y/%m/%d")
            speak(f"the date is {strTime}")
            print(strTime)

        elif 'joke' in query:
            print(pyjokes.get_joke())
            speak(pyjokes.get_joke())

        elif 'today headlines' in query:
            news = webbrowser.open_new_tab(
                "https://timesofindia.indiatimes.com//home//headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif 'tell' in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("Internet connection error")

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "log off" in query or "sign out" in query:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

            time.sleep(3)

        elif "send email" in query:
            try:
                speak("to whom?")
                to = input()
                speak("What shoud I send?")
                content = takeCommand().lower()
                sendEmail(to, content)
                speak("Email has been sent!")

            except Exception as e:
                print(e)
                speak("sorry email can't be send")

        elif "weather" in query:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
                speak(" Temperature in kelvin unit is " + str(current_temperature) +
                      "\n humidity in percentage is " + str(current_humidiy) +
                      "\n description  " + str(weather_description))

            else:
                speak(" City Not Found ")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(5)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'who are you' in query or 'what can you do' in query:
            speak('I am Bharat, your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,stackoverflow, sending gmail  ,predict time,take a photo,search wikipedia,predict weather'
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')
            print('I am Bharat, your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,stackoverflow, sending gmail  ,predict time,take a photo,search wikipedia,predict weather'
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')

        elif "who made you" in query or "who created you" in query or "who discovered you" in query:
            speak("I was built by Shivam, Shaurya, Ritik and Satyam")
            print("I was built by Shivam, Shaurya, Ritik and Satyam")

        elif "no thanks" in query:
            speak("Thanks for using me sir, have a good day.")
            sys.exit()

        speak("sir , do you have any other work")
