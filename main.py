import os
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import QTimer, Qt, QMetaObject, Q_ARG
import requests
import sys
import random
from JVFullFolder.Image_Generate.imagegenerator import createimage
import cv2
from JVFullFolder.Alert.notify import alert
from JVFullFolder.Automation.open_apps.app_opener import open_application
from JVFullFolder.Checks.CheckSystem import get_system_info
from JVFullFolder.Checks.CheckWeather import get_weather
from JVFullFolder.Checks.CheckOnlineStatus import isonline
from JVFullFolder.Brain.askwolfram import ask_mr_wolf
from JVFullFolder.Processes.Speak import speak
from JVFullFolder.Automation.open_websites.open_websites import open_website


class JarvisApp(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Jarvis by Ved")


        window_width = 1680
        window_height = 990
        self.setGeometry(0, 0, window_width, window_height)


        self.city = "Nagpur"  # Default city, can be changed dynamically


        bg_label = QLabel(self)
        movie = QMovie("Files/background.gif")  # Replace with the path to your GIF file
        bg_label.setMovie(movie)
        bg_label.setGeometry(0, 0, window_width, window_height)
        bg_label.setScaledContents(True)
        movie.start()


        self.text_widget = QTextEdit(self)
        self.text_widget.setGeometry(20, 20, window_width - 40, 150)
        self.text_widget.setFont(QFont("Helvetica", 14))
        self.text_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); color: white;")
        self.text_widget.setReadOnly(True)


        title_label = QLabel("Jarvis AI Assistant", self)
        title_label.setFont(QFont("Helvetica", 20))
        title_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.5);")
        title_label.setGeometry(20, 180, window_width - 40, 40)


        self.system_info_label = QLabel(self)
        self.system_info_label.setFont(QFont("Courier", 12))
        self.system_info_label.setStyleSheet("color: lightblue; background-color: rgba(0, 0, 0, 0.7);")
        self.system_info_label.setGeometry(20, window_height - 380, 350, 150)  # Left side
        self.update_system_info()


        self.weather_label = QLabel(self)
        self.weather_label.setFont(QFont("Courier", 12))
        self.weather_label.setStyleSheet("color: lightblue; background-color: rgba(0, 0, 0, 0.7);")
        self.weather_label.setGeometry(window_width - 370, window_height - 380, 350, 150)  # Right side, parallel to system info
        self.update_weather()


        self.hacker_text_label = QLabel(self)
        self.hacker_text_label.setFont(QFont("Courier", 14))
        self.hacker_text_label.setStyleSheet("color: green; background-color: rgba(0, 0, 0, 0.7);")
        self.hacker_text_label.setGeometry(20, window_height - 200, 350, 180)  # Below system info
        self.update_hacker_text()


        self.time_label = QLabel(self)
        self.time_label.setFont(QFont("Courier", 14))
        self.time_label.setStyleSheet("color: lightblue; background-color: rgba(0, 0, 0, 0.7);")
        self.time_label.setGeometry(window_width - 210, window_height - 60, 200, 40)  # Adjusted for full visibility
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)


        self.update_time()

    def update_weather(self):
        weather_info = get_weather(city=self.city)
        self.weather_label.setText(weather_info)
        QTimer.singleShot(60000, self.update_weather)  # Update weather every 60 seconds

    def update_time(self):
        current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
        self.time_label.setText(current_time)
        QTimer.singleShot(1000, self.update_time)  # Update every second

    def update_system_info(self):
        system_info = get_system_info()
        self.system_info_label.setText(system_info)
        QTimer.singleShot(5000, self.update_system_info)  # Update every 5 seconds

    def update_text_widget(self, text):
        QMetaObject.invokeMethod(self.text_widget, "append", Qt.QueuedConnection, Q_ARG(str, text))

    def update_hacker_text(self):
        hacker_text = self.generate_hacker_text()
        self.hacker_text_label.setText(hacker_text)
        QTimer.singleShot(1000, self.update_hacker_text)  # Update every second

    def generate_hacker_text(self):
        """Generates a random 'hacker' style text for display."""
        characters = '0123456789ABCDEF'
        hacker_text_lines = [''.join(random.choice(characters) for _ in range(50)) for _ in range(4)]  # 4 lines of random characters
        return '\n'.join(hacker_text_lines)


