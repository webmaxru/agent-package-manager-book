# Chapter 11 — Enterprise at Fleet Scale · verified samples

Verified against **apm v0.23.1** on 2026-07-02 (Windows). `microsoft/apm-action` latest **v1.10.0**.
Full reference: [../../../content/research/11-enterprise-at-fleet-scale-reference.md](../../../content/research/11-enterprise-at-fleet-scale-reference.md).

## What is RUNNABLE vs SKIPPED-needs-network

| Surface | Status | Notes |
|---|---|---|
| `apm audit --ci` (the required CI gate) | **RUNNABLE** | exit **0** clean (`All 9 check(s) passed`) / exit **1** on a policy violation — both re-confirmed live |
| `apm config` / `apm cache` | **RUNNABLE** | introspected live (keys / cache location / prune) |
| `microsoft/apm-action` workflow YAML | **SKIPPED-needs-network** | a GitHub Action cannot run locally; the gate it invokes IS verified |
| Registry proxy / air-gapped (`PROXY_REGISTRY_*`, `apm pack`) | **SKIPPED-needs-network** | needs an Artifactory/private host; env-var knobs documented from the docs |
| Org-remote policy discovery + `extends:` MERGE | **SKIPPED-needs-network** | needs `<org>/.github`; local-file `extends:` does not merge (Chapter 9) |

## Files
- [workflows/apm-audit.yml](workflows/apm-audit.yml) — minimal required-check gate (`microsoft/apm-action@v1` + `apm audit --ci`).
- [workflows/apm-audit-sarif.yml](workflows/apm-audit-sarif.yml) — SARIF for Code Scanning (`if: always()` upload).
- [workflows/apm-audit-setup-only.yml](workflows/apm-audit-setup-only.yml) — audit-only pattern (detects post-install tampering).

All three workflow files are **documentation samples** (SKIPPED-needs-network) — copy into a real repo's
`.github/workflows/` and set the `APM_PAT` secret to use them.

## How the RUNNABLE gate was verified (exit codes)

The one clearly runnable enterprise surface. Reuses the Chapter 9 `require_pinned_constraint` recipe
(needs network for one public package; **no tokens**):

```powershell
# PATH refresh (v0.23.1), scratch dir OUTSIDE the repo
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$root = "$env:TEMP\apm-ch11"; Remove-Item -Recurse -Force $root -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $root | Out-Null; Set-Location $root

apm init -y --target copilot
apm install microsoft/apm-sample-package#v1.0.0      # pinned DIRECT dep + lockfile -> exit 0
apm audit --ci                                       # clean gate -> "All 9 check(s) passed", exit 0

@'
name: fleet-block
version: "1.0.0"
enforcement: block
dependencies:
  require_pinned_constraint: true
'@ | Set-Content pol-block.yml
apm audit --ci --policy ./pol-block.yml              # pinned direct + unpinned transitive -> exit 0 (29 checks)

# Same policy against an UNPINNED direct dep -> the gate fails:
$b = "$env:TEMP\apm-ch11\block-demo"; New-Item -ItemType Directory -Force $b | Out-Null; Set-Location $b
apm init -y --target copilot
apm install microsoft/apm-sample-package#main        # bare branch = UNPINNED direct dep
Copy-Item ..\pol-block.yml .\pol-block.yml
apm audit --ci --policy ./pol-block.yml              # dependency-pinned-constraint fails -> exit 1
```

Expected `dependency-pinned-constraint` detail on the exit-1 run:
`microsoft/apm-sample-package: bare branch 'main' tracks a moving tip` → `[x] 1 of 18 check(s) failed`.

## Notes
- **`require_pinned_constraint` targets DIRECT deps only** (verified): a pinned direct dep with an
  unpinned *transitive* passes (`All 29 check(s) passed`, exit 0). The install-time `unpinned` warning is
  advisory.
- **The clean gate = 8 baseline checks + drift = 9.** Baseline runs independently of the `enforcement`
  dial and is never bypassable.
- **`apm audit --ci --policy` is `[experimental]`** at v0.23.1. Pin the CLI before relying on it as a
  production gate.
- **Proxy knobs are environment variables, not `apm config` keys** — `apm config get` lists only
  `auto-integrate`, `temp-dir`, `mcp-registry-url`. Pin `PROXY_REGISTRY_*` / `HTTPS_PROXY` in CI secrets.
