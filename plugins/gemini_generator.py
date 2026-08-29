"""Gemini-backed generator for safe staged plugin proposals."""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from plugins.proposals import PluginCodeGenerator, PluginDraft, PluginProposalError


load_dotenv()


class GeminiPluginGenerator(PluginCodeGenerator):
    """Ask Gemini for one JSON plugin draft without installing or running it."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise PluginProposalError("GEMINI_API_KEY is missing from .env")

        self.client = genai.Client(api_key=api_key)
        self.model = (
            os.getenv("GEMINI_PLUGIN_MODEL")
            or os.getenv("GEMINI_MODEL")
            or "gemini-2.5-flash"
        )

    def generate(self, request: str) -> PluginDraft:
        prompt = f"""
Create one safe ROV plugin proposal for this request: {request!r}

Return JSON only with this exact shape:
{{
  "name": "lowercase_plugin_name",
  "description": "one sentence",
  "commands": ["a short command phrase"],
  "permissions": [],
  "plugin_code": "complete Python source"
}}

Rules for plugin_code:
- Define one Plugin subclass with a run(self, command: str) method.
- Import only Python standard-library modules and `from plugins.plugin import Plugin`.
- Do not use network access, shell commands, filesystem writes, dynamic imports, eval, exec, input, or open.
- Return a dictionary containing a short `message` string from run.
- Do not perform any action at import time.
""".strip()
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        raw_response = (response.text or "").strip()

        try:
            data = json.loads(raw_response)
            return PluginDraft(
                name=data["name"],
                description=data["description"],
                commands=data["commands"],
                permissions=data.get("permissions", []),
                plugin_code=data["plugin_code"],
            )
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            raise PluginProposalError("Gemini did not return a valid plugin draft") from error
