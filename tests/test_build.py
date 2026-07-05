"""Tests for scripts/build.py — front matter, styling, email shell."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import build  # noqa: E402

SAMPLE = """---
subject: "Test subject"
preview: "Test preview line."
issue: 001
---

# The AI Edge — Test

*Tagline here.*

---

🛠️ **Section**

[**Headline (2 minute read)**](https://example.com)
Body sentence.

> *"A prompt in a blockquote."*
"""


def test_front_matter_parsed():
    meta, body = build.split_front_matter(SAMPLE)
    assert meta["subject"] == "Test subject"
    assert meta["preview"] == "Test preview line."
    assert meta["issue"] == "001"
    assert body.lstrip().startswith("# The AI Edge")


def test_no_front_matter_passthrough():
    meta, body = build.split_front_matter("# Just a heading\n")
    assert meta == {}
    assert body.startswith("# Just a heading")


def test_inline_styles_applied():
    html = build.inline_styles("<p>x</p><a href='#'>y</a><blockquote>z</blockquote><hr>")
    assert 'p style="font-size:15px' in html
    assert f'a style="color:{build.BRAND["accent"]}' in html
    assert "blockquote style=" in html
    assert "border-top:1px solid" in html


def test_shell_has_preview_and_single_column():
    shell = build.wrap_shell("<p>body</p>", {"subject": "S", "preview": "P-text"})
    assert shell.startswith("<!DOCTYPE html>")
    assert "P-text" in shell and "display:none" in shell  # hidden inbox preview
    assert "max-width:600px" in shell
    assert "<script" not in shell and "<link" not in shell


def test_build_end_to_end(tmp_path):
    src = tmp_path / "issue.md"
    src.write_text(SAMPLE, encoding="utf-8")
    dest = tmp_path / "issue.html"
    meta = build.build(src, dest)
    html = dest.read_text(encoding="utf-8")
    assert meta["subject"] == "Test subject"
    assert "Headline (2 minute read)" in html
    assert 'href="https://example.com"' in html
    assert "A prompt in a blockquote." in html
