"""Render a single downloadable PDF of the whole APM book.

The PDF is built from the *same* source of truth as the HTML site
(``content/toc.yml`` + ``content/chapters/<slug>.html`` fragments), so it stays
in lock-step with the book: whenever the content changes, re-running the build
regenerates the PDF. Presentation helpers and constants are reused from
``generate.py`` so titles, ordering, parts, and authored slots never drift from
the website.

Pipeline: assemble one print-optimised HTML document (cover -> table of
contents -> every chapter) with a self-contained print stylesheet, then let
headless Chromium (via Playwright) paginate it to ``site/apm-book.pdf`` with a
navigable outline (PDF bookmarks), a tagged/accessible tree, and a page-number
footer.

Run directly (``python site/generate_pdf.py``) or let ``generate.py`` invoke it
at the end of a normal site build.
"""
from __future__ import annotations

import datetime
import sys
from pathlib import Path
from typing import Any

# Allow both "python site/generate_pdf.py" and "import generate_pdf" from
# generate.py: ensure this file's directory (site/) is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate  # noqa: E402  (local module in site/)

SITE = generate.SITE
ASSETS = SITE / "assets"
COVER_SVG = generate.ROOT / "assets" / "cover.svg"
OUT_PDF = SITE / "apm-book.pdf"

# Public download name/URL surfaced on the site.
PDF_FILENAME = "apm-book.pdf"


# ── Print stylesheet ────────────────────────────────────────────────────────
# Self-contained: mirrors the site's light-theme palette and the content
# classes authored in the fragments (callouts, meridian beats, code cards,
# property pills, tables), simplified for paged media (no shadows, fixed
# elements, hovers, or per-line reveal animations). color-mix() and logical
# break-* properties are used, matching modern Chromium support.
PRINT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400&display=swap');

:root {
  --bg: #FFFFFF;
  --surface: #FFFFFF;
  --surface-2: #EEF1F8;
  --text: #171A22;
  --muted: #5A6478;
  --border: #DCE1EC;
  --indigo: #5A54F0;
  --indigo-strong: #3F38D6;
  --amber: #B87613;
  --amber-strong: #8F5A0C;
  --prop-portability: #5A54F0;
  --prop-reproducibility: #0EA5A5;
  --prop-security: #B87613;
  --prop-governance: #C2468A;
  --ink: #10141F;
  --ink-2: #171D2C;
  --ink-text: #E6EAF6;
  --ink-muted: #9AA6C0;
  --ink-border: #2B3448;
  --ink-amber: #E7B23D;
  --ink-indigo: #9E98FF;
  --radius: 12px;
  --radius-sm: 9px;
  --font-display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --font-body: "Literata", Georgia, "Times New Roman", serif;
  --font-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
}

