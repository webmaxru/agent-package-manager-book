# Canonical Git/LF checkout verification — book 1.2 / APM 0.31.0

**Verdict: PASS for the five primary fixtures and the representative ZIP
round-trip.** All five original locks work with the actual Git/LF source
bytes in fresh scratch projects. Frozen install, ordinary install, and
their CI audits preserve the complete original lock bytes.

**Platform scope: canonical LF on native Windows x86_64 — NOT Linux
execution.** No Linux binary, container, WSL, POSIX permission, or symlink
compatibility result is claimed. This is an additional checkout-equivalence
gate, not a replacement for the previous raw-Windows evidence or a blanket
release/reviewer acceptance.

## Executable, isolation, and exact scope

| Item | Value |
| --- | --- |
| CLI actually executed | Exactly **APM 0.31.0** |
| Executable SHA256 | `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2` |
| Execution date | 2026-09-16 UTC |
| First / last invocation start | `02:53:13.041488Z` / `02:54:45.362287Z` |
| Native invocations | **31**: 6 version guards, 1 help command, 24 example/control commands |
| Summed native runtime | **99.038 s**; parallel batches, not a performance benchmark |
| Failures / timeouts / network skips | **0 / 0 / 0** |

Aliases used throughout this report:

| Alias | Meaning |
| --- | --- |
| `RunRoot` | Orchestrator's session artifact directory, `files/book-v1.2` |
| `VerifyRoot` | `RunRoot/verify-checkout` |
| `Scratch` | New owned short temporary root, recorded in `VerifyRoot/runtime-layout.json` |
| `Examples` | `backend/examples/updates/1.2` in the book checkout |
| `Zip` | `Scratch/p/pbi/dist/meridian-standards-1.0.0.zip` |

Every APM command used this executable's **absolute path**, not PATH lookup:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

Each fixture batch and the separate ZIP consumer checked that exact banner
before executing examples. All projects used short **normal CWDs**, not
the book root or `--root`. HOME, APM home/cache, app-data/config, temp,
and credential locations were isolated per batch. Child environments were
allowlisted; host tokens, `gh`/agent-runtime PATH entries, user/system Git
configuration, and credential helpers were not inherited.

Local batches used unavailable loopback HTTP/HTTPS proxies to bound
unintended network use. The pinned skill used actual anonymous public Git.
No global config or root-dependency command, live publish, MCP server,
or agent runtime was run.

## Checkout model — exact Git bytes, not a normalization assumption

The five fixture trees contain **18 files**: **13 authored text files**
and **five genuine locks**. For scratch inputs only:

1. UTF-8 text without NUL was transformed using **only**
   `CRLF -> LF`. No trimming, BOM removal, lone-CR conversion, YAML
   reserialization, filename change, or binary normalization occurred.
2. Each resulting file was compared byte-for-byte with
   `git --no-pager show :<repository-relative-path>`, the actual raw
   **Git index blob**. All 18 matched. `git ls-files --eol` independently
   showed index `i/lf`, authored working files `w/crlf`, and locks `w/lf`.
   This verifier did not stage, commit, or change Git configuration.
3. All five original `apm.lock.yaml` files were already LF. They were
   copied **unchanged**, not normalized or regenerated to make a test pass.
4. Each fixture received **two fresh projects**, both starting with the
   same LF sources and original lock, without modules or deployed output:
   - `*f`: `install --frozen`, then `audit --ci`;
   - `*i`: ordinary `install`, then `audit --ci`.

The first frozen project starts with its batch's fresh isolated package
cache. The second project has no generated project state but may reuse
that batch's Git cache. In particular, the pinned public skill's frozen
acquisition is cold; its ordinary-install project is fresh but its Git
cache is warm. Neither project receives a lock repaired by the other.

Raw Git commands/exit codes and input byte receipts are in
`git-commands.json`, `git-eol.txt`, `line-endings/*.json`,
`workspace-inputs/*.zip`, and `lf-inputs/*.zip`.

## Per-example status

All paths below are relative to `Examples`; all CLI evidence is **0.31.0**.
Runtime excludes version guards/help and is the sum of the listed
materialization/audit commands for that case.

