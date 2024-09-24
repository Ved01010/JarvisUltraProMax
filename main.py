import os
import pyttsx3
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
import psutil  # For system information
import subprocess
import wolframalpha
from APIs.apikeyofweather import apikey
from APIs.wolfapi import mrwolfapi
from imagegenerator import createimage
import cv2


# Initialize the text-to-speech engine
engine = pyttsx3.init()
wolf_asker = wolframalpha.Client(mrwolfapi)

def ask_mr_wolf(query):
    try:
        res = wolf_asker.query(query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return f"Sorry i could'nt find that answer {e}"


def get_weather(city="Nagpur"):
    """Fetches the current weather from OpenWeatherMap API and returns the weather info along with the city name."""
    api_key = apikey  # API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Get the current weather for the city
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        weather_data = data["main"]
        temperature = weather_data["temp"]
        humidity = weather_data["humidity"]
        weather_desc = data["weather"][0]["description"]
        location_name = data["name"]  # This gives the exact name of the location from the API

        return f"Location: {location_name}\nTemp: {temperature}°C\nHumidity: {humidity}%\nCondition: {weather_desc.capitalize()}"
    else:
        return "City Not Found"


apps = {
    "notepad" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Notepad.lnk",
    "browser" : r"C:\Users\Ved\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Vivaldi.lnk",
    "terminal" : r"C:\Users\Ved\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Hyper.lnk",
    "chatgpt" : r"C:\Users\Ved\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Vivaldi Apps\ChatGPT.lnk",
    "spotify" : r"C:\Users\Ved\Desktop\Spotify.lnk",
    "discord" : r"C:\Users\Ved\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"


}


def get_system_info():
    """Fetches system information such as CPU usage and memory availability."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return (f"CPU Usage: {cpu_usage}%\n"
            f"Memory Available: {memory.available // (1024 * 1024)} MB\n"
            f"Memory Used: {memory.used // (1024 * 1024)} MB\n"
            f"Memory Total: {memory.total // (1024 * 1024)} MB")

class JarvisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Jarvis by Ved")

        # Set the window size
        window_width = 1680
        window_height = 990
        self.setGeometry(0, 0, window_width, window_height)

        # Initialize city name for weather updates
        self.city = "Nagpur"  # Default city, can be changed dynamically

        # Load and set the GIF background
        bg_label = QLabel(self)
        movie = QMovie("background.gif")  # Replace with the path to your GIF file
        bg_label.setMovie(movie)
        bg_label.setGeometry(0, 0, window_width, window_height)
        bg_label.setScaledContents(True)
        movie.start()

        # Set up the text widget to display recognized text and responses
        self.text_widget = QTextEdit(self)
        self.text_widget.setGeometry(20, 20, window_width - 40, 150)
        self.text_widget.setFont(QFont("Helvetica", 14))
        self.text_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); color: white;")
        self.text_widget.setReadOnly(True)

        # Set up the title label (optional)
        title_label = QLabel("Jarvis AI Assistant", self)
        title_label.setFont(QFont("Helvetica", 20))
        title_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.5);")
        title_label.setGeometry(20, 180, window_width - 40, 40)

        # Set up the system information label (left side)
        self.system_info_label = QLabel(self)
        self.system_info_label.setFont(QFont("Courier", 12))
        self.system_info_label.setStyleSheet("color: lightblue; background-color: rgba(0, 0, 0, 0.7);")
        self.system_info_label.setGeometry(20, window_height - 380, 350, 150)  # Left side
        self.update_system_info()

        # Set up the weather label (parallel to system info but on right side)
        self.weather_label = QLabel(self)
        self.weather_label.setFont(QFont("Courier", 12))
        self.weather_label.setStyleSheet("color: lightblue; background-color: rgba(0, 0, 0, 0.7);")
        self.weather_label.setGeometry(window_width - 370, window_height - 380, 350, 150)  # Right side, parallel to system info
        self.update_weather()

        # Set up the hacker text box
        self.hacker_text_label = QLabel(self)
        self.hacker_text_label.setFont(QFont("Courier", 14))
        self.hacker_text_label.setStyleSheet("color: green; background-color: rgba(0, 0, 0, 0.7);")
        self.hacker_text_label.setGeometry(20, window_height - 200, 350, 180)  # Below system info
        self.update_hacker_text()

        # Set up the time label with hi-tech style (fully visible in 1680x990)
        self.time_label = QLabel(self)
        self.time_label.setFont(QFont("Courier", 14))
        self.time_label.setStyleSheet("color: lightblue; background-color: rgba(0, 0, 0, 0.7);")
        self.time_label.setGeometry(window_width - 210, window_height - 60, 200, 40)  # Adjusted for full visibility
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # Start the clock update
        self.update_time()

    def update_weather(self):
        # Fetch weather information for the current city
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


def speak(text, jarvis_app):
    """This function will make the assistant speak the text passed to it."""
    engine.say(text)
    engine.runAndWait()
    jarvis_app.update_text_widget(f"Jarvis: {text}")

def isonline():
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

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

def open_application(app_name, jarvis_app):
    """Function to open specific application or shortcut based on voice command"""
    app_name = app_name.lower()

    if app_name in apps:
        app_path = apps[app_name]
        try:
            subprocess.Popen(app_path, shell=True)  # Added shell=True for better compatibility with .lnk files
            speak(f"Opening {app_name}", jarvis_app)
        except FileNotFoundError:
            speak(f"The file or shortcut for {app_name} was not found.", jarvis_app)
        except PermissionError:
            speak(f"Permission denied while trying to open {app_name}.", jarvis_app)
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}. Error: {str(e)}", jarvis_app)
            print(f"Error opening {app_name}: {e}")
    else:
        speak(f"Sorry, I don't know how to open {app_name}.", jarvis_app)

def greet_user(jarvis_app):
    """This function will greet the user based on the time of the day."""
    hour = int(datetime.datetime.now().hour)
    speak("Initializing", jarvis_app)
    time.sleep(2)  # Shorter delay for initialization
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

    listening_active = False  # Initially in "rest mode"
    while True:
        # Always listen for commands, regardless of mode
        command = take_command(jarvis_app)
        if command is None:
            continue

        # Handle the "start listening" and "stop listening" commands
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

        # Process other commands only if in "listening" mode
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

            elif 'open' in command:
                app_name = command.replace('open', '').strip()
                open_application(app_name, jarvis_app)

            elif 'what are the current system stats' in command:
                speak(get_system_info(), jarvis_app)

            elif 'generate image of' in command:
                gen_image = command.replace("generate image of", "")
                speak(f"Generating image of {gen_image}", jarvis_app)
                createimage(gen_image)
                speak("Generated and Saved the Image", jarvis_app)
                for_show = cv2.imread('created_image.png')
                cv2.imshow('generated image', for_show)
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

            elif 'open github' in command:
                speak("Opening Github", jarvis_app)
                webbrowser.open("https://www.github.com")

            elif 'open youtube' in command:
                speak("Opening YouTube", jarvis_app)
                webbrowser.open("https://www.youtube.com")

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

    # Run voice assistant in a separate thread to keep the GUI responsive
    voice_assistant_thread = threading.Thread(target=run_voice_assistant, args=(jarvis_app,))
    voice_assistant_thread.start()

    # Start the GUI loop
    jarvis_app.show()
    sys.exit(app.exec_())
