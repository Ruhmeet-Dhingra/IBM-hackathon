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

    UNKNOWN = "UNKNOWN"
