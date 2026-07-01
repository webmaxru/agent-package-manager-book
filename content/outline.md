# Agent Package Manager Book Outline

This outline follows `content/book-brief.md`: concepts first, `apm`-CLI-and-manifest-primary
coverage, mid-level practical depth, no CLI internals, and content decoupled from the interactive
HTML presentation.

> **Status: awaiting architecture.** The previous chapter arc has been cleared as part of reframing
> the repository to Agent Package Manager. The `book-architect` populates the chapter table below
> and `content/toc.yml` (the machine-readable source of truth) from `content/book-brief.md` when the
> book is built. `content/toc.yml` currently holds an empty `chapters: []` with the expected schema.

## Chapter table

_(To be produced by `book-architect`.)_

| # | Chapter | Objective | APM features | Depends on |
|---:|---|---|---|---|
| — | _pending_ | _pending_ | — | — |

## Navigation model

- `content/toc.yml` is the machine-readable source of truth for chapter navigation.
- The frontend should render top-level chapter subpages from `chapters[*].slug`.
- Within each subpage, render ordered section anchors from `chapters[*].sections`.
- Cross-references should link from every `In APM` section back to the earliest chapter that
  introduced the underlying concept in `depends_on`.

## Per-chapter section skeleton (same every chapter)

- Objective
- Concept/Theory
- In APM
- When to use / pitfalls
- Worked example
- Recap & next

## Wave plan

_(To be produced by `book-architect`.)_ Each chapter follows the dispatch path:
`theory-researcher` and `apm-cli-explorer` research in parallel, then `chapter-author`,
`code-verifier`, `chapter-reviewer`, and `frontend-builder`. Pure-concept chapters may skip CLI
exploration unless the author needs command/manifest mapping context.
