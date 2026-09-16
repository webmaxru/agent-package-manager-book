# Changelog

All notable changes to the **book content** — the chapters you read — are recorded here.

This changelog tracks the **content edition only**. Site tooling, build scripts, analytics, and
other infrastructure changes are intentionally excluded: they never bump the edition. The version
below drives the edition shown on the site and in the downloadable PDF, and matches the `vX.Y`
[GitHub Release](https://github.com/webmaxru/agent-package-manager-book/releases) tag.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the book uses
a `major.minor` content-edition scheme (see [`content/version.yml`](version.yml)).

## [1.2] - 2026-09-16

### Changed
- Refresh all twelve chapters across the ten stable APM releases after **0.23.1**
  through **0.31.0**, preserving the concept-first progression, Meridian story,
  and engineering-leader track.
- Explain consented discovery of existing packages, declaration-first source
  selection, explicit targets, and the distinction between legacy plugin
  projection and native Agent Plugins 1.0.
- Update lockfile and lifecycle guidance for timestamp-free state, deployment
  ownership, source-specific identities, bounded frozen checks, cold audit,
  and registry Current/Wanted/Latest reporting.
- Reconcile security and governance guidance with actual scan coverage,
  local policy inheritance, warn/block behavior, consumer fail-closed settings,
  protected CI inputs, and precisely documented APM limitations.
- Expand the producer path with current local-only bundles and a real ZIP
  consumer round-trip. Distinguish experimental registry implementation from a
  public hosted hub, and correct gh-aw target/version inputs and context isolation.

### Added
- Version-pinned practice fixtures for core installation, operations/policy,
  and producer workflows, with genuine lockfiles and independent per-chapter
  verification and editorial evidence.
- A canonical Git/LF checkout check for five primary fixtures and the ZIP
  round-trip on Windows, with source-identity records linking reviewed bytes
  to the published Git content.

### Fixed
- Overbroad install, frozen-restore, audit, trust, and integration guarantees.
  Observed upstream failures remain visible rather than being treated as
  network skips or successful security guarantees.
- Cross-chapter carry-forward of Meridian's reviewed dependencies, MCP
  declaration, and script; the raw-download checksum and gh-aw cross-reference.

Historical **0.23.1** recordings and the **2026-07-01** competitor snapshot
remain explicitly dated. Private infrastructure, paid runtimes, and live
package-publication examples retain their specific execution exclusions.

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
