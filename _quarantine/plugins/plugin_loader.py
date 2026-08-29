"""
ROV Plugin Loader

Discovers and loads plugins from disk.
"""

from __future__ import annotations

import importlib
import json
import logging
from pathlib import Path
from typing import Any

from plugin import Plugin

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class PluginLoaderError(Exception):
    """Base Plugin Loader exception."""


# ============================================================
# Plugin Loader
# ============================================================


class PluginLoader:
    """
    Discovers and loads ROV plugins.
    """

    def __init__(
        self,
        plugins_directory: Path,
    ) -> None:

        self.plugins_directory = Path(
            plugins_directory
        )

        logger.info(
            "Plugin Loader initialized."
        )

    # ============================================================
    # Discovery
    # ============================================================

    def discover(self) -> list[Path]:
        """
        Return every plugin directory.
        """

        if not self.plugins_directory.exists():

            return []

        return [

            path

            for path in self.plugins_directory.iterdir()

            if path.is_dir()

            and (
                path / "manifest.json"
            ).exists()

        ]
        # ============================================================
    # Manifest
    # ============================================================

    @staticmethod
    def _load_manifest(
        plugin_directory: Path,
    ) -> dict[str, Any]:
        """
        Read manifest.json.
        """

        manifest = (
            plugin_directory / "manifest.json"
        )

        if not manifest.exists():

            raise PluginLoaderError(
                f"Manifest not found: {manifest}"
            )

        with manifest.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    # ============================================================
    # Plugin Loading
    # ============================================================

    def load_plugin(
        self,
        plugin_directory: Path,
    ) -> Plugin:
        """
        Load a single plugin.
        """

        manifest = self._load_manifest(
            plugin_directory
        )

        module_name = manifest["entry"]["module"]

        class_name = manifest["entry"]["class"]

        package = plugin_directory.name

        module = importlib.import_module(
            f"{package}.{module_name}"
        )

        plugin_class = getattr(
            module,
            class_name,
        )

        if not issubclass(
            plugin_class,
            Plugin,
        ):

            raise PluginLoaderError(
                f"{class_name} is not a Plugin."
            )

        logger.info(
            "Loaded plugin: %s",
            manifest["name"],
        )

        return plugin_class()

    # ============================================================
    # Load All
    # ============================================================

    def load_all(
        self,
    ) -> list[Plugin]:
        """
        Load every discovered plugin.
        """

        plugins: list[Plugin] = []

        for directory in self.discover():

            try:

                plugin = self.load_plugin(
                    directory
                )

                plugins.append(plugin)

            except Exception:

                logger.exception(
                    "Failed to load %s",
                    directory.name,
                )

        return plugins
        # ============================================================
    # Reload
    # ============================================================

    def reload_plugin(
        self,
        plugin_directory: Path,
    ) -> Plugin:
        """
        Reload a plugin from disk.
        """

        logger.info(
            "Reloading plugin: %s",
            plugin_directory.name,
        )

        return self.load_plugin(
            plugin_directory
        )

    # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        plugins: list[Plugin],
    ) -> str:
        """
        Human-readable summary of loaded plugins.
        """

        lines = [

            "Loaded Plugins",
            "==============",
            ""

        ]

        if not plugins:

            lines.append(
                "No plugins loaded."
            )

            return "\n".join(lines)

        for plugin in plugins:

            lines.append(
                f"- {plugin.NAME} "
                f"(v{plugin.VERSION})"
            )

        lines.append("")
        lines.append(
            f"Total: {len(plugins)}"
        )

        return "\n".join(lines)

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        plugins: list[Plugin],
    ) -> dict[str, Any]:
        """
        Return loader diagnostics.
        """

        return {

            "plugin_directory":
                str(self.plugins_directory),

            "discovered":
                len(self.discover()),

            "loaded":
                len(plugins),

            "plugin_names":
                [
                    plugin.NAME
                    for plugin in plugins
                ],

        }

    # ============================================================
    # Representation
    # ============================================================

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"plugins_directory="
            f"{self.plugins_directory!r})"
        )