# Chapter 4 independent delta verification — book 1.2 / APM 0.31.0

**Verdict: PASS — chapter claim gate closed by the prose/comment-only delta,
2026-09-16 UTC.** F4.1–F4.3 are resolved in the final source below. The
two documented audit discrepancies remain actual CLI **FAIL** results;
this is not an install-and-audit guarantee for those controls.
No APM command was rerun and no reviewer acceptance is claimed.

## Final prose/comment delta — source-specific PASS

| Revision | SHA256 |
| --- | --- |
| Original independently checked source; claim gate blocked | `4aa890b23b5a25ea7c2557e78040605ad3df28e040c6cffef628411a6937cada` |
| **Final source; chapter claim gate PASS** | **`c0f3d81788556838e3f55b1adc225b9716231786040544aa98ab098e73c41005`** |

**Chapter:** `content/chapters/the-manifest-apm-yml.html`.
**CLI evidence:** retained exact **APM 0.31.0** execution.
**New APM invocations: 0**, including no new `--version` call.
**New native runtime: 0.000 s.** No scratch project was created or resumed.

The final source was reconstructed **byte-for-byte** from the captured
original using only these three author corrections:

1. `#ch4-local-source-selection` now visibly states that CI audit exits
   **1** because the legacy-plugin input lacks `pkg/apm.yml`. It separates
   successful skill selection from an audit-clean guarantee.
2. `#ch4-includes-boundary` now visibly describes the combined-layout
   control's audit exit **1**: replay expects root `unlisted` and treats
   installed `secure-payment-review` as orphaned across shared and Claude
   paths. It distinguishes that failed replay from the successful pack
   selection and the clean single-layout instruction fixture.
3. The opening `RunRoot` comment uses a symbolic session-artifact location
   instead of the workstation-specific path.

No other source bytes changed. All **13 `<pre><code>` blocks** remain
identical, including attributes, entities, whitespace, line endings,
decoded content, and example IDs. No command/manifest/projection or
historical 0.23.1 stamp was changed.

The shared Ch3/Ch4 comparison verifies **38 captured fixture files across
eight fixture groups** against the original hashes and complete canonical
ZIP bytes. The exact noncanonical `path-options` and nested-MCP inputs,
registry helper, and competing-root-skill source also match the retained
input records. No fixture, complete lock, or operative command input was
silently changed to obtain this PASS.

### Resolved chapter claims; CLI failures remain FAIL

| Chapter ID / finding | Current chapter-claim status | Retained original CLI result |
| --- | --- | --- |
| `ch4-local-source-selection`, F4.1 | **PASS — scoped selection and visible audit failure** | `decl-path-options-install`: `install`, **0**, **1.864 s**; `decl-path-options-audit`: `audit --ci`, **FAIL / 1**, **1.868 s** |
| `ch4-includes-boundary`, F4.2 | **PASS — pack result distinguished from failed audit replay** | `pack2-auto-layout-pack`: `pack -o selected --verbose`, **0**, **1.926 s**; `pack2-source-audit`: `audit --ci`, **FAIL / 1**, **2.346 s** |
| Opening `RunRoot` comment, F4.3 | **PASS — symbolic provenance** | No executable effect or new command |

The raw audit bytes and their original version guards were reread,
not reexecuted. The retained diagnostics remain exact below, with only
the absolute scratch-root prefix represented by its existing alias:

```text
  config-consistency details:
    - ./pkg: package manifest not found at <Scratch>\p\ps\pkg\apm.yml; re-run 'apm install' to restore it

[x] 1 of 8 check(s) failed
```

```text
  drift details:
    - unintegrated: .agents/skills/unlisted/SKILL.md
    - unintegrated: .claude/skills/unlisted/SKILL.md
    - orphaned: .agents/skills/secure-payment-review/SKILL.md
    - orphaned: .claude/skills/secure-payment-review/SKILL.md

[x] 1 of 10 check(s) failed
```

The clean single-layout contrast remains backed by independent
`local-local-instruction-audit`: `audit --ci`, exit **0**, original
**3.031 s**, with the same canonical Core bytes. The main manifest,
native projections, Git/registry/MCP fragments, and dev-only example keep
their already verified input scopes. Native-plugin and marker-present
legacy replay limitations likewise remain unchanged. No actual CLI failure
became PASS or a network skip.

