"""
ROV Router

Routes Brain execution plans to the appropriate skills.
"""

from __future__ import annotations

from router.registry import SkillRegistry
from brain_v2.models import Plan


class Router:
    """
    Executes a Brain execution plan.
    """

    def __init__(self) -> None:

        self.registry = SkillRegistry()

    def execute(
        self,
        plan: Plan,
    ) -> list:

        results = []

        for step in plan.steps:

            skill = self.registry.get(
                step.action
            )

            if skill is None:
                raise ValueError(
                    f"No skill registered for action: {step.action}"
                )

            result = skill.execute(step)

            results.append(result)

        return results