# Chapter 10 independent verification — book 1.2 / APM 0.31.0

**Chapter claim/recipe verdict: PASS, with documented CLI FAILs retained.**
The new producer recipes and their stated negative outcomes were independently
executed. Native-plugin CI replay and legacy Copilot shared-skill delivery are
still **FAIL**, not successful compatibility tests or network skips. The chapter
already describes both defects accurately. **Reviewer acceptance is pending.**

| Source identity | Value |
| --- | --- |
| Chapter | `content/chapters/becoming-a-producer.html` |
| **Final chapter SHA-256** | **`250ba7641d1e9af6f1633f723eacdebfd82e9a93ea5af66598bf89e084c61b75`** |
| Execution date | 2026-09-16 UTC |
| Frozen target | Exactly **APM 0.31.0**, not latest |
| Previous edition evidence | Book 1.1 / APM 0.23.1; historical stamps unchanged |
| Source commit | `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` |
| Book/code fixes | **None** |

## Environment, independence, and evidence

```powershell
$RunRoot = 'C:\Users\masalnik\.copilot\session-state\2d4facdd-cd43-4bef-9f47-dc669687d65a\files\book-v1.2'
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
```

Executable SHA-256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
The prepared Windows archive also matched its publisher sidecar:
`a5b2b46378f560b3a2c4ff0c8a5e027cb851c5220ca8a31f9a44f9667ddb0f01`.
No installer, global upgrade, registry upload, or agent runtime was invoked.

**VerifyRoot** = `RunRoot\verify-ch10-ch12`.
**Scratch** = `C:\Windows\Temp\v12-zwwo0gts`.
**P** = `Scratch\p`.
**Producer** = `backend/examples/updates/1.2/producer`.
These aliases bind every abbreviated CWD/command below; native logs contain the
fully expanded executable, arguments, and CWD. The initial help-only batch used
a separate profile-temp root; materialization used the short root above.

Each execution batch checked the exact banner and executable digest first.
Child environments allowlisted OS/Git essentials and used separate
HOME/USERPROFILE, APM/config/cache/application-data/temp paths. Git system/global
configuration and credential helpers were isolated; neither `gh` nor agent
runtimes were on the child PATH. Public Git acquisition was anonymous. Local
batches also used unavailable loopback HTTP/HTTPS proxies; their successful
results did not require those transports. No host token was collected or echoed.

The **combined Ch10–12 logged run** contains **136 native invocations**:
20 version guards, 13 help inspections, and 103 example/control commands,
including a retained verifier-authored invalid control. Summed native runtime:
**784.094 s**; no timeouts. This is not elapsed time or a benchmark. An initial
banner inspection preceded the logged batches. This was a scoped independent
suite, **not replay of the explorer's 131-command runner**.

No older execution is used to turn a new producer input green. Ch5 equivalence
was examined independently; literal launcher/line-ending code hashes differ,
so even Ch11's shared two-command recipe was rerun. Explorer records informed
test selection, never the independent PASS result.

### Durable artifacts

| Under VerifyRoot | Evidence |
| --- | --- |
| `sources/ch10-blocks.json`, `sources/becoming-a-producer.html` | Exact captured source; 20 pre/code blocks, raw and decoded SHA-256s |
| `source-probe-map.json` | Every source code ID mapped to status and independent records; includes four inline `ch10-ex11-metadata-gates/command-N` IDs |
| `logs/<id>.json`, `.txt`, `.stdout.bin`, `.stderr.bin` | Exact command/CWD/exit/runtime, original output bytes, project hashes and mtimes before/after |
| `command-index.json`, `.csv`, `verification-status.json` | Complete command ledger and per-example tags |
| `inputs/`, `snapshots/`, `final-projects.zip` | Actual input bytes, genuine generated locks, archives, and deployments |
| `assertions/*inventory*.json`, `*raw-zip.json`, `zip-consumer.json` | Payload hashes, raw ZIP members, and eight-file native inventory |
| `mutations/`, `batches/`, `assertions/` | Explicit scratch-only negative controls and retained failed verifier assumptions |
| `final-source-checks.json`, `summary.json` | Final chapter identities; unchanged canonical/historical fixtures and protected metadata/root dependencies |

