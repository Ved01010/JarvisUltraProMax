import os
from winotify import Notification, audio

def alert(name, text):
    logo_path = r"C:\Users\Ved\PycharmProjects\JarvisUltraProMax\JVFullFolder\Files\nlogo.png"


    if not os.path.exists(logo_path):
        print(f"Logo not found at {logo_path}")
        return

    note = Notification(
        app_id="Jarvis",
        title=name,
        msg=text,
        duration="long",
        icon=logo_path
    )

    note.set_audio(audio.Default, loop=False)
    note.show()