| Example ID | Fixture / scope | Status | Exits: frozen, audit, ordinary, audit | Native seconds |
| --- | --- | --- | --- | ---: |
| `checkout-core-local-instruction` | `core/local-instruction` | **PASS** | 0 / 0 / 0 / 0 | 13.532 |
| `checkout-core-onboard-skill` | `core/onboard-skill` | **PASS** | 0 / 0 / 0 / 0 | 13.418 |
| `checkout-core-pinned-skill` | `core/pinned-skill` | **PASS** | 0 / 0 / 0 / 0 | 16.647 |
| `checkout-operations-repro` | `operations/repro` | **PASS** | 0 / 0 / 0 / 0 | 14.345 |
| `checkout-producer-local-bundle` | `producer/local-bundle` | **PASS** | 0 / 0 / 0 / 0 | 14.779 |
| `checkout-producer-zip-consumer` | Real producer ZIP, separate LF consumer | **PASS** | Pack / init / ZIP install / audit: 0 / 0 / 0 / 0 | 10.981 |

Expected native file paths and every lock-attested project-relative file
hash were checked, not inferred solely from exit 0. Each audit preserved
the complete project byte inventory. No source or lock input changed
during materialization.

## Exact original and post-command lock hashes

The **Before** column is the working-tree lock, Git blob, and both fresh
scratch inputs. The **After** column is the lock after **each** frozen,
ordinary, and audit command. The producer lock also remains identical
after ZIP packing. Full per-command transitions are recorded in
`verification-status.json` and the raw logs.

| Fixture | Before SHA256 | After every relevant command SHA256 |
| --- | --- | --- |
| `core/local-instruction` | `0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa` | `0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa` |
| `core/onboard-skill` | `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28` | `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28` |
| `core/pinned-skill` | `6b9ebb9ddcba38e6eddae38ca0c3658c2fabeee90e279857c9159f149ba09507` | `6b9ebb9ddcba38e6eddae38ca0c3658c2fabeee90e279857c9159f149ba09507` |
| `operations/repro` | `79fe2a70ae0c8b9987ddd0105d013c6593a6c3fd8135ae94601d4df58fd22772` | `79fe2a70ae0c8b9987ddd0105d013c6593a6c3fd8135ae94601d4df58fd22772` |
| `producer/local-bundle` | `2b906800526ba3942b583d75db6057551e9101447e733be60ef41a7beb66fe07` | `2b906800526ba3942b583d75db6057551e9101447e733be60ef41a7beb66fe07` |

## Exact authored-input transformation hashes

Aliases in this table: **LI** = `core/local-instruction`; **OS** =
`core/onboard-skill`; **PS** = `core/pinned-skill`; **RO** =
`operations/repro`; **PB** = `producer/local-bundle`.
The five unchanged lock inputs are accounted for above. Every **LF**
hash below also equals the corresponding actual Git blob's SHA256.

