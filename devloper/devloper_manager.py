"""
ROV Developer v1.0
developer_manager.py

Coordinates the complete Developer pipeline.

Pipeline

User Request
      │
      ▼
Planner
      ▼
Architect
      ▼
Generator
      ▼
Template Engine
      ▼
Validator
      ▼
Reviewer
      ▼
Preview Builder
      ▼
Installer
      ▼
DeveloperResult
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from devloper.architect import Architect
from devloper.generator import Generator
from devloper.installer import Installer
from devloper.models import (
    DeveloperResult,
    DeveloperStage,
    ProjectAnalysis,
)
from devloper.planner import Planner
from devloper.preview import PreviewBuilder
from devloper.reviewer import Reviewer
from devloper.template_engine import TemplateEngine
from devloper.validator import Validator

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class DeveloperManagerError(Exception):
    """Base Developer Manager exception."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class DeveloperManagerConfig:
    """
    Configuration for the Developer Manager.
    """

    auto_install: bool = False

    stop_on_validation_failure: bool = True

    stop_on_review_failure: bool = True


# ============================================================
# Developer Manager
# ============================================================


class DeveloperManager:
    """
    Coordinates the complete Developer pipeline.
    """

    def __init__(
        self,
        planner: Planner,
        architect: Architect,
        generator: Generator,
        template_engine: TemplateEngine,
        validator: Validator,
        reviewer: Reviewer,
        preview: PreviewBuilder,
        installer: Installer,
        config: DeveloperManagerConfig | None = None,
    ) -> None:

        self.planner = planner

        self.architect = architect

        self.generator = generator

        self.template_engine = template_engine

        self.validator = validator

        self.reviewer = reviewer

        self.preview = preview

        self.installer = installer

        self.config = (
            config or DeveloperManagerConfig()
        )

        logger.info(
            "Developer Manager initialized."
        )

    # --------------------------------------------------------

    def build(
        self,
        request: str,
        analysis: ProjectAnalysis,
        destination: Path,
    ) -> DeveloperResult:
        """
        Execute the complete Developer pipeline.
        """

        result = DeveloperResult(
            stage=DeveloperStage.PLANNING,
            
        )
        result.analysis = analysis
        logger.info(
            "Developer pipeline started."
        )
        # --------------------------------------------------------
        # Planning
        # --------------------------------------------------------

        result.stage = DeveloperStage.PLANNING

        planner_result = self.planner.plan(
    request=request,
   )

        result.planner = planner_result

        # --------------------------------------------------------
        # Architecture
        # --------------------------------------------------------

        result.stage = DeveloperStage.ARCHITECTING

        architecture = self.architect.design(
            planner_result,
        )

        result.architecture = architecture

        # --------------------------------------------------------
        # Generation
        # --------------------------------------------------------

        result.stage = DeveloperStage.GENERATING

        generator_result = self.generator.generate(
            architecture,
        )

        result.generator = generator_result

        # --------------------------------------------------------
        # Template Rendering
        # --------------------------------------------------------

        result.stage = DeveloperStage.BUILDING

        template_result = self.template_engine.render(
            generator_result.tasks,
        )

        result.templates = template_result

        # --------------------------------------------------------
        # Validation
        # --------------------------------------------------------

        result.stage = DeveloperStage.VALIDATING

        validation_result = self.validator.validate(
            template_result.files,
        )

        result.validation = validation_result

        if (
            self.config.stop_on_validation_failure
            and not validation_result.valid
        ):

            result.stage = DeveloperStage.FAILED

            result.finish()

            return result

        # --------------------------------------------------------
        # Review
        # --------------------------------------------------------

        result.stage = DeveloperStage.REVIEWING

        review_result = self.reviewer.review(
            template_result.files,
        )

        result.review = review_result

        if (
            self.config.stop_on_review_failure
            and not review_result.approved
        ):

            result.stage = DeveloperStage.FAILED

            result.finish()

            return result

        # --------------------------------------------------------
        # Preview
        # --------------------------------------------------------

        result.stage = DeveloperStage.PREVIEWING

        preview_report = self.preview.build(
            generator=generator_result,
            files=template_result.files,
            validation=validation_result,
            review=review_result,
        )

        result.preview = preview_report
        # --------------------------------------------------------
        # Installation
        # --------------------------------------------------------

        if self.config.auto_install:

            result.stage = DeveloperStage.INSTALLING

            installation = self.installer.install(
                plugin_name=generator_result.plugin_name,
                destination=destination,
                files=template_result.files,
            )

            result.installation = installation

        # --------------------------------------------------------
        # Complete
        # --------------------------------------------------------

        result.stage = DeveloperStage.COMPLETED

        result.successful = True

        result.finish()

        logger.info(
            "Developer pipeline completed successfully."
        )

        return result

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        result: DeveloperResult,
    ) -> dict[str, object]:
        """
        Return pipeline diagnostics.
        """

        return {

            "stage":
                result.stage.value,

            "successful":
                result.successful,

            "planner":
                result.planner is not None,

            "architecture":
                result.architecture is not None,

            "generator":
                result.generator is not None,

            "templates":
                result.templates is not None,

            "validation":
                result.validation is not None,

            "review":
                result.review is not None,

            "preview":
                result.preview is not None,

            "installation":
                result.installation is not None,

            "duration":
                result.duration,

        }

    # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        result: DeveloperResult,
    ) -> str:
        """
        Human-readable pipeline summary.
        """

        return (
            f"Pipeline: {result.stage.value}\n"
            f"Successful: {result.successful}\n"
            f"Plugin: "
            f"{result.planner.plugin_name if result.planner else 'N/A'}\n"
            f"Validation: "
            f"{result.validation.valid if result.validation else 'N/A'}\n"
            f"Review Score: "
            f"{result.review.score if result.review else 'N/A'}\n"
            f"Installed: "
            f"{result.installation.success if result.installation else False}"
        )

    # ============================================================
    # Representation
    # ============================================================

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"config={self.config!r})"
        )