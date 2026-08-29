import webbrowser
import time
import pyautogui
from core.memory import memory
from core.audio import speaker
from config import WEBSITES
from core.logger import log
import string 

def google_search(query):
    """Search Google."""
    log(f"Searching Google: {query}")
    memory["last_search"] = query
    memory["last_command"] = "search"

    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    webbrowser.open(url)

    speaker.speak(f"Searching for {query}")


def chrome_search(query):
    memory["last_search"] = query
    """Open Chrome (already open or launched) and search."""

    time.sleep(2)

    pyautogui.write(query, interval=0.04)
    pyautogui.press("enter")

def open_website(name):
    name = name.lower().strip(string.punctuation)
    print("Website requested:", name)
    print("Available websites:", WEBSITES)

    log(f"Opening website: {name}")
    memory["last_website"] = name

    url = WEBSITES.get(name)

    if url:
        webbrowser.open(url)
        speaker.speak(f"Opening {name}")
        return True

    return False