### Check receipt and handoff

`python <Wave>/prose-delta/check.py <Repo>` completed with exit **0** in
**0.256 s**, at `2026-09-16T02:32:57.436453Z`. This is a shared read-only
comparison, not extra native execution or a second per-chapter run.
`Wave` is `RunRoot/verify-core-wave`; `Repo` is the book checkout.
The original **78 invocations / 241.350 s** and previous reuse counts,
raw outputs, negative assertions, and source-specific records are intact.

Receipts are `Wave/prose-delta/check.json`, `ch04-source.html`,
`ch04-source.diff`, and `ch04-report-before.md`. The original
`Wave/verification-status.json` still describes the initial source;
this dated delta supersedes only that source's chapter-claim blockers.

**Remaining mandatory Chapter 4 corrections: none within this gate.**
The author supplied the prose/comment edits. This verifier changed only
the two requested reports and raw receipts, not chapter code, fixtures,
root dependencies, metadata, or Chapter 5. There is no broader research,
new runtime assurance, or reviewer acceptance in this closure.

---

## Original independent record — retained; chapter-claim blockers superseded above

The following verdict, source hash, line anchors, and pending corrections
describe the originally tested revision. Its underlying CLI failures
remain valid, with the complete diagnostics and execution record preserved.

**Verdict: FAIL pending minimal visibility/provenance corrections.**
The main local-instruction example, its native projections, pinned Git
fragment, MCP configuration fragment, registry fragment, and author-only
tooling example work within their stated input scopes. The local
skill-subset fixture and a coupled two-layout control have real CI-audit
failures that must not acquire an audit-clean guarantee. The opening
evidence alias also contains a workstation-specific path to remove.

No chapter, fixture, lockfile, root dependency, site, or edition metadata
was edited. No broad prose rewrite or new research wave is requested.

## Source identity and exact CLI

| Item | Value |
| --- | --- |
| Chapter | `content/chapters/the-manifest-apm-yml.html` |
| Source SHA256 | `4aa890b23b5a25ea7c2557e78040605ad3df28e040c6cffef628411a6937cada` |
| Current target/executed CLI | Exactly **0.31.0** |
| Execution date | 2026-09-16 UTC |
| Code blocks | **13**, individually accounted for below |
| Historical boundary | Original scaffold, Meridian manifest, and transcript remain **0.23.1** |

Aliases: `RunRoot` = orchestrator's session `files/book-v1.2`;
`Wave`/`N` = `RunRoot/verify-core-wave`; `Prior`/`R` =
`RunRoot/verify-ch05`; `ProbeInputs` = `RunRoot/core-probes/projects`;
`Core`, `Operations`, `Producer` are the corresponding directories under
`backend/examples/updates/1.2`. `Scratch` is the new owned short root
recorded in `Wave/runtime-layout.json`.

All table commands are exact arguments after:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

Executable SHA256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
New batches checked the exact banner before examples. They used the
absolute executable, normal short CWDs, isolated HOME/cache/config/temp/
credentials, and no `--root` redirection. No host/global configuration,
credential helper, inherited token, or root authoring dependency was used.
Experimental registry settings changed **only disposable batch homes**.

This report shares the four-chapter **78-invocation / 241.350 s** delta
wave: 9 version guards, 7 help commands, 62 example/control commands.
The original explorer and Ch5 suites were not rerun. **53 independently
executed Ch5 records and 13 original version guards** were read and
cross-checked instead; see `Wave/reuse-evidence.json`.

## Every code block: status, origin, and input scope

All current CLI evidence in this table is **0.31.0**. “R” means retained
independent Ch5 execution, not an explorer observation. Exact command
exits/runtimes follow the table.

