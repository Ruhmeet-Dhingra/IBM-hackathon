import ctypes
from core.logger import log


def lock_screen():
    """Lock the Windows computer."""
    log("Locking Windows")

    ctypes.windll.user32.LockWorkStation()

    return True