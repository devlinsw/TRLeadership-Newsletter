# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); versioning is simple incremental (this is a newsletter repo, not a library).

## [0.3.0] — 2026-07-04

### Added
- `scripts/curate.py` — RSS curation helper: pulls the last N days of candidates from configured feeds into a markdown checklist (`issues/candidates-YYYY-MM-DD.md`), with per-feed failure reporting
- `scripts/feeds.json` — editable feed configuration
- `tests/` — 12 tests covering the build pipeline (front matter, inline styles, email shell, end-to-end) and curation (date filtering, sorting, HTML stripping, report rendering, stubbed end-to-end)
- `.github/workflows/tests.yml` — CI: pytest on every push/PR
- `requirements.txt`, `requirements-dev.txt`, `.gitignore`
- This changelog

## [0.2.0] — 2026-07-04

### Added
- `templates/issue-template.md` — reusable weekly template with subject/preview front matter, read-time slots, and CASL/CAN-SPAM-compliant footer
- `PRODUCTION-CHECKLIST.md` — ≤90-minute weekly workflow, mandatory fact-check gate, kill criteria
- `scripts/build.py` — markdown → email-safe HTML (600px single column, inline styles, hidden inbox preview text) with pre-flight warnings for empty/unverified links

### Changed
- `PROPOSAL.md`: tooling comparison updated (ConvertKit → Kit rebrand; beehiiv added and recommended for its built-in referral program and free tier to 2,500 subscribers); CASL compliance section added; editorial-integrity rules added; name options table flags "The AI Edge" collision (6+ existing newsletters) and recommends a brand-anchored name
- `sample-issue-001.md`: subject line + preview text front matter added; read-time estimates added to every linked item; all placeholder links/stats tagged `VERIFY-URL` so they can't ship silently

### Fixed
- Data-privacy item in the sample issue: corrected the outdated claim that paid AI plans don't train on user data — since Aug 2025, personal ChatGPT and Claude plans (including paid tiers) train unless the user opts out; only business/commercial plans exclude training by default

## [0.1.0] — original

### Added
- `PROPOSAL.md` — concept, section structure, production guide, growth strategy, name options
- `sample-issue-001.md` — sample first issue in TLDR format
- `README.md`
