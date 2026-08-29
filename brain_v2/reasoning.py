"""
ROV Brain v2

Reasoning Engine

The Reasoner improves the Brain's understanding of a request
before an execution plan is created.

It never executes actions.
"""

from __future__ import annotations

from dataclasses import dataclass

from brain_v2.models import Plan


@dataclass
class ReasoningResult:
    """
    Result produced by the reasoning engine.
    """

    plan: Plan

    requires_clarification: bool = False

    clarification_question: str | None = None


class Reasoner:
    """
    Performs lightweight reasoning on a generated execution plan.
    """

    def reason(
        self,
        plan: Plan,
    ) -> ReasoningResult:
        """
        Analyze an execution plan.

        Future versions may:
        - Reorder actions
        - Remove duplicate actions
        - Detect ambiguity
        - Request clarification
        - Use conversation context

        For now, simply return the original plan.
        """

        return ReasoningResult(
            plan=plan
        )