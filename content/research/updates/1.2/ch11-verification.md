# Chapter 11 independent verification — book 1.2 / APM 0.31.0

**Chapter claim/recipe verdict: PASS within the stated integration boundaries.**
Local gate and policy recipes passed their asserted outcomes. The narrow
instruction pack/restore control passed; **legacy shared-skill delivery remains
an actual FAIL**. Workflow YAML/source validation is not Actions execution,
gh-aw compilation, private authorization, or branch-protection acceptance.
**Reviewer acceptance is pending.**

| Source identity | Value |
| --- | --- |
| Chapter | `content/chapters/enterprise-at-fleet-scale.html` |
| **Final chapter SHA-256** | **`4a77f11386578721414e4797077d4eb17073919b55cc56b351141660e970ede5`** |
| Frozen CLI | Exactly **APM 0.31.0** |
| Independently inspected Action | **v1.10.0**, `d723bb64ed70c135bbaf87d126b721dd2dae0439` |
| APM/shared-import source | `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` |
| Date | 2026-09-16 UTC |
| Minimal book fix | **None** |

## Executable, isolation, and provenance

```powershell
$RunRoot = 'C:\Users\masalnik\.copilot\session-state\2d4facdd-cd43-4bef-9f47-dc669687d65a\files\book-v1.2'
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
```

Executable SHA-256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
**VerifyRoot** = `RunRoot\verify-ch10-ch12`;
**P** = `C:\Windows\Temp\v12-zwwo0gts\p`.
All command tables below give exact arguments following `& $Apm`.
The complete absolute commands, environment isolation, exits, original output
bytes, runtimes, hashes, and mtimes are in `VerifyRoot/logs/<id>.*`.

Fresh short projects and independent HOME/USERPROFILE/config/cache/temp paths
were used, without inherited host credentials, user Git configuration,
credential helpers, `gh`, or agent-runtime PATH entries. `APM_POLICY_DISABLE`
was absent except in explicit scratch-only negative controls. Public reads
used the actual pinned GitHub source anonymously. Local suites also succeeded
with unavailable loopback proxies. No corporate service or paid runtime was
silently substituted.

Shared execution accounting and the retained verifier-only setup corrections
are in [Ch10 verification](ch10-verification.md): **136 logged native
invocations**, including 20 guards and 13 help checks; **784.094 s** summed
native runtime, no timeouts. Per-example times below overlap where controls
support more than one claim. This is not a benchmark.

## Ch5 reuse decision — checked, then independently rerun

The earlier **independent** `verify-ch05` evidence was read and checked:
three canonical local-instruction input hashes, the two relevant raw output
streams and snapshots, exact argument lists/executable digest, and all
18 retained version guards matched their records. No explorer result was used
as independent evidence.

However, the literal chapter block uses `& $Apm` and CRLF, whereas the retained
Ch5 two-line suffix uses `apm` and LF. The normalized commands are equivalent,
but **literal source code hashes are not equal**. Rather than call that an
exact-code-hash cache hit, this task executed a fresh materialization plus the
displayed frozen/audit pair in `P/ql`. **No old native result was reused or
restamped.**

Details, original hashes/records, and the fresh-record mapping are in
`assertions/ch05-equivalent-reuse.json`. The current complete local lock
remained:
`0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa`.

## Source code IDs and verification status

The chapter has **12** pre/code blocks; each figure has `/code-1`.
`sources/ch11-blocks.json` stores their exact raw and decoded hashes.
`source-probe-map.json` binds those IDs to command records and fixture paths.
The cold evidence table and compatibility callout also have separately mapped
verification IDs. Historical blocks retain their original 0.23.1 scope.

