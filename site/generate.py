"""Generate the static Agent Package Manager book site from content/toc.yml."""
from __future__ import annotations

import datetime
import html
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CHAPTERS_DIR = SITE / "chapters"
TOC_PATH = ROOT / "content" / "toc.yml"
CONTENT_CHAPTERS_DIR = ROOT / "content" / "chapters"

# Matches an HTML-comment slot delimiter: <!-- SLOT: <slot-id> -->
SLOT_RE = re.compile(r"<!--\s*SLOT:\s*([a-z0-9-]+)\s*-->")

BOOK_TITLE = "The Missing Package Manager"
BOOK_SUBTITLE = "Managing AI Agent Context with APM"
BOOK_TAGLINE = "Portable by manifest \u00b7 secure by default \u00b7 governed by policy."
BOOK_INTRO = (
    "A hands-on guide to APM, the package manager for AI agent context. Declare the skills, "
    "prompts, instructions, agents, and MCP servers your project needs in one manifest, then "
    "install and restore the same context across every supported harness."
)

# Deployment + SEO identity. The site is published to a custom domain at the
# root, so canonical / Open Graph / JSON-LD URLs are absolute against SITE_URL
# (crawlers and social scrapers require absolute URLs).
SITE_URL = "https://apm.isainative.dev"
BOOK_AUTHOR = "Maxim Salnikov"
AUTHOR_URL = "https://www.linkedin.com/in/webmaxru/"
REPO_URL = "https://github.com/webmaxru/agent-package-manager-book"
APM_DOCS_URL = "https://microsoft.github.io/apm/"
# Single-file, printable PDF of the whole book. Built by generate_pdf.py into
# site/ and offered as a download from the site; regenerated on every build.
PDF_FILENAME = "apm-book.pdf"
LOCALE = "en_US"
OG_IMAGE_PATH = "assets/og-cover.png"
OG_IMAGE_ALT = "The Missing Package Manager \u2014 Managing AI Agent Context with APM"
OG_IMAGE_W = 1200
OG_IMAGE_H = 630
THEME_LIGHT = "#F6F7FB"
THEME_DARK = "#10141F"
THEME_INDIGO = "#5A54F0"

# Blocking, inline anti-FOUC snippet: reflect an explicit stored theme choice
# onto <html> before first paint so a forced theme never flashes. Absence of a
# stored choice leaves the attribute off, so CSS falls back to the OS preference.
THEME_HEAD_SCRIPT = (
    "<script>(function(){try{var t=localStorage.getItem('apm-theme');"
    "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}"
    "catch(e){}})();</script>"
)

# ── Analytics (cookieless Application Insights RUM) ──────────────────────────
# One-line kill switch: set to False to disable ALL telemetry site-wide on the
# next build/deploy (no beacon, no events). The client is also a safe no-op when
# no connection string is injected. The connection string itself is a public,
# write-only client key provided at BUILD time (never committed as source):
# in CI as the APPINSIGHTS_CONNECTION_STRING repo variable, locally via .env.
ANALYTICS_ENABLED = True
ANALYTICS_ENV_VAR = "APPINSIGHTS_CONNECTION_STRING"


# ── Content edition (version) ────────────────────────────────────────────────
# The BOOK CONTENT is versioned independently of the site tooling: content/version.yml
# is the single source of truth (major.minor) and content/CHANGELOG.md records each
# edition. The edition + its date are surfaced on the site and in the PDF, and every
# edition maps to a `vX.Y` GitHub Release (see .github/workflows/release-content.yml).
VERSION_PATH = ROOT / "content" / "version.yml"
CHANGELOG_URL = f"{REPO_URL}/blob/main/content/CHANGELOG.md"
RELEASES_URL = f"{REPO_URL}/releases"


def load_content_edition() -> tuple[str, str]:
    """Return ``(version, iso_date)`` for the current book content edition.

    Falls back to a safe ``("0.0.0", "")`` when version.yml is missing or malformed
    so a build never fails purely because the edition metadata is absent.
    """
    try:
        with VERSION_PATH.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except (OSError, yaml.YAMLError):
        data = {}
    version = str(data.get("version", "0.0.0")).strip() or "0.0.0"
    date = str(data.get("date", "")).strip()
    return version, date


CONTENT_VERSION, CONTENT_DATE = load_content_edition()


def human_date(iso: str) -> str:
    """Render an ISO date (YYYY-MM-DD) as e.g. 'July 8, 2026'; pass through on error."""
    try:
        parsed = datetime.date.fromisoformat(iso)
    except ValueError:
        return iso
    return f"{parsed:%B} {parsed.day}, {parsed.year}"