def take_command(jarvis_app):
    """This function will take microphone input from the user and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        jarvis_app.update_text_widget("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        jarvis_app.update_text_widget("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        jarvis_app.update_text_widget(f"You: {query}")
        return query.lower()

    except Exception as e:
        jarvis_app.update_text_widget("Say that again please...")
        return None


def greet_user(jarvis_app):
    """This function will greet the user based on the time of the day."""
    hour = int(datetime.datetime.now().hour)
    speak("Initializing", jarvis_app)
    time.sleep(2)
    alert("Welcome", "Sir I am online now, You can start giving commands after speaking Jarvis Start Listening")
    if 0 <= hour < 12:
        speak("Good morning!", jarvis_app)
    elif 12 <= hour < 18:
        speak("Good afternoon!", jarvis_app)
    else:
        speak("Good evening!", jarvis_app)

    speak("I am Jarvis. How can I assist you today?", jarvis_app)
    time.sleep(1)


def run_voice_assistant(jarvis_app):
    greet_user(jarvis_app)

    listening_active = False
    while True:

        command = take_command(jarvis_app)
        if command is None:
            continue


        if "jarvis start listening" in command:
            if not listening_active:
                listening_active = True
                speak("I am now listening", jarvis_app)
            continue

        if "jarvis stop listening" in command:
            if listening_active:
                listening_active = False
                speak("I will stop listening now", jarvis_app)
            continue


        if listening_active:
            if 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"The time is {current_time}", jarvis_app)

            elif 'weather' in command:
                speak("Fetching the weather...", jarvis_app)
                weather_info = get_weather()
                speak(weather_info, jarvis_app)

            elif 'wikipedia' in command:
                speak("Searching Wikipedia...", jarvis_app)
                command = command.replace("wikipedia", "")
                result = wikipedia.summary(command, sentences=2)
                speak(result, jarvis_app)

            elif 'open website' in command:
                webs = command.replace('open website', '').strip()
                webs = webs.lower()
                open_website(webs, jarvis_app)

            elif 'open app' in command:
                app_name = command.replace('open app', '').strip()
                open_application(app_name, jarvis_app)

            elif 'what are the current system stats' in command:
                speak(get_system_info(), jarvis_app)

            elif 'am i connected to the network' in command:
                if isonline():
                    speak("Yes sir, your are connected to the network")
                else:
                    speak("You are not connected to the network")

            elif 'generate image of' in command:
                gen_image = command.replace("generate image of", "")
                speak(f"Generating image of {gen_image}", jarvis_app)
                createimage(gen_image)
                speak("Generated and Saved the Image", jarvis_app)
                for_show = cv2.imread('gen_image.png')
                cv2.imshow('gen image', for_show)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            elif 'what is' in command or 'calculate' in command:
                wolf_result = ask_mr_wolf(command)
                speak(wolf_result, jarvis_app)

            elif 'play music' in command:
                music_path = r"C:\Users\Ved\Music"
                music_list = os.listdir(music_path)
                random_music = random.choice(music_list)
                full_path = os.path.join(music_path, random_music)
                speak("playing music", jarvis_app)
                os.startfile(full_path)

            elif 'search youtube' in command or 'youtube' in command:
                search_query = command.replace("search youtube", "").replace("youtube", "").strip()
                if search_query:
                    speak(f"Searching YouTube for {search_query}", jarvis_app)
                    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                else:
                    speak("What do you want to search for on YouTube?", jarvis_app)

            elif 'search' in command or 'google' in command:
                search_query = command.replace("search", "").replace("google", "").strip()
                if search_query:
                    speak(f"Searching Google for {search_query}", jarvis_app)
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                else:
                    speak("What do you want to search for?", jarvis_app)

            elif 'exit' in command or 'stop' in command:
                speak("Goodbye!", jarvis_app)
                sys.exit()

            elif 'how are you' in command:
                speak("I am good. How can I assist you?", jarvis_app)

            elif 'who are you' in command:
                speak("I am Jarvis, your personal assistant created by Ved", jarvis_app)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis_app = JarvisApp()


    voice_assistant_thread = threading.Thread(target=run_voice_assistant, args=(jarvis_app,))
    voice_assistant_thread.start()


    jarvis_app.show()
    sys.exit(app.exec_())
