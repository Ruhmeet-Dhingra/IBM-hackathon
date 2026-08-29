import subprocess
from core.memory import memory
from config import APPS
from core.audio import speaker
from core.logger import log
import string 
def open_app(app_name):
    app_name = app_name.lower().strip(string.punctuation)
    path = APPS.get(app_name.lower())

    if path:
        log(f"Opening application: {app_name}")
        memory["last_app"] = app_name
        memory["last_command"] = "open"
        subprocess.Popen(path)
        speaker.speak(f"Opening {app_name}")
        return True

    
    return False