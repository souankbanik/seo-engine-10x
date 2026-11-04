---
name: seo-parasite
description: "Comprehensive Parasite SEO orchestration: platform-native content generation, high-DR host selection (Reddit, LinkedIn, Medium, Quora, Substack, Dev.to), Google Site Reputation Abuse (SRA) compliance, conversion bridging, and manual publishing blueprints. Triggers on: parasite SEO, parasite, Reddit SEO, LinkedIn Pulse, Medium ranking, Quora SEO, third-party ranking, high DR piggybacking."
user-invocable: true
argument-hint: "[keyword or plan] [offer-url]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "2.6.0"
  category: seo
---

# Parasite SEO: Universal High-DR Hijacking & Execution Skill

Parasite SEO is the art and science of publishing optimized content on high-authority, established third-party platforms (Reddit, LinkedIn Pulse, Medium, Quora, Substack, Dev.to, GitHub Pages) to rank on Google Page 1 within hours or days rather than waiting months for a brand-new domain to escape the Google sandbox.

This skill automates the heavy lifting: **keyword targeting, host platform opportunity scoring, psychological copy framing, and full post drafting**. It then hands you an explicit manual blueprint for account warming, publishing, and off-page velocity.

---

## The Initial Strategic Question

Whenever a user requests an SEO audit, campaign plan, content strategy, or asks `/seo plan` or `/seo audit`, **you MUST first ask the user:**

> **"Which SEO strategy do you want to pursue?"**
> 1. **Standard SEO Only:** Pure focus on your own domain (technical hygiene, on-page optimization, sitemaps, internal PageRank, and brand entity authority).
> 2. **Standard SEO + Parasite SEO (Recommended for rapid ROI):** Optimize your primary domain while simultaneously deploying high-converting parasite content across Reddit, LinkedIn, Medium, or Quora to capture instant Page 1 traffic and direct leads.
> 3. **What is Parasite SEO? (Explain it to me first):** Learn how high-DR host piggybacking works, why it ranks in hours, and how your primary site is insulated from risk before deciding.

*Note:* If Option 3 is chosen, provide the psychological & architectural explanation below, then let the user choose [1] or [2].

---

## How It Works: The Decision Flow

```
User Selects SEO Strategy
         │
         ├─────────────────────────────────────────┐
         ▼                                         ▼
[ 1. Standard SEO ]                    [ 2. Hybrid / Parasite SEO ]
• Technical audit                      • Standard technical audit
• Schema.org fix                       • PLUS: Run 'parasite_hunter.py'
• Internal link graph                  • PLUS: AI drafts full native posts
• Content on money site                • PLUS: AI builds conversion bridges
                                       • PLUS: User receives manual execution SOP
```

If the user selects **Standard SEO + Parasite SEO**, execute the 5-phase workflow below.

---

## Phase 1: Target Keyword & Intent Classification

Run the zero-auth keyword engine to isolate commercial and high-intent comparison queries:

```bash
python scripts/keyword_intel.py "<seed-keyword>"
```

Target queries with **Commercial Investigation** or **High-Intent Informational** modifiers:
* `best [product/software] for [use-case]`
* `[product] vs [competitor] review`
* `how to solve [expensive problem] in 2026`
* `[product] alternative for small business`

---

## Phase 2: Host Platform Opportunity Matrix

Run the Parasite Opportunity Hunter:

```bash
python scripts/parasite_hunter.py "<target-keyword>"
```

Select the host that matches the search intent and SERP features:

| Platform | Domain Authority | Indexing Latency | Primary Intent | Link Equity | SRA Hazard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Reddit** | DR 94 | < 30 Minutes | Reviews, Comparisons, User Opinions | Nofollow / UGC | Very Low |
| **LinkedIn Pulse** | DR 98 | 1 – 4 Hours | B2B, SaaS, Enterprise, Agency | Nofollow | Low |
| **Medium** | DR 93 | 2 – 6 Hours | Tech Tutorials, Deep Dives, Dev tools | Nofollow | Moderate |
| **Quora** | DR 92 | 2 – 12 Hours | Direct Problem Solving, Q&A | Nofollow | Low |
| **Substack** | DR 91 | 4 – 12 Hours | Financial, Longform Thought Leadership | Dofollow / Mixed | Very Low |
| **Dev.to / GitHub** | DR 88-96 | < 2 Hours | Code, APIs, Libraries, Open Source | Canonical / Dofollow | Very Low |

---

## Phase 3: What Claude Does (Automated Content Creation)

Claude writes the **complete, publication-ready post** using native psychological framing. Run:

```bash
python scripts/parasite_post_writer.py "<keyword>" --offer-name "<name>" --offer-url "<url>" --platform <reddit|linkedin|medium|quora>
```

### The 4 Native Formatting Paradigms

1. **Reddit (The Skeptical Practitioner):**
   * Never sounds like marketing copy.
   * Acknowledges flaws, tests competitors honestly, uses conversational slang, and soft-recommends the offer as the pragmatic standout.
2. **LinkedIn Pulse (The Executive Teardown):**
   * Structured with bold frameworks, ROI metrics, time-to-value benchmarks, and executive takeaways.
3. **Medium / Substack (The Data-Driven Case Study):**
   * Editorial storytelling, problem breakdown, comparative tables, and deep analysis.
4. **Quora (The Authoritative Problem-Solver):**
   * Answers existing top-ranking questions directly with 300+ words of upfront value before introducing the tool.

---

## Phase 4: Conversion & Traffic Routing Architecture

To protect your primary domain from algorithmic link penalties under Google's SpamBrain:
* **DO NOT** blast exact-match commercial anchor texts from parasite articles directly into your money site's homepage.
* **DO** route traffic through:
  * **Direct Affiliate Links:** Monetize directly on the parasite page.
  * **Lead Magnets / Free Tools:** Push traffic to an email capture or interactive calculator.
  * **Branded Naked Links:** Link to your brand name or URL (`yourbrand.com`) without keyword-stuffed anchor text.

---

## Phase 5: What Claude CANNOT Do (The User's Manual Checklist)

Claude generates the strategy and the copy, but the user must physically execute the platform interactions:

### 1. Account Age & Trust Preparation
* **Reddit:** Use an account with **30+ days age** and **100+ comment karma**. Posting commercial content on a fresh 0-karma burner triggers instant shadowbans.
* **LinkedIn:** Ensure your profile has a real photo, headline, and connection history.
* **Quora:** Fill out your bio credentials demonstrating expertise in the topic.

### 2. Manual Publishing & Formatting
* Copy the markdown generated by Claude into the target platform's editor.
* Add 1–2 relevant inline images or screenshots to break up text walls.
* Add relevant platform tags/hashtags (e.g. subreddits, LinkedIn tags).

### 3. Velocity Seeding (The First 3 Hours)
* Platforms calculate algorithmic momentum within the first 180 minutes.
* Reply immediately and thoughtfully to the first 3 comments on Reddit or LinkedIn.
* Share the published link in relevant Discord channels, Slack groups, or Twitter to spark early engagement.

### 4. Optional Tier-2 Power Blast
* Because high-DR platforms absorb link penalties, you can safely boost the parasite URL with secondary backlinks (social bookmarks, niche citations, Web 2.0s).
* **Rule:** Never point Tier-2 blasts at your main website—only point them at the high-DR parasite URL.
