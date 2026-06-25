---
description: Conventions for Microsoft Agent Framework (Python) code examples used in the playbook.
applyTo: "**/*.py"
---

# MAF Code Example Conventions

Applies to all Python example/backend code in the playbook. Goal: every example is **minimal,
runnable, version-aware, and secret-free**.

## Environment
- Target **Python 3.10+**. Develop/run inside the project venv (see the `maf-environment-setup` skill).
- Import from the real packages: `agent_framework` and provider submodules (e.g.
  `agent_framework.openai`). Confirm names by introspection — do not invent symbols.

## Style
- **Minimal**: smallest snippet that demonstrates the component; no unrelated scaffolding.
- MAF is **async-first** — show `async def` + `await`, and a clear entry point
  (`asyncio.run(main())`) when runnable standalone.
- Type-hint public examples; keep imports explicit at the top.
- Add a brief comment stating which concept/component the example demonstrates.

## Secrets & live calls
- **Never hardcode or commit credentials.** Read from environment / a gitignored `.env`.
- For examples that would call a live LLM/provider, prefer **mocks/stubs**, or guard the live call
  and mark the example `SKIPPED-needs-creds` so verification stays deterministic.

## Verification
- Every example must be run by `code-verifier` and reach **PASS** (or documented
  `SKIPPED-needs-creds`) before it ships in a chapter.
- Record the **`agent-framework` version** the example was verified against.
- Pin dependencies for reproducibility (`backend/requirements.lock.txt`).

## Versioning
- MAF evolves quickly; flag any use of preview (`--pre`) packages or APIs that may be unstable.
