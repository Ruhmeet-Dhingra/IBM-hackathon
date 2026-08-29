from brain_v2.gemini_provider import ask

from core.app import open_app
from core.browser import open_website
from core.files import create_file
from core.system import lock_screen

from devloper.developer_service import developer_service


def handle(command: str):

    original_command = command.strip()
    command = original_command.lower()

    # ---------------------------------
    # Built-in Commands
    # ---------------------------------

    if command.startswith("open "):

        app = original_command[5:].strip()

        if open_app(app):
            return f"Opening {app}"

    if command.startswith("website "):

        website = original_command[8:].strip()

        if open_website(website):
            return f"Opening {website}"

    if command.startswith("create file"):

        filename = original_command[11:].strip()

        if "." not in filename:
            filename += ".txt"

        create_file(filename)

        return f"Created {filename}"

    if command in (
        "lock screen",
        "lock my screen",
        "lock computer",
    ):

        lock_screen()

        return "Locking your computer."

    # ---------------------------------
    # Developer Mode
    # ---------------------------------

    developer_verbs = (
        "create",
        "build",
        "make",
        "generate",
        "add",
    )

    developer_targets = (
        "plugin",
        "plug-in",
        "feature",
    )

    if (
        any(verb in command for verb in developer_verbs)
        and
        any(target in command for target in developer_targets)
    ):

        try:

            result = developer_service.build_plugin(original_command)

            if result.successful:

                plugin_name = (
                    result.planner.plugin_name
                    if result.planner
                    else "Unknown Plugin"
                )

                return (
                    f"✅ Successfully created plugin '{plugin_name}'."
                )

            return "❌ Plugin generation failed."

        except Exception as e:

            return f"Developer Error: {e}"

    # ---------------------------------
    # Default (Gemini)
    # ---------------------------------

    return ask(original_command)