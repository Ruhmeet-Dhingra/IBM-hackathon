from abc import ABC, abstractmethod


class Skill(ABC):
    """
    Base class for every ROV skill.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, action: str, **kwargs):
        pass