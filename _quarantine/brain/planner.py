from brain.intents import Intent
from brain.entities import EntityType, Action
from brain.models import Plan, Step


class Planner:
    """
    Creates an execution plan from the Brain's understanding.

    No AI.
    No execution.
    Just planning.
    """

    def create(self, intent, entities):

        plan = Plan()

        # -------------------------
        # OPEN
        # -------------------------
        if intent == Intent.OPEN:

            if not entities:
                return plan

            entity = entities[0]

            if entity.type == EntityType.APPLICATION:
                plan.steps = [
   Step(
        action=Action.LAUNCH_APPLICATION,
        parameters={
            "application": entity.name
        }
    )
]

            elif entity.type == EntityType.WEBSITE:
                plan.steps = [
                     Action.OPEN_WEBSITE
                ]

            elif entity.type == EntityType.PROJECT:
                plan.steps = [
                    "locate_project",
                    "open_project"
                ]

        # -------------------------
        # CLOSE
        # -------------------------
        elif intent == Intent.CLOSE:

            plan.steps = [
                Action.CLOSE_ITEMS
            ]

        # -------------------------
        # SHOW
        # -------------------------
        elif intent == Intent.SHOW:

            plan.steps = [
                Action.SHOW_COMPONENTS
            ]

        # -------------------------
        # HIDE
        # -------------------------
        elif intent == Intent.HIDE:

            plan.steps = [
                Action.HIDE_COMPONENTS
            ]

        # -------------------------
        # EXPLAIN
        # -------------------------
        elif intent == Intent.EXPLAIN:

            plan.steps = [
                Action.NEED_REASONING
            ]

        # -------------------------
        # GENERATE
        # -------------------------
        elif intent == Intent.GENERATE:

            plan.steps = [
                Action.GENERATE_PLUGIN
            ]

        return plan