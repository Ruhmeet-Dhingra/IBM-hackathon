from brain.brain import Brain
from router.router import Router

brain = Brain()
router = Router()

result = brain.think("Open Chrome")

router.execute(
    result.plan,
    result.entities,
)