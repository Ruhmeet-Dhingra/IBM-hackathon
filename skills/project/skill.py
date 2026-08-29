"""
Project skill — handles LOCATE_PROJECT and OPEN_PROJECT.

Full implementation is not yet available; these actions return a clear
"not yet implemented" result rather than raising an unhandled error.
"""

from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Step


class ProjectSkill:
    """Handles project-related actions (locate and open)."""

    def execute(self, step: Step) -> str:
        if step.action == Action.LOCATE_PROJECT:
            project = step.parameters.get("project", "")
            return f"[not yet implemented] LOCATE_PROJECT: cannot locate '{project}' — project discovery is not yet available."

        if step.action == Action.OPEN_PROJECT:
            project = step.parameters.get("project", "")
            return f"[not yet implemented] OPEN_PROJECT: cannot open '{project}' — project open is not yet available."

        raise ValueError(f"ProjectSkill cannot handle action: {step.action}")
