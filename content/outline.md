# Agent Package Manager Book Outline

This outline follows `content/playbook-brief.md`: concepts first, `apm`-CLI-and-manifest-primary
coverage, mid-level practical depth, no CLI internals, and content decoupled from the interactive
HTML presentation.

> **Status: architected.** The `book-architect` has populated the chapter table below and
> `content/toc.yml` (the machine-readable source of truth) from `content/playbook-brief.md`,
> `.source-docs/v2/outline.md`, and `.source-docs/v2/running-example.md`. The book is a
> **12-chapter, 6-part** progression built on three narrative devices — the package-manager
> **spine**, the **Meridian** running thread, and the four-properties **frame** with a
> per-chapter "For engineering leaders" callout.

## Chapter table

The book is 12 chapters across 6 parts. Every chapter shares the same six-section skeleton and
carries a "For engineering leaders" callout. This table mirrors `content/toc.yml`.

| # | Chapter | Part | Objective | APM features | Depends on |
|---:|---|---|---|---|---|
| 1 | The Context Problem | I — Why | Articulate why agent context needs a package manager and name the four properties APM protects. | `apm.yml`, `apm.lock.yaml`, `apm-policy.yml`, `apm install`, harness parity | — |
| 2 | Lessons from Package Managers | I — Why | Map package-manager concepts onto agent context so APM feels familiar, not novel. | manifest/lockfile analogy, version pinning, git sources, `apm update`/`outdated`/`audit` | 1 |
| 3 | Primitives & Harnesses | I — Why | Know the vocabulary of what APM manages and how primitives relate to harnesses. | skills, prompts, instructions, agents, plugins, MCP servers; AGENTS.md, SKILL.md, MCP | 1, 2 |
| 4 | The Manifest: `apm.yml` | II — Portable by manifest | Author a valid `apm.yml` that declares Meridian's first shared dependencies. | `apm.yml`, dependencies, git sources, version pinning, scripts, targets | 3 |
| 5 | Install & Restore | II — Portable by manifest | Install and restore a project's agent context with the daily consumer loop. | `apm init`, `apm install <pkg>`, `apm install`, `apm run`, harness targets | 4 |
| 6 | The Lockfile & Reproducibility | III — Reproducible by lockfile | Reproduce an APM setup exactly and explain how the lockfile guarantees it. | `apm.lock.yaml`, exact versions, content hashes, byte-for-byte `--frozen` restore | 5 |
| 7 | Lifecycle | III — Reproducible by lockfile | Keep dependencies current while detecting drift and risk deliberately. | `apm outdated`, `apm update`, `apm audit` | 6 |
| 8 | Security by Default | IV — Secure & governed | Rely on install-time security checks without confusing them with runtime sandboxing. | hidden-Unicode scanning, content-hash pinning, transitive MCP blocking | 7 |
| 9 | Governance & Policy | IV — Secure & governed | Write and pilot an `apm-policy.yml` enforced at install time. | `apm-policy.yml`, install-time enforcement, tighten-only inheritance, warn→block | 8 |
| 10 | Becoming a Producer | V — Producing & sharing | Package and publish reusable primitives for the normal install loop. | producer package shape, `apm pack`, `apm plugin init`, `apm marketplace` | 9 |
| 11 | Enterprise at Fleet Scale | VI — At scale & ahead | Gate and govern APM across an org without bottlenecking developer setup. | `apm audit --ci`, CI gating, registry proxy, air-gapped, `microsoft/apm-action` | 10 |
| 12 | The Landscape & What's Next | VI — At scale & ahead | Place APM in the market/standards landscape and decide what to adopt, watch, or build. | OpenAPM v0.1, SKILL.md, AGENTS.md, MCP, git distribution, registry roadmap | 11 |

## Navigation model

- `content/toc.yml` is the machine-readable source of truth for chapter navigation.
- The frontend should render top-level chapter subpages from `chapters[*].slug`.
- Within each subpage, render ordered section anchors from `chapters[*].sections`.
- Cross-references should link from every `In APM` section back to the earliest chapter that
  introduced the underlying concept in `depends_on`.

## Per-chapter section skeleton (same every chapter)

Every chapter renders these six section anchors in order:

- Objective
- Concept/Theory
- In APM
- When to use / pitfalls
- Worked example
- Recap & next

In addition, every chapter embeds a **"For engineering leaders"** callout *in the flow* (not a
separate section) that translates the hands-on work into risk, ROI, onboarding, and governance
terms — the book's second reading path. The three narrative devices from
`content/playbook-brief.md` run through all six sections: the package-manager **spine** (why this
layer had to exist), the **Meridian** running thread (advance the story by exactly one beat per
chapter), and the four-properties **frame** (portability, reproducibility, provenance/security,
governance).

## Wave plan

Work proceeds in waves so the pilot chapter validates the pipeline before the rest scale out.
Each chapter follows the same dispatch path:

`theory-researcher` ∥ `apm-cli-explorer` → `chapter-author` → `code-verifier` → `chapter-reviewer` → `frontend-builder`

Concept-only chapters (**1–3** and **12**) still get *light* CLI exploration — enough for the
author to map concepts to the correct commands, manifest keys, and file shapes — but their worked
examples stay illustrative rather than fully executed.

| Wave | Chapters | Theme | Notes |
|---|---|---|---|
| 0 (pilot) | 1 | Prove the pipeline | Ch 1 runs end-to-end first; validates the skeleton, leader callout, and Meridian thread before scaling. |
| 1 | 2, 3 | Concepts | Package-manager lessons + primitive/harness vocabulary; light CLI exploration only. |
| 2 | 4, 5 | Portable by manifest | First real `apm.yml`; the daily install/restore loop. |
| 3 | 6, 7 | Reproducible by lockfile | Lockfile + `--frozen`; the `outdated`/`update`/`audit` lifecycle. |
| 4 | 8, 9 | Secure & governed (hardest) | Install-time security, then `apm-policy.yml` warn→block. Highest verification load. |
| 5 | 10, 11, 12 | Producing, scaling, positioning | Producer packaging, fleet CI gating, and the landscape/positioning close. |

Sequencing rules:

- A chapter enters a wave only after all its `depends_on` chapters have passed review.
- Meridian version numbers advance monotonically across waves (`0.1.0` → `0.2.0` → `0.3.x` →
  `1.0.0`); keep them consistent with `.source-docs/v2/running-example.md`.
- Wave 4 is the hardest (security + policy); budget extra `code-verifier` time for the
  transitive-MCP block and the warn→block policy flip.
