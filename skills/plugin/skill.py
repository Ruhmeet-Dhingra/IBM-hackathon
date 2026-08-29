"""Routes plugin proposal commands without auto-installing generated code."""

from __future__ import annotations

from brain_v2.entities import Action
from brain_v2.models import Step
from plugins.gemini_generator import GeminiPluginGenerator
from plugins.proposals import PluginProposalService
from plugins.runtime import PluginRuntime


class PluginSkill:
    """Generate, review, and run plugins through an explicit approval gate."""

    def __init__(self) -> None:
        self._proposal_service: PluginProposalService | None = None
        self.runtime = PluginRuntime()

    def execute(self, step: Step):
        if step.action == Action.GENERATE_PLUGIN:
            # GENERATE_PLUGIN is the planner's high-level "build me a plugin" intent;
            # route it into the gated proposal flow with the raw request string.
            request = step.parameters.get("request", "")
            return self._get_proposal_service().propose(request)

        if step.action == Action.PROPOSE_PLUGIN:
            return self._get_proposal_service().propose(step.parameters["request"])

        if step.action == Action.PREVIEW_PLUGIN:
            return self._get_proposal_service().preview(step.parameters["proposal_id"])

        if step.action == Action.APPROVE_PLUGIN:
            return self._get_proposal_service().approve(step.parameters["proposal_id"])

        if step.action == Action.REJECT_PLUGIN:
            return self._get_proposal_service().reject(step.parameters["proposal_id"])

        if step.action == Action.RUN_PLUGIN:
            return self.runtime.run(
                step.parameters["plugin_id"],
                step.parameters["command"],
            )

        raise ValueError(f"Unsupported action: {step.action}")

    def _get_proposal_service(self) -> PluginProposalService:
        if self._proposal_service is None:
            self._proposal_service = PluginProposalService(GeminiPluginGenerator())
        return self._proposal_service
