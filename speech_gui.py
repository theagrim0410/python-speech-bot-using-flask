import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import yt_dlp
import requests
import os
import shutil
import numpy as np
import cv2


def say(text):

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def take():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand. Please try again.")
            return ""
        except sr.RequestError:
            say("Network error. Please check your connection.")
            return ""


def wishme():

    now = datetime.datetime.now()
    hour = now.hour
    if 4 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 16:
        greeting = "Good Afternoon"
    elif 16 <= hour < 20:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    say(f"{greeting}, sir.")


def chat():

    try:
        genai.configure(api_key="AIzaSyB0sGG0nbpqotG0NXzDi50KteUp7mGD3-A")
        model = genai.GenerativeModel("gemini-2.0-flash")
        chat_session = model.start_chat(history=[])

        say("If you want to exit, just say 'quit' or 'exit'.")

        while True:
            text = take()
            if text in ["exit", "quit"]:
                say("Okay sir, let's restart.")
                return

            if text:
                response = chat_session.send_message(text)
                say(response.text)

    except Exception as e:
        say("An error occurred in chat mode.")
        print(f"Error: {e}")


def playsongs(query):
    search_url = f"ytsearch1:{query}"

    try:
        ydl_opts = {

            "quiet": True,
            "default_search": "ytsearch",
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["webpage_url"]
                say(f"Sir wait playing {query} song")

                # Update if needed
                brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
                webbrowser.register(
                    "brave", None, webbrowser.BackgroundBrowser(brave_path))
                webbrowser.get("brave").open(video_url)

            else:
                say("Sorry sir this song is not found")

    except Exception as e:
        say("Sir some error occured")
    return


def google(query):
    say("searching s")
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    return


def weather(city):
    try:
        api_weather = "7f3c63f98ed248e5a4271257252002"
        url_weather = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": api_weather,
            "q": city,
            "aqi": "no"
        }

        response = requests.get(url_weather, params=params)

        if response.status_code == 200:
            data = response.json()

            location = data['location']['name']
            temp_c = data['current']['temp_c']
            condition = data['current']['condition']['text']
            humidity = data['current']['humidity']

            say(f"temperature in {location} is {temp_c} degree celcius condition is {condition} and humidity is {humidity}")

        else:
            say("sir city is not found")

    except Exception as e:
        say("sir some error occurred")

    return


def app(app_name):

    if "calculator" in app_name:
        app_path = "calc.exe"  # update if needed
    else:
        app_path = shutil.which(app_name)

    if app_path:
        say(f"sir opening the{app_name}")
        os.startfile(app_path)
    else:
        say("sir application not found")

    return

def face():
    say("hello agrim sir")
    cascade_path = cv2.data.haarcascades
    face_cascade = cv2.CascadeClassifier(os.path.join(cascade_path, 'haarcascade_frontalface_default.xml'))
    eye_cascade = cv2.CascadeClassifier(os.path.join(cascade_path, 'haarcascade_eye.xml'))

    cap = cv2.VideoCapture(0)

    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        cv2.imshow('img',img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            requests.get("http://127.0.0.1:5000/shutdown")
            break

    cap.release()
    cv2.destroyAllWindows()
    return
    
    
def main():

    say("Hello, I am Lalli, the A I i am here to assist you")

    while True:
        text = take()

        if not text:
            continue

        if "open" in text: # open instagram
            word = text.split()
            if len(word) > 1:
                website = "".join(word[1:])

            say(f"Opening {website}")
            webbrowser.open(f"https://www.{website}.com")
            site_found = True
            requests.get("http://127.0.0.1:5000/shutdown")
            break

        elif "the time" in text: #the time lalli
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {current_time}")

        elif "let us talk" in text: #let us talk lalli
            say("Yes sir, let's begin.")
            chat()

        elif "what is your name" in text: # what is your name
            say("Sir, my name is  Lalli developed by agrim saxena")

        elif "wish me" in text: #wish me lalli
            wishme()

        elif "show my songs" in text: #show my song lalli
            say("okey sir showing")
            webbrowser.open(
                "https://open.spotify.com/playlist/44kMHX5eWfaJmtHab86mBm")
            requests.get("http://127.0.0.1:5000/shutdown")
            break

        elif "play" in text: #play tum hi ho
            word = text.split()
            if len(word) > 1:
                song = " ".join(word[1:])

            else:
                song = "songs"

            playsongs(song)
            requests.get("http://127.0.0.1:5000/shutdown")
            break

        elif "search" in text: #search apple in google
            word = text.split()
            if len(word) > 2:
                prompt = " ".join(word[1:-2])
                google(prompt)
                requests.get("http://127.0.0.1:5000/shutdown")
                break
            else:
                say("sir what to search")

        elif "weather" in text or "tempreture" in text: #weather in bareilly
            word = text.split()
            if len(word) > 2:
                city = " ".join(word[2:])
                weather(city)
            else:
                say("sir tell the city name")

        elif "app" in text or "application" in text: #application calculator
            word = text.split()
            if len(word) > 1:
                app_name = " ".join(word[1:])
                app(app_name)
                requests.get("http://127.0.0.1:5000/shutdown")
                break
            else:
                say("sir application not found")
                
        elif "detect me" in text: #detect me lalli
            say("Sir detecting you ,to close press q")
            face()
            requests.get("http://127.0.0.1:5000/shutdown")
            break
        
        # add 2 and 3 lalli
        
        elif "add" in text: 
            word = text.split()
            if len(word) == 4:
                num1 = int(word[1])
                num2 = int(word[3])
                say(f"Sir the sum is {str(num1+num2)}")
            else:
                say("wrong inputs")
        elif "subtract" in text:
            word = text.split()
            if len(word) == 4:
                num1 = int(word[1])
                num2 = int(word[3])
                say(f"Sir the difference is {str(num1-num2)}")
            else:
                say("wrong inputs")
        elif "multiply" in text:
            word = text.split()
            if len(word) == 4:
                num1 = int(word[1])
                num2 = int(word[3])
                say(f"Sir the multiplication is {str(num1*num2)}")
            else:
                say("wrong inputs")
            say(str(num1+num2))
        elif "divide" in text:
            word = text.split()
            if len(word) == 4:
                num1 = int(word[1])
                num2 = int(word[3])
                if num2 == 0:
                    say("sorry cannot divide")
                elif num2 != 0:
                    say(f"Sir the division is {str(num1//num2)}")
            else:
                say("wrong inputs")

        elif "what you can do" in text: #what you can do lalli
            say('''I Can do many things 
            1 i can open a website
            2 i can tell my name
            3 i can chat with you as chat bot
            4 i can open the applications
            5 i can play any songs
            6 i can wish you
            7 i can tell the weather conditions
            8 i can do simple calculations of four main operations
            9 i can tell you the current time
            10 i can search on google
            ''')

        elif "exit please" in text: #exit please yar
            say("Okay sir, exiting.")
            requests.get("http://127.0.0.1:5000/shutdown")
            break


if __name__ == '__main__':
    main()

