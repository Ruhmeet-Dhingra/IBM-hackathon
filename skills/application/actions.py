from core_v2.app import (
    launch_application,
    close_application,
)


def launch(name: str):
    return launch_application(name)


def close(name: str):
    return close_application(name)