| Example ID / chapter path | Status | New vs reused / exact input scope |
| --- | --- | --- |
| `#ch4-init-historical` | **PASS — preservation only**, original 0.23.1 | No current execution of the annotated `acme-agents` block; current plain-init field set checked separately with R `discover2-plain-init` |
| `#ch4-git-source` | **PASS** | R exact dependency subtree of `Core/pinned-skill/apm.yml`, including `mcp: []`; full fixture executed, not a fabricated Git+MCP composite |
| `#ch4-local-source-selection` | **FAIL for coupled CI audit**; install assertion passes | N exact `ProbeInputs/path-options/apm.yml` and its four companion plugin/skill files; install 0, audit 1; F4.1 |
| `#ch4-registry-source` | **PASS, complete-fixture scope** | N exact registry mapping and first dependency of `Operations/registry`; full three-entry manifest/server used, not the fragment alone |
| `#ch4-mcp-shape` | **PASS, configuration-only** | N exact `dependencies` subtree of `Operations/mcp/apm.yml`; no Git dependency, server, or harness execution |
| `#ch4-dev-dependencies` | **PASS** | N complete `Producer/dev-only` authored input, including `.apm/skills/ship`, `tool/apm.yml`, and its dev-only skill; install/audit/pack 0 |
| `#ch4-meridian-manifest-historical` | **PASS — preservation only**, original 0.23.1 | No fresh CLI stamp or execution of the historical recording |
| `#ch4-current-manifest` | **PASS** | R exact `Core/local-instruction/apm.yml` plus authored instruction, starting without a lock/generated files |
| `#ch4-local-instruction` | **PASS, exact shared-fixture evidence** | R same original instruction bytes; dual historical/current caption is supported by the independently executed canonical fixture, not a new run here |
| `#ch4-install-historical` | **PASS — preservation only**, original 0.23.1 | Original transcript wording/timing retained; no current-output promise |
| `#ch4-current-install` | **PASS** | R exact `["install"]` with the stated source-only Core input |
| `#ch4-claude-projection` | **PASS** | R actual native output; display CRLF normalizes to native LF, plus the omitted final newline only |
| `#ch4-cursor-projection` | **PASS** | R actual native output, including quoted description; old Cursor bytes/hash not substituted |

Historical code content matches Git HEAD after only checkout EOL conversion.
Those preservation PASS labels have **no current CLI exit/runtime** and do
not certify the old illustrative/annotated inputs under the new version.

## Main example and projections — independent evidence reused

The complete canonical Core input/lock bytes equal
`Prior/canonical-core.zip`. The first-install before-inventory contains
only the two authored files. Exact argv, original raw stdout/stderr,
preceding version guard, output snapshots, and subsequent input continuity
were checked, rather than trusting a matching filename or explorer caption.

| Input/output | SHA256 |
| --- | --- |
| `Core/local-instruction/apm.yml` | `60102cbbe3d3d0fbdf2e7cce6c3d3c6bab11d5605583947f77086cddcd00c934` |
| Authored `.apm/instructions/meridian-checkout.instructions.md` | `29e9848b2a7463c34fa57e1dbd65caf7f3a1d23dd61df107f11ed73653facfad` |
| Complete lock | `0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa` |
| Native Claude rule | `3f8ff5771908aa7f602fd6279a2ff775b54613d1c9fc44b4b1dcc31c6ead5be1` |
| Native Cursor rule | `a468f35842275baf34baaba82bf986b6d84aefb28da78ecdc1d32690fde538fa` |

The displayed manifest and authored instruction equal the canonical input
bytes after adding only their omitted terminal newline. Native projections
were compared to the **actual** independent snapshot, not regenerated in
Python. Copilot retains the instruction metadata; Claude has `paths` and
no description; Cursor has `globs` and the quoted description. The chapter
does not promise raw cross-harness or source-CRLF/output-LF byte identity.

| R record ID | Exact command | Exit | Original seconds |
| --- | --- | ---: | ---: |
| `local-local-instruction-install` | `install` | 0 | 4.584 |
| `local-local-instruction-restore` | `install` | 0 | 2.007 |
| `local-local-instruction-frozen` | `install --frozen` | 0 | 2.429 |
| `local-local-instruction-audit` | `audit --ci` | 0 | 3.031 |
| `public-pinned-skill-install` | `install` | 0 | 8.574 |
| `public-pinned-skill-restore` | `install` | 0 | 3.148 |
| `public-pinned-skill-frozen` | `install --frozen` | 0 | 2.969 |
| `public-pinned-skill-audit` | `audit --ci` | 0 | 2.896 |
| `cold-frozen` | `install --frozen` | 0 | 10.335 |
| `cold-audit` | `audit --ci` | 0 | 2.544 |

The local lock has `dependencies: []`, three canonical deployment rows,
and compatible `local_deployed_*` fields; it omits `generated_at` and
`apm_version`. `.gitignore` receives `apm_modules/`.