| Fixture / relative file | Original working-tree SHA256 | LF scratch / Git-blob SHA256 |
| --- | --- | --- |
| LI `apm.yml` | `60102cbbe3d3d0fbdf2e7cce6c3d3c6bab11d5605583947f77086cddcd00c934` | `8b86dafff9043b13e16f038574ede77757c44e5c14f20e0f8fed4c847a7d0069` |
| LI `.apm/instructions/meridian-checkout.instructions.md` | `29e9848b2a7463c34fa57e1dbd65caf7f3a1d23dd61df107f11ed73653facfad` | `bf0a95675dd08131c972acfa85ba61e73e9d9ab0c042f1fcb59fb12cb601da49` |
| OS `apm.yml` | `a865eef2ce859f724178723a72152678a19012a6a8ad1b9bca949c76927d7210` | `469c0da7aa9b3401ff22f0e89becfa086ebdd0db453bf34245efa0c2d47618b7` |
| OS `.claude/skills/checkout-review/SKILL.md` | `838837e021cefe28b5624e508d2ec2a7871c7b59c7166f42e57e5c7d1502d8f6` | `5a6599461a905a241ad544f87c54a39c945982e327a1f19fa748d19c0a994e49` |
| PS `apm.yml` | `345bd03e5b24af37425cffe624cf8d3ebafff7e60b061b7af1288de7ce65162b` | `1fd06563f3f192ab5ad6fb4a250b12486e537a5090bd626fd6dd277027eb4cde` |
| RO `apm.yml` | `d30b320e9ace5f31e87888215b648a7485d0586b48d1ac1d2b19bfde9f4bf2a3` | `cbd74843376fe59531441aa1e84e461fc0be6ca086e6963f35000cc9c82ca02c` |
| RO `.apm/instructions/workspace.instructions.md` | `88bddf525846c8fa1f4dd8ef500632020409a9a3abdc3a59e74a9e8729c4c50e` | `2399c0e96cf03bf9b386d6a1f00ae3afadee2b1d58c21f321765549e27e716b3` |
| RO `package/apm.yml` | `daebf91ef4c8506a309ca7fb1e279decc36183c4ec6238718f59f080ac8a783d` | `2725123da654d58e8e0b3cf72ae302ac683addb08d81df048faa2dc29b3856b9` |
| RO `package/.apm/instructions/library.instructions.md` | `e236df26e1700b25aee4c79922bade77ca14c2c65643a2d485665da083757989` | `bbd17dce3e54d910f4ce715acc9af57e80a18a7ca766a810e454e755db56214c` |
| PB `apm.yml` | `1fc5d2123e1dd9a02f42a17fe062434310780c7d6335a27c56c096cab8a782a4` | `710f7225f8a69bafae35c0a925dcaf4f24b76118161206a5b6dd9a22bd5b879a` |
| PB `.apm/instructions/meridian-engineering.instructions.md` | `54cd3b7369c0b9941d761a9b22edf8e08fd64e5a7795c7cf94f2955aa958dadb` | `d7dcb85632871a9f1667dcfd5667578a7230bb80c2ae17178b1d98418bf52bc0` |
| PB `.apm/prompts/checkout-review.prompt.md` | `6adcf431e4eb89f3773899545c8e98d9696ce1d658ce56b016c4ea2281e50858` | `851711a4c4b3ba13275e8b69cf277c0d14a0ab23a0fa969f6116031f735be01a` |
| PB `.apm/skills/secure-payment-review/SKILL.md` | `11364be3f043fa396a5a2cbf1c26bb908b3409d86b02cfcc2988b021b7b05847` | `1a8d4fa132a7ffd0d70d1872f07943f6fe2bbe00402718edd1dc1a278082762f` |

The authoritative full byte/size/CRLF counts and hashes are in
`line-endings/{li,os,ps,ro,pb}.json`; no canonical fixture file was rewritten.

## Exact APM commands, exits, and runtime

Record IDs resolve to `VerifyRoot/logs/<id>.json`, `.txt`, `.stdout.bin`,
and `.stderr.bin`. Commands are exact arguments after `& $Apm`; CWDs are
under `Scratch/p`.