| Example ID / path | Status | CLI / integration evidence | Runtime (s) |
| --- | --- | --- | ---: |
| `ch11-ci-current` — `producer/ci/apm-audit.yml` | **SKIPPED-needs-network** runner/ruleset; static contract PASS, underlying cold CLI gate PASS | CLI 0.31.0; Action source v1.10.0 | 8.902 local CLI |
| `ch11-ghaw-import` — `producer/ci/gh-aw-review.md` | **SKIPPED-needs-network** compiler/runner/runtime; source/input checks and narrow instruction CLI pair PASS | CLI 0.31.0; frozen shared file; Action source v1.10.0 | 51.543 local CLI |
| `ch11-local-audit` — `core/local-instruction` | **PASS**, fresh execution, not cached reuse | 0.31.0 | 13.144 including materialization |
| `ch11-cold-audit-evidence` | **PASS**, reachable/unreachable/tamper/SARIF assertions | 0.31.0 | 38.136 |
| `ch11-local-policy` — `operations/policy` | **PASS**, resolution 0 and required-package block 1 | 0.31.0 | 13.274 |
| `ch11-consumer-policy` | **PASS**, missing-org install/audit both fail closed | 0.31.0 | 6.311 |
| `ch11-org-policy-current` | **SKIPPED-needs-network** publication/private discovery; exact YAML locally accepted | Parser/status 0.31.0, not live authority | 4.598 |
| `ch11-proxy-current` | **SKIPPED-needs-network**, unavailable fictional corporate proxy and credentials | Source-grounded target 0.31.0, no corporate execution | 0 |
| `ch11-workflow-historical`, `ch11-sarif-historical` | **SKIPPED-needs-network**, historical runner/upload sketches | Original 0.23.1 pins retained | 0 |
| `ch11-clean-historical`, `ch11-direct-historical`, `ch11-transitive-historical` | PASS archival boundary only; **not new CLI PASS results** | Original 0.23.1 transcripts retained | 0 |
| Verifier ID `ch10/ch11-legacy-shared-skill` | **FAIL**, actual empty pack/restore despite exit 0 | 0.31.0 | 8.750 |
| `ch11-audit-coverage`, native-plugin branch | **FAIL native audit**, already documented; registration PASS | Independent Ch10 records at 0.31.0 | See Ch10 |

## Exact local commands, exits, and observed state

| Record ID | CWD | Exact command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `ch11-local-materialize` | `P/ql` | `install` | 0 | 4.885 |
| `ch11-local-frozen` | `P/ql` | `install --frozen` | 0 | 3.779 |
| `ch11-local-audit` | `P/ql` | `audit --ci` | 0 | 4.480 |
| `cold-audit` | `P/c` | `audit --ci` | 0 | 8.902 |
| `cold-offline-unreachable` | `P/co` | `audit --ci` | **1 expected** | 11.854 |
| `cold-sarif` | `P/c` | `audit --ci -o apm-audit.sarif` | 0 | 8.616 |
| `cold-tamper` | `P/c` | `audit --ci` after harmless deployed-byte edit | **1 expected** | 8.764 |
| `policy-frozen` | `P/q` | `install --frozen` | 0 | 4.461 |
| `policy-status` | `P/q` | `policy status --policy-source ./apm-policy.child.yml --json --check` | 0 | 4.603 |
| `policy-audit` | `P/q` | `audit --ci --policy ./apm-policy.child.yml -f json` | **1 expected** | 4.210 |
| `policy-org-schema` | `P/q` | `policy status --policy-source ./chapter-org-policy.yml --json --check` | 0 | 4.598 |
| `policy-explicit-block` | `P/q` | `audit --ci --policy ./apm-policy.block.yml -f json` | **1 expected** | 4.860 |
| `policy-explicit-beats-flag` | `P/q` | `audit --ci --policy ./apm-policy.block.yml --no-policy -f json` | **1 expected** | 4.977 |
| `policy-env-disables-explicit` | `P/q` | `audit --ci --policy ./apm-policy.block.yml -f json`, child env `APM_POLICY_DISABLE=1` | 0, documented bypass | 3.307 |
| `policy-missing-org-install` | `P/q` | `install`, after adding the exact consumer fail-closed excerpt | **1 expected** | 3.152 |
| `policy-missing-org-audit` | `P/q` | `audit --ci`, same fail-closed input and no remote | **1 expected** | 3.159 |
| `policy-env-disables-failclosed` | `P/q` | `audit --ci --policy ./apm-policy.block.yml -f json`, child env `APM_POLICY_DISABLE=1` | 0, documented bypass | 2.301 |

### Cold is not offline

