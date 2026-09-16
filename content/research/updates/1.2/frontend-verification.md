# Frontend verification - edition 1.2

**Date:** 2026-09-16

**Final result: PASS for the requested release-presentation scope.**
The original page-overflow, caption/badge-clipping, and inaccurate page-count
findings are resolved. Required HTML/PDF rebuild, edition, source preservation,
navigation, and local asset/anchor checks also **PASS**. Final served gate:
**06:07:10-06:08:32 +02:00**. This is not a new editorial or example-verification
ACCEPT; [integration-review.md](integration-review.md) remains the content gate
for edition **1.2**, target APM **0.31.0**, at the protected identities.

## Scope and source preservation

- Existing Python/PyYAML generator and Playwright Chromium `148.0.7778.96`;
  existing MuPDF and `pypdf` for actual-PDF checks. No installations, APM CLI
  invocations, chapter authoring, scaffolding, print redesign, or new dependencies.
- Twelve chapters and TOC matched all raw/LF/blob identities in
  [source-identities.json](source-identities.json); producer-reference hash also
  matched [integration-review.md](integration-review.md).
- **251 protected files unchanged** from the follow-up baseline, excluding the
  two intentionally changed shell files and this report. Accepted sources,
  research, edition metadata, dependencies, workflows, other design/assets,
  analytics, and Azure files were preserved. No assertion about a future commit.
- All **13 actual HTML files** matched the generator. Removing only the new
  table wrappers and pre `tabindex` attributes recovered all **72 authored slots
  byte-for-byte**. Chapter/section navigation, prerequisites, updated feature
  lists, current-page markers, and prev/next matched the accepted TOC.

## Exact surgical shell changes

- `site/assets/style.css`:
  - `.section-content`: `overflow-wrap: break-word` permits long prose paths and
    hashes to wrap without collapsing tables' intrinsic column widths.
  - `.table-scroll`: `max-width: 100%; overflow-x: auto; margin: 1.6rem 0`.
    `.section-content .table-scroll > table` gets `margin: 0`; native table
    styling, cell/header semantics, captions, and content remain intact.
  - `.code-example > figcaption`: `overflow-wrap: anywhere`; its direct children
    get `min-width: 0; max-width: 100%`.
  - `.apm-version, .needs-network`: `display: inline-block; max-width: 100%;
    white-space: normal; overflow-wrap: anywhere`, replacing the two nowrap
    declarations. This also fixes standalone badges outside figures.
  - `.table-scroll:focus-visible` joins the existing 3px indigo focus rule.
    `pre:focus-visible` uses a 3px `var(--ink-indigo)` outline at `-3px`, visible
    inside a code card's rounded boundary. Existing local pre scrolling remains.
  - No root/body overflow hiding, fixed table layout, font-size reduction,
    palette/branding, navigation, or motion-rule changes.
- `site/generate.py`: new web-only `present_fragment()` wraps **52 tables** in
  `<div class="table-scroll" role="region" aria-label="Scrollable table" tabindex="0">`
  and makes **109 chapter pre blocks** keyboard-focusable with `tabindex="0"`.
  It runs only at chapter-page slot injection; `load_fragment()` and the PDF
  renderer still receive the untouched authored fragments.
- Removed `"numberOfPages": len(chapters)` from home Book JSON-LD. The optional
  field is **omitted**, not replaced with another estimate or a circular PDF
  build dependency. The shared chapter Book reference is unchanged.
- Added `tests/test_frontend_layout.py`: six regression tests for markup/code
  preservation, focusability, untouched print fragments, and omitted page count.
  The full existing offline suite plus these tests passed: **57/57**.

## Actual build and edition checks

Executed from the repository root:

```powershell
python .\site\validate_release.py --base-ref v1.1
$env:APM_PDF_REQUIRED = '1'
python .\site\generate.py
```

Both exited **0**; required rebuild **05:59:59-06:00:09 +02:00**, after release
preflight. The integration-build PDF was copied outside `site/`, then removed
from the output path before generation: no stale fallback. Analytics environment
value unset, `.env` absent, generated connection string empty: **no-op telemetry**.
No local key/credentials; CI injection unchanged.

| Actual output | Finding |
| --- | --- |
| Home hero and all 13 book-page footers | `Edition v1.2 · Updated September 16, 2026` |
| Home Book JSON-LD | `bookEdition: v1.2`, `version: 1.2`, `dateModified: 2026-09-16`; twelve chapter entries; inaccurate `numberOfPages` omitted |
| Chapter JSON-LD | Correct chapter identity/order and shared Book reference; existing template does not repeat edition/date |
| `llms.txt` | v1.2 / September 16, 2026; all twelve chapter links |
| `sitemap.xml` | All 15 `lastmod` values are `2026-09-16` |
| Actual PDF cover | v1.2; updated and generated September 16, 2026 |
| Actual PDF footers | **113/113** show v1.2 and the correct `Page n of 113`; existing footer is version-only, not dated |

