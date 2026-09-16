# Chapter 12 independent verification — book 1.2 / APM 0.31.0

**Verdict: PASS — source, claim-boundary, historical-snapshot, and link checks
only.** There are **zero runnable pre/code examples** in this chapter. No new
Chapter 12 CLI recipe, competitor execution, market survey, workflow
compilation, or runtime integration is claimed. **Reviewer acceptance is
pending.**

| Source identity | Value |
| --- | --- |
| Chapter | `content/chapters/the-landscape-and-whats-next.html` |
| **Final chapter SHA-256** | **`7460ab5177c7e68718dedbc9237ecba98f2da903d7dbd1610c119803e4062aed`** |
| APM capability baseline | Exactly **0.31.0**, book 1.2 target |
| Pinned APM source commit | `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` |
| Competitor baseline | **2026-07-01 historical snapshot**, not re-researched |
| Verification date | 2026-09-16 UTC |
| New Chapter 12 APM invocations | **0** |
| Book/code fixes | **None** |

## Evidence and method

**RunRoot**:
`C:\Users\masalnik\.copilot\session-state\2d4facdd-cd43-4bef-9f47-dc669687d65a\files\book-v1.2`.
**VerifyRoot** = `RunRoot\verify-ch10-ch12`.

The shared Ch10/11 real-CLI work used the supplied absolute executable:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
```

Its SHA-256 was
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
Those executions are reported in [Ch10 verification](ch10-verification.md)
and [Ch11 verification](ch11-verification.md), not counted as newly executed
Chapter 12 examples.

The independent static checker:

- Captured current and Git-HEAD historical chapter bytes; enumerated **zero**
  pre/code blocks and retained all claim/link anchors.
- Re-read the pinned APM Git objects and checked the supplied Windows source
  checkout against them, accounting explicitly for CRLF/LF. Source HEAD was the
  frozen commit. No source or user/global Git setting was edited.
- Independently fetched pinned Action sources and checked the shared-import
  YAML contract with YAML-1.2 boolean handling and duplicate-key rejection.
- Compared the **four competitor rows** to the historical chapter.
- Checked local file/fragment destinations and frozen-source links; made
  anonymous **HTTP HEAD** requests for live URLs. Those requests checked
  reachability, not current competitor functionality or versions.

Reproduction command:
`python '<VerifyRoot>\static_checks.py' static-complete` → **exit 0**.
The completed shared static source/YAML/snapshot/link checks took **17.449 s**
after the version guard; this is a shared check runtime, not a Chapter 12 CLI
runtime or performance benchmark. Final indexing/source-hash verification:
`python '<VerifyRoot>\summarize.py'` → **exit 0**.

| Artifact under VerifyRoot | What it proves |
| --- | --- |
| `sources/the-landscape-and-whats-next.html`, `historical-the-landscape-and-whats-next.html` | Exact current and historical inputs |
| `sources/ch12-blocks.json` | Empty executable-block inventory |
| `assertions/ch12-snapshot.json` | Four unchanged normalized competitor rows; raw hashes retained separately |
| `source-receipts.json` | Frozen Git blob/worktree hashes and line-ending equivalence |
| `http-source-receipts.json`, `sources/action/`, `assertions/integration-contract.json` | Independently read Action/shared source contract, not execution |
| `link-checks.json` | Exact URLs, local/pinned checks, HTTP status, redirect destination, time |
| `final-source-checks.json`, `summary.json` | Final source SHA, no chapter/fixture/metadata/root dependency modifications |

## Claim IDs / status / scope

These are **claim anchors, not new code example IDs**.

| Claim ID / chapter area | Status | Independent evidence and limitation |
| --- | --- | --- |
| Objective and comparison caption | **PASS snapshot boundary** | APM alone advances to 0.31.0; competitor claims explicitly remain July 1 |
| `ch12-standards` | **PASS source check** | Agent Plugins 1.0, APM 0.31.0, OpenAPM 0.1, and reserved 0.2 work are separate version domains |
| `ch12-apm-scope` | **PASS bounded source claim** | Mixed primitive management does not promise identical deployment/audit/runtime support |
| `ch12-plugin-boundary` | **PASS source/claim consistency** | Default Claude-compatible versus opt-in strict format; Copilot loading boundary preserved; actual native audit FAIL remains in Ch10 |
| Target-catalog paragraph | **PASS source check only** | Grok Build and Kiro agent support; Hermes stable/explicit-only; Grok Cloud experimental—not runtime tests |
| `ch12-registry-boundary` | **PASS source check** | Implemented experimental client and implementable API are not a hosted searchable hub |
| `ch12-roadmap` | **PASS source check** | Issue-backed priorities/milestones are planning, not implementation permission or delivery promises |
| `ch12-gh-aw` | **PASS static contract**; runtime **SKIPPED-needs-network** | Required concrete target, isolated imports, and explicit version override checked against pinned sources |
| `ch12-gh-aw-compatibility` | **PASS accuracy of bounded claim**; shared-skill delivery itself **FAIL** | Independent Ch11 instruction success and actual skill omission agree with the text |
| Four competitor rows | **PASS historical preservation only** | No new competitor capability, version, count, or ranking evidence asserted |
| All chapter links | **PASS reachability/path checks** | 47 unique chapter references; 18 live URLs HTTP 200; no feature survey |

## Source-grounded boundaries checked

### Standards versus implementation

At the frozen commit:

- `docs/src/content/docs/specs/openapm-v0.1.md` identifies OpenAPM 0.1 as an
  **editor's Working Draft**. Its registry wire contract is informational/
  non-normative in 0.1; normative registry work, publisher attestation, archive
  determinism, and version withdrawal have reserved 0.2 scope.
- `docs/src/content/docs/reference/registry-http-api.md` labels its API
  **v1 (implementable)** and lists version-list, archive-download, and publish
  endpoints. The specified endpoint set is not a public search service.
- `docs/src/content/docs/guides/registries.md` and the shipped publish/client
  implementation establish experimental registry support, **not evidence of a
  Microsoft-operated public searchable hub**. No real backend was tested here.

The chapter does not turn a standards reservation into “no registry client,”
or an implemented API into a hosted-service or OpenAPM 0.2 delivery claim.

### Format, harness, and trust boundaries

The frozen pack and native-consumer references preserve:

- No-flag/`plugin` compatibility output remains Claude-compatible.
- Strict Agent Plugins output carries skills/MCP, not Meridian's entire
  instruction/prompt/skill package.
- Recognized native plugins register whole for Copilot; actual loading requires
  **Copilot CLI >=1.0.81**. Registration is not agent execution or audit success.
- Package hashes and install-time scans do not establish publisher signatures,
  benign content, complete runtime coverage, or injection impossibility.

The actual updated producer recipes underlying those distinctions were tested
in Ch10. In particular, the **native canonical-IR audit failure remains FAIL**,
not a source-only guess or a network skip.

### Catalog and roadmap

`reference/targets-matrix.md` supports Grok Build's inclusion in the default
set, Kiro's agent projection, stable but explicit-only Hermes, and experimental
Grok Cloud. These are catalog/source facts, not a new multi-harness test.

`GOVERNANCE.md` links Project 2304 and differentiates **Now / Next / Later**,
reviewed issue scope, and plausible milestone cohorts. It explicitly does not
grant implementation permission or dates merely through roadmap placement.
This contributor process is not enterprise `apm-policy.yml` governance.

### gh-aw contract and compatibility

The frozen shared file requires a concrete target matching the engine and
rejects `all`. It still defaults to **APM 0.28.0**; the chapter correctly
requires explicit **0.31.0 for both pack and restore**. Its independently
reviewed Action selection is **v1.10.0**, not an automatically selected CLI
version. Imported packages build an isolated context; host manifest, lock,
primitives and policy do not automatically carry over.

The independent Ch11 CLI pair restored one nonempty pinned instruction
byte-for-byte. The legacy Copilot shared-skill pair exited **0/0** but delivered
no skill. Exact relevant failure output:

```text
[!] No files to pack for target 'copilot'
[i] Bundle target: copilot (0 dep(s), 0 file(s))
[!] No files were unpacked
```

**Actual status: FAIL for that skill inventory.** Owner:
`apm-cli-explorer` / upstream. This report does not relabel it PASS because the
chapter accurately describes it, or SKIPPED because compiler/runtime execution
is unavailable. Ch10/11 hold the exact commands, exits, runtimes and inventories.

The source-copy digest in the chapter's hidden provenance comment is the
Windows **CRLF checkout** digest
`6ebe127ee1ae527249b81239a8fa52f3a3ead298042b2d43122d6a68faf0f3ae`.
The pinned **LF Git blob** digest is
`fb036a7a688eb24d0fb9fa0749dbf1840bd9e7c025ab95ca7546859f150727d8`.
They are line-ending-equivalent, not raw-byte-identical downloads.

## Competitor snapshot and links — no fake survey

The normalized text of each `gh skill`, `orthogonalhq/apm`,
`TheLarkInn/aipm`, and `vercel-labs/skills` table row exactly equals its
historical row. Raw HTML hashes are retained separately because formatting/
line endings differ. Versions, primitive coverage, registry assertions, and the
approximate agent count were **not re-researched or recertified**.

The comparison caption, introductory evidence note, warning callout, and
closing questions explicitly retain the **2026-07-01** boundary. HTTP success
for a competitor link does not promote that snapshot into September research.

All **47** unique Chapter 12 references passed:

- Local chapter files and fragment IDs exist.
- Frozen APM source links resolve to existing files at the reviewed commit.
- All **18 live URLs** returned HTTP **200**, including the four competitor
  destinations, standards sites, public roadmap, gh-aw documentation, and
  governance guidance. Exact URLs/redirects/timing are in `link-checks.json`.

No compiler/runtime error output exists to report because those integrations
were not run. Their visible marker remains **SKIPPED-needs-network**:
no separately reviewed gh-aw compiler, authorized Actions runner/artifact/
authentication chain, configured agent runtime, or live registry backend was
supplied. Source validation does not fill those gaps.

**Reviewer handoff: PASS at the final source SHA above, for the source/
snapshot/link scope only.** Keep the historical competitor boundary and the
actual compatibility FAIL explicit. No chapter, historical verification
stamp, other chapter, fixture, metadata, TOC, site, root dependency, commit, or
publication was changed.
