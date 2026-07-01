---
description: Conventions for Agent Package Manager (APM) manifest and command examples used in the book.
applyTo: "**/apm*.yml"
---

# APM Example Conventions

Applies to all APM example artifacts in the book — `apm.yml` manifests, `apm-policy.yml` policies,
and the `apm` command snippets shown alongside them. Goal: every example is **minimal, valid,
reproducible, and secret-free**.

## Environment
- Use the real `apm` CLI (see the `apm-environment-setup` skill). Confirm command and flag names by
  running `apm --help` / `apm <cmd> --help` — do not invent them.
- Prefer **public** sample packages (e.g. `microsoft/apm-sample-package`) so examples resolve
  without private tokens.

## Style
- **Minimal**: the smallest manifest that demonstrates the feature; no unrelated dependencies.
- **Pin references.** Show explicit version/ref pinning (e.g. `#v2.1`, a tag, or a commit) rather
  than floating refs, so the lockfile is deterministic.
- Declare **MCP servers explicitly** — APM blocks undeclared transitive MCP servers by default.
- Add a brief comment stating which concept/feature the example demonstrates.
- Keep `apm.yml` keys and structure faithful to a freshly `apm init`-generated manifest.

## Secrets & live actions
- **Never hardcode or commit tokens.** Read host credentials from environment / a gitignored `.env`.
- For examples that would push, publish, or need private access, mark them `SKIPPED-needs-network`
  so verification stays deterministic.

## Verification
- Every example must be checked by `code-verifier`: the manifest schema is valid and (where the
  environment allows) `apm install` resolves it and `apm audit` passes. Reach **PASS** (or documented
  `SKIPPED-needs-network`) before it ships in a chapter.
- Record the **`apm` CLI version** the example was verified against.
- Commit the resulting `apm.lock.yaml` for any committed sample project for reproducibility.

## Versioning
- APM evolves quickly; flag any command, flag, or manifest key that may be preview/unstable, and
  re-confirm it against the installed CLI version.