Git input is only the pinned `style-checker` subpath, not the sample's
whole/floating transitive graph. Manifest SHA256:
`345bd03e5b24af37425cffe624cf8d3ebafff7e60b061b7af1288de7ce65162b`;
complete lock SHA256:
`6b9ebb9ddcba38e6eddae38ca0c3658c2fabeee90e279857c9159f149ba09507`.

## F4.1 — local skill selection installs, but CI audit fails

**Example:** `#ch4-local-source-selection`;
`ProbeInputs/path-options/apm.yml`.
**CLI:** 0.31.0. **Status:** **FAIL for audit**, not a network skip.

Starting source is exactly the shown complete manifest plus:

```text
pkg/plugin.json
pkg/skills/kept/SKILL.md
pkg/skills/unlisted/SKILL.md
pkg/extra/custom/SKILL.md
```

There is intentionally **no `pkg/apm.yml`** in this supported legacy-plugin
install input. No manifest/lock was added or patched to manufacture green
audit output.

| N record ID | CWD | Exact command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `decl-path-options-install` | `Scratch/p/ps` | `install` | 0 | 1.864 |
| `decl-path-options-audit` | Same project | `audit --ci` | **1** | 1.868 |

Install resolves alias `scoped-skills`, deploys **only**
`.claude/skills/kept/SKILL.md`, and creates neither Copilot/shared skills
nor the unselected Claude skills. That narrow selection claim passes.

Exact audit failure wording follows; only the owned absolute scratch-root
prefix is replaced by `<Scratch>`. Full unmodified native bytes are in
`N/logs/decl-path-options-audit.*`.

```text
  config-consistency details:
    - ./pkg: package manifest not found at <Scratch>\p\ps\pkg\apm.yml; re-run 'apm install' to restore it

[x] 1 of 8 check(s) failed
```

Stderr:

```text
[>] Replaying install (cache-only)...
[+] Replayed 1 package(s)
[>] Diffing scratch vs working tree...
[+] No drift detected
```

**Diagnosis/owner:** legacy-plugin intake without a source `apm.yml` is
accepted by install but rejected by audit's config-consistency check —
`apm-cli-explorer` / upstream. `chapter-author` owns the disclosure.

The “not an audit-clean” qualification is currently **only in an HTML
comment**, line 373. The rendered caption, lines 377–380, disclaims
runtime loading but not this audit failure. Add a visible, precise
limitation. Alternatively, an author-chosen corrected companion fixture
must receive its own input-equivalent verification; do not transfer the
different metadata-only control's PASS to this fixture.

## Other declaration, schema, and target controls

| Origin / record ID | Exact command | Exit | Seconds |
| --- | --- | ---: | ---: |
| N `decl-metadata-legacy-install` | `install` | 0 | 2.348 |
| N `decl-metadata-legacy-audit` | `audit --ci` | 0 | 2.161 |
| N `decl-undeclared-skill` | `install --skill not-declared` | **1, expected** | 2.577 |
| N `decl-legacy-empty` | `install` | 0 | 2.633 |
| N `decl-legacy-missing` | `install` | **1, expected** | 2.422 |
| N `final-omitted-skills-install` | `install` | 0 | 5.185 |
| N `final-omitted-skills-audit` | `audit --ci` | 0 | 5.262 |
| N `decl-empty-targets` | `install --dry-run` | **2, expected** | 1.799 |
| N `decl-conflicting-targets` | `install --dry-run` | **2, expected** | 1.627 |
| N `decl-git-version-key` | `install --dry-run` | **1, expected** | 2.299 |
| N `decl-legacy-manifest-all` | `install` | **2, expected** | 2.017 |
| R `ownership2-four-target-install` | `install` | 0 | 8.905 |
| R `ownership2-four-target-audit` | `audit --ci` | **1, known limitation** | 7.583 |
| R `control-no-marker-install` | `install` | 0 | 5.954 |
| R `control-no-marker-audit` | `audit --ci` | 0 | 5.485 |

The new metadata-only legacy control confirms explicit `kept`/`custom`
declarations and exclusion of `unlisted`; omission allows conventional
`kept`/`unlisted` discovery, while an empty declaration deploys none.
The invalid-selection diagnostic names `Available: custom, kept`.
Its project bytes are unchanged; two cache-file mtimes change, so no
universal no-write/mtime promise is inferred.

