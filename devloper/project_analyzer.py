"""
ROV Developer v1.0
project_analyzer.py

Scans an existing project and produces a ProjectAnalysis.
"""

from __future__ import annotations

import logging
import platform
from dataclasses import dataclass
from pathlib import Path

from devloper.models import (
    ProjectAnalysis,
    ProjectInfo,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class ProjectAnalyzerError(Exception):
    """Base Project Analyzer exception."""


# ============================================================
# Configuration
# ============================================================


@dataclass(slots=True)
class ProjectAnalyzerConfig:
    """
    Configuration for project scanning.
    """

    ignore_hidden: bool = True

    ignore_git: bool = True

    follow_symlinks: bool = False


# ============================================================
# Project Analyzer
# ============================================================


class ProjectAnalyzer:
    """
    Analyze an existing project directory.
    """

    def __init__(
        self,
        config: ProjectAnalyzerConfig | None = None,
    ) -> None:

        self.config = (
            config or ProjectAnalyzerConfig()
        )

        logger.info(
            "Project Analyzer initialized."
        )

    # --------------------------------------------------------

    def analyze(
        self,
        root: Path,
    ) -> ProjectAnalysis:
        """
        Analyze a project.
        """

        root = Path(root).resolve()

        if not root.exists():

            raise ProjectAnalyzerError(
                f"Directory does not exist: {root}"
            )

        logger.info(
            "Analyzing project: %s",
            root,
        )

        project = ProjectInfo(
            project_name=root.name,
            root_directory=root,
            python_version=platform.python_version(),
        )

        # --------------------------------------------------------
        # Project Scanning
        # --------------------------------------------------------

        python_files = self._find_python_files(
            root,
        )

        packages = self._find_packages(
            python_files,
            root,
        )

        modules = self._find_modules(
            python_files,
            root,
        )

        plugins = self._find_plugins(
            root,
        )

        imports = self._find_imports(
            python_files
        )

        dependencies = self._find_dependencies(
            imports
        )

        capabilities = self._find_capabilities(
            imports
        )

        return ProjectAnalysis(
            project=project,
            python_files=python_files,
            packages=packages,
            modules=modules,
            plugins=plugins,
            imports=imports,
            capabilities=capabilities,
            dependencies=dependencies,
        )

    # ============================================================
    # Discovery
    # ============================================================

    def _find_python_files(
        self,
        root: Path,
    ) -> list[Path]:
        """
        Find every Python file.
        """

        files: list[Path] = []

        for path in root.rglob("*.py"):

            if (
                self.config.ignore_hidden
                and any(
                    part.startswith(".")
                    for part in path.parts
                )
            ):
                continue

            if (
                self.config.ignore_git
                and ".git" in path.parts
            ):
                continue

            files.append(path)

        return sorted(files)

    def _find_packages(
        self,
        python_files: list[Path],
        root: Path,
    ) -> list[str]:
        """
        Find Python packages.
        """

        packages: list[str] = []

        for file in python_files:

            if file.name != "__init__.py":
                continue

            package = (
                file.parent
                .relative_to(root)
                .as_posix()
                .replace("/", ".")
            )

            packages.append(package)

        return sorted(packages)

    def _find_modules(
        self,
        python_files: list[Path],
        root: Path,
    ) -> list[str]:
        """
        Find Python modules.
        """

        modules: list[str] = []

        for file in python_files:

            if file.name == "__init__.py":
                continue

            module = (
                file.relative_to(root)
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
            )

            modules.append(module)

        return sorted(modules)

    def _find_plugins(
        self,
        root: Path,
    ) -> list[str]:
        """
        Find plugin folders by locating
        directories containing manifest.json.
        """

        plugins: list[str] = []

        for manifest in root.rglob("manifest.json"):

            plugins.append(
                manifest.parent.name
            )

        return sorted(plugins)
        # ============================================================
    # Analysis
    # ============================================================

    def _find_imports(
        self,
        python_files: list[Path],
    ) -> list[str]:
        """
        Collect imported modules using AST.
        """

        import ast

        imports: set[str] = set()

        for file in python_files:

            try:

                tree = ast.parse(
                    file.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception:

                continue

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.Import,
                ):

                    for alias in node.names:

                        imports.add(
                            alias.name.split(".")[0]
                        )

                elif isinstance(
                    node,
                    ast.ImportFrom,
                ):

                    if node.module:

                        imports.add(
                            node.module.split(".")[0]
                        )

        return sorted(imports)

    def _find_dependencies(
        self,
        imports: list[str],
    ) -> list[str]:
        """
        Estimate third-party dependencies.
        """

        import sys

        stdlib = set(sys.stdlib_module_names)

        dependencies = [

            module

            for module in imports

            if module not in stdlib

        ]

        return sorted(dependencies)

    def _find_capabilities(
        self,
        imports: list[str],
    ) -> list[str]:
        """
        Infer project capabilities from imports.
        """

        capabilities: set[str] = set()

        mapping = {

            "requests": "networking",
            "httpx": "networking",
            "socket": "networking",

            "cv2": "computer_vision",
            "PIL": "image_processing",

            "numpy": "scientific_computing",
            "pandas": "data_processing",

            "sqlite3": "database",
            "sqlalchemy": "database",

            "subprocess": "process_management",

            "pathlib": "filesystem",
            "os": "filesystem",
            "shutil": "filesystem",

            "threading": "multithreading",
            "asyncio": "async_programming",

        }

        for module in imports:

            capability = mapping.get(module)

            if capability:

                capabilities.add(
                    capability
                )

        return sorted(capabilities)