def edition_label() -> str:
    """Short human edition string, e.g. 'Edition v1.1 \u00b7 Updated July 8, 2026'."""
    label = f"Edition v{CONTENT_VERSION}"
    if CONTENT_DATE:
        label += f" \u00b7 Updated {human_date(CONTENT_DATE)}"
    return label


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"&", " and ", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def load_chapters() -> list[dict[str, Any]]:
    with TOC_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    chapters = data.get("chapters") or []
    if not isinstance(chapters, list):
        raise ValueError(f"'chapters' in {TOC_PATH} must be a list, found {type(chapters).__name__}")
    return chapters


def load_fragment(slug: str) -> dict[str, str]:
    """Return a mapping of slot id -> authored inner HTML for one chapter.

    Authored content lives in content/chapters/<slug>.html, decoupled from this
    presentation layer. Sections are divided by HTML-comment slot markers (see
    SLOT_RE); everything from a marker up to the next marker (or EOF) is that
    slot's trusted inner HTML. A missing file, unknown slot ids, or empty slots
    simply yield no override, so the section keeps its "Content pending" note.
    """
    fragment_path = CONTENT_CHAPTERS_DIR / f"{slug}.html"
    if not fragment_path.exists():
        return {}
    raw = fragment_path.read_text(encoding="utf-8")
    # re.split with one capture group yields: [preamble, id1, body1, id2, body2, ...]
    parts = SLOT_RE.split(raw)
    slots: dict[str, str] = {}
    for i in range(1, len(parts), 2):
        slot_id = parts[i]
        body = parts[i + 1].strip()
        if body:
            slots[slot_id] = body
    return slots


def abs_url(path: str = "") -> str:
    """Absolute URL for a site-relative path.

    Canonical / Open Graph / JSON-LD must be absolute, and the site is served at
    the domain root, so a bare join against SITE_URL is correct.
    """
    path = path.lstrip("/")
    return f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"


def json_ld(data: Any) -> str:
    """Serialize a schema.org object into a safe application/ld+json script."""
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    # Neutralize characters that could break out of the <script> element.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return '<script type="application/ld+json">\n' + payload + "\n  </script>"


def social_meta(full_title: str, description: str, path: str, og_type: str) -> str:
    """Canonical URL, robots directives, Open Graph, and Twitter Card tags."""
    canonical = abs_url(path)
    og_image = abs_url(OG_IMAGE_PATH)
    return f"""  <link rel=\"canonical\" href=\"{esc(canonical)}\">
  <meta name=\"robots\" content=\"index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1\">
  <meta name=\"googlebot\" content=\"index, follow\">
  <meta name=\"author\" content=\"{esc(BOOK_AUTHOR)}\">
  <meta name=\"theme-color\" content=\"{THEME_LIGHT}\" media=\"(prefers-color-scheme: light)\">
  <meta name=\"theme-color\" content=\"{THEME_DARK}\" media=\"(prefers-color-scheme: dark)\">
  <meta property=\"og:type\" content=\"{esc(og_type)}\">
  <meta property=\"og:site_name\" content=\"{esc(BOOK_TITLE)}\">
  <meta property=\"og:locale\" content=\"{LOCALE}\">
  <meta property=\"og:title\" content=\"{esc(full_title)}\">
  <meta property=\"og:description\" content=\"{esc(description)}\">
  <meta property=\"og:url\" content=\"{esc(canonical)}\">
  <meta property=\"og:image\" content=\"{esc(og_image)}\">
  <meta property=\"og:image:type\" content=\"image/png\">
  <meta property=\"og:image:width\" content=\"{OG_IMAGE_W}\">
  <meta property=\"og:image:height\" content=\"{OG_IMAGE_H}\">
  <meta property=\"og:image:alt\" content=\"{esc(OG_IMAGE_ALT)}\">
  <meta name=\"twitter:card\" content=\"summary_large_image\">
  <meta name=\"twitter:title\" content=\"{esc(full_title)}\">
  <meta name=\"twitter:description\" content=\"{esc(description)}\">
  <meta name=\"twitter:image\" content=\"{esc(og_image)}\">
  <meta name=\"twitter:image:alt\" content=\"{esc(OG_IMAGE_ALT)}\">"""


def icon_links(prefix: str) -> str:
    """Favicon, Apple touch icon, and web app manifest links (prefix-relative)."""
    return f"""  <link rel=\"icon\" href=\"{prefix}favicon.ico\" sizes=\"32x32\">
  <link rel=\"icon\" href=\"{prefix}favicon.svg\" type=\"image/svg+xml\">
  <link rel=\"apple-touch-icon\" href=\"{prefix}apple-touch-icon.png\">
  <link rel=\"manifest\" href=\"{prefix}site.webmanifest\">"""