| Record ID | CWD | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `li-version` | `vli` | `--version` | 0 | 2.416 |
| `li-f-materialize` | `lif` | `install --frozen` | 0 | 5.200 |
| `li-f-audit` | `lif` | `audit --ci` | 0 | 2.773 |
| `li-i-materialize` | `lii` | `install` | 0 | 2.675 |
| `li-i-audit` | `lii` | `audit --ci` | 0 | 2.884 |
| `os-version` | `vos` | `--version` | 0 | 2.389 |
| `os-f-materialize` | `osf` | `install --frozen` | 0 | 5.095 |
| `os-f-audit` | `osf` | `audit --ci` | 0 | 2.804 |
| `os-i-materialize` | `osi` | `install` | 0 | 2.824 |
| `os-i-audit` | `osi` | `audit --ci` | 0 | 2.695 |
| `ps-version` | `vps` | `--version` | 0 | 2.469 |
| `ps-f-materialize` | `psf` | `install --frozen` | 0 | 8.302 |
| `ps-f-audit` | `psf` | `audit --ci` | 0 | 2.788 |
| `ps-i-materialize` | `psi` | `install` | 0 | 3.221 |
| `ps-i-audit` | `psi` | `audit --ci` | 0 | 2.336 |
| `ro-version` | `vro` | `--version` | 0 | 2.300 |
| `ro-f-materialize` | `rof` | `install --frozen` | 0 | 5.328 |
| `ro-f-audit` | `rof` | `audit --ci` | 0 | 2.822 |
| `ro-i-materialize` | `roi` | `install` | 0 | 2.970 |
| `ro-i-audit` | `roi` | `audit --ci` | 0 | 3.225 |
| `pb-version` | `vpb` | `--version` | 0 | 2.240 |
| `pb-f-materialize` | `pbf` | `install --frozen` | 0 | 5.326 |
| `pb-f-audit` | `pbf` | `audit --ci` | 0 | 2.990 |
| `pb-i-materialize` | `pbi` | `install` | 0 | 3.067 |
| `pb-i-audit` | `pbi` | `audit --ci` | 0 | 3.396 |
| `pb-pack-help` | `pbi` | `pack --help` | 0 | 1.944 |
| `pb-zip` | `pbi` | `pack --archive -o dist --verbose` | 0 | 2.459 |
| `zc-version` | `vzc` | `--version` | 0 | 1.578 |
| `zc-init` | `zc` | `init --yes --target copilot,claude,cursor` | 0 | 4.131 |
| `zc-install` | `zc` | `install "$Zip" --target copilot,claude,cursor` | 0 | 2.204 |
| `zc-audit` | `zc` | `audit --ci` | 0 | 2.187 |

The ZIP consumer's init-generated manifest was converted to LF **before**
ZIP installation, using the same CRLF-only transformation and a recorded
scratch mutation. The archive itself was never edited or normalized.

## Why this is not a claim that raw package-tree normalization is harmless

The frozen implementation hashes a package tree from sorted POSIX
relative paths and **raw file bytes**, excluding `.git`, `__pycache__`,
symlinks, and the root `.apm-pin` cache marker. It does **not** normalize
the tree's text. Canonical per-deployment file hashing is a different
operation. Source receipt:
`src/apm_cli/utils/content_hash.py` at
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`;
`VerifyRoot/hash-contract.json`.

Independent calculations demonstrate that the two authored local
dependency trees really change:

| Raw authored package tree | CRLF source tree hash | LF source tree hash |
| --- | --- | --- |
| Onboard skill directory, `SKILL.md` | `sha256:4d9eb397c45b2d8a496e28d8228feb86aa557f52b554458d03493491961997ad` | `sha256:1305137b0743046d94e82d662f3bb4c845c2de004406b3c6e2eb346119c08576` |
| Operations `package/`, manifest + instruction | `sha256:934134a8fa7984e871aa324f308aaf8facb93cff5847879a82e51985502b87ec` | `sha256:4d29ed2b536f0e43309291cfb23e8cbdf9aa63e9b8a15d2b6308dd8a84a73932` |

These particular local dependency lock entries have **no `content_hash`
field**. Their recorded deployment hashes use canonical text, which the
real install/audit commands validated. Root-local instruction and producer
content likewise use their actual local deployment records. A clean result
does not magically equate the two raw trees.

The public Git skill is different: its lock **does** record a raw
package-tree hash. After both materializations an independent calculation
over the actual downloaded package, without text normalization, equals:

```text
sha256:867912713bf45048211440b81ea0ced396ad0a0993447dd540fe5c219722d318
```

The sole hashed package member is `SKILL.md`; the cache marker is excluded
by the frozen contract. The Git commit remains
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`. Normalizing the **consumer
manifest** did not alter the pinned upstream artifact.

Thus the selected locks are checkout-compatible, but this result is **not
permission to normalize arbitrary CRLF-committed upstream packages** with
raw content hashes, regenerate locks silently, or infer Linux behavior.

## Representative producer ZIP round-trip — PASS

The real archive produced from LF Git inputs is preserved as
`VerifyRoot/meridian-standards-1.0.0.zip`.

```text
ZIP SHA256:
6502b46ff1d6784b05e08b74b8ac16b6dc3c68a2655a7df6a420d7d88659d0b7

producer root lock before/after pack:
2b906800526ba3942b583d75db6057551e9101447e733be60ef41a7beb66fe07
```

