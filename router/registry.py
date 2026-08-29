"""
ROV Skill Registry

Maps Brain actions to their corresponding skills.
"""

from __future__ import annotations

from brain_v2.entities import Action

from skills.application.skill import ApplicationSkill
from skills.browser.skill import BrowserSkill
from skills.plugin.skill import PluginSkill
from skills.knowledge.skill import KnowledgeSkill
from skills.project.skill import ProjectSkill
from skills.reasoning.skill import ReasoningSkill
from skills.ui.skill import UISkill

class SkillRegistry:
    """
    Registry of all available skills.
    """

    def __init__(self) -> None:

        application = ApplicationSkill()
        browser = BrowserSkill()
        plugin = PluginSkill()
        knowledge = KnowledgeSkill()
        project = ProjectSkill()
        reasoning = ReasoningSkill()
        ui = UISkill()
        self._skills = {

            # =========================
            # Application
            # =========================

            Action.LAUNCH_APPLICATION: application,
            Action.CLOSE_APPLICATION: application,

            # =========================
            # Browser
            # =========================

            Action.OPEN_URL: browser,
            Action.OPEN_WEBSITE: browser,
            Action.SEARCH_WEB: browser,

            # =========================
            # Plugins
            # =========================

            Action.GENERATE_PLUGIN: plugin,
            Action.PROPOSE_PLUGIN: plugin,
            Action.PREVIEW_PLUGIN: plugin,
            Action.APPROVE_PLUGIN: plugin,
            Action.REJECT_PLUGIN: plugin,
            Action.RUN_PLUGIN: plugin,

            # =========================
            # Knowledge (RAG)
            # =========================

            Action.SEARCH_KNOWLEDGE_BASE: knowledge,

            # =========================
            # Project
            # =========================

            Action.LOCATE_PROJECT: project,
            Action.OPEN_PROJECT: project,

            # =========================
            # Reasoning
            # =========================

            Action.NEEDS_REASONING: reasoning,

            # =========================
            # UI
            # =========================

            Action.SHOW_COMPONENT: ui,
            Action.HIDE_COMPONENT: ui,

        }

    def get(self, action: Action):
        """
        Return the skill responsible for an action.
        """
        return self._skills.get(action)

    def register(self, action: Action, skill) -> None:
        """
        Register a new action at runtime.
        """
        self._skills[action] = skill

    def unregister(self, action: Action) -> None:
        """
        Remove an action from the registry.
        """
        self._skills.pop(action, None)
