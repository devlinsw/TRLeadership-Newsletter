#!/usr/bin/env python3
"""Curation helper: pull the week's candidate stories from RSS feeds.

Usage:
    python3 scripts/curate.py                    # last 7 days → issues/candidates-YYYY-MM-DD.md
    python3 scripts/curate.py --days 10
    python3 scripts/curate.py --feeds scripts/feeds.json -o my-candidates.md

Output: a markdown checklist grouped by source. Check the items worth
keeping, then draft the issue from templates/issue-template.md.

This replaces the *collection* step of curation, not the judgment step.
Sources without RSS (LinkedIn, TLDR AI, Anthropic news) still need a
manual scan.
"""

import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from html import unescape
from pathlib import Path

try:
    import feedparser
except ImportError:
    sys.exit("Missing dependency. Run: pip install -r requirements.txt")

USER_AGENT = "TRLeadershipNewsletterBot/1.0 (curation script; contact via trleadership.ca)"
FETCH_TIMEOUT = 15  # seconds per feed
SNIPPET_LEN = 160


# ---------------------------------------------------------------- fetch ----
def fetch_feed(url: str) -> "feedparser.FeedParserDict":
    """Fetch a feed with an explicit timeout and UA, then parse."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        raw = resp.read()
    return feedparser.parse(raw)


# ---------------------------------------------------------------- filter ----
def entry_date(entry) -> datetime | None:
    """Best-effort published/updated datetime (UTC) for a feed entry."""
    for attr in ("published_parsed", "updated_parsed"):
        parsed = entry.get(attr)
        if parsed:
            return datetime.fromtimestamp(time.mktime(parsed), tz=timezone.utc)
    return None


def filter_entries(entries, days: int, now: datetime | None = None):
    """Keep entries newer than `days`; undated entries are kept (flagged later)."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    kept = []
    for e in entries:
        dt = entry_date(e)
        if dt is None or dt >= cutoff:
            kept.append((dt, e))
    kept.sort(key=lambda pair: pair[0] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return kept


# ---------------------------------------------------------------- render ----
def clean_snippet(html: str, limit: int = SNIPPET_LEN) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = unescape(re.sub(r"\s+", " ", text)).strip()
    return (text[: limit - 1].rstrip() + "…") if len(text) > limit else text


def render_item(dt, entry) -> str:
    title = (entry.get("title") or "(untitled)").strip()
    link = entry.get("link") or ""
    date_str = dt.strftime("%b %d") if dt else "no date"
    snippet = clean_snippet(entry.get("summary", ""))
    line = f"- [ ] [{title}]({link}) — *{date_str}*"
    if snippet:
        line += f" — {snippet}"
    return line


def render_report(sections: dict, errors: dict, days: int) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = sum(len(v) for v in sections.values())
    out = [
        f"# Candidate stories — {today} (last {days} days)",
        "",
        f"{total} items across {len(sections)} feeds. Check the keepers, cut the rest,",
        "then draft from `templates/issue-template.md`. Target: 10-12 kept items.",
        "",
        "**Manual-scan sources (no RSS):** LinkedIn, TLDR AI, Anthropic news.",
        "",
    ]
    for name, items in sections.items():
        out.append(f"## {name} ({len(items)})")
        out.append("")
        out.extend(render_item(dt, e) for dt, e in items)
        if not items:
            out.append("*(no items in window)*")
        out.append("")
    if errors:
        out.append("## ⚠️ Feeds that failed")
        out.append("")
        for name, err in errors.items():
            out.append(f"- **{name}** — {err}")
        out.append("")
        out.append("*Feed URLs move; update `scripts/feeds.json` if a failure persists.*")
        out.append("")
    return "\n".join(out)


# ------------------------------------------------------------------ main ----
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7, help="lookback window (default 7)")
    ap.add_argument("--feeds", type=Path, default=Path(__file__).parent / "feeds.json")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args(argv)

    config = json.loads(args.feeds.read_text(encoding="utf-8"))
    sections, errors = {}, {}
    for feed in config["feeds"]:
        name, url = feed["name"], feed["url"]
        try:
            parsed = fetch_feed(url)
            sections[name] = filter_entries(parsed.entries, args.days)
            print(f"✓ {name}: {len(sections[name])} items")
        except Exception as exc:  # noqa: BLE001 — any feed failure is non-fatal
            errors[name] = f"{type(exc).__name__}: {exc}"
            print(f"✗ {name}: {errors[name]}")

    out_path = args.output or Path("issues") / f"candidates-{datetime.now(timezone.utc):%Y-%m-%d}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_report(sections, errors, args.days), encoding="utf-8")
    print(f"\nWrote {out_path}")
    return 0 if sections else 1


if __name__ == "__main__":
    sys.exit(main())
