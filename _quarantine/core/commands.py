from core.app import open_application
from voice.speaker import speak
import subprocess
from config import APPS
from core.typing import type_text
from core.browser import google_search, chrome_search, open_website
from core.file import create_folder, create_file, delete_folder, rename_file, delete_file, move_file, copy_file, open_file
IGNORE_WORDS = {
    "and",
    "please",
    "could",
    "would",
    "kindly",
    "then",
    "just",
    "the",
    "a",
    "an"
}

def open_application(app_name):
    path = APPS.get(app_name)

    if path:
        subprocess.Popen(path)
        speak(f"Opening {app_name}")
        return True

    
    return False


def execute_command(parsed):

    command = parsed["text"]
    words = parsed["words"]
    action = parsed["action"]
    words = [word for word in words if word not in IGNORE_WORDS]

    if not words:
        return

    action = words[0]

    if not command:
        return


    # -------------------------
    # GOOGLE SEARCH
    # -------------------------

    if action == "search":

        target = " ".join(words[1:])

        if not target:
            speak("What do you want to search?")
            return

        google_search(target)

        return

    # -------------------------
    # OPEN COMMANDS
    # -------------------------

    if action == "open":

        # ---------------------
        # open chrome search ...
        # ---------------------

        if "search" in words:

            search_index = words.index("search")

            app_name = " ".join(words[1:search_index])

            search_text = " ".join(words[search_index + 1:])

            if open_application(app_name):

                chrome_search(search_text)
            return

        # ---------------------
        # open notepad type ...
        # ---------------------

        if "type" in words:

            type_index = words.index("type")

            app_name = " ".join(words[1:type_index])

            text = " ".join(words[type_index + 1:])

            if open_application(app_name):
                type_text(text)

            return

        # ---------------------
        # Normal open
        # ---------------------

        app_name = " ".join(words[1:])

        if open_application(app_name):
            return

        if open_website(app_name):
            return

        speak("Application or website not found.")
        return

    if action == "create":
        if len(words) >= 3:
            item = words[1]
            name = " ".join(words[2:])

            if item == "folder":
                create_folder(name)
                return
            elif item == "file":
                create_file(name)
                return

    # -------------------------
# RENAME COMMAND
# -------------------------

    if action == "rename":

     if len(words) >= 5 and words[1] == "file":

        if "to" not in words:

            speak("Please specify the new file name.")
            return

        to_index = words.index("to")

        old_name = " ".join(words[2:to_index])

        new_name = " ".join(words[to_index + 1:])

        rename_file(old_name, new_name)

        return
    if action == "delete":

      if len(words) >= 3 and words[1] == "file":

        file_name = " ".join(words[2:])

        delete_file(file_name)

        return
    if action == "move":

       if len(words) >= 4 and words[1] == "file":

        if "to" not in words:

            speak("Please specify the destination.")
            return

        to_index = words.index("to")

        source = " ".join(words[2:to_index])

        destination = " ".join(words[to_index + 1:])

        move_file(source, destination)

        return
    if action == "copy":

        if len(words) >= 4 and words[1] == "file":

         if "to" not in words:

            speak("Please specify the destination.")
            return

        to_index = words.index("to")

        source = " ".join(words[2:to_index])

        destination = " ".join(words[to_index + 1:])

        copy_file(source, destination)

        return
    if action == "open":

        if len(words) >= 3 and words[1] == "file":

          file_name = " ".join(words[2:])

        open_file(file_name)

        return
    if action == "delete":

     if len(words) >= 3:

        item = words[1]

        name = " ".join(words[2:])

        if item == "file":

            delete_file(name)

            return

        elif item == "folder":

            delete_folder(name)

            return

    # -------------------------
    # UNKNOWN COMMAND
    # -------------------------

    speak("Sorry, I don't understand that command.")