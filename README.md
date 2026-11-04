# Claude-SEO 10X

<p align="center">
  <b>The Universal Autonomous SEO & AI Search Engine</b><br />
  Built by <a href="https://github.com/souankbanik">Souank Banik</a>. Runs everywhere: Terminal, Claude Code, Antigravity, and Cursor.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue.svg" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Zero--Auth-100%25%20Free-brightgreen.svg" alt="Zero-Auth Engine" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-purple.svg" alt="Platforms" />
  <a href="https://github.com/souankbanik/claude-seo-10x"><img src="https://img.shields.io/badge/Status-Production%20Ready-success" alt="Status" /></a>
</p>

---

## What is Claude-SEO 10X?

Traditional SEO tools suffer from two fatal flaws: they trap you behind **\$500/month API subscriptions** (Ahrefs, Semrush, Google Ads developer tokens) and they only audit single pages in isolation.

**Claude-SEO 10X** is a next-generation autonomous SEO suite. It pairs deterministic mathematical graph algorithms (internal PageRank power iteration, multi-threaded site crawling, zero-auth keyword suggestion harvesting) with an **autonomous Parasite SEO engine** that drafts platform-native content to hijack Google Page 1 rankings within hours.

Whether you run it inside **Claude Code**, **Google Antigravity**, **Cursor**, or directly from your **Terminal CLI**, it delivers comprehensive audits, fixes code automatically, and executes high-velocity ranking campaigns.

---

## The 5 Pillars of 10X

```
┌────────────────────────────────────────────────────────────────────────┐
│                        seo_engine.py (Master CLI)                      │
│        python seo_engine.py <audit | crawl | keywords | parasite | fix> │
└──────────────────┬─────────────────┬───────────────────┬───────────────┘
                   │                 │                   │
  ┌────────────────▼─────────┐ ┌─────▼─────────────┐ ┌───▼──────────────┐
  │ site_graph_crawler.py    │ │ keyword_intel.py  │ │ autofix_engine.py│
  │ • Concurrent Link Graph  │ │ • Zero-Auth Intel │ │ • /llms.txt Gen  │
  │ • Iterative PageRank Math│ │ • Intent Clusters │ │ • JSON-LD Schema │
  │ • Orphan Page Detection  │ │ • Difficulty Heur.│ │ • Meta & OG Tags │
  └──────────────────────────┘ └───────────────────┘ └──────────────────┘
```

### 1. 🕸️ Concurrent Site Graph & Internal PageRank Engine
* **Iterative Power Method:** Computes exact mathematical internal PageRank ($PR$, damping 0.85) across your entire domain.
* **Orphan Page Detection:** Automatically flags pages that have zero internal links pointing to them.
* **Click Depth & Broken Link Mapping:** Traces crawl depth from the homepage and catches 404/500 redirect errors concurrently.

### 2. ⚡ Zero-Auth Keyword & Semantic Intent Engine
* **No Paid API Keys Required:** Bypasses expensive SaaS subscriptions by tapping real-time search suggestion APIs.
* **Recursive Alphabet-Soup:** Expands any seed keyword across `[seed] + a-z` and prepositions (`how to`, `best`, `vs`, `why`).
* **Algorithmic Intent Classification:** Categorizes queries into **Informational, Commercial Investigation, Transactional, and Navigational**.
* **Semantic Topic Silos:** Automatically groups 150+ long-tail queries into topical content clusters with difficulty scores.

### 3. 🩸 Autonomous Parasite SEO Engine
* **Strategic Decision Gate:** When planning a campaign, choose between Standard SEO or Standard + Parasite SEO (with built-in explainer for beginners).
* **Platform Feasibility Matrix:** Scores host titans (Reddit, LinkedIn Pulse, Medium, Quora, Substack, Dev.to) for authority (DR 85–98) and Google **Site Reputation Abuse (SRA)** policy compliance.
* **Autonomous Native Content Writer:** Generates publication-ready articles matching native psychological framing (skeptical practitioner style for Reddit, executive teardown for LinkedIn, deep-dive for Medium).
* **Manual Execution SOP:** Hands you the exact step-by-step checklist for account warming, karma requirements, image placement, and early velocity seeding.

### 4. 🤖 AI Search & GEO Optimization (Generative Engine Optimization)
* **Automated `/llms.txt` Generator:** Extracts navigation and core documentation to create standardized markdown summaries for Perplexity, ChatGPT, Gemini, and Claude.
* **Schema.org `@graph` Synthesizer:** Detects page entity types and emits valid JSON-LD structured data.
* **Metadata Auto-Fixer:** Generates canonical tags, OpenGraph cards, and Twitter cards ready to copy directly into your HTML.

### 5. 💻 Universal Master CLI (`seo_engine.py`)
* One unified entry point for all workflows. Run audits, crawls, keyword harvesting, or content generation on any operating system with terminal tables and optional `--json` export.

---

## Quickstart & Installation

