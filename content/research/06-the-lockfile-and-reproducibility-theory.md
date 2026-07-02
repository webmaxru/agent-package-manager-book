# Concept Brief — Chapter 6: The Lockfile & Reproducibility

- **Chapter:** 6 — The Lockfile & Reproducibility (Part III — Reproducible by lockfile)
- **Objective it serves:** Reproduce an APM setup exactly and explain how the lockfile supports that
  guarantee.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30). Feature/file/field
  names tagged `Implemented in APM by:` are conceptual hand-offs — the `apm-cli-explorer` confirms exact
  fields, `--frozen` behavior, and exit codes; the `code-verifier` runs them. The empirical v0.2.0
  lockfile is already captured in
  [`05-install-and-restore-reference.md`](05-install-and-restore-reference.md) and should be reused, not
  re-invented, here.
- **Frame note (which property this chapter feeds).** This chapter is where **reproducibility** stops
  being a promise and becomes a fact. Chapter 5 realized *portability* — one manifest fanned out into
  every developer's tools — and *seeded* the lockfile as a by-product every install writes. Chapter 6
  turns that by-product into the subject: the lockfile is the artifact that makes "the same manifest"
  mean "the same bytes, on every machine, at every later point in time." It is APM's answer to the
  package-manager-era lesson that **a manifest alone drifts** — the same reason `package-lock.json`,
  `poetry.lock`, and `Cargo.lock` exist ([The three promises →
  "Why a lockfile?"](https://microsoft.github.io/apm/concepts/the-three-promises/)).
- **Prerequisite recap.** Chapter 4 authored `apm.yml`; Chapter 5 ran the install/restore loop and the
  reader *noticed* `apm.lock.yaml` appear, containing `resolved_commit` and content hashes it did not yet
  study. Chapter 6 answers the question Chapter 5 deliberately deferred: *"What is that lockfile, and why
  does bare `apm install` reproduce the same bytes instead of chasing whatever `main` points to today?"*
- **Scope boundary with Chapter 7.** This chapter covers the lockfile as a **reproducibility contract**:
  what it records, byte-for-byte restore, `apm install --frozen` as the CI gate, and the fact that the
  lockfile is *generated, never hand-edited*. The chapter's closing beat — the team *decides to update
  intentionally* — is a **hand-off to Chapter 7** (`apm outdated` / `apm update` / `apm audit` as
  deliberate change). Name `apm update` here as the intentional-change door; develop it in Chapter 7. The
  running example's `apm update --dry-run` / `apm update --yes` commands belong to that hand-off.

---

## Concepts covered

1. **Why a manifest isn't enough** — version ranges and moving branches resolve to *different* artifacts
   over time and across machines; the lockfile pins the exact resolved graph so a later restore matches
   known-good. This is the *reproducibility* property made concrete.
2. **Exact versions + content hashes** — the lockfile records the resolved commit *and* content hashes,
   so "the same prompt/skill" means "the same bytes." Three levels of identity: `resolved_ref` (what you
   asked for) → `resolved_commit` (what it resolved to) → `content_hash` (what the bytes actually are).
3. **Byte-for-byte restore & `--frozen`** — the lockfile is the reproducibility contract; `apm install
   --frozen` reproduces it exactly (CI-safe) and *fails* when the manifest and lockfile disagree.
   Lockfile changes are reviewed like application-dependency changes.
4. **Generated, never hand-edited** — you change the manifest; APM regenerates the lockfile; the diff
   tells the review story.

---

## Concept 1 — Why a manifest isn't enough (the manifest resolves; the lockfile freezes)

**Definition.** A manifest declares *intent* — often a **range or a moving target**, not an exact
artifact. APM lets a dependency's `ref:` be a branch (`main`), a tag (`v1.2.0`), a commit SHA, or a
**semver range** (`^1.2.0`, `~1.4`, `>=2.0 <3`, `1.5.x`); for a range, "APM runs `git ls-remote` against
the dep, picks the highest tag matching the range, and pins the resolved tag plus commit SHA, version,
and original constraint in `apm.lock.yaml`" ([apm
install](https://microsoft.github.io/apm/reference/cli/install/)). The **lockfile** is the record of that
resolution: the exact commit each declared dependency *resolved to at lock time*, for the whole
transitive graph. Where the manifest says "give me something matching this," the lockfile says "here is
exactly what you got."

**The problem it solves.** Intent and resolution drift apart. A branch pointer moves with every upstream
push; a range admits whatever tag is newest when you happen to run `git ls-remote`. Two developers who
install from the *same* manifest a week apart — or a laptop and a CI runner installing the *same* minute
— can therefore resolve *different* bytes. That is the agent-context version of "works on my machine."
The lockfile closes the gap: it turns a resolvable declaration into a **frozen graph**, so a later
install *replays* the recorded commits instead of re-resolving. "Subsequent installs replay the lockfile
without network; use `--update` (or change the manifest constraint) to re-resolve" ([apm
install](https://microsoft.github.io/apm/reference/cli/install/)). This is precisely the four-things
purpose the lockfile spec opens with: "**Reproducibility.** `apm install --frozen` reinstalls the exact
commits recorded here — no resolution, no network drift" ([Lockfile
specification](https://microsoft.github.io/apm/reference/lockfile-spec/)).

**Key distinctions.**
- *Manifest = resolvable intent; lockfile = resolved fact.* The manifest can float (`#main`, `^1.2.0`);
  the lockfile cannot — every entry carries a concrete `resolved_commit`, "the pin" ([Lockfile
  specification](https://microsoft.github.io/apm/reference/lockfile-spec/)).
- *The lockfile covers the whole graph, not just your top-level entries.* "`apm install` resolves the
  full dependency graph, not just your top-level entries. Versions and content hashes are pinned in
  `apm.lock.yaml` so every contributor and CI run installs the exact same bytes" ([Install
  packages](https://microsoft.github.io/apm/consumer/install-packages/)). This is why an *unpinned*
  transitive edge still restores deterministically — see the Meridian beat.
- *Reproducibility ⟂ freshness.* Pinning is not staleness. The lockfile guarantees *the same* bytes on
  replay; deliberately moving to *newer* bytes is a separate, consent-gated act (`apm update`, Chapter
  7). Conflating "restore the locked graph" with "get the latest" is the misconception this whole part
  is built to prevent.

**Common misconception.** *"If everyone installs from the same `apm.yml`, they get the same context."*
Not over time. A manifest with a branch ref or a range is a *recipe whose ingredients change*; without a
committed lockfile, "the same manifest" silently means "whatever `main` resolved to when you ran it." The
manifest makes the setup *portable*; only the lockfile makes it *reproducible*.

**Meridian beat (for the author).** This is the chapter's opening pain. In Chapter 5 the team's direct
dependency was pinned (`microsoft/apm-sample-package#v1.0.0`), but it pulled a **transitive** skill from
`github/awesome-copilot` that resolved **unpinned** — APM even warned: `[!] 1 dependency unpinned … add
#tag or #sha to prevent drift`
([`05-install-and-restore-reference.md`](05-install-and-restore-reference.md)). Chapter 6 shows *why that
warning matters and why restore still worked*: the manifest edge floats, but the lockfile pinned that
skill by `resolved_commit`, so every restore reproduced it. The drift risk lives in the *next*
re-resolution, not in restore — exactly the seam the lockfile is designed to hold.

**Implemented in APM by:** `apm.lock.yaml` (the frozen resolved graph); the `resolved_commit` pin per
entry; replay-without-re-resolution on bare `apm install`; the `constraint` / `resolved_tag` fields that
record how a semver range was pinned. (Exact replay behavior and range-pinning fields confirmed by the
explorer; the empirical graph is in the Ch5 reference.)

---

## Concept 2 — Exact versions + content hashes ("the same prompt means the same bytes")

**Definition.** Each lockfile entry records identity at **three levels**, and keeping them separate is
the heart of the chapter:

| Level | Field | What it captures | The question it answers |
|---|---|---|---|
| Intent | `resolved_ref` | "The user-supplied ref from `apm.yml` (`main`, `v1.2.0`, a SHA)" | *What did you ask for?* |
| Resolution | `resolved_commit` | "Exact 40-char commit SHA installed. **The pin.**" | *What did it resolve to?* |
| Content | `content_hash` / `deployed_file_hashes` | SHA-256 over the package tree / per deployed file | *What are the bytes, exactly?* |

Field definitions quoted from the [Lockfile
specification](https://microsoft.github.io/apm/reference/lockfile-spec/). The content layer is what makes
"reproducible" mean *byte-for-byte*, not merely "same commit": the three-promises page cites
`LockEntry.content_hash` — "SHA-256 of the package file tree — that makes 'same install on every clone'
mean byte-for-byte the same" ([The three
promises](https://microsoft.github.io/apm/concepts/the-three-promises/)).

**The problem it solves.** A commit SHA answers *where* the content came from; a content hash answers
*what the content is*. Agent context is executable — "a prompt is a program for an LLM" ([The three
promises](https://microsoft.github.io/apm/concepts/the-three-promises/)) — so "the same review prompt"
has to mean the same *characters*, not just the same source pointer. The two hashes give APM a
falsifiable definition of "same": if the recorded hash and the on-disk bytes differ, something changed,
full stop. That is the basis of both reproducibility (every clone lays down bytes matching the hash) and
integrity ("`content_hash` lets `apm audit` detect any drift between what the lockfile says you installed
and what is on disk right now — including hand-edits to files inside `apm_modules/`" — [The three
promises → "Why a lockfile?"](https://microsoft.github.io/apm/concepts/the-three-promises/)).

**Key distinctions.**
- *`resolved_ref` vs. `resolved_commit`.* The ref is your *request* and can be a moving name; the commit
  is the *immutable* 40-char SHA it resolved to. A ref like `main` stays `main` in the manifest while its
  `resolved_commit` changes only when you deliberately re-resolve.
- *`resolved_commit` vs. `content_hash`.* The commit identifies a point in a repo's history; the content
  hash identifies the *bytes actually deployed*. They usually move together, but the content hash is the
  layer `apm audit` checks for tampering — the commit can't detect a local hand-edit; the hash can.
- *Package-level vs. per-file hashing.* The lockfile pins content at more than one granularity —
  `deployed_file_hashes` is a "path → sha256" map that "powers audit's content-integrity check," and it
  is deliberately computed over **canonical** content: "UTF-8 text is normalized CRLF → LF … so the hash
  is the same whether git checks the file out with Windows or POSIX line endings" ([Lockfile
  specification](https://microsoft.github.io/apm/reference/lockfile-spec/)). "Same bytes" therefore means
  *same canonical content*, which is what lets a Windows laptop and a Linux CI box agree.
- *Hashes are metadata you trust; names are metadata you don't.* The spec is blunt that `name`/`version`
  are "SELF-ASSERTED author-claim metadata — NOT integrity-verified … Always cross-reference `repo_url` +
  `resolved_commit` (or `resolved_hash`) for provenance" ([Lockfile
  specification](https://microsoft.github.io/apm/reference/lockfile-spec/)). Reproducibility rests on the
  commit and the hash, not on a package's self-reported version string.

**Common misconception.** *"Pinning the version (or the commit) is enough."* A version string is a label
the author controls and can silently re-point; even a commit only says *which* source, not *what bytes
landed*. Only the content hash makes "the same skill" verifiable at the byte level — which is why the
lockfile records both the pin and the hash rather than trusting either alone.

**Meridian beat (for the author).** Use the artifact the team already has: the Ch5 lockfile shows
`microsoft/apm-sample-package` with `resolved_ref: v1.0.0`, `resolved_commit: fb2851683b…`, and
`content_hash: sha256:744cca54…` — three lines that say, in order, *"we asked for the v1.0.0 tag, it
pointed at this exact commit, and these are the exact bytes"*
([`05-install-and-restore-reference.md`](05-install-and-restore-reference.md)). The same lockfile shows
one review prompt deployed to three harnesses sharing **one identical hash** — concrete proof that "one
source primitive → many harness files" is still *one* set of bytes.

**Implemented in APM by:** the per-entry `resolved_ref`, `resolved_commit`, and `content_hash` fields;
`deployed_file_hashes` (per-file SHA-256 over canonical, line-ending-normalized content); `resolved_hash`
for registry archives. (Which hash fields appear on which dependency kinds in v0.23.1 — and the Ch5 note
that *local* file hashes can vary by environment while the *dependency* `content_hash`/`resolved_commit`
are fixed — are for the explorer to confirm against
[`05-install-and-restore-reference.md`](05-install-and-restore-reference.md).)

---

## Concept 3 — Byte-for-byte restore & `--frozen` (the reproducibility contract)

**Definition.** Bare `apm install` *restores* from the lockfile — it replays the recorded commits and
lays down the recorded bytes (Chapter 5's idempotent, cache-served no-op). `apm install --frozen` is the
**strict, CI-safe** form of that restore: a "lockfile-only install: refuse to resolve anything new and
fail if `apm.yml` and `apm.lock.yaml` have drifted. Mirrors `npm ci`" ([apm
install](https://microsoft.github.io/apm/reference/cli/install/)). Concretely: "With `--frozen`, install
resolves only what is in `apm.lock.yaml`. A direct dependency missing from the lockfile, or a missing
lockfile entirely, exits `1`" ([apm install](https://microsoft.github.io/apm/reference/cli/install/)).
The lockfile spec frames this as the file's first job: "`apm install --frozen` reinstalls the exact
commits recorded here — no resolution, no network drift" ([Lockfile
specification](https://microsoft.github.io/apm/reference/lockfile-spec/)).

**The problem it solves.** Reproducibility is only *real* if something enforces it. A regular install is
forgiving — if `apm.yml` gained a dependency that isn't locked yet, it will resolve and lock it for you.
That convenience is exactly wrong in CI, where a passing build must prove that *what's committed* is
internally consistent. `--frozen` makes the lockfile a **contract**: install refuses to invent a
resolution, so a manifest that has drifted from its lockfile *fails the build* instead of silently
"fixing" itself and masking an un-reviewed change. The consumer guidance is explicit — "`apm install
--frozen`  # CI: lockfile-only; fail on drift" and "Fail fast on any drift; never bypass policy in CI"
([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)).

**Key distinctions.**
- *Restore vs. strict restore.* Bare `apm install` will resolve-and-lock a newly-added manifest entry;
  `--frozen` will not — it treats any manifest↔lockfile disagreement as a failure. Both reproduce; only
  `--frozen` *refuses to paper over drift*.
- *`--frozen` is a **structural** check, not a content check.* This is the load-bearing nuance: "This is
  a structural check, not a content check — run `apm audit --ci` for hash verification" ([apm
install](https://microsoft.github.io/apm/reference/cli/install/)). `--frozen` guarantees the *right
  commits are present and the manifest agrees with the lockfile*; verifying that the *deployed bytes*
  still match the recorded hashes is `apm audit`'s job (Chapters 7–8). The chapter should pair them
  conceptually: `--frozen` = "the graph is the locked graph"; `apm audit --ci` = "the bytes are the
  locked bytes."
- *Tolerant where it should be.* "Orphan lockfile entries (locked but no longer in `apm.yml`) are
  tolerated; local-path deps are skipped" ([apm
  install](https://microsoft.github.io/apm/reference/cli/install/)). `--frozen` fails on *missing* pins,
  not on *extra* ones.
- *Lockfile changes are reviewed like code.* Because *add* and *update* both rewrite `apm.lock.yaml`, the
  diff surfaces in the pull request. A lockfile change is a dependency change; review it with the same
  seriousness as a `package-lock.json` diff — the outline's leader beat: if a team "cannot say which
  agent context produced a change, it cannot confidently investigate regressions or satisfy audit
  questions."

**Common misconception.** *"`--frozen` verifies my installed files are untampered."* No — `--frozen` is a
*structural* gate (lockfile present, manifest and lockfile agree, pins resolvable). Byte-level integrity
against the recorded hashes is `apm audit --ci`. Treating `--frozen` as a content check is the one error
the chapter must head off, because it's the intuitive-but-wrong reading.

**Meridian beat (for the author).** This is the chapter's headline story. Priya adds a branch-pinned
dependency and pushes **without committing the regenerated lockfile**. CI runs `apm install --frozen`;
because `apm.yml` now names something the committed `apm.lock.yaml` doesn't pin, the manifest and lockfile
*disagree* and the job **fails** — reproducibility caught the drift instead of shipping it. The fix is not
to hand-fix the lockfile: the team runs `apm install` (or `apm update`) locally to **regenerate** it,
**reviews the lockfile diff** in the PR, and commits it. Then `--frozen` passes because manifest and
lockfile agree again. (The "should we take the newer version at all?" decision hands off to Chapter 7.)

**Implemented in APM by:** bare `apm install` (restore / replay); `apm install --frozen` (strict,
`npm ci`-parity restore — fails on missing lockfile or manifest↔lockfile drift, exit `1`; structural, not
content); `apm audit --ci` (the *content*-integrity companion, Chapters 7–8); the reviewed
`apm.lock.yaml` diff. (Exact `--frozen` failure modes, exit codes, and the frozen-vs-audit split confirmed
by the explorer.)

---

## Concept 4 — The lockfile is generated, never hand-edited

**Definition.** `apm.lock.yaml` is a **build product of resolution**, not an authored file. You edit
`apm.yml`; APM writes the lockfile. The commands that (re)generate it are `apm install` (writes it as
pipeline phase 5 — "Write `apm.lock.yaml` with pinned versions, content hashes, and the resolved
dependency set" — [Install packages](https://microsoft.github.io/apm/consumer/install-packages/)) and the
dedicated `apm lock`, which "runs the full resolver and downloader so every dependency SHA is pinned,
then writes `apm.lock.yaml`" **without deploying any files** ([apm
lock](https://microsoft.github.io/apm/reference/cli/lock/)). `apm lock` exists precisely so you can
"refresh the lockfile after editing `apm.yml` … so you can review the new lockfile before applying it"
and "verify that `apm.yml` resolves cleanly (useful in PR checks)" — it "mirrors the ergonomics of
`cargo generate-lockfile` and `pnpm lock`" ([apm
lock](https://microsoft.github.io/apm/reference/cli/lock/)).

**The problem it solves.** If the lockfile were something people hand-edited, it would stop being
trustworthy — its whole value is that it is a *faithful, mechanical record* of what resolution produced.
Making it generated-only means the **review story lives in the diff**: change the manifest, regenerate,
and the lockfile diff shows exactly which commits and hashes moved as a consequence. It also makes the
lockfile *self-healing* rather than a fragile hand-maintained artifact: "A lockfile that fails to parse
is treated as absent — APM logs the error and, for non-frozen installs, proceeds to regenerate from
`apm.yml`" ([Lockfile specification](https://microsoft.github.io/apm/reference/lockfile-spec/)). And it
keeps diffs meaningful: "`apm install` only rewrites the file when its semantic content changes
(`generated_at` and `apm_version` are ignored when comparing). A no-op install leaves the file
untouched" ([Lockfile specification](https://microsoft.github.io/apm/reference/lockfile-spec/)).

**Key distinctions.**
- *You author intent; APM authors the record.* The manifest is the human surface (hand-written, reviewed
  as intent); the lockfile is the machine surface (generated, reviewed as *consequence*). Editing the
  lockfile to "fix" a problem inverts the flow — fix the manifest and regenerate instead.
- *`apm lock` vs. `apm install`.* Both write the lockfile, but `apm lock` **resolves and pins without
  deploying** — "no files are copied to `.github/`, `.agents/`, or any other harness directory" ([apm
  lock](https://microsoft.github.io/apm/reference/cli/lock/)). It's the "regenerate and review before I
  touch my working tree" tool, ideal for a PR check; `apm install` regenerates *and* materializes.
- *`apm lock` (regenerate) vs. `apm update` (re-resolve to newer).* Plain `apm lock` pins the *current*
  resolution of the manifest; `apm lock --update` (like `apm install --update` / `apm update`) re-resolves
  to *newer* matching SHAs ([apm lock](https://microsoft.github.io/apm/reference/cli/lock/)). Regenerating
  to reflect a manifest edit is Chapter 6; deliberately moving versions is Chapter 7.
- *Never author the synthesized parts.* Even the internal "self entry" APM builds for a project's own
  primitives is explicitly off-limits: "Treat the self entry as an implementation detail; do not author
  it by hand" ([Lockfile specification](https://microsoft.github.io/apm/reference/lockfile-spec/)).

**Common misconception.** *"CI fails on a lockfile mismatch, so I'll just edit `apm.lock.yaml` to match."*
That defeats the contract: the lockfile is only trustworthy because it is *derived*. The correct fix for
`--frozen` drift is to change the manifest (if needed) and **regenerate** — `apm install` or `apm lock` —
then commit the resulting diff. Hand-editing produces a lockfile that no resolution actually created.

**Meridian beat (for the author).** Closing the CI story from Concept 3: the team does **not** hand-patch
`apm.lock.yaml` to make CI green. They regenerate it (`apm install`, or `apm lock` to review before
deploying), read the diff — which shows exactly the new dependency's `resolved_commit` and `content_hash`
— approve it in the PR like any other dependency change, and commit. The lockfile stays a *record*, and
the PR history can now answer "which agent context produced this build?" precisely.

**Implemented in APM by:** `apm install` (regenerates the lockfile as pipeline phase 5, only on semantic
change); `apm lock` (resolve-and-pin *without* deploying — the review/PR-check regenerator; `cargo
generate-lockfile` / `pnpm lock` analogue); parse-fail-means-regenerate for non-frozen installs; the
reviewed lockfile diff as the change story. `apm update` / `apm lock --update` (re-resolve to newer) are
named here but developed in Chapter 7. (Exact `apm lock` phases, no-deploy guarantee, and regeneration
triggers confirmed by the explorer.)

---

## Notes for the `apm-cli-explorer` (what to confirm for Chapter 6)

1. **`--frozen` failure surface on v0.23.1.** Confirm the two failure triggers (missing/unparseable
   lockfile; a direct dep in `apm.yml` absent from `apm.lock.yaml`) both exit `1`, and that *orphan*
   lockfile entries and local-path deps are tolerated/skipped. Capture the actual teaching message for a
   manifest↔lockfile drift so the author can quote a real terminal block for Priya's CI failure.
2. **Structural vs. content split.** Verify empirically that `--frozen` does **not** re-hash deployed
   files (structural only) and that `apm audit --ci` is the command that flags a hand-edited file via
   `deployed_file_hashes`. The chapter's central pairing depends on this being exactly right.
3. **`apm lock` no-deploy.** Confirm `apm lock` writes/refreshes `apm.lock.yaml` while touching no harness
   directory, and that `apm lock` vs. `apm lock --update` is the regenerate-vs-re-resolve distinction.
4. **Which hash fields appear per dependency kind.** Reconcile the spec (`content_hash` described for
   path deps; `resolved_hash` for registry; `deployed_file_hashes` per deployed file) with what v0.23.1
   actually emitted for the git-source `microsoft/apm-sample-package` in
   [`05-install-and-restore-reference.md`](05-install-and-restore-reference.md) (which shows a
   `content_hash` on a git dep). Give the author one clear sentence on what a reader will see.
5. **Reuse the captured lockfile.** The v0.2.0 lockfile is already verified; the worked example should
   *evolve* it (Priya's drift → regenerate → diff), not author a new one from scratch.

---

## Sources

Official APM documentation — reference (primary for this chapter):
- Lockfile specification (the four purposes; per-entry fields `resolved_ref` / `resolved_commit` /
  `content_hash` / `deployed_file_hashes`; canonical line-ending-normalized hashing; self-asserted
  `name`/`version` caveat; "do not author by hand"; parse-fail-regenerate; no-op leaves file untouched;
  normative contract is OpenAPM v0.1 §5) —
  <https://microsoft.github.io/apm/reference/lockfile-spec/>
- apm install (`--frozen` = `npm ci` parity; frozen resolves only the lockfile, exits `1` on missing
  lockfile or absent direct dep; **structural not content** check → `apm audit --ci`; semver-range
  pinning to tag + commit SHA; replay-without-network) —
  <https://microsoft.github.io/apm/reference/cli/install/>
- apm lock (resolve-and-pin without deploying; bootstrap / refresh-and-review / PR-check use cases;
  `cargo generate-lockfile` / `pnpm lock` ergonomics; `--update` re-resolves) —
  <https://microsoft.github.io/apm/reference/cli/lock/>

Official APM documentation — consumer ramp:
- Install packages (pipeline phase 5 writes pinned versions + content hashes + resolved set; "the exact
  same bytes"; `--frozen` "CI: lockfile-only; fail on drift"; "never bypass policy in CI"; commit the
  lockfile) — <https://microsoft.github.io/apm/consumer/install-packages/>

Official APM documentation — concepts (framing):
- The three promises (Promise 1 "the lockfile pins exact versions and content hashes"; `LockEntry.
  content_hash` = "byte-for-byte the same"; FAQ "Why a lockfile?" = reproducibility + integrity) —
  <https://microsoft.github.io/apm/concepts/the-three-promises/>

Internal artifacts (reuse, do not re-derive):
- Chapter 5 CLI reference — the verified v0.2.0 `apm.lock.yaml` with real `resolved_ref` /
  `resolved_commit` / `content_hash` values and the unpinned-transitive wrinkle —
  [`05-install-and-restore-reference.md`](05-install-and-restore-reference.md).

---

## Artifact path

`content/research/06-the-lockfile-and-reproducibility-theory.md`
