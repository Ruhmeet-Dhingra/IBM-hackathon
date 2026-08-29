"""
ROV Developer v1.0
reviewer.py

Reviews validated plugin files for quality,
maintainability, security and best practices.

Pipeline

GeneratedFile(s)
        │
        ▼
Reviewer
        │
        ▼
ReviewResult
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from devloper.models import (
    GeneratedFile,
    ReviewFinding,
    ReviewResult,
    ReviewSeverity,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class ReviewerError(Exception):
    """Base reviewer exception."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class ReviewerConfig:
    """
    Reviewer configuration.
    """

    check_security: bool = True

    check_style: bool = True

    check_maintainability: bool = True

    check_documentation: bool = True


# ============================================================
# Reviewer
# ============================================================


class Reviewer:
    """
    Reviews generated plugin files.
    """

    def __init__(
        self,
        config: ReviewerConfig | None = None,
    ) -> None:

        self.config = config or ReviewerConfig()

        logger.info("Reviewer initialized.")

    # --------------------------------------------------------

    def review(
        self,
        files: list[GeneratedFile],
    ) -> ReviewResult:
        """
        Review generated plugin files.
        """

        start = time.perf_counter()

        result = ReviewResult(
            approved=True,
            score=100.0,
        )

        for file in files:

            self._review_file(
                file,
                result,
            )

        self._calculate_score(
            result,
        )

        result.summary = self.summary(
            result,
        )

        logger.info(
            "Review completed in %.2f ms.",
            (
                time.perf_counter()
                - start
            )
            * 1000,
        )

        return result
        # ============================================================
    # File Review
    # ============================================================

    def _review_file(
        self,
        file: GeneratedFile,
        result: ReviewResult,
    ) -> None:
        """
        Review a single generated file.
        """

        if self.config.check_security:
            self._review_security(
                file,
                result,
            )

        if self.config.check_style:
            self._review_style(
                file,
                result,
            )

        if self.config.check_documentation:
            self._review_documentation(
                file,
                result,
            )

        if self.config.check_maintainability:
            self._review_maintainability(
                file,
                result,
            )

    # ============================================================
    # Security Review
    # ============================================================

    def _review_security(
        self,
        file: GeneratedFile,
        result: ReviewResult,
    ) -> None:
        """
        Review for common security concerns.
        """

        dangerous = (
            "eval(",
            "exec(",
            "os.system(",
            "subprocess.Popen(",
            "pickle.loads(",
        )

        for pattern in dangerous:

            if pattern in file.content:

                result.findings.append(
                    ReviewFinding(
                        severity=ReviewSeverity.WARNING,
                        category="Security",
                        title="Potentially Dangerous Code",
                        description=(
                            f"Found '{pattern}' "
                            "in generated code."
                        ),
                        recommendation=(
                            "Review this usage carefully."
                        ),
                        file=file.path,
                    )
                )

    # ============================================================
    # Style Review
    # ============================================================

    def _review_style(
        self,
        file: GeneratedFile,
        result: ReviewResult,
    ) -> None:
        """
        Perform basic style checks.
        """

        lines = file.content.splitlines()

        for index, line in enumerate(
            lines,
            start=1,
        ):

            if len(line) > 100:

                result.findings.append(
                    ReviewFinding(
                        severity=ReviewSeverity.INFO,
                        category="Style",
                        title="Long Line",
                        description=(
                            "Line exceeds "
                            "100 characters."
                        ),
                        recommendation=(
                            "Break long lines."
                        ),
                        file=file.path,
                        line=index,
                    )
                )

    # ============================================================
    # Documentation Review
    # ============================================================

    def _review_documentation(
        self,
        file: GeneratedFile,
        result: ReviewResult,
    ) -> None:
        """
        Ensure Python files contain a module docstring.
        """

        if file.path.suffix != ".py":
            return

        stripped = file.content.lstrip()

        if not (
            stripped.startswith('"""')
            or stripped.startswith("'''")
        ):

            result.findings.append(
                ReviewFinding(
                    severity=ReviewSeverity.INFO,
                    category="Documentation",
                    title="Missing Module Docstring",
                    description=(
                        "Python module has no "
                        "top-level docstring."
                    ),
                    recommendation=(
                        "Add a module docstring."
                    ),
                    file=file.path,
                )
            )

    # ============================================================
    # Maintainability Review
    # ============================================================

    def _review_maintainability(
        self,
        file: GeneratedFile,
        result: ReviewResult,
    ) -> None:
        """
        Perform basic maintainability checks.
        """

        line_count = len(
            file.content.splitlines()
        )

        if line_count > 500:

            result.findings.append(
                ReviewFinding(
                    severity=ReviewSeverity.WARNING,
                    category="Maintainability",
                    title="Large File",
                    description=(
                        f"{line_count} lines detected."
                    ),
                    recommendation=(
                        "Consider splitting "
                        "the file."
                    ),
                    file=file.path,
                )
            )
        # ============================================================
    # Score Calculation
    # ============================================================

    def _calculate_score(
        self,
        result: ReviewResult,
    ) -> None:
        """
        Calculate an overall review score.
        """

        score = 100.0

        for finding in result.findings:

            if finding.severity == ReviewSeverity.INFO:
                score -= 1

            elif finding.severity == ReviewSeverity.WARNING:
                score -= 5

            elif finding.severity == ReviewSeverity.ERROR:
                score -= 15

            elif finding.severity == ReviewSeverity.CRITICAL:
                score -= 30

        result.score = max(0.0, score)

        result.approved = (
            result.critical_count == 0
            and result.error_count == 0
        )

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        result: ReviewResult,
    ) -> dict[str, object]:
        """
        Return review diagnostics.
        """

        return {
            "approved": result.approved,
            "score": result.score,
            "findings": len(result.findings),
            "critical": result.critical_count,
            "errors": result.error_count,
            "warnings": result.warning_count,
        }

    # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        result: ReviewResult,
    ) -> str:
        """
        Human-readable review summary.
        """

        status = (
            "APPROVED"
            if result.approved
            else "REQUIRES CHANGES"
        )

        return (
            f"Review {status}\n"
            f"Score : {result.score:.1f}/100\n"
            f"Findings : {len(result.findings)}\n"
            f"Critical : {result.critical_count}\n"
            f"Errors : {result.error_count}\n"
            f"Warnings : {result.warning_count}"
        )

    # ============================================================
    # Utility
    # ============================================================

    @staticmethod
    def has_findings(
        result: ReviewResult,
    ) -> bool:
        """
        Return True if any findings exist.
        """

        return len(result.findings) > 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(config={self.config!r})"
        )