def theme_toggle() -> str:
    """A fixed light/dark switch shared by every page.

    The button is ``position: fixed``, so its place in the DOM is irrelevant to
    layout; ``assets/theme-toggle.js`` owns the behaviour, the visible icon
    (moon in light, sun in dark), and the aria label.
    """
    return (
        '<button class="theme-toggle" type="button" data-theme-toggle '
        'aria-label="Switch color theme" aria-pressed="false">\n'
        '    <svg class="theme-toggle__icon theme-toggle__sun" viewBox="0 0 24 24" aria-hidden="true" focusable="false">\n'
        '      <circle cx="12" cy="12" r="4.2"></circle>\n'
        '      <path d="M12 2.4v2.6M12 19v2.6M4.5 4.5l1.9 1.9M17.6 17.6l1.9 1.9M2.4 12H5M19 12h2.6M4.5 19.5l1.9-1.9M17.6 6.4l1.9-1.9"></path>\n'
        '    </svg>\n'
        '    <svg class="theme-toggle__icon theme-toggle__moon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">\n'
        '      <path d="M20.6 14.3A8.2 8.2 0 0 1 9.7 3.4 8.2 8.2 0 1 0 20.6 14.3z"></path>\n'
        '    </svg>\n'
        '  </button>'
    )


def root_head(
    title: str,
    description: str,
    prefix: str = "",
    path: str = "",
    og_type: str = "website",
    jsonld: str = "",
) -> str:
    full_title = f"{BOOK_TITLE} \u2014 {BOOK_SUBTITLE}" if path == "" else f"{title} | {BOOK_TITLE}"
    jsonld_block = f"\n  {jsonld}" if jsonld else ""
    return f"""<meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  {THEME_HEAD_SCRIPT}
  <meta name=\"description\" content=\"{esc(description)}\">
  <title>{esc(full_title)}</title>
{social_meta(full_title, description, path, og_type)}
{icon_links(prefix)}
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link rel=\"preconnect\" href=\"https://cdnjs.cloudflare.com\">
  <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400&display=swap\">
  <link rel=\"stylesheet\" href=\"{prefix}assets/style.css\">
  <script defer src=\"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"></script>
  <script defer src=\"{prefix}assets/app.js\"></script>
  <script defer src=\"{prefix}assets/theme-toggle.js\"></script>
  <script defer src=\"{prefix}assets/analytics-config.js\"></script>
  <script defer src=\"{prefix}assets/analytics.js\"></script>{jsonld_block}"""


def chapter_url(chapter: dict[str, Any], prefix: str = "chapters/") -> str:
    return f"{prefix}{chapter['slug']}.html"


def build_chapter_nav(chapters: list[dict[str, Any]], current_id: str | None = None, prefix: str = "chapters/") -> str:
    """Render the sidebar chapter list as a resolution spine.

    Chapters are a real ordered ``depends_on`` sequence, so each item carries a
    ``data-state`` (resolved for prior chapters, current, pending for later
    ones) that the stylesheet threads into a vertical dependency path. The
    chapter number renders as a monospace version-pin tag (``ch01``).
    """
    current_index = next((i for i, c in enumerate(chapters) if c["id"] == current_id), None)
    items: list[str] = []
    for i, chapter in enumerate(chapters):
        if current_index is None or i > current_index:
            state = "pending"
        elif i < current_index:
            state = "resolved"
        else:
            state = "current"
        is_current = state == "current"
        aria = ' aria-current="page"' if is_current else ""
        cls = ' class="is-current"' if is_current else ""
        href = chapter_url(chapter, prefix)
        pin = f"ch{int(chapter['number']):02d}"
        items.append(
            f'          <li data-state="{state}"><a{cls}{aria} href="{esc(href)}">'
            f'<span class="pin-tag">{esc(pin)}</span>'
            f'<span class="chapter-name">{esc(chapter["title"])}</span></a></li>'
        )
    return "\n".join(items)


PARTS: list[tuple[str, str, tuple[int, ...]]] = [
    ("I", "Why context needs a manifest", (1, 2, 3)),
    ("II", "Portable by manifest", (4, 5)),
    ("III", "Reproducible by lockfile", (6, 7)),
    ("IV", "Secure & governed", (8, 9)),
    ("V", "Producing & sharing", (10,)),
    ("VI", "At scale & ahead", (11, 12)),
]


def render_part_map(by_number: dict[int, dict[str, Any]]) -> str:
    """The resolution path across the six parts.

    Renders the chapter spine motif on the index so every part is one click
    away: a connected row of nodes, each anchoring to its ``#part-*`` section.
    Skips any part whose chapters are not present so no anchor dangles.
    """
    nodes: list[str] = []
    for roman, part_title, numbers in PARTS:
        present = [n for n in numbers if n in by_number]
        if not present:
            continue
        lo, hi = min(present), max(present)
        pins = f"ch{lo:02d}\u2013{hi:02d}" if lo != hi else f"ch{lo:02d}"
        part_id = f"part-{roman.lower()}"
        nodes.append(f'''            <li class="spine-node">
              <a class="spine-link" href="#{part_id}">
                <span class="spine-dot" aria-hidden="true"></span>
                <span class="spine-text">
                  <span class="spine-meta"><span class="spine-part">Part {esc(roman)}</span> <span class="spine-pins">{pins}</span></span>
                  <span class="spine-title">{esc(part_title)}</span>
                </span>
              </a>
            </li>''')
    if not nodes:
        return ""
    return (
        '      <nav class="resolution-path" aria-label="Jump to a part">\n'
        '        <ol class="spine-track">\n'
        + chr(10).join(nodes)
        + '\n        </ol>\n'
        '      </nav>'
    )


