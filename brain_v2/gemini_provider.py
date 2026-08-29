"""
Gemini Provider
"""

from __future__ import annotations

import os

import google.generativeai as genai  # type: ignore[import]
from dotenv import load_dotenv

from brain_v2.provider import Provider


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiProvider(Provider):
    """
    Google Gemini implementation.
    """

    def __init__(self) -> None:

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.model.generate_content(
            prompt
        )

        return response.text