### Actual PDF, not just assembled HTML

`site/apm-book.pdf`: **5,666,408 bytes (5.40 MiB), 113 A4 pages, PDF 1.4**.

SHA256:
`b486e41b539018b66762ce12845608744579fda7dd3516a2d67d2f2aea96e613`

Size and page count happen to equal the prior integration PDF; the bytes/hash
are fresh (PDF creation timestamp `2026-09-16T04:00:04Z`). The prior SHA256 was
`b2fa8d145e4ce3865c931d381ab4a49a9fbdc960de1d174a6e36843f84a07cbc`.

MuPDF and `pypdf` strict parsing succeeded: nonempty, unencrypted, no repair,
valid framing, matching counts. Actual PDF text contained all twelve chapters
and **72 section headings**; chapter page ranges are in `pdf-verification.json`.

All **319 outline entries** and **99 named links / 65 distinct destinations**
resolve within the PDF; no extracted text span exceeded a page boundary.
All **113 pages' extracted text and all 13,390 text-span geometries/font sizes**
are identical to the prior integration artifact. The assembled print HTML hash
also matched; `site/generate_pdf.py` was not changed. This confirms no new print
clipping/reflow was introduced by the screen fix. The approximately
**8.64pt body / 6.85pt code** scale remains a preexisting, nonblocking readability
caveat, not a reason to redo print design. Rasterized 56 actual PDF pages.
Final F2/F3 text is present in HTML and actual PDF: injection verification,
not technical-accuracy verification.

## Measured before/after presentation - original blockers resolved

Reproduced the original findings against the actual served DOM before editing,
not just screenshots. Final validation rendered home and all twelve chapters
at **390x844 and 1440x1000, in both light and dark**: **52 page renders**, plus
**12 expanded-disclosure states**. Every document and body fit the viewport.
Assertions allow 1px rounding; actual final document widths were exactly
**390 / 1440px**. Neither root nor body masks overflow with `hidden`/`clip`.

| Page | Before document width at 390px | After |
| --- | ---: | ---: |
| Home | 390 | 390 |
| Ch1 | 551 | 390 |
| Ch2 | 812 | 390 |
| Ch3 | 872 | 390 |
| Ch4 | 638 | 390 |
| Ch5 | 838 | 390 |
| Ch6 | 597 | 390 |
| Ch7 | 494 | 390 |
| Ch8 | 618 | 390 |
| Ch9 | 578 | 390 |
| Ch10 | 553 | 390 |
| Ch11 | 541 | 390 |
| Ch12 | 1052 | 390 |

At desktop, **Ch12: 1480 -> 1440px**; the other twelve pages remain 1440px.
Its table retains its **1031.75px** intrinsic width, inside a **350px mobile /
864px desktop** scroll region (`scrollWidth: 1032`), rather than squeezing the
columns or clipping the page. Table captions remain part of their native,
keyboard-scrollable table region.

All eleven originally clipped figure captions are fixed. Values below are
caption `scrollWidth / clientWidth` in pixels on mobile:

| Figure ID | Before | After |
| --- | ---: | ---: |
| `ch4-registry-source` | 931 / 348 | 348 / 348 |
| `ch4-mcp-shape` | 368 / 348 | 348 / 348 |
| `ch5-meridian-clone` | 500 / 303 | 303 / 303 |
| `ch5-onboard-manifest` | 312 / 306 | 306 / 306 |
| `ch5-current-restore` | 361 / 348 | 348 / 348 |
| `ch6-current-lock` | 429 / 348 | 348 / 348 |
| `ch7-registry-manifest` | 408 / 348 | 348 / 348 |
| `ch7-history-lock-diff` | 383 / 348 | 348 / 348 |
| `ch9-schema-031` | 374 / 348 | 348 / 348 |
| `ch10-ex15-declared-git` | 417 / 348 | 348 / 348 |
| `ch11-ghaw-import` | 338 / 306 | 306 / 306 |

`ch4-registry-source` also improves **931 / 862 -> 862 / 862** at desktop.
Its mobile caption expands naturally to **255 / 255px scroll/client height**.
No caption height is clamped.

Across all four matrices, with native disclosures keyboard-opened for their
contents, all **105 figures** (104 chapter figures plus home), **157 captions**
(figure plus table), and **155 badges** were measured: **420 figure, 628 caption,
620 badge observations**, zero clipping. Both `scrollWidth <= clientWidth + 1`
and `scrollHeight <= clientHeight + 1` passed, as did caption-child containment.

The experiment also exposed long inline paths/hashes in Ch6/8 and standalone
nowrap badges in Ch6/9. Caption-only wrapping left Ch6 at **457px** and Ch9 at
**403px**; the final shared prose/badge rules bring both to **390px**. This is
part of resolving page overflow, not an unrelated styling change.