The chapter's four current complete producer manifests match their canonical
fixtures as YAML; raw source/code/fixture hashes are recorded separately, not
claimed identical across HTML decoding and CRLF/LF. The CLI, not that YAML
comparison, accepted and materialized the projects.

## Per-example verification tags

Paths in this table are `Chapter#<id>` unless a fixture is named. A figure with
two blocks has `/code-1` (YAML) and `/code-2` (commands); one-block figures have
`/code-1`. Runtime totals include associated controls where listed in the
machine-readable map, exclude version/help guards, and overlap; do not sum them.

| Example ID / input | Status | CLI evidence | Runtime (s) |
| --- | --- | --- | ---: |
| `ch10-ex01-source-tree` | PASS historical source inventory only | Historical 0.23.1; no new tree transcript | 0 |
| `ch10-ex02-manifest-history` | PASS preserved snapshot; unchanged package accepted in current routing control | Historical stamp retained; current control 0.31.0 | 4.159 |
| `ch10-ex03-plugin-json-history` | PASS JSON-equivalent generated metadata | Historical stamp retained; current control 0.31.0 | 3.257 |
| `ch10-ex04-manifest-only-pack` — historical Meridian copy | **PASS** | 0.31.0 | 11.945 |
| `ch10-ex05-dev-only` — `Producer/dev-only` | **PASS**, actual skill payload excluded; embedded dev metadata is not erased | 0.31.0 | 20.861 |
| `ch10-ex06-plugin-init` | **PASS**, two separate empty directories | 0.31.0 | 5.592 |
| `ch10-ex07-agent-plugin-pack` — `Producer/portable-plugin` | **PASS**, strict output and expected Meridian refusal | 0.31.0 | 19.754 |
| `ch10-ex08-native-registration` | **FAIL native CI audit**, visibly documented; registration PASS | 0.31.0 | 24.364 |
| `ch10-ex09-marketplace-init` | **PASS** scaffold, not placeholder resolution/publication | 0.31.0 | 7.808 |
| `ch10-ex10-marketplace-gates` — `Producer/marketplace` | **PASS**, including expected drift/path failures | 0.31.0 | 50.327 |
| `ch10-ex11-metadata-gates` — `Producer/metadata-offline` | **PASS** expected `0/5/4/5` | 0.31.0 | 10.506 |
| `ch10-ex12-registry-preview` — `Producer/registry-preview` | **PASS local preview**; live backend SKIPPED-needs-network | 0.31.0 | 73.704 |
| `ch10-ex13-local-bundle` — `Producer/local-bundle` | **PASS**, real directory and ZIP | 0.31.0 | 19.935 |
| `ch10-ex14-zip-consumer` | **PASS**, genuine archive consumed; eight native files and audit | 0.31.0 | 44.294 |
| `ch10-ex15-declared-git` — `Producer/pinned-bundle` | **PASS**, actual immutable public Git acquisition | 0.31.0 | 56.778 |
| `ch10-ex16-meridian-return-history` | **SKIPPED-needs-network**, fictional/private Meridian Git source and permission unavailable | Historical 0.23.1, not restamped | 0 |
| Verifier ID `ch10/ch11-legacy-shared-skill` | **FAIL**, requested skill absent despite two exit-0 commands | 0.31.0 | 8.750 |

The source/probe map binds the chapter's producer probe names to the independent
records below. Names such as `meridian-install`, `local-bundle-archive`,
`native-bundle-audit`, and `action-cli-pack-apm` remain *explorer provenance* in
the chapter, not names of new independent executions.

## Exact current commands and exits

Commands are the exact arguments following `& $Apm`. Sequences within a cell
are ordered; the corresponding exit list is ordered identically. Every
individual duration and full command is in `command-index.json`.