* { box-sizing: border-box; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body {
  margin: 0;
  font-family: var(--font-body);
  color: var(--text);
  font-size: 10.6pt;
  line-height: 1.62;
  background: #FFFFFF;
}

h1, h2, h3, h4 { font-family: var(--font-display); color: var(--text); line-height: 1.2; }
h1 { font-size: 22pt; font-weight: 800; letter-spacing: -0.01em; }
h2 { font-size: 15pt; font-weight: 700; margin: 1.6rem 0 0.7rem; }
h3 { font-size: 12.5pt; font-weight: 700; margin: 1.4rem 0 0.5rem; }
h4 { font-size: 11pt; font-weight: 700; margin: 1.1rem 0 0.45rem; color: var(--muted); }
p { margin: 0 0 0.85rem; }
strong { font-weight: 600; }
em { font-style: italic; }

a { color: var(--indigo-strong); text-decoration: none; }

ul, ol { margin: 0 0 0.9rem; padding-left: 1.3rem; }
li { margin: 0.28rem 0; }
li::marker { color: var(--amber); }

/* Inline code */
:not(pre) > code {
  font-family: var(--font-mono);
  font-size: 0.86em;
  background: color-mix(in srgb, var(--amber) 10%, var(--surface-2));
  border: 1px solid color-mix(in srgb, var(--amber) 22%, var(--border));
  border-radius: 5px;
  padding: 0.05em 0.32em;
  color: var(--text);
}

/* Code blocks — the site's dark "ink" artifact surface */
pre {
  margin: 1rem 0;
  background: var(--ink);
  color: var(--ink-text);
  border: 1px solid var(--ink-border);
  border-radius: var(--radius-sm);
  padding: 0.85rem 1rem;
  font-size: 8.4pt;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: anywhere;
}
pre code { font-family: var(--font-mono); color: var(--ink-text); background: none; border: 0; padding: 0; font-size: inherit; }

/* Code-as-figure card */
figure.code-example {
  background: var(--ink);
  border: 1px solid var(--ink-border);
  border-radius: var(--radius);
  margin: 1.1rem 0;
  overflow: hidden;
  break-inside: avoid;
}
figure.code-example > figcaption {
  font-family: var(--font-mono);
  font-size: 7.8pt;
  line-height: 1.55;
  color: var(--ink-muted);
  background: var(--ink-2);
  border-bottom: 1px solid var(--ink-border);
  padding: 0.55rem 0.8rem;
  break-after: avoid;
}
figure.code-example > figcaption code { background: rgba(255,255,255,0.08); border: 0; color: var(--ink-text); padding: 0.05em 0.3em; }
figure.code-example > figcaption em { color: var(--ink-text); }
figure.code-example > figcaption a { color: var(--ink-indigo); }
figure.code-example pre { margin: 0; border: 0; border-radius: 0; background: var(--ink); }
figure > figcaption { margin: 0; }

.apm-version {
  font-family: var(--font-mono);
  font-size: 7pt;
  color: var(--ink-amber);
  background: color-mix(in srgb, var(--ink-amber) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--ink-amber) 32%, transparent);
  border-radius: 6px;
  padding: 0.1rem 0.4rem;
  white-space: nowrap;
}
.needs-network {
  font-family: var(--font-mono);
  font-size: 6.6pt;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-amber);
  background: color-mix(in srgb, var(--ink-amber) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--ink-amber) 45%, transparent);
  border-radius: 999px;
  padding: 0.1rem 0.45rem;
  white-space: nowrap;
}
.needs-network::before { content: "\\25d0 "; }

/* Tables */
table { border-collapse: collapse; width: 100%; margin: 1.1rem 0; font-size: 8.8pt; break-inside: avoid; }
caption { caption-side: bottom; color: var(--muted); font-family: var(--font-mono); font-size: 7.6pt; padding-top: 0.5rem; text-align: left; }
th, td { border: 1px solid var(--border); padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }
thead th { background: var(--surface-2); font-family: var(--font-display); font-weight: 600; font-size: 8.8pt; }
tbody tr:nth-child(even) { background: color-mix(in srgb, var(--surface-2) 55%, transparent); }
thead, tr { break-inside: avoid; }

/* Callouts */
.callout {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin: 1.1rem 0;
  padding: 0.85rem 1.05rem;
  break-inside: avoid;
}
.callout > h3 { font-family: var(--font-display); font-size: 11pt; margin: 0 0 0.4rem; }
.callout > :last-child { margin-bottom: 0; }
.callout-info { background: color-mix(in srgb, var(--indigo) 6%, var(--surface)); border-color: color-mix(in srgb, var(--indigo) 32%, var(--border)); }
.callout-info > h3 { color: var(--indigo-strong); }
.callout-info > h3::before { content: "\\24d8 "; font-weight: 700; }
.callout-warn { background: color-mix(in srgb, var(--amber) 9%, var(--surface)); border-color: color-mix(in srgb, var(--amber) 40%, var(--border)); }
.callout-warn > h3 { color: var(--amber-strong); }
.callout-warn > h3::before { content: "\\26a0 "; }

/* Leader aside */
.leader-callout {
  background: color-mix(in srgb, var(--indigo) 5%, var(--surface-2));
  border: 1px solid color-mix(in srgb, var(--indigo) 30%, var(--border));
  border-left: 3px solid var(--indigo);
  border-radius: var(--radius);
  margin: 1.1rem 0;
  padding: 0.85rem 1.05rem;
  break-inside: avoid;
}
.leader-callout > h3 {
  font-family: var(--font-mono);
  font-size: 7.6pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--indigo-strong);
  margin: 0 0 0.45rem;
}
.leader-callout > h3::before { content: "\\25c6  "; }
.leader-callout p { color: var(--muted); }
.leader-callout > :last-child { margin-bottom: 0; }

