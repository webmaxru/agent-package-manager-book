# Changelog

All notable changes to the **book content** — the chapters you read — are recorded here.

This changelog tracks the **content edition only**. Site tooling, build scripts, analytics, and
other infrastructure changes are intentionally excluded: they never bump the edition. The version
below drives the edition shown on the site and in the downloadable PDF, and matches the `vX.Y`
[GitHub Release](https://github.com/webmaxru/agent-package-manager-book/releases) tag.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the book uses
a `major.minor` content-edition scheme (see [`content/version.yml`](version.yml)).

## [1.1] — 2026-07-08

### Added
- **Chapter 12 — The Landscape & What's Next:** a new *"tools that consume APM"* subsection that
  positions **GitHub Agentic Workflows (`gh-aw`)** as a complementary consumer/runtime of APM,
  not a rival, and places it on the wider landscape map.
- **Chapter 11 — Enterprise at Fleet Scale:** a callout explaining how `gh-aw` wraps
  `microsoft/apm-action` via a `shared/apm.md` import, so the manifest, lockfile SHA pins, and org
  `apm-policy.yml` baseline carry into an agent's execution environment — paired with GitHub's
  Well-Architected guidance for governing agentic workflows.

## [1.0] — 2026-07-03

### Added
- Initial published edition of *The Missing Package Manager — Managing AI Agent Context with APM*:
  12 chapters across six parts, taking the reader from *"why agent context needs a package
  manager"* through the `apm.yml` manifest, install/restore, the lockfile and reproducibility,
  lifecycle, security by default, governance and policy, becoming a producer, and enterprise
  fleet-scale adoption.
