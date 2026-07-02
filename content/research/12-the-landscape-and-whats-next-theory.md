# Concept Brief — Chapter 12: The Landscape & What's Next

- **Chapter:** 12 — The Landscape & What's Next (Part VI — At scale & ahead)
- **Objective it serves:** Place APM in the market and standards landscape, then decide what to
  *adopt*, *watch*, or *build around* — a grounded map, not a winner-takes-all prediction.
- **Focus:** **positioning** (per outline). This is the book's closing chapter and its only
  landscape/market chapter. There is **no CLI exploration here** — nothing in this brief is a command
  hand-off to the `apm-cli-explorer`. It is grounded in the landscape research and the official docs,
  specs, competitor repos, and standards sites. What the `code-verifier` owes this chapter is *link
  liveness and version accuracy*, not example runs.
- **Inspected APM CLI version:** `apm-cli` **v0.23.1**; landscape research dated **2026-07-01**;
  **OpenAPM v0.1** is an editor's *Working Draft*. **Version-awareness is the single most important
  discipline in this chapter:** every tool named below — APM included — is **pre-1.0** and moving.
  Any comparison must be stamped with the version/date it was true, because the whole point of the
  chapter is that the category is *still settling*. Re-check the docs, the roadmap, and each
  competitor repo immediately before publication.
- **Depends on:** Chapter 11 (fleet-scale adoption; make-vs-adopt lives here). Strongly **reinforces
  Chapter 2** — the name-collision disambiguation and, especially, Chapter 2's Concept 4 ("the
  registry is the *most optional* part of a package manager; the load-bearing parts are the manifest
  and the lockfile"). This chapter cashes in that framing when it explains why APM's missing registry
  is not a missing core.
- **Running-example note:** Per the outline, the Ch12 Meridian beat is a *decision*, not a new
  manifest: the team decides **what to standardize now** (APM for manifests, lockfiles, policy, and
  internal packages) and **what to watch** (registry evolution; SKILL.md ↔ OpenAPM convergence),
  while **not confusing** Microsoft APM with same-name or adjacent tools. No new `apm.yml` is
  introduced; keep code out of this chapter's theory.

## Frame note (which property this chapter feeds)