### Option A: Direct Terminal CLI (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/souankbanik/claude-seo-10x.git
cd claude-seo-10x

# 2. Install lightweight dependencies
pip install beautifulsoup4 lxml requests urllib3

# 3. Verify system health
python seo_engine.py doctor
```

### Option B: Inside Claude Code

Add as a plugin directly inside Claude Code:
```bash
/plugin marketplace add souankbanik/claude-seo-10x
/plugin install claude-seo@souankbanik-claude-seo
/seo setup
```

---

## CLI Command Cheatsheet

| Command | Action |
| :--- | :--- |
| `python seo_engine.py doctor` | Check core libraries and system readiness |
| `python seo_engine.py audit <url>` | Full on-page, schema, and AI readiness audit |
| `python seo_engine.py audit <url> --output report.md` | Run audit and export findings to Markdown |
| `python seo_engine.py crawl <url> --max-pages 40` | Concurrent link graph crawl & mathematical PageRank |
| `python seo_engine.py keywords "<seed>"` | Zero-auth long-tail keyword harvesting & intent clustering |
| `python seo_engine.py parasite "<keyword>"` | Parasite SEO platform opportunity matrix & SRA check |
| `python seo_engine.py write "<keyword>" --offer-name "<name>" --offer-url "<url>" --platform reddit --save` | Draft complete native parasite article + manual guide |
| `python seo_engine.py fix llms-txt <url> --save` | Auto-generate `/llms.txt` for AI search visibility |
| `python seo_engine.py fix schema <url>` | Auto-generate structured Schema.org JSON-LD |
| `python seo_engine.py plan <url>` | Interactive strategic planning session (Standard vs Parasite) |

---

## The Strategic Decision Gate

When running `python seo_engine.py plan <url>` or invoking `/seo plan`, the engine provides an interactive choice gate:

```text
Select your operational route:
  [1] Standard SEO Only (On-page, technical, schema, and internal PageRank)
  [2] Standard SEO + Parasite SEO (Recommended: Rapid Page 1 hijack via Reddit/LinkedIn/Medium + Direct Leads)
  [3] What is Parasite SEO? (Explain how it works, pros/cons, and risks before I decide)
```

* **Option 1:** Focuses purely on long-term authority and technical foundation for your primary domain.
* **Option 2:** Audits your primary domain while simultaneously drafting high-converting parasite content for instant Page 1 traffic.
* **Option 3:** Explains how high-DR domain piggybacking works, the psychology of authority bias, and how your money site is insulated from risk before prompting you to choose.

---

## Division of Labor (AI Automation vs. Human Execution)

```
┌────────────────────────────────────────────────────────┐
│             WHAT THE ENGINE DOES FOR YOU               │
├────────────────────────────────────────────────────────┤
│ • Zero-Auth Keyword Mining & Commercial Intent Mapping │
│ • Platform Opportunity Scoring (DR 85-98) & SRA Check  │
│ • Mathematical Internal PageRank & Graph Calculations  │
│ • Full Post Drafting in Native Platform Tone:          │
│   - Reddit: Skeptical, honest breakdown (anti-shill)   │
│   - LinkedIn Pulse: Executive teardown & ROI metrics   │
│   - Medium / Substack: Deep-dive comparative case study│
│   - Quora: High-authority problem-solver response      │
│ • Auto-generates /llms.txt and Schema.org JSON-LD      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              WHAT YOU (THE USER) DO                    │
├────────────────────────────────────────────────────────┤
│ 1. Account Prep: Use a 30+ day account (100+ karma)    │
│ 2. Publishing: Paste the markdown draft into the host  │
│ 3. Polish: Drop 1–2 inline screenshots or banner       │
│ 4. Velocity: Reply to first 3 comments within 3 hours  │
│ 5. Tier-2 Blast: (Optional) Point web 2.0 links at     │
│    the parasite URL (never at your money site)         │
└────────────────────────────────────────────────────────┘
```

---

## Architecture & Sub-Skills

This repository contains **27 sub-skills** and **20 specialized agents** following the open Agent Skills architecture:

* `skills/seo/`: Main orchestration router and interactive decision gate.
* `skills/seo-parasite/`: Dedicated Parasite SEO strategy, platform taxonomy, and execution guide.
* `skills/seo-technical/`: 9-category technical hygiene, crawlability, and security inspection.
* `skills/seo-content/`: E-E-A-T evaluator, content depth scoring, and metadata templating lint.
* `skills/seo-geo/`: Generative Engine Optimization for ChatGPT, Perplexity, and Google AI Overviews.
* `skills/seo-schema/`: Rich results markup detection, validation, and generation.
* `skills/seo-sitemap/`: XML sitemap structure, freshness checks, and generation.

---

## Author & Credits

* **Architect & Developer:** **[Souank Banik](https://github.com/souankbanik)**
* **License:** [MIT License](LICENSE) — free and open source for commercial and personal use.
