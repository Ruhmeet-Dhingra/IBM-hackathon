"""
Reasoning skill — handles NEEDS_REASONING.

Full LLM-backed reasoning is not yet wired; this action returns a clear
"not yet implemented" result rather than raising an unhandled error.
"""

from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Step


class ReasoningSkill:
    """Handles intents that require free-form AI reasoning."""

    def execute(self, step: Step) -> str:
        if step.action == Action.NEEDS_REASONING:
            return "[not yet implemented] NEEDS_REASONING: free-form reasoning is not yet available."

        raise ValueError(f"ReasoningSkill cannot handle action: {step.action}")
