"""Generate the static Agent Package Manager book site from content/toc.yml."""
from __future__ import annotations

import html
import re
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


def root_head(title: str, description: str, prefix: str = "") -> str:
    return f"""<meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta name=\"description\" content=\"{esc(description)}\">
  <title>{esc(title)} | {esc(BOOK_TITLE)}</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link rel=\"preconnect\" href=\"https://cdnjs.cloudflare.com\">
  <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400&display=swap\">
  <link rel=\"stylesheet\" href=\"{prefix}assets/style.css\">
  <script defer src=\"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"></script>
  <script defer src=\"{prefix}assets/app.js\"></script>"""


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
  {root_head("Home", BOOK_INTRO)}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header" role="banner">
    <div class="container">
      <div class="hero">
        <div class="hero-copy">
          <p class="eyebrow">{esc(BOOK_TITLE)}</p>
          <h1 class="hero-title">Agent context is a dependency. Manage it like one.</h1>
          <p class="hero-sub">{esc(BOOK_INTRO)}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="{esc(start_href)}">Start reading</a>
            <a class="btn btn-secondary" href="https://github.com/microsoft/apm" rel="noreferrer">View microsoft/apm</a>
          </div>
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
      <p>By <a href="https://www.linkedin.com/in/webmaxru/" rel="noreferrer">Maxim Salnikov</a> &middot; <a href="https://github.com/webmaxru/agent-package-manager-book" rel="noreferrer">Source on GitHub</a></p>
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
  {root_head(chapter["title"], chapter["objective"], "../")}
</head>
<body class="chapter-page">
  <a class="skip-link" href="#main-content">Skip to main content</a>
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
        <p>By <a href="https://www.linkedin.com/in/webmaxru/" rel="noreferrer">Maxim Salnikov</a> &middot; <a href="https://github.com/webmaxru/agent-package-manager-book" rel="noreferrer">Source on GitHub</a></p>
      </footer>
    </div>
  </div>
</body>
</html>
'''


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


def main() -> None:
    chapters = load_chapters()
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    (SITE / "index.html").write_text(render_index(chapters), encoding="utf-8")
    for index, _chapter in enumerate(chapters):
        output = CHAPTERS_DIR / f"{chapters[index]['slug']}.html"
        output.write_text(render_chapter(chapters, index), encoding="utf-8")
    removed = prune_stale_chapters(chapters)
    print(f"Generated {1 + len(chapters)} HTML files in {SITE}")
    if removed:
        print(f"Removed {len(removed)} stale chapter file(s): {', '.join(removed)}")


if __name__ == "__main__":
    main()
