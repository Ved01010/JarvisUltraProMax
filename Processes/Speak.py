import pyttsx3

engine = pyttsx3.init()

def speak(text, jarvis_app):
    """This function will make the assistant speak the text passed to it."""
    engine.say(text)
    engine.runAndWait()
    jarvis_app.update_text_widget(f"Jarvis: {text}")