| Independent record(s) | CWD | Exact command(s) | Exit(s) |
| --- | --- | --- | --- |
| `local-history-{install,preview,pack}` | `P/h` | `install`; `pack --dry-run --verbose`; `pack --archive -o dist --verbose` | `0 / 0 / 0` |
| `local-history-audit` | `P/h` | `audit --ci` | `0` |
| `authority-dev-{install,audit,pack}` | `P/d` | `install`; `audit --ci`; `pack` | `0 / 0 / 0` |
| `native-scaffold-s1` | `P/s1` | `plugin init --yes --target copilot` | `0` |
| `native-scaffold-s2` | `P/s2` | `plugin init --yes --target copilot --format agent-plugin` | `0` |
| `native-portable-{lock,pack}` | `P/n` | `lock`; `pack --format agent-plugin --verbose` | `0 / 0` |
| `native-portable-source-{install,audit}` | `P/n` | `install`; `audit --ci` | `0 / 0` |
| `native-plugin-alias` | `P/n` | `pack --format plugin -o alias` | `0` |
| `local-resume-meridian-strict-rejection` | `P/b` | `pack --format agent-plugin -o rejected` | **`1` expected** |
| `native-native-{install,audit}` | `P/nc` | `install`; `audit --ci` | **`0 / 1`**, actual audit FAIL |
| `native-native-imperative-rejected` | `P/ni` | `install 'C:\Windows\Temp\v12-zwwo0gts\p\n\build\portable-review-1.0.0' --target copilot` | **`1` expected** |
| `native-metadata-{install,audit}` | `P/nm2` | `install`; `audit --ci` | **`0 / 1`**, actual audit FAIL |
| `catalog-init` | `P/mi` | `marketplace init --name meridian-marketplace --owner meridian-finance` | `0` |
| `catalog-{generate,check}` | `P/m` | `pack --offline --strict-metadata`; `pack --offline --check-clean` | `0 / 0` |
| `catalog-drift` | `P/m` | `pack --offline --check-clean` after harmless catalog-name edit | **`4` expected** |
| `catalog-override-missing` | `P/m` | `pack --offline --check-clean --marketplace-path claude=alternate/marketplace.json` | **`4` expected** |
| `catalog-mixed-{generate,check,no-zip-check}` | `P/mm` | `pack --offline --archive`; then twice `pack --offline --check-clean --force --archive`, second check after deleting the ZIP | `0 / 0 / 0` |
| `catalog-dot-path-rejected` | `P/mdot` | `pack --offline --strict-metadata`, output path changed to `./catalog/marketplace.json` | **`1` expected** |
| `catalog-metadata-preview` | `P/mo` | `pack --offline --dry-run --json` | `0`, uncertifiable |
| `catalog-metadata-strict` | `P/mo` | `pack --offline --strict-metadata --json` | **`5` expected** |
| `catalog-metadata-clean` | `P/mo` | `pack --offline --check-clean --json` | **`4` expected** |
| `catalog-metadata-strict-clean` | `P/mo` | `pack --offline --strict-metadata --check-clean --json` | **`5` expected** |
| `registry-{enable,install,preview,disable}` | `P/r` | `experimental enable registries`; `install`; `publish --package book-fixtures/review --dry-run`; `experimental disable registries` | `0 / 0 / 0 / 0` |
| `registry-{manifest-gate,publish-gate}` | `P/r`, feature initially disabled | `install`; `publish --package book-fixtures/review --dry-run` | **`1 / 1` expected** |
| `registry-{frozen,audit}` | `P/r`, feature enabled | `install --frozen`; `audit --ci` | `0 / 0` |
| `local-bundle-{install,audit,preview,directory,archive}` | `P/b` | `install`; `audit --ci`; `pack --dry-run --verbose`; `pack --verbose`; `pack --archive -o dist --verbose` | `0 / 0 / 0 / 0 / 0` |
| `local-resume-zip-init` | `P/z` | `init --yes --target copilot,claude,cursor` | `0` |
| `local-resume-zip-install` | `P/z` | `install 'C:\Windows\Temp\v12-zwwo0gts\p\b\dist\meridian-standards-1.0.0.zip' --target copilot,claude,cursor` | `0` |
| `local-resume-zip-audit` | `P/z` | `audit --ci` | `0` |
| `local-resume-zip-no-flag-{init,install}` | `P/zt` | `init --yes --target copilot,claude,cursor`; `install 'C:\Windows\Temp\v12-zwwo0gts\p\b\dist\meridian-standards-1.0.0.zip'` | `0 / 0`, Copilot only |
| `local-resume-source-{add,audit}` | `P/hs`, historical source copied into `pkg` | `install ./pkg`; `audit --ci` | `0 / 0` |
| `local-resume-runtime-local-pack-rejected` | `P/hs` | `pack` | **`1` expected**, runtime local dependency |
| `public-{install,frozen,audit,pack}` | `P/g` | `install`; `install --frozen`; `audit --ci`; `pack --archive --json` | `0 / 0 / 0 / 0` |

