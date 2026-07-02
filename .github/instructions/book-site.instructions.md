---
description: How the book site is built and which files are safe to edit — generation pipeline, asset ownership, and the verified design system.
applyTo: "site/**"
---

# Book Site: Build Pipeline & Presentation

The `site/` tree is the interactive HTML book. Most of it is **generated**, so knowing what is
generated vs. hand-authored is the difference between an edit that sticks and one that is wiped on
the next build. `frontend-builder` owns this layer (chrome, nav, theming, the build script).

## The generation pipeline (read before editing anything under `site/`)

`site/generate.py` is the generator. Running it (see "Build & preview") writes:

- `site/index.html` from `render_index()` — the home page.
- `site/chapters/<slug>.html` from `render_chapter()` — one file per chapter in the TOC.

Sources of truth it reads:
- `content/toc.yml` — chapter list, order, numbers, slugs, objectives, `apm_features`, `depends_on`.
- `content/chapters/<slug>.html` — the authored **section bodies**, injected into the generated
  page at `<!-- SLOT: <section-id> -->` markers. A missing file or empty slot renders a
  "Content pending" note.

`prune_stale_chapters()` also **deletes** any `site/chapters/*.html` whose slug is no longer in the
TOC.

### Never hand-edit generated files
Do **not** edit `site/index.html` or any `site/chapters/*.html` directly. They are overwritten (and
can be deleted) on the next `generate.py` run, so the edit is silently lost. Change the source
instead, then regenerate.

## Where to change what

| To change… | Edit | Regenerate? |
|---|---|---|
| Chapter prose / worked examples | `content/chapters/<slug>.html` (SLOT markers) | Yes |
| Chapter set, order, titles, numbers, `apm_features`, `depends_on` | `content/toc.yml` | Yes |
| Home-page copy (hero, intro, tagline, the sample `apm.yml` artifact, part titles) | constants + `render_index()` in `site/generate.py` | Yes |
| Chapter shell / sidebar / nav / pager / metadata cards | `render_chapter()` / `build_chapter_nav()` in `site/generate.py` | Yes |
| Styling, theme, tokens, layout | `site/assets/style.css` (**static, not generated**) | No — live immediately |
| Client-side behavior | `site/assets/app.js` (**static, not generated**) | No — live immediately |
| The standalone orchestration animation page | `site/orchestration.html` (**hand-authored, not generated**) | No — live immediately |

Note the split: home-page and chapter-**shell** prose lives in `generate.py`; chapter **section**
prose lives in `content/chapters/`. Don't confuse the two.

## Build & preview

- Build: `python site/generate.py` (requires `pyyaml`; paths resolve from the repo root regardless
  of cwd). Prints `Generated N HTML files`.
- CI mirrors this: `.github/workflows/deploy-pages.yml` runs `pip install pyyaml`, then
  `python site/generate.py`, then publishes `site/` to GitHub Pages.
- Local preview: from `site/`, `python -m http.server` (bind `127.0.0.1` if a corporate proxy
  interferes with `localhost`), then open the served page.

## Verified design system (don't "fix" these)

- **Three font families, paired on a contrast axis** (loaded via Google Fonts in `generate.py`
  `root_head()`): **Bricolage Grotesque** (display), **Literata** (serif body), **IBM Plex Mono**
  (code). A lint "single font" finding is a **false positive**.
- **Dual-voice brand tokens** in `style.css` `:root`, with a `@media (prefers-color-scheme: dark)`
  override block: `--indigo` (`#5A54F0`) = human / manifest voice; `--amber` (`#B87613`) = machine /
  lockfile voice. Any token rework must keep the light and dark values in sync.
- **Signature motifs:** the "resolution spine" (chapters as an ordered dependency path), monospace
  version-pin tags (`ch01`…`ch12`), and dual-voice syntax coloring on `apm.yml` artifacts.
- The `ch01`…`ch12` pins are a **real ordered `depends_on` sequence**, not decorative scaffolding,
  so a lint "numbered-section-markers" finding is a **false positive** here.

## Presentation guardrails

- No structural AI-slop tells: no `>1px` side/top accent stripes used as decoration (use full 1px
  tinted borders, background tints, or leading glyphs/icons instead), no gradient text, no
  decorative glassmorphism.
- Keep contrast at WCAG 2.2 AA: body text ≥4.5:1, large text ≥3:1.
- Em-dash cadence: hand-authored presentation prose in this lane (e.g. `orchestration.html`, the
  copy inside `generate.py`) should vary its punctuation rather than lean on uniform ` — `
  connectors. **Chapter content under `content/**` is out of this lane** — it is verified, reviewed
  content owned by the content pipeline (`book-content.instructions.md`); do not mass-rewrite it
  from a design pass.
