# Edition 1.2 producer fixtures — APM 0.31.0

These are **new research fixtures**, not replacements for `ch10` or `ch11`.
Use the orchestrator's checksum-verified, absolute **0.31.0** executable as
`$Apm`, in a **short, disposable copy** of a fixture with isolated user/config
and cache directories. Do not run these commands in the book root.

The eight `apm.lock.yaml` files are unedited CLI output. Explorer observations
are recorded in the [producer reference](../../../../../content/research/updates/1.2/producer-reference.md).
Independent code-verifier/reviewer gates are still required; these notes are
not their PASS/ACCEPT verdicts.

## Fixtures and observed commands

| Directory | Purpose | Observed 0.31.0 result |
| --- | --- | --- |
| `local-bundle` | Meridian's instruction, prompt, and skill with explicit `dependencies: {}` | Install, frozen restore, CI audit, default pack, and ZIP pack: exit 0. A real ZIP consumer also installed and audited successfully. |
| `pinned-bundle` | One immutable public skill; dependency attestation and SBOM | Install, frozen, audit, and Claude-compatible pack: exit 0. Both plugin exporters rejected an altered attested skill. **Legacy `apm` format omitted this shared-path skill; see below.** |
| `portable-plugin` | Skill-only source for `pack --format agent-plugin` | Lock, source-project install/audit, and strict pack: exit 0. **The resulting native consumer's audit failed**, independently of successful registration. |
| `marketplace` | Contained local package and generated catalog | Lock, install/audit, offline strict pack, and clean check: exit 0. Deliberately changed catalog: clean check exit 4, no rewrites. |
| `metadata-offline` | Pinned public marketplace source with metadata intentionally absent | Ordinary offline preview: exit 0 but uncertifiable; `--strict-metadata`: 5; `--check-clean`: 4. Empty dependency lock is genuine, not a remote package resolution. |
| `registry-preview` | Experimental registry parsing and flat publish archive | With the feature enabled in an isolated home: install/audit and publish dry-run exit 0. **No registry service was contacted or package uploaded.** |
| `action-pinned` | Pinned public instruction using the Action's isolated manifest shape | Install/frozen/audit: 0; legacy pack and deprecated `unpack`: 0, with one instruction restored byte-for-byte. **Not an Action execution.** |
| `dev-only` | Author-only local tooling | Install/audit/pack: 0; deployed `dev-only` skill absent from the shipped bundle. |
| `ci` | Pinned Action and gh-aw input sketches | **SKIPPED-needs-network**: no GitHub runner, separately reviewed gh-aw compiler, credentials, or agent runtime was exercised. |

Cold public installs need GitHub access. Public references are fixed at commit
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`, not a moving branch.

### Default local-only bundle

From a disposable copy of `local-bundle`:

```powershell
& $Apm install
& $Apm audit --ci
& $Apm pack --dry-run --verbose
& $Apm pack --archive -o dist
# dist/meridian-standards-1.0.0.zip
```

In a separate consumer directory, pass the targets **explicitly**:

```powershell
& $Apm init --yes --target copilot,claude,cursor
& $Apm install '<absolute path to the ZIP>' --target copilot,claude,cursor
& $Apm audit --ci
```

The imperative bundle route is a one-shot deployment. It did not add an archive
dependency to the consumer manifest; the real lock recorded local deployed
files. Retain the artifact for reinstall. Omitting the install target flag in
this route used Copilot only in the probe, despite three manifest targets.

Do **not** change this package to `--format agent-plugin`: that format rejects
its commands/instructions before writing. `type: hybrid` is reserved metadata,
not permission to bypass format restrictions.

### Portable Agent Plugin

```powershell
# In a disposable copy of portable-plugin:
& $Apm lock
& $Apm pack --format agent-plugin
# build/portable-review-1.0.0/
```

The resulting directory has a pinned Agent Plugins 1.0.0 `$schema`, a skill,
`mcp.json`, and an embedded lock. Consume it **declaratively**, not with
`install <bundle>`: use a consumer `dependencies.apm` entry with
`path: ./pkg` after copying the generated bundle to `pkg`, and pin
`targets: [copilot]`.

Native registration succeeded without running Copilot. Its **CI drift replay
failed with `Native Agent Plugin canonical IR is missing`**. The source
project's empty-graph audit is not evidence that the native consumer is
audit-clean. Actual runtime loading needs Copilot CLI >=1.0.81 and remains
`SKIPPED-needs-network` in this research.

### Marketplace release checks

```powershell
& $Apm pack --offline --strict-metadata
& $Apm pack --offline --check-clean
```

Use the `marketplace` fixture for exit 0. Its output path deliberately omits
leading `./`; the inspected pack parser rejected that spelling as traversal.
The `metadata-offline` fixture deliberately produces exits 5/4 because
`--offline` cannot certify absent remote metadata. It is not a broken network
test. `--check-clean` never repairs a changed or missing catalog and is not a
bundle-integrity check.

### SBOM and Action-shaped CLI compatibility

```powershell
# pinned-bundle:
& $Apm lock export --format cyclonedx --timestamp '2026-09-16T00:00:00Z' -o sbom.cdx.json

# action-pinned:
& $Apm install
& $Apm pack --format apm --target copilot --archive
# In a DIFFERENT scratch consumer:
& $Apm unpack '<absolute path to inline-workflow-1.0.0.zip>' -o .
```

`unpack` and pack `--target` are deprecated but are still used by Action
v1.10.0. This narrowly tested instruction path is not blanket compatibility:
the same legacy Copilot pack on `pinned-bundle` returned 0 with **no skill** in
the archive. Do not hide this with an empty-output success check or switch the
Action to a plugin bundle: its pinned restore code does not support that format.

### Registry dry-run — no upload

Only in an isolated APM home:

```powershell
& $Apm experimental enable registries
& $Apm install
& $Apm publish --package book-fixtures/review --dry-run
& $Apm experimental disable registries
```

The reserved `registry.example.com` address is not a working server.
**SKIPPED-needs-network:** real registry consumption/publication requires an
authorized compatible backend; publishing was not authorized. Dry-run writes
`registry-boundary-1.0.0.zip` locally, with `apm.yml` and `.apm/` at its root,
but uploads nothing. It is not a read-only command.

## Integration boundaries

- `ci/apm-audit.yml` uses setup-only and then explicit `audit --ci`. It does not
  create branch protection or authoritative policy. Protect those separately.
- For `ci/gh-aw-review.md`, re-vendor the target-tag canonical `shared/apm.md`
  into the **consumer's** `.github/workflows/shared/`, then compile with a
  separately reviewed gh-aw version. The import is local, not a remote `uses`.
- The example overrides the shared default **0.28.0** with **0.31.0** and
  supplies `target: copilot`. It deliberately uses the tested instruction,
  not the shared-skill case with the legacy-pack omission.
- No archive, SARIF upload, Action run, gh-aw runtime, private host, or policy
  discovery is claimed verified by the documentation samples.
