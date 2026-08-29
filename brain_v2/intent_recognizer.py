"""
Recognizes the user's intent from normalized text.
"""
from brain_v2.intents import (
    Intent,
    OPEN_APPLICATION,
    CLOSE_APPLICATION,
    PLUGIN_CREATION,
    SEARCH,
)


class IntentRecognizer:

    def recognize(self, text: str) -> Intent:

        if not text:
            return Intent.UNKNOWN

        words = text.split()
        first_word = words[0]

        if len(words) >= 2 and words[1] in {"plugin", "proposal"}:
            if first_word in {"approve", "install"}:
                return Intent.APPROVE_PLUGIN
            if first_word in {"preview", "review", "show"}:
                return Intent.PREVIEW_PLUGIN
            if first_word in {"reject", "discard"}:
                return Intent.REJECT_PLUGIN

        if (
            first_word in PLUGIN_CREATION
            and len(words) >= 3
            and words[1] in {"feature", "plugin"}
        ):
            return Intent.PROPOSE_PLUGIN

        if first_word in OPEN_APPLICATION:
            return Intent.OPEN

        if first_word in CLOSE_APPLICATION:
            return Intent.CLOSE

        if first_word in SEARCH:
            return Intent.SEARCH

        from brain_v2.intents import ASK_KNOWLEDGE_KEYWORDS
        if any(keyword in text.lower() for keyword in ASK_KNOWLEDGE_KEYWORDS):
            return Intent.ASK_KNOWLEDGE

        return Intent.UNKNOWN
