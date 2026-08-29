from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Step

from skills.application import actions


class ApplicationSkill:
    """
    Executes application-related actions.
    """

    def execute(
        self,
        step: Step,
    ):

        if step.action == Action.LAUNCH_APPLICATION:

            return actions.launch(step.parameters["application"])

        elif step.action == Action.CLOSE_APPLICATION:

            return actions.close(step.parameters["application"])

        raise ValueError(
            f"Unsupported action: {step.action}"
        )
