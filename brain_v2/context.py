"""
ROV Brain v2

Conversation Context

Stores the current conversational context so the
Brain can understand follow-up commands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from brain_v2.models import Entity


@dataclass
class Context:
    """
    Stores the current conversational context.
    """

    last_intent: Optional[str] = None

    last_entity: Optional[Entity] = None

    last_command: Optional[str] = None

    metadata: dict = field(default_factory=dict)

    def clear(self) -> None:
        """
        Reset the conversation context.
        """

        self.last_intent = None
        self.last_entity = None
        self.last_command = None
        self.metadata.clear()