def render_index(chapters: list[dict[str, Any]]) -> str:
    start_href = chapter_url(chapters[0]) if chapters else "#"

    # Hand-authored apm.yml artifact (dual-voice colored; hljs skips it via
    # .nohighlight so the per-line reveal spans survive).
    manifest_lines = [
        '<span class="tok-c"># apm.yml \u2014 your agent\u2019s context, declared</span>',
        '<span class="tok-k">name</span>: <span class="tok-n">meridian-checkout</span>',
        '<span class="tok-k">version</span>: <span class="tok-pin">1.4.0</span>',
        '&nbsp;',
        '<span class="tok-k">dependencies</span>:',
        '  <span class="tok-n">microsoft/apm-sample-package</span>: <span class="tok-pin">^1.2.0</span>',
        '  <span class="tok-n">meridian/review-prompts</span>: <span class="tok-pin">3.1.0</span>',
        '  <span class="tok-n">meridian/money-skill</span><span class="tok-pin">#main</span>: <span class="tok-pin">latest</span>',
        '&nbsp;',
        '<span class="tok-k">targets</span>: [<span class="tok-t">copilot</span>, <span class="tok-t">claude</span>, <span class="tok-t">cursor</span>]',
    ]
    artifact_body = "".join(
        f'<span class="reveal-line" style="--i:{i}">{line}</span>' for i, line in enumerate(manifest_lines)
    )

    by_number = {int(chapter["number"]): chapter for chapter in chapters}
    parts_html: list[str] = []
    for roman, part_title, numbers in PARTS:
        entries: list[str] = []
        for number in numbers:
            chapter = by_number.get(number)
            if not chapter:
                continue
            features = chapter.get("apm_features") or []
            tag_cap = 5
            if len(features) > tag_cap + 1:
                shown = features[:tag_cap]
                more = len(features) - tag_cap
                tag_items = "".join(f"<li>{esc(feature)}</li>" for feature in shown)
                tag_items += f'<li class="field-tags-more">+{more} more</li>'
            else:
                tag_items = "".join(f"<li>{esc(feature)}</li>" for feature in features)
            tags_html = f'\n                <ul class="field-tags">{tag_items}</ul>' if tag_items else ""
            pin = f"ch{int(chapter['number']):02d}"
            entries.append(f'''            <li class="dep-entry">
              <span class="dep-pin"><span class="pin-tag pin-tag--lg">{esc(pin)}</span></span>
              <div class="dep-body">
                <h3 class="dep-title"><a href="{esc(chapter_url(chapter))}">{esc(chapter["title"])}</a></h3>
                <p class="dep-objective">{esc(chapter["objective"])}</p>{tags_html}
              </div>
            </li>''')
        if not entries:
            continue
        part_id = f"part-{roman.lower()}"
        parts_html.append(f'''        <section class="part" aria-labelledby="{part_id}">
          <header class="part-head">
            <span class="part-roman">Part {esc(roman)}</span>
            <h2 class="part-title" id="{part_id}">{esc(part_title)}</h2>
          </header>
          <ol class="dep-list">
{chr(10).join(entries)}
          </ol>
        </section>''')

    if parts_html:
        parts_block = chr(10).join(parts_html)
    else:
        parts_block = '''        <section class="part">
          <p>The table of contents in <code>content/toc.yml</code> is currently empty. Once the book-architect populates it, chapters will appear here.</p>
        </section>'''

    part_map = render_part_map(by_number)

    return f'''<!doctype html>
<html lang="en">
<head>
  {root_head("Home", BOOK_INTRO, path="", og_type="website", jsonld=index_jsonld(chapters))}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  {theme_toggle()}
  <header class="site-header" role="banner">
    <div class="container">
      <div class="hero">
        <div class="hero-copy">
          <p class="eyebrow">{esc(BOOK_TITLE)}</p>
          <h1 class="hero-title">Agent context is a dependency. Manage it like one.</h1>
          <p class="hero-sub">{esc(BOOK_INTRO)}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="{esc(start_href)}">Start reading</a>
            <a class="btn btn-secondary" href="{PDF_FILENAME}" download>Download PDF</a>
            <a class="btn btn-secondary" href="https://github.com/microsoft/apm" rel="noreferrer">View microsoft/apm</a>
          </div>
          <p class="hero-edition"><a href="{RELEASES_URL}" rel="noreferrer">{esc(edition_label())}</a></p>
        </div>
        <figure class="manifest-artifact" aria-label="An apm.yml manifest, resolved">
          <figcaption class="artifact-bar">
            <span class="artifact-file">apm.yml</span>
            <span class="artifact-stamp">resolved</span>
          </figcaption>
          <pre class="artifact-code"><code class="nohighlight">{artifact_body}</code></pre>
        </figure>
      </div>
    </div>
  </header>

  <main id="main-content" class="container" tabindex="-1">
    <section class="intro-panel" aria-labelledby="start-heading">
      <h2 id="start-heading">How to read this book</h2>
      <p>Chapters build in order, concept before command. Every APM feature is introduced as the implementation of one of four properties &mdash; <span class="property property--portability">Portability</span> <span class="property property--reproducibility">Reproducibility</span> <span class="property property--security">Security</span> <span class="property property--governance">Governance</span>.</p>
      <div class="reading-paths">
        <div class="reading-path">
          <p class="path-lane-label">For developers</p>
          <p>Follow the body and the worked examples end to end.</p>
          <a class="path-link" href="{esc(start_href)}">Start reading</a>
        </div>
        <div class="reading-path reading-path--leader">
          <p class="path-lane-label">For engineering leaders</p>
          <p>Skim the <strong>For engineering leaders</strong> asides for the risk, ROI, onboarding, and governance story.</p>
          <a class="path-link" href="{esc(start_href)}">Start with Chapter 1</a>
        </div>
      </div>
      <p class="reading-note">A recurring <strong>Meridian</strong> marker tracks what one team does next, chapter by chapter.</p>
    </section>

    <div class="parts-intro">
      <p class="eyebrow">The reading path</p>
      <h2>Twelve chapters, six parts</h2>
      <p>Chapters resolve in order &mdash; each one depends on the ones before it, like a dependency graph. Read straight through, or jump to the part you need.</p>
    </div>

{part_map}

{parts_block}
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>By <a href="https://www.linkedin.com/in/webmaxru/" rel="noreferrer">Maxim Salnikov</a> &middot; <a href="https://github.com/webmaxru/agent-package-manager-book" rel="noreferrer">Source on GitHub</a> &middot; <a href="{PDF_FILENAME}" download>Download the book (PDF)</a></p>
      <p class="footer-edition"><a href="{RELEASES_URL}" rel="noreferrer">{esc(edition_label())}</a></p>
    </div>
  </footer>
</body>
</html>
'''


