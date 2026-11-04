# Claude-SEO 10X Architecture & Operational Guide (v3.0.0)

**Engineered by Souank Banik · Nexus Web Studios**  
**Certified Standard:** Production-Grade 10/10 Autonomous SEO Engine  
**Runtime:** Python 3.11+, Linux, macOS, Windows

---

## 1. Unified Master Orchestration (`seo_engine.py`)

`seo_engine.py` is the single, hardened execution entrypoint for all automated workflows. It includes structured CLI parsing, ANSI color diagnostics, machine-readable `--json` modes, IndexNow push hooks, and unified exception handling.

### Master CLI Reference

```bash
# 1. System Health Check & Environment Diagnostic
python seo_engine.py doctor [--json]

# 2. Comprehensive On-Page, Schema & AI Search Audit
python seo_engine.py audit <url> [--output report.md] [--json]

# 3. Concurrent Multi-Threaded Link Graph & PageRank Calculation
python seo_engine.py crawl <url> [--max-pages 40] [--workers 6] [--json]

# 4. Zero-Auth Keyword Intent Harvesting & Topic Clustering
python seo_engine.py keywords "<seed-phrase>" [--json]

# 5. Parasite SEO Opportunity Matrix & SRA Check
python seo_engine.py parasite "<target-keyword>" [--json]

# 6. Autonomous Native Parasite Post Generation
python seo_engine.py write "<keyword>" --offer-name "<name>" --offer-url "<url>" --platform <reddit|linkedin|medium|quora> [--save]

# 7. AST & Framework-Aware Auto-Fixer (Safe Dry-Run by Default)
python seo_engine.py autofix <file_or_url> [--apply] [--title "..."] [--description "..."] [--canonical "..."]

# 8. Interactive Strategic Campaign Planner
python seo_engine.py plan <url> [--mode standard|parasite]

# 9. IndexNow Instant Search Submission
python seo_engine.py index <url1> <url2> [--host <host>] [--key <key>]
```

---

## 2. AST & Framework-Aware Auto-Fixer (`scripts/autofix_engine.py`)

The Auto-Fixer is not a crude regex string replacer. It inspects file structure and framework conventions to inject production metadata:

### Supported Frameworks
* **Next.js App Router (`.tsx`, `.jsx`)**:
  * Detects `layout.tsx` or `page.tsx`.
  * Injects or merges `export const metadata: Metadata = { ... }` with canonical links, OpenGraph, and Twitter cards.
  * Prepends `import type { Metadata } from 'next';` if missing.
* **Astro (`.astro`)**:
  * Detects frontmatter code fences (`--- ... ---`).
  * Injects canonical, title, and description props directly into frontmatter variables.
* **HTML5 (`.html`, `.htm`, or remote URL)**:
  * Uses BeautifulSoup DOM tree mutation.
  * Injects canonical tags, meta description, OpenGraph properties, and Schema.org JSON-LD graphs.
* **AI Engine Optimization (`/llms.txt`)**:
  * Emits standardized `/llms.txt` and `/llms-full.txt` for ChatGPT, Perplexity, and Claude citation engines.

### Mandatory Safe Mutation Engine
To prevent code corruption on production codebases:
1. **Dry-Run Mode (Default):** Running `python seo_engine.py autofix <file>` computes a unified diff preview without touching the disk.
2. **Git Branch Isolation:** Passing `--apply` automatically checks if the file is inside a Git repository and checks out an isolated safety branch:
   ```bash
   seo-autofix-<timestamp>  # e.g., seo-autofix-20261105-004012
   ```
3. **Rollback Backup:** Creates an immutable file snapshot (`<filename>.bak.<timestamp>`) before modifying a single byte.

---

## 3. Directed Site Graph & Mathematical PageRank Engine (`scripts/site_graph_crawler.py`)

* **Power Iteration Math:** Calculates internal PageRank using the exact Google PageRank formulation with a $0.85$ damping factor:
  $$PR(u) = \frac{1-d}{N} + d \sum_{v \in B_u} \frac{PR(v)}{L(v)}$$
* **Normalized Distribution:** Scaled to an intuitive $0 - 100$ score to identify top link hubs.
* **Orphan Detection:** Identifies pages with zero inbound internal links.
* **Click Depth:** Calculates shortest click path distance from homepage.

---

## 4. Zero-Auth Keyword Intel (`scripts/keyword_intel.py`)

* Bypasses \$500/mo API paywalls by executing recursive alphabet-soup expansion (`seed + a-z`) and preposition interrogatives (`how to`, `best`, `vs`, `why`).
* Classifies queries into **Informational, Commercial, Transactional, and Navigational**.
* Calculates algorithmic difficulty based on search intent saturation and term length.

---

## 5. Running the 10X Test Suite

The 10X engine includes an automated `pytest` verification suite covering all additions:

```bash
# Run complete 10X test suite
python -m pytest tests/test_seo_engine.py tests/test_autofix_engine.py tests/test_site_graph_crawler.py tests/test_keyword_intel.py tests/test_parasite_hunter.py tests/test_parasite_post_writer.py -v
```

All 22 test units verify:
- Environment diagnostic assertions and command parser tree.
- Mock network audit flows (simulated HTML and IndexNow webhooks).
- AST Next.js metadata injection, Astro frontmatter, and HTML DOM injection.
- Deterministic mathematical PageRank calculations and orphan page tracking.
- Zero-auth intent classification rules and harvest mocking.
- Parasite opportunity scoring algorithms and native post formatting.