Both cold projects began with the genuine pinned manifest/lock and deployed
skill, **no `apm_modules`**, and their own initially empty caches. The source was
the one immutable public style-checker slice at
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`, not the full floating sample graph.

- Reachable cold audit passed and changed **no checkout file hash or mtime**;
  it did not populate checkout `apm_modules`.
- The separate unavailable-loopback-proxy run failed during hydration/replay
  with exit **1**, also leaving the checkout unchanged. This is a successfully
  asserted negative, **not SKIPPED-needs-network**.
- The harmless ASCII deployed edit failed CI with exit **1**, without repair.
- `-o apm-audit.sarif` produced a genuine SARIF **2.1.0** report. That report was
  the **only** project file changed by the command. No Code Scanning upload
  was attempted. The SARIF command ran after the first clean cold audit; it is
  report-output evidence, not another independently empty-cache experiment.

### Policy authority and bypass

The child policy resolved as `outcome: found`, `enforcement: block`,
one deny and one required dependency, despite its attempted `warn`/empty-list
relaxation. `extends_chain: []` did **not** mean inheritance was absent.
The expected audit failure reported this exact JSON check:

```json
{
  "name": "required-packages",
  "passed": false,
  "message": "1 required package(s) missing from manifest",
  "details": [
    "example-org/required-review-package"
  ]
}
```

The full report had 12 passing checks and one failure; this is this fixture's
enumeration, not a timeless total. Status and audit remained read-only for
project files.

The exact displayed organization YAML was copied to
`P/q/chapter-org-policy.yml` and parsed by real `policy status --check`.
This proves accepted keys, **not publication or discovery**. The consumer
`policy.fetch_failure_default: block` excerpt was added to a complete
materialized manifest; absent authority then failed install and audit.
The environment-disable controls still suppressed explicit policy, even with
that setting. Neither result was hidden by changing a lock or adding
`--no-drift`.

## Action and gh-aw: source validation, not deployment

Independent anonymous GETs fetched `action.yml`, `src/runner.ts`,
`src/installer.ts`, and `src/bundler.ts` from the **exact Action commit**.
`git ls-remote https://github.com/microsoft/apm-action.git refs/tags/v1.10.0 refs/tags/v1.10.0^{}`
exited **0** and resolved the reviewed commit. Receipts are in
`http-source-receipts.json`, `assertions/action-tag.json`, and `sources/action/`.
These were source reads, not reuse of the explorer's Action verdict.

The YAML parser used YAML-1.2 boolean handling and duplicate-key rejection:
GitHub's `on:` was not accidentally parsed as a boolean key. Checks established:

1. Current CI YAML uses the immutable Action commit, `setup-only: 'true'`,
   `apm-version: '0.31.0'`, and an explicit **`apm audit --ci`** step. The
   supplied `with` keys exist in the pinned Action contract.
2. The Action default is **0.14.0**, not 0.31.0. Its setup-only branch exits
   after CLI setup. Default install and informational `audit-report` are not
   substituted for the checked-out-content integrity gate.
3. The shared import still defaults to **0.28.0**. The example's explicit
   **0.31.0** reaches **both pack and restore**. The shared file selects Action
   **v1.10.0** in both steps; that tag selection is distinct from the direct
   CI example's immutable commit pin.
4. Required `target: copilot` matches `engine: copilot`; prep rejects blank
   and `all`. The pinned package input matches the `import-schema`.
5. Pack is isolated, uses the explicit target and imported packages, and has
   its own work directory. Its generated manifest matches the independently
   executed `producer/action-pinned` fixture. No automatic host
   manifest/lock/primitives/policy inheritance is asserted.
6. `token-source: github-token` is the current-repository read-token selector,
   not authorization for unrelated private repositories.
7. The pinned wrapper explicitly builds legacy `--format apm` pack arguments
   and restores using deprecated `unpack`; its supported format selector is
   not a tested plugin-format repair. Its installer uses tool-cache and
   supports Linux/macOS, not an executed Windows Action.

### Shared-source byte provenance

A fresh scratch import at
`P/static/.github/workflows/shared/apm.md` byte-matched the supplied Windows
source checkout:
`6ebe127ee1ae527249b81239a8fa52f3a3ead298042b2d43122d6a68faf0f3ae`.
That checkout is **CRLF**. The actual pinned Git blob is **LF**, SHA-256
`fb036a7a688eb24d0fb9fa0749dbf1840bd9e7c025ab95ca7546859f150727d8`;
the bytes match after only CRLF-to-LF normalization.

Do **not** advertise the CRLF checkout digest as the digest of an unmodified
`raw.githubusercontent.com` download. This distinction is recorded in
`source-receipts.json`; no canonical source or global Git setting was changed.
It does not change the YAML contract, and the chapter's receipt refers to its
scratch source copy, not a newly executed download/compile recipe.

## Narrow instruction PASS and real shared-skill FAIL

