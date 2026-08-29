from typing import List

from .entities import EntityType
from .models import Entity


class EntityExtractor:
    """
    Extracts entities from a user's sentence.
    """

    def __init__(self):

        self.applications = [
            "chrome",
            "fusion 360",
            "visual studio code",
            "vs code",
            "notepad",
            "calculator",
            "spotify",
            "discord"
        ]

        self.websites = [
            "youtube",
            "google",
            "github",
            "chatgpt",
            "gmail"
        ]

        self.components = [
            "housing",
            "shaft",
            "gear",
            "bearing",
            "bolt",
            "nut",
            "washer",
            "casing"
        ]

    def extract(self, text: str) -> List[Entity]:

        text = text.lower()

        entities = []

        # Applications
        for app in self.applications:
            if app in text:
                entities.append(
                    Entity(
                        type=EntityType.APPLICATION,
                        name=app.title()
                    )
                )

        # Websites
        for website in self.websites:
            if website in text:
                entities.append(
                    Entity(
                        type=EntityType.WEBSITE,
                        name=website.title()
                    )
                )

        # Components
        for component in self.components:
            if component in text:
                entities.append(
                    Entity(
                        type=EntityType.COMPONENT,
                        name=component
                    )
                )

        return entities