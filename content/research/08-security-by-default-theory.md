# Concept Brief — Chapter 8: Security by Default

- **Chapter:** 8 — Security by Default (Part IV — Secure & governed)
- **Objective it serves:** Understand and rely on APM's install-time security checks without confusing
  them with runtime sandboxing.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30; the executable-trust
  gate landed in v0.22, "Executable Trust Governance"). Feature/file/command names tagged
  `Implemented in APM by:` are conceptual hand-offs — the `apm-cli-explorer` confirms exact flags, block
  messages, severity tables, and exit codes; the `code-verifier` runs them.
- **Frame note (which property this chapter feeds).** This chapter delivers the **provenance / security**
  property and APM's second promise, *secure by default*. Chapters 4–5 made context **portable**;
  Chapters 6–7 made it **reproducible**. Chapter 8 asks the question those chapters set up but did not
  answer: *when untrusted context flows from a git source onto my disk, what stops something dangerous
  from reaching the agent?* APM's answer is a **pre-deploy gate** — it scans, pins, and blocks *before*
  files land in agent-readable directories
  ([Security model](https://microsoft.github.io/apm/enterprise/security/)).
- **Prerequisite recap.** Chapter 6 introduced the lockfile's `content_hash` (SHA-256 of the package
  tree) as a *reproducibility* device; Chapter 7 introduced `apm audit` as the explicit integrity/safety
  tool (hidden-Unicode + drift, **not** a CVE feed). Chapter 8 reframes both as **security** mechanisms:
  the same content hash that guarantees "same bytes" also *detects tampering*, and the same audit scan
  that runs on demand also runs **automatically on every install**. This chapter names the built-in
  defaults; Chapter 9 makes them configurable org policy.
- **Scope boundary with Chapter 9 (security defaults vs. governance policy).** Chapter 8 is the
  **always-on, built-in security posture** every `apm install` applies with no configuration: the Unicode
  scan, content-hash verification, transitive-MCP block, and executable-trust gate. Chapter 9 is the
  **configurable governance layer** (`apm-policy.yml`) an organization *adds on top*: allow/deny lists,
  scope rules, warn→block rollout. Keep the line sharp — security answers *"is this safe?"*; governance
  answers *"is this allowed here?"* ([The three
  promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). The transitive-MCP block
  exists **even with no policy file present**; that is why it belongs to this chapter.
- **The accuracy trap to reinforce up front (from Chapter 1).** APM is an **install-time integrity and
  governance layer, not a runtime sandbox.** The docs are blunt: *"apm-policy.yml governs what gets
  installed; your agent harness governs what runs. The two planes do not overlap"*
  ([microsoft/apm README](https://github.com/microsoft/apm)). Every claim in this chapter must stay on
  the install side of that line. Concept 4 makes the boundary explicit; the author should not let
  Concepts 1–3 drift across it.

---

## Concepts covered

1. **A prompt is a program for an LLM** — agent context is *executable*: instructions, prompts, skills,
   and MCP declarations shape what an agent writes and which tools it can reach. That makes unvetted
   context — and undeclared transitive MCP servers — real **supply-chain surface**, the same class of
   risk a poisoned npm package is.
2. **The trust boundary is install time** — agent config has **no install→run gap**: the moment a file
   lands in `.github/prompts/` or `.claude/agents/`, a watching harness may already ingest it. *File
   presence is execution.* So installation is the one chokepoint where APM can scan, pin, and block
   *before* content touches disk.
3. **Install-time security mechanisms** — three built-in, always-on defaults (plus the executable-trust
   gate): **hidden-Unicode scanning** (invisible/bidi characters = a prompt-injection vector),
   **content-hash pinning** (lockfile hashes prove the bytes didn't change), and **transitive MCP
   blocking** (undeclared MCP servers pulled by a dependency are blocked unless explicitly declared or
   trusted).
4. **Not a runtime sandbox** — APM gates what gets **installed**; the harness governs what **runs**. This
   is a pre-deploy gate, not endpoint security. Naming the limits (no plain-text-injection detection, no
   malware analysis, no package signing, no runtime MCP sandboxing) is what keeps the promise honest.

---

## Concept 1 — A prompt is a program for an LLM (agent context is supply-chain surface)

**Definition.** Agent context is not inert documentation; it is **executable input to a model**. APM
states the premise directly: *"Agent context is executable — a prompt is a program for an LLM. APM treats
it that way"* ([The three
promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). A skill tells an agent *how* to
do a task, an instruction file steers *every* generation, a prompt is a runnable procedure, and an MCP
server grants *tool and data access*. Installing an agent package therefore imports behavior — the same
way importing an npm package imports code — which makes its **provenance** (where it came from) and its
**content** (what it actually says) security-relevant, not merely stylistic.

**The problem it solves.** Framing context as "just some markdown" is the mistake that makes teams
careless. If a prompt is a program, then an *unvetted* prompt is unreviewed code running against your
codebase through an agent, and an *undeclared transitive MCP server* is an unaudited capability grant —
network access, filesystem access, tool calls — that arrived as a side effect of installing something
else. Chapter 1 already named this: *"a prompt is, in effect, a program for an LLM, so an unvetted prompt
or transitive MCP server is real supply-chain surface"*
([the-context-problem.html](../chapters/the-context-problem.html)). Concept 1's job is to make that
intuition rigorous *before* any mechanism is shown, so the mechanisms read as inevitable responses to a
real threat rather than ceremony.

**Key distinctions.**
- *Executable ≠ compiled.* "Executable" here means *interpreted by a model at read time*, not "runs a
  binary." A prompt never spawns a process on your machine; it changes what the *agent* does. That is a
  different — and, for a coding agent with tool access, comparably consequential — execution surface.
- *Provenance vs. content.* Two independent questions: *where did this come from?* (a pinned commit at a
  named host — Chapter 6's `resolved_commit`) and *what does it actually say?* (the exact bytes — the
  content hash and the Unicode scan). Supply-chain safety needs both; a trusted source can still ship
  tainted bytes, and clean bytes from an unknown source are still unaccountable.
- *The MCP surface is the sharpest edge.* Skills and prompts influence *generation*; an MCP server grants
  *capabilities*. A malicious instruction is bad; a silently-added MCP server that can reach your network
  or filesystem is worse, because it widens what the agent can *do*, not just what it might *say*. This
  is why transitive MCP gets its own default block (Concept 3).

**Common misconception.** *"It's just prompt text in a repo — reviewing it is a style nicety, not a
security control."* The opposite: because the model acts on that text (and on the tools MCP declarations
wire up), reviewing agent context is a supply-chain control of the same *kind* as reviewing a
dependency's code — different in mechanism, identical in stakes.

**Meridian beat (for the author).** Open on the stakes, not the tool. A teammate finds a genuinely useful
internal package — `checkout-review-pack` — that would sharpen the team's review prompt. It looks like
harmless markdown. But it *depends on* a GitHub MCP server the team never chose, which would gain tool
access the moment it installed. The point to land: the danger isn't hypothetical malware; it's an
ordinary-looking, useful package quietly bringing a **capability** along for the ride. That reframes the
rest of the chapter — Meridian isn't paranoid, it's treating context like the dependency it is.

**Implemented in APM by:** the *provenance* half — `apm.lock.yaml`'s `resolved_commit` (pinned commit at a
named host, Chapter 6) — and the *content/capability* half — the built-in install scan, `content_hash`
verification, and the MCP trust model (Concept 3). (The "prompt is a program" framing is APM's own; the
explorer confirms which lockfile fields carry provenance for git vs. registry deps.)

---

## Concept 2 — The trust boundary is install time (file presence is execution)

**Definition.** For agent context, **installation is the security chokepoint** — the one moment APM
controls before content becomes live. APM explains why this differs from ordinary package managers:
*"Traditional package managers install code that sits inert until a developer or CI pipeline explicitly
executes it. Between `npm install` and `npm start`, there is a gap — time for `npm audit`, code review,
and policy checks. Agent configuration has no such gap. The moment a skill, instruction, or prompt file
lands in `.github/prompts/` or `.claude/agents/`, any IDE agent watching the filesystem — Copilot,
Cursor, Claude Code — may already be ingesting it. There is no 'execution step.' **File presence IS
execution.**"* Its conclusion: *"APM treats package deployment as a pre-deployment gate: scan first,
deploy only if clean"* ([Security model](https://microsoft.github.io/apm/enterprise/security/)).

**The problem it solves.** If there is no gap between install and execution, then a post-install audit is
*too late* — by the time you run it, a watching harness may already have read the tainted file. The only
place a check can be *preventive* rather than *forensic* is **before the bytes reach an agent-readable
directory**. APM moves the gate there: during `apm install`, source files staged in `apm_modules/` are
scanned *before any integrator copies them* to `.github/`, `.claude/`, `.cursor/`, etc. — a
`download → scan source → block or deploy → report` pipeline
([Security model](https://microsoft.github.io/apm/enterprise/security/)). This is also why the protection
cannot be opt-in: it *"already runs automatically in `apm install`, `apm compile`, and `apm unpack`; you
do not need to call `apm audit` to be safe by default"*
([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)).

**Key distinctions.**
- *Pre-deploy gate vs. post-install audit.* The built-in install scan is **preventive** — it blocks
  before deploy. `apm audit` (Chapter 7) is the **on-demand re-verification** power tool and the CI gate.
  Same underlying scan; different moment. Safety-by-default lives in install, *not* in remembering to run
  audit.
- *"Install→run gap" is the load-bearing contrast with npm.* The whole reason APM's security model looks
  different from `npm audit` is this missing gap. The author should make the contrast explicit: npm can
  afford a separate audit step because code waits to be run; APM cannot, because context is read on sight.
- *Cached-but-not-deployed is the safe failure state.* When the gate blocks, the package is still
  downloaded and cached under `apm_modules/owner/package/` *so you can inspect it* — *"nothing reaches
  agent-readable directories"* ([Security
  model](https://microsoft.github.io/apm/enterprise/security/)). Blocking means "not deployed," not "lost."

**Common misconception.** *"I'll install now and audit later, like `npm install` then `npm audit`."* There
is no "later" that is still safe — a watching harness can ingest a freshly written file immediately. APM's
model deliberately front-loads the check to install time *because* the audit-later habit does not
translate to executable-on-arrival context.

**Meridian beat (for the author).** Make the timing visceral: had `checkout-review-pack` deployed its
files first and let the team "review them next sprint," Priya's Cursor session could have picked up the
new prompt — and the MCP capability — the instant the files hit `.cursor/`. Instead, `apm install` stops
at the gate and reports the block, so the risky content sits in `apm_modules/` for inspection and never
reaches a harness. Nothing executed because nothing was deployed.

**Implemented in APM by:** the built-in `_pre_deploy_security_scan` inside `apm install` (source files
scanned in `apm_modules/` before integration; critical findings block and exit `1`; the same scan runs in
`apm compile`, `apm unpack`); `--force` as the explicit, logged override; `apm audit`
[`--strip`] as the on-demand/remediation surface. (Exact block wording, per-package continue-on-block
behavior, and the multi-package exit-code aggregation confirmed by the explorer against v0.23.1.)

---

## Concept 3 — Install-time security mechanisms (scan, pin, block)

**Definition.** "Secure by default" is not a slogan; it is three concrete, always-on checks plus a fourth
gate for executables. APM's own summary: each install *"scans for invisible Unicode that can hijack agent
behavior, pins content hashes in the lockfile, and blocks transitive MCP servers unless they are
explicitly declared or trusted"* ([The three
promises](https://microsoft.github.io/apm/concepts/the-three-promises/)).

**(a) Hidden-Unicode scanning — the invisible-instruction vector.** LLMs tokenize characters a human
never sees on screen, so invisible Unicode is a genuine prompt-injection surface. APM scans deployed
prompt/instruction/skill/rules files for it: *"Researchers have found hidden Unicode characters embedded
in popular shared rules files. Tag characters (U+E0001–E007F) map 1:1 to invisible ASCII. Bidirectional
overrides can reorder visible text. … The Glassworm campaign (2026) exploited this mechanism to compromise
repositories and VS Code extensions. LLMs tokenize all of these individually, meaning models process
instructions that developers cannot see on screen"* ([Security
model](https://microsoft.github.io/apm/enterprise/security/)). Findings are severity-ranked: **critical**
(tag characters, bidi overrides, the Glassworm variation-selector vector) *block* the install; **warnings**
(zero-width spaces/joiners, mid-file BOM) are non-blocking and reported; `apm audit --strip` remediates in
place while preserving legitimate emoji ([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)).

**(b) Content-hash pinning — tamper detection.** The lockfile's `content_hash` (Chapter 6's reproducibility
field) does double duty as an integrity check. *"APM computes a SHA-256 hash of each downloaded package's
file tree and stores it in `apm.lock.yaml` as `content_hash`. On subsequent installs, cached packages …
are verified against the lockfile hash. When the on-disk tree no longer matches, APM … re-downloads. If
freshly downloaded content still does not match the lockfile record, the install aborts (possible
supply-chain tampering)"* ([Security model](https://microsoft.github.io/apm/enterprise/security/)). Same
field, second job: reproducibility says *"same bytes on every clone,"* integrity says *"and I can prove
nobody changed them."*

**(c) Transitive MCP blocking — no silent capability grants.** Trust is scoped by dependency depth.
*"MCP servers declared by your direct dependencies (packages listed in your `apm.yml`) are auto-trusted.
You explicitly chose to depend on these packages."* But *"MCP servers declared by transitive dependencies
… are blocked by default. Transitive MCP servers can request tool access, file system permissions, or
network capabilities — blocking them ensures that adding a prompt package cannot silently grant MCP access
to an unknown transitive dependency."* Two sanctioned escape hatches: *"Re-declare the dependency in your
own `apm.yml`, promoting it to a direct dependency,"* or *"Pass `--trust-transitive-mcp` to explicitly opt
in"* ([Security model](https://microsoft.github.io/apm/enterprise/security/)). This is the chapter's
headline mechanism and the running example's spine.

**(d) The executable-trust gate (related, for context).** Beyond MCP, APM *"blocks executable primitives
from dependency packages by default: hooks, `bin/` executables, self-defined MCP servers (`registry:
false`), and canvas extensions. Text primitives (skills, agents, instructions) are never gated."* Trust is
resolved through a deny-wins ladder and managed with `apm approve` / `apm deny`; each dependency's state is
recorded in the lockfile's `exec_status` field ([Security
model](https://microsoft.github.io/apm/enterprise/security/)). Treat this as the *generalization* of the
transitive-MCP idea — "don't auto-run code you didn't choose" — and keep it lightweight so it doesn't
crowd out the MCP story.

**The problem it solves.** Each mechanism closes a specific attack that traditional package managers either
can't see or don't face. APM's own comparison is worth citing: hidden-Unicode injection is *"not
applicable (binary packages)"* for npm but real for prompt files (mitigated by the pre-deploy scan);
version substitution is caught because *"the lock file pins exact commit SHA; content hash detects
post-download tampering"*; and the *"compromised transitive MCP"* path — unique to agent packages — is shut
by the depth-scoped block ([Security model](https://microsoft.github.io/apm/enterprise/security/)). This is
the concrete cash value of "a prompt is a program."

**Key distinctions.**
- *Direct = chosen = trusted; transitive = inherited = blocked.* The dividing line is **authorship of the
  decision**. You put a direct dependency in your manifest on purpose, so its MCP declarations are
  accepted; a transitive server arrived without your say-so, so it is blocked until you *make* the decision
  (re-declare, or opt in).
- *Re-declare vs. `--trust-transitive-mcp` are not equivalent.* Re-declaring promotes one specific server
  to a **reviewed, committed, auditable** manifest entry — a durable trust decision the whole team sees in
  the diff. `--trust-transitive-mcp` is a **blanket, per-install opt-in** for *all* transitive servers in
  that run, leaving no manifest record. Prefer the first for anything shared; reserve the flag for trusted,
  throwaway environments. The author should draw this contrast explicitly.
- *Critical blocks; warnings inform.* The Unicode scan is not all-or-nothing. Critical categories stop the
  deploy (exit `1`); warnings are surfaced but ship. Conflating the two ("any hidden character fails my
  install") overstates the gate.
- *Content hash detects change, not intent.* A hash mismatch proves the bytes differ from the lockfile; it
  cannot say *why*. A legitimate upstream update and a malicious tamper look identical to the hash — which
  is exactly why moving to new bytes is the deliberate, reviewed `apm update` (Chapter 7), not a silent
  install-time acceptance.
- *`--force` is the labeled fire exit.* It *"bypass[es] the security scan's critical-finding block … Use
  only after independent verification"* ([apm install](https://microsoft.github.io/apm/reference/cli/install/)).
  It is intentionally explicit and loud, not a convenience.

**Common misconception.** *"If a package installs, its MCP servers are all trusted."* No — only *direct*
dependencies' MCP servers are auto-trusted. A server pulled in *transitively* is blocked by default; the
install can succeed for everything else while that server is held back, and you must explicitly declare or
trust it to proceed. Installation success ≠ blanket MCP trust.

**Meridian beat (for the author).** This is the chapter's worked example, in three moves.
*(1) Block.* Meridian adds `checkout-review-pack` (v0.3.0); `apm install` blocks its **transitive**
`io.github.github/github-mcp-server` and prints the remedy — declare it explicitly in `dependencies.mcp`,
or re-run in a trusted environment with `--trust-transitive-mcp`.
*(2) Decide.* The team takes the **reviewable** path: after a security review, they promote the server to
a **direct** `mcp:` entry in `apm.yml` (v0.3.1), so the trust decision is committed, diffed, and owned —
*not* a blanket `--trust-transitive-mcp` opt-in.
*(3) Record.* The lockfile now carries the server with its provenance (`depth: 2`,
`resolved_by: …/checkout-review-pack`), turning an invisible transitive capability into a visible,
auditable line. The alternative ending — reject the dependency entirely — is equally valid and worth
naming: sometimes the right move is *not* to grant the capability. (Mark private-package and MCP-registry
steps `SKIPPED-needs-network`; the `code-verifier` confirms exact block text and lockfile fields.)

**For engineering leaders (callout seed).** Security by default changes the *rollout* conversation:
developers keep moving quickly, but risky content is checked *before* it becomes local tool access, not
after an incident. The reframe for leaders is that a transitive MCP server is an **ungoverned capability
grant** — the kind of thing that used to be invisible until a review or an audit surfaced it — and APM now
makes that grant an explicit, reviewable decision at install time. It is *not* a substitute for endpoint
security or harness governance (Concept 4); it is the pre-deploy gate that makes the capability visible in
the first place.

**Implemented in APM by:** the built-in content scanner in `apm install` (Unicode severity table:
critical blocks, warnings inform) and `apm audit` [`--strip`] for on-demand scan/remediation;
`apm.lock.yaml` `content_hash` verification (re-download on cache mismatch, abort on fresh mismatch);
the MCP trust model (direct auto-trusted, transitive blocked) with `--trust-transitive-mcp` and manifest
re-declaration as the two opt-in paths; the executable-trust gate managed by `apm approve` / `apm deny`
(lockfile `exec_status`). (Severity categories, exact block/remedy strings, `depth`/`resolved_by` lockfile
fields, and the approve/deny ladder confirmed by the explorer.)

---

## Concept 4 — Not a runtime sandbox (the install/integrity plane ⟂ runtime)

**Definition.** APM's guarantees stop at the moment of install. It governs **what reaches disk and whether
it conforms** — the *install and integrity plane* — and hands off everything after that to the harness:
*"This governance covers the install and integrity plane — what reaches disk and whether it conforms to
policy. Runtime behavior governance belongs to your agent harness, not to APM"* ([The three
promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). The security model draws the
same line as an explicit non-goal list: *"APM does NOT sandbox MCP servers at runtime, does not do malware
analysis on dependency code, does not sign packages, and does not inspect what an agent does once it has
read your context"* ([Security model](https://microsoft.github.io/apm/enterprise/security/)). And it has
*"no runtime footprint … APM generates files then terminates. It does not run alongside your application"*
([Security model](https://microsoft.github.io/apm/enterprise/security/)).

**The problem it solves.** A security tool that *overclaims* is worse than one that states its limits,
because teams build on the parts that don't exist. Naming the boundary precisely lets a security reviewer
compose APM with the right *other* controls — harness permissions, endpoint security, network policy —
instead of assuming APM covers them. This is the honesty that makes "secure by default" a claim you can
put in a compliance document: APM provides **dependency governance** (controlled sources, locked versions,
byte-level verification), and its docs say to *"describe the guarantees as APM dependency governance …
rather than as supply-chain signing or attestation"* ([Security
model](https://microsoft.github.io/apm/enterprise/security/)).

**Key distinctions.**
- *Install/integrity plane vs. runtime plane.* APM decides *whether an MCP server's config reaches your
  disk*; the harness decides *what that server may do when the agent calls it*. Once a server is trusted
  and deployed, APM is out of the loop — it does not proxy, throttle, or sandbox the calls.
- *"Secure by default" is preventive hygiene, not detection.* The scan catches *known invisible-character
  classes*; it explicitly *"does not detect: plain-text prompt injection (visible but malicious
  instructions), homoglyph substitution, semantic manipulation, [or] binary payload embedding"* ([Security
  model](https://microsoft.github.io/apm/enterprise/security/)). A clean scan means "no hidden Unicode and
  no drift," never "this prompt is benign." Human review of *visible* content is still required.
- *No signing, no attestation, no malware analysis.* Content hashing detects *tampering after download*;
  it does **not** verify publisher identity (*"package signing is a planned hardening item"*) and APM emits
  an SBOM inventory, *"not a security attestation"* ([Security
  model](https://microsoft.github.io/apm/enterprise/security/)). Treat installed packages with the same
  diligence as any external dependency.
- *This chapter is defaults; Chapter 9 is policy; the harness is runtime.* Three distinct planes. Chapter 8
  = built-in install-time defaults. Chapter 9 = configurable org policy (still install-time). The harness =
  runtime behavior. The two-plane rule (*"the two planes do not overlap"*) is the sentence to repeat.

**Common misconception.** *"APM sandboxes or monitors my agents / blocks malicious tools while they run."*
It does neither. APM is a build-time dependency manager with **no runtime component** — it writes files and
exits. It can stop a dangerous *file* or an unchosen *capability* from being installed; it cannot police an
agent's live behavior. Expecting runtime enforcement from APM is the single most common overclaim, and the
one this chapter exists to prevent.

**Meridian beat (for the author).** Close the loop honestly. Even after Meridian *approves* the GitHub MCP
server and installs it cleanly, APM's job is finished — it verified provenance, scanned the bytes, and made
the capability an explicit, reviewed choice. What that server is *allowed to do* when Omar's Claude Code
session calls it is now a **harness** question (its MCP permissions), not an APM one. The team's security
posture is APM's pre-deploy gate *plus* harness-level runtime controls — never APM alone. That is the
correct, non-overclaiming takeaway to carry into Chapter 9.

**For engineering leaders (callout seed).** Position APM accurately in the control stack: it is a
**pre-deploy gate for agent packages**, not endpoint security and not a runtime monitor. In compliance
terms it provides *dependency governance* — controlled sources, locked versions, byte-level integrity, and
an install-time capability gate — which is a real, auditable control, but one that composes *with* harness
runtime governance and endpoint tooling rather than replacing them. Leaders who understand the boundary buy
the right complements; leaders who don't develop a false sense of coverage.

**Implemented in APM by:** the *absence* of a runtime component (install writes files and exits — no
daemon, no phone-home by default); the documented non-goals (no runtime MCP sandbox, no malware analysis,
no package signing, no agent-behavior inspection); the stated scan limitations (no plain-text-injection,
homoglyph, semantic, or binary-payload detection); and the two-plane rule that assigns runtime governance
to the harness. Chapter 9's `apm-policy.yml` extends the *install* plane, not the runtime plane. (Non-goals
and limitations quoted verbatim from the security model; the explorer confirms nothing in v0.23.1 adds a
runtime surface beyond opt-in lifecycle scripts and the experimental canvas primitive, both gated.)

---

## Sources

Official APM documentation (enterprise/security first, then the promise and command references):

- **Security model** — threat model and defended properties; *"the prompt supply chain is different"*
  (no install→run gap; *"file presence IS execution"*); the `download → scan source → block or deploy →
  report` pre-deploy gate; hidden-Unicode threat (Glassworm 2026) and detection/severity table;
  content-integrity hashing (re-download on mismatch, abort on fresh mismatch); MCP server trust model
  (direct auto-trusted, transitive blocked; re-declare or `--trust-transitive-mcp`); executable-trust gate
  (`apm approve` / `apm deny`, `exec_status`); *"what APM does NOT do"* non-goals; content-scan limitations;
  attack-surface comparison; *"describe the guarantees as APM dependency governance."*
  <https://microsoft.github.io/apm/enterprise/security/>
- **The three promises** — Promise 2 *secure by default* (*"a prompt is a program for an LLM"*; scan +
  content-hash pin + transitive-MCP block); Promise 3 *governed by policy* (*"install and integrity plane …
  runtime behavior governance belongs to your agent harness, not to APM"*); FAQ *"what does the policy
  engine actually block?"* <https://microsoft.github.io/apm/concepts/the-three-promises/>
- **apm audit** — the explicit content scan + drift tool; *"already runs automatically in `apm install`,
  `apm compile`, and `apm unpack`; you do not need to call `apm audit` to be safe by default"*; severity
  levels; `--strip` remediation; `--ci` gate. <https://microsoft.github.io/apm/reference/cli/audit/>
- **apm install** — the built-in security scan (critical findings block, exit `1`); `--trust-transitive-mcp`
  (*"Trust self-defined MCP servers shipped by transitive packages without re-declaring them"*); `--force`
  (*"bypass the security scan's critical-finding block … Use only after independent verification"*).
  <https://microsoft.github.io/apm/reference/cli/install/>
- **apm approve / apm deny** — managing the executable-trust gate.
  <https://microsoft.github.io/apm/reference/cli/approve/>
- **Drift and secure by default (consumer)** — consumer-side overview of the two-layer security model.
  <https://microsoft.github.io/apm/consumer/drift-and-secure-by-default/>
- **microsoft/apm README** — the boundary sentence reinforced from Chapter 1: *"apm-policy.yml governs what
  gets installed; your agent harness governs what runs. The two planes do not overlap."*
  <https://github.com/microsoft/apm>

Cross-references within the book (not external sources): Chapter 1's accuracy trap and provenance/security
framing ([content/chapters/the-context-problem.html](../chapters/the-context-problem.html)); Chapter 6's
`content_hash` as a reproducibility field
([content/research/06-the-lockfile-and-reproducibility-theory.md](06-the-lockfile-and-reproducibility-theory.md));
Chapter 7's `apm audit` introduction
([content/research/07-lifecycle-theory.md](07-lifecycle-theory.md)).

---

## Artifact path

`content/research/08-security-by-default-theory.md` (this file).