def render_chapter(chapters: list[dict[str, Any]], index: int) -> str:
    chapter = chapters[index]
    prev_chapter = chapters[index - 1] if index > 0 else None
    next_chapter = chapters[index + 1] if index < len(chapters) - 1 else None

    slots = load_fragment(chapter["slug"])
    section_nav: list[str] = []
    sections: list[str] = []
    used_ids: set[str] = set()
    pending_note = (
        '            <p class="pending-note"><strong>Content pending.</strong> This section is '
        "reserved for the chapter author. Authored content lives in "
        "<code>content/chapters/&lt;slug&gt;.html</code> under the matching "
        "<code>&lt;!-- SLOT: id --&gt;</code> marker.</p>"
    )
    for title in chapter.get("sections", []):
        base = slugify(title)
        section_id = base
        counter = 2
        while section_id in used_ids:
            section_id = f"{base}-{counter}"
            counter += 1
        used_ids.add(section_id)
        section_nav.append(f'              <li><a href="#{esc(section_id)}">{esc(title)}</a></li>')
        authored = slots.get(section_id)
        section_body = authored if authored else pending_note
        sections.append(f'''        <section class="chapter-section" data-section="{esc(section_id)}">
          <h2 id="{esc(section_id)}"><a class="anchor-link" href="#{esc(section_id)}" aria-label="Link to {esc(title)} section">{esc(title)}</a></h2>
          <div class="section-content" data-content-slot="{esc(section_id)}">
{section_body}
          </div>
        </section>''')

    prev_link = (
        f'<a class="pager-link" rel="prev" href="{esc(prev_chapter["slug"])}.html">← Chapter {esc(prev_chapter["number"])}: {esc(prev_chapter["title"])}</a>'
        if prev_chapter else '<span class="pager-link is-disabled">← No previous chapter</span>'
    )
    next_link = (
        f'<a class="pager-link" rel="next" href="{esc(next_chapter["slug"])}.html">Chapter {esc(next_chapter["number"])}: {esc(next_chapter["title"])} →</a>'
        if next_chapter else '<span class="pager-link is-disabled">No next chapter →</span>'
    )

    features = chapter.get("apm_features") or []
    features_html = ""
    if features:
        features_html = "\n".join(f"            <li>{esc(feature)}</li>" for feature in features)
        features_html = f'''
          <aside class="metadata-card" aria-labelledby="features-heading">
            <h2 id="features-heading">APM features</h2>
            <ul class="tag-list">
{features_html}
            </ul>
          </aside>'''

    depends = chapter.get("depends_on") or []
    depends_html = ""
    if depends:
        id_to_chapter = {item["id"]: item for item in chapters}
        depends_items = []
        for dep_id in depends:
            dep = id_to_chapter.get(dep_id)
            if dep:
                depends_items.append(f'            <li><a href="{esc(dep["slug"])}.html">Chapter {esc(dep["number"])}: {esc(dep["title"])}</a></li>')
            else:
                depends_items.append(f"            <li>{esc(dep_id)}</li>")
        depends_html = f'''
          <aside class="metadata-card" aria-labelledby="depends-heading">
            <h2 id="depends-heading">Prerequisites</h2>
            <ul>
{chr(10).join(depends_items)}
            </ul>
          </aside>'''

    return f'''<!doctype html>
<html lang="en">
<head>
  {root_head(chapter["title"], chapter["objective"], "../", path=chapter_url(chapter), og_type="article", jsonld=chapter_jsonld(chapters, index))}
</head>
<body class="chapter-page">
  <a class="skip-link" href="#main-content">Skip to main content</a>
  {theme_toggle()}
  <button class="sidebar-toggle" type="button" aria-controls="chapter-sidebar" aria-expanded="false">☰ Chapters</button>

  <div class="page-shell">
    <aside id="chapter-sidebar" class="sidebar" aria-label="Book chapters">
      <div class="sidebar-inner">
        <a class="site-title" href="../index.html">{esc(BOOK_TITLE)}</a>
        <p class="sidebar-tagline">A pinned guide to APM</p>
        <nav class="chapter-nav" aria-label="Chapter navigation">
          <ol>
{build_chapter_nav(chapters, chapter["id"], "")}
          </ol>
        </nav>
      </div>
    </aside>

    <div class="content-shell">
      <header class="chapter-header">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Chapter {esc(chapter["number"])}</nav>
        <p class="eyebrow">Chapter {esc(chapter["number"])}</p>
        <h1>{esc(chapter["title"])}</h1>
        <p class="lead">{esc(chapter["objective"])}</p>
      </header>

      <main id="main-content" class="chapter-main" tabindex="-1">
        <div class="chapter-meta">
          <nav class="metadata-card" aria-labelledby="section-nav-heading">
            <h2 id="section-nav-heading">On this page</h2>
            <ol>
{chr(10).join(section_nav)}
            </ol>
          </nav>{features_html}{depends_html}
        </div>

{chr(10).join(sections)}

        <nav class="pager" aria-label="Chapter pagination">
          {prev_link}
          {next_link}
        </nav>
      </main>

      <footer class="site-footer chapter-footer">
        <p>By <a href="https://www.linkedin.com/in/webmaxru/" rel="noreferrer">Maxim Salnikov</a> &middot; <a href="https://github.com/webmaxru/agent-package-manager-book" rel="noreferrer">Source on GitHub</a> &middot; <a href="../{PDF_FILENAME}" download>Download the book (PDF)</a></p>
        <p class="footer-edition"><a href="{RELEASES_URL}" rel="noreferrer">{esc(edition_label())}</a></p>
      </footer>
    </div>
  </div>
</body>
</html>
'''


