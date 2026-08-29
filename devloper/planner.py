"""
ROV Developer v1.0
planner.py

The Planner is responsible for converting a natural language
development request into a validated PlannerResult.

The planner NEVER generates code.

Pipeline

User Request
      │
      ▼
Prepare Request
      ▼
Build AI Prompt
      ▼
AI Provider
      ▼
Parse JSON
      ▼
Validate
      ▼
PlannerResult
"""

from __future__ import annotations

import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from devloper.models import (
    PlannerResult,
    PluginPermission,
    PluginType,
    Requirement,
)

logger = logging.getLogger(__name__)


# ============================================================
# Exceptions
# ============================================================


class PlannerError(Exception):
    """Base planner exception."""


class PlannerValidationError(PlannerError):
    """Raised when the AI response is invalid."""


class PlannerAIError(PlannerError):
    """Raised when the AI provider fails."""


# ============================================================
# AI Provider Interface
# ============================================================


class AIProvider(ABC):
    """
    Base interface for every AI backend.

    Planner should never know whether it is using

    - Gemini
    - OpenAI
    - Claude
    - Ollama
    - ROV AI

    All providers implement this interface.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate a response.

        Returns
        -------
        str
            JSON string.
        """


# ============================================================
# Planner Configuration
# ============================================================


@dataclass(slots=True)
class PlannerConfig:

    temperature: float = 0.2

    max_retries: int = 3

    timeout: int = 60

    max_request_length: int = 5000


# ============================================================
# Planner
# ============================================================