| Independent record | CWD | Exact command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `integration-instruction-install` | `P/i` | `install` | 0 | 17.576 |
| `integration-instruction-frozen` | `P/i` | `install --frozen` | 0 | 8.982 |
| `integration-instruction-audit` | `P/i` | `audit --ci` | 0 | 9.923 |
| `integration-instruction-pack` | `P/i` | `pack -o build --format apm --target copilot --archive` | 0 | 6.351 |
| `integration-instruction-unpack` | `P/iu` | `unpack 'C:\Windows\Temp\v12-zwwo0gts\p\i\build\inline-workflow-1.0.0.zip' -o .` | 0 | 8.711 |
| `integration-instruction-legacy-tamper` | `P/i` | `pack -o rejected --format apm --target copilot --archive`, altered included instruction | **1 expected** | 7.937 |
| `public-resume-legacy-skill-pack` | `P/g` | `pack -o legacy --format apm --target copilot --archive` | **0, delivery FAIL** | 4.630 |
| `public-resume-legacy-skill-unpack` | `P/gu` | `unpack 'C:\Windows\Temp\v12-zwwo0gts\p\g\legacy\pinned-bundle-1.0.0.zip' -o .` | **0, delivery FAIL** | 4.120 |

The instruction archive contained only its embedded lock and
`.github/instructions/design-standards.instructions.md`. The restored file
was **535 bytes**, SHA-256
`6f5d994d6437416e14e4ca5540f4d1cf06fad079728a1419acfb1dd7038ec38d`,
identical to the installed instruction. The empty consumer acquired **no**
`apm.yml` or `apm.lock.yaml`. This is the demonstrated compatibility scope.

The actual shared-skill failure has no failing process exit or stderr to
quote. Instead, exact relevant stdout was:

```text
[!] No files to pack for target 'copilot'
[i] Bundle target: copilot (0 dep(s), 0 file(s))
[!] No files were unpacked
```

The resulting ZIP contained **only `apm.lock.yaml`** under its archive wrapper;
the consumer stayed empty. Full output, hashes, and inventories are in
`logs/public-resume-legacy-skill-{pack,unpack}.*` and
`assertions/legacy-skill-failure.json`.

**Diagnosis / owner:** `apm-cli-explorer` / upstream should track legacy Copilot
pack-prefix selection omitting the shared `.agents/skills` path. **FAIL is
retained**, not renamed a network skip. The chapter correctly avoids blanket
gh-aw/all-skills compatibility and does not substitute a different bundle
format to manufacture a pass.

Native-plugin local-path CI audit independently retained the exact failure
`Native Agent Plugin canonical IR is missing, so deployment was blocked.`
See Ch10 F10.1 for the original bundle and nonconflicting metadata control.

## Skips, cross-wave limits, and reviewer handoff

**SKIPPED-needs-network**, visibly bounded in the chapter:

- No authorized GitHub runner, required-check/ruleset changes, artifact jobs,
  or Code Scanning upload permission was supplied or exercised.
- No separately reviewed/frozen gh-aw compiler was supplied; **compilation was
  not run**. No agent loading, paid runtime, or credential integration was run.
  Source/YAML validation is not compilation.
- The corporate proxy/Artifactory endpoint and credentials are fictional or
  unavailable. The loopback failure control is not proxy acceptance.
- No Meridian policy was published; no private GitHub/GitLab/ADO
  discovery/permission chain was tested.
- Real registry consumption/publication lacks an authorized compatible
  backend; no real publish was permitted. Ch10's local dry-run writes are
  independent evidence, not a registry integration pass.

The updated Ch11 prose also cites operations controls for HTTPS warm-cache/TTL
parity, remote policy-byte hash mismatch, direct/transitive registry pin rules,
Unicode severity, invalid ownership, and native MCP coverage. **Those explorer
experiments were not relabeled as fresh independent executions here.** Their
source/provenance boundaries were read against the operations/core references;
the linked Ch6–9 independent gate remains the authority for those shared
experiments. This task independently reran the displayed Ch11 local recipes,
the policy-bypass/no-org controls, cold CI cases, and relevant producer/native
compatibility cases—not an entire operations or explorer suite.

All **35** unique Chapter 11 link references passed local/fragment,
pinned-source, or live reachability checks; its **4** live documentation URLs
returned HTTP **200**. No stale workflow/transcript stamp was advanced.

**Reviewer handoff: PASS for the bounded updated recipes and integration
claims, at the final SHA above.** Retain the actual compatibility FAILs, the
compiler/runner/private-infrastructure skips, and cross-wave provenance.
No chapter/fixture/root dependency/metadata/TOC/site edit, commit, or publication
was made. Only this report and the companion Ch10/12 reports are repository
outputs of this task.
