import os
import subprocess
from urllib.parse import quote_plus

from core_v2.app_index import (
    build_index,
    find_application,
    find_windows_application,
    save_index,
)
from core_v2.core_types import OperationResult


def _launch_shortcut(name: str, shortcut: str) -> OperationResult:
    try:
        os.startfile(shortcut)
    except OSError as error:
        return OperationResult(success=False, message=str(error))

    return OperationResult(
        success=True,
        message=f"{name} launched successfully.",
    )


def _launch_windows_app(name: str, app_id: str) -> OperationResult:
    try:
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
    except OSError as error:
        return OperationResult(success=False, message=str(error))

    return OperationResult(
        success=True,
        message=f"{name} launched successfully.",
    )


def _search_application_on_google(name: str) -> OperationResult:
    query = f"{name} application"
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    chrome = find_application("chrome")

    if chrome.success:
        try:
            os.startfile(chrome.data["shortcut"], arguments=search_url)
            return OperationResult(
                success=True,
                message=f"{name} is not installed. Searching Google in Chrome.",
            )
        except OSError:
            pass

    from core_v2.browser import search_google

    result = search_google(query)
    if result.success:
        result.message = f"{name} is not installed. Searching Google in the default browser."

    return result


def launch_application(name: str) -> OperationResult:
    """
    Launch an application by name.
    """

    result = find_application(name)

    if result.success:
        return _launch_shortcut(result.data["name"], result.data["shortcut"])

    windows_result = find_windows_application(name)
    if windows_result.success:
        return _launch_windows_app(
            windows_result.data["name"],
            windows_result.data["app_id"],
        )

    return _search_application_on_google(name)



def refresh_index() -> OperationResult:
    """
    Rebuild and save the application index.
    """

    result = build_index()

    if not result.success:
        return result

    save_index(result.data)

    return OperationResult(
        success=True,
        message="Application index refreshed.",
        data=result.data
    )
def close_application(name: str) -> OperationResult:
    """
    Close an application by name.
    """

    from core_v2.process import close_process

    return close_process(name)
def is_running(name: str) -> OperationResult:
    """
    Check if an application is currently running.
    """

    from core_v2.process import is_process_running

    return is_process_running(name)
if __name__ == "__main__":

    result = is_running("chrome")

    print(result)
def get_running_applications() -> OperationResult:
    """
    Return all currently running applications.
    """

    from core_v2.process import get_running_application_names

    return get_running_application_names()