Chapters 1–11 built the reader's competence around the book's **four properties** — *portability,
reproducibility, provenance/security, governance* — mapped onto APM's three promises: "portable by
manifest, secure by default, governed by policy"
([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). Chapter 12 does
not add a fifth property. Instead it **turns the four properties into a yardstick**: the honest way to
compare APM with `gh skill`, `orthogonalhq/apm`, `aipm`, and `vercel-labs/skills` is *which of the
four each tool actually delivers, and across how many primitive types* — not which has the slickest
`install` command. That reframing is the chapter's whole job, and it is also the leader takeaway
(make-vs-adopt is a scope-and-governance decision, not an install-UX decision).

## Scope & accuracy notes (read before drafting)

- **Positioning, not a market report.** No rankings, no "winner," no adoption forecasts, no sales
  pitch. Describe what each tool *is* and *is not*, tie it to the four properties, and stop. End the
  chapter on **open questions**, not a recommendation to buy.
- **Everything is pre-1.0 — stamp it.** APM ships ~1–3 releases/week and gives no backward-compat
  guarantee until v1.0 ([OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v0.1.md)). Every
  competitor is likewise early. The comparison table **must** carry a "versions as of 2026-07-01"
  caveat, and the author must re-verify before publication.
- **APM has no central registry today.** Distribution is **git-based** — "any git repository is a
  valid APM package" ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)). The
  registry HTTP API is **explicitly deferred to OpenAPM v0.2**
  ([OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v0.1.md)). State this plainly; it is
  the chapter's central open question, not a footnote.
- **Some landscape facts are research-derived, not first-party.** Competitor internals (e.g. `aipm`'s
  content-addressable store, `vercel-labs/skills`' agent count) and standards-governance details
  (e.g. AGENTS.md stewardship) come from the landscape research and third-party repos, not the APM
  docs. Attribute them to their primary source (the competitor's own repo / the standard's own site)
  and phrase them as "per its repo/docs," so the author never launders a secondary claim into a
  first-party one. Flag the AGENTS.md-governance line for confirmation against
  [agents.md](https://agents.md) at publication.
- **Reinforce the name-collision (Chapter 2), don't re-teach it.** Readers met the disambiguation in
  Ch2; here it returns with *teeth*, because `orthogonalhq/apm` is a real, actively-developed tool
  with the same CLI name and an actual registry. Point back to Ch2 and add the one new fact: the
  collision is not hypothetical.

---

## Concepts covered

1. **A young, still-settling category** — standards, registries, and package scopes are not fixed
   yet; the responsible move is a *grounded map* of what exists and what it optimizes, using the four
   properties as axes — not a prediction of who wins.
2. **The standards layer underneath the tools** — SKILL.md, AGENTS.md, and MCP are the shared
   foundations APM (and most rivals) build on; **OpenAPM v0.1** is Microsoft's broader bid to
   standardize the *manifest + lockfile + policy* triad, with the registry HTTP API deferred to v0.2.
3. **Adjacent and competing tools** — `gh skill`, `vercel-labs/skills`, `orthogonalhq/apm` (same
   name), and `TheLarkInn/aipm` overlap with APM but each optimizes a *subset* of the four properties
   over a *narrower* primitive set; APM's distinction is breadth (all primitive types) plus
   governance (`apm-policy.yml`), at the cost of a central registry it does not yet have.
4. **The registry gap and the path to v1.0** — the biggest open question is discovery: APM is
   git-based with no central index, while narrower rivals already ship registries. Because the
   registry is the *most optional* part (Ch2), git-based APM still delivers all four properties today;
   OpenAPM v0.2 is the milestone to watch. The make-vs-adopt call is therefore about **scope and
   governance**, not install UX.

---

## Concept 1 — A young, still-settling category

**Definition.** "Agent context management" is an emerging tool category — barely a year old as a named
idea — in which standards, registries, and package *scopes* (skills-only vs. full-primitive) are still
being negotiated in public. APM itself was introduced on the GitHub Blog in October 2025
([GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-to-build-reliable-ai-workflows-with-agentic-primitives-and-context-engineering/))
and reached the `microsoft/apm` org only in early 2026 ([microsoft/apm](https://github.com/microsoft/apm)).
A category this young has **no settled winner and no frozen interfaces**.

**The honest positioning.** The responsible closing move for the book is a **grounded map**, not a
forecast. Show readers *what exists*, *what each tool optimizes*, and *where the seams are* — and be
explicit that the map is a snapshot dated 2026-07-01 that will move. Resist "APM wins" language; the
book's credibility in this chapter comes from *not* overclaiming. The four properties are the map's
coordinate system: portability, reproducibility, provenance/security, governance.

**Key distinction — map vs. prediction.** A market report ranks vendors and forecasts share; a
*grounded map* plots tools against stable axes (the four properties + primitive breadth) so a reader
can locate their own need on it. The book does the latter. The reader should leave able to *place a
new tool they encounter next year*, not memorize today's leaderboard.

**Common misconception.** *"There's a standard package manager for agents now, and APM is it."* No —
the category is contested. A broad-spec bid (OpenAPM) and a widely-adopted narrow standard (SKILL.md)
are both in play (Concept 2), and several capable installers exist (Concept 3). APM is *a* strong,
broad answer, not *the* settled answer.

**Ties to the four properties.** This concept establishes the *yardstick*: the rest of the chapter
compares every tool by which of the four properties it delivers and over how many primitive types.
That is the chapter's spine and the reason the four properties recur one last time here.

---

## Concept 2 — The standards layer underneath the tools

**Definition.** Beneath the competing CLIs sits a **shared standards layer** that most of them build
on. Three community standards matter, plus one broader spec:

- **SKILL.md / Agent Skills** ([agentskills.io](https://agentskills.io)) — the community format for
  packaging a reusable skill; Anthropic-originated, community-stewarded, and adopted by a large number
  of agents. APM implements it for its `skill` primitive.
- **AGENTS.md** ([agents.md](https://agents.md)) — the shared convention for agent instruction files.
  *Per the landscape research*, it is now stewarded by the Agentic AI Foundation under the Linux
  Foundation (since ~Dec 2025) — **confirm against [agents.md](https://agents.md) at publication.**
  APM builds on it as one of its foundations.
- **MCP** ([modelcontextprotocol.io](https://modelcontextprotocol.io)) — the Model Context Protocol
  for tool/data servers; APM declares and governs MCP servers as a primitive.
- **OpenAPM v0.1** ([spec](https://microsoft.github.io/apm/specs/openapm-v0.1.md)) — **Microsoft's own
  spec**, a broader bid that standardizes the *manifest* (`apm.yml`), *lockfile* (`apm.lock.yaml`), and
  *policy* (`apm-policy.yml`) formats, dependency-resolution semantics, and the primitive type system.
  It is an editor's Working Draft with no backward-compat guarantee before v1.0, and its **registry
  HTTP API is explicitly deferred to v0.2**.

APM's README states plainly that it is "built on open standards" — AGENTS.md, Agent Skills / SKILL.md,
and MCP ([microsoft/apm](https://github.com/microsoft/apm)).

**The honest positioning.** APM does not compete *with* SKILL.md, AGENTS.md, or MCP — it **consumes
and composes** them. Where it makes a distinct bet is one layer up: OpenAPM tries to standardize the
whole *manifest + lockfile + policy* triad, which is broader than any single-primitive format. The
landscape research frames this as an emerging tension — a widely-adopted narrow standard (SKILL.md)
versus a broader spec (OpenAPM) — and the book should present it exactly that way: **two live bids at
different scopes**, not a war with a foregone conclusion.

**Key distinction — standard vs. tool, and narrow vs. broad.** SKILL.md standardizes *one primitive*
(the skill); OpenAPM standardizes *the packaging system* (manifest/lockfile/policy across all
primitives). A tool (APM, `gh skill`) *implements* standards; a spec (SKILL.md, OpenAPM) *defines*
them. Keeping "who defines the format" separate from "who ships the CLI" is the clarity this concept
must deliver.

**Common misconception.** *"OpenAPM and SKILL.md are rivals for the same slot."* They operate at
different scopes: SKILL.md is a skill-packaging format that OpenAPM-based tools can (and do) *consume*.
The interesting question is **convergence** — whether the broad spec absorbs or aligns with the narrow
one — which is exactly what the Meridian team is told to *watch*, not bet on.

**Ties to the four properties.** The standards layer is what makes **portability** possible at all: a
skill written to SKILL.md or an instruction file written to AGENTS.md can move across harnesses because
the *format* is shared, not the tool. OpenAPM extends that shared-format guarantee to
**reproducibility** (a normative lockfile) and **governance** (a normative policy file). Standards are
the substrate; the four properties are what they buy.

---

## Concept 3 — Adjacent and competing tools

**Definition.** Several tools overlap with APM. Each is real and actively developed as of 2026-07-01;
each optimizes a *subset* of the four properties over a *narrower* primitive set than APM:

- **`gh skill`** — an **official GitHub** feature (GitHub CLI v2.90.0, Apr 16 2026) for installing
  SKILL.md-based skills. **Skills-only**, no manifest/lockfile/policy; its strength is a clean
  **supply-chain/provenance** story (immutable releases, tree-SHA) via GitHub-as-registry
  ([GitHub changelog](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) ·
  [gh skill manual](https://cli.github.com/manual/gh_skill_install)).
- **`vercel-labs/skills`** ("npx skills") — a TypeScript skill installer from Vercel Labs with very
  broad agent support (per its repo, ~72 agents) and git/URL sources plus a `skills.sh` index.
  **Skills-only**; no lockfile, manifest, or governance ([vercel-labs/skills](https://github.com/vercel-labs/skills)).
- **`orthogonalhq/apm`** ⚠️ **same CLI name** — an independent Rust CLI + Next.js site with a real
  **public, searchable registry** (`apm.orthg.nl`) and an `apm-lock.json`. **Skills-only**, no
  governance. This is the collision Ch2 warned about, and it is *not hypothetical*
  ([orthogonalhq/apm](https://github.com/orthogonalhq/apm) · [apm.orthg.nl](https://apm.orthg.nl)).
- **`TheLarkInn/aipm`** — Sean Larkin's (ex-Microsoft/webpack) Rust "AI Plugin Manager" with an
  `aipm.toml` manifest, a planned content-addressable store, semver resolution, and VS Code/LSP
  ambitions. Covers skills, agents, MCP, and hooks; Claude-focused. Notably, its design doc ships a
  **16-point critique of Microsoft APM** — a useful, non-hyped signal of where a serious competitor
  thinks APM is weak ([TheLarkInn/aipm](https://github.com/TheLarkInn/aipm)).
- *(Adjacent, complementary — not head-to-head.)* **`anthropics/skills`** is a content library + the
  SKILL.md reference implementation, not a manager ([anthropics/skills](https://github.com/anthropics/skills));
  the **MCP Registry** ([modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry))
  and **Smithery** ([smithery.ai](https://smithery.ai)) are MCP-server indexes APM can *consume*
  rather than replace.

**The honest positioning.** APM's distinction, per the landscape research, is that it is the **only**
tool covering the full primitive breadth (skills + prompts + instructions + agents + plugins + MCP +
hooks) **and** shipping enterprise governance (`apm-policy.yml`) — but it currently does so **without a
central registry**, using git-based distribution, while several narrower rivals already ship
registries and supply-chain features. State both halves. The competitors are not strawmen: `gh skill`
has the cleanest provenance story, `orthogonalhq/apm` has the registry APM lacks, and `aipm` openly
argues APM is over-broad. Presenting those strengths is what makes the book's positioning trustworthy.

**Key distinction — breadth + governance vs. depth on one slice.** The skill installers (`gh skill`,
`vercel-labs/skills`, `orthogonalhq/apm`) do *one primitive type* well and often add discovery or
provenance on top. APM trades a narrower, polished install experience for **coverage of every
primitive type plus install-time policy** — the things a regulated team needs and a solo developer may
not. `aipm` is the closest in ambition (multi-primitive, lockfile-like store) but is Claude-focused and
earlier-stage.

**Common misconception.** *"They all do the same thing, so pick the one with the nicest CLI."* They do
*not* do the same thing: a skills-only installer cannot express a project's prompts, instructions,
agents, and MCP servers as one governed, locked dependency graph. Choosing on install UX alone hides
the scope difference that actually matters (Concept 4 / the leader callout).

**Ties to the four properties.** Map each tool onto the four:
- *Portability:* every tool here delivers some (that is the price of entry), but only APM/`aipm` carry
  it across *all* primitive types.
- *Reproducibility:* requires a lockfile — APM (`apm.lock.yaml`), `orthogonalhq/apm` (`apm-lock.json`),
  and `aipm` (planned store) have one; `gh skill` and `vercel-labs/skills` do not.
- *Provenance/security:* `gh skill` leads on supply-chain integrity; APM ships content-hash pinning +
  hidden-Unicode scanning + transitive-MCP blocking (Ch8).
- *Governance:* **APM is effectively alone** here with `apm-policy.yml` (Ch9). No skills-only installer
  offers an org-level allow/deny policy gate.

This is the concept where the four-property yardstick does its heaviest lifting; the comparison table
below is its artifact.

### Comparison table (author renders this; stamp it "versions as of 2026-07-01")

> **Pre-1.0 caveat (author must keep this visible):** every tool below is pre-1.0 and moving; this is a
> snapshot dated **2026-07-01** (APM `apm-cli` v0.23.1, OpenAPM v0.1 Working Draft). Treat it as a map,
> not a verdict, and re-verify each cell before publication.

| Tool (as of 2026-07-01) | Owner / lang | Manifest | Lockfile | Central registry | Primitive coverage | Governance / policy | Property emphasis |
|---|---|---|---|---|---|---|---|
| **Microsoft APM** (`apm-cli` v0.23.1) | Microsoft · Python | `apm.yml` | `apm.lock.yaml` (versions + content hashes) | **None yet** — git-based; registry API deferred to OpenAPM v0.2 | **Broadest:** skills, prompts, instructions, agents, plugins, MCP, hooks | **`apm-policy.yml`**, install-time, tighten-only inheritance | **All four** |
| **`gh skill`** (GitHub CLI v2.90.0) | GitHub (official) · Go | none (provenance in SKILL.md) | none | GitHub-as-registry | Skills only | none (relies on GitHub supply chain) | Provenance + portability (skills) |
| **`orthogonalhq/apm`** ⚠️ *same name* | Orthogonal (indep.) · Rust + Next.js | none | `apm-lock.json` | **Public, searchable** (`apm.orthg.nl`) | Skills only | none | Discovery + portability (skills) |
| **`TheLarkInn/aipm`** | Sean Larkin (indep.) · Rust | `aipm.toml` | content-addressable store (planned) | planned | skills, agents, MCP, hooks | none stated | Reproducibility ambitions; Claude-focused |
| **`vercel-labs/skills`** ("npx skills") | Vercel Labs · TypeScript | none | none | git URLs + `skills.sh` index | Skills only | none | Portability (skills), ~72-agent breadth |

*Read the table as: "which properties, over how many primitive types" — not "which install command is
shortest."*

---

## Concept 4 — The registry gap and the path to v1.0

**Definition.** APM's most-discussed open question is **discovery**: it distributes packages over plain
git ("any git repository is a valid APM package",
[What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)) and has **no central, searchable
index**. The registry HTTP API — publisher identity, search, yank/deprecate — is **deferred to OpenAPM
v0.2** ([OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v0.1.md)); progress is tracked on
the public roadmap (Project #2304 and the roadmap discussion on [microsoft/apm](https://github.com/microsoft/apm)).
Meanwhile several narrower rivals already ship a registry (`orthogonalhq/apm`) or GitHub-backed
discovery (`gh skill`).

**The honest positioning.** Say the gap out loud — it is the biggest strategic question for APM and the
book should not hide it. But immediately supply the Chapter 2 counterweight: **the registry is the most
*optional* part of a package manager.** The load-bearing parts are the manifest (declared intent) and
the lockfile (pinned, verified result); npm, pip, and Cargo all worked with git and path sources long
before central indexes mattered. So git-based APM *already* delivers all four properties today — a
team gets portability, reproducibility, provenance, and governance without a registry. What it does not
yet get is **easy discovery/search** of third-party packages. That is a real limitation, and it is a
limitation about *convenience of finding*, not *ability to manage*.

**Key distinction — "no registry" ≠ "no core value."** A missing registry limits *discovery*; it does
not weaken the manifest/lockfile/policy contract. Conflating the two is the trap. The chapter should
draw the line cleanly: adopt APM for the contract you can rely on now (manifest, lockfile, policy,
internal packages); *watch* the registry story (OpenAPM v0.2) rather than block adoption on it.

**Common misconception.** *"No central registry means APM isn't really a package manager yet."* This is
the Chapter 2 misconception in new clothes ("a package manager is basically a downloader with a
registry"). It is wrong for the same reason: the manifest + lockfile are what make it a *package
manager*; the index is a discovery convenience layered on top.

**Make-vs-adopt (the leader-facing decision).** Frame the choice as **scope + governance, not install
UX**:
- A **narrow skill installer** (`gh skill`, `vercel-labs/skills`, `orthogonalhq/apm`) may be entirely
  sufficient for an *individual* workflow that only needs skills and values a registry/discovery today.
- A **regulated or multi-team** context needs the manifest, lockfile, **policy**, and audit story
  across *all* primitive types — which is APM's coverage. Building that in-house means re-deriving
  OpenAPM; adopting APM means inheriting it, at the cost of living with git-based distribution until
  v0.2.
- "Build around" (a thin wrapper, an internal registry proxy — Ch11) is the middle path for teams that
  want APM's contract *and* internal discovery before the official registry lands.

**Ties to the four properties.** This concept closes the loop: git-based APM delivers **portability,
reproducibility, provenance/security, and governance** *now*; the missing piece is a discovery layer,
not a property. The four properties are exactly why the make-vs-adopt call is a scope-and-governance
call — a team that has already decided it needs all four has, in effect, already answered it.

---

## Meridian beat (for the author)

No new manifest — Chapter 12 is a **decision**, matching the outline's worked-example beat. The
Meridian staff engineer writes a short "what we standardize / what we watch" note for the platform
group:

- **Adopt now:** APM for `apm.yml` manifests, `apm.lock.yaml` lockfiles, the org `apm-policy.yml`
  (Ch9/Ch11), and the internal `meridian-standards` package (Ch10) — the contract the team already
  relies on across Copilot, Claude Code, and Cursor.
- **Watch, don't block on:** the OpenAPM **v0.2 registry** story (Project #2304); **SKILL.md ↔ OpenAPM
  convergence**; and whether an internal **registry proxy** (Ch11) should bridge the discovery gap
  before v0.2 ships.
- **Guard against:** the name collision — internal docs and search links must say "**Microsoft APM**"
  / `microsoft/apm`, never bare "apm", so nobody installs `orthogonalhq/apm` or `aipm` by mistake
  (Ch2 reinforced).

The chapter should end on the team's *open questions*, not a triumphal close — mirroring the book's
own honest posture.

## For engineering leaders (callout guidance)

The make-vs-adopt decision is a **scope-and-governance** decision, not an install-UX comparison. A
narrow skill installer can be right for a single developer's skills; a regulated, multi-team org that
has already committed to the four properties needs the manifest + lockfile + policy + audit story over
*all* primitive types, which today points to APM — with eyes open about the git-based distribution and
the deferred registry. The strategic variable to track is **OpenAPM v0.2** (the registry, publisher
identity, and yank/deprecate), because it decides whether Microsoft standardizes the category or the
category fragments across narrower tools and SKILL.md. Adopt for the contract you can rely on now;
budget attention, not a blocking dependency, for the registry.

---

## Sources

Official APM documentation & spec (primary):
- What is APM? ("any git repository is a valid APM package"; manifest-plus-lockfile shape) —
  <https://microsoft.github.io/apm/concepts/what-is-apm/>
- The three promises (portable by manifest · secure by default · governed by policy) —
  <https://microsoft.github.io/apm/concepts/the-three-promises/>
- Docs landing page (Consumer/Producer/Enterprise ramps, CLI reference, specs) —
  <https://microsoft.github.io/apm/>
- Enterprise ramp (governance/policy positioning) — <https://microsoft.github.io/apm/enterprise/>
- OpenAPM v0.1 spec (editor's Working Draft; no backward-compat until v1.0; **registry HTTP API
  deferred to v0.2**) — <https://microsoft.github.io/apm/specs/openapm-v0.1.md>

Official repository & editorial (identity, roadmap, origin):
- microsoft/apm README + repo ("built on open standards" AGENTS.md/Agent Skills/MCP; public roadmap
  Project #2304; roadmap discussion #116) — <https://github.com/microsoft/apm>
- GitHub Blog — "How to build reliable AI workflows with agentic primitives and context engineering"
  (Oct 2025; APM's flagship official-channel introduction) —
  <https://github.blog/ai-and-ml/github-copilot/how-to-build-reliable-ai-workflows-with-agentic-primitives-and-context-engineering/>

Standards layer (primary sites):
- Agent Skills / SKILL.md — <https://agentskills.io>
- AGENTS.md (confirm Linux Foundation / Agentic AI Foundation stewardship line at publication) —
  <https://agents.md>
- Model Context Protocol (MCP) — <https://modelcontextprotocol.io>

Adjacent & competing tools (primary competitor sources):
- `gh skill` — GitHub CLI v2.90.0 (Apr 16 2026); SKILL.md-only; supply-chain integrity —
  <https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/> ·
  <https://cli.github.com/manual/gh_skill_install>
- `orthogonalhq/apm` — **name collision**; Rust CLI + public registry; skills-only —
  <https://github.com/orthogonalhq/apm> · <https://apm.orthg.nl>
- `TheLarkInn/aipm` — Rust AI Plugin Manager (`aipm.toml`, planned content-addressable store); ships a
  16-point critique of Microsoft APM — <https://github.com/TheLarkInn/aipm>
- `vercel-labs/skills` ("npx skills") — TypeScript skill installer, broad agent support; skills-only —
  <https://github.com/vercel-labs/skills>
- `anthropics/skills` — SKILL.md reference implementation + content library (not a manager) —
  <https://github.com/anthropics/skills>

Adjacent registries (complementary, APM can consume):
- MCP Registry — <https://github.com/modelcontextprotocol/registry>
- Smithery (MCP-server index) — <https://smithery.ai>

Name-collision reinforcement (Chapter 2 callback):
- Issoh tech team — APM explainer with multi-way "APM" disambiguation —
  <https://www.issoh.co.jp/tech/details/12779/>

---

## Artifact path

`content/research/12-the-landscape-and-whats-next-theory.md`