### Source selection and attestation controls

- `authority-resume-authority-install` / `source-layout`, `P/a`: `install`,
  `pack` → **0/0**. With both `.apm/` and root `skills/unlisted`, pack chose
  `.apm/`; the unlisted root skill was absent.
- `authority-resume-includes-exhaustive`: `pack -o only` → **0** after setting
  `includes: [skills/unlisted]`; only that skill plus plugin/lock metadata
  shipped. `includes-missing`: `pack -o missing` → **1**, no file/hash/mtime
  changes, for `includes: [skills/missing]`.
- `authority-resume-reserved-type-{install,pack}`: `install`,
  `pack -o reserved` → **0/0** with `type: prompts`; all three primitive kinds
  survived. `source-not-deployment`: `pack -o fresh-source` → **0**; an ASCII
  source marker entered the command while the old deployed prompt was unchanged.
- `authority-resume-includes-install`, `P/ai`: `install` → **0** with only one
  of two instructions listed. The other instruction still deployed to all
  three targets. This is an independently authored control, not reuse of a
  similarly named core explorer result.
- `public-tamper-claude-plugin`: `pack --format claude-plugin -o bad-claude-plugin`
  → **1**. `public-resume-tamper-agent-plugin`:
  `pack --format agent-plugin -o bad-agent-plugin` → **1**.
  Both refused the altered attested skill before project writes. Exact error:

```text
Error: Cannot pack dependency microsoft/apm-sample-package: installed file '.agents/skills/style-checker/SKILL.md' does not match the hash recorded in apm.lock.yaml. The installed copy may be stale or tampered. Run 'apm install' to restore attested content, then pack again.
```

- `public-resume-missing`: `pack -o bad-missing` → **1** after deleting the
  attested file. `public-resume-cache-not-authority`:
  `pack -o cache-control` → **0** with a clean deployed file but altered cached
  skill; packed bytes equaled the original export, not the altered cache.
- `integrity-{tampered,extra,missing}`, CWDS `P/itc`, `P/iec`, `P/imc`:
  `install 'C:\Windows\Temp\v12-zwwo0gts\p\<it|ie|im>' --target copilot,claude,cursor`
  → **1/1/1**. These are three real bundle copies, each with one controlled
  payload mutation and an untouched embedded lock. Consumers remained empty.

All negative fixtures and exact diagnostics are retained, including the
unmodified genuine locks. No attestation failure was “fixed” by editing a lock.

## Genuine ZIP, native inventory, and declarative replay

First Meridian ZIP SHA-256:
`0a649a9a90caf41b4047d97eb19bc231f7b9a3bd33472e559190cc5c7f5a7de7`.
Its **complete raw file inventory** has one `meridian-standards-1.0.0/` wrapper:

| Member beneath that wrapper | Bytes |
| --- | ---: |
| `apm.lock.yaml` | 2911 |
| `plugin.json` | 229 |
| `commands/checkout-review.md` | 521 |
| `instructions/meridian-engineering.instructions.md` | 516 |
| `skills/secure-payment-review/SKILL.md` | 771 |

