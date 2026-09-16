# Operations reference fixtures — APM 0.31.0 / book 1.2

These are **Chapters 6–9 research fixtures**, not updated chapter text or a
release acceptance verdict. Every committed `apm.lock.yaml` is unedited output
from the exact 0.31.0 executable. Local dependency paths and ownership keys are
portable; no lockfile contains a local username, credential, or absolute home
path.

## Run safely

Use the orchestrator's **absolute, already verified 0.31.0 executable**:

```powershell
$Apm = '<absolute path to the prepared APM 0.31.0 executable>'
python .\backend\examples\updates\1.2\operations\verify.py --apm $Apm --suite all
```

Requirements: Python 3.10+ and PyYAML 6 (inspected: Python 3.12.10, PyYAML
6.0.3). The runner creates a new short scratch directory, copies the fixtures
there, redirects child HOME/config/cache, removes inherited credential
variables, hides the desktop `gh` helper, and uses only the supplied APM path.
It never changes the real user configuration or the book's root dependencies.
It retains `results.json` and the test projects in the printed scratch path.

On Windows, long staging paths can fail even when APM describes the Git
failure as a network error. Pass a **new, short, writable absolute** `--work`
path if needed. Do not run the fixtures in this long repository checkout.

The registry suite binds **127.0.0.1:18431** for its lifetime. If that port is
busy, stop and choose another time; do not kill an unrelated process. The
fixed port is part of the genuine lockfile URLs. The server accepts anonymous
reads only, serves inert deterministic ZIP fixtures, and has no publishing
endpoint. Its project manifests use an experimental APM feature; the runner
enables it only in a throwaway fixture HOME. No global-install command runs.

MCP examples use intentionally nonexistent commands. APM writes configuration
but the runner never starts a server or harness. Its MCP registry lookup is
bounded to an unavailable loopback endpoint. Hook commands are harmless and
are **not** invoked by a harness. Lifecycle commands write only synthetic event
names to scratch `events.json`.

## Fixtures and suites

| Fixture / suite | Smallest useful demonstration |
| --- | --- |
| `repro/`, `--suite repro` | Timestamp-free restore, frozen install, per-target ordinary drift, invalid owners, CRLF-normalized deployed hashes, lock-only ownership retention |
| `hooks/`, `--suite hooks` | Native event casing, sibling script bundles, owned sidecar drift versus user-owned merged hooks |
| `mcp/`, `--suite mcp` | Separate Copilot/VS Code/Claude paths, manifest-to-lock frozen checks, required native write failures and native-audit coverage limit |
| `lifecycle/`, `--suite lifecycle` | Explicit subtree-bound trust, update/uninstall pre-event side effects, kill switch, edited-file cleanup refusal |
| `policy/`, `--suite policy` | Correct schema, warn/block exit difference, working local inheritance, empty-list non-relaxation, explicit-policy bypass discrepancy |
| `registry/`, `--suite registry` | Experimental Current/Wanted/Latest, exact pin versus range, selected update, cache-drift regression and frozen repair |
| `registry-graph/`, same suite | Cold frozen replay of a locked graph; bounded direct constraint with an unbounded transitive constraint |
| `pack-check/`, `--suite pack` | `pack --check-clean` is read-only; marketplace-output drift exits 4 |
| `--suite security` | Generates **benign character-class markers only** in scratch; critical=1, warning-only=2 in bare audit, installed warning-only can pass CI |
| `--suite credential` | Uses a public dummy marker, never a secret: HTTP auth refused; different URL binding permits only anonymous access |
| `trust/`, `--suite trust-limit` | Reproduces parked-hook replay failure and direct-local MCP gate mismatch, then shows canonical approval |
| `--suite cleanup-limit` | Windows-only reproduction: an exclusively locked materialized file remains even though uninstall reports success |

`--suite baseline` materializes the six ordinary local fixtures and audits
them without making deliberate negative changes. `--suite all` runs the main
suites, including explicitly labelled coverage/regression observations.
`trust-limit` and `cleanup-limit` are separate opt-in reproductions.

## Read results correctly

- `OBSERVED` means the command returned its asserted outcome. An expected
  negative test, such as audit of a deliberately edited file, legitimately
  returns nonzero.
- `KNOWN-CLI-LIMITATION` is **not PASS for that security/integrity guarantee**.
  The runner asserts a reproducible 0.31.0 discrepancy so an author/verifier
  cannot silently omit it.
- A successful `--suite all` therefore means the **test expectations were
  reproduced**, not that APM has no failures.

Current discrepancies that must remain visible:

1. `APM_POLICY_DISABLE=1` suppresses an explicit `audit --ci --policy FILE`.
   `--no-policy` alone does not. Protect the job's environment as well as its
   command line.
2. Direct local self-defined MCP was configured despite a `default-deny`
   executable decision. Parked hooks stayed withheld, but CI replay reported
   their missing deployment. Do not present `trust/` as a green pre-approval
   deployment example.
3. Missing or edited native MCP config was not detected by CI audit in the
   tested MCP-only project. Frozen checks compare manifest-to-lock service
   state, not all native bytes.
4. A selected registry update preserved the unselected dependency's lock and
   deployed files but advanced its materialized cache. Immediate CI audit
   failed. `install --frozen` repaired that cache without moving the lock;
   the subsequent audit passed. This failure is tested before repair.
5. On this Windows binary, an exclusive file lock did not produce the
   documented uninstall directory-deletion error. Uninstall returned 0,
   removed the declaration/ownership, and left the locked file. The separate
   edited-target-file refusal correctly returned 1 and retained the contract.

The detailed evidence, policy hash/fetch-failure discrepancies, exact probe
IDs, source citations, and chapter-by-chapter author directions are in
[`operations-reference.md`](../../../../../content/research/updates/1.2/operations-reference.md).
Raw logs are session artifacts, not checked-in caches.

## Scope boundaries

Public Git frozen/cold-cache runs were performed separately against the real
sample package at `fb2851683be0e0e7711421d518bd8dba23b0b1f6`; the report records
the transitive pin actually resolved. These local fixtures do not claim that
private GitHub/GHES/GitLab/ADO infrastructure or a real MCP server was tested.

User-scope plugin `bin/` deployment, machine admin policies, live policy
publication, signing, paid runtimes, and pushes were not executed. The
project-scope `--trust-bin` probe still reported that actual bin deployment
required global scope; no global install was used to force coverage.
