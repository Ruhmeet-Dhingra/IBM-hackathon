"""
ROV Brain v2

Working Memory

Stores information the Brain may need across
multiple commands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from brain_v2.models import Entity


@dataclass
class Memory:
    """
    Working memory for the Brain.
    """

    last_entity: Optional[Entity] = None

    last_intent: Optional[str] = None

    last_plan = None

    history: list[str] = field(default_factory=list)

    def remember(
        self,
        command: str,
    ) -> None:
        """
        Store a command in history.
        """

        self.history.append(command)

    def clear(self) -> None:
        """
        Clear the Brain's memory.
        """

        self.last_entity = None

        self.last_intent = None

        self.last_plan = None

        self.history.clear()