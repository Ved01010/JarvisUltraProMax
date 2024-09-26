import subprocess
from JVFullFolder.Automation.open_apps.apps_dictionary import apps
from JVFullFolder.Processes.Speak import speak

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
