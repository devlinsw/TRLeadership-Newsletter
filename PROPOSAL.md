# Newsletter Proposal for TRLeadership

## The Concept

A clean, scannable weekly email that demystifies AI for non-technical professionals — curated specifically around **how AI helps you at work**, not the tech industry itself.

Modeled after the [TLDR newsletter](https://tldr.tech) format: bold headlines, "(X minute read)" estimates, one-sentence summaries, organized into emoji-headed sections.

## Why This Works for TRLeadership

TRLeadership's brand is leadership development. A workplace AI newsletter extends that naturally:

- **It's not "here's AI news"** — it's "here's how a good leader thinks about and uses AI."
- **It's practical.** Every issue has something the reader can try that day.
- **It builds authority.** TRLeadership becomes the bridge between AI hype and real workplace value.
- **It grows the list.** A useful, free newsletter is a low-friction entry point for new subscribers who may later engage with TRLeadership's programs.

## Section Structure

| Icon | Section | What Goes In It |
|---|---|---|
| 🛠️ | **Tools You Can Use Today** | New ChatGPT/Copilot/Claude features explained plainly. "This week: Copilot can now summarize your meetings — here's the 30-second version." |
| 🏢 | **AI at Work** | How real companies are using AI. Not the tech — the outcome. "Sales team cut admin time 40% with this one workflow." |
| 📋 | **Quick Wins** | One or two actionable prompts or tips per issue. Copy-paste ready. |
| 🔍 | **What Leaders Need to Know** | Policy, ethics, team management around AI. Data privacy, when to say no, how to set guidelines. |
| ⚡ | **Worth a Click** | 4-5 short items. Light curation — interesting but not mission-critical. |

## What Makes It Different From TLDR

1. **Weekly, not daily.** Daily is overkill for this audience. Friday morning = ideal (readers have weekend headspace to try something).
2. **Zero technical vocabulary.** No "LLM," "RAG," "fine-tuning." Just "ChatGPT can now do X, here's how."
3. **Action-first.** Every issue has something the reader can *try that day*.
4. **Leadership lens.** Every section is filtered through "what does a leader need to know about this?"

## Production Guide

### Curation Sources (5-10 min/day to scan)

- **The Verge** / **TechCrunch** — AI section (consumer-facing coverage)
- **ZDNet** / **CNET** — practical AI coverage for non-devs
- **Microsoft 365 Blog** — Copilot feature updates
- **OpenAI Blog** — ChatGPT new features
- **LinkedIn** — what business people are actually sharing about AI
- **TLDR AI** — grab the 1-2 items that are workplace-relevant

### Tooling (Cheap/Free to Start)

| Platform | Why | Watch out |
|---|---|---|
| **Buttondown** | Writes in native markdown — pairs perfectly with this repo's workflow. Cheapest at small list sizes. | Fewer growth features; referral program is DIY |
| **beehiiv** | Built for TLDR-style newsletters: built-in referral program, web archive, polls, and a recommendation network that actually grows lists. Free to 2,500 subscribers. | Editor is block-based, not markdown-native (use `scripts/build.py` to paste HTML) |
| **Kit** (formerly ConvertKit) | Strong automations if the newsletter later feeds into TRLeadership program funnels | Priciest of the three as the list grows |

**Recommendation:** start on **beehiiv** — the free tier covers the first 2,500 subscribers, and the referral program in the growth plan (step 4 below) comes built-in instead of being a separate project at 500 subs.

- Write each issue in markdown from `templates/issue-template.md`
- Run `python3 scripts/build.py issues/issue-NNN.md` to generate email-ready HTML plus the subject/preview text
- Curation takes ~30 min/week once you have a rhythm (see `PRODUCTION-CHECKLIST.md`)

### Growth Strategy

1. Write 3 sample issues before launching — so subscribers see value immediately
2. Send to existing TRLeadership list first
3. Add a "Subscribe to The AI Edge" CTA on trleadership.ca
4. Encourage forwarding — TLDR-style referral program once list hits 500+
5. LinkedIn posts teasing individual items from each issue

## Name Options

| Name | Vibe | Availability |
|---|---|---|
| ~~**The AI Edge**~~ | Sharp, leadership-y | ⚠️ **Crowded.** At least six active newsletters already use this exact name (beehiiv, Substack, LinkedIn, standalone sites). Hard to rank for, easy to confuse. |
| **AI @ Work** | Literal, clear, no explanation needed | Check before committing |
| **Work Smarter** | Ties to productivity, softer | Check before committing |
| **The TRLeadership Brief** | Short, professional, brand-anchored | Safest — the brand name makes it unique by definition |

**Recommendation:** "The TRLeadership Brief" or another brand-anchored name. Generic AI names are saturated; anchoring to the TRLeadership brand is unique, searchable, and reinforces that this is *leadership* content, not another AI newsletter. Whatever the pick, search it + check the domain/handle before writing issue 2.

## Compliance (Canada — do this before the first send)

TRLeadership is Canadian, so **CASL** applies — and it's stricter than the US CAN-SPAM Act (penalties up to $10M for organizations):

1. **Express consent, recorded.** Double opt-in through the email platform, with date and method logged. Don't blast the existing TRLeadership list wholesale — send one invitation email asking people to opt in to the newsletter specifically.
2. **Identification.** Business name and a physical mailing address in every footer.
3. **Unsubscribe.** Working one-click unsubscribe in every send, honored within 10 business days. (The template and build script already include the footer slots.)

## Editorial Integrity (the credibility rule)

This newsletter's entire value is trust with a non-technical audience — one wrong claim they repeat in a meeting burns it. Two rules:

1. **No stat without a link to its primary source.** Not a blog citing the survey — the survey.
2. **Re-verify product claims every issue.** AI product features, pricing, and privacy policies change monthly. (Example: the common claim "paid AI plans don't train on your data" is now wrong for both ChatGPT and Claude — personal paid plans train unless the user opts out; only business plans exclude it by default. The kind of thing that changes under you.)

The fact-check gate in `PRODUCTION-CHECKLIST.md` makes this a 15-minute step, not a research project.

## Getting Started

1. Pick a name
2. Write 3 sample issues (see `sample-issue-001.md` for the first)
3. Send one to 10 people and ask: "Would you open this every Friday?"
4. If 7+ say yes — launch
5. Consistency beats perfection. A decent newsletter every Friday for 6 months beats a perfect one that ships twice.
