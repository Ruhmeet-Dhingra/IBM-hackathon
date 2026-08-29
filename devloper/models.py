"""
ROV Developer v1.0
models.py

Author:
    Ruhmeet Dhingra

Description:
    Central data models used throughout the ROV Developer
    pipeline.

This module contains immutable and mutable dataclasses that
represent every stage of plugin generation.

Pipeline:

Project Analyzer
        ↓
Planner
        ↓
Architect
        ↓
Generator
        ↓
Template Engine
        ↓
Validator
        ↓
Reviewer
        ↓
Preview
        ↓
Installer

No business logic belongs here.

Only data structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# ENUMS
# ============================================================


class DeveloperStage(Enum):
    """
    Current stage of the Developer pipeline.
    """

    ANALYZING = "Analyzing"

    PLANNING = "Planning"

    ARCHITECTING = "Architecting"

    GENERATING = "Generating"

    BUILDING = "Building"

    VALIDATING = "Validating"

    REVIEWING = "Reviewing"

    PREVIEWING = "Previewing"

    INSTALLING = "Installing"

    COMPLETED = "Completed"

    FAILED = "Failed"


class PluginType(Enum):
    """
    Type of plugin.
    """

    COMMAND = "command"

    AUTOMATION = "automation"

    TOOL = "tool"

    API = "api"

    UI = "ui"

    SYSTEM = "system"

    AI = "ai"

    OTHER = "other"


class PluginPermission(Enum):
    """
    Permissions required by plugin.
    """

    INTERNET = "internet"

    FILESYSTEM = "filesystem"

    CAMERA = "camera"

    MICROPHONE = "microphone"

    CLIPBOARD = "clipboard"

    SHELL = "shell"

    NOTIFICATIONS = "notifications"

    PROCESS = "process"

    WINDOW = "window"

    NONE = "none"


class ReviewSeverity(Enum):

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"


# ============================================================
# BASE MODEL
# ============================================================


@dataclass(slots=True)
class BaseModel:
    """
    Base model for every Developer dataclass.
    """

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)


# ============================================================
# PROJECT ANALYSIS
# ============================================================


@dataclass(slots=True)
class ProjectInfo(BaseModel):
    """
    Basic information about the scanned project.
    """

    project_name: str

    root_directory: Path

    python_version: str

    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):

        self.root_directory = Path(self.root_directory)

        if not self.project_name.strip():
            raise ValueError("Project name cannot be empty.")


@dataclass(slots=True)
class ProjectAnalysis(BaseModel):
    """
    Output of ProjectAnalyzer.
    """

    project: ProjectInfo

    python_files: List[Path]

    packages: List[str]

    modules: List[str]

    plugins: List[str]

    imports: List[str]

    capabilities: List[str]

    dependencies: List[str]

    ignored_files: List[Path] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    def total_python_files(self) -> int:
        return len(self.python_files)

    def total_plugins(self) -> int:
        return len(self.plugins)


# ============================================================
# PLANNER
# ============================================================


@dataclass(slots=True)
class Requirement(BaseModel):
    """
    A single functional requirement.
    """

    description: str

    required: bool = True


@dataclass(slots=True)
class PlannerResult(BaseModel):
    """
    Output of Planner.
    """

    user_request: str

    plugin_name: str

    description: str

    plugin_type: PluginType

    requirements: List[Requirement]

    commands: List[str]

    permissions: List[PluginPermission]

    assumptions: List[str] = field(default_factory=list)

    notes: List[str] = field(default_factory=list)

    confidence: float = 1.0

    def __post_init__(self):

        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1.")


# ============================================================
# ARCHITECT
# ============================================================


@dataclass(slots=True)
class ArchitecturePlan(BaseModel):
    """
    Output of Architect.
    """

    plugin_name: str

    description: str

    plugin_type: PluginType

    module_name: str

    entry_class: str

    commands: List[str]

    dependencies: List[str]

    permissions: List[PluginPermission]

    required_files: List[str]

    communication: List[str]

    security_notes: List[str]

    future_extensions: List[str] = field(default_factory=list)

    estimated_complexity: str = "Medium"

    estimated_time: int = 0

    def requires_internet(self) -> bool:
        return PluginPermission.INTERNET in self.permissions

    def requires_shell(self) -> bool:
        return PluginPermission.SHELL in self.permissions


# ============================================================
# GENERATOR
# ============================================================


@dataclass(slots=True)
class GeneratedFile(BaseModel):
    """
    Represents a generated source file before
    writing it to disk.
    """

    path: Path

    content: str

    description: str

    overwrite: bool = False

    executable: bool = False

    encoding: str = "utf-8"

    def __post_init__(self):

        self.path = Path(self.path)

        if not self.content.strip():
            raise ValueError(
                f"{self.path} has no content."
            )


@dataclass(slots=True)
class TemplateTask(BaseModel):
    """
    A template rendering task produced by the Generator.
    """

    template: str

    output: Path

    context: Dict[str, Any]

    overwrite: bool = False

    def __post_init__(self):
        self.output = Path(self.output)


@dataclass(slots=True)
class GeneratorResult(BaseModel):
    """
    Output from Generator.
    """

    plugin_name: str

    description: str

    plugin_type: PluginType

    tasks: List[TemplateTask]

    commands: List[str]

    dependencies: List[str]

    permissions: List[PluginPermission]

    estimated_lines: int

    summary: str

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def task_count(self) -> int:
        return len(self.tasks)


# ============================================================
# TEMPLATE ENGINE
# ============================================================


@dataclass(slots=True)
class TemplateResult(BaseModel):
    """
    Final rendered files.
    """

    files: List[GeneratedFile]

    rendered_templates: List[str]

    variables: Dict[str, Any]

    successful: bool

    duration_ms: float

    def total_files(self) -> int:
        return len(self.files)


# ============================================================
# VALIDATOR
# ============================================================


@dataclass(slots=True)
class ValidationIssue(BaseModel):
    """
    Single validation issue.
    """

    severity: ReviewSeverity

    title: str

    message: str

    file: Optional[Path] = None

    line: Optional[int] = None

    column: Optional[int] = None

    suggestion: Optional[str] = None

    def __post_init__(self):

        if self.file is not None:
            self.file = Path(self.file)


@dataclass(slots=True)
class ValidationResult(BaseModel):
    """
    Validation output.
    """

    valid: bool

    syntax_valid: bool

    manifest_valid: bool

    imports_valid: bool

    ast_valid: bool

    issues: List[ValidationIssue] = field(
        default_factory=list
    )

    checked_files: List[Path] = field(
        default_factory=list
    )

    validation_time_ms: float = 0.0

    def error_count(self) -> int:

        return sum(
            issue.severity in (
                ReviewSeverity.ERROR,
                ReviewSeverity.CRITICAL,
            )
            for issue in self.issues
        )

    def warning_count(self) -> int:

        return sum(
            issue.severity == ReviewSeverity.WARNING
            for issue in self.issues
        )

    def add_issue(
        self,
        issue: ValidationIssue,
    ) -> None:

        self.issues.append(issue)

        if issue.severity in (
            ReviewSeverity.ERROR,
            ReviewSeverity.CRITICAL,
        ):
            self.valid = False
    # ============================================================
# REVIEWER
# ============================================================


@dataclass(slots=True)
class ReviewFinding(BaseModel):
    """
    A single AI review finding.
    """

    severity: ReviewSeverity

    category: str

    title: str

    description: str

    recommendation: str

    file: Optional[Path] = None

    line: Optional[int] = None

    confidence: float = 1.0

    def __post_init__(self):

        if self.file is not None:
            self.file = Path(self.file)

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )


@dataclass(slots=True)
class ReviewResult(BaseModel):
    """
    Output produced by the Reviewer.
    """

    approved: bool

    score: float

    findings: List[ReviewFinding] = field(default_factory=list)

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    summary: str = ""

    reviewed_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def __post_init__(self):

        if not 0 <= self.score <= 100:
            raise ValueError(
                "Review score must be between 0 and 100."
            )

    @property
    def critical_count(self) -> int:

        return sum(
            finding.severity == ReviewSeverity.CRITICAL
            for finding in self.findings
        )

    @property
    def warning_count(self) -> int:

        return sum(
            finding.severity == ReviewSeverity.WARNING
            for finding in self.findings
        )

    @property
    def error_count(self) -> int:

        return sum(
            finding.severity == ReviewSeverity.ERROR
            for finding in self.findings
        )


# ============================================================
# PREVIEW
# ============================================================


@dataclass(slots=True)
class PreviewReport(BaseModel):
    """
    Installation preview shown to the user.
    """

    plugin_name: str

    description: str

    files_to_create: List[Path]

    dependencies: List[str]

    permissions: List[PluginPermission]

    commands: List[str]

    warnings: List[str]

    review_score: float

    install_size: int

    estimated_install_time: float

    safe_to_install: bool

    def total_files(self) -> int:

        return len(self.files_to_create)


# ============================================================
# INSTALLER
# ============================================================


@dataclass(slots=True)
class InstallationResult(BaseModel):
    """
    Final installation status.
    """

    success: bool

    plugin_name: str

    installed_path: Optional[Path]

    installed_files: List[Path]

    duration_ms: float

    backup_created: bool

    rollback_available: bool

    message: str

    installed_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def __post_init__(self):

        if self.installed_path is not None:
            self.installed_path = Path(
                self.installed_path
            )


# ============================================================
# PIPELINE RESULT
# ============================================================


@dataclass(slots=True)
class DeveloperResult(BaseModel):
    """
    Complete result of the Developer pipeline.

    Returned only by DeveloperManager.
    """

    stage: DeveloperStage

    analysis: Optional[ProjectAnalysis] = None

    planner: Optional[PlannerResult] = None

    architecture: Optional[ArchitecturePlan] = None

    generator: Optional[GeneratorResult] = None

    templates: Optional[TemplateResult] = None

    validation: Optional[ValidationResult] = None

    review: Optional[ReviewResult] = None

    preview: Optional[PreviewReport] = None

    installation: Optional[
        InstallationResult
    ] = None

    successful: bool = False

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    completed_at: Optional[datetime] = None

    def finish(self) -> None:

        self.completed_at = datetime.utcnow()

    @property
    def duration(self) -> float | None:

        if self.completed_at is None:
            return None

        return (
            self.completed_at - self.started_at
        ).total_seconds()


# ============================================================
# EXPORTS
# ============================================================


__all__ = [

    "DeveloperStage",

    "PluginPermission",

    "PluginType",

    "ReviewSeverity",

    "BaseModel",

    "ProjectInfo",

    "ProjectAnalysis",

    "Requirement",

    "PlannerResult",

    "ArchitecturePlan",

    "GeneratedFile",

    "TemplateTask",

    "GeneratorResult",

    "TemplateResult",

    "ValidationIssue",

    "ValidationResult",

    "ReviewFinding",

    "ReviewResult",

    "PreviewReport",

    "InstallationResult",

    "DeveloperResult",
]
