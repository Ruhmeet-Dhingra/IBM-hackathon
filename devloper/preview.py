"""
ROV Developer v1.0
preview.py

Builds an installation preview for the user before
the plugin is written to disk.

Pipeline

GeneratedFile(s)
        │
ValidationResult
        │
ReviewResult
        ▼
PreviewBuilder
        │
        ▼
PreviewReport
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from devloper.models import (
    GeneratedFile,
    GeneratorResult,
    PreviewReport,
    ReviewResult,
    ValidationResult,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class PreviewError(Exception):
    """Base Preview exception."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class PreviewConfig:
    """
    Preview configuration.
    """

    include_warnings: bool = True

    include_dependencies: bool = True

    include_permissions: bool = True


# ============================================================
# Preview Builder
# ============================================================


class PreviewBuilder:
    """
    Builds a PreviewReport before installation.
    """

    def __init__(
        self,
        config: PreviewConfig | None = None,
    ) -> None:

        self.config = config or PreviewConfig()

        logger.info("Preview Builder initialized.")

    # --------------------------------------------------------

    def build(
        self,
        generator: GeneratorResult,
        files: list[GeneratedFile],
        validation: ValidationResult,
        review: ReviewResult,
    ) -> PreviewReport:
        """
        Build an installation preview.
        """

        start = time.perf_counter()

        report = PreviewReport(

            plugin_name=generator.plugin_name,

            description=generator.description,

            files_to_create=[
                file.path
                for file in files
            ],

            dependencies=(
                generator.dependencies
                if self.config.include_dependencies
                else []
            ),

            permissions=(
                generator.permissions
                if self.config.include_permissions
                else []
            ),

            commands=generator.commands,

            warnings=[],

            review_score=review.score,

            install_size=self._install_size(
                files
            ),

            estimated_install_time=0.0,

            safe_to_install=False,

        )

        self._populate_warnings(
            report,
            validation,
            review,
        )

        report.safe_to_install = self._is_safe(
         validation,
       review,
)

        report.estimated_install_time = (
        self._estimate_install_time(
        files
    )
)
        return report
        # ============================================================
    # Warning Collection
    # ============================================================

    def _populate_warnings(
        self,
        report: PreviewReport,
        validation: ValidationResult,
        review: ReviewResult,
    ) -> None:
        """
        Collect warnings from validation and review.
        """

        if self.config.include_warnings:

            for issue in validation.issues:

                report.warnings.append(
                    f"[{issue.severity.value}] "
                    f"{issue.title}: {issue.message}"
                )

            for finding in review.findings:

                report.warnings.append(
                    f"[{finding.severity.value}] "
                    f"{finding.title}: "
                    f"{finding.description}"
                )

    # ============================================================
    # Installation Size
    # ============================================================

    def _install_size(
        self,
        files: list[GeneratedFile],
    ) -> int:
        """
        Calculate the total installation size
        in bytes.
        """

        return sum(
            len(
                file.content.encode("utf-8")
            )
            for file in files
        )

    # ============================================================
    # Estimated Installation Time
    # ============================================================

    def _estimate_install_time(
        self,
        files: list[GeneratedFile],
    ) -> float:
        """
        Estimate installation time in seconds.
        """

        file_count = len(files)

        if file_count <= 5:
            return 0.5

        if file_count <= 20:
            return 1.5

        return 3.0

    # ============================================================
    # Safety Evaluation
    # ============================================================

    def _is_safe(
        self,
        validation: ValidationResult,
        review: ReviewResult,
    ) -> bool:
        """
        Determine whether installation is safe.
        """

        return (
            validation.valid
            and review.approved
        )
        # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        report: PreviewReport,
    ) -> str:
        """
        Build a human-readable preview summary.
        """

        status = (
            "SAFE TO INSTALL"
            if report.safe_to_install
            else "REVIEW REQUIRED"
        )

        return (
            f"Plugin: {report.plugin_name}\n"
            f"Status: {status}\n"
            f"Files: {len(report.files_to_create)}\n"
            f"Dependencies: {len(report.dependencies)}\n"
            f"Permissions: {len(report.permissions)}\n"
            f"Warnings: {len(report.warnings)}\n"
            f"Review Score: {report.review_score:.1f}/100\n"
            f"Install Size: {report.install_size} bytes\n"
            f"Estimated Install Time: "
            f"{report.estimated_install_time:.1f}s"
        )

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        report: PreviewReport,
    ) -> dict[str, object]:
        """
        Return diagnostic information about
        the preview report.
        """

        return {
            "plugin_name": report.plugin_name,
            "safe_to_install": report.safe_to_install,
            "file_count": len(report.files_to_create),
            "dependency_count": len(report.dependencies),
            "permission_count": len(report.permissions),
            "warning_count": len(report.warnings),
            "review_score": report.review_score,
            "install_size": report.install_size,
            "estimated_install_time": (
                report.estimated_install_time
            ),
        }

    # ============================================================
    # Utility
    # ============================================================

    @staticmethod
    def has_warnings(
        report: PreviewReport,
    ) -> bool:
        """
        Return True if the preview contains warnings.
        """

        return len(report.warnings) > 0

    @staticmethod
    def total_files(
        report: PreviewReport,
    ) -> int:
        """
        Return the number of files that will
        be created.
        """

        return len(report.files_to_create)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(config={self.config!r})"
        )