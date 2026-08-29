from planner import Planner
from intents import Intent
from entities import EntityType

planner = Planner()

entities = [
    {
        "type": EntityType.APPLICATION,
        "name": "Chrome"
    }
]

plan = planner.create(Intent.OPEN, entities)

print(plan.steps)


