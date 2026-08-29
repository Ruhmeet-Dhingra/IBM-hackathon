from pathlib import Path
import json
import subprocess

from core_v2.core_types import OperationResult



PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = PROJECT_ROOT / "data" / "app_index.json"


START_MENU_PATHS = [
    Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"),
    Path.home() / r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs",
]


def scan_start_menu() -> dict:
    """
    Scan the Windows Start Menu for application shortcuts.
    """

    index = {}

    for start_menu in START_MENU_PATHS:
        print(f"Scanning: {start_menu}")
        print(f"Exists: {start_menu.exists()}")
        if not start_menu.exists():
            continue

        for shortcut in start_menu.rglob("*.lnk"):
            print(shortcut)
            app_name = shortcut.stem.lower()

            index[app_name] = {
                "name": shortcut.stem,
                "shortcut": str(shortcut)
            }

    return index

def build_index() -> OperationResult:
    """
    Build the application index by scanning the Start Menu.
    """

    index = scan_start_menu()

    return OperationResult(
        success=True,
        message="Application index created.",
        data=index
    )
def save_index(index: dict) -> OperationResult:
    """
    Save the application index to disk.
    """

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=4)

    return OperationResult(
        success=True,
        message="Application index saved."
    )
def load_index() -> OperationResult:
    """
    Load the application index from disk.
    """

    if not INDEX_FILE.exists():
        return OperationResult(
            success=False,
            message="Application index not found."
        )

    with open(INDEX_FILE, "r", encoding="utf-8") as file:
        index = json.load(file)

    return OperationResult(
        success=True,
        message="Application index loaded.",
        data=index
    )
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
def find_application(name: str) -> OperationResult:
    """
    Find an application by name.
    """

    result = load_index()

    if not result.success:
        return result

    index = result.data

    search_name = name.lower().strip()
    # Exact match
    app = index.get(search_name)

    if app is not None:
        return OperationResult(
            success=True,
            message="Application found.",
            data=app
        )

    # Partial match
    for app_name, app_data in index.items():
        if search_name in app_name:
            return OperationResult(
                success=True,
                message="Application found (partial match).",
                data=app_data
            )

    # No match
    return OperationResult(
        success=False,
        message=f"{name} not found."
    )


def find_windows_application(name: str) -> OperationResult:
    """Find a registered Windows Start app by its display name."""

    command = [
        "powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        "Get-StartApps | Select-Object Name,AppID | ConvertTo-Json -Compress",
    ]

    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        applications = json.loads(completed.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return OperationResult(
            success=False,
            message=f"Unable to search registered Windows apps: {error}",
        )

    if isinstance(applications, dict):
        applications = [applications]

    search_name = name.casefold().strip()
    candidates = [
        application
        for application in applications
        if isinstance(application.get("Name"), str)
        and isinstance(application.get("AppID"), str)
        and application["AppID"]
    ]

    for application in candidates:
        if application["Name"].casefold() == search_name:
            return OperationResult(
                success=True,
                message="Registered Windows app found.",
                data={"name": application["Name"], "app_id": application["AppID"]},
            )

    for application in candidates:
        if search_name in application["Name"].casefold():
            return OperationResult(
                success=True,
                message="Registered Windows app found (partial match).",
                data={"name": application["Name"], "app_id": application["AppID"]},
            )

    return OperationResult(
        success=False,
        message=f"{name} not found in registered Windows apps.",
    )
if __name__ == "__main__":
    result = load_index()
    if not result.success:
        print(result.message)
    else:
        for key in result.data.keys():
            print(key)
