# Demo Walkthrough — *A Supply Chain for Agent Context*

**Talk track + exact terminal commands for the live demo.**
Everything here was tested end‑to‑end against the real `apm` CLI (**v0.23.1**) and a real GitHub repo.

- **Portal (trusted source):** <https://github.com/webmaxru/apm-enterprise-portal-demo> — released **`v1.0.0`**
- **Packages:** `skills/secure-coding`, `skills/pr-review`, `skills/api-standards` + `apm-policy.yml`
- **Harnesses proven:** Copilot, Claude, Cursor (from one manifest)
- **Deck:** [`slides/index.html`](index.html) — this demo fills live segments 7–10.

> **Mental model for the room:** the portal repo is Atlas Corp’s *trusted source*; a team’s `apm.yml`
> is the *bill of materials*; `apm.lock.yaml` is the *stamped, hash‑verified* BOM; `apm-policy.yml` is
> the *sourcing policy*; `apm audit --ci` is the *inspection gate*.

---

## 0 · Pre‑flight (before you present)

Run these once; they are **not** part of the live track.

```powershell
apm --version           # expect: Agent Package Manager (APM) CLI version 0.23.1
gh auth status          # expect: Logged in to github.com account webmaxru
```

Prepare a **clean, empty working folder** for the consumer and open it in your terminal:

```powershell
# pick a scratch location you like
$demo = "$HOME\Downloads\projects\orders-service"
Remove-Item -Recurse -Force $demo -ErrorAction Ignore
New-Item -ItemType Directory $demo | Out-Null
Set-Location $demo
```

Terminal tips: font size ≥ 18pt, window wide enough for the lockfile, and set
`$env:APM_LOG_LEVEL="INFO"`. First `apm` call after boot is slow (a few seconds) — **warm it up**
before you go on stage by running `apm --version` once.

Have **two things open**: this terminal, and the portal repo in a browser tab
(`github.com/webmaxru/apm-enterprise-portal-demo`).

---

## 1 · Consume — one manifest, every harness  *(deck slide 7 · ~4 min)*

**Say:** *“Marco just joined the Orders squad. Instead of hunting wiki links, he sources the org’s
approved agent context from our trusted registry — pinned to a version.”*

Create the team’s manifest (paste live so they see it):

```powershell
@'
name: orders-service
version: 2.4.0
targets:
  - copilot
  - claude
  - cursor
dependencies:
  apm:
    - webmaxru/apm-enterprise-portal-demo/skills/secure-coding#v1.0.0
    - webmaxru/apm-enterprise-portal-demo/skills/pr-review#v1.0.0
    - webmaxru/apm-enterprise-portal-demo/skills/api-standards#v1.0.0
includes: auto
'@ | Set-Content apm.yml
```

**Point at:** `targets:` (three harnesses, one file) and the `#v1.0.0` pins (trusted source + version).

Install:

```powershell
apm install
```

**Expected (abridged):**

```
[i] Targets: claude, copilot, cursor  (source: apm.yml)
  [+] github.com/webmaxru/apm-enterprise-portal-demo/skills/api-standards#v1.0.0 #v1.0.0 @22d3f0f8
      |-- Skill integrated -> .agents/skills/, .claude/skills/
  ... (pr-review, secure-coding) ...
[*] Installed 3 APM dependencies in ~12s.
```

Show what landed — the **same rules, native to each harness**:

```powershell
Get-ChildItem .agents\skills, .claude\skills
apm deps list
```

**Say:** *“One command. Copilot, Claude, and Cursor all now carry Atlas’s secure‑coding standard,
PR‑review checklist, and API rules. No copy‑paste, no drift.”*

---

## 2 · Reproduce — the stamped bill of materials  *(deck slide 8 · ~3 min)*

**Say:** *“What Marco got is exactly what CI gets — down to the hash.”*

```powershell
Get-Content apm.lock.yaml
```

**Point at**, for each package: `resolved_ref: v1.0.0`, `resolved_commit:`, `content_hash: sha256:…`,
and `deployed_file_hashes:`. **Say:** *“That hash is provenance. If anyone tampers with a package or a
tag moves, the next install refuses. This is the SBOM for our agent context.”*

Prove the CI‑safe path:

```powershell
apm install --frozen
```

**Expected:** `No changes -- install state already up to date` and **exit 0**. `--frozen` fails a build
if `apm.yml` and `apm.lock.yaml` disagree.

---

## 3 · Publish — become a trusted source  *(deck slide 9 · ~4 min)*

**Say:** *“A package is just a folder with a `SKILL.md`. When a team’s pattern is good enough for
everyone, the platform team publishes it as a new version.”*

Switch to a **clone of the portal** (pre‑clone before the talk to save time):

```powershell
# pre-flight: git clone https://github.com/webmaxru/apm-enterprise-portal-demo
Set-Location "$HOME\Downloads\projects\apm-enterprise-portal-demo"
```

Author a new approved skill (paste live):

