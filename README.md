# TRLeadership Newsletter — working title "The AI Edge"

A TLDR-style weekly newsletter for TRLeadership's audience: beginner-level AI news and practical tips customized for the workplace.

> ⚠️ **Naming:** "The AI Edge" is used by 6+ existing newsletters. See the name options in [`PROPOSAL.md`](PROPOSAL.md) — recommendation is a brand-anchored name like "The TRLeadership Brief".

**Audience:** Business professionals, leaders, and managers who want to use AI tools (ChatGPT, Microsoft Copilot, Claude, etc.) to work smarter — not people who write code.

**Format:** Clean, scannable email. 4-5 curated sections with 1-2 sentence summaries per item. Modeled after [TLDR](https://tldr.tech).

**Cadence:** Weekly (Friday mornings).

---

## Repository structure

| Path | Purpose |
|---|---|
| [`PROPOSAL.md`](PROPOSAL.md) | Strategy: rationale, section structure, tooling comparison, growth plan, CASL compliance, editorial-integrity rules, naming |
| [`PRODUCTION-CHECKLIST.md`](PRODUCTION-CHECKLIST.md) | The ≤90-minute weekly workflow, fact-check gate, and kill criteria |
| [`sample-issue-001.md`](sample-issue-001.md) | Sample first issue. Illustrative — every `VERIFY-URL` must become a real source link before any send |
| [`templates/issue-template.md`](templates/issue-template.md) | Copy this to start each issue: subject/preview front matter, read-time slots, compliant footer |
| [`scripts/curate.py`](scripts/curate.py) | Pulls the week's candidate stories from RSS feeds into a checklist |
| [`scripts/feeds.json`](scripts/feeds.json) | Which feeds to pull — edit freely |
| [`scripts/build.py`](scripts/build.py) | Converts an issue's markdown into email-safe HTML + subject/preview, with pre-flight link checks |
| [`tests/`](tests/) | Test suite (runs in CI on every push) |
| [`CHANGELOG.md`](CHANGELOG.md) | What changed and when |

## Setup (once)

```bash
pip install -r requirements.txt        # markdown + feedparser
pip install -r requirements-dev.txt    # + pytest, if you'll run tests
```

## Weekly workflow

```bash
# 1. Collect candidates (Thu, ~1 min) — writes issues/candidates-YYYY-MM-DD.md
python3 scripts/curate.py

# 2. Draft — check the keepers in the candidates file, then:
cp templates/issue-template.md issues/issue-002.md
#    ...write the issue, run the fact-check gate in PRODUCTION-CHECKLIST.md...

# 3. Build — generates issue-002.html + prints subject/preview text
python3 scripts/build.py issues/issue-002.md
```

Paste the HTML into the email platform (or on Buttondown, paste the markdown directly). `build.py` refuses to stay quiet about empty `[]()` links or leftover `VERIFY` tags.

## Testing

```bash
python -m pytest tests/ -v
```

CI runs the same suite on every push and pull request (`.github/workflows/tests.yml`).

## Publishing this repo to GitHub

```bash
git init && git add -A
git commit -m "v0.3.0: proposal, sample issue, templates, build + curation scripts, tests, CI"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/trleadership-newsletter.git
git push -u origin main
```

Keep it **private** — issue drafts and subscriber strategy don't need to be public.
