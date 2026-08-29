"""
Extracts entities from normalized commands.
"""

from brain_v2.entities import EntityType
from brain_v2.intents import Intent
from brain_v2.models import Entity


class EntityExtractor:

    def extract(self, text: str) -> list[Entity]:

        words = text.split()

        if len(words) <= 1:
            return []

        if len(words) >= 2 and words[1] in {"plugin", "proposal"}:
            entity = " ".join(words[2:]) or "latest"
            return [
                Entity(
                    type=EntityType.PLUGIN,
                    name=entity,
                    value=entity,
                )
            ]

        if (
            len(words) >= 3
            and words[0] in {"add", "build", "create", "make", "teach"}
            and words[1] in {"feature", "plugin"}
        ):
            entity = " ".join(words[2:])
            return [
                Entity(
                    type=EntityType.PLUGIN,
                    name=entity,
                    value=entity,
                )
            ]

        entity = " ".join(words[1:])
        from brain_v2.intents import ASK_KNOWLEDGE_KEYWORDS
        
        is_rag_query = any(k in text.lower() for k in ASK_KNOWLEDGE_KEYWORDS)
        if is_rag_query:
            # We want the whole text or everything after the keyword
            entity_type = EntityType.QUERY
            entity = text
        else:
            entity_type = (
                EntityType.QUERY
                if words[0] == Intent.SEARCH.value.lower()
                else EntityType.APPLICATION
            )

        return [
            Entity(
                type=entity_type,
                name=entity,
                value=entity,
            )
        ]
if __name__ == "__main__":

    extractor = EntityExtractor()

    tests = [
        "open chrome",
        "open google chrome",
        "search quantum computing",
        "close visual studio code",
    ]

    for test in tests:

        print(test)

        print(extractor.extract(test))

        print()
