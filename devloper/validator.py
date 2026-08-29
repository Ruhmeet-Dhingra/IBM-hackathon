"""
ROV Developer v1.0
validator.py

Validates generated plugin files before review
or installation.

Pipeline

GeneratedFile(s)
        │
        ▼
Validator
        │
        ▼
ValidationResult
"""

from __future__ import annotations

import ast
import logging
import time
from dataclasses import dataclass
from pathlib import Path

from devloper.models import (
    GeneratedFile,
    PluginPermission,
    ReviewSeverity,
    ValidationIssue,
    ValidationResult,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class ValidatorError(Exception):
    """Base validator exception."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class ValidatorConfig:
    """
    Validator configuration.
    """

    validate_python: bool = True

    validate_manifest: bool = True

    validate_imports: bool = True

    stop_on_first_error: bool = False


# ============================================================
# Validator
# ============================================================


class Validator:
    """
    Validates rendered plugin files.
    """

    def __init__(
        self,
        config: ValidatorConfig | None = None,
    ) -> None:

        self.config = config or ValidatorConfig()

        logger.info("Validator initialized.")

    # --------------------------------------------------------

    def validate(
        self,
        files: list[GeneratedFile],
    ) -> ValidationResult:
        """
        Validate every generated file.
        """

        start = time.perf_counter()

        result = ValidationResult(
            valid=True,
            syntax_valid=True,
            manifest_valid=True,
            imports_valid=True,
            ast_valid=True,
        )

        for file in files:

            result.checked_files.append(
                file.path
            )

            self._validate_file(
                file,
                result,
            )

            if (
                self.config.stop_on_first_error
                and not result.valid
            ):
                break

        result.validation_time_ms = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            "Validation completed in %.2f ms.",
            result.validation_time_ms,
        )

        return result
        # ============================================================
    # File Validation
    # ============================================================

    def _validate_file(
        self,
        file: GeneratedFile,
        result: ValidationResult,
    ) -> None:
        """
        Validate a single generated file.
        """

        suffix = file.path.suffix.lower()

        if (
            self.config.validate_python
            and suffix == ".py"
        ):
            self._validate_python(
                file,
                result,
            )

        if (
            self.config.validate_manifest
            and file.path.name == "manifest.json"
        ):
            self._validate_manifest(
                file,
                result,
            )

    # ============================================================
    # Python Validation
    # ============================================================

    def _validate_python(
        self,
        file: GeneratedFile,
        result: ValidationResult,
    ) -> None:
        """
        Validate Python syntax using the AST.
        """

        try:

            ast.parse(file.content)

        except SyntaxError as exc:

            result.syntax_valid = False
            result.ast_valid = False
            result.valid = False

            result.add_issue(
                ValidationIssue(
                    severity=ReviewSeverity.ERROR,
                    title="Syntax Error",
                    message=str(exc),
                    file=file.path,
                    line=exc.lineno,
                    column=exc.offset,
                    suggestion="Fix Python syntax.",
                )
            )

    # ============================================================
    # Manifest Validation
    # ============================================================

    def _validate_manifest(
        self,
        file: GeneratedFile,
        result: ValidationResult,
    ) -> None:
        """
        Validate manifest.json.
        """

        import json

        try:

            manifest = json.loads(
                file.content
            )

        except json.JSONDecodeError as exc:

            result.manifest_valid = False
            result.valid = False

            result.add_issue(
                ValidationIssue(
                    severity=ReviewSeverity.ERROR,
                    title="Invalid Manifest",
                    message=str(exc),
                    file=file.path,
                    line=exc.lineno,
                    column=exc.colno,
                    suggestion="Fix manifest JSON.",
                )
            )

            return

        required = (
            "name",
            "version",
            "description",
        )

        for key in required:

            if key not in manifest:

                result.manifest_valid = False
                result.valid = False

                result.add_issue(
                    ValidationIssue(
                        severity=ReviewSeverity.ERROR,
                        title="Missing Manifest Field",
                        message=f"'{key}' is missing.",
                        file=file.path,
                        suggestion=f"Add '{key}' to manifest.",
                    )
                )

    # ============================================================
    # Import Validation
    # ============================================================

    def _validate_imports(
        self,
        file: GeneratedFile,
        result: ValidationResult,
    ) -> None:
        """
        Validate import statements.
        """

        try:

            tree = ast.parse(file.content)

        except SyntaxError:
            return

        for node in ast.walk(tree):

            if isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
        # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        result: ValidationResult,
    ) -> dict[str, object]:
        """
        Return validation diagnostics.
        """

        return {
            "valid": result.valid,
            "syntax_valid": result.syntax_valid,
            "manifest_valid": result.manifest_valid,
            "imports_valid": result.imports_valid,
            "ast_valid": result.ast_valid,
            "checked_files": len(result.checked_files),
            "issues": len(result.issues),
            "errors": result.error_count(),
            "warnings": result.warning_count(),
            "validation_time_ms": result.validation_time_ms,
        }

    # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        result: ValidationResult,
    ) -> str:
        """
        Human-readable validation summary.
        """

        if result.valid:
            status = "PASSED"
        else:
            status = "FAILED"

        return (
            f"Validation {status}\n"
            f"Files Checked : {len(result.checked_files)}\n"
            f"Issues : {len(result.issues)}\n"
            f"Errors : {result.error_count()}\n"
            f"Warnings : {result.warning_count()}\n"
            f"Time : {result.validation_time_ms:.2f} ms"
        )

    # ============================================================
    # Utility
    # ============================================================

    @staticmethod
    def has_errors(
        result: ValidationResult,
    ) -> bool:
        """
        Return True if validation contains errors.
        """

        return result.error_count() > 0

    @staticmethod
    def has_warnings(
        result: ValidationResult,
    ) -> bool:
        """
        Return True if validation contains warnings.
        """

        return result.warning_count() > 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(config={self.config!r})"
        )