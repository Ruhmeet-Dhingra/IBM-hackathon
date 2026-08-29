"""
ROV Developer v1.0
installer.py

Installs generated plugin files into the ROV project.

Pipeline

GeneratedFile(s)
        │
        ▼
Installer
        │
        ▼
InstallationResult
"""

from __future__ import annotations

import logging
import shutil
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from devloper.models import (
    GeneratedFile,
    InstallationResult,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class InstallerError(Exception):
    """Base installer exception."""


class RollbackError(InstallerError):
    """Raised when rollback fails."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class InstallerConfig:
    """
    Installer configuration.
    """

    create_backup: bool = True

    overwrite_existing: bool = False

    backup_directory: Path = Path(".rov_backups")


# ============================================================
# Installer
# ============================================================


class Installer:
    """
    Installs generated plugin files.
    """

    def __init__(
        self,
        config: InstallerConfig | None = None,
    ) -> None:

        self.config = config or InstallerConfig()

        logger.info("Installer initialized.")

    # --------------------------------------------------------

    def install(
        self,
        plugin_name: str,
        destination: Path,
        files: list[GeneratedFile],
    ) -> InstallationResult:
        """
        Install generated files.
        """

        start = time.perf_counter()

        destination = Path(destination)

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        installed_files: list[Path] = []

        backups: list[tuple[Path, Path]] = []

        try:

            for file in files:

                target = destination / file.path

                self._install_file(
                    file=file,
                    target=target,
                    installed=installed_files,
                    backups=backups,
                )

        except Exception as exc:

            self._rollback(
                backups,
                installed_files,
            )

            raise InstallerError(
                str(exc)
            ) from exc

        duration = (
            time.perf_counter()
            - start
        ) * 1000

        return InstallationResult(

            success=True,

            plugin_name=plugin_name,

            installed_path=destination,

            installed_files=installed_files,

            duration_ms=duration,

            backup_created=len(backups) > 0,

            rollback_available=len(backups) > 0,

            message="Plugin installed successfully.",
        )
        # ============================================================
  # File Installation
    # ============================================================

    def _install_file(
        self,
        file: GeneratedFile,
        target: Path,
        installed: list[Path],
        backups: list[tuple[Path, Path]],
    ) -> None:
        """
        Install a single generated file.
        """

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if target.exists():

            if not self.config.overwrite_existing:

                raise InstallerError(
                    f"{target} already exists."
                )

            if self.config.create_backup:

                backup = self._backup_file(
                    target
                )

                backups.append(
                    (target, backup)
                )

        target.write_text(
            file.content,
            encoding=file.encoding,
        )

        installed.append(target)

    # ============================================================
    # Backup
    # ============================================================

    def _backup_file(
        self,
        target: Path,
    ) -> Path:
        """
        Create a backup of an existing file.
        """

        self.config.backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup = (
            self.config.backup_directory
            / f"{target.name}.{timestamp}.bak"
        )

        shutil.copy2(
            target,
            backup,
        )

        logger.info(
            "Created backup: %s",
            backup,
        )

        return backup

    # ============================================================
    # File Writing
    # ============================================================

    @staticmethod
    def _write_file(
        target: Path,
        file: GeneratedFile,
    ) -> None:
        """
        Write file contents to disk.
        """

        target.write_text(
            file.content,
            encoding=file.encoding,
        )

        if file.executable:

            target.chmod(0o755)
    # ============================================================
    # Rollback
    # ============================================================

    def _rollback(
        self,
        backups: list[tuple[Path, Path]],
        installed: list[Path],
    ) -> None:
        """
        Restore backups and remove newly created files.
        """

        try:

            # Restore overwritten files

            for original, backup in backups:

                shutil.copy2(
                    backup,
                    original,
                )

            # Remove newly installed files

            for file in reversed(installed):

                if file.exists():

                    file.unlink()

        except Exception as exc:

            raise RollbackError(
                "Rollback failed."
            ) from exc

    # ============================================================
    # Summary
    # ============================================================

    def summary(
        self,
        result: InstallationResult,
    ) -> str:
        """
        Human-readable installation summary.
        """

        status = (
            "SUCCESS"
            if result.success
            else "FAILED"
        )

        return (
            f"Installation {status}\n"
            f"Plugin: {result.plugin_name}\n"
            f"Files Installed: "
            f"{len(result.installed_files)}\n"
            f"Backup Created: "
            f"{result.backup_created}\n"
            f"Rollback Available: "
            f"{result.rollback_available}\n"
            f"Duration: "
            f"{result.duration_ms:.2f} ms"
        )

    # ============================================================
    # Diagnostics
    # ============================================================

    def diagnostics(
        self,
        result: InstallationResult,
    ) -> dict[str, object]:
        """
        Return installation diagnostics.
        """

        return {

            "success":
                result.success,

            "plugin_name":
                result.plugin_name,

            "installed_files":
                len(result.installed_files),

            "backup_created":
                result.backup_created,

            "rollback_available":
                result.rollback_available,

            "duration_ms":
                result.duration_ms,

        }

    # ============================================================
    # Utility
    # ============================================================

    @staticmethod
    def installed_count(
        result: InstallationResult,
    ) -> int:
        """
        Number of installed files.
        """

        return len(
            result.installed_files
        )

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(config={self.config!r})"
        )