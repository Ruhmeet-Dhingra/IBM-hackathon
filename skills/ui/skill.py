"""
UI skill — handles SHOW_COMPONENT and HIDE_COMPONENT.

Full UI component control is not yet wired; these actions return a clear
"not yet implemented" result rather than raising an unhandled error.
"""

from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Step


class UISkill:
    """Handles UI component visibility actions."""

    def execute(self, step: Step) -> str:
        if step.action == Action.SHOW_COMPONENT:
            return "[not yet implemented] SHOW_COMPONENT: UI component control is not yet available."

        if step.action == Action.HIDE_COMPONENT:
            return "[not yet implemented] HIDE_COMPONENT: UI component control is not yet available."

        raise ValueError(f"UISkill cannot handle action: {step.action}")
