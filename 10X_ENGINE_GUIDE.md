# Claude-SEO 10X Upgrade: The Complete Architecture & Execution Guide

---

## Overview

The standard `claude-seo` repository has been upgraded from a Claude-Code-only audit plugin to a **10/10 Universal Autonomous SEO Engine**. It now operates independently across Windows, Linux, macOS, and inside AI agent harnesses (Antigravity, Cursor, Cline, or direct terminal CLI) with zero mandatory paid API dependencies.

---

## What Was Added (The 10/10 Upgrades)

### 1. Master CLI Orchestrator (`seo_engine.py`)
A unified command-line entrypoint at the root of the repository. Run any audit, crawl, keyword query, parasite analysis, or code generation with a single command:
```bash
python seo_engine.py doctor
python seo_engine.py audit <url> [--json] [--output report.md]
python seo_engine.py crawl <url> [--max-pages 50] [--json]
python seo_engine.py keywords <seed> [--json]
python seo_engine.py parasite <keyword> [--json]
python seo_engine.py fix <llms-txt|schema|meta|all> <target> [--save]
```

### 2. Concurrent Site Graph & Mathematical PageRank Engine (`scripts/site_graph_crawler.py`)
* **Solves the crawling blindspot:** Does not just audit a single page.
* Crawls entire internal site networks using multi-threaded worker pools.
* Calculates mathematical **Internal PageRank** ($PR$) distribution across all URLs using the iterative power method (damping factor 0.85).
* Identifies **Orphan Pages** (pages with zero internal inbound links).
* Pinpoints **Click Depth** from the homepage and catches broken links / redirect chains.

### 3. Zero-Auth Keyword & Semantic Intent Engine (`scripts/keyword_intel.py`)
* **Solves the API-lockout blindspot:** Eliminates the requirement for paid \$500/mo API keys (Ahrefs, Semrush, or Google Ads developer tokens).
* Performs recursive alphabet-soup (`seed + a-z`) and prepositional queries (`how to`, `best`, `vs`, `why`).
* Automatically classifies Search Intent:
  * **Informational** (guides, definitions, tutorials)
  * **Commercial Investigation** (reviews, comparisons, alternatives)
  * **Transactional** (pricing, buy, coupon, discount)
  * **Navigational** (login, portal, download)
* Calculates algorithmic difficulty based on word count, modifier density, and commercial saturation.
* Groups queries into semantic topic clusters for easy content silo creation.

### 4. Parasite SEO Hunter & Feasibility Engine (`scripts/parasite_hunter.py`)
* Evaluates top high-DR platforms: **Reddit, LinkedIn Pulse, Medium, Quora, Substack, Dev.to, GitHub Pages**.
* Computes Parasite Opportunity Index (POI) against target search keywords.
* Assesses vulnerability against Google's **Site Reputation Abuse (SRA)** policy.
* Outlines tactical execution blueprints (native tone rules, traffic routing, and indexing speed).

### 5. Automated "One-Click" Generator & Auto-Fixer (`scripts/autofix_engine.py`)
* **Generates `/llms.txt` and `/llms-full.txt`:** Automatically extracts navigation and documentation links from any site or HTML file to optimize for Perplexity, ChatGPT, and AI Overviews.
* **Synthesizes Schema.org JSON-LD Graphs:** Detects page entity type and outputs valid structured data with complete `@graph` hierarchy.
* **Builds Social & Meta Directives:** Emits canonicals, OpenGraph, and Twitter Cards ready to copy-paste into code.

---

## Quick Reference CLI Cheatsheet

| Task | Command |
| :--- | :--- |
| **Verify System Health** | `python seo_engine.py doctor` |
| **Run Full Site Audit** | `python seo_engine.py audit https://your-site.com` |
| **Export Audit to Markdown** | `python seo_engine.py audit https://your-site.com --output audit.md` |
| **Internal PageRank Crawl** | `python seo_engine.py crawl https://your-site.com --max-pages 40` |
| **Zero-Auth Keyword Research** | `python seo_engine.py keywords "saas analytics"` |
| **Parasite SEO Evaluation** | `python seo_engine.py parasite "best email tracker"` |
| **Auto-Generate /llms.txt** | `python seo_engine.py fix llms-txt https://your-site.com --save` |
| **Generate Schema JSON-LD** | `python seo_engine.py fix schema https://your-site.com` |

| **Autonomous Parasite Post Writer** | `python seo_engine.py write "keyword" --offer-name "Brand" --offer-url "https://..." --platform reddit --save` |
| **Interactive Strategy Planner** | `python seo_engine.py plan https://your-site.com` |

---

## The Strategic Decision Gate (Standard SEO vs Hybrid Parasite SEO)

Whenever you launch an audit, strategy session, or campaign planning flow, the system poses the **Strategic Decision Gate**:

> **"Do you want to run:**
> 1. **Standard SEO Only:** Technical hygiene, on-page optimization, sitemaps, internal PageRank, and brand entity authority.
> 2. **Standard SEO + Parasite SEO (Recommended):** Standard domain audit PLUS instant Page 1 high-DR parasite deployment (Reddit, LinkedIn, Medium, Quora) to capture immediate organic clicks and leads."

### Division of Labor (AI vs User)

```
┌──────────────────────────────────────────────┐
│        WHAT CLAUDE & THE ENGINE DO           │
├──────────────────────────────────────────────┤
│ 1. Harvest high-intent commercial keywords   │
│ 2. Score host platforms (DR, index speed)    │
│ 3. Check Google Site Reputation Abuse risk   │
│ 4. Write 100% complete, platform-native copy │
│    • Reddit: skeptical, unbiased breakdown   │
│    • LinkedIn: executive benchmark teardown  │
│    • Medium: editorial case study            │
│    • Quora: expert problem-solver format     │
│ 5. Construct conversion bridge & lead paths  │
└──────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│           WHAT YOU (THE USER) DO             │
├──────────────────────────────────────────────┤
│ 1. Use 30+ day aged account (100+ karma)     │
│ 2. Copy/paste draft into target platform     │
│ 3. Add 1-2 native images or screenshots      │
│ 4. Seed early engagement in first 180 min    │
│ 5. Point secondary Tier-2 links (optional)   │
└──────────────────────────────────────────────┘
```
