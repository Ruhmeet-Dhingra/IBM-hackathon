
"""
ROV Developer v1.0
generator.py

The Generator converts an ArchitecturePlan into a collection
of template rendering tasks.

The Generator DOES NOT

- generate Python source code
- write files
- install plugins

Those responsibilities belong to the Template Engine and Installer.

Pipeline

ArchitecturePlan
        │
        ▼
Generator
        │
        ▼
TemplateTask(s)
        │
        ▼
GeneratorResult
"""

from __future__ import annotations
from devloper.models import TemplateTask
import logging 
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devloper.models import (
    ArchitecturePlan,
    GeneratorResult,
    TemplateTask,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class GeneratorError(Exception):
    """Base Generator exception."""


class InvalidArchitectureError(GeneratorError):
    """Raised when an ArchitecturePlan is invalid."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class GeneratorConfig:
    """
    Generator configuration.
    """

    template_directory: str = "templates"

    plugin_template: str = "plugin.py.jinja"

    manifest_template: str = "manifest.json.jinja"

    readme_template: str = "README.md.jinja"

    init_template: str = "__init__.py.jinja"

    include_readme: bool = True

    include_init: bool = True


# ============================================================
# Generator
# ============================================================


class Generator:
    """
    Converts an ArchitecturePlan into template rendering tasks.
    """

    def __init__(
        self,
        config: GeneratorConfig | None = None,
    ) -> None:

        self.config = config or GeneratorConfig()

        logger.info("Generator initialized.")

    # --------------------------------------------------------

    def generate(
        self,
        architecture: ArchitecturePlan,
    ) -> GeneratorResult:
        """
        Generate template tasks.
        """

        start = time.perf_counter()

        self._validate(architecture)

        tasks = self._build_tasks(
            architecture
        )

        result = GeneratorResult(

            plugin_name=architecture.plugin_name,

            description=(
                f"Generated template tasks "
                f"for {architecture.plugin_name}"
            ),

            plugin_type=architecture.plugin_type,

            tasks=tasks,

            commands=[],

            dependencies=architecture.dependencies,

            permissions=architecture.permissions,

            estimated_lines=0,

            summary=self._summary(
                architecture,
                tasks,
            ),

        )

        logger.info(

            "Generator created %d task(s) in %.2f seconds.",

            len(tasks),

            time.perf_counter() - start,

        )

        return result

    # ============================================================
    # Validation
    # ============================================================

    def _validate(
        self,
        architecture: ArchitecturePlan,
    ) -> None:

        if not architecture.plugin_name.strip():

            raise InvalidArchitectureError(
                "Plugin name cannot be empty."
            )

        if not architecture.module_name.strip():

            raise InvalidArchitectureError(
                "Module name cannot be empty."
            )

        if not architecture.entry_class.strip():

            raise InvalidArchitectureError(
                "Entry class cannot be empty."
            )

    # ============================================================
    # Context
    # ============================================================

    def _context(
    self,
    architecture: ArchitecturePlan,
) -> dict[str, Any]:

     return {

        "plugin_name": architecture.plugin_name,

        "commands": architecture.commands,

        "description": architecture.description,

        "class_name": architecture.entry_class,

        "plugin_type": architecture.plugin_type.value,

        "module_name": architecture.module_name,

        "entry_class": architecture.entry_class,

        "dependencies": architecture.dependencies,

        "permissions": [
            permission.value
            for permission in architecture.permissions
        ],

        "security_notes": architecture.security_notes,

        "complexity": architecture.estimated_complexity,
    }
        # ============================================================
    # Task Builder
    # ============================================================

    def _build_tasks(
        self,
        architecture: ArchitecturePlan,
    ) -> list[TemplateTask]:
        """
        Build every template rendering task.
        """

        context = self._context(architecture)

        tasks: list[TemplateTask] = []

        # plugin.py

        tasks.append(
            TemplateTask(
                template=self.config.plugin_template,
                output=Path(
                    architecture.module_name
                ) / "plugin.py",
                context=context,
            )
        )

        # manifest.json

        tasks.append(
            TemplateTask(
                template=self.config.manifest_template,
                output=Path(
                    architecture.module_name
                ) / "manifest.json",
                context=context,
            )
        )

        # README

        if self.config.include_readme:

            tasks.append(
                TemplateTask(
                    template=self.config.readme_template,
                    output=Path(
                        architecture.module_name
                    ) / "README.md",
                    context=context,
                )
            )

        # __init__.py

        if self.config.include_init:

            tasks.append(
                TemplateTask(
                    template=self.config.init_template,
                    output=Path(
                        architecture.module_name
                    ) / "__init__.py",
                    context=context,
                )
            )

        return tasks

    # ============================================================
    # Summary
    # ============================================================

    def _summary(
        self,
        architecture: ArchitecturePlan,
        tasks: list[TemplateTask],
    ) -> str:
        """
        Build a generation summary.
        """

        lines = [

            f"Plugin : {architecture.plugin_name}",

            f"Module : {architecture.module_name}",

            f"Templates : {len(tasks)}",

            f"Dependencies : {len(architecture.dependencies)}",

            f"Permissions : {len(architecture.permissions)}",

            f"Complexity : {architecture.estimated_complexity}",

        ]

        return "\n".join(lines)

    # ============================================================
    # Utility
    # ============================================================

    @staticmethod
    def task_count(
        result: GeneratorResult,
    ) -> int:
        """
        Number of rendering tasks.
        """

        return len(result.tasks)

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(config={self.config!r})"
        )
    