def index_jsonld(chapters: list[dict[str, Any]]) -> str:
    """schema.org graph for the home page: WebSite + Person + Book (w/ chapters)."""
    author = {"@id": abs_url() + "#author"}
    has_part = [
        {
            "@type": "Chapter",
            "position": int(chapter["number"]),
            "name": chapter["title"],
            "url": abs_url(chapter_url(chapter)),
            "abstract": chapter.get("objective", ""),
        }
        for chapter in chapters
    ]
    graph = [
        {
            "@type": "WebSite",
            "@id": abs_url() + "#website",
            "url": abs_url(),
            "name": BOOK_TITLE,
            "alternateName": BOOK_SUBTITLE,
            "description": BOOK_INTRO,
            "inLanguage": "en",
            "publisher": author,
        },
        {
            "@type": "Person",
            "@id": abs_url() + "#author",
            "name": BOOK_AUTHOR,
            "url": AUTHOR_URL,
        },
        {
            "@type": "Book",
            "@id": abs_url() + "#book",
            "name": BOOK_TITLE,
            "alternateName": BOOK_SUBTITLE,
            "url": abs_url(),
            "description": BOOK_INTRO,
            "inLanguage": "en",
            "bookFormat": "https://schema.org/EBook",
            "numberOfPages": len(chapters),
            "genre": "Technology",
            "bookEdition": f"v{CONTENT_VERSION}",
            "version": CONTENT_VERSION,
            "dateModified": CONTENT_DATE,
            "author": author,
            "publisher": author,
            "image": abs_url(OG_IMAGE_PATH),
            "about": [
                "Agent Package Manager",
                "AI agents",
                "dependency management",
                "developer tooling",
                "Model Context Protocol",
            ],
            "hasPart": has_part,
        },
    ]
    return json_ld({"@context": "https://schema.org", "@graph": graph})


