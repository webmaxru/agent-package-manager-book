from __future__ import annotations

import os
import re
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

    def test_release_build_is_read_only_and_publish_rechecks_provenance(self):
        workflow = self.workflow("release.yml")
        self.assertEqual(workflow["permissions"], {})
        self.assertNotIn("push", workflow["on"])
        self.assertEqual(workflow["jobs"]["build"]["permissions"], {"contents": "read"})
        steps = workflow["jobs"]["build"]["steps"]
        self.assertIn("validate_evidence.py", str(steps))
        self.assertIn("python site/generate_pdf.py", str(steps))
        self.assertIn("needs.authorize.outputs.sha", str(steps))
        publish = workflow["jobs"]["publish"]
        self.assertEqual(publish["needs"], ["authorize", "build"])
        self.assertIn("release-plan", str(publish["steps"]))
        self.assertIn("scripts/book_release.py publish", str(publish["steps"]))
        self.assertIn("gh workflow run deploy-pages.yml", str(publish["steps"]))
        dispatch = publish["steps"][-1]
        self.assertIn('-f ref="$TAG"', dispatch["run"])
        self.assertEqual(dispatch["env"]["TAG"], "${{ needs.build.outputs.tag }}")

    def test_pr_workflow_is_read_only_and_covers_both_platforms(self):
        workflow = self.workflow("ci.yml")
        self.assertIn("pull_request", workflow["on"])
        self.assertEqual(workflow["on"]["push"]["branches"], ["main"])
        self.assertNotIn("pull_request_target", workflow["on"])
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        job = workflow["jobs"]["preflight"]
        self.assertEqual(job["strategy"]["matrix"]["os"], ["ubuntu-24.04", "windows-2025"])
        self.assertIn("unittest discover", str(job["steps"]))
        self.assertIn("validate_release.py --root . --base-ref", str(job["steps"]))
        self.assertIn("validate_evidence.py", str(job["steps"]))
        self.assertIn("trusted/site/release_candidate.py --root .", str(job["steps"]))
        self.assertIn("site/generate_pdf.py", str(job["steps"]))
        self.assertEqual(workflow["jobs"]["book-release-preflight"]["name"], "Book release preflight")
        self.assertNotIn("APM_PDF_REQUIRED", str(job["steps"]))

    def test_approval_signal_is_unprivileged_and_controller_uses_trusted_ref(self):
        signal = self.workflow("book-approval-signal.yml")
        self.assertEqual(signal["permissions"], {})
        self.assertNotIn("checkout", str(signal["jobs"]))
        controller = self.workflow("approved-book.yml")
        self.assertEqual(controller["permissions"], {})
        self.assertEqual(controller["concurrency"],
                         {"group": "approved-book", "cancel-in-progress": "false"})
        self.assertIn("workflow_run", controller["on"])
        self.assertIn("issue_comment", controller["on"])
        self.assertIn("schedule", controller["on"])
        self.assertEqual(controller["jobs"]["preflight"]["permissions"], {"contents": "read"})
        self.assertIn("ref': 'main", str(controller["jobs"]["authorize"]["steps"]))

    def test_pages_runs_preflight_before_build_and_remains_main_only(self):
        workflow = self.workflow("deploy-pages.yml")
        self.assertEqual(workflow["on"]["push"]["branches"], ["main"])
        steps = workflow["jobs"]["build"]["steps"]
        preflight = next(i for i, step in enumerate(steps)
                         if "validate_release.py" in step.get("run", ""))
        build = next(i for i, step in enumerate(steps)
                     if step.get("run") == "python site/generate.py")
        self.assertLess(preflight, build)
        self.assertNotIn("APM_PDF_REQUIRED", str(steps))

    def test_all_workflows_parse_and_workflow_run_names_exist(self):
        workflows = [self.workflow(path.name) for path in (ROOT / ".github" / "workflows").glob("*.yml")]
        names = {workflow["name"] for workflow in workflows}
        for workflow in workflows:
            for name in workflow["on"].get("workflow_run", {}).get("workflows", []):
                self.assertIn(name, names)

    def test_documented_dispatch_commands_match_real_workflow_inputs(self):
        docs = (ROOT / "RELEASING.md").read_text(encoding="utf-8")
        commands = re.findall(r"gh workflow run ([\w-]+\.yml)([^\n`]*)", docs)
        self.assertTrue(commands)
        for filename, arguments in commands:
            dispatch = self.workflow(filename)["on"]["workflow_dispatch"]
            supplied = set(re.findall(r"-f (\w+)=", arguments))
            declared = dispatch.get("inputs", {})
            self.assertTrue(supplied.issubset(declared), (filename, supplied))
            for name, field in declared.items():
                if field.get("required") == "true":
                    self.assertIn(name, supplied, (filename, arguments))

    def test_privileged_jobs_are_main_only_and_run_trusted_controllers(self):
        for name in ("approved-book.yml", "release.yml", "deploy-pages.yml"):
            workflow = self.workflow(name)
            for job in workflow["jobs"].values():
                self.assertIn("github.ref == 'refs/heads/main'", job["if"])
                checkouts = [step for step in job["steps"] if step.get("uses", "").startswith("actions/checkout@")]
                self.assertTrue(checkouts)
                for step in checkouts:
                    self.assertEqual(step["with"]["persist-credentials"], "false")
                    if step["with"].get("path") != "book":
                        self.assertEqual(step["with"]["ref"], "main")
                for step in job["steps"]:
                    if any(script in step.get("run", "") for script in
                           ("validate_release.py", "validate_evidence.py", "release_candidate.py")):
                        self.assertIn("trusted/site/", step["run"])

    def test_published_source_gates_build_and_deploy_without_yaml_path_lists(self):
        workflow = self.workflow("deploy-pages.yml")
        self.assertEqual(workflow["permissions"], {})
        self.assertEqual(workflow["on"]["workflow_dispatch"]["inputs"]["ref"]["required"], "true")
        gate = workflow["jobs"]["published-source"]
        self.assertEqual(gate["permissions"], {"contents": "read"})
        self.assertIn("book_release.py deploy-plan --sha", str(gate["steps"]))
        self.assertIn("book_release.py deploy-plan --ref", str(gate["steps"]))
        self.assertNotIn("paths", workflow["on"]["push"])
        self.assertNotIn("content/chapters", str(gate))
        for name in ("build", "deploy"):
            job = workflow["jobs"][name]
            self.assertIn("published-source", job["needs"])
            self.assertIn("needs.published-source.outputs.eligible == 'true'", job["if"])
        checkouts = [step for step in workflow["jobs"]["build"]["steps"]
                     if step.get("with", {}).get("path") == "book"]
        self.assertEqual(checkouts[0]["with"]["ref"], "${{ needs.published-source.outputs.sha }}")
        smoke = workflow["jobs"]["deploy"]["steps"][-1]
        self.assertIn("check_site.py", smoke["run"])
        self.assertEqual(smoke["env"]["TAG"], "${{ needs.published-source.outputs.tag }}")


if __name__ == "__main__":
    unittest.main()
