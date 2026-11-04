#!/usr/bin/env python3
"""
Claude-SEO 10X Unified Master Orchestration Engine.
Engineered by Souank Banik (Nexus Web Studios).

Single robust entrypoint for:
  - Full-spectrum site audits (On-page, Schema, AI / LLM readiness)
  - Concurrent site graph crawling & mathematical internal PageRank (0.85 damping)
  - Zero-auth real-time keyword intelligence & intent clustering
  - Parasite SEO opportunity scoring & autonomous native post generation
  - AST & Framework-Aware Auto-Fixing (Next.js, Astro, React, HTML5) with git branch isolation
  - IndexNow submission hooks & environment validation
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

# Resolve local scripts directory
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


# -----------------------------------------------------------------------------
# Unified Logging & ANSI Styling
# -----------------------------------------------------------------------------
class TerminalColor:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


class EngineLogger:
    def __init__(self, json_mode: bool = False):
        self.json_mode = json_mode

    def info(self, msg: str):
        if not self.json_mode:
            print(f"{TerminalColor.CYAN}[INFO]{TerminalColor.RESET} {msg}", file=sys.stderr)

    def success(self, msg: str):
        if not self.json_mode:
            print(f"{TerminalColor.GREEN}[OK]{TerminalColor.RESET} {msg}", file=sys.stderr)

    def warn(self, msg: str):
        if not self.json_mode:
            print(f"{TerminalColor.YELLOW}[WARN]{TerminalColor.RESET} {msg}", file=sys.stderr)

    def error(self, msg: str):
        if not self.json_mode:
            print(f"{TerminalColor.RED}[ERROR]{TerminalColor.RESET} {msg}", file=sys.stderr)


# -----------------------------------------------------------------------------
# Environment & Diagnostic Validation
# -----------------------------------------------------------------------------
def check_environment() -> Dict[str, Any]:
    core_packages = ["requests", "bs4", "lxml", "urllib3"]
    pkg_status = {}
    for p in core_packages:
        try:
            __import__(p)
            pkg_status[p] = True
        except ImportError:
            pkg_status[p] = False

    env_vars = {
        "DATAFORSEO_LOGIN": bool(os.getenv("DATAFORSEO_LOGIN")),
        "GOOGLE_APPLICATION_CREDENTIALS": bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")),
        "MOZ_ACCESS_ID": bool(os.getenv("MOZ_ACCESS_ID")),
        "INDEXNOW_KEY": bool(os.getenv("INDEXNOW_KEY")),
        "BING_API_KEY": bool(os.getenv("BING_API_KEY"))
    }

    git_ready = False
    try:
        res = subprocess.run(["git", "--version"], capture_output=True, text=True)
        git_ready = res.returncode == 0
    except Exception:
        git_ready = False

    return {
        "python_version": sys.version.split()[0],
        "git_available": git_ready,
        "packages": pkg_status,
        "credentials": env_vars,
        "all_core_installed": all(pkg_status.values()),
        "mode": "Zero-Auth Autonomous" if not any(env_vars.values()) else "API-Augmented Hybrid"
    }


def run_doctor(json_mode: bool = False):
    diag = check_environment()
    if json_mode:
        print(json.dumps(diag, indent=2))
        return

    print("\n" + "="*70)
    print(f" {TerminalColor.BOLD}CLAUDE-SEO 10X: SYSTEM DIAGNOSTIC & ENVIRONMENT HEALTH{TerminalColor.RESET}")
    print("="*70)
    print(f"Engine Runtime  : Python {diag['python_version']} (Git: {'Ready' if diag['git_available'] else 'Not Found'})")
    print(f"Operating Mode  : {TerminalColor.GREEN}{diag['mode']}{TerminalColor.RESET}")

    print("\n[ Core Parsers & Network Libraries ]")
    for pkg, status in diag["packages"].items():
        if status:
            print(f"  {TerminalColor.GREEN}[OK]{TerminalColor.RESET} {pkg:<12} (Installed)")
        else:
            print(f"  {TerminalColor.RED}[X]{TerminalColor.RESET} {pkg:<12} (Missing: run 'pip install {pkg}')")

    print("\n[ Optional External Credential Bridges ]")
    for cred, status in diag["credentials"].items():
        state = f"{TerminalColor.GREEN}Configured{TerminalColor.RESET}" if status else f"{TerminalColor.DIM}Unset (Zero-Auth Fallback Active){TerminalColor.RESET}"
        print(f"  - {cred:<32}: {state}")

    if diag["all_core_installed"]:
        print(f"\n{TerminalColor.GREEN}[STATUS] System is fully certified for 10X production workflows.{TerminalColor.RESET}\n")
    else:
        print(f"\n{TerminalColor.YELLOW}[ACTION REQUIRED] Install missing libraries: pip install beautifulsoup4 lxml requests{TerminalColor.RESET}\n")


# -----------------------------------------------------------------------------
# Audit Workflow
# -----------------------------------------------------------------------------
def run_audit(url: str, logger: EngineLogger, json_out: bool = False, output_file: str = "") -> Dict[str, Any]:
    if not HAS_LIBS:
        logger.error("requests and beautifulsoup4 required for site audits.")
        sys.exit(1)

    logger.info(f"Auditing target: {url}")
    start_time = time.perf_counter()
    headers = {"User-Agent": "Claude-SEO-Engine/10.0 (Autonomous Systems Auditor)"}

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        latency = round((time.perf_counter() - start_time) * 1000, 2)
    except Exception as exc:
        logger.error(f"Network error while connecting to {url}: {exc}")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    final_url = resp.url

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    desc = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
    canonical = soup.find("link", rel=re.compile("canonical", re.I))
    canonical_href = canonical["href"].strip() if canonical and canonical.get("href") else ""
    
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
    schemas = soup.find_all("script", type="application/ld+json")
    images = soup.find_all("img")
    missing_alt = [img.get("src", "[inline]") for img in images if not img.get("alt")]

    llms_url = urljoin(final_url, "/llms.txt")
    llms_active = False
    try:
        llms_active = requests.head(llms_url, timeout=3).status_code == 200
    except Exception:
        pass

    score = 100
    findings = []
    if not title:
        score -= 15; findings.append("Missing <title> tag (Critical)")
    elif len(title) < 30 or len(title) > 65:
        score -= 5; findings.append(f"Suboptimal title length ({len(title)} chars; recommend 40-60)")

    if not desc:
        score -= 12; findings.append("Missing meta description (High)")
    elif len(desc) < 80 or len(desc) > 165:
        score -= 4; findings.append(f"Suboptimal meta description length ({len(desc)} chars)")

    if not canonical_href:
        score -= 10; findings.append("Missing canonical tag (High)")

    if len(h1s) == 0:
        score -= 10; findings.append("Missing H1 heading (High)")
    elif len(h1s) > 1:
        score -= 5; findings.append(f"Multiple H1 tags found ({len(h1s)}; recommend exactly 1)")

    if len(schemas) == 0:
        score -= 10; findings.append("Missing Schema.org JSON-LD structured data")

    if not llms_active:
        score -= 8; findings.append("Missing /llms.txt (Suboptimal for AI search engines & LLMs)")

    if missing_alt:
        score -= min(10, len(missing_alt) * 2); findings.append(f"{len(missing_alt)} images missing alt text")

    score = max(10, score)

    report = {
        "url": final_url,
        "score": score,
        "latency_ms": latency,
        "status_code": resp.status_code,
        "title": title,
        "meta_description": desc,
        "canonical": canonical_href,
        "h1_count": len(h1s),
        "h2_count": len(h2s),
        "schema_count": len(schemas),
        "image_count": len(images),
        "missing_alt_count": len(missing_alt),
        "llms_txt_active": llms_active,
        "findings": findings
    }

    if json_out:
        print(json.dumps(report, indent=2))
        return report

    print("\n" + "="*70)
    print(f" {TerminalColor.BOLD}CLAUDE-SEO 10X AUDIT: {final_url}{TerminalColor.RESET}")
    print("="*70)
    color = TerminalColor.GREEN if score >= 80 else (TerminalColor.YELLOW if score >= 50 else TerminalColor.RED)
    print(f"Health Score           : {color}{score} / 100{TerminalColor.RESET}")
    print(f"Latency & HTTP Status  : {latency} ms (HTTP {resp.status_code})")
    print(f"Page Title             : {title or '[NONE]'}")
    print(f"Canonical URL          : {canonical_href or '[NONE]'}")
    print(f"Schema JSON-LD Blocks  : {len(schemas)}")
    print(f"AI Search (/llms.txt)  : {'ACTIVE (Found)' if llms_active else 'MISSING'}")
    print("\n[ ACTIONABLE FINDINGS ]")
    if findings:
        for f in findings:
            print(f"  {TerminalColor.YELLOW}[!]{TerminalColor.RESET} {f}")
    else:
        print(f"  {TerminalColor.GREEN}[OK] Pristine technical health.{TerminalColor.RESET}")

    if output_file:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(f"# SEO Audit Report for {final_url}\n\n- **Score:** {score}/100\n- **Latency:** {latency}ms\n\n## Findings\n")
            for f in findings:
                out.write(f"- {f}\n")
        logger.success(f"Report exported to: {output_file}")

    return report


# -----------------------------------------------------------------------------
# IndexNow Submission Hook
# -----------------------------------------------------------------------------
def submit_indexnow(urls: List[str], key: str = "", host: str = "", logger: Optional[EngineLogger] = None):
    if not urls:
        if logger:
            logger.warn("No URLs provided for indexing submission.")
        return

    first_url = urls[0]
    parsed = urlparse(first_url)
    target_host = host or parsed.netloc
    target_key = key or os.getenv("INDEXNOW_KEY", "claude_seo_10x_key")

    payload = {
        "host": target_host,
        "key": target_key,
        "keyLocation": f"https://{target_host}/{target_key}.txt",
        "urlList": urls
    }

    if logger:
        logger.info(f"Submitting {len(urls)} URLs to IndexNow for host '{target_host}'...")

    try:
        resp = requests.post("https://api.indexnow.org/indexnow", json=payload, headers={"Content-Type": "application/json; charset=utf-8"}, timeout=8)
        if resp.status_code in (200, 202):
            if logger:
                logger.success(f"IndexNow submission accepted (HTTP {resp.status_code}).")
        else:
            if logger:
                logger.warn(f"IndexNow returned HTTP {resp.status_code}: {resp.text}")
    except Exception as exc:
        if logger:
            logger.error(f"IndexNow dispatch failed: {exc}")


# -----------------------------------------------------------------------------
# Main CLI Router
# -----------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seo_engine.py",
        description="Claude-SEO 10X Autonomous Engine by Souank Banik (Nexus Web Studios)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Verify system environment & API credentials")
    p_doc.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # audit
    p_audit = subparsers.add_parser("audit", help="Run comprehensive technical & AI-readiness audit")
    p_audit.add_argument("url", help="Target URL to inspect")
    p_audit.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    p_audit.add_argument("--output", default="", help="Export markdown report file")

    # crawl
    p_crawl = subparsers.add_parser("crawl", help="Concurrent site graph & mathematical PageRank crawl")
    p_crawl.add_argument("url", help="Target site root URL")
    p_crawl.add_argument("--max-pages", type=int, default=30, help="Max internal pages (default: 30)")
    p_crawl.add_argument("--workers", type=int, default=6, help="Worker threads (default: 6)")
    p_crawl.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # keywords
    p_kw = subparsers.add_parser("keywords", help="Zero-auth long-tail keyword intel & intent clusters")
    p_kw.add_argument("seed", help="Seed search phrase")
    p_kw.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # parasite
    p_para = subparsers.add_parser("parasite", help="Parasite SEO platform opportunity matrix & SRA check")
    p_para.add_argument("keyword", help="Target keyword")
    p_para.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # write
    p_write = subparsers.add_parser("write", help="Autonomous platform-native parasite content writer")
    p_write.add_argument("keyword", help="Target keyword")
    p_write.add_argument("--offer-name", required=True, help="Product or offer name")
    p_write.add_argument("--offer-url", required=True, help="Destination or affiliate link")
    p_write.add_argument("--platform", choices=["reddit", "linkedin", "medium", "quora", "substack"], default="reddit")
    p_write.add_argument("--save", action="store_true", help="Save directly to disk")

    # autofix
    p_fix = subparsers.add_parser("autofix", help="AST & Framework-Aware Auto-Fixer (Next.js, Astro, HTML)")
    p_fix.add_argument("target", help="Target file (.tsx, .jsx, .astro, .html) or URL")
    p_fix.add_argument("--title", default="", help="Page title")
    p_fix.add_argument("--description", default="", help="Meta description")
    p_fix.add_argument("--canonical", default="", help="Canonical URL")
    p_fix.add_argument("--apply", action="store_true", help="Apply mutations directly to disk (default: dry-run)")
    p_fix.add_argument("--no-branch", action="store_true", help="Skip git branch creation when applying")
    p_fix.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # plan
    p_plan = subparsers.add_parser("plan", help="Interactive strategic planner (Standard vs Parasite SEO)")
    p_plan.add_argument("url", help="Your site root URL")
    p_plan.add_argument("--mode", choices=["standard", "parasite"], default="", help="Pre-select strategy route")

    # index
    p_idx = subparsers.add_parser("index", help="Submit URLs to IndexNow open indexing network")
    p_idx.add_argument("urls", nargs="+", help="One or more URLs to index")
    p_idx.add_argument("--host", default="", help="Explicit host")
    p_idx.add_argument("--key", default="", help="IndexNow key")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    logger = EngineLogger(json_mode=getattr(args, "json", False))

    if not args.command:
        print(r"""
  ___ _       _   _      ___ ___ ___   __  _____  __
 / __| |__ _ | | | |    / __| __/ _ \ /  \|_   _| \ \