def chapter_jsonld(chapters: list[dict[str, Any]], index: int) -> str:
    """schema.org graph for a chapter page: TechArticle + BreadcrumbList."""
    chapter = chapters[index]
    page = abs_url(chapter_url(chapter))
    graph = [
        {
            "@type": "TechArticle",
            "@id": page + "#article",
            "headline": chapter["title"],
            "name": chapter["title"],
            "description": chapter["objective"],
            "url": page,
            "image": abs_url(OG_IMAGE_PATH),
            "inLanguage": "en",
            "position": int(chapter["number"]),
            "articleSection": f"Chapter {chapter['number']}",
            "author": {"@type": "Person", "name": BOOK_AUTHOR, "url": AUTHOR_URL},
            "isPartOf": {
                "@type": "Book",
                "@id": abs_url() + "#book",
                "name": BOOK_TITLE,
                "url": abs_url(),
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": abs_url()},
                {"@type": "ListItem", "position": 2, "name": chapter["title"], "item": page},
            ],
        },
    ]
    return json_ld({"@context": "https://schema.org", "@graph": graph})


def render_robots() -> str:
    """robots.txt — welcome search + AI/agent crawlers; point to the sitemap."""
    ai_agents = [
        "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User",
        "anthropic-ai", "PerplexityBot", "Perplexity-User", "Google-Extended",
        "Applebot-Extended", "CCBot", "cohere-ai", "Amazonbot", "meta-externalagent",
    ]
    agent_group = "\n".join(f"User-agent: {name}" for name in ai_agents)
    return (
        f"# robots.txt \u2014 {BOOK_TITLE}\n"
        "# Search engines and AI/agent crawlers are welcome.\n"
        "# LLM-friendly index: /llms.txt\n"
        "\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "# AI / agent crawlers (explicitly welcomed)\n"
        f"{agent_group}\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {abs_url('sitemap.xml')}\n"
    )


def render_sitemap(chapters: list[dict[str, Any]]) -> str:
    """XML sitemap for the home page, chapters, and the orchestration page."""
    today = datetime.date.today().isoformat()
    entries: list[tuple[str, str]] = [(abs_url(), "1.0")]
    entries += [(abs_url(chapter_url(chapter)), "0.8") for chapter in chapters]
    entries.append((abs_url(PDF_FILENAME), "0.6"))
    entries.append((abs_url("orchestration.html"), "0.5"))
    rows = "\n".join(
        "  <url>\n"
        f"    <loc>{esc(loc)}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>"
        for loc, priority in entries
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{rows}\n"
        "</urlset>\n"
    )