Every payload SHA-256 was recomputed and equaled `pack.bundle_files`; the lock
does not hash itself. The generated directory has the same three primitives.
The producer's root lock remained
`2b906800526ba3942b583d75db6057551e9101447e733be60ef41a7beb66fe07`.
By contrast, the unchanged historical manifest produced only
`.github/plugin/plugin.json` and `.claude-plugin/plugin.json`: **no ZIP**.

`P/z` contained exactly these **eight distinct native files**, not just an
exit-0/copy-counter assertion:

```text
.github/prompts/checkout-review.prompt.md
.github/instructions/meridian-engineering.instructions.md
.agents/skills/secure-payment-review/SKILL.md
.claude/commands/checkout-review.md
.claude/rules/meridian-engineering.md
.claude/skills/secure-payment-review/SKILL.md
.cursor/commands/checkout-review.md
.cursor/rules/meridian-engineering.mdc
```

Its manifest bytes were unchanged by imperative ZIP install. The genuine
consumer lock has empty `dependencies`, these `local_deployed_files` and hashes,
and `local-bundle` ownership. It is **not a declared archive dependency**.
The no-install-target control produced only the Copilot/shared files despite
three manifest targets. The separate local-source add retained `./pkg`.

The public Git example resolved exactly
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`, one `claude_skill` virtual slice,
`version: unknown`, and package content hash
`sha256:867912713bf45048211440b81ea0ced396ad0a0993447dd540fe5c219722d318`.
The complete root lock matched the canonical
`379bce78204582002c4070fb666c973a4194a131fb6afa0df31ebe819c542429`.
`pack --archive --json` really wrote `build/pinned-bundle-1.0.0.zip` while
reporting `"bundle": null`; no synthetic corrected JSON was substituted.

Repeated packing (`pack --archive -o repeat --verbose`, exit **0**) preserved
payload bytes but changed `packed_at` and ZIP metadata; the second ZIP SHA-256
was `26e1929d504c9ea6b80769fb9ba3f8dd2f33be40c381c768302d1ab4ce8b5d69`.
The README's additional
`lock export --format cyclonedx --timestamp '2026-09-16T00:00:00Z' -o sbom.cdx.json`
also ran, exit **0**, **4.833 s**, producing CycloneDX 1.5. Neither result is
publisher authentication or an agent-runtime test.

## Actual FAILs — preserve in the chapter

### F10.1 Native CI replay — FAIL, owner `apm-cli-explorer` / upstream

`P/nc` used the exact displayed declaration and an unchanged generated strict
bundle. Install registered the whole plugin and created Copilot
marketplace/settings files, with no loose skill duplicate. `audit --ci`
exited **1**. Exact diagnostic details from stdout:

```text
    - ./pkg: package manifest not found at C:\Windows\Temp\v12-zwwo0gts\p\nc\pkg\apm.yml; re-run 'apm install' to restore it
    - Native Agent Plugin canonical IR is missing, so deployment was blocked. Use 'apm pack --claude-plugin' or ask the publisher for a legacy-compatible package.
```

The separately authored metadata-only source control `P/nm2` removed the
manifest-consistency complaint but still exited **1**, with:

```text
    - Native Agent Plugin canonical IR is missing, so deployment was blocked. Use 'apm pack --claude-plugin' or ask the publisher for a legacy-compatible package.
