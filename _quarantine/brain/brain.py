from brain.intent_engine import IntentEngine
from brain.entity_extractor import EntityExtractor
from brain.planner import Planner
from brain.working_memory import WorkingMemory
from brain.context_manager import ContextManager
from brain.models import BrainResult


class Brain:
    """
    Central decision-making component for ROV.
    """

    def __init__(self):

        self.intent_engine = IntentEngine()
        self.entity_extractor = EntityExtractor()
        self.memory = WorkingMemory()
        self.context = ContextManager(self.memory)
        self.planner = Planner()

    def think(self, text: str):

        # Resolve references like "it", "that", etc.
        text = self.context.resolve(text)

        # Detect intent
        intent = self.intent_engine.detect(text)

        # Extract entities
        entities = self.entity_extractor.extract(text)

        # Create execution plan
        plan = self.planner.create(intent, entities)

        # Store latest entities in memory
        if entities:
            self.memory.remember("last_entities", entities)

        return BrainResult(
            intent=intent,
            entities=entities,
            plan=plan,
            response=f"Detected {intent.name.lower()} intent."
        )