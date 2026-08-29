class WorkingMemory:
    """
    Stores temporary conversational context.
    """

    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key)

    def clear(self):
        self.memory.clear()

    def dump(self):
        return dict(self.memory)