"""
ROV Plugin Base Class

Every generated plugin inherits from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """
    Base class for every ROV plugin.
    """

    NAME = "Unnamed Plugin"

    DESCRIPTION = ""

    VERSION = "1.0.0"

    def __init__(self) -> None:

        self.enabled = True

    @abstractmethod
    def run(
        self,
        *args,
        **kwargs,
    ) -> Any:
        """
        Execute the plugin.
        """

        raise NotImplementedError
        # ============================================================
    # Plugin State
    # ============================================================

    def enable(self) -> None:
        """
        Enable the plugin.
        """

        self.enabled = True

    def disable(self) -> None:
        """
        Disable the plugin.
        """

        self.enabled = False

    @property
    def is_enabled(self) -> bool:
        """
        Whether the plugin is enabled.
        """

        return self.enabled

    # ============================================================
    # Metadata
    # ============================================================

    @property
    def metadata(self) -> dict[str, Any]:
        """
        Return plugin metadata.
        """

        return {
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "enabled": self.enabled,
        }