"""Load and run only plugins that were explicitly approved and installed."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from core_v2.core_types import OperationResult
from plugins.plugin import Plugin


class PluginRuntime:
    def __init__(self, plugin_root: Path | None = None) -> None:
        root = plugin_root or Path(__file__).resolve().parent
        self.installed_root = root / "installed"

    def find_for_command(self, command: str) -> str | None:
        normalized_command = self._normalize(command)
        for metadata_path in self.installed_root.glob("*/proposal.json"):
            metadata = self._read_metadata(metadata_path)
            for trigger in metadata["draft"]["commands"]:
                if self._normalize(trigger) == normalized_command:
                    return metadata["proposal_id"]
        return None

    def run(self, plugin_id: str, command: str) -> OperationResult:
        plugin_directory = self.installed_root / plugin_id
        metadata_path = plugin_directory / "proposal.json"
        source_path = plugin_directory / "plugin.py"
        if not metadata_path.is_file() or not source_path.is_file():
            return OperationResult(False, f"Installed plugin '{plugin_id}' was not found.")

        metadata = self._read_metadata(metadata_path)
        if metadata.get("status") != "approved":
            return OperationResult(False, f"Plugin '{plugin_id}' is not approved.")

        try:
            module_name = f"rov_plugin_{plugin_id}"
            specification = importlib.util.spec_from_file_location(module_name, source_path)
            if specification is None or specification.loader is None:
                raise RuntimeError("plugin module could not be loaded")
            module = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(module)
            plugin_class = next(
                value
                for value in vars(module).values()
                if isinstance(value, type) and issubclass(value, Plugin) and value is not Plugin
            )
            result = plugin_class().run(command=command)
        except Exception as error:
            return OperationResult(False, f"Plugin '{plugin_id}' failed: {error}")

        if isinstance(result, dict):
            return OperationResult(
                bool(result.get("success", True)),
                str(result.get("message", f"Plugin '{plugin_id}' completed.")),
                data=result,
            )
        return OperationResult(True, str(result))

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(value.casefold().split())

    @staticmethod
    def _read_metadata(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))
