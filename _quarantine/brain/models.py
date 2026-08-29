from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .entities import EntityType


@dataclass
class BrainResult:
    """
    Final output produced by the Brain.
    """
    intent: str
    entities: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    response: str = ""
    plan: List[str] = field(default_factory=list)


@dataclass
class Plan:
    """
    Represents a sequence of actions required to satisfy an intent.
    """

    steps: List["Step"] = field(default_factory=list)


@dataclass
class Entity:
    type: EntityType
    name: str
    value: Optional[str] = None
    