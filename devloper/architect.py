"""
ROV Developer v1.0
architect.py

The Architect converts a PlannerResult into a complete
ArchitecturePlan.

Responsibilities
----------------
• Design plugin structure.
• Determine project layout.
• Decide dependencies.
• Decide communication.
• Determine required files.
• Produce ArchitecturePlan.

The Architect NEVER generates Python code.
The Architect NEVER writes files.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass
from typing import List

from devloper.models import (
    ArchitecturePlan,
    PlannerResult,
    PluginPermission,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class ArchitectError(Exception):
    """Base architect exception."""


class ArchitectureValidationError(ArchitectError):
    """Raised when the planner output is invalid."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class ArchitectConfig:
    """
    Configuration for the Architect.
    """

    plugin_directory: str = "plugins"

    enable_logging: bool = True

    estimate_build_time: bool = True


# ============================================================
# Architect
# ============================================================


class Architect:
    """
    Creates the software architecture for a plugin.

    Input
    -----
    PlannerResult

    Output
    ------
    ArchitecturePlan
    """

    def __init__(
        self,
        config: ArchitectConfig | None = None,
    ):

        self.config = config or ArchitectConfig()

        logger.info("Architect initialized.")

    # --------------------------------------------------------

    def design(
        self,
        plan: PlannerResult,
    ) -> ArchitecturePlan:
        """
        Main architecture pipeline.
        """

        start = time.perf_counter()

        self._validate(plan)

        module_name = self._module_name(
            plan.plugin_name
        )

        entry_class = self._entry_class(
            plan.plugin_name
        )

        dependencies = self._dependencies(
            plan
        )

        permissions = self._permissions(
            plan
        )

        required_files = self._required_files(
            module_name
        )

        communication = self._communication(
            plan
        )

        security = self._security_notes(
            plan
        )

        extensions = self._future_extensions(
            plan
        )

        complexity = self._complexity(
            plan
        )

        estimate = self._estimated_time(
            complexity
        )

        architecture = ArchitecturePlan(

            plugin_name=plan.plugin_name,
            plugin_type=plan.plugin_type,
            description=plan.description,
            
            module_name=module_name,

            entry_class=entry_class,
            commands=plan.commands,
            dependencies=dependencies,

            permissions=permissions,

            required_files=required_files,

            communication=communication,

            security_notes=security,

            future_extensions=extensions,

            estimated_complexity=complexity,

            estimated_time=estimate,
        )

        logger.info(

            "Architecture created in %.2f seconds.",

            time.perf_counter() - start,

        )

        return architecture

    # ============================================================
    # Validation
    # ============================================================

    def _validate(
        self,
        plan: PlannerResult,
    ) -> None:

        if not plan.plugin_name.strip():

            raise ArchitectureValidationError(
                "Plugin name cannot be empty."
            )

        if not plan.description.strip():

            raise ArchitectureValidationError(
                "Description cannot be empty."
            )

    # ============================================================
    # Naming
    # ============================================================

    def _module_name(
        self,
        plugin_name: str,
    ) -> str:
        """
        Convert plugin name into a valid
        Python package name.
        """

        name = plugin_name.lower()

        name = re.sub(
            r"[^a-z0-9]+",
            "_",
            name,
        )

        return name.strip("_")

    def _entry_class(
        self,
        plugin_name: str,
    ) -> str:
        """
        Create plugin entry class.
        """

        cleaned = re.sub(
            r"[^a-zA-Z0-9 ]",
            "",
            plugin_name,
        )

        cleaned = cleaned.title()

        cleaned = cleaned.replace(
            " ",
            "",
        )

        return f"{cleaned}Plugin"
        # ============================================================
    # Dependency Resolution
    # ============================================================

    def _dependencies(
        self,
        plan: PlannerResult,
    ) -> List[str]:
        """
        Determine third-party dependencies required
        for the plugin.
        """

        dependencies: set[str] = set()

        permission_map = {
            PluginPermission.INTERNET: {
                "requests",
            },
            PluginPermission.CAMERA: {
                "opencv-python",
            },
            PluginPermission.MICROPHONE: {
                "sounddevice",
            },
            PluginPermission.NOTIFICATIONS: {
                "plyer",
            },
        }

        for permission in plan.permissions:

            dependencies.update(
                permission_map.get(
                    permission,
                    set(),
                )
            )

        return sorted(dependencies)

    # ============================================================
    # Permission Resolution
    # ============================================================

    def _permissions(
        self,
        plan: PlannerResult,
    ) -> List[PluginPermission]:
        """
        Normalize permissions.
        """

        permissions = sorted(
            set(plan.permissions),
            key=lambda permission: permission.value,
        )

        if not permissions:
            permissions.append(
                PluginPermission.NONE
            )

        return permissions

    # ============================================================
    # Required Files
    # ============================================================

    def _required_files(
        self,
        module_name: str,
    ) -> List[str]:
        """
        Files that Generator must create.
        """

        return [

            f"{module_name}/__init__.py",

            f"{module_name}/plugin.py",

            f"{module_name}/manifest.json",

            f"{module_name}/README.md",

        ]

    # ============================================================
    # Communication
    # ============================================================

    def _communication(
        self,
        plan: PlannerResult,
    ) -> List[str]:
        """
        Describe plugin communication.
        """

        communication = [

            "Plugin Loader",

            "Command Registry",

        ]

        if plan.permissions:

            communication.append(
                "Permission Manager"
            )

        if plan.commands:

            communication.append(
                "Command Dispatcher"
            )

        return communication

    # ============================================================
    # Security
    # ============================================================

    def _security_notes(
        self,
        plan: PlannerResult,
    ) -> List[str]:
        """
        Security recommendations.
        """

        notes: List[str] = []

        if (
            PluginPermission.INTERNET
            in plan.permissions
        ):
            notes.append(
                "Validate all network responses."
            )

        if (
            PluginPermission.FILESYSTEM
            in plan.permissions
        ):
            notes.append(
                "Restrict file access to approved paths."
            )

        if (
            PluginPermission.SHELL
            in plan.permissions
        ):
            notes.append(
                "Validate shell commands before execution."
            )

        if (
            PluginPermission.PROCESS
            in plan.permissions
        ):
            notes.append(
                "Limit process privileges."
            )

        if not notes:

            notes.append(
                "No special security requirements."
            )

        return notes

    # ============================================================
    # Future Extensions
    # ============================================================

    def _future_extensions(
        self,
        plan: PlannerResult,
    ) -> List[str]:
        """
        Suggest future improvements.
        """

        suggestions: List[str] = []

        if (
            PluginPermission.INTERNET
            in plan.permissions
        ):
            suggestions.append(
                "Add caching support."
            )

        if plan.commands:

            suggestions.append(
                "Support command aliases."
            )

        suggestions.append(
            "Add configuration page."
        )

        suggestions.append(
            "Add localization support."
        )

        return suggestions
        # ============================================================
    # Complexity Estimation
    # ============================================================

    def _complexity(
        self,
        plan: PlannerResult,
    ) -> str:
        """
        Estimate implementation complexity.
        """

        score = 0

        score += len(plan.permissions)

        score += len(plan.commands)

        score += len(plan.requirements)

        if PluginPermission.INTERNET in plan.permissions:
            score += 2

        if PluginPermission.SHELL in plan.permissions:
            score += 2

        if PluginPermission.PROCESS in plan.permissions:
            score += 2

        if score <= 4:
            return "Low"

        if score <= 9:
            return "Medium"

        return "High"

    # ============================================================
    # Time Estimation
    # ============================================================

    def _estimated_time(
        self,
        complexity: str,
    ) -> int:
        """
        Estimated generation time in seconds.
        """

        estimates = {
            "Low": 3,
            "Medium": 8,
            "High": 15,
        }

        return estimates.get(complexity, 10)

    # ============================================================
    # Architecture Summary
    # ============================================================

    def summary(
        self,
        architecture: ArchitecturePlan,
    ) -> str:
        """
        Generate a human-readable summary.
        """

        return (
            f"Plugin: {architecture.plugin_name}\n"
            f"Module: {architecture.module_name}\n"
            f"Entry Class: {architecture.entry_class}\n"
            f"Complexity: {architecture.estimated_complexity}\n"
            f"Dependencies: {len(architecture.dependencies)}\n"
            f"Permissions: {len(architecture.permissions)}\n"
            f"Files: {len(architecture.required_files)}"
        )

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        architecture: ArchitecturePlan,
    ) -> dict:
        """
        Diagnostic information used by Preview
        and Developer Manager.
        """

        return {

            "plugin": architecture.plugin_name,

            "complexity": architecture.estimated_complexity,

            "estimated_time": architecture.estimated_time,

            "dependency_count": len(
                architecture.dependencies
            ),

            "permission_count": len(
                architecture.permissions
            ),

            "required_file_count": len(
                architecture.required_files
            ),

        }

    # ============================================================
    # Representation
    # ============================================================

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"config={self.config!r})"
        )
        # ============================================================
    # Complexity Estimation
    # ============================================================

    def _complexity(
        self,
        plan: PlannerResult,
    ) -> str:
        """
        Estimate plugin implementation complexity.
        """

        score = 0

        score += len(plan.commands)
        score += len(plan.requirements)
        score += len(plan.permissions)

        if PluginPermission.INTERNET in plan.permissions:
            score += 2

        if PluginPermission.FILESYSTEM in plan.permissions:
            score += 2

        if PluginPermission.SHELL in plan.permissions:
            score += 3

        if PluginPermission.PROCESS in plan.permissions:
            score += 2

        if score <= 5:
            return "Low"

        if score <= 10:
            return "Medium"

        return "High"

    # ============================================================
    # Time Estimation
    # ============================================================

    def _estimated_time(
        self,
        complexity: str,
    ) -> int:
        """
        Estimated generation time in seconds.
        """

        estimates = {
            "Low": 3,
            "Medium": 8,
            "High": 15,
        }

        return estimates.get(complexity, 10)

    # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        architecture: ArchitecturePlan,
    ) -> str:
        """
        Human-readable architecture summary.
        """

        return (
            f"Plugin: {architecture.plugin_name}\n"
            f"Type: {architecture.plugin_type.value}\n"
            f"Module: {architecture.module_name}\n"
            f"Entry Class: {architecture.entry_class}\n"
            f"Complexity: {architecture.estimated_complexity}\n"
            f"Dependencies: {len(architecture.dependencies)}\n"
            f"Permissions: {len(architecture.permissions)}\n"
            f"Files: {len(architecture.required_files)}"
        )

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        architecture: ArchitecturePlan,
    ) -> dict[str, object]:
        """
        Diagnostic information used by the Preview
        and Developer Manager.
        """

        return {
            "plugin_name": architecture.plugin_name,
            "plugin_type": architecture.plugin_type.value,
            "module_name": architecture.module_name,
            "entry_class": architecture.entry_class,
            "complexity": architecture.estimated_complexity,
            "estimated_time": architecture.estimated_time,
            "dependency_count": len(architecture.dependencies),
            "permission_count": len(architecture.permissions),
            "required_file_count": len(architecture.required_files),
        }

    # ============================================================
    # Representation
    # ============================================================

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"config={self.config!r})"
        )