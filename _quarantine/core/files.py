from pathlib import Path
from core.audio import speaker


def create_file(filename: str):

    desktop = Path.home() / "Desktop"

    file_path = desktop / filename

    if file_path.exists():
        speaker.speak(f"{filename} already exists.")
        return True

    file_path.touch()

    speaker.speak(f"Created {filename}")
    return True