/* Meridian running thread */
.meridian-beat {
  background: color-mix(in srgb, var(--indigo) 6%, var(--surface));
  border: 1px solid color-mix(in srgb, var(--indigo) 26%, var(--border));
  border-left: 3px solid var(--indigo);
  border-radius: var(--radius);
  margin: 1.1rem 0;
  padding: 0.85rem 1.05rem;
  break-inside: avoid;
}
.meridian-beat > h3 {
  font-family: var(--font-mono);
  font-size: 7.6pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--indigo-strong);
  margin: 0 0 0.45rem;
}
.meridian-beat > h3::before { content: "\\25cf  "; font-size: 0.7em; }
.meridian-beat > :last-child { margin-bottom: 0; }

/* Four-property cue pills */
.property {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-family: var(--font-mono);
  font-size: 6.8pt;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text);
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.08rem 0.45rem 0.08rem 0.38rem;
  white-space: nowrap;
}
.property::before { content: ""; width: 0.42rem; height: 0.42rem; border-radius: 50%; display: inline-block; }
.property--portability { border-color: color-mix(in srgb, var(--prop-portability) 45%, var(--border)); }
.property--portability::before { background: var(--prop-portability); }
.property--reproducibility { border-color: color-mix(in srgb, var(--prop-reproducibility) 45%, var(--border)); }
.property--reproducibility::before { background: var(--prop-reproducibility); }
.property--security { border-color: color-mix(in srgb, var(--prop-security) 45%, var(--border)); }
.property--security::before { background: var(--prop-security); }
.property--governance { border-color: color-mix(in srgb, var(--prop-governance) 45%, var(--border)); }
.property--governance::before { background: var(--prop-governance); }

/* ── Page structure ─────────────────────────────────────────────────── */

/* Cover */
.cover { break-after: page; padding-top: 0.4rem; }
.cover-art { width: 100%; height: auto; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.cover-art svg { display: block; width: 100%; height: auto; }
.cover-meta {
  margin-top: 1.6rem;
  font-family: var(--font-mono);
  font-size: 8.4pt;
  color: var(--muted);
  line-height: 1.9;
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}
.cover-meta strong { color: var(--text); font-weight: 600; }
.cover-meta .cover-version { color: var(--indigo-strong); font-weight: 600; }
.cover-meta .cover-props { display: block; margin-top: 0.4rem; }

/* Table of contents */
.toc { break-before: page; }
.toc h1 { margin: 0 0 0.4rem; }
.toc-sub { color: var(--muted); margin: 0 0 1.4rem; font-size: 9.6pt; }
.toc-part { margin: 1.3rem 0 0.5rem; }
.toc-part-label {
  font-family: var(--font-mono);
  font-size: 7.6pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--indigo-strong);
  margin: 0 0 0.15rem;
}
.toc-part-title { font-family: var(--font-display); font-size: 11.5pt; font-weight: 700; margin: 0; }
.toc-list { list-style: none; margin: 0.4rem 0 0; padding: 0; }
.toc-item { display: flex; gap: 0.6rem; padding: 0.28rem 0; border-bottom: 1px dotted var(--border); break-inside: avoid; }
.toc-num {
  font-family: var(--font-mono);
  font-size: 7.8pt;
  font-weight: 600;
  color: var(--amber-strong);
  background: color-mix(in srgb, var(--amber) 10%, var(--surface-2));
  border: 1px solid color-mix(in srgb, var(--amber) 22%, var(--border));
  border-radius: 5px;
  padding: 0.05rem 0.4rem;
  height: max-content;
  white-space: nowrap;
}
.toc-item-body { flex: 1; }
.toc-item-title { font-family: var(--font-display); font-weight: 600; font-size: 10pt; }
.toc-item-obj { color: var(--muted); font-size: 8.8pt; margin-top: 0.1rem; }

/* Chapters */
.chapter { break-before: page; }
.chapter-head { border-bottom: 2px solid var(--indigo); padding-bottom: 0.8rem; margin-bottom: 1.2rem; }
.chapter-eyebrow {
  font-family: var(--font-mono);
  font-size: 7.8pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--indigo-strong);
  margin: 0 0 0.3rem;
}
.chapter-head h1 { margin: 0 0 0.4rem; }
.chapter-lead { color: var(--muted); font-size: 11pt; margin: 0; }
.chapter-section { margin-top: 0.4rem; }
.chapter-section > h2 {
  border-left: 3px solid color-mix(in srgb, var(--indigo) 55%, var(--border));
  padding-left: 0.6rem;
}

