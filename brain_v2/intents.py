from enum import Enum


class Intent(Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"

    SHOW = "SHOW"
    HIDE = "HIDE"

    SELECT = "SELECT"
    DESELECT = "DESELECT"

    CREATE = "CREATE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"

    SEARCH = "SEARCH"
    EXPLAIN = "EXPLAIN"
    ANSWER = "ANSWER"

    GENERATE = "GENERATE"
    ASK_KNOWLEDGE = "ASK_KNOWLEDGE"

    PROPOSE_PLUGIN = "PROPOSE_PLUGIN"
    PREVIEW_PLUGIN = "PREVIEW_PLUGIN"
    APPROVE_PLUGIN = "APPROVE_PLUGIN"
    REJECT_PLUGIN = "REJECT_PLUGIN"

    UNKNOWN = "UNKNOWN"
OPEN_APPLICATION = {
    "open",
    "launch",
    "start",
    "run",
    "bring"
}

CLOSE_APPLICATION = {
    "close",
    "exit",
    "quit",
    "terminate",
    "kill"
}

SEARCH = {
    "search",
    "google",
    "look",
    "find"
}

PLUGIN_CREATION = {
    "add",
    "build",
    "create",
    "make",
    "teach",
}

ASK_KNOWLEDGE_KEYWORDS = {
    "according to my notes",
    "from my files",
    "in my knowledge base",
    "search my documents",
    "what do my notes say",
    "check my notes",
}
