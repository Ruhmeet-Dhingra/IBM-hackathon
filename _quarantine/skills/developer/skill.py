from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Plan

from skills.developer import actions


class DeveloperSkill:
    """
    Executes developer-related actions.
    """

    def execute(
        self,
        step: Plan,
    ):

        if step.action == Action.GENERATE_PLUGIN:

            return actions.generate_plugin(
                step.parameters["prompt"]
            )

        elif step.action == Action.ANALYZE_PROJECT:

            return actions.analyze_project(
                step.parameters["path"]
            )

        elif step.action == Action.REVIEW_CODE:

            return actions.review_code(
                step.parameters["path"]
            )

        elif step.action == Action.CREATE_PROJECT:

            return actions.create_project(
                step.parameters["prompt"]
            )

        raise ValueError(
            f"Unsupported action: {step.action}"
        )