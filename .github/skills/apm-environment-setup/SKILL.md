---
name: apm-environment-setup
description: Installs the real Agent Package Manager (APM) CLI and scaffolds a sample repo so agents can introspect the tool, run commands, and validate manifests. Use before any CLI exploration or example verification.
---

# APM Environment Setup

Provides a reproducible environment in which the book's agents can **install, introspect, and run
the real `apm` CLI**. Used by `apm-cli-explorer` and `code-verifier`.

## Requirements
- A shell with network access to fetch the CLI installer and sample packages.
- Git (APM resolves dependencies from git servers).
- A scratch directory kept out of version control for sample projects.

## Install the CLI (Windows / PowerShell)
```powershell
# from the repo root
irm https://aka.ms/apm-windows | iex

# Unix equivalent:
#   curl -sSL https://aka.ms/apm-unix | sh
```

> Each PowerShell tool call runs in a fresh process. If `apm` is not yet on `PATH` in a new shell,
> re-open the shell or reference the installed binary directly.

## Record the version you study
```powershell
apm --version
```
Always note the inspected version in research/verification artifacts — APM moves fast.

## Introspection starting points
```powershell
apm --help
apm install --help
apm run --help
apm audit --help
```
Read the top-level help and each subcommand's help to document real commands and flags. Study the
`apm.yml`, `apm.lock.yaml`, and `apm-policy.yml` schemas from the docs and from a generated project.

## Scaffold a sample project (for hands-on introspection)
```powershell
# in a scratch dir (NOT the repo)
apm init                                   # creates apm.yml
apm install microsoft/apm-sample-package   # add and resolve a real dependency
apm install                                # restore from apm.lock.yaml
```
Inspect the generated `apm.yml` and `apm.lock.yaml` to see version pinning and content hashes.

## Credentials
Public packages need no tokens. For **private** git sources, provide host tokens via a **`.env`**
(gitignored), never in code or committed files:
```
GITHUB_TOKEN=...
# GITLAB_TOKEN, AZURE_DEVOPS_PAT, etc. as needed for private sources
```
For examples that would push or require private access, prefer **public sample packages** or mark
them `SKIPPED-needs-network` so verification stays deterministic and secret-free.

## Reproducibility
Commit the `apm.lock.yaml` from any committed sample project so others reproduce the same setup
byte-for-byte, and record the `apm --version` you used.

## References
- Docs: https://microsoft.github.io/apm/
- Consumer ramp: https://microsoft.github.io/apm/consumer/
- Repo & samples: https://github.com/microsoft/apm