Schema negatives use fresh scratch copies with only the named manifest
change. Exact diagnostic excerpts:

```text
Error: [x] 'targets:' in apm.yml is empty
Error: [x] Cannot use both 'target:' and 'targets:' in apm.yml
Git dependency field 'version' is unsupported; use 'ref' for a branch, tag, or commit
Error: [x] No harness detected
```

The last follows the warning that manifest `all` makes the **whole field**
act as omitted, including a valid sibling target. All four negatives
preserve project hashes and mtimes; no invalid manifest was activated.

The eligible APM-versus-plugin input equals the original independent
`ProbeInputs/apm-over-plugin` before-state. Its install classifies
`apm_package` and ignores plugin-only command content, but its audit
still reports:

```text
    - unintegrated: .claude/commands/legacy-command.md
    - unintegrated: .cursor/commands/legacy-command.md
    - unintegrated: .github/prompts/legacy-command.prompt.md
[x] 1 of 10 check(s) failed
```

This is the already recorded [Ch5 F2 limitation](ch05-verification.md),
not an audit-clean precedence fixture. The marker-free control is
separate and byte-identified; no original failure was erased.

## Registry, MCP, and author tooling — new independent execution

| N record ID | Input / CWD under `Scratch/p` | Exact command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `reg-feature-disabled` | Complete `Operations/registry`, `rg` | `install` | **1, expected** | 2.130 |
| `reg-enable` | Isolated registry HOME | `experimental enable registries` | 0 | 1.746 |
| `reg-install` | `rg`, literal loopback endpoint | `install` | 0 | 2.821 |
| `reg-audit` | Same project | `audit --ci` | 0 | 2.104 |
| `reg-view-routed` | Same default-registry project | `view operations/exact versions` | 0 | 2.567 |
| `reg-disable` | Isolated registry HOME | `experimental disable registries` | 0 | 2.179 |
| `final-enable-registries` | Separate isolated HOME, `gr` | `experimental enable registries` | 0 | 3.944 |
| `final-explicit-git-install` | Pinned Git fixture + registry default, `gr` | `install` | 0 | 11.315 |
| `final-explicit-git-audit` | Same new input | `audit --ci` | 0 | 5.122 |
| `final-disable-registries` | Separate isolated HOME | `experimental disable registries` | 0 | 3.342 |
| `mcp-root-config-install` | Complete `Operations/mcp` manifest, `mc` | `install` | 0 | 15.883 |
| `mcp-root-config-audit` | Same project | `audit --ci` | 0 | 2.355 |
| `pack-dev-install` | `Producer/dev-only` authored files, `dv` | `install` | 0 | 2.002 |
| `pack-dev-audit` | Same project | `audit --ci` | 0 | 1.793 |
| `pack-dev-pack` | Same project | `pack` | 0 | 1.657 |

**Registry fragment:** mapping and first dependency equal the complete
Operations fixture; two range entries, identity, targets, and includes
are intentionally omitted in the chapter. The fixture server actually
ran at `http://127.0.0.1:18431`. All requests were anonymous and the
server has no publication endpoint. A disabled feature fails before
project writes; a configured default routes shorthand queries to
registry versions. Explicit Git under that default used real public Git,
made **zero** registry requests, and produced the canonical Git lock.
This different configuration received new execution, not a reused
no-registry PASS. Detailed reporting controls are in
[Ch2 verification](ch02-verification.md).

