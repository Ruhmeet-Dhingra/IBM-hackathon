from working_memory import WorkingMemory
from context_manager import ContextManager

memory = WorkingMemory()

memory.remember("last_app", "Chrome")

context = ContextManager(memory)

print(context.resolve("Close it"))