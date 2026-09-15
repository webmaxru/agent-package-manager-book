from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts" / "run-fleet.ps1"
PWSH = shutil.which("pwsh")


@unittest.skipUnless(PWSH, "PowerShell 7 is required for launcher tests.")
class LauncherTests(unittest.TestCase):
    def run_launcher(self, *args, env=None):
        return subprocess.run(
            [PWSH, "-NoProfile", "-File", str(LAUNCHER), *args], cwd=ROOT, env=env,
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )

    def test_default_prompt_exists_and_dry_run_succeeds(self):
        result = self.run_launcher("-DryRun")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("run-playbook.prompt.md", result.stdout)
        self.assertNotIn("run-book.prompt.md", result.stdout)

    def test_update_target_and_mode_resolve_without_launching(self):
        result = self.run_launcher("-UpdateBook", "-CheckOnly", "-ApmVersion", "v0.31.0", "-DryRun")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("update-book.prompt.md", result.stdout)
        self.assertIn("Mode: check; target APM: 0.31.0; publication: disabled", result.stdout)

    def test_update_defaults_to_prepare(self):
        result = self.run_launcher("-UpdateBook", "-DryRun")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Mode: prepare", result.stdout)

    def test_missing_prompt_and_incompatible_parameters_fail(self):
        for args in [
            ("-PromptPath", ".github\\prompts\\does-not-exist.prompt.md", "-DryRun"),
            ("-UpdateBook", "-PromptPath", str(LAUNCHER), "-DryRun"),
            ("-UpdateBook", "-ApmVersion", "latest", "-DryRun"),
            ("-UpdateBook", "-ApmVersion", "0.31.0-rc.1", "-DryRun"),
        ]:
            with self.subTest(args=args):
                self.assertNotEqual(self.run_launcher(*args).returncode, 0)

    def test_invocation_inputs_and_failure_exit_code_reach_caller(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            fake = scratch / "copilot.ps1"
            fake.write_text(
                "param([string]$p)\n"
                "[System.IO.File]::WriteAllText($env:BOOK_TEST_CAPTURE, $p)\n"
                "exit 23\n", encoding="utf-8",
            )
            fake.chmod(0o755)
            capture = scratch / "prompt.txt"
            env = dict(os.environ, PATH=str(scratch), BOOK_TEST_CAPTURE=str(capture))
            result = self.run_launcher("-UpdateBook", "-CheckOnly", "-ApmVersion", "0.31.0", env=env)
            self.assertEqual(result.returncode, 23, result.stderr)
            prompt = capture.read_text(encoding="utf-8")
            self.assertIn("Mode: check\nTarget APM: 0.31.0", prompt)
            self.assertIn("Never push, tag, merge, or publish in this run.", prompt)


class WorkflowContractTests(unittest.TestCase):
    def workflow(self, filename):
        with (ROOT / ".github" / "workflows" / filename).open(encoding="utf-8") as handle:
            return yaml.load(handle, Loader=yaml.BaseLoader)

    def test_release_uses_exact_tag_and_preflight_before_build(self):
        workflow = self.workflow("release-content.yml")
        steps = workflow["jobs"]["release"]["steps"]
        checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout"))
        self.assertEqual(checkout["with"]["fetch-depth"], "0")
        self.assertEqual(checkout["with"]["ref"], "refs/tags/${{ steps.meta.outputs.tag }}")
        preflight = next(i for i, step in enumerate(steps)
                         if "validate_release.py --tag" in step.get("run", ""))
        build = next(i for i, step in enumerate(steps)
                     if step.get("run") == "python site/generate.py")
        self.assertLess(preflight, build)
        self.assertEqual(steps[build]["env"]["APM_PDF_REQUIRED"], "1")
        self.assertNotIn("::warning::", str(steps))
        self.assertTrue(steps[0]["env"]["RELEASE_TAG"])
        self.assertNotIn("${{", steps[0]["run"])

    def test_pr_workflow_is_read_only_and_covers_both_platforms(self):
        workflow = self.workflow("check-book.yml")
        self.assertIn("pull_request", workflow["on"])
        self.assertNotIn("pull_request_target", workflow["on"])
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        job = workflow["jobs"]["preflight"]
        self.assertEqual(job["strategy"]["matrix"]["os"], ["ubuntu-latest", "windows-latest"])
        self.assertIn("unittest discover", str(job["steps"]))
        self.assertIn("validate_release.py --base-ref", str(job["steps"]))
        self.assertIn("APM_PDF_REQUIRED", str(job["steps"]))

    def test_pages_runs_preflight_before_build_and_remains_main_only(self):
        workflow = self.workflow("deploy-pages.yml")
        self.assertEqual(workflow["on"]["push"]["branches"], ["main"])
        steps = workflow["jobs"]["build"]["steps"]
        preflight = next(i for i, step in enumerate(steps)
                         if "validate_release.py" in step.get("run", ""))
        build = next(i for i, step in enumerate(steps)
                     if step.get("run") == "python site/generate.py")
        self.assertLess(preflight, build)
        self.assertEqual(steps[build]["env"]["APM_PDF_REQUIRED"], "1")


if __name__ == "__main__":
    unittest.main()