**MCP fragment:** the complete input has one deliberately nonexistent
server command, no APM package dependency, and explicit Copilot/VS Code/
Claude targets. Correct native paths, containers, arguments, and MCP-only
lock were inspected. Identity lookup used only process-local
`MCP_REGISTRY_URL=https://127.0.0.1:9` with two-second connection/read
limits, allowing the CLI's existing name-comparison fallback. No server
or harness ran and no TLS validation was disabled. This clean
configuration-only audit is not a native-MCP-byte or health guarantee;
the separate nested-MCP failure is retained in
[Ch3 verification](ch03-verification.md#f31--withheld-depth-two-mcp-is-not-audit-clean).

**Dev fixture:** the code block plus terminal newline equals the
canonical manifest bytes, SHA256
`c21b17a48b1fc72a0a3fc916965fee76b43a2babe9e1443e5e8f558c07f1b5dc`.
`license: MIT` parses. Both `ship` and `dev-only` are installed for the
author; CI audit succeeds. Literal no-flag `pack` writes a **directory**
`build/dev-boundary-1.0.0`, not a ZIP. Its complete contents are the
generated plugin manifest, embedded real lock, and `skills/ship/SKILL.md`;
the author-only skill is absent. No archive round-trip or consumer runtime
is claimed. The embedded lock still retains development provenance marked
`is_dev: true`; payload exclusion does **not** mean that every mention of
the dev dependency disappears from bundle metadata.

## Includes: installation versus packing, with the audit split retained

| N record ID | Exact input | Exact command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `decl-includes-install` | `ProbeInputs/includes-list`, only manifest + two instructions | `install` | 0 | 4.073 |
| `decl-includes-audit` | Same six native rule outputs | `audit --ci` | 0 | 2.837 |
| `pack2-source-install` | Fresh Producer/local-bundle authored source + competing root skill | `install` | 0 | 4.165 |
| `pack2-source-audit` | Same combined-layout project | `audit --ci` | **1** | 2.346 |
| `pack2-auto-layout-pack` | Same combined-layout project, `includes: auto` | `pack -o selected --verbose` | 0 | 1.926 |
| `pack2-pe-pack` | Fresh authored sources, `includes: [skills/unlisted]` | `pack -o selected --verbose` | 0 | 2.034 |
| `pack2-px-pack` | Fresh authored sources, `includes: [skills/missing]` | `pack -o selected --verbose` | **1, expected** | 2.278 |

The install-list control deploys both instructions across all three
targets despite listing only one. It audits cleanly.

Packing controls are **new executions**, not reused producer explorer
stamps. They copy only `Producer/local-bundle` authored files (not its
lock or prior generated output) and the exact
`producer-probes/materialized/l/skills/unlisted/SKILL.md` source.
With `auto`, the bundle directory contains the `.apm` instruction,
prompt, and skill, not the extra root skill. The explicit list ships
only the named root skill. Missing listed source exits 1 before any
project-byte or mtime change:

```text
Error: includes path 'skills/missing' does not exist. Fix the path in apm.yml or create it.
```

### F4.2 — the competing-layout control is not audit-clean

**Status: FAIL**, CLI **0.31.0**, `audit --ci` exit **1**, **2.346 s**.
Install and the separately asserted pack selections work; the coupled
audit replays a different skill selection:

```text
  drift details:
    - unintegrated: .agents/skills/unlisted/SKILL.md
    - unintegrated: .claude/skills/unlisted/SKILL.md
    - orphaned: .agents/skills/secure-payment-review/SKILL.md
    - orphaned: .claude/skills/secure-payment-review/SKILL.md

[x] 1 of 10 check(s) failed
```

Exact full output is `N/logs/pack2-source-audit.*`.
Diagnosis/owner: combined `.apm`/root-skill install and audit replay
disagree on source selection — `apm-cli-explorer` / upstream.
This is a **new narrow coupled-control result**, not an assertion that
the original producer probe had identical generated state. It is not
a network failure and does not invalidate the clean one-instruction
Core fixture or the clean dev-only fixture.

Keep the correct operation-specific `includes` explanation, but make
this control's audit limitation visible if it remains the illustration
of coexisting source layouts. A successful pack is not a blanket
install/audit guarantee.

## Reused init, writer, target, and frozen boundaries

| R record ID | Exact command | Exit | Original seconds |
| --- | --- | ---: | ---: |
| `discover2-plain-init` | `init --yes` | 0 | 1.940 |
| `discover2-plain-overwrite` | `init --yes` | 0 | 1.991 |
| `discover2-inventory` | `init --discover --format json` | 0 | 3.959 |
| `discover2-apply` | `init --discover --apply --yes --format json` | 0 | 5.067 |
| `discover2-idempotent` | `init --discover --apply --yes --format json` | 0 | 4.963 |
| `targets2-local-add` | `install .\pkg --target copilot` | 0 | 4.399 |
| `targets2-local-add-restore` | `install` | 0 | 3.950 |
| `targets2-local-add-stable` | `install` | 0 | 3.337 |
| `targets2-local-add-audit` | `audit --ci` | 0 | 3.729 |
| `targets2-bootstrap` | `install .\pkg --target copilot` | 0 | 3.154 |
| `targets2-bootstrap-audit` | `audit --ci` | 0 | 2.839 |
| `mcp-direct-add` | `install --mcp checkout-probe --transport stdio --env 'VALUE=${CORE_MCP_VALUE}' -- apm-book-mcp-not-a-real-executable --probe` | 0 | 10.366 |
| `mcp-audit` | `audit --ci` | 0 | 5.850 |
| `frozenlocal-baseline-install` | `install` | 0 | 2.690 |
| `frozenlocal-new-local-frozen` | `install --frozen` | **0, documented exception** | 1.696 |
| `frozenlocal-new-local-audit` | `audit --ci` | 0 | 1.562 |
| `frozenlocal-missing-git-frozen` | `install --frozen` | **1, expected** | 1.780 |
| `boundaries-missing-lock` | `install --frozen` | **1, expected** | 6.193 |

These records retain exact original inputs, mutations, argv, native output,
and version guards. They support only their tested boundaries:

- Plain init writes one scaffold, with `author: Developer` in the
  credential/Git-config-isolated control, not the historical illustrative
  author. Plain init can overwrite; consented discovery/apply merges local
  references without moving the source.
- APM dependency addition preserves the tested comment/blank line/target
  style. The separate MCP path reserializes; the environment value was a
  deliberately public fixture value, never a host secret.
- Existing-manifest target override does not replace its target list;
  missing-manifest bootstrap can persist the flag.
- Newly declared local dependencies can deploy and rewrite the old lock
  under frozen mode. Missing Git/lock controls refuse. Original failed
  universal-refusal assertions in Ch5 are preserved, not silently changed.

Frozen-source receipts at
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` independently cross-check
required identity fields, optional metadata, MCP entry forms, reserved
`type`, implicit includes consent, and documented target precedence.
Support statements about other Git hosts and real harnesses are not
live integration tests.

## Mandatory author corrections / no broad changes

1. **F4.1, `#ch4-local-source-selection`:** move the audit limitation into
   visible prose/caption and name the missing `pkg/apm.yml`
   `config-consistency` error. Install selection remains a valid,
   narrowly verified assertion. Do not label the whole fixture audit-clean.
2. **F4.2, `#ch4-includes-boundary`:** disclose the combined-layout
   control's CI-audit drift limitation while preserving the correct
   install-versus-pack explanation. The clean local-instruction baseline
   remains distinct. No archive/runtime guarantee should be added.
3. **Opening evidence comment, line 14:** replace the absolute
   workstation-specific `RunRoot` value with the session-artifact alias
   used in the other chapters/reports. HTML comments also ship in
   published artifacts; do not expose a local user profile path.

Suggested owner for these minimal content changes: `chapter-author`.
Suggested owner for both actual audit discrepancies:
`apm-cli-explorer` / upstream. No subagent was dispatched.

**Skips:** no changed command was skipped for network. Public Git and the
anonymous loopback registry actually ran. Historical blocks, live MCP/
harness execution, private sources, server publication, and org-policy
authority are not freshly certified. Baseline audit output explicitly
may skip org enforcement when no Git remote identifies an organization;
the policy bypass/fetch-failure limitations in the operations reference
were not replaced with a PASS guarantee.

Verifier-only corrections: the first pack inspection incorrectly expected
a ZIP from no-flag `pack`; its directory output was inspected without
rerunning that command. Diagnostic wording/mtime assertions were corrected
read-only. Original logs and failed verifier assertions remain under
`Wave/assertion-delta/`; the three actual native audit failures remain FAIL.

All 78 new raw-record snapshots/output-byte hashes and chapter/fixture/
protected-file hashes were checked at native-evidence finalization.
A later unrelated TOC change is recorded in the
[shared handoff note](ch01-verification.md#artifacts-and-handoff); the
chapter, executable fixture inputs, and root APM dependencies are unchanged.
Full inputs, generated locks,
native commands/exits/runtimes, mutations, source receipts, and snapshots
are under `Wave`; original independent evidence is untouched.

**Minimal fixes applied to book content: none.** Stop for the small author
corrections above. If only disclosures/comments change, compare the new
source hash and unchanged code/fixture bytes against these retained records;
do not repeat the full 111+/143-probe suites.
