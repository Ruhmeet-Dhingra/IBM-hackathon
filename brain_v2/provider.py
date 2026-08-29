"""
ROV Brain v2

LLM Provider Interface

Every AI provider used by the Brain must implement
this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Provider(ABC):
    """
    Base class for all Brain providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the provider.
        """

        raise NotImplementedError