h1, h2, h3, h4 { break-after: avoid; }
figure, img { max-width: 100%; }
"""


def _part_by_number() -> dict[int, tuple[str, str]]:
    """Map a chapter number -> (roman part label, part title)."""
    mapping: dict[int, tuple[str, str]] = {}
    for roman, title, numbers in generate.PARTS:
        for number in numbers:
            mapping[number] = (roman, title)
    return mapping


def _load_cover_svg() -> str:
    """Inline the branded cover SVG (crisp + text stays selectable)."""
    if COVER_SVG.exists():
        return COVER_SVG.read_text(encoding="utf-8")
    return ""


def _chapter_sections_html(chapter: dict[str, Any]) -> str:
    """Render a chapter's authored sections, skipping any empty slot."""
    slots = generate.load_fragment(chapter["slug"])
    blocks: list[str] = []
    used: set[str] = set()
    for title in chapter.get("sections", []):
        base = generate.slugify(title)
        section_id = base
        counter = 2
        while section_id in used:
            section_id = f"{base}-{counter}"
            counter += 1
        used.add(section_id)
        body = slots.get(section_id)
        if not body:
            continue
        blocks.append(
            f'<section class="chapter-section">\n'
            f'  <h2>{generate.esc(title)}</h2>\n'
            f'{body}\n'
            f'</section>'
        )
    return "\n".join(blocks)


def build_book_html(chapters: list[dict[str, Any]]) -> str:
    """Assemble the full print HTML document from the book's source of truth."""
    parts = _part_by_number()
    today = datetime.date.today().strftime("%B %d, %Y")

    # ── Cover ────────────────────────────────────────────────────────────
    cover_svg = _load_cover_svg()
    cover = f'''  <section class="cover">
    <div class="cover-art">{cover_svg}</div>
    <div class="cover-meta">
      <div><strong>{generate.esc(generate.BOOK_TITLE)}</strong> &mdash; {generate.esc(generate.BOOK_SUBTITLE)}</div>
      <div>By {generate.esc(generate.BOOK_AUTHOR)} &middot; Read online at {generate.esc(generate.SITE_URL.replace("https://", ""))}</div>
      <div class="cover-version">{generate.esc(generate.edition_label())}</div>
      <div>Free interactive edition &middot; Full-book PDF &middot; Generated {generate.esc(today)}</div>
      <span class="cover-props">Portability &middot; Reproducibility &middot; Security &middot; Governance</span>
    </div>
  </section>'''

    # ── Table of contents (grouped by part; bookmarks come from headings) ─
    by_number = {int(c["number"]): c for c in chapters}
    toc_parts: list[str] = []
    for roman, part_title, numbers in generate.PARTS:
        entries: list[str] = []
        for number in numbers:
            chapter = by_number.get(number)
            if not chapter:
                continue
            entries.append(
                f'''        <li class="toc-item">
          <span class="toc-num">ch{int(chapter["number"]):02d}</span>
          <span class="toc-item-body">
            <span class="toc-item-title">{generate.esc(chapter["title"])}</span>
            <span class="toc-item-obj">{generate.esc(chapter["objective"])}</span>
          </span>
        </li>'''
            )
        if not entries:
            continue
        toc_parts.append(
            f'''      <div class="toc-part">
        <p class="toc-part-label">Part {generate.esc(roman)}</p>
        <p class="toc-part-title">{generate.esc(part_title)}</p>
      </div>
      <ul class="toc-list">
{chr(10).join(entries)}
      </ul>'''
        )
    toc = f'''  <nav class="toc">
    <h1>Contents</h1>
    <p class="toc-sub">{len(chapters)} chapters, {len(generate.PARTS)} parts. Concept before command &mdash; every APM feature is introduced as the implementation of one of four properties.</p>
{chr(10).join(toc_parts)}
  </nav>'''

    # ── Chapters ─────────────────────────────────────────────────────────
    chapter_blocks: list[str] = []
    for chapter in chapters:
        number = int(chapter["number"])
        roman, part_title = parts.get(number, ("", ""))
        eyebrow = f"Part {roman} &middot; {generate.esc(part_title)} &nbsp;/&nbsp; Chapter {number}" if roman else f"Chapter {number}"
        sections_html = _chapter_sections_html(chapter)
        chapter_blocks.append(
            f'''  <section class="chapter">
    <header class="chapter-head">
      <p class="chapter-eyebrow">{eyebrow}</p>
      <h1>{generate.esc(chapter["title"])}</h1>
      <p class="chapter-lead">{generate.esc(chapter["objective"])}</p>
    </header>
{sections_html}
  </section>'''
        )

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{generate.esc(generate.BOOK_TITLE)} \u2014 {generate.esc(generate.BOOK_SUBTITLE)}</title>
  <style>{PRINT_CSS}</style>