| (__| / _` || |_| |___ \__ \ _| (_) | () | | |    > >
 \___|_\__,_||___|_____||___/___|___/ \__/  |_|   /_/ 
   Production 10X Engine · Souank Banik · Nexus Web Studios
        """)
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "doctor":
            run_doctor(json_mode=args.json)

        elif args.command == "audit":
            run_audit(args.url, logger=logger, json_out=args.json, output_file=args.output)

        elif args.command == "crawl":
            from site_graph_crawler import SiteGraphCrawler
            logger.info(f"Crawling link graph: {args.url} (max pages: {args.max_pages})")
            crawler = SiteGraphCrawler(args.url, max_pages=args.max_pages, max_workers=args.workers)
            crawler.crawl()
            summary = crawler.summary()
            if args.json:
                print(json.dumps(summary, indent=2))
            else:
                print("\n" + "="*70)
                print(f" {TerminalColor.BOLD}INTERNAL PAGERANK & LINK GRAPH REPORT: {args.url}{TerminalColor.RESET}")
                print("="*70)
                print(f"Pages Crawled : {summary['total_crawled']}")
                print(f"Broken Links  : {summary['broken_count']}")
                print(f"Orphan Pages  : {summary['orphan_count']}")
                print(f"Average Latency: {summary['average_load_ms']} ms")
                print("\n[ TOP PAGERANK HUBS ]")
                for it in summary["top_pagerank"][:6]:
                    print(f"  [{it['pr_score']:>5.2f}] Inbound: {it['in_links']} | Depth: {it['depth']} -> {it['url']}")

        elif args.command == "keywords":
            from keyword_intel import KeywordIntelEngine
            logger.info(f"Harvesting zero-auth long-tail queries for: '{args.seed}'")
            engine = KeywordIntelEngine(args.seed)
            data = engine.harvest()
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print("\n" + "="*70)
                print(f" {TerminalColor.BOLD}KEYWORD INTENT INTELLIGENCE: '{args.seed.upper()}'{TerminalColor.RESET}")
                print("="*70)
                print(f"Discovered: {data['total_harvested']} queries across {len(data['clusters'])} topic clusters\n")
                for cluster, items in list(data["clusters"].items())[:6]:
                    print(f"-- [ Topic Cluster: {cluster} ({len(items)} queries) ] --")
                    for it in items[:4]:
                        print(f"   [{it['intent']:<13}] ({it['difficulty_level']:<6} Diff {it['difficulty_score']:>2}) -> {it['keyword']}")
                    print()

        elif args.command == "parasite":
            from parasite_hunter import ParasiteHunter
            logger.info(f"Evaluating parasite host platforms for: '{args.keyword}'")
            hunter = ParasiteHunter(args.keyword)
            data = hunter.evaluate()
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print("\n" + "="*70)
                print(f" {TerminalColor.BOLD}PARASITE SEO OPPORTUNITY MATRIX: '{args.keyword.upper()}'{TerminalColor.RESET}")
                print("="*70)
                for p in data["recommended_platforms"][:4]:
                    print(f"Platform: {p['platform']} (DR {p['domain_rating']}) | Score: {p['opportunity_score']}/100 | SRA Risk: {p['sra_risk']}")
                    print(f" - Speed: {p['indexing_speed']} | Moderation: {p['moderation']}")
                    print(f" - Strategy: {p['notes']}\n")

        elif args.command == "write":
            from parasite_post_writer import ParasiteContentWriter
            logger.info(f"Drafting native {args.platform.title()} content for: '{args.keyword}'")
            writer = ParasiteContentWriter(args.keyword, args.offer_name, args.offer_url, args.platform)
            res = writer.generate()
            print("\n" + "="*70)
            print(f" {TerminalColor.BOLD}AUTONOMOUS PARASITE POST: [{args.platform.upper()}]{TerminalColor.RESET}")
            print("="*70)
            print(f"\n[SUGGESTED TITLE]\n{res['title']}\n")
            print("[POST BODY]")
            print(res["content"])
            print("\n" + "-"*70)
            print(res["manual_checklist"])
            print("-"*70)
            if args.save:
                fname = f"parasite_{args.platform}_{args.keyword.replace(' ', '_')}.md"
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(f"# {res['title']}\n\n{res['content']}\n\n---\n\n{res['manual_checklist']}\n")
                logger.success(f"Draft saved to: {fname}")

        elif args.command == "autofix":
            from autofix_engine import AutoFixEngine
            engine = AutoFixEngine(args.target, title=args.title, description=args.description, canonical_url=args.canonical)
            res = engine.execute_safely(dry_run=not args.apply, create_branch=not args.no_branch)
            if args.json:
                print(json.dumps({
                    "target": res.target_path,
                    "framework": res.framework,
                    "applied": res.applied,
                    "branch": res.branch_name,
                    "backup": res.backup_path,
                    "diff": res.diff_preview,
                    "error": res.error
                }, indent=2))
            else:
                print("\n" + "="*70)
                print(f" {TerminalColor.BOLD}AUTO-FIXER RESULT: {res.target_path} [{res.framework.upper()}]{TerminalColor.RESET}")
                print("="*70)
                if res.applied:
                    logger.success("Mutation applied successfully to disk.")
                    if res.branch_name:
                        print(f"  [GIT SAFETY] Branch isolated: {res.branch_name}")
                    if res.backup_path:
                        print(f"  [BACKUP] Snapshot created: {res.backup_path}")
                else:
                    logger.info("DRY-RUN PREVIEW (No files modified. Pass --apply to execute)")
                print("\n[ UNIFIED DIFF PREVIEW ]")
                print(res.diff_preview or "No modifications required.")

        elif args.command == "plan":
            print("\n" + "="*70)
            print(f" {TerminalColor.BOLD}STRATEGIC SEO PLANNING ENGINE: {args.url}{TerminalColor.RESET}")
            print("="*70)
            mode = args.mode.lower()
            if not mode:
                while True:
                    print("\nSelect your operational route:")
                    print("  [1] Standard SEO Only (On-page, technical, schema, and internal PageRank)")
                    print("  [2] Standard SEO + Parasite SEO (Recommended: Rapid Page 1 hijack via Reddit/LinkedIn/Medium + Direct Leads)")
                    print("  [3] What is Parasite SEO? (Explain how it works, pros/cons, and risks before I decide)")
                    choice = input("\nEnter choice (1, 2, or 3, default: 2): ").strip()
                    if choice == "3":
                        print("\n" + "="*70)
                        print(" [EXPLAINER: WHAT IS PARASITE SEO?]")
                        print("="*70)
                        print("• Concept: You publish high-converting content on high-authority titan domains")
                        print("  (like Reddit, LinkedIn Pulse, Medium, or Quora) instead of waiting 6-12 months")
                        print("  for a brand-new website to escape the Google sandbox.")
                        print("• Psychology & Trust: Readers and Google algorithms already trust domain giants")
                        print("  (DR 90-98). Your content inherits that root trust instantly (Halo Effect).")
                        print("• Velocity: Pages index in minutes/hours and can rank on Google Page 1 in days.")
                        print("• Safety: If Google algorithmically demotes the page, the hit lands on the host")
                        print("  platform, NOT your money site. You route traffic via clean brand links or offers.")
                        print("="*70)
                        continue
                    mode = "standard" if choice == "1" else "parasite"
                    break

            logger.info(f"Executing strategy route: {mode.upper()}")
            print("\n--- [ PHASE 1: TECHNICAL & DOMAIN AUDIT ] ---")
            run_audit(args.url, logger=logger)

            if mode == "parasite":
                print("\n--- [ PHASE 2: PARASITE HIGH-DR FAST-TRACK ] ---")
                kw = input("\nEnter primary commercial keyword (e.g. 'best crm software'): ").strip() or "best productivity software"
                offer_name = input("Enter product / offer brand name: ").strip() or "Our Platform"
                offer_url = input(f"Enter target URL for {offer_name}: ").strip() or args.url

                from parasite_hunter import ParasiteHunter
                from parasite_post_writer import ParasiteContentWriter

                hunter = ParasiteHunter(kw)
                p_data = hunter.evaluate()
                top_platform = p_data["recommended_platforms"][0]["platform"].lower()
                plat_slug = "reddit" if "reddit" in top_platform else ("linkedin" if "linkedin" in top_platform else "medium")

                logger.success(f"Best host platform: {p_data['recommended_platforms'][0]['platform']} (Score: {p_data['recommended_platforms'][0]['opportunity_score']}/100)")
                logger.info(f"Drafting native {plat_slug.title()} article...")

                writer = ParasiteContentWriter(kw, offer_name, offer_url, plat_slug)
                p_post = writer.generate()

                fname = f"parasite_{plat_slug}_{kw.replace(' ', '_')}.md"
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(f"# {p_post['title']}\n\n{p_post['content']}\n\n---\n\n{p_post['manual_checklist']}\n")

                logger.success(f"Drafted and saved to: {fname}")
                print("\n" + "="*70)
                print(" [WHAT CLAUDE DID FOR YOU]:")
                print(f" - Scored host platforms for '{kw}'")
                print(f" - Formatted publication-ready {plat_slug.title()} post with conversion hooks")
                print(f" - Saved draft to {fname}")
                print("\n [WHAT YOU MUST MANUALLY DO]:")
                print(p_post["manual_checklist"])
                print("="*70)

        elif args.command == "index":
            submit_indexnow(args.urls, key=args.key, host=args.host, logger=logger)

    except KeyboardInterrupt:
        logger.warn("Operation aborted by user.")
        sys.exit(130)
    except Exception as exc:
        logger.error(f"Execution failed: {exc}")
        if os.getenv("DEBUG"):
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
