from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

import generate
import generate_pdf


class FrontendLayoutTests(unittest.TestCase):
    def test_table_wrapper_preserves_native_table_and_caption_markup(self):
        table = (
            '<table id="stable-table"><caption>A &amp; B</caption>'
            '<thead><tr><th scope="col">Key</th></tr></thead>'
            '<tbody><tr><td><code>long.path</code></td></tr></tbody></table>'
        )
        self.assertEqual(
            generate.present_fragment(table),
            '<div class="table-scroll" role="region" aria-label="Scrollable table" tabindex="0">'
            + table + "</div>",
        )

    def test_pre_is_keyboard_focusable_without_changing_code(self):
        source = '<pre class="sample"><code>&lt;table&gt;\n  preserve spaces</code></pre>'
        self.assertEqual(generate.present_fragment(source),
                         source.replace("<pre ", '<pre tabindex="0" ', 1))

    def test_existing_pre_tabindex_and_non_pre_tags_are_untouched(self):
        source = '<pre class="sample" tabindex="-1"><code>text</code></pre><prefix>text</prefix>'
        self.assertEqual(generate.present_fragment(source), source)

    def test_each_accepted_fragment_is_recoverable_without_prose_changes(self):
        chapters = generate.load_chapters()
        for chapter in chapters:
            for slot, source in generate.load_fragment(chapter["slug"]).items():
                with self.subTest(chapter=chapter["slug"], slot=slot):
                    presented = generate.present_fragment(source)
                    self.assertEqual(presented.count('class="table-scroll"'),
                                     len(re.findall(r"<table\b", source)))
                    self.assertEqual(presented.count('<pre tabindex="0"'),
                                     len(re.findall(r"<pre(?=[\s>])", source)))
                    recovered = re.sub(
                        r'<div class="table-scroll"[^>]*>(<table\b[\s\S]*?</table>)</div>',
                        lambda match: match[1], presented,
                    ).replace('<pre tabindex="0"', "<pre")
                    self.assertEqual(recovered, source)

    def test_web_presentation_is_not_injected_into_print(self):
        for chapter in generate.load_chapters():
            with self.subTest(chapter=chapter["slug"]):
                printed = generate_pdf._chapter_sections_html(chapter)
                self.assertNotIn('class="table-scroll"', printed)
                self.assertNotIn('<pre tabindex="0"', printed)
                for source in generate.load_fragment(chapter["slug"]).values():
                    self.assertIn(source, printed)

    def test_book_metadata_omits_false_pdf_page_count(self):
        chapters = generate.load_chapters()
        script = generate.index_jsonld(chapters)
        graph = json.loads(re.search(r"<script[^>]*>([\s\S]*?)</script>", script)[1])["@graph"]
        book = next(node for node in graph if node["@type"] == "Book")
        self.assertNotIn("numberOfPages", book)
        self.assertEqual(len(book["hasPart"]), len(chapters))
        self.assertEqual(book["version"], generate.CONTENT_VERSION)
        self.assertEqual(book["dateModified"], generate.CONTENT_DATE)


if __name__ == "__main__":
    unittest.main()
