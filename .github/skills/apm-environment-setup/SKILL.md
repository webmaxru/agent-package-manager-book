---
name: apm-environment-setup
description: Prepares a version-pinned APM CLI and scratch projects for empirical exploration and example verification without updating the user's global CLI or the book's installed skills.
---

# APM Environment Setup

Use this before CLI exploration or example verification. The orchestrator supplies an exact
stable **APM `X.Y.Z`** and a run-specific scratch directory outside the repository.
Do not independently install "latest" after the update's target has been frozen.

## Requirements

- Python 3.10+ and Git; network access for a missing CLI distribution and public packages.
- An absolute, session-owned scratch directory, not the repository or the user's home root.
- The selected release's installation guidance. The official Python distribution is `apm-cli`;
  do not install the unrelated `apm` package.

## Pin and isolate the executable

First try the run's existing executable and check `--version`. Reuse it only if it reports the
exact requested version. If it is missing, use a dedicated venv or the checksum-verified standalone binary below.
Do not modify package-index policy or disable TLS if the configured index fails.

### Isolated Python distribution

```powershell
# Inputs from the orchestrator; 0.31.0 is an example, not a floating default.
$ApmVersion = "0.31.0"
$RunRoot = "<absolute session artifacts directory>\apm-verification"
$Venv = Join-Path $RunRoot "venv-$ApmVersion"

python -m venv $Venv
if ($LASTEXITCODE -ne 0) { throw "Could not create the verification venv" }
$Python = Join-Path $Venv "Scripts\python.exe"
& $Python -m pip install "apm-cli==$ApmVersion"
if ($LASTEXITCODE -ne 0) { throw "Could not install the pinned APM version" }
$Apm = Join-Path $Venv "Scripts\apm.exe"
& $Apm --version
if ($LASTEXITCODE -ne 0) { throw "The pinned APM executable failed" }
```

Compare the reported version with `$ApmVersion`; mismatch is a blocker. If the exact distribution or configured package index is unavailable, stop retries and use
that release's official binary if permitted by the environment's source policy, or report the
blocker. Never downgrade silently, bypass checksum failures, or fall back to latest.
For Unix use the same `python -m venv` + exact `apm-cli==X.Y.Z` install, with the venv's `bin`
executables instead of `Scripts`.

### Standalone Windows binary, without a global installer

This avoids Python dependency installation and does not modify PATH or an existing global CLI.
Use the selected release's Windows x86_64 asset (confirm platform support in that release):

```powershell
$ApmVersion = "0.31.0"
$RunRoot = "<absolute session artifacts directory>\apm-verification"
$Native = Join-Path $RunRoot "native-$ApmVersion"
New-Item -ItemType Directory -Path $Native -Force -ErrorAction Stop | Out-Null
$Base = "https://github.com/microsoft/apm/releases/download/v$ApmVersion"
$Archive = Join-Path $Native "apm-windows-x86_64.zip"
$Checksum = "$Archive.sha256"
Invoke-WebRequest "$Base/apm-windows-x86_64.zip" -OutFile $Archive -TimeoutSec 90 -ErrorAction Stop
Invoke-WebRequest "$Base/apm-windows-x86_64.zip.sha256" -OutFile $Checksum -TimeoutSec 90 -ErrorAction Stop
$Expected = ((Get-Content -LiteralPath $Checksum -Raw).Trim() -split "\s+")[0]
if ($Expected -notmatch "^[0-9a-fA-F]{64}$") { throw "Malformed publisher checksum" }
if ((Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash -ne $Expected) {
    throw "APM archive checksum mismatch"
}
$Unpacked = Join-Path $Native "unpacked"
Expand-Archive -LiteralPath $Archive -DestinationPath $Unpacked -ErrorAction Stop
$Executables = @(Get-ChildItem -LiteralPath $Unpacked -Filter apm.exe -File -Recurse)
if ($Executables.Count -ne 1) { throw "Expected one APM executable" }
$Apm = $Executables[0].FullName
& $Apm --version
if ($LASTEXITCODE -ne 0) { throw "The pinned APM executable failed" }
```

Use a fresh version-specific directory, or reuse an already verified executable; do not force
extraction over another run. Require the reported version to equal the frozen target before use.
For a binary install record the release URL and verified SHA-256 instead of `pip freeze`.
Do not skip missing checksums or bypass a download/execution warning.

### Share the verified environment

Always invoke the **absolute executable path**. PowerShell tool calls use fresh processes, so
activation/PATH changes and variables do not persist. Pass the executable path to every agent
and reconstruct variables in each shell call. Record `apm --version`, the platform, executable
path, and installation provenance (Python version + `pip freeze`, or binary checksum).

A venv isolates Python packages, **not APM's per-user cache/configuration or host credentials**.
Use a disposable container/test user for global-state tests. Ordinary book verification must not
run global installs, self-update, mutate user configuration, or change the book repo's root
`apm.yml` / `apm.lock.yaml`. Do not update the authoring skills as a side effect of studying APM.

## Inspect and scaffold in scratch projects

Start with the pinned executable's `--help` and the relevant subcommand help. Confirm the flags
before running examples; existing agent reference lists are hints, not authority.

```powershell
& $Apm --help
& $Apm init --help
& $Apm install --help
& $Apm audit --help
```

Give each chapter/verifier a separate project under `$RunRoot`. Scaffold with the selected CLI,
then run the chapter's exact commands there. Select real public dependency refs from the
existing examples or the package's published tags/commits, and **pin them before verification**.
Do not use a floating sample install to establish reproducibility. Inspect the generated
manifest and lockfile; preserve their real schema rather than hand-inventing fields.

Commands that are meant to fail must assert the expected exit code and behavior. Capture
generated lockfiles for committed examples under `backend/examples`, along with their verified
CLI version. Keep caches, raw logs, venvs, and temporary projects out of Git.

## Credentials and cleanup

Public examples should not require private tokens. Never echo, hardcode, or commit credentials.
If authentication, private infrastructure, or a live publish is required, document
`SKIPPED-needs-network` with the exact reason. Do not use that marker for a broken local example.

Clean up only the explicitly identified scratch projects after preserving evidence. Do not
remove shared caches, another agent's environment, or the entire session-artifacts directory.

## References

- Installation: https://microsoft.github.io/apm/getting-started/installation/
- Source/package metadata: https://github.com/microsoft/apm
- Consumer ramp: https://microsoft.github.io/apm/consumer/