All five members below are LF. The three primitive payloads equal the
normalized Git source bytes, and every raw payload hash equals the
archive's own `pack.bundle_files` entry.

| Member below `meridian-standards-1.0.0/` | Bytes | SHA256 |
| --- | ---: | --- |
| `apm.lock.yaml` | 2911 | `47b9117e4fd0fb950a6fc820d84faccd0e583448ada7ee212fe61455cf4e0301` |
| `plugin.json` | 229 | `fc0df3ad28613afbc4a403192a7d04d7361838dc4734943b0194bae3f961312d` |
| `commands/checkout-review.md` | 508 | `851711a4c4b3ba13275e8b69cf277c0d14a0ab23a0fa969f6116031f735be01a` |
| `instructions/meridian-engineering.instructions.md` | 503 | `d7dcb85632871a9f1667dcfd5667578a7230bb80c2ae17178b1d98418bf52bc0` |
| `skills/secure-payment-review/SKILL.md` | 755 | `1a8d4fa132a7ffd0d70d1872f07943f6fe2bbe00402718edd1dc1a278082762f` |

The separate, isolated consumer materialized all eight expected files:

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

The init-generated consumer manifest's CRLF SHA256 was
`81edfd370fe0d06708605dd4b00a00743de88b8b2175f39e1af0a2891e40a8d1`.
The recorded CRLF-only conversion produced the LF SHA256
`bbe8d6c2ad19e00c356682fd5f6d7d559c469961a8069626e7001081e7f9ec7d`,
which remained unchanged across ZIP install/audit.
ZIP install created the genuine consumer lock from an initially absent
lock; its SHA256 was then unchanged by audit:
`de47ffc1e7f8349acf342dca8788b98e9ac9260b6b3c8a60bfd85ac5424816ff`.

The archive route remains **imperative**: no archive dependency was added
to the manifest and the consumer lock has empty `dependencies`. This
does not certify declarative ZIP replay. The new ZIP hash is not expected
to equal the earlier CRLF-source ZIP: payload bytes and `packed_at`/archive
metadata legitimately differ. Earlier raw-Windows ZIP evidence remains
valid for its own bytes.

## Attributes, preservation, and handoff

The already-present `Examples/.gitattributes` pins:

```gitattributes
apm.lock.yaml text eol=lf
producer/marketplace/catalog/marketplace.json text eol=lf
```

Git reports `text: set`, `eol: lf` for the tested locks. This preserves
their current genuine LF output bytes; **no fixture or attribute edit
was needed**. The catalog rule was observed, not independently certified
as another example in this primary-fixture task.

At final integrity check (`2026-09-16T03:00:49.928765Z`):

- All five canonical fixture inventories, the attribute file, root
  `apm.yml`/`apm.lock.yaml`, and **all twelve chapter hashes** remain
  unchanged from this task's initial capture.
- All 31 raw command records, version guards, original stdout/stderr bytes,
  and complete resulting snapshots pass integrity checks.
- No previous verification report/raw execution record was rewritten.
  Only this new report and owned checkout evidence were added.

The read-only final integrity check exited **0**, runtime **1.565 s**.
Raw artifacts under `VerifyRoot` include `runtime-layout.json`,
`source-inputs.json`, `git-commands.json`, `line-endings/`,
`workspace-inputs/`, `lf-inputs/`, `inputs/`, `snapshots/`, `logs/`,
`assertions/`, `zip.json`, `zip-consumer.json`, `verification-status.json`,
`command-index.json`, `summary.json`, and `final-source-checks.json`.
Actual absolute argv/CWDs are in raw logs; published paths use aliases.

**Fix recommendation: none for these five fixtures.** Retain explicit LF
checkout for genuine generated locks. No lock regeneration, canonical
source normalization, global config, or chapter restamp is required by
this result.

**SKIPPED-needs-network: none.** Public Git was exercised; local cases
were bounded locally. CI audit here checks the fixtures' baseline content
and recorded state, not unavailable organization-policy authority, live
MCP health, agent behavior, or Linux execution.
