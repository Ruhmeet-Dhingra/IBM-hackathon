from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Step

from skills.browser import actions


class BrowserSkill:
    """
    Executes browser-related actions.
    """

    def execute(
        self,
        step: Step,
    ):

        if step.action == Action.OPEN_URL:

            return actions.open(
                step.parameters["url"]
            )

        elif step.action == Action.OPEN_WEBSITE:

            return actions.open(
                step.parameters["url"]
            )

        elif step.action == Action.SEARCH_WEB:

            return actions.search(
                step.parameters["query"]
            )

        raise ValueError(
            f"Unsupported action: {step.action}"
        )
