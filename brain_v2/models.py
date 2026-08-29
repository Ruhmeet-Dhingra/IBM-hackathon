from dataclasses import dataclass, field
from typing import Any

from brain_v2.entities import Action, EntityType


@dataclass
class Entity:
    type: EntityType
    name: str
    value: str | None = None


@dataclass
class Step:
    action: Action
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class Plan:
    """A sequence of typed actions required to fulfil a command."""

    steps: list[Step] = field(default_factory=list)
