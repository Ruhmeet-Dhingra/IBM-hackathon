import os
import shutil
from voice.speaker import speak
from core.logger import log


def create_folder(folder_name):

    try:

        os.makedirs(folder_name, exist_ok=True)

        log(f"Folder created: {folder_name}")

        speak(f"Created folder {folder_name}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to create folder.")

        return False


def create_file(file_name):

    try:

        with open(file_name, "w") as file:
            pass

        log(f"File created: {file_name}")

        speak(f"Created file {file_name}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to create file.")

        return False


def rename_file(old_name, new_name):

    try:

        os.rename(old_name, new_name)

        log(f"File renamed from {old_name} to {new_name}")

        speak(f"Renamed file from {old_name} to {new_name}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to rename file.")

        return False


def delete_file(file_name):

    try:

        os.remove(file_name)

        log(f"Deleted file: {file_name}")

        speak(f"Deleted file {file_name}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to delete file.")

        return False
def move_file(source, destination):

    try:

        shutil.move(source, destination)

        log(f"Moved {source} to {destination}")

        speak(f"Moved {source}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to move file.")

        return False
def copy_file(source, destination):

    try:

        shutil.copy(source, destination)

        log(f"Copied {source} to {destination}")

        speak(f"Copied {source}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to copy file.")

        return False
def open_file(file_name):

    try:

        os.startfile(file_name)

        log(f"Opened {file_name}")

        speak(f"Opening {file_name}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to open file.")

        return False
def delete_folder(folder_name):

    try:

        shutil.rmtree(folder_name)

        log(f"Deleted folder: {folder_name}")

        speak(f"Deleted folder {folder_name}")

        return True

    except Exception as e:

        log(f"Error: {e}")

        speak("Unable to delete folder.")

        return False