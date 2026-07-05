#!/usr/bin/env python3
"""Build an email-ready HTML file from a markdown newsletter issue.

Usage:
    python3 scripts/build.py issues/issue-001.md
    python3 scripts/build.py issues/issue-001.md -o out.html

Output: email-safe HTML (600px single column, inline styles, no external
fonts or scripts) that pastes cleanly into Buttondown, Kit, or beehiiv's
custom-HTML editor. Also prints the subject + preview text from the
front matter so you can copy them into the platform.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Run: pip install markdown")

# ---------------------------------------------------------------- brand ----
BRAND = {
    "accent": "#1f3a5f",      # deep navy — link + header color; swap for TRLeadership brand color
    "text": "#24292f",
    "muted": "#6a737d",
    "rule": "#e1e4e8",
    "prompt_bg": "#f6f8fa",
    "prompt_border": "#1f3a5f",
    "max_width": "600px",
    "font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
}

# ------------------------------------------------------------ front matter --
def split_front_matter(text: str):
    meta = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            return meta, parts[2]
    return meta, text


# --------------------------------------------------------------- styling ----
def inline_styles(html: str) -> str:
    b = BRAND
    rules = [
        (r"<h1>", f'<h1 style="font-size:26px;line-height:1.25;color:{b["text"]};'
                  f'margin:0 0 6px;font-weight:700;">'),
        (r"<h2>", f'<h2 style="font-size:19px;color:{b["text"]};margin:28px 0 12px;">'),
        (r"<p>", f'<p style="font-size:15px;line-height:1.6;color:{b["text"]};margin:0 0 14px;">'),
        (r"<ul>", '<ul style="padding-left:20px;margin:0 0 14px;">'),
        (r"<li>", f'<li style="font-size:15px;line-height:1.6;color:{b["text"]};margin:0 0 10px;">'),
        (r"<a ", f'<a style="color:{b["accent"]};text-decoration:none;font-weight:inherit;" '),
        (r"<strong>", f'<strong style="color:{b["text"]};">'),
        (r"<hr\s*/?>", f'<hr style="border:none;border-top:1px solid {b["rule"]};margin:26px 0;">'),
        (r"<blockquote>",
         f'<blockquote style="margin:0 0 14px;padding:14px 16px;background:{b["prompt_bg"]};'
         f'border-left:3px solid {b["prompt_border"]};border-radius:0 6px 6px 0;">'),
        (r"<em>", f'<em style="color:{b["muted"]};">'),
    ]
    for pattern, replacement in rules:
        html = re.sub(pattern, replacement, html)
    return html


def wrap_shell(body: str, meta: dict) -> str:
    b = BRAND
    preview = meta.get("preview", "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{meta.get("subject", "The AI Edge")}</title>
</head>
<body style="margin:0;padding:0;background:#ffffff;font-family:{b['font']};">
<!-- inbox preview text (hidden) -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{preview}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td align="center" style="padding:24px 16px;">
<table role="presentation" width="{b['max_width'].rstrip('px')}" cellpadding="0" cellspacing="0" border="0" style="max-width:{b['max_width']};width:100%;">
<tr><td style="text-align:left;">
{body}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""


# ------------------------------------------------------------------ main ----
def build(src: Path, dest: Path) -> dict:
    raw = src.read_text(encoding="utf-8")
    meta, body_md = split_front_matter(raw)
    html = markdown.markdown(body_md, extensions=["extra"])
    html = inline_styles(html)
    dest.write_text(wrap_shell(html, meta), encoding="utf-8")
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path, help="markdown issue file")
    ap.add_argument("-o", "--output", type=Path, help="output HTML path")
    args = ap.parse_args()

    out = args.output or args.source.with_suffix(".html")
    meta = build(args.source, out)

    print(f"Built: {out}")
    if meta.get("subject"):
        print(f"Subject: {meta['subject']}")
    if meta.get("preview"):
        print(f"Preview: {meta['preview']}")

    # simple pre-flight checks
    text = args.source.read_text(encoding="utf-8")
    empty_links = text.count("]()")
    if empty_links:
        print(f"⚠️  {empty_links} empty link(s) []() — fill before sending.")
    if "VERIFY" in text:
        print("⚠️  [VERIFY] tags present — fact-check before sending.")
