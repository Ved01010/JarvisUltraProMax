import webbrowser
from JVFullFolder.Automation.open_websites.Website_dictionary import websites
from JVFullFolder.Processes.Speak import speak

def open_website(website_name, jarvis_app):
    website_name.lower()
    if website_name in websites:
        web_url = websites[website_name]
        webbrowser.open(web_url)
        speak(f"opening {website_name}", jarvis_app)
    else:
        speak("couldn't find website in dictionary", jarvis_app)


