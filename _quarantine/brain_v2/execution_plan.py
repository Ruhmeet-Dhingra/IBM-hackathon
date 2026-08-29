"""
Execution plan produced by the Brain.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionPlan:
    intent: str
    entities: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0