[x] 1 of 10 check(s) failed
```

Full stdout/stderr and original terminal formatting:
`logs/native-native-audit.*`, `logs/native-metadata-audit.*`.
**Diagnosis:** successful native registration does not establish local-path
canonical-IR audit replay. No drift suppression or packed-lock modification
was used. The chapter's diagnostic example is accurate; the CLI result is not
green.

Strict-format rejection was independently asserted as an expected negative,
not confused with this defect. Exact stderr:

```text
Error: Cannot pack Agent Plugin: non-portable primitives would be discarded (commands, instructions). Agent Plugins v1 portable components are limited to root plugin.json, skills/, and root mcp.json. Use 'apm pack --format claude-plugin' to preserve commands, instructions in the legacy Claude client format.
```

### F10.2 Legacy shared skill omission — FAIL, owner `apm-cli-explorer` / upstream

In `P/g`:
`pack -o legacy --format apm --target copilot --archive` → **0**, **4.630 s**.
In empty `P/gu`:
`unpack 'C:\Windows\Temp\v12-zwwo0gts\p\g\legacy\pinned-bundle-1.0.0.zip' -o .`
→ **0**, **4.120 s**.

Exact relevant stdout:

```text
[!] No files to pack for target 'copilot'
[i] Bundle target: copilot (0 dep(s), 0 file(s))
[!] No files were unpacked
```

The archive contained **only the embedded lock**, and the consumer remained
empty. Archive SHA-256:
`345994fd2185e20667ee13337a43ae7b772a7f1c155dc413a818ca48e86cb380`.
The requested `.agents/skills/style-checker/SKILL.md` was not delivered.
**Diagnosis:** legacy Copilot pack selection omits the shared skill path;
zero exits are not inventory success. See [Ch11 verification](ch11-verification.md)
for the separately successful pinned instruction pair. No plugin-format
“repair” was substituted for the pinned Action contract.

## Read-only gates, no-upload boundary, and limitations

- All catalog clean/drift/override/mixed checks preserved project file hashes
  **and mtimes**. Missing ZIP did not make a clean catalog fail or recreate it.
  Metadata failures named `metadata_incomplete` (**5**) and
  `marketplace_metadata_uncertifiable` (**4**); combined strict/clean returned
  **5** before comparison, not a network skip.
- Publish preview wrote a **flat** 628-byte ZIP containing only root `apm.yml`
  and `.apm/skills/review/SKILL.md`, SHA-256
  `7f16ba771e0190a60d2f16cfbbc11b0aa223dceabadba7fa0c3da152c64442a5`.
  Output explicitly said `(dry-run -- nothing uploaded)`. The pinned
  `commands/publish.py` returns before constructing the registry client on
  that branch. The feature was disabled again in the owned scratch home.
- **SKIPPED-needs-network:** real registry consume/publish lacks an authorized
  compatible backend and publication permission; the reserved fixture URL is
  not a service. Private Meridian publication/resolution likewise lacks a real
  authorized repository. Native runtime loading has no supplied configured
  Copilot CLI/session. All these limitations remain visible in the chapter.
- Source-grounded package-intake rules and target/runtime contracts were checked
  against the frozen sources; this run does not claim independent reexecution
  of every core/operations explorer control, global plugin-bin consent, or paid
  harness behavior.
- All **34** unique chapter link references resolved by local-file/fragment,
  pinned-source-object, or live-URL checks. Its **5** live documentation URLs
  returned HTTP **200**. Reachability is not a rolling-doc version guarantee.

### Retained verifier-only corrections

Raw failed assertions were not erased. The first ZIP assertion incorrectly
expected flat members; it was corrected to inventory the actual wrapper.
A separate verifier-authored native metadata control initially supplied a
conflicting `description` and failed with:
`Local Agent Plugin is invalid: Agent Plugin portable identity is owned by plugin.json; conflicting apm.yml fields: description`.
A new, nonconflicting name/version-only source control was then executed.
The dev assertion initially expected metadata rows to disappear; actual payload
exclusion passed, while `is_dev` metadata remained with empty exported files.
An attestation predicate looked for “mismatch” instead of the actual “does not
match” diagnostic. These are verifier setup/assertion corrections, **not book
fixes or silently repaired CLI regressions**.

**Reviewer handoff:** the bounded Chapter 10 recipes/claims PASS at the final SHA
above. Preserve F10.1/F10.2 as actual FAILs and the visible integration skips.
No chapter, fixture, historical stamp, metadata, TOC, site, root dependency,
commit, or publication was changed by this verification.