## Served navigation, keyboard, and local links

- **838 local link/asset references**,
  including **256 anchors**, with zero missing targets or duplicate IDs.
  **23 unique HTTP targets returned 200**; downloaded PDF bytes/hash matched disk.
- All overflowing regions at both widths were exercised in light mode:
  **32 tables / 87 pre blocks mobile; 1 table / 8 pre blocks desktop**.
  Arrow keys scroll locally in both directions, full scroll ranges are reachable,
  3px focus rings are visible, Tab exits without a trap, and page `scrollX`
  remains zero. Native table/header/caption roles survive the wrappers.
- Keyboard skip/section focus, mobile menu navigation/closing, theme toggle,
  all four native disclosures opening/closing, and no-JS desktop next navigation
  passed. **No-JS mobile table keyboard scrolling** also passed. Reduced-motion
  styles and the motion-enabled home reveal both retain their existing behavior.
- **109 chapter code blocks / copy buttons**, existing highlighting/nohighlight
  choices, and **34 access-badge texts** are unchanged. Clipboard payload matched
  after Windows CRLF-to-LF normalization. The home artifact fits without scrolling.
- Final F3 URL points to the upstream guide pinned at
  `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`, not Chapter 11.
  External documentation endpoints were not live-validated.
- Final gate: zero JavaScript errors, failed resource requests, blocked requests,
  or telemetry requests. Light/dark computed palettes are distinct as expected.
- Every attached server used an OS-assigned free port on **127.0.0.1** and closed
  in `finally`. Final pass: **port 65401, PID 18572**; closure confirmed.
  Only owned servers were stopped; no unrelated process cleanup.

**No open presentation blocker remains in this scope.** The shared chapter Book
reference and version-only PDF footer are unchanged and acceptable; dense print
is preexisting and nonblocking. No new editorial/example ACCEPT is implied.

## Files and evidence

Owned source changes:

```text
site/assets/style.css
site/generate.py
tests/test_frontend_layout.py                 (new)
content/research/updates/1.2/frontend-verification.md
```

Regenerated tracked HTML outputs changed in this follow-up:

```text
site/index.html
site/chapters/the-context-problem.html
site/chapters/lessons-from-package-managers.html
site/chapters/primitives-and-harnesses.html
site/chapters/the-manifest-apm-yml.html
site/chapters/install-and-restore.html
site/chapters/the-lockfile-and-reproducibility.html
site/chapters/lifecycle.html
site/chapters/security-by-default.html
site/chapters/governance-and-policy.html
site/chapters/becoming-a-producer.html
site/chapters/enterprise-at-fleet-scale.html
site/chapters/the-landscape-and-whats-next.html
```

The build also regenerated `site/llms.txt`, `site/sitemap.xml`, `site/robots.txt`,
`site/site.webmanifest`, and `site/assets/og-cover.png`; their bytes are unchanged
from the follow-up baseline. The caller's existing v1.2 tracked diffs in
`llms.txt`/`sitemap.xml` remain intact. No generated pages were hand-edited.

Ignored outputs: `site/apm-book.pdf`, `site/assets/analytics-config.js`.
The former was rebuilt as required; the latter remains no-op telemetry.
This report is the only content/research file changed by the follow-up.

Original integration diagnostics remain in the parent `frontend` directory.
All new raw logs, JSON measurements, PDF text, **169 PNG screenshots/rasters**,
the prior integration PDF/report, and the verification script are outside the
repository under:

```text
C:\Users\masalnik\.copilot\session-state\2d4facdd-cd43-4bef-9f47-dc669687d65a\files\book-v1.2\frontend\layout-fix
```

Primary evidence: `before-browser-verification.json`, `experiment.log`,
`experiment-badges.log`, `preflight.log`, `tests.log`, `build.log`, `after.log`,
`after-browser-verification.json`, `pdf-verification.json`,
`pdf-layout-and-links.json`, `html-source-parity.json`, `source-preservation.json`,
and `final-summary.json`.

Earlier follow-up harness attempts are retained with `attempt-*` suffixes.
The final harness opens native disclosures before focusing their contents,
waits for focus-ring painting, and waits for navigation/font loading instead of
aborting in-flight CDN requests. These were harness fixes, not later production
changes or waived layout assertions; the final gate exits **0**.

To serve locally on a free loopback port:

```powershell
python -m http.server 0 --bind 127.0.0.1 --directory site
```

Use the printed port; stop that foreground server with Ctrl+C. No APM examples
were re-executed or re-certified. This follow-up performed no repository commits,
PRs, pushes, tags, merges, releases, subagent dispatches, workflow/dependency
changes, or Azure operations. Concurrent controller changes were left untouched;
publication remains with the main orchestrator.
