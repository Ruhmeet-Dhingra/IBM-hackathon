"""
ROV Developer v1.0
template_engine.py

Renders TemplateTask objects into GeneratedFile objects.

Pipeline

TemplateTask
      │
      ▼
Load Jinja Template
      ▼
Render Context
      ▼
GeneratedFile
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
)

from devloper.models import (
    GeneratedFile,
    TemplateResult,
    TemplateTask,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class TemplateEngineError(Exception):
    """Base template engine exception."""


class TemplateNotFoundError(TemplateEngineError):
    """Raised when a template cannot be found."""


class TemplateRenderError(TemplateEngineError):
    """Raised when template rendering fails."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class TemplateEngineConfig:
    """
    Configuration for the Template Engine.
    """

    template_directory: Path = Path("devloper/templates")

    encoding: str = "utf-8"

    strict: bool = True


# ============================================================
# Template Engine
# ============================================================


class TemplateEngine:
    """
    Renders TemplateTask objects into GeneratedFile objects.
    """

    def __init__(
        self,
        config: TemplateEngineConfig | None = None,
    ) -> None:

        self.config = config or TemplateEngineConfig()

        self.environment = Environment(
            loader=FileSystemLoader(
                self.config.template_directory
            ),
            undefined=StrictUndefined,
            autoescape=False,
        )

        logger.info("Template Engine initialized.")

    # --------------------------------------------------------

    def render(
        self,
        tasks: list[TemplateTask],
    ) -> TemplateResult:
        """
        Render every template task.
        """

        start = time.perf_counter()

        rendered_files: list[GeneratedFile] = []

        rendered_templates: list[str] = []

        for task in tasks:

            if not self.validate_task(task):
                raise TemplateRenderError(
                    f"Invalid template task: {task.template}"
                )

            generated = self._render_task(task)

            rendered_files.append(generated)

            rendered_templates.append(task.template)

        duration = (
            time.perf_counter() - start
        ) * 1000

        return TemplateResult(
            files=rendered_files,
            rendered_templates=rendered_templates,
            variables={},
            successful=True,
            duration_ms=duration,
        )
        # ============================================================
    # Task Rendering
    # ============================================================

    def _render_task(
        self,
        task: TemplateTask,
    ) -> GeneratedFile:
        """
        Render a single TemplateTask into a GeneratedFile.
        """

        template = self._load_template(
            task.template
        )

        content = self._render_template(
            template,
            task.context,
        )

        return GeneratedFile(
            path=task.output,
            content=content,
            description=(
                f"Rendered from {task.template}"
            ),
            overwrite=task.overwrite,
        )

    # ============================================================
    # Template Loading
    # ============================================================

    def _load_template(
        self,
        template_name: str,
    ):
        """
        Load a Jinja template from the configured
        template directory.
        """

        try:

            return self.environment.get_template(
                template_name
            )

        except Exception as exc:

            raise TemplateNotFoundError(
                f"Template '{template_name}' not found."
            ) from exc

    # ============================================================
    # Template Rendering
    # ============================================================

    def _render_template(
        self,
        template,
        context: dict[str, Any],
    ) -> str:
        """
        Render a Jinja template using the supplied context.
        """

        try:

            return template.render(**context)

        except Exception as exc:

            raise TemplateRenderError(
                f"Failed to render '{template.name}': {exc}"
            ) from exc

    # ============================================================
    # Validation
    # ============================================================

    def validate_task(
        self,
        task: TemplateTask,
    ) -> bool:
        """
        Validate a TemplateTask before rendering.
        """

        if not task.template.strip():
            return False

        if not str(task.output).strip():
            return False

        if not isinstance(task.context, dict):
            return False

        return True