"""Run ROV as a single background process after Windows sign-in."""

import ctypes
import logging
import os
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIRECTORY = PROJECT_ROOT / "data" / "logs"
MUTEX_NAME = "Local\\ROVDesktopAssistant"
ERROR_ALREADY_EXISTS = 183


def configure_logging() -> None:
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_DIRECTORY / "rov.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def acquire_single_instance_mutex() -> int | None:
    handle = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if ctypes.windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        ctypes.windll.kernel32.CloseHandle(handle)
        return None

    return handle


def main() -> None:
    os.chdir(PROJECT_ROOT)
    configure_logging()
    mutex_handle = acquire_single_instance_mutex()

    if mutex_handle is None:
        logging.info("ROV is already running.")
        return

    try:
        time.sleep(8)
        from main import ROV

        logging.info("Starting ROV background service.")
        ROV().start()
    except Exception:
        logging.exception("ROV background service stopped unexpectedly.")
        raise
    finally:
        ctypes.windll.kernel32.CloseHandle(mutex_handle)


if __name__ == "__main__":
    main()
