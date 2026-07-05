"""Tests for scripts/curate.py — filtering, snippet cleaning, rendering."""

import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path

import feedparser

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import curate  # noqa: E402

FIXTURE = Path(__file__).parent / "fixture_feed.xml"


def load_fixture():
    now = datetime.now(timezone.utc)
    xml = FIXTURE.read_text(encoding="utf-8")
    xml = xml.replace("{RECENT}", format_datetime(now - timedelta(days=2)))
    xml = xml.replace("{OLD}", format_datetime(now - timedelta(days=30)))
    return feedparser.parse(xml)


def test_filter_keeps_recent_and_undated_drops_old():
    parsed = load_fixture()
    kept = curate.filter_entries(parsed.entries, days=7)
    titles = [e.get("title") for _, e in kept]
    assert "Recent story about Copilot" in titles
    assert "Undated story kept for review" in titles
    assert "Old story that should be filtered" not in titles


def test_filter_sorts_newest_first():
    parsed = load_fixture()
    kept = curate.filter_entries(parsed.entries, days=60)  # keep all three
    dates = [dt for dt, _ in kept if dt is not None]
    assert dates == sorted(dates, reverse=True)


def test_clean_snippet_strips_html_and_entities():
    snippet = curate.clean_snippet("<p>Copilot &amp; <b>formulas</b></p>")
    assert snippet == "Copilot & formulas"


def test_clean_snippet_truncates_with_ellipsis():
    snippet = curate.clean_snippet("word " * 100, limit=50)
    assert len(snippet) <= 50
    assert snippet.endswith("…")


def test_render_item_contains_link_and_checkbox():
    parsed = load_fixture()
    kept = curate.filter_entries(parsed.entries, days=7)
    dt, entry = next((d, e) for d, e in kept if e["title"].startswith("Recent"))
    line = curate.render_item(dt, entry)
    assert line.startswith("- [ ] [Recent story about Copilot](https://example.com/recent)")
    assert "Copilot can now generate formulas" in line


def test_render_report_includes_errors_section():
    report = curate.render_report({"Feed A": []}, {"Feed B": "HTTPError: 404"}, days=7)
    assert "## ⚠️ Feeds that failed" in report
    assert "Feed B" in report and "404" in report
    assert "(no items in window)" in report


def test_main_with_fixture_config(tmp_path, monkeypatch):
    """End-to-end: main() with a stubbed fetch writes the candidates file."""
    monkeypatch.setattr(curate, "fetch_feed", lambda url: load_fixture())
    feeds = tmp_path / "feeds.json"
    feeds.write_text('{"feeds": [{"name": "Fixture", "url": "https://example.com/rss"}]}')
    out = tmp_path / "candidates.md"
    assert curate.main(["--feeds", str(feeds), "-o", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "## Fixture (2)" in text
    assert "Recent story about Copilot" in text
