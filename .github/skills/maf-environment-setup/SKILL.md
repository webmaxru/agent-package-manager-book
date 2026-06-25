---
name: maf-environment-setup
description: Creates a reproducible Python backend environment for the playbook and installs the Microsoft Agent Framework packages so agents can import, introspect, and run the framework. Use before any library exploration or code verification.
---

# MAF Environment Setup

Provides a reproducible Python environment in which the playbook's agents can **import, introspect,
and execute the real Microsoft Agent Framework**. Used by `maf-library-explorer` and `code-verifier`.

## Requirements
- **Python 3.10+** (MAF supports 3.10–3.14).
- A virtual environment kept out of version control.

## Setup (Windows / PowerShell)
```powershell
# from the repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# Full framework (recommended for exploration — installs core + all integrations)
pip install agent-framework

# OR selective install for lighter envs:
#   pip install agent-framework-core         # core: OpenAI/Azure OpenAI + workflows/orchestrations
#   pip install agent-framework-foundry       # + Azure AI Foundry
#   pip install agent-framework-copilotstudio --pre   # + Copilot Studio (preview)
```

> Each PowerShell tool call runs in a fresh process — re-activate the venv (or call
> `.\.venv\Scripts\python.exe` directly) in every command.

## Record the version you study
```powershell
.\.venv\Scripts\python.exe -c "import importlib.metadata as m; print('agent-framework', m.version('agent-framework'))"
```
Always note the inspected version in research/verification artifacts — MAF moves fast.

## Introspection starting points
```powershell
.\.venv\Scripts\python.exe -c "import agent_framework, inspect; print([n for n in dir(agent_framework) if not n.startswith('_')])"
.\.venv\Scripts\python.exe -c "import agent_framework.openai as o; print([n for n in dir(o) if not n.startswith('_')])"
```
Use `inspect.signature`, `obj.__doc__`, and `inspect.getsource` to document real signatures, and
read the installed package source plus the GitHub samples for usage patterns.

## Credentials
Agents and chat clients need provider keys to make live calls. Put them in a **`.env`** (gitignored),
never in code or committed files:
```
OPENAI_API_KEY=...
OPENAI_MODEL=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_MODEL=...
FOUNDRY_PROJECT_ENDPOINT=...
```
For examples that would make live calls, prefer **mocks/stubs** or mark them SKIPPED-needs-creds so
verification stays deterministic and secret-free.

## Reproducibility
Pin what you used so others can reproduce:
```powershell
.\.venv\Scripts\python.exe -m pip freeze > backend\requirements.lock.txt
```

## References
- PyPI: https://pypi.org/project/agent-framework/
- Docs: https://learn.microsoft.com/en-us/agent-framework/
- Repo & samples: https://github.com/microsoft/agent-framework
