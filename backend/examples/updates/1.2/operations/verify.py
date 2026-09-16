"""Re-run the operations fixtures with exactly APM 0.31.0, never a PATH-selected APM.

Python 3.10+ and PyYAML 6 are required. All mutations happen in a new, short,
owned scratch directory. No global install/config command, policy publication,
real MCP process, agent runtime, or external package download is performed.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

sys.dont_write_bytecode = True
from registry_fixture import RegistryFixture

FIXTURES = Path(__file__).resolve().parent


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def save_yaml(path, value):
    write(path, yaml.safe_dump(value, sort_keys=False))


def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def inventory(root):
    result = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if ".git" in rel.parts or not path.is_file():
            continue
        try:
            result[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        except PermissionError:
            result[rel.as_posix()] = "PermissionError"
    return result


class Probe:
    def __init__(self, apm, work):
        self.apm = Path(apm)
        if not self.apm.is_absolute() or not self.apm.is_file():
            raise ValueError("--apm must be the prepared executable's absolute path")
        self.work = Path(work) if work else Path(tempfile.mkdtemp(prefix="apo-"))
        if not self.work.is_absolute():
            raise ValueError("--work must be absolute")
        if work:
            self.work.mkdir(parents=True, exist_ok=False)
        self.env = self.environment()
        self.results, self.n = [], 0
        write(self.work / ".operations-fixture", "APM 0.31.0 operations fixture; safe to preserve as evidence.\n")
        banner = self.run(self.work, "version", ["--version"])
        if "CLI version 0.31.0" not in banner["stdout"]:
            raise RuntimeError("Wrong APM release; refusing to continue")

    def environment(self):
        env = {
            key: value for key, value in os.environ.items()
            if not re.search(r"TOKEN|SECRET|PASSWORD|CREDENTIAL|AUTHTOKEN|API_KEY|^APM_|^GIT_|^GH_|^GITHUB_|^GITLAB_|^ADO_|^AZURE_|^MCP_|PROXY", key, re.I)
        }
        paths = []
        for part in env.get("PATH", "").split(os.pathsep):
            if part and any((Path(part) / ("gh" + ext)).is_file() for ext in [".exe", ".cmd", ".bat", ""]):
                continue
            paths.append(part)
        env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.pathsep.join(paths)
        home = self.work / "h"
        for path in [home, home / "local", home / "roaming", self.work / "tmp", self.work / "cache"]:
            path.mkdir(parents=True, exist_ok=True)
        env.update({
            "HOME": str(home), "USERPROFILE": str(home),
            "APPDATA": str(home / "roaming"), "LOCALAPPDATA": str(home / "local"),
            "XDG_CONFIG_HOME": str(home / ".config"), "XDG_CACHE_HOME": str(home / ".cache"),
            "APM_HOME": str(home / ".apm"), "APM_CACHE_DIR": str(self.work / "cache"),
            "GH_CONFIG_DIR": str(home / ".config/gh"),
            "ProgramData": str(home / "program-data"),  # No admin policy file is created.
            "TEMP": str(self.work / "tmp"), "TMP": str(self.work / "tmp"),
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(home / "no-gitconfig"),
            "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "credential.helper", "GIT_CONFIG_VALUE_0": "",
            "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never", "GIT_PAGER": "cat", "PAGER": "cat",
            "NO_COLOR": "1", "COLUMNS": "180", "APM_NON_INTERACTIVE": "1", "PYTHONIOENCODING": "utf-8",
            # Bound the CLI's synthetic MCP identity lookup; no server runs here.
            "MCP_REGISTRY_URL": "https://127.0.0.1:9",
            "MCP_REGISTRY_CONNECT_TIMEOUT": "2", "MCP_REGISTRY_READ_TIMEOUT": "2",
        })
        return env

    def project(self, fixture=None, clone=None):
        self.n += 1
        path = self.work / f"p{self.n}"
        if clone:
            shutil.copytree(clone, path)
        elif fixture:
            shutil.copytree(FIXTURES / fixture, path)
        else:
            path.mkdir()
        return path

    def run(self, project, name, args, expected=0, *, extra=None, known_limitation=False):
        env = dict(self.env)
        env.update(extra or {})
        before = inventory(project) if project != self.work else {}
        process = subprocess.Popen([str(self.apm), *args], cwd=project, env=env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = process.communicate(b"", timeout=120)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                command = (
                    "function Stop-FixtureTree([int]$ProcessId) { "
                    "Get-CimInstance Win32_Process -Filter \"ParentProcessId = $ProcessId\" | "
                    "ForEach-Object { Stop-FixtureTree $_.ProcessId }; "
                    "Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue }; "
                    f"Stop-FixtureTree {process.pid}"
                )
                subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True)
            else:
                process.kill()
            out, err = process.communicate()
            raise RuntimeError(f"{name}: timed out; project is preserved at {project}")
        after = inventory(project) if project != self.work else {}
        result = {
            "sequence": len(self.results) + 1,
            "id": name, "apm_version": "0.31.0", "executable": str(self.apm),
            "cwd": str(project), "argv": args, "exit_code": process.returncode, "expected_exit": expected,
            "known_cli_limitation": known_limitation,
            "stdout": out.decode("utf-8", errors="replace"), "stderr": err.decode("utf-8", errors="replace"),
            "before": before, "after": after,
        }
        self.results.append(result)
        write(self.work / "results.json", json.dumps(self.results, indent=2, ensure_ascii=True) + "\n")
        label = "KNOWN-CLI-LIMITATION" if known_limitation else "OBSERVED"
        print(f"{label} {name}: exit {process.returncode} (expected {expected})", flush=True)
        if process.returncode != expected:
            print(result["stdout"], result["stderr"])
            raise RuntimeError(f"{name}: unexpected result; preserved at {self.work}")
        return result

    def materialize(self, fixture):
        project = self.project(fixture)
        lock = (project / "apm.lock.yaml").read_bytes()
        self.run(project, fixture + "-frozen", ["install", "--frozen"])
        self.run(project, fixture + "-ci", ["audit", "--ci", "--no-fail-fast", "-f", "json"])
        assert lock == (project / "apm.lock.yaml").read_bytes(), fixture + " changed its locked contract"
        return project

    def baseline(self):
        for fixture in ["repro", "hooks", "lifecycle", "policy", "mcp", "pack-check"]:
            self.materialize(fixture)

    def repro(self):
        project = self.materialize("repro")
        for target, relative in [
            ("copilot", ".github/instructions/library.instructions.md"),
            ("claude", ".claude/rules/library.md"),
            ("cursor", ".cursor/rules/library.mdc"),
        ]:
            p = self.project(clone=project)
            path = p / relative
            write(path, path.read_text(encoding="utf-8") + "\nBenign fixture edit.\n")
            self.run(p, target + "-bare-drift", ["audit", "-f", "json"])
            self.run(p, target + "-ci-drift", ["audit", "--ci", "--no-fail-fast", "-f", "json"], 1)
        p = self.project(clone=project)
        lock = read_yaml(p / "apm.lock.yaml")
        lock["deployments"][0]["owners"] = ["not-a-declared-owner"]
        lock["deployments"][0]["active_owner"] = "not-a-declared-owner"
        save_yaml(p / "apm.lock.yaml", lock)  # Deliberate scratch corruption, never an exported lock.
        self.run(p, "invalid-owner-bare", ["audit", "-f", "json"], 1)
        self.run(p, "invalid-owner-ci", ["audit", "--ci", "--no-fail-fast", "-f", "json"], 1)
        p = self.project(clone=project)
        for path in list((p / ".github").rglob("*.md")) + list((p / ".claude").rglob("*.md")) + list((p / ".cursor").rglob("*.mdc")):
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.run(p, "canonical-crlf-hashes", ["audit", "--ci", "--no-fail-fast", "-f", "json"])
        p = self.project(clone=project)
        before = read_yaml(p / "apm.lock.yaml")
        canary = p / ".github/instructions/library.instructions.md"
        canary.unlink()
        self.run(p, "lock-retains-ownership", ["lock"])
        assert not canary.exists()
        assert before["deployments"] == read_yaml(p / "apm.lock.yaml")["deployments"]

    def policy(self):
        p = self.materialize("policy")
        self.run(p, "local-parent-merged", ["policy", "status", "--policy-source", "./apm-policy.child.yml", "--json", "--check"])
        self.run(p, "policy-warning", ["audit", "--ci", "--policy", "./apm-policy.warn.yml", "-f", "json"])
        self.run(p, "policy-blocking", ["audit", "--ci", "--policy", "./apm-policy.block.yml", "-f", "json"], 1)
        self.run(p, "child-cannot-clear-parent", ["audit", "--ci", "--policy", "./apm-policy.child.yml", "-f", "json"], 1)
        self.run(p, "explicit-policy-beats-flag", ["audit", "--ci", "--policy", "./apm-policy.block.yml", "--no-policy", "-f", "json"], 1)
        self.run(p, "env-disables-explicit-policy", ["audit", "--ci", "--policy", "./apm-policy.block.yml", "-f", "json"],
                 extra={"APM_POLICY_DISABLE": "1"}, known_limitation=True)

    def security(self):
        p = self.project()
        write(p / "critical.md", "Benign marker\n" + chr(0x202E) + "\n")
        write(p / "warning.md", "Benign " + chr(0x200B) + " spacing marker\n")
        self.run(p, "critical-scan", ["audit", "--file", "critical.md"], 1)
        self.run(p, "warning-scan", ["audit", "--file", "warning.md"], 2)
        self.run(p, "strip-preview", ["audit", "--file", "critical.md", "--strip", "--dry-run"])
        self.run(p, "strip", ["audit", "--file", "critical.md", "--strip"])
        self.run(p, "clean-after-strip", ["audit", "--file", "critical.md"])
        p = self.project("repro")
        (p / "apm.lock.yaml").unlink()
        path = p / "package/.apm/instructions/library.instructions.md"
        write(path, path.read_text(encoding="utf-8") + "\nBenign spacing marker " + chr(0x200B) + ".\n")
        self.run(p, "warning-install", ["install"])
        self.run(p, "warning-installed-bare", ["audit", "-f", "json"], 2)
        self.run(p, "warning-installed-ci", ["audit", "--ci", "--no-fail-fast", "-f", "json"])

    def lifecycle(self):
        p = self.materialize("lifecycle")
        assert not (p / "events.json").exists()
        self.run(p, "lifecycle-validate", ["lifecycle", "validate"])
        self.run(p, "lifecycle-trust", ["lifecycle", "trust"])
        self.run(p, "install-preview-no-events", ["install", "--dry-run"])
        assert not (p / "events.json").exists()
        self.run(p, "update-preview-has-pre-events", ["update", "--dry-run"])
        assert "pre-update" in json.loads((p / "events.json").read_text(encoding="utf-8"))
        before = (p / "events.json").read_bytes()
        self.run(p, "update-preview-kill-switch", ["update", "--dry-run"], extra={"APM_NO_SCRIPTS": "1"})
        assert before == (p / "events.json").read_bytes()
        self.run(p, "uninstall-preview-pre-event", ["uninstall", "./package", "--dry-run"])
        self.run(p, "lifecycle-untrust", ["lifecycle", "untrust"])
        f = p / ".github/instructions/notice.instructions.md"
        write(f, f.read_text(encoding="utf-8") + "\nBenign user annotation.\n")
        old_lock = (p / "apm.lock.yaml").read_bytes()
        self.run(p, "uninstall-retains-edited-file", ["uninstall", "_local/package"], 1)
        assert old_lock == (p / "apm.lock.yaml").read_bytes() and f.exists()

    def hooks(self):
        p = self.materialize("hooks")
        settings = p / ".claude/settings.json"
        data = json.loads(settings.read_text(encoding="utf-8"))
        data["hooks"]["SessionStart"].append({"hooks": [{"type": "command", "command": "echo User-owned harmless fixture"}]})
        write(settings, json.dumps(data, indent=2) + "\n")
        self.run(p, "user-hook-is-not-drift", ["audit", "--ci", "--no-fail-fast", "-f", "json"])
        self.run(p, "user-hook-survives-uninstall", ["uninstall", "./package"])
        assert "User-owned harmless fixture" in settings.read_text(encoding="utf-8")
        p = self.materialize("hooks")
        sidecar = p / ".claude/apm-hooks.json"
        write(sidecar, sidecar.read_text(encoding="utf-8").replace("notice.mjs", "notice-edited.mjs"))
        self.run(p, "owned-hook-sidecar-is-drift", ["audit", "--ci", "--no-fail-fast", "-f", "json"], 1)

    def mcp(self):
        p = self.materialize("mcp")
        path = p / ".github/mcp.json"
        path.unlink()
        self.run(p, "mcp-native-missing-not-audit-gated", ["audit", "--ci", "--no-fail-fast", "-f", "json"],
                 known_limitation=True)
        self.run(p, "mcp-frozen-repairs-native-file", ["install", "--frozen"])
        assert path.is_file()
        m = read_yaml(p / "apm.yml")
        m["dependencies"]["mcp"][0]["args"] = ["--changed-fixture"]
        save_yaml(p / "apm.yml", m)
        self.run(p, "mcp-frozen-catches-manifest-lock-mismatch", ["install", "--frozen"], 1)
        self.run(p, "mcp-reconcile-new-intent", ["install"])
        path.unlink()
        path.mkdir()
        self.run(p, "mcp-native-write-error", ["install"], 1)
        self.run(p, "force-does-not-hide-write-error", ["install", "--force"], 1)

    def pack(self):
        p = self.materialize("pack-check")
        self.run(p, "pack-generate-local-output", ["pack", "--offline", "--json"])
        before = inventory(p)
        self.run(p, "check-clean-readonly", ["pack", "--check-clean", "--offline", "--json"])
        assert before == inventory(p)
        path = p / ".claude-plugin/marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["description"] = "Benign generated-output drift marker."
        write(path, json.dumps(data, indent=2) + "\n")
        before = inventory(p)
        self.run(p, "check-clean-drift-four", ["pack", "--check-clean", "--offline", "--json"], 4)
        assert before == inventory(p)

    def credential(self):
        with RegistryFixture() as server:
            p = self.project()
            manifest = {
                "name": "operations-credential-fixture", "version": "1.0.0", "targets": ["copilot"],
                "registries": {"fixture": {"url": server.base}, "default": "fixture"},
                "dependencies": {"apm": ["operations/exact#1.0.0"]},
                "includes": "auto",
            }
            save_yaml(p / "apm.yml", manifest)
            config = Path(self.env["HOME"]) / ".apm/config.json"
            write(config, json.dumps({"experimental": {"registries": True},
                                     "registries": {"fixture": {"url": server.base}}}) + "\n")
            dummy = {"APM_REGISTRY_TOKEN_FIXTURE": "PUBLIC-NON-CREDENTIAL-FIXTURE"}
            self.run(p, "http-never-sends-credential", ["install"], 1, extra=dummy)
            assert not server.requests
            # A different binding withholds the marker, so the public fixture is anonymous.
            write(config, json.dumps({"experimental": {"registries": True},
                                     "registries": {"fixture": {"url": server.base + "/another-path"}}}) + "\n")
            self.run(p, "different-binding-anonymous-only", ["install"], extra=dummy)
            assert not any(r["authorization_present"] for r in server.requests)

    def registry(self):
        # Explicit fixture config only, under disposable HOME; no `apm config` call.
        write(Path(self.env["HOME"]) / ".apm/config.json", '{"experimental":{"registries":true}}\n')
        with RegistryFixture() as server:
            p = self.materialize("registry")
            server.advance()
            self.run(p, "registry-current-wanted-latest", ["outdated"])
            self.run(p, "registry-selected-preview", ["update", "operations/range", "--dry-run", "--verbose"])
            self.run(p, "registry-consent-required", ["update", "operations/range"], 1)
            self.run(p, "registry-selected-update", ["update", "operations/range", "--yes"])
            versions = {d["repo_url"]: d["version"] for d in read_yaml(p / "apm.lock.yaml")["dependencies"]}
            assert versions == {"operations/exact": "1.0.0", "operations/range": "1.1.0", "operations/other": "1.0.0"}
            # The plan/lock/deployed files preserve the unselected dep, but this
            # binary stages its newer cache content anyway. Do not hide the drift.
            self.run(p, "registry-selected-cache-drift", ["audit", "--ci", "--no-fail-fast", "-f", "json"],
                     1, known_limitation=True)
            before = (p / "apm.lock.yaml").read_bytes()
            self.run(p, "registry-selected-frozen-repair", ["install", "--frozen"])
            assert before == (p / "apm.lock.yaml").read_bytes()
            self.run(p, "registry-updated-ci-after-repair", ["audit", "--ci", "--no-fail-fast", "-f", "json"])
            p = self.materialize("registry-graph")
            self.run(p, "bounded-direct-unbounded-transitive", ["audit", "--ci", "--policy", "./apm-policy.yml", "-f", "json"])
            m = read_yaml(p / "apm.yml")
            m["dependencies"]["apm"][0]["version"] = ">=1.0.0"
            save_yaml(p / "apm.yml", m)
            self.run(p, "new-direct-intent", ["install"])
            self.run(p, "unbounded-direct-fails-policy", ["audit", "--ci", "--policy", "./apm-policy.yml", "-f", "json"], 1)
            assert not any(r["authorization_present"] for r in server.requests)
            write(self.work / "registry-requests.json", json.dumps(server.requests, indent=2) + "\n")

    def trust_limit(self):
        p = self.project("trust")
        self.run(p, "parked-hook-install", ["install"])
        self.run(p, "parked-decision", ["approve", "--list"])
        assert (p / ".github/mcp.json").exists()  # Observed local MCP gate mismatch, not an intended guarantee.
        self.run(p, "parked-hook-audit-replay", ["audit", "--ci", "--no-fail-fast", "-f", "json"], 1, known_limitation=True)
        self.run(p, "canonical-approval", ["approve", "./package"])
        self.run(p, "approved-install", ["install"])
        self.run(p, "approved-audit", ["audit", "--ci", "--no-fail-fast", "-f", "json"])

    def cleanup_limit(self):
        if os.name != "nt":
            print("SKIPPED-platform: exclusive Windows file-lock reproduction")
            return
        p = self.materialize("lifecycle")
        file = p / "apm_modules/_local/package/apm.yml"
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p,
                                      ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        kernel.CreateFileW.restype = ctypes.c_void_p
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.CreateFileW(str(file), 0x80000000, 0, None, 3, 0x80, None)
        if handle == ctypes.c_void_p(-1).value:
            raise OSError(ctypes.get_last_error(), "Could not create exclusive fixture lock")
        try:
            self.run(p, "windows-locked-cleanup-reports-success", ["uninstall", "./package"],
                     known_limitation=True)
        finally:
            kernel.CloseHandle(handle)
        assert file.exists() and not (p / "apm.lock.yaml").exists()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apm", required=True, help="Absolute prepared APM 0.31.0 executable; never use PATH")
    parser.add_argument("--work", help="New absolute short scratch path (must not already exist)")
    parser.add_argument("--suite", choices=["baseline", "repro", "policy", "security", "lifecycle", "hooks", "mcp", "pack", "credential", "registry",
                                          "trust-limit", "cleanup-limit", "all"], default="baseline")
    args = parser.parse_args()
    probe = Probe(args.apm, args.work)
    suites = ["baseline", "repro", "policy", "security", "lifecycle", "hooks", "mcp", "pack", "credential", "registry"] if args.suite == "all" else [args.suite]
    for suite in suites:
        getattr(probe, suite.replace("-", "_"))()
    print(f"Evidence retained: {probe.work}")
    print("Observed expected outcomes. Known CLI limitations are NOT a claim that those guarantees passed.")


if __name__ == "__main__":
    main()
