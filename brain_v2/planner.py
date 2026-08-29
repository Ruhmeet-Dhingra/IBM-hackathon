from brain_v2.intents import Intent
from brain_v2.entities import EntityType, Action
from brain_v2.models import Entity, Plan, Step


class Planner:
    """
    Creates an execution plan from the Brain's understanding.

    No AI.
    No execution.
    Just planning.
    """

    def plan(self, intent: Intent, entities: list[Entity]) -> Plan:

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
                        parameters={"application": entity.name},
                    )
                ]

            elif entity.type == EntityType.WEBSITE:
                plan.steps = [
                    Step(
                        action=Action.OPEN_WEBSITE,
                        parameters={"url": entity.name},
                    )
                ]

            elif entity.type == EntityType.PROJECT:
                plan.steps = [
                    Step(action=Action.LOCATE_PROJECT, parameters={"project": entities[0].name}),
                    Step(action=Action.OPEN_PROJECT, parameters={"project": entities[0].name}),
                ]

        # -------------------------
        # CLOSE
        # -------------------------
        elif intent == Intent.CLOSE:

            if entities:
                plan.steps = [
                    Step(
                        action=Action.CLOSE_APPLICATION,
                        parameters={"application": entities[0].name},
                    )
                ]

        # -------------------------
        # SHOW
        # -------------------------
        elif intent == Intent.SHOW:

            plan.steps = [
                Step(action=Action.SHOW_COMPONENT, parameters={})
            ]

        # -------------------------
        # HIDE
        # -------------------------
        elif intent == Intent.HIDE:

            plan.steps = [
                Step(action=Action.HIDE_COMPONENT, parameters={})
            ]

        # -------------------------
        # EXPLAIN
        # -------------------------
        elif intent == Intent.EXPLAIN:
            plan.steps = [Step(action=Action.NEEDS_REASONING, parameters={})]

        # -------------------------
        # GENERATE
        # -------------------------
        elif intent == Intent.GENERATE:

            plan.steps = [
                Step(action=Action.GENERATE_PLUGIN, parameters={})
            ]

        elif intent == Intent.PROPOSE_PLUGIN and entities:
            plan.steps = [
                Step(
                    action=Action.PROPOSE_PLUGIN,
                    parameters={"request": entities[0].name},
                )
            ]

        elif intent == Intent.PREVIEW_PLUGIN and entities:
            plan.steps = [
                Step(
                    action=Action.PREVIEW_PLUGIN,
                    parameters={"proposal_id": entities[0].name},
                )
            ]

        elif intent == Intent.APPROVE_PLUGIN and entities:
            plan.steps = [
                Step(
                    action=Action.APPROVE_PLUGIN,
                    parameters={"proposal_id": entities[0].name},
                )
            ]

        elif intent == Intent.REJECT_PLUGIN and entities:
            plan.steps = [
                Step(
                    action=Action.REJECT_PLUGIN,
                    parameters={"proposal_id": entities[0].name},
                )
            ]

        elif intent == Intent.ASK_KNOWLEDGE and entities:
            plan.steps = [
                Step(
                    action=Action.SEARCH_KNOWLEDGE_BASE,
                    parameters={"query": entities[0].name}
                )
            ]

        elif intent == Intent.SEARCH and entities:
            plan.steps = [
                Step(
                    action=Action.SEARCH_WEB,
                    parameters={"query": entities[0].name},
                )
            ]

        return plan
