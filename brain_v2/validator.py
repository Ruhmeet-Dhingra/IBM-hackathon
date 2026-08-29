"""
ROV Brain v2

Execution Plan Validator

Responsible for validating plans before they
are sent to the Router.
"""

from __future__ import annotations

from dataclasses import dataclass

from brain_v2.models import Plan


@dataclass
class ValidationResult:
    """
    Result of validating an execution plan.
    """

    valid: bool

    message: str = ""


class Validator:
    """
    Validates execution plans.
    """

    def validate(
        self,
        plan: Plan,
    ) -> ValidationResult:
        """
        Validate an execution plan.

        Future versions may check:

        - Empty plans
        - Unsupported actions
        - Missing parameters
        - Permission requirements
        - Safety rules
        """

        if not plan.steps:

            return ValidationResult(
                valid=False,
                message="Execution plan contains no steps.",
            )

        return ValidationResult(
            valid=True,
        )