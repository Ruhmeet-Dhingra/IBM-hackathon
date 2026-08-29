"""
ROV Brain v2

The Brain is responsible for understanding a command and
producing an execution plan.

It never executes actions itself.
"""
from brain_v2.memory import Memory
from brain_v2.planner import Planner
from brain_v2.reasoning import Reasoner
from brain_v2.validator import Validator
from brain_v2.context import Context
from brain_v2.normalizer import normalize
from brain_v2.intent_recognizer import IntentRecognizer
from brain_v2.entity_extractor import EntityExtractor
from brain_v2.entities import Action
from brain_v2.models import Plan, Step
from plugins.runtime import PluginRuntime


class Brain:
    """
    Main Brain orchestrator.
    """

    def __init__(self):

        self.intent_recognizer = IntentRecognizer()

        self.entity_extractor = EntityExtractor()

        self.planner = Planner()

        self.reasoner = Reasoner()

        self.validator = Validator()

        self.context = Context()

        self.memory = Memory()

        self.plugin_runtime = PluginRuntime()

    def process(
        self,
        command: str,
    ):

        # -------------------------
        # Normalize command
        # -------------------------

        normalized = normalize(command)

        installed_plugin_id = self.plugin_runtime.find_for_command(normalized)
        if installed_plugin_id:
            plan = Plan(
                steps=[
                    Step(
                        action=Action.RUN_PLUGIN,
                        parameters={
                            "plugin_id": installed_plugin_id,
                            "command": normalized,
                        },
                    )
                ]
            )
            self.context.last_command = command
            self.memory.remember(command)
            self.memory.last_plan = plan
            return plan

        # -------------------------
        # Recognize intent
        # -------------------------

        intent = self.intent_recognizer.recognize(
            normalized
        )

        # -------------------------
        # Extract entities
        # -------------------------

        entities = self.entity_extractor.extract(
            normalized
        )

        # -------------------------
        # Planner
        # -------------------------

        plan = self.planner.plan(
            intent,
            entities,
        )

        # -------------------------
        # Reasoning
        # -------------------------

        reasoning = self.reasoner.reason(plan)

        # -------------------------
        # Validation
        # -------------------------

        validation = self.validator.validate(
            reasoning.plan
        )

        if not validation.valid:
            raise ValueError(validation.message)

        # -------------------------
        # Update Context
        # -------------------------

        self.context.last_command = command
        self.context.last_intent = intent

        if entities:
            self.context.last_entity = entities[0]

        # -------------------------
        # Update Memory
        # -------------------------

        self.memory.last_intent = intent

        if entities:
            self.memory.last_entity = entities[0]

        self.memory.last_plan = reasoning.plan

        self.memory.remember(command)

        return reasoning.plan
