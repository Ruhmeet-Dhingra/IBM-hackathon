from .intents import Intent


class IntentEngine:
    """
    Detects the user's intent from text.

    Current version:
    Rule-based.

    Future:
    AI / ML classifier.
    """

    def __init__(self):

        self.intent_keywords = {

            Intent.OPEN: [
                "open",
                "launch",
                "start"
            ],

            Intent.CLOSE: [
                "close",
                "exit",
                "quit"
            ],

            Intent.SHOW: [
                "show",
                "display",
                "view"
            ],

            Intent.HIDE: [
                "hide",
                "remove"
            ],

            Intent.EXPLAIN: [
                "explain",
                "describe",
                "tell"
            ],

            Intent.GENERATE: [
                "generate",
                "create",
                "build"
            ],
        }

    def detect(self, text: str) -> Intent:

        text = text.lower()

        for intent, keywords in self.intent_keywords.items():

            for keyword in keywords:

                if keyword in text:
                    return intent

        return Intent.UNKNOWN