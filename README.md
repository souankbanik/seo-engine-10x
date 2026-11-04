# Claude-SEO 10X

<p align="center">
  <b>The Universal Autonomous SEO &amp; AI Search Engine</b><br />
  Engineered by <a href="https://github.com/souankbanik">Souank Banik</a> · <b>Nexus Web Studios</b>.<br />
  Runs natively in Terminal CLI, Claude Code, Google Antigravity, and Cursor.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue.svg" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Zero--Auth-100%25%20Free-brightgreen.svg" alt="Zero-Auth Engine" />
  <img src="https://img.shields.io/badge/Tests-22%20Passing%20(100%25)-success" alt="Tests" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-purple.svg" alt="Platforms" />
  <a href="https://github.com/souankbanik/claude-seo-10x"><img src="https://img.shields.io/badge/Release-v3.0.0%20Certified-blue" alt="Version" /></a>
</p>

---

## What is Claude-SEO 10X?

Traditional SEO tools suffer from two fatal flaws: they trap you behind **\$500/month API subscriptions** (Ahrefs, Semrush, Google Ads developer tokens) and they only audit single pages in isolation.

**Claude-SEO 10X** is a production-hardened autonomous SEO engine. It pairs deterministic mathematical graph algorithms (internal PageRank power iteration, multi-threaded site crawling, zero-auth keyword suggestion harvesting) with an **autonomous Parasite SEO engine** that drafts platform-native content to hijack Google Page 1 rankings within hours.

Additionally, its **AST & Framework-Aware Auto-Fixer** directly patches modern framework codebases (**Next.js App Router**, **Astro**, **React**, **HTML5**) with automated Git branch safety isolation.

---

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        seo_engine.py (Master CLI)                      │
│     python seo_engine.py <audit|crawl|keywords|parasite|write|autofix> │
└──────────────────┬─────────────────┬───────────────────┬───────────────┘
                   │                 │                   │
  ┌────────────────▼─────────┐ ┌─────▼─────────────┐ ┌───▼──────────────┐
  │ site_graph_crawler.py    │ │ keyword_intel.py  │ │ autofix_engine.py│
  │ • Concurrent Link Graph  │ │ • Zero-Auth Intel │ │ • Next.js App Rtr│
  │ • Iterative PageRank Math│ │ • Intent Clusters │ │ • Astro Fences   │
  │ • Orphan Page Detection  │ │ • Difficulty Heur.│ │ • Branch Isolation│
  └──────────────────────────┘ └───────────────────┘ └──────────────────┘
```

### The 5 Pillars of 10X

1. **🕸️ Concurrent Site Graph & Internal PageRank Engine (`scripts/site_graph_crawler.py`)**
   * **Iterative Power Method:** Computes exact mathematical internal PageRank ($PR$, damping 0.85) across your entire domain.
   * **Orphan Page Detection:** Automatically flags pages that have zero internal links pointing to them.
   * **Click Depth & Broken Link Mapping:** Traces shortest path distance from homepage and catches 404/500 errors concurrently.

2. **⚡ Zero-Auth Keyword & Semantic Intent Engine (`scripts/keyword_intel.py`)**
   * **Zero Paid API Keys Required:** Bypasses expensive SaaS subscriptions by tapping real-time search suggestion APIs.
   * **Recursive Alphabet-Soup:** Expands any seed keyword across `[seed] + a-z` and prepositions (`how to`, `best`, `vs`, `why`).
   * **Algorithmic Intent Classification:** Categorizes queries into **Informational, Commercial Investigation, Transactional, and Navigational**.
   * **Semantic Topic Silos:** Automatically groups 150+ long-tail queries into topical content clusters with difficulty scores.

3. **🩸 Autonomous Parasite SEO Engine (`skills/seo-parasite/`)**
   * **Strategic Decision Gate:** When planning a campaign, choose between Standard SEO or Standard + Parasite SEO (with built-in explainer for beginners).
   * **Platform Feasibility Matrix:** Scores host titans (Reddit, LinkedIn Pulse, Medium, Quora, Substack, Dev.to) for authority (DR 85–98) and Google **Site Reputation Abuse (SRA)** policy compliance.
   * **Autonomous Native Content Writer:** Generates publication-ready articles matching native psychological framing (skeptical practitioner style for Reddit, executive teardown for LinkedIn, deep-dive for Medium).
   * **Manual Execution SOP:** Hands you the exact step-by-step checklist for account warming, karma requirements, image placement, and early velocity seeding.

4. **🛠️ AST & Framework-Aware Auto-Fixer (`scripts/autofix_engine.py`)**
   * **Modern Framework Support:**
     * **Next.js App Router:** Automatically injects or merges `export const metadata: Metadata = { ... }` in `layout.tsx` or `page.tsx`.
     * **Astro:** Injects frontmatter code variables (`--- ... ---`).
     * **HTML5:** Injects Canonical tags, OpenGraph properties, and Schema.org `@graph` JSON-LD.
   * **Mandatory Safe Mutation:** Defaults to non-destructive unified diff dry-runs. When applied with `--apply`, automatically creates an isolated git branch (`seo-autofix-<timestamp>`) with backup rollback files.

5. **💻 Unified Master CLI (`seo_engine.py`)**
   * One unified entry point for all workflows. Run audits, crawls, keyword harvesting, or content generation on any operating system with ANSI color formatting and `--json` pipeline support.

---

## Quickstart & Installation

```bash
# 1. Clone the repository
git clone https://github.com/souankbanik/claude-seo-10x.git
cd claude-seo-10x

# 2. Install lightweight dependencies
pip install beautifulsoup4 lxml requests urllib3 pytest

# 3. Verify system health
python seo_engine.py doctor
```

---

## Master CLI Cheatsheet

| Command | Action |
| :--- | :--- |
| `python seo_engine.py doctor` | Check core libraries and system readiness |
| `python seo_engine.py audit <url>` | Full on-page, schema, and AI readiness audit |
| `python seo_engine.py audit <url> --output report.md` | Run audit and export findings to Markdown |
| `python seo_engine.py crawl <url> --max-pages 40` | Concurrent link graph crawl & mathematical PageRank |
| `python seo_engine.py keywords "<seed>"` | Zero-auth long-tail keyword harvesting & intent clustering |
| `python seo_engine.py parasite "<keyword>"` | Parasite SEO platform opportunity matrix & SRA check |
| `python seo_engine.py write "<keyword>" --offer-name "<name>" --offer-url "<url>" --platform reddit --save` | Draft complete native parasite article + manual guide |
| `python seo_engine.py autofix page.tsx` | Dry-run preview of Next.js metadata injection |
| `python seo_engine.py autofix page.tsx --apply` | Apply mutation safely on an isolated Git branch |
| `python seo_engine.py plan <url>` | Interactive strategic planning session (Standard vs Parasite) |
| `python seo_engine.py index <url>` | Dispatch URLs to IndexNow open search API |

---

## Running the Automated Test Suite

Verify all systems with the comprehensive 10X test suite:

```bash
python -m pytest tests/test_seo_engine.py tests/test_autofix_engine.py tests/test_site_graph_crawler.py tests/test_keyword_intel.py tests/test_parasite_hunter.py tests/test_parasite_post_writer.py -v
```

**Test Status:** 22 passing (100% pass rate).

---

## Author & Organization

* **Architect & Maintainer:** **[Souank Banik](https://github.com/souankbanik)**
* **Studio:** **Nexus Web Studios**
* **License:** [MIT License](LICENSE) — free and open source for commercial and personal use.
