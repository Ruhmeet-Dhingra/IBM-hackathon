"""
ROV Plugin Registry

Stores and manages loaded plugins.
"""

from __future__ import annotations

import logging

from plugin import Plugin

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class PluginRegistryError(Exception):
    """Base Plugin Registry exception."""


# ============================================================
# Plugin Registry
# ============================================================


class PluginRegistry:
    """
    Registry of loaded plugins.
    """

    def __init__(self) -> None:

        self._plugins: dict[str, Plugin] = {}

        logger.info(
            "Plugin Registry initialized."
        )

    # ============================================================
    # Registration
    # ============================================================

    def register(
        self,
        plugin: Plugin,
    ) -> None:
        """
        Register a plugin.
        """

        name = plugin.NAME

        if name in self._plugins:

            raise PluginRegistryError(
                f"Plugin '{name}' is already registered."
            )

        self._plugins[name] = plugin

        logger.info(
            "Registered plugin: %s",
            name,
        )

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a plugin from the registry.
        """

        if name not in self._plugins:

            raise PluginRegistryError(
                f"Plugin '{name}' not found."
            )

        del self._plugins[name]

        logger.info(
            "Unregistered plugin: %s",
            name,
        )
        # ============================================================
    # Lookup
    # ============================================================

    def get(
        self,
        name: str,
    ) -> Plugin:
        """
        Return a registered plugin.
        """

        try:

            return self._plugins[name]

        except KeyError as exc:

            raise PluginRegistryError(
                f"Plugin '{name}' is not registered."
            ) from exc

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a plugin exists.
        """

        return name in self._plugins

    # ============================================================
    # Listing
    # ============================================================

    def all_plugins(
        self,
    ) -> list[Plugin]:
        """
        Return every registered plugin.
        """

        return list(
            self._plugins.values()
        )

    def plugin_names(
        self,
    ) -> list[str]:
        """
        Return the names of all registered plugins.
        """

        return sorted(
            self._plugins.keys()
        )

    @property
    def count(self) -> int:
        """
        Number of registered plugins.
        """

        return len(
            self._plugins
        )
        # ============================================================
    # Plugin State
    # ============================================================

    def enable_plugin(
        self,
        name: str,
    ) -> None:
        """
        Enable a registered plugin.
        """

        self.get(name).enable()

        logger.info(
            "Enabled plugin: %s",
            name,
        )

    def disable_plugin(
        self,
        name: str,
    ) -> None:
        """
        Disable a registered plugin.
        """

        self.get(name).disable()

        logger.info(
            "Disabled plugin: %s",
            name,
        )

    # ============================================================
    # Maintenance
    # ============================================================

    def clear(self) -> None:
        """
        Remove every registered plugin.
        """

        self._plugins.clear()

        logger.info(
            "Plugin registry cleared."
        )

    # ============================================================
    # Summary
    # ============================================================

    def summary(self) -> str:
        """
        Human-readable registry summary.
        """

        lines = [

            "Plugin Registry",
            "===============",
            ""

        ]

        if not self._plugins:

            lines.append(
                "No plugins registered."
            )

            return "\n".join(lines)

        for plugin in self.all_plugins():

            state = (
                "Enabled"
                if plugin.is_enabled
                else "Disabled"
            )

            lines.append(
                f"- {plugin.NAME} "
                f"(v{plugin.VERSION}) "
                f"[{state}]"
            )

        lines.append("")
        lines.append(
            f"Total: {self.count}"
        )

        return "\n".join(lines)

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return registry diagnostics.
        """

        return {

            "count":
                self.count,

            "plugin_names":
                self.plugin_names(),

            "enabled":
                sum(
                    plugin.is_enabled
                    for plugin in self.all_plugins()
                ),

            "disabled":
                sum(
                    not plugin.is_enabled
                    for plugin in self.all_plugins()
                ),

        }

    # ============================================================
    # Representation
    # ============================================================

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"count={self.count})"
        )