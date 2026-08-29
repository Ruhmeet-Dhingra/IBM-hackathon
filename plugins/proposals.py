"""Create, review, approve, and reject generated ROV plugin proposals."""

from __future__ import annotations

import ast
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from core_v2.core_types import OperationResult


class PluginProposalError(Exception):
    """Raised when a plugin proposal is unsafe or invalid."""


@dataclass(frozen=True)
class PluginDraft:
    name: str
    description: str
    commands: list[str]
    permissions: list[str]
    plugin_code: str


class PluginCodeGenerator(Protocol):
    def generate(self, request: str) -> PluginDraft:
        """Generate a draft plugin without writing it to disk."""


class PluginProposalService:
    """Persist generated code in staging until the user explicitly approves it."""

    _ALLOWED_IMPORTS = {
        "collections",
        "dataclasses",
        "datetime",
        "json",
        "math",
        "re",
        "statistics",
        "typing",
        "plugins",
    }
    _BLOCKED_CALLS = {
        "compile",
        "eval",
        "exec",
        "input",
        "open",
        "__import__",
    }

    def __init__(
        self,
        generator: PluginCodeGenerator,
        plugin_root: Path | None = None,
    ) -> None:
        self.generator = generator
        self.plugin_root = plugin_root or Path(__file__).resolve().parent
        self.staging_root = self.plugin_root / "staged"
        self.installed_root = self.plugin_root / "installed"

    def propose(self, request: str) -> OperationResult:
        request = request.strip()
        if not request:
            return OperationResult(False, "Please describe the feature you want ROV to add.")

        try:
            draft = self.generator.generate(request)
            self._validate_draft(draft)
            proposal_id = self._create_proposal_id(draft.name)
            proposal_directory = self.staging_root / proposal_id
            proposal_directory.mkdir(parents=True, exist_ok=False)
            metadata = {
                "proposal_id": proposal_id,
                "status": "pending",
                "request": request,
                "created_at": datetime.now(UTC).isoformat(),
                "draft": asdict(draft),
            }
            self._write_json(proposal_directory / "proposal.json", metadata)
            (proposal_directory / "plugin.py").write_text(
                draft.plugin_code,
                encoding="utf-8",
            )
        except (PluginProposalError, OSError, ValueError) as error:
            return OperationResult(False, f"Plugin proposal was not created: {error}")

        preview = self.preview(proposal_id)
        return OperationResult(
            True,
            (
                f"I created plugin proposal '{proposal_id}'. It is staged only and "
                "will not run until you approve it."
            ),
            data={"proposal_id": proposal_id, "preview": preview.data["preview"]},
        )

    def preview(self, proposal_id: str) -> OperationResult:
        proposal_directory = self._resolve_staged_proposal(proposal_id)
        if proposal_directory is None:
            return OperationResult(False, f"No staged plugin proposal named '{proposal_id}' exists.")

        metadata = self._read_json(proposal_directory / "proposal.json")
        draft = metadata["draft"]
        preview = "\n".join(
            [
                f"Plugin proposal: {metadata['proposal_id']}",
                f"Status: {metadata['status']}",
                f"Request: {metadata['request']}",
                f"Description: {draft['description']}",
                f"Commands: {', '.join(draft['commands']) or 'None'}",
                f"Permissions: {', '.join(draft['permissions']) or 'None'}",
                "",
                "--- plugin.py ---",
                draft["plugin_code"],
                "--- end plugin.py ---",
            ]
        )
        return OperationResult(True, f"Showing proposal '{metadata['proposal_id']}'.", data={"preview": preview})

    def approve(self, proposal_id: str) -> OperationResult:
        proposal_directory = self._resolve_staged_proposal(proposal_id)
        if proposal_directory is None:
            return OperationResult(False, f"No staged plugin proposal named '{proposal_id}' exists.")

        metadata_path = proposal_directory / "proposal.json"
        metadata = self._read_json(metadata_path)
        if metadata["status"] != "pending":
            return OperationResult(False, f"Proposal '{metadata['proposal_id']}' is {metadata['status']}.")

        destination = self.installed_root / proposal_directory.name
        if destination.exists():
            return OperationResult(False, f"A plugin named '{proposal_directory.name}' is already installed.")

        metadata["status"] = "approved"
        metadata["approved_at"] = datetime.now(UTC).isoformat()
        self._write_json(metadata_path, metadata)
        self.installed_root.mkdir(parents=True, exist_ok=True)
        shutil.move(str(proposal_directory), str(destination))

        return OperationResult(
            True,
            f"Plugin '{metadata['proposal_id']}' is now installed and available to ROV.",
            data={"plugin_id": metadata["proposal_id"]},
        )

    def reject(self, proposal_id: str) -> OperationResult:
        proposal_directory = self._resolve_staged_proposal(proposal_id)
        if proposal_directory is None:
            return OperationResult(False, f"No staged plugin proposal named '{proposal_id}' exists.")

        metadata_path = proposal_directory / "proposal.json"
        metadata = self._read_json(metadata_path)
        if metadata["status"] != "pending":
            return OperationResult(False, f"Proposal '{metadata['proposal_id']}' is {metadata['status']}.")

        metadata["status"] = "rejected"
        metadata["rejected_at"] = datetime.now(UTC).isoformat()
        self._write_json(metadata_path, metadata)
        return OperationResult(True, f"Plugin proposal '{metadata['proposal_id']}' was rejected and remains inactive.")

    def _validate_draft(self, draft: PluginDraft) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_]{2,63}", draft.name):
            raise PluginProposalError("plugin names must use lowercase letters, numbers, and underscores")
        if not draft.description.strip():
            raise PluginProposalError("the plugin description is empty")
        if not draft.commands:
            raise PluginProposalError("the plugin does not declare a command")
        if not draft.plugin_code.strip():
            raise PluginProposalError("the plugin code is empty")

        try:
            tree = ast.parse(draft.plugin_code)
        except SyntaxError as error:
            raise PluginProposalError(f"plugin code has invalid Python syntax: {error.msg}") from error

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = node.names
                module = node.module if isinstance(node, ast.ImportFrom) else None
                imported = [module] if module else [name.name for name in names]
                for name in imported:
                    root_name = (name or "").split(".")[0]
                    if root_name not in self._ALLOWED_IMPORTS:
                        raise PluginProposalError(f"import '{name}' is not permitted in generated plugins")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in self._BLOCKED_CALLS:
                    raise PluginProposalError(f"call to '{node.func.id}' is not permitted in generated plugins")

    def _create_proposal_id(self, name: str) -> str:
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        return f"{name}_{timestamp}"

    def _resolve_staged_proposal(self, proposal_id: str) -> Path | None:
        if proposal_id == "latest":
            candidates = sorted(
                self.staging_root.glob("*/proposal.json"),
                key=lambda path: path.stat().st_mtime,
                reverse=True,
            )
            for metadata_path in candidates:
                if self._read_json(metadata_path).get("status") == "pending":
                    return metadata_path.parent
            return None

        candidate = self.staging_root / proposal_id
        if candidate.is_dir() and (candidate / "proposal.json").is_file():
            return candidate
        return None

    @staticmethod
    def _read_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write_json(path: Path, content: dict) -> None:
        path.write_text(json.dumps(content, indent=2), encoding="utf-8")
