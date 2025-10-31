import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import shutil
import requests
import cv2
import yt_dlp
import google.generativeai as genai
import numpy as np
import time


def say(text):

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    # Choose a voice safely (not all systems have multiple voices)
    try:
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        else:
            engine.setProperty('voice', voices[0].id)
    except Exception:
        pass
    engine.say(text)
    engine.runAndWait()


def take():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Shorter ambient noise adjustment to reduce wait time; tune as needed
        r.adjust_for_ambient_noise(source, duration=0.6)
        r.pause_threshold = 0.6
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
        # Read API key from environment for security and flexibility
        api_key = 'AIzaSyAoTnkF1HJ8e4Am9uOV_NPEvWAnXeBcl4w'
        if not api_key:
            say("Chat unavailable: API key not configured.")
            return
        genai.configure(api_key=api_key)
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
            "default_search": "ytsearch1",
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

                # Try opening in the default browser; fallback to Brave if that fails
                try:
                    webbrowser.open(video_url)
                except Exception:
                    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
                    try:
                        webbrowser.register(
                            "brave", None, webbrowser.BackgroundBrowser(brave_path))
                        webbrowser.get("brave").open(video_url)
                    except Exception:
                        say("Unable to open browser for the song.")

            else:
                say("Sorry sir this song is not found")

    except Exception as e:
        say("Sir some error occured")
    return


# Wake word configuration
WAKE_WORDS = ["hii lalli", "hi lalli", "hello", "hey lalli", "hii lali"]


def take_command(timeout=6, phrase_time_limit=6):
    """Listen for a single command after wake word. Returns lowercased text or empty string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = r.recognize_google(audio, language='en-in')
            print(f"Command heard: {command}")
            return command.lower()
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand. Please try again.")
            return ""
        except sr.RequestError:
            say("Network error. Please check your connection.")
            return ""
        except Exception:
            return ""


def google(query):
    say("Searching on Google")
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open_new_tab(search_url)
    return


def weather(city):
    try:
        # Allow using an environment variable for the weather API key
        api_weather =  '7f3c63f98ed248e5a4271257252002'
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
        app_path = "calc.exe"  
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
            break

    cap.release()
    cv2.destroyAllWindows()
    return
    
    
def main():
    """Run as a background wake-word listener. The assistant stays idle until the wake word is heard,
    then listens for a single command, handles it, and returns to sleep.
    """
    say("Hii Sir , need magical words to activate me.")

    r = sr.Recognizer()
    mic = sr.Microphone()

    # Calibrate once at start
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.6)

    while True:
        # Wait for wake word
        print("Waiting for wake word...")
        try:
            with mic as source:
                audio = r.listen(source, timeout=None, phrase_time_limit=4)
            try:
                heard = r.recognize_google(audio, language='en-in').lower()
            except Exception:
                continue

            print(f"Heard (wake loop): {heard}")
            if any(w in heard for w in WAKE_WORDS):
                say("Yes sir, I'm listening.")

                # Get the actual command
                cmd = take_command()
                if not cmd:
                    continue

                # Basic command handling (non-exhaustive)
                if "open" in cmd:
                    parts = cmd.split()
                    if len(parts) > 1:
                        website = "".join(parts[1:])
                        say(f"Opening {website}")
                        webbrowser.open(f"https://www.{website}.com")

                elif "the time" in cmd:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    say(f"Sir, the time is {current_time}")

                elif "let us talk" in cmd or "chat" in cmd:
                    say("Yes sir, let's begin.")
                    chat()

                elif "what is your name" in cmd:
                    say("Sir, my name is Lalli, developed by Agrim Saxena")

                elif "wish me" in cmd:
                    wishme()

                elif "show my songs" in cmd:
                    say("Okay sir, showing your songs")
                    webbrowser.open("https://open.spotify.com/playlist/44kMHX5eWfaJmtHab86mBm")

                elif "play" in cmd:
                    parts = cmd.split()
                    song = " ".join(parts[1:]) if len(parts) > 1 else "songs"
                    playsongs(song)

                elif "search" in cmd:
                    parts = cmd.split()
                    if len(parts) > 1:
                        prompt = " ".join(parts[1:])
                        google(prompt)
                    else:
                        say("Sir, what should I search?")

                elif "weather" in cmd or "temperature" in cmd or "tempreture" in cmd:
                    parts = cmd.split()
                    if len(parts) > 1:
                        # assume city is last words
                        city = " ".join(parts[1:])
                        weather(city)
                    else:
                        say("Sir, tell the city name")

                elif "app" in cmd or "application" in cmd:
                    parts = cmd.split()
                    if len(parts) > 1:
                        app_name = " ".join(parts[1:])
                        app(app_name)
                    else:
                        say("Sir, application not found")

                elif "detect me" in cmd:
                    say("Sir detecting you, to close press q")
                    face()

                elif "add" in cmd:
                    parts = cmd.split()
                    if len(parts) == 4:
                        try:
                            num1 = int(parts[1]); num2 = int(parts[3])
                            say(f"Sir the sum is {str(num1+num2)}")
                        except Exception:
                            say("Wrong inputs")
                    else:
                        say("Wrong inputs")

                elif "subtract" in cmd:
                    parts = cmd.split()
                    if len(parts) == 4:
                        try:
                            num1 = int(parts[1]); num2 = int(parts[3])
                            say(f"Sir the difference is {str(num1-num2)}")
                        except Exception:
                            say("Wrong inputs")
                    else:
                        say("Wrong inputs")

                elif "multiply" in cmd:
                    parts = cmd.split()
                    if len(parts) == 4:
                        try:
                            num1 = int(parts[1]); num2 = int(parts[3])
                            say(f"Sir the multiplication is {str(num1*num2)}")
                        except Exception:
                            say("Wrong inputs")
                    else:
                        say("Wrong inputs")

                elif "divide" in cmd:
                    parts = cmd.split()
                    if len(parts) == 4:
                        try:
                            num1 = int(parts[1]); num2 = int(parts[3])
                            if num2 == 0:
                                say("Sorry cannot divide")
                            else:
                                say(f"Sir the division is {str(num1//num2)}")
                        except Exception:
                            say("Wrong inputs")
                    else:
                        say("Wrong inputs")

                elif "what you can do" in cmd:
                    say('''I can do many things:
                    1. Open a website
                    2. Tell my name
                    3. Chat with you as a chatbot
                    4. Open applications
                    5. Play songs
                    6. Wish you
                    7. Tell weather conditions
                    8. Do simple calculations
                    9. Tell the current time
                    10. Search on Google
                    ''')

                elif "exit please" in cmd or "exit" == cmd.strip():
                    say("Okay sir, exiting.")
                    # terminate this assistant process; Flask will continue running
                    try:
                        os._exit(0)
                    except Exception:
                        break

                else:
                    say("Sorry sir, I didn't understand that. Please say the command again.")

                # after handling command, go back to waiting for wake word
                time.sleep(0.5)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()

