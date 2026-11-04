#!/usr/bin/env python3
"""
Claude-SEO 10X Master Engine & CLI Runner.
Universal entry point for Antigravity, Cursor, Claude Code, and terminal automation.

Commands:
  audit     - Comprehensive on-page, technical, schema, and AI-readiness audit
  crawl     - Deep multi-threaded site crawl with mathematical internal PageRank & orphan detection
  keywords  - Zero-auth real-time keyword intelligence, search intent, & semantic clustering
  parasite  - Parasite SEO feasibility scanner, host platform scoring & SRA policy check
  write     - Autonomous platform-native parasite post generator (Reddit, LinkedIn, Medium, Quora)
  fix       - Instant generator for /llms.txt, Schema.org JSON-LD graphs, and meta tags
  plan      - Interactive strategy session (Prompts: Standard SEO vs Standard + Parasite SEO)
  doctor    - Diagnostic check of environment, libraries, and optional API keys
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


def print_banner():
    banner = r"""
  ___ _       _   _      ___ ___ ___   __  _____  __
 / __| |__ _ | | | |    / __| __/ _ \ /  \|_   _| \ \
| (__| / _` || |_| |___ \__ \ _| (_) | () | | |    > >
 \___|_\__,_||___|_____||___/___|___/ \__/  |_|   /_/ 
            10/10 Universal Autonomous Engine
    """
    print(banner)


def run_doctor():
    print("\n" + "="*65)
    print(" CLAUDE-SEO 10X ENGINE: SYSTEM DIAGNOSTIC")
    print("="*65)
    print(f"Python Version : {sys.version.split()[0]}")
    print(f"Working Dir    : {os.getcwd()}")
    print(f"Scripts Path   : {SCRIPTS_DIR}")

    modules = ["requests", "bs4", "lxml", "urllib3"]
    print("\n[ Core Libraries ]")
    for m in modules:
        try:
            __import__(m)
            print(f"  [OK] {m:<12} (Installed)")
        except ImportError:
            print(f"  [MISSING] {m:<8} (Run: pip install {m})")

    optional_keys = [
        ("DATAFORSEO_LOGIN", "Live SERP & Merchant data"),
        ("MOZ_ACCESS_ID", "Moz DA/PA & Link Explorer"),
        ("GOOGLE_APPLICATION_CREDENTIALS", "Google Search Console & CrUX APIs"),
        ("BING_API_KEY", "Bing Webmaster Tools & IndexNow")
    ]
    print("\n[ Optional External APIs (Not required for Zero-Auth) ]")
    for var, desc in optional_keys:
        status = "CONFIGURED" if os.getenv(var) else "NOT SET (Zero-Auth mode active)"
        print(f"  - {var:<30} : {status}")
    print("\nSystem status: READY FOR FULL-POWER EXECUTION.\n")


def run_audit(url: str, json_out: bool = False, output_file: str = ""):
    if not HAS_LIBS:
        sys.stderr.write("Error: requests and beautifulsoup4 required.\n")
        sys.exit(1)

    print(f"[*] Auditing {url} across technical, semantic, schema, and AI-readiness vectors...", file=sys.stderr)
    start_time = time.perf_counter()
    headers = {"User-Agent": "Claude-SEO-Engine/10.0 (Autonomous Audit Bot)"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        load_time = round((time.perf_counter() - start_time) * 1000, 2)
    except Exception as exc:
        sys.stderr.write(f"Failed to fetch {url}: {exc}\n")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    final_url = resp.url

    # Technical
    status_code = resp.status_code
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    desc_content = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
    canonical = soup.find("link", rel=re.compile("canonical", re.I))
    canonical_href = canonical["href"].strip() if canonical and canonical.get("href") else ""
    robots_meta = soup.find("meta", attrs={"name": re.compile(r"robots", re.I)})
    robots_content = robots_meta["content"].strip() if robots_meta and robots_meta.get("content") else "index, follow"

    # Headings
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]

    # Structured Data
    json_lds = soup.find_all("script", type="application/ld+json")
    schemas_detected = len(json_lds)

    # Images
    images = soup.find_all("img")
    missing_alt = [img.get("src", "[inline]") for img in images if not img.get("alt")]

    # AI Readiness (GEO / AEO)
    llms_url = urljoin(final_url, "/llms.txt")
    llms_status = False
    try:
        llm_check = requests.head(llms_url, timeout=3)
        if llm_check.status_code == 200:
            llms_status = True
    except Exception:
        pass

    # Score calculation
    score = 100
    findings = []
    
    if not title:
        score -= 15
        findings.append("Missing <title> tag (Critical)")
    elif len(title) < 30 or len(title) > 65:
        score -= 5
        findings.append(f"Suboptimal title length ({len(title)} chars; recommend 40-60)")

    if not desc_content:
        score -= 12
        findings.append("Missing meta description (High)")
    elif len(desc_content) < 80 or len(desc_content) > 165:
        score -= 4
        findings.append(f"Suboptimal meta description length ({len(desc_content)} chars; recommend 120-160)")

    if not canonical_href:
        score -= 10
        findings.append("Missing self-referential canonical tag (High)")

    if len(h1s) == 0:
        score -= 10
        findings.append("Missing H1 heading tag (High)")
    elif len(h1s) > 1:
        score -= 5
        findings.append(f"Multiple H1 tags detected ({len(h1s)} found; recommend exactly 1)")

    if schemas_detected == 0:
        score -= 10
        findings.append("No Schema.org JSON-LD structured data detected (High for Rich Results)")

    if not llms_status:
        score -= 8
        findings.append("Missing /llms.txt file (Medium for AI Search & LLM citation)")

    if missing_alt:
        score -= min(10, len(missing_alt) * 2)
        findings.append(f"{len(missing_alt)} images missing 'alt' attributes")

    score = max(10, score)

    report_data = {
        "url": final_url,
        "score": score,
        "load_time_ms": load_time,
        "status_code": status_code,
        "title": title,
        "meta_description": desc_content,
        "canonical": canonical_href,
        "robots_directive": robots_content,
        "h1_tags": h1s,
        "h2_count": len(h2s),
        "schema_blocks_found": schemas_detected,
        "images_analyzed": len(images),
        "missing_alt_count": len(missing_alt),
        "llms_txt_active": llms_status,
        "findings": findings
    }

    if json_out:
        print(json.dumps(report_data, indent=2))
        return

    print("\n" + "="*70)
    print(f" CLAUDE-SEO 10X AUDIT REPORT: {final_url}")
    print("="*70)
    print(f"Overall SEO Health Score: {score} / 100")
    print(f"Server Response Latency : {load_time} ms (HTTP {status_code})")
    print(f"Title Tag               : {title or '[NONE]'}")
    print(f"Meta Description        : {desc_content or '[NONE]'}")
    print(f"Canonical Target        : {canonical_href or '[NONE]'}")
    print(f"Schema JSON-LD Blocks   : {schemas_detected}")
    print(f"AI Readiness (/llms.txt): {'ACTIVE (Found)' if llms_status else 'MISSING (Unoptimized for LLMs)'}")
    print(f"Image Optimization      : {len(images)} total ({len(missing_alt)} missing alt)")

    print("\n[ ACTIONABLE FINDINGS & RECOMMENDATIONS ]")
    if findings:
        for f in findings:
            print(f" [!] {f}")
    else:
        print(" [OK] Pristine technical hygiene. No critical flags detected.")

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# SEO Audit Report for {final_url}\n\n")
            f.write(f"- **Score:** {score}/100\n")
            f.write(f"- **Response Latency:** {load_time}ms\n\n")
            f.write("## Findings\n")
            for f in findings:
                f.write(f"- {f}\n")
        print(f"\n[+] Full markdown report exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Claude-SEO 10X Autonomous Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Audit
    p_audit = subparsers.add_parser("audit", help="Run comprehensive on-page & AI audit")
    p_audit.add_argument("url", help="Target URL")
    p_audit.add_argument("--json", action="store_true", help="JSON output")
    p_audit.add_argument("--output", default="", help="Export to markdown file")

    # Crawl
    p_crawl = subparsers.add_parser("crawl", help="Crawl site graph & calculate PageRank")
    p_crawl.add_argument("url", help="Root URL")
    p_crawl.add_argument("--max-pages", type=int, default=25, help="Max pages")
    p_crawl.add_argument("--json", action="store_true", help="JSON output")

    # Keywords
    p_kw = subparsers.add_parser("keywords", help="Zero-auth keyword research & intent clustering")
    p_kw.add_argument("seed", help="Seed keyword phrase")
    p_kw.add_argument("--json", action="store_true", help="JSON output")

    # Parasite
    p_para = subparsers.add_parser("parasite", help="Parasite SEO platform matrix & SRA check")
    p_para.add_argument("keyword", help="Target keyword")
    p_para.add_argument("--json", action="store_true", help="JSON output")

    # Write (Parasite Post Generator)
    p_write = subparsers.add_parser("write", help="Generate platform-native parasite post")
    p_write.add_argument("keyword", help="Target search keyword")
    p_write.add_argument("--offer-name", required=True, help="Product or offer name")
    p_write.add_argument("--offer-url", required=True, help="Affiliate or destination URL")
    p_write.add_argument("--platform", choices=["reddit", "linkedin", "medium", "quora", "substack"], default="reddit")
    p_write.add_argument("--save", action="store_true", help="Save directly to markdown file")

    # Fix
    p_fix = subparsers.add_parser("fix", help="Generate /llms.txt, Schema, or Meta tags")
    p_fix.add_argument("action", choices=["llms-txt", "schema", "meta", "all"])
    p_fix.add_argument("target", help="Target URL or local HTML file")
    p_fix.add_argument("--save", action="store_true", help="Save directly to disk")

    # Plan (Interactive Strategy Selector)
    p_plan = subparsers.add_parser("plan", help="Interactive SEO strategy planner (Standard vs Hybrid Parasite)")
    p_plan.add_argument("url", help="Your website URL")
    p_plan.add_argument("--mode", choices=["standard", "parasite"], default="", help="Skip prompt and set mode directly")

    # Doctor
    subparsers.add_parser("doctor", help="System and dependency diagnostic")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    if args.command == "doctor":
        run_doctor()
    elif args.command == "audit":
        run_audit(args.url, json_out=args.json, output_file=args.output)
    elif args.command == "crawl":
        from site_graph_crawler import SiteGraphCrawler
        crawler = SiteGraphCrawler(args.url, max_pages=args.max_pages)
        crawler.crawl()
        summary = crawler.summary()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("\n" + "="*70)
            print(f" INTERNAL PAGERANK & LINK GRAPH REPORT: {args.url}")
            print("="*70)
            print(f"Crawled: {summary['total_crawled']} pages | Broken: {summary['broken_count']} | Orphans: {summary['orphan_count']}")
            print("\n[ TOP PAGERANK HUBS ]")
            for item in summary["top_pagerank"][:6]:
                print(f" - PR: {item['pr_score']:>5.2f} (Inbound: {item['in_links']}, Depth: {item['depth']}) -> {item['url']}")
    elif args.command == "keywords":
        from keyword_intel import KeywordIntelEngine
        engine = KeywordIntelEngine(args.seed)
        data = engine.harvest()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"\n[+] Discovered {data['total_harvested']} Long-Tail Keywords for '{args.seed}':")
            for cluster, items in list(data["clusters"].items())[:6]:
                print(f"\n-- {cluster} ({len(items)} queries) --")
                for it in items[:4]:
                    print(f"   [{it['intent']:<13}] ({it['difficulty_level']:<6}) -> {it['keyword']}")
    elif args.command == "parasite":
        from parasite_hunter import ParasiteHunter
        hunter = ParasiteHunter(args.keyword)
        data = hunter.evaluate()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"\n[+] Parasite SEO Recommendations for '{args.keyword}':")
            for p in data["recommended_platforms"][:3]:
                print(f" - {p['platform']} (DR {p['domain_rating']}) | Score: {p['opportunity_score']}/100 | SRA Risk: {p['sra_risk']}")
                print(f"   Edge: {p['notes']}\n")
    elif args.command == "fix":
        from autofix_engine import AutoFixEngine
        engine = AutoFixEngine(args.target)
        if args.action in ("llms-txt", "all"):
            res = engine.generate_llms_txt()
            print("\n--- GENERATED /llms.txt ---")
            print(res)
            if args.save:
                with open("llms.txt", "w", encoding="utf-8") as f:
                    f.write(res)
                print("[+] Saved llms.txt")
        if args.action in ("schema", "all"):
            res = engine.generate_schema()
            print("\n--- GENERATED SCHEMA.ORG JSON-LD ---")
            print(json.dumps(res, indent=2))
        if args.action in ("meta", "all"):
            res = engine.generate_meta_tags()
            print("\n--- GENERATED META TAGS ---")
            print(res)
    elif args.command == "write":
        from parasite_post_writer import ParasiteContentWriter
        writer = ParasiteContentWriter(args.keyword, args.offer_name, args.offer_url, args.platform)
        res = writer.generate()
        print("\n" + "="*70)
        print(f" AUTONOMOUS PARASITE POST: [{args.platform.upper()}] FOR '{args.keyword.upper()}'")
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
            print(f"\n[+] Saved to {fname}")
    elif args.command == "plan":
        print("\n" + "="*70)
        print(f" STRATEGIC SEO PLANNING ENGINE: {args.url}")
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

        print(f"\n[*] Executing strategy mode: {mode.upper()}")
        print("\n--- [ PHASE 1: TECHNICAL & DOMAIN AUDIT ] ---")
        run_audit(args.url)

        if mode == "parasite":
            print("\n--- [ PHASE 2: PARASITE HIGH-DR FAST-TRACK ] ---")
            kw = input("\nEnter your primary commercial keyword (e.g. 'best crm software'): ").strip() or "best productivity software"
            offer_name = input("Enter your product / offer brand name: ").strip() or "Our Platform"
            offer_url = input(f"Enter target URL / link for {offer_name}: ").strip() or args.url

            from parasite_hunter import ParasiteHunter
            from parasite_post_writer import ParasiteContentWriter

            hunter = ParasiteHunter(kw)
            p_data = hunter.evaluate()
            top_platform = p_data["recommended_platforms"][0]["platform"].lower()
            if "reddit" in top_platform:
                plat_slug = "reddit"
            elif "linkedin" in top_platform:
                plat_slug = "linkedin"
            else:
                plat_slug = "medium"

            print(f"\n[+] Best matching host platform: {p_data['recommended_platforms'][0]['platform']} (Score: {p_data['recommended_platforms'][0]['opportunity_score']}/100)")
            print(f"[*] Drafting native {plat_slug.title()} post...")

            writer = ParasiteContentWriter(kw, offer_name, offer_url, plat_slug)
            p_post = writer.generate()

            fname = f"parasite_{plat_slug}_{kw.replace(' ', '_')}.md"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(f"# {p_post['title']}\n\n{p_post['content']}\n\n---\n\n{p_post['manual_checklist']}\n")

            print(f"\n[+] Ready-to-publish post drafted and saved to: {fname}")
            print("\n" + "="*70)
            print(" [WHAT CLAUDE DID FOR YOU]:")
            print(f" - Scored host platforms for '{kw}'")
            print(f" - Formatted publication-ready {plat_slug.title()} article with native conversion hooks")
            print(f" - Saved complete draft to {fname}")
            print("\n [WHAT YOU MUST MANUALLY DO]:")
            print(p_post["manual_checklist"])
            print("="*70)


if __name__ == "__main__":
    main()
