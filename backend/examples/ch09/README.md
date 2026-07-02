# Chapter 9 — Governance & Policy · verified sample policies

Verified against **apm v0.23.1** on 2026-07-02 (Windows). The policy *engine* is flagged
**early preview** at this version — pin the CLI before relying on any of this as a production gate.

## Files
- [apm-policy.warn.yml](apm-policy.warn.yml) — Meridian **pilot** policy (`enforcement: warn`).
- [apm-policy.block.yml](apm-policy.block.yml) — Meridian **post-pilot** policy (`enforcement: block`).

Both are the running-example's before/after pair with the one schema bug fixed: the running example
put target rules under a **top-level `targets:`** key, which apm v0.23.1 **silently ignores**. The
real key is **`compilation.target.allow`**.

## How they were validated (parse + rule registration)
```powershell
apm policy status --policy-source ./apm-policy.warn.yml  -o json   # outcome=found, enforcement=warn
apm policy status --policy-source ./apm-policy.block.yml -o json   # outcome=found, enforcement=block
```
Both report `compilation_targets_allowed: 3` (the corrected key registers 3 targets). The identical
policy written with a top-level `targets:` block instead reports `-1` — i.e. no rule at all.

## How warn → block was proven (exit codes)
`apm audit --ci --policy <file>` returns **exit 0** under `enforcement: warn` (violations printed but
rendered `[+] passed`) and **exit 1** under `enforcement: block` (`[x] N of M check(s) failed`).
The baseline (8–9 lockfile/integrity checks) always runs and is independent of `enforcement`.

Reproduce the headline `require_pinned_constraint` violation end to end (needs network for one public
package):
```powershell
$root = "$env:TEMP\apm-ch09-repro"; New-Item -ItemType Directory -Force $root | Out-Null; Set-Location $root
apm init -y --target copilot
apm install microsoft/apm-sample-package#main        # bare branch = UNPINNED (resolves to a commit)
apm audit --ci --no-policy                           # baseline only  -> exit 0 (9 checks pass)

@'
name: pin-warn
version: "1.0.0"
enforcement: warn
dependencies:
  require_pinned_constraint: true
'@ | Set-Content pol-warn.yml
apm audit --ci --policy ./pol-warn.yml               # dependency-pinned-constraint flagged -> exit 0

(Get-Content pol-warn.yml).Replace('warn','block') | Set-Content pol-block.yml
apm audit --ci --policy ./pol-block.yml              # same violation -> exit 1
```
Expected `dependency-pinned-constraint` detail: `microsoft/apm-sample-package: bare branch 'main'
tracks a moving tip`.

## Notes / SKIPPED-needs-network
- `dependencies.require: meridian-finance/...` and `mcp.allow: io.github.github/github-mcp-server`
  reference a private package and a registry MCP. The **rules parse and enforce** (a missing required
  package fails `required-packages`; a self-defined MCP fails `mcp-self-defined`), but resolving those
  specific artifacts is **SKIPPED-needs-network**.
- `compilation.target.allow` registers as a rule but the **audit** check evaluates a *resolved* target;
  on a static manifest that only lists candidate `targets:`, it reports "No compilation target set in
  manifest" and passes. It bites at `apm install` / `apm compile` time (org-remote discovery →
  SKIPPED-needs-network).
- Full details, the confirmed schema, and the diff vs the running example:
  [../../../content/research/09-governance-and-policy-reference.md](../../../content/research/09-governance-and-policy-reference.md).