</head>
<body>
{cover}
{toc}
{chr(10).join(chapter_blocks)}
</body>
</html>
'''


def _footer_template() -> str:
    return (
        '<div style="width:100%;font-size:8px;color:#8A93A8;'
        'padding:0 16mm;display:flex;justify-content:space-between;'
        'font-family:Georgia,serif;">'
        f'<span>apm.isainative.dev &middot; Edition v{generate.esc(generate.CONTENT_VERSION)}</span>'
        '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>'
        '</div>'
    )


def _header_template() -> str:
    return (
        '<div style="width:100%;font-size:8px;color:#B4BCCB;'
        'padding:0 16mm;text-align:right;font-family:Georgia,serif;">'
        'The Missing Package Manager</div>'
    )


def render_pdf_from_html(html: str, out_path: Path) -> None:
    """Paginate the print HTML to a PDF with Chromium via Playwright.

    Raises if Playwright or its Chromium build is unavailable, so callers can
    decide whether a missing PDF toolchain is fatal (CI) or a soft skip (local).
    """
    from playwright.sync_api import sync_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_kwargs: dict[str, Any] = dict(
        path=str(out_path),
        format="A4",
        print_background=True,
        display_header_footer=True,
        header_template=_header_template(),
        footer_template=_footer_template(),
        margin={"top": "20mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
        prefer_css_page_size=False,
    )
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.set_default_timeout(60000)
            # 'load' is deterministic for a self-contained document; font network
            # idleness is handled explicitly below (networkidle can be flaky in CI).
            page.set_content(html, wait_until="load")
            page.emulate_media(media="print")
            # Wait for web fonts to finish loading (or fail) so glyph metrics are
            # settled before painting. fonts.ready resolves even offline, so this
            # never hangs; guard anyway so a slow font never fails the build.
            try:
                page.evaluate("async () => { await document.fonts.ready; }")
            except Exception:
                pass
            # `outline`/`tagged` add PDF bookmarks + an accessible tree. They are
            # only supported on newer Playwright/Chromium; degrade gracefully.
            try:
                page.pdf(outline=True, tagged=True, **pdf_kwargs)
            except TypeError:
                page.pdf(**pdf_kwargs)
        finally:
            browser.close()


def build_pdf(chapters: list[dict[str, Any]] | None = None, *, required: bool = False) -> Path | None:
    """Build ``site/apm-book.pdf`` from the current book content.

    Returns the output path on success, or ``None`` when the PDF toolchain is
    missing and ``required`` is False (a soft skip with an actionable message).
    """
    if chapters is None:
        chapters = generate.load_chapters()
    if not chapters:
        print("generate_pdf: no chapters in content/toc.yml; skipping PDF.")
        return None

    html = build_book_html(chapters)
    try:
        render_pdf_from_html(html, OUT_PDF)
    except ImportError as exc:
        message = (
            "generate_pdf: Playwright is not installed, so the PDF was not built. "
            "Install it with `pip install playwright` and `playwright install chromium`."
        )
        if required:
            raise RuntimeError(message) from exc
        print(message)
        return None
    except Exception as exc:  # e.g. Chromium not installed / launch failure
        message = (
            f"generate_pdf: could not render the PDF ({exc.__class__.__name__}: {exc}). "
            "Run `playwright install chromium` to install the browser."
        )
        if required:
            raise
        print(message)
        return None

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"generate_pdf: wrote {OUT_PDF} ({size_kb:.0f} KB) from {len(chapters)} chapters")
    return OUT_PDF


def main() -> None:
    # Standalone runs treat a missing toolchain as fatal so failures are loud;
    # generate.py passes required=False for a graceful local skip.
    build_pdf(required=True)


if __name__ == "__main__":
    main()