def render_manifest() -> str:
    """Web app manifest (PWA installability + a named, themed install target)."""
    data = {
        "name": f"{BOOK_TITLE} \u2014 {BOOK_SUBTITLE}",
        "short_name": "APM Book",
        "description": BOOK_INTRO,
        "id": "/",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "lang": "en",
        "dir": "ltr",
        "background_color": THEME_LIGHT,
        "theme_color": THEME_INDIGO,
        "categories": ["books", "education", "developer tools", "reference"],
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def render_llms(chapters: list[dict[str, Any]]) -> str:
    """llms.txt (llmstxt.org): a concise, link-first index for LLMs / agents."""
    lines = [
        f"# {BOOK_TITLE}",
        "",
        f"> {BOOK_SUBTITLE}. {BOOK_INTRO}",
        "",
        f"Edition v{CONTENT_VERSION}"
        + (f" \u00b7 updated {human_date(CONTENT_DATE)}" if CONTENT_DATE else "")
        + f" \u00b7 changelog: {CHANGELOG_URL}",
        "",
        "An interactive, multi-page HTML book. Chapters build in order, concept before "
        "command. Every APM feature is introduced as the implementation of one of four "
        "properties \u2014 portability, reproducibility, security, and governance \u2014 and every "
        "example is verified against the real `apm` CLI.",
        "",
        "## Chapters",
        "",
    ]
    lines += [
        f"- [Chapter {chapter['number']}: {chapter['title']}]({abs_url(chapter_url(chapter))}): {chapter['objective']}"
        for chapter in chapters
    ]
    lines += [
        "",
        "## About",
        "",
        f"- [Home]({abs_url()}): overview, reading paths, and the full table of contents.",
        f"- [Download the full book (PDF)]({abs_url(PDF_FILENAME)}): the entire book as one printable, offline PDF.",
        f"- [How the fleet built this]({abs_url('orchestration.html')}): the agent-orchestration pipeline that produced the book.",
        "",
        "## Reference",
        "",
        f"- [APM documentation]({APM_DOCS_URL}): official Agent Package Manager docs.",
        "- [microsoft/apm](https://github.com/microsoft/apm): the APM source repository and samples.",
        f"- [Book source]({REPO_URL}): source for this book.",
        f"- [Changelog]({CHANGELOG_URL}): what changed in each content edition.",
        f"- [Releases]({RELEASES_URL}): versioned editions, each with a downloadable PDF.",
        "",
    ]
    return "\n".join(lines)


def copy_og_image() -> None:
    """Copy the shared cover PNG into site/ so the Open Graph image resolves."""
    src = ROOT / "assets" / "cover.png"
    dst = SITE / "assets" / "og-cover.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copyfile(src, dst)


def write_seo_files(chapters: list[dict[str, Any]]) -> None:
    """Emit robots.txt, sitemap.xml, site.webmanifest, llms.txt; copy the OG image."""
    (SITE / "robots.txt").write_text(render_robots(), encoding="utf-8")
    (SITE / "sitemap.xml").write_text(render_sitemap(chapters), encoding="utf-8")
    (SITE / "site.webmanifest").write_text(render_manifest(), encoding="utf-8")
    (SITE / "llms.txt").write_text(render_llms(chapters), encoding="utf-8")
    copy_og_image()


def prune_stale_chapters(chapters: list[dict[str, Any]]) -> list[str]:
    """Delete site/chapters/*.html whose slug is not in the current TOC."""
    current_slugs = {chapter["slug"] for chapter in chapters}
    removed: list[str] = []
    if not CHAPTERS_DIR.exists():
        return removed
    for existing in sorted(CHAPTERS_DIR.glob("*.html")):
        if existing.stem not in current_slugs:
            existing.unlink()
            removed.append(existing.name)
    return removed


def read_connection_string() -> str:
    """Return the Application Insights connection string for build-time injection.

    A public, write-only client key — never a secret. In CI it arrives as the
    APPINSIGHTS_CONNECTION_STRING repo *variable* (an environment variable on the
    build step); locally it can live in a gitignored ``.env`` at the repo root.
    Returns an empty string when unset, which makes the beacon a safe no-op.
    """
    value = os.environ.get(ANALYTICS_ENV_VAR)
    if value and value.strip():
        return value.strip()
    env_path = ROOT / ".env"
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            if key.strip() == ANALYTICS_ENV_VAR:
                return val.strip().strip('"').strip("'")
    return ""


def write_analytics_config() -> None:
    """Emit site/assets/analytics-config.js with the build-time RUM config.

    This file is generated (and gitignored) so the public client key is injected
    at build time rather than committed as source. It sets ``window.__APM_ANALYTICS__``,
    which the deferred bundle ``assets/analytics.js`` reads to initialize the
    cookieless Application Insights beacon. ``enabled`` is the master kill switch.
    """
    config = {"connectionString": read_connection_string(), "enabled": bool(ANALYTICS_ENABLED)}
    assets_dir = SITE / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    body = (
        "/* Generated by generate.py at build time \u2014 do not edit or commit. */\n"
        "window.__APM_ANALYTICS__ = " + json.dumps(config) + ";\n"
    )
    (assets_dir / "analytics-config.js").write_text(body, encoding="utf-8")


def build_pdf_artifact(chapters: list[dict[str, Any]]) -> None:
    """Regenerate the downloadable book PDF as part of the site build.

    This keeps the PDF in lock-step with the book: any change to the HTML site
    (which is driven by content/toc.yml + content/chapters/*) rebuilds the PDF
    from the same sources in the same run. Building the PDF needs Playwright +
    Chromium, so it is optional by default: a plain HTML build still works
    without that toolchain and only prints an actionable skip notice. CI sets
    APM_PDF_REQUIRED=1 to make a missing/broken toolchain a hard failure, so the
    published site never ships without a fresh PDF.
    """
    required = os.environ.get("APM_PDF_REQUIRED", "").strip().lower() in {"1", "true", "yes"}
    try:
        import generate_pdf  # local module in site/; imported lazily to avoid a cycle
    except ImportError as exc:
        message = "generate: generate_pdf module unavailable; skipping apm-book.pdf."
        if required:
            raise RuntimeError(message) from exc
        print(message)
        return
    generate_pdf.build_pdf(chapters, required=required)


def main() -> None:
    chapters = load_chapters()
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    (SITE / "index.html").write_text(render_index(chapters), encoding="utf-8")
    for index, _chapter in enumerate(chapters):
        output = CHAPTERS_DIR / f"{chapters[index]['slug']}.html"
        output.write_text(render_chapter(chapters, index), encoding="utf-8")
    write_seo_files(chapters)
    write_analytics_config()
    removed = prune_stale_chapters(chapters)
    print(f"Generated {1 + len(chapters)} HTML files in {SITE}")
    print("Wrote robots.txt, sitemap.xml, site.webmanifest, llms.txt; copied assets/og-cover.png")
    connection_present = "present" if read_connection_string() else "absent (no-op)"
    print(f"Wrote assets/analytics-config.js (enabled={bool(ANALYTICS_ENABLED)}, connection string {connection_present})")
    if removed:
        print(f"Removed {len(removed)} stale chapter file(s): {', '.join(removed)}")
    build_pdf_artifact(chapters)


if __name__ == "__main__":
    main()