```powershell
New-Item -ItemType Directory skills\commit-standards -Force | Out-Null
@'
---
name: commit-standards
description: Atlas commit-message conventions for AI coding agents. Use when writing commits or preparing a PR in an Atlas service.
license: MIT
metadata:
  author: Atlas Platform Engineering
  version: "1.0"
---

# Atlas Commit Standards

- Conventional Commits: `type(scope): summary` (feat, fix, docs, refactor, test, chore).
- Imperative, <= 72-char summary. Explain the *why* in the body.
- Reference the issue: `Refs #1234`. Never commit secrets or generated artifacts.
'@ | Set-Content skills\commit-standards\SKILL.md
```

Publish it as **v1.1.0** (this is a real release):

```powershell
git add -A
git commit -m "Add commit-standards skill"
git push
gh release create v1.1.0 --title "v1.1.0" --notes "Add commit-standards skill"
```

Adopt it from the consumer — add the new line **under `dependencies.apm`** (in your editor), or
re-paste the whole manifest so the indentation is correct:

```powershell
Set-Location $demo
@'
name: orders-service
version: 2.4.0
targets:
  - copilot
  - claude
  - cursor
dependencies:
  apm:
    - webmaxru/apm-enterprise-portal-demo/skills/secure-coding#v1.0.0
    - webmaxru/apm-enterprise-portal-demo/skills/pr-review#v1.0.0
    - webmaxru/apm-enterprise-portal-demo/skills/api-standards#v1.0.0
    - webmaxru/apm-enterprise-portal-demo/skills/commit-standards#v1.1.0
includes: auto
'@ | Set-Content apm.yml
apm install
```

> The new dependency must sit **inside** the `dependencies.apm:` list — don’t append it after
> `includes:` (that’s outside the list and breaks the manifest).

**Say:** *“Published once, adopted by pinning a version. That’s how a good pattern stops being tribal
knowledge.”*

> **Alt (bundle/air‑gapped):** `apm pack` bundles a package with content hashes for offline
> distribution; `apm publish` targets a registry (early‑preview). For most orgs today, a git tag
> *is* the trusted source — that’s what we just did.

---

## 4 · Govern — the unbypassable gate  *(deck slide 10 · ~3 min)*

**Say:** *“Sourcing rules aren’t a wiki page — they’re enforced. Legal or Security sets the org
baseline once; CI won’t merge anything that violates it.”*

Show the org policy in the browser tab
([`apm-policy.yml`](https://github.com/webmaxru/apm-enterprise-portal-demo/blob/main/apm-policy.yml)):
trusted‑source **allow‑list** + **`require_pinned_constraint`**.

Run the gate against the org policy (fetched from the portal):

```powershell
apm audit --ci --policy webmaxru/apm-enterprise-portal-demo
```

**Expected:** a table of checks incl. `dependency-allowlist`, `dependency-pinned-constraint`,
`required-manifest-fields` → **`All 29 check(s) passed`**, **exit 0**.

Now play the careless PR — introduce an **unpinned** dependency:

```powershell
(Get-Content apm.yml) -replace 'secure-coding#v1.0.0','secure-coding#main' | Set-Content apm.yml
apm install | Out-Null
apm audit --ci --policy webmaxru/apm-enterprise-portal-demo
$LASTEXITCODE
```

**Expected:** `dependency-pinned-constraint … 1 dependency(ies) use unbounded constraints` →
**`check(s) failed`**, and `$LASTEXITCODE` = **`1`** (the required check blocks the merge).

**Say:** *“A developer can `--force` locally. CI can’t. The org baseline is the one thing nobody
can quietly skip — untrusted or unpinned context never reaches an agent.”*

Fix it back (leave the demo green):

```powershell
(Get-Content apm.yml) -replace 'secure-coding#main','secure-coding#v1.0.0' | Set-Content apm.yml
apm install | Out-Null
apm audit --ci --policy webmaxru/apm-enterprise-portal-demo   # passes again, exit 0
```

---

## 5 · Close  *(deck slides 11–12)*

**Say:** *“Trusted sources, pinned + hashed dependencies, an inspection gate in CI — the software
supply chain you already run, now for your agents. A few YAML files and one CI check.”*

---

## Reset between runs

**Consumer** (start fresh):

```powershell
Set-Location $demo
Remove-Item -Recurse -Force apm_modules, .agents, .claude, apm.lock.yaml -ErrorAction Ignore
# then re-create apm.yml from section 1
```

**Portal** — only if you created `v1.1.0` live and want to rehearse again:

```powershell
Set-Location "$HOME\Downloads\projects\apm-enterprise-portal-demo"
gh release delete v1.1.0 --yes --cleanup-tag
git reset --hard v1.0.0
git push --force origin main        # rewrites the pushed commit — you own this demo repo
```

> Skip the portal reset if you present the publish step as narration. The repo ships ready at
> `v1.0.0`; nothing needs to change before a run.

---

## Fallbacks (if the room’s network is flaky)

| Problem | Fallback |
| --- | --- |
| `apm install` can’t fetch | Pre‑install before the talk; the cache serves it offline. Show the already‑deployed files + lockfile. |
| First `apm` call hangs | It’s the cold start — always warm up with `apm --version` beforehand. |
| `gh release create` fails on stage | Skip live publish; narrate it and show an existing release in the browser. |
| Audit `--policy owner/repo` can’t fetch | Use a local copy: `apm audit --ci --policy .\apm-policy.yml` (behaves identically). |

## Command cheat‑sheet (all verified)

```text
apm --version
apm install                                             # consume (pinned, all targets)
apm deps list                                           # what resolved
Get-Content apm.lock.yaml                               # provenance: refs + sha256 hashes
apm install --frozen                                    # CI-safe reproduce (exit 0)
gh release create v1.1.0 --title v1.1.0 --notes "..."   # publish a new version
apm audit --ci --policy webmaxru/apm-enterprise-portal-demo   # gate: pass (29 checks, exit 0)
#   unpinned dependency -> dependency-pinned-constraint fails, exit 1
```
