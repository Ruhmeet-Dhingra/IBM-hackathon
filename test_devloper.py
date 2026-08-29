

from pathlib import Path
import sys

from devloper.mock_provider import MockProvider
from devloper.project_analyzer import ProjectAnalyzer
from devloper.planner import Planner
from devloper.architect import Architect
from devloper.generator import Generator
from devloper.template_engine import TemplateEngine
from devloper.validator import Validator
from devloper.reviewer import Reviewer
from devloper.preview import PreviewBuilder
from devloper.installer import Installer
from devloper.devloper_manager import (
    DeveloperManager,
    DeveloperManagerConfig,
)


def main():

    # ---------------------------------------------------------
    # Analyze project
    # ---------------------------------------------------------

    analyzer = ProjectAnalyzer()

    analysis = analyzer.analyze(
        Path(".")
    )

    print(
        f"Project: {analysis.project.project_name}"
    )

    print(
        f"Python files: {analysis.total_python_files()}"
    )

    # ---------------------------------------------------------
    # Create pipeline
    # ---------------------------------------------------------

    manager = DeveloperManager(

        planner = Planner(
    provider=MockProvider()
),

        architect=Architect(),

        generator=Generator(),

        template_engine=TemplateEngine(),

        validator=Validator(),

        reviewer=Reviewer(),

        preview=PreviewBuilder(),

        installer=Installer(),

        config=DeveloperManagerConfig(
            auto_install=False
        ),
    
    )
        # ---------------------------------------------------------
    # Generate Plugin
    # ---------------------------------------------------------

    result = manager.build(
        request="Create a Hello World plugin",
        analysis=analysis,
        destination=Path("generated_plugins"),
    )

    # ---------------------------------------------------------
    # Display Results
    # ---------------------------------------------------------

    print()

    print("=" * 60)
    print("ROV Developer Pipeline")
    print("=" * 60)

    print(
        f"Stage: {result.stage.value}"
    )

    print(
        f"Successful: {result.successful}"
    )

    print(
        f"Duration: {result.duration}"
    )

    if result.planner:

        print()
        print("Planner")

        print(
            f"Plugin Name: {result.planner.plugin_name}"
        )

        print(
            f"Type: {result.planner.plugin_type.value}"
        )

    if result.validation:

        print()
        print("Validation")

        print(
            f"Valid: {result.validation.valid}"
        )

        print(
            f"Issues: {len(result.validation.issues)}"
        )

    if result.review:

        print()
        print("Review")

        print(
            f"Approved: {result.review.approved}"
        )

        print(
            f"Score: {result.review.score}"
        )

    if result.preview:

        print()
        print("Preview")

        print(
            f"Files: {result.preview.total_files()}"
        )

        print(
            f"Safe: {result.preview.safe_to_install}"
        )

    if result.installation:

        print()
        print("Installation")

        print(
            f"Installed: {result.installation.success}"
        )


if __name__ == "__main__":
    main()
