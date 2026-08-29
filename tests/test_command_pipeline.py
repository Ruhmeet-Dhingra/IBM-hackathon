import unittest
from unittest.mock import patch

from brain_v2.brain import Brain
from brain_v2.entities import Action
from core_v2.app import launch_application
from core_v2.core_types import OperationResult
from router.router import Router


class RecordingSkill:
    def __init__(self) -> None:
        self.steps = []

    def execute(self, step):
        self.steps.append(step)
        return "handled"


class CommandPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.brain = Brain()

    def test_open_application_creates_a_launch_step(self) -> None:
        plan = self.brain.process("Please launch Chrome for me")

        self.assertEqual(len(plan.steps), 1)
        self.assertEqual(plan.steps[0].action, Action.LAUNCH_APPLICATION)
        self.assertEqual(plan.steps[0].parameters["application"], "chrome")

    def test_search_creates_a_browser_step(self) -> None:
        plan = self.brain.process("Search quantum computing")

        self.assertEqual(len(plan.steps), 1)
        self.assertEqual(plan.steps[0].action, Action.SEARCH_WEB)
        self.assertEqual(plan.steps[0].parameters["query"], "quantum computing")

    def test_router_dispatches_without_performing_a_system_action(self) -> None:
        plan = self.brain.process("Open Chrome")
        router = Router()
        skill = RecordingSkill()
        router.registry.register(Action.LAUNCH_APPLICATION, skill)

        result = router.execute(plan)

        self.assertEqual(result, ["handled"])
        self.assertEqual(skill.steps, plan.steps)

    @patch("core_v2.app.subprocess.Popen")
    @patch("core_v2.app.find_windows_application")
    @patch("core_v2.app.find_application")
    def test_registered_windows_app_is_launched_by_app_id(
        self,
        find_indexed_application,
        find_windows_application,
        popen,
    ) -> None:
        find_indexed_application.return_value = OperationResult(
            success=False,
            message="calculator not found.",
        )
        find_windows_application.return_value = OperationResult(
            success=True,
            message="Registered Windows app found.",
            data={
                "name": "Calculator",
                "app_id": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            },
        )

        result = launch_application("calculator")

        self.assertTrue(result.success)
        popen.assert_called_once_with([
            "explorer.exe",
            "shell:AppsFolder\\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
        ])

    @patch("core_v2.app.os.startfile")
    @patch("core_v2.app.find_windows_application")
    @patch("core_v2.app.find_application")
    def test_unknown_app_searches_google_in_chrome(
        self,
        find_indexed_application,
        find_windows_application,
        startfile,
    ) -> None:
        missing = OperationResult(success=False, message="not found")
        chrome = OperationResult(
            success=True,
            message="Application found.",
            data={"name": "Google Chrome", "shortcut": "C:\\Chrome.lnk"},
        )
        find_indexed_application.side_effect = [missing, chrome]
        find_windows_application.return_value = missing

        result = launch_application("imaginary app")

        self.assertTrue(result.success)
        self.assertIn("Searching Google in Chrome", result.message)
        self.assertEqual(startfile.call_args.args[0], "C:\\Chrome.lnk")
        self.assertIn("imaginary+app", startfile.call_args.kwargs["arguments"])


if __name__ == "__main__":
    unittest.main()
