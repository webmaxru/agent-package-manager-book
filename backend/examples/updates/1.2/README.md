# Edition 1.2 examples - APM 0.31.0

These fixtures accompany the reviewed update from APM 0.23.1 to **0.31.0**.
Use the exact prepared CLI in short, disposable project copies, not in the book
repository or a production agent workspace. Copy hidden source directories too.

| Directory | Purpose and reproduction guidance |
| --- | --- |
| `core/local-instruction` | Meridian's minimal instruction, projected to three harnesses. Copy the full fixture and use `apm install`, `apm install --frozen`, and `apm audit --ci`. |
| `core/onboard-skill` | The declared end state after discovering an existing Claude-layout skill. It is not the pre-apply discovery input. |
| `core/pinned-skill` | One public skill at an immutable Git commit; a cold acquisition needs GitHub access. |
| [operations](operations/README.md) | Focused lockfile, lifecycle, policy, hook, MCP, and loopback-registry controls, with an isolated runner. |
| [producer](producer/README.md) | Local-only bundles, explicit plugin formats, catalogs, pinned integration sketches, and no-upload registry preview. |

The `apm.lock.yaml` files are genuine CLI output. Git attributes preserve their
LF bytes, and the generated marketplace catalog's LF bytes, even on Windows.
Ordinary source-file line endings and target-native projection are separate
from the recorded lock and catalog integrity demonstrations. Verification
reports distinguish exact local working-tree hashes from canonical Git bytes.

Read the chapter's input scope: some excerpts are deliberately partial; negative
controls require the described setup; historical 0.23.1 examples are not
automatically current 0.31.0 recipes. The operations runner retains failed
guarantees as explicitly labelled limitations, not successful security outcomes.
Do not suppress those failures to make a demonstration appear green.

Independent command results and editorial gates are under
[`content/research/updates/1.2`](../../../../content/research/updates/1.2).
Raw experiment logs, temporary caches, binaries, and private infrastructure are
not distributed with the fixtures. No example requires a live package
publication or paid agent invocation.
