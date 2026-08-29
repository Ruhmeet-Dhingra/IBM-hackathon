"""
Process management utilities for Core v2.
"""

import psutil

from core_v2.core_types import OperationResult


def get_running_processes() -> OperationResult:
    """
    Return a list of all running processes.
    """

    processes = []

    for process in psutil.process_iter(["pid", "name"]):

        try:
            processes.append({
                "pid": process.info["pid"],
                "name": process.info["name"]
            })

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            continue

    return OperationResult(
        success=True,
        message="Running processes retrieved.",
        data=processes
    )
def find_process(name: str) -> OperationResult:
    """
    Find a running process by name.
    """

    result = get_running_processes()

    if not result.success:
        return result

    processes = result.data
    search_name = name.lower().strip()

    # Exact match
    for process in processes:

        process_name = process["name"].lower()

        if process_name == search_name:
            return OperationResult(
                success=True,
                message="Process found.",
                data=process
            )

    # Partial match
    for process in processes:

        process_name = process["name"].lower()

        if search_name in process_name:
            return OperationResult(
                success=True,
                message="Process found (partial match).",
                data=process
            )

    return OperationResult(
        success=False,
        message=f"{name} is not running."
    )

def close_process(name: str) -> OperationResult:
    """
    Close all running processes matching the given name.
    """

    search_name = name.lower().strip()
    closed = 0

    for process in psutil.process_iter(["pid", "name"]):

        try:
            process_name = process.info["name"]

            if process_name is None:
                continue
                
            process_lower = process_name.lower()
            if process_lower == search_name or process_lower == f"{search_name}.exe":
                process.terminate()
                closed += 1

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    if closed == 0:
        return OperationResult(
            success=False,
            message=f"{name} is not running."
        )

    return OperationResult(
        success=True,
        message=f"Closed {closed} process(es)."
    )
result = get_running_processes()

def is_process_running(name: str) -> OperationResult:
    """
    Check whether a process is currently running.
    """

    result = find_process(name)

    if result.success:
        return OperationResult(
            success=True,
            message=f"{name} is running.",
            data=True
        )

    return OperationResult(
        success=False,
        message=f"{name} is not running.",
        data=False
    )
def get_running_application_names() -> OperationResult:
    """
    Return the names of all running applications.
    """

    result = get_running_processes()

    if not result.success:
        return result

    names = sorted({
        process["name"]
        for process in result.data
        if process["name"] is not None
    })

    return OperationResult(
        success=True,
        message="Running applications retrieved.",
        data=names
    )