class Planner:
    """
    ROV Planning Engine.

    Converts a natural language request into
    PlannerResult.

    The planner performs NO code generation.
    """

    def __init__(

        self,

        provider: AIProvider,

        config: PlannerConfig | None = None,

    ):

        self.provider = provider

        self.config = config or PlannerConfig()

        logger.info("Planner initialized.")

    # --------------------------------------------------------

    def plan(

        self,

        request: str,

    ) -> PlannerResult:

        """
        Main planning pipeline.
        """

        start = time.perf_counter()

        request = self._prepare_request(request)

        prompt = self._build_prompt(request)

        raw_response = self._request_ai(prompt)

        data = self._parse_json(raw_response)

        self._validate_response(data)

        result = self._build_result(
            request,
            data,
        )

        logger.info(

            "Planning completed in %.2f seconds.",

            time.perf_counter() - start,

        )

        return result
        # =========================================================
    # Request Preparation
    # =========================================================

    def _prepare_request(self, request: str) -> str:
        """
        Normalize and validate the incoming request.
        """

        if not isinstance(request, str):
            raise TypeError("Request must be a string.")

        request = request.strip()

        if not request:
            raise PlannerValidationError(
                "Request cannot be empty."
            )

        if len(request) > self.config.max_request_length:
            raise PlannerValidationError(
                "Request exceeds maximum allowed length."
            )

        request = " ".join(request.split())

        return request

    # =========================================================
    # Prompt Builder
    # =========================================================

    def _build_prompt(self, request: str) -> str:
        """
        Build the planning prompt.

        The model MUST return JSON only.
        """

        schema = """
{
    "plugin_name": "...",
    "plugin_type": "...",
    "description": "...",
    "commands": [],
    "permissions": [],
    "requirements": [
        {
            "description": "...",
            "required": true
        }
    ],
    "assumptions": [],
    "notes": [],
    "confidence": 0.95
}
"""

        return f"""
You are the ROV Developer Planner.

Your ONLY responsibility is planning.

Never generate Python code.

Never explain.

Return ONLY valid JSON.

Determine:

- plugin name
- plugin type
- description
- commands
- permissions
- requirements
- assumptions
- notes
- confidence

Request:

{request}

Output JSON exactly matching this schema:

{schema}
"""

    # =========================================================
    # AI Request
    # =========================================================

    def _request_ai(self, prompt: str) -> str:
        """
        Call the configured AI provider with retries.
        """

        last_exception = None

        for attempt in range(
            1,
            self.config.max_retries + 1,
        ):

            try:

                logger.info(
                    "Planner AI attempt %d/%d",
                    attempt,
                    self.config.max_retries,
                )

                response = self.provider.generate(
                    prompt=prompt,
                    temperature=self.config.temperature,
                )

                if not response.strip():
                    raise PlannerAIError(
                        "AI returned an empty response."
                    )

                return response

            except Exception as exc:

                last_exception = exc

                logger.exception(
                    "Planner AI attempt failed."
                )

        raise PlannerAIError(
            f"Planning failed after "
            f"{self.config.max_retries} attempts."
        ) from last_exception

    # =========================================================
    # JSON Parsing
    # =========================================================

    def _parse_json(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse the AI JSON response.
        """

        try:

            return json.loads(response)

        except json.JSONDecodeError as exc:

            logger.exception(
                "Planner returned invalid JSON."
            )

            raise PlannerValidationError(
                "AI returned invalid JSON."
            ) from exc
        # =========================================================
    # Response Validation
    # =========================================================

    REQUIRED_FIELDS = (
        "plugin_name",
        "plugin_type",
        "description",
        "commands",
        "permissions",
        "requirements",
        "assumptions",
        "notes",
        "confidence",
    )

    def _validate_response(
        self,
        data: dict[str, Any],
    ) -> None:
        """
        Validate the JSON returned by the AI provider.
        """

        missing = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in data
        ]

        if missing:
            raise PlannerValidationError(
                "Missing required fields: "
                + ", ".join(missing)
            )

        if not isinstance(data["commands"], list):
            raise PlannerValidationError(
                "'commands' must be a list."
            )

        if not isinstance(data["permissions"], list):
            raise PlannerValidationError(
                "'permissions' must be a list."
            )

        if not isinstance(data["requirements"], list):
            raise PlannerValidationError(
                "'requirements' must be a list."
            )

        if not isinstance(data["assumptions"], list):
            raise PlannerValidationError(
                "'assumptions' must be a list."
            )

        if not isinstance(data["notes"], list):
            raise PlannerValidationError(
                "'notes' must be a list."
            )

        if not isinstance(
            data["confidence"],
            (int, float),
        ):
            raise PlannerValidationError(
                "'confidence' must be numeric."
            )

        confidence = float(data["confidence"])

        if not 0 <= confidence <= 1:
            raise PlannerValidationError(
                "Confidence must be between 0 and 1."
            )

    # =========================================================
    # Enum Conversion
    # =========================================================

    def _plugin_type(
        self,
        value: str,
    ) -> PluginType:

        value = value.lower().strip()

        try:
            return PluginType(value)

        except ValueError:

            logger.warning(
                "Unknown plugin type '%s'. "
                "Using OTHER.",
                value,
            )

            return PluginType.OTHER

    def _permissions(
        self,
        values: list[str],
    ) -> list[PluginPermission]:

        permissions: list[PluginPermission] = []

        for permission in values:

            try:

                permissions.append(
                    PluginPermission(
                        permission.lower()
                    )
                )

            except ValueError:

                logger.warning(
                    "Ignoring unknown permission '%s'",
                    permission,
                )

        return permissions

    def _requirements(
        self,
        values: list[dict[str, Any]],
    ) -> list[Requirement]:

        requirements: list[Requirement] = []

        for item in values:

            requirements.append(

                Requirement(

                    description=item["description"],

                    required=item.get(
                        "required",
                        True,
                    ),
                )

            )

        return requirements

    # =========================================================
    # Result Builder
    # =========================================================

    def _build_result(
        self,
        request: str,
        data: dict[str, Any],
    ) -> PlannerResult:
        """
        Convert validated JSON into PlannerResult.
        """

        return PlannerResult(

            user_request=request,

            plugin_name=data["plugin_name"],

            description=data["description"],

            plugin_type=self._plugin_type(
                data["plugin_type"]
            ),

            commands=[
                command.strip()
                for command in data["commands"]
                if command.strip()
            ],

            permissions=self._permissions(
                data["permissions"]
            ),

            requirements=self._requirements(
                data["requirements"]
            ),

            assumptions=data["assumptions"],

            notes=data["notes"],

            confidence=float(
                data["confidence"]
            ),
        )