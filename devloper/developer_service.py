"""
ROV Developer Service

Provides a simple interface between ROV and the
Developer pipeline.
"""

from pathlib import Path

from devloper.architect import Architect
from devloper.devloper_manager import (
    DeveloperManager,
    DeveloperManagerConfig,
)
from devloper.generator import Generator
from devloper.installer import Installer
from devloper.mock_provider import MockProvider
from devloper.planner import Planner
from devloper.preview import PreviewBuilder
from devloper.project_analyzer import ProjectAnalyzer
from devloper.reviewer import Reviewer
from devloper.template_engine import TemplateEngine
from devloper.validator import Validator


class DeveloperService:

    def __init__(self):

        self.analyzer = ProjectAnalyzer()

        self.manager = DeveloperManager(

            planner=Planner(
                provider=MockProvider(),
            ),

            architect=Architect(),

            generator=Generator(),

            template_engine=TemplateEngine(),

            validator=Validator(),

            reviewer=Reviewer(),

            preview=PreviewBuilder(),

            installer=Installer(),

            config=DeveloperManagerConfig(
                auto_install=False,
            ),
        )

    def build_plugin(self, request: str):

        analysis = self.analyzer.analyze(
            Path(".")
        )

        result = self.manager.build(
            request=request,
            analysis=analysis,
            destination=Path("generated_plugins"),
        )

        return result


developer_service = DeveloperService()
def build_plugin(self, request: str):
    try:
        analysis = self.analyzer.analyze(Path("."))

        return self.manager.build(
            request=request,
            analysis=analysis,
            destination=Path("generated_plugins"),
        )

    except Exception as e:
        print(f"DeveloperService error: {e}")
        raise