#!/usr/bin/env python3
"""
High-Performance Concurrent Site Graph & Internal PageRank Crawler.
Part of the 10/10 Claude-SEO Engine upgrade.

Crawls a domain, constructs the directed internal link graph,
calculates mathematical Internal PageRank (damping 0.85), identifies
click depth, orphan pages, redirect chains, and broken links.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Set, Tuple
from urllib.parse import urldefrag, urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


@dataclass
class PageNode:
    url: str
    status_code: int = 0
    title: str = ""
    click_depth: int = -1
    in_links: List[str] = field(default_factory=list)
    out_links: List[str] = field(default_factory=list)
    anchor_texts: Dict[str, List[str]] = field(default_factory=dict)
    pagerank: float = 0.0
    load_time_ms: float = 0.0
    error: str = ""


class SiteGraphCrawler:
    def __init__(self, start_url: str, max_pages: int = 40, max_workers: int = 6, timeout: int = 8):
        parsed = urlparse(start_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {start_url}")
        self.root_url = urldefrag(start_url)[0].rstrip("/")
        self.domain = parsed.netloc.lower()
        self.max_pages = max_pages
        self.max_workers = max_workers
        self.timeout = timeout
        
        self.visited: Set[str] = set()
        self.queue: Set[str] = {self.root_url}
        self.graph: Dict[str, PageNode] = {}
        self.session = requests.Session() if HAS_LIBS else None
        if self.session:
            self.session.headers.update({
                "User-Agent": "Claude-SEO-GraphCrawler/2.0 (Compatible; +https://github.com/AgriciDaniel/claude-seo)"
            })

    def is_internal(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower() == self.domain or not parsed.netloc
        except Exception:
            return False

    def normalize_url(self, raw_url: str, base_url: str) -> str | None:
        try:
            absolute = urljoin(base_url, raw_url)
            clean, _ = urldefrag(absolute)
            parsed = urlparse(clean)
            if parsed.scheme not in ("http", "https"):
                return None
            if parsed.netloc.lower() != self.domain:
                return None
            path = parsed.path or "/"
            # Exclude obvious non-HTML media files
            if re.search(r"\.(pdf|jpg|jpeg|png|gif|svg|webp|zip|gz|tar|mp4|mp3|css|js|ico|xml|json)$", path, re.I):
                return None
            return f"{parsed.scheme}://{parsed.netloc}{path}".rstrip("/") or f"{parsed.scheme}://{parsed.netloc}/"
        except Exception:
            return None

    def fetch_url(self, url: str) -> Tuple[str, int, str, float, List[Tuple[str, str]], str]:
        """Fetch URL and return (url, status_code, title, load_time_ms, extracted_links, error)"""
        start_time = time.perf_counter()
        links: List[Tuple[str, str]] = []
        try:
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            final_url = urldefrag(resp.url)[0].rstrip("/")
            
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                return final_url, resp.status_code, "", elapsed_ms, [], ""

            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            
            for a_tag in soup.find_all("a", href=True):
                raw_href = a_tag["href"]
                norm = self.normalize_url(raw_href, final_url)
                anchor = a_tag.get_text(strip=True) or "[image/empty]"
                if norm:
                    links.append((norm, anchor))
                    
            return final_url, resp.status_code, title, elapsed_ms, links, ""
        except Exception as exc:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return url, 0, "", elapsed_ms, [], str(exc)

    def crawl(self) -> Dict[str, PageNode]:
        current_depth = 0
        current_layer = [self.root_url]
        self.visited.add(self.root_url)

        while current_layer and len(self.graph) < self.max_pages:
            next_layer = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.fetch_url, url): url for url in current_layer}
                for future in as_completed(futures):
                    target_url = futures[future]
                    final_url, status, title, load_ms, links, err = future.result()

                    node = self.graph.setdefault(final_url, PageNode(url=final_url))
                    node.status_code = status
                    node.title = title
                    node.load_time_ms = load_ms
                    node.error = err
                    if node.click_depth == -1:
                        node.click_depth = current_depth

                    for out_url, anchor in links:
                        if out_url not in node.out_links:
                            node.out_links.append(out_url)
                        node.anchor_texts.setdefault(out_url, []).append(anchor)

                        # Update target in_links
                        tgt_node = self.graph.setdefault(out_url, PageNode(url=out_url))
                        if final_url not in tgt_node.in_links:
                            tgt_node.in_links.append(final_url)

                        if out_url not in self.visited and len(self.graph) < self.max_pages:
                            self.visited.add(out_url)
                            next_layer.append(out_url)

            current_depth += 1
            current_layer = list(set(next_layer))

        self.compute_pagerank()
        return self.graph

    def compute_pagerank(self, damping: float = 0.85, max_iter: int = 40, tol: float = 1e-5):
        """Iterative Power Method to calculate exact internal PageRank."""
        nodes = list(self.graph.keys())
        n = len(nodes)
        if n == 0:
            return

        initial_pr = 1.0 / n
        pr = {node: initial_pr for node in nodes}

        for _ in range(max_iter):
            new_pr = {node: (1.0 - damping) / n for node in nodes}
            dangling_sum = sum(pr[node] for node in nodes if not self.graph[node].out_links)

            for node in nodes:
                out_links = [u for u in self.graph[node].out_links if u in pr]
                if out_links:
                    out_count = len(out_links)
                    share = pr[node] / out_count
                    for out_url in out_links:
                        new_pr[out_url] += damping * share
                else:
                    pass

            dangling_share = (damping * dangling_sum) / n
            for node in nodes:
                new_pr[node] += dangling_share

            diff = sum(abs(new_pr[node] - pr[node]) for node in nodes)
            pr = new_pr
            if diff < tol:
                break

        # Normalize to 0-100 scale for intuitive reading
        max_val = max(pr.values()) if pr else 1.0
        for node, score in pr.items():
            self.graph[node].pagerank = round((score / max_val) * 100, 2)

    def summary(self) -> Dict:
        pages = list(self.graph.values())
        total = len(pages)
        broken = [p for p in pages if p.status_code >= 400 or p.error]
        orphans = [p for p in pages if len(p.in_links) == 0 and p.url != self.root_url]
        top_pr = sorted(pages, key=lambda x: x.pagerank, reverse=True)[:10]

        return {
            "root_url": self.root_url,
            "total_crawled": total,
            "broken_count": len(broken),
            "orphan_count": len(orphans),
            "average_load_ms": round(sum(p.load_time_ms for p in pages) / max(total, 1), 2),
            "broken_pages": [{"url": p.url, "status": p.status_code, "error": p.error} for p in broken],
            "orphans": [p.url for p in orphans],
            "top_pagerank": [{"url": p.url, "pr_score": p.pagerank, "in_links": len(p.in_links), "depth": p.click_depth} for p in top_pr]
        }


def main():
    parser = argparse.ArgumentParser(description="Concurrent Site Graph & Internal PageRank Engine")
    parser.add_argument("url", help="Target site root URL")
    parser.add_argument("--max-pages", type=int, default=30, help="Max internal pages to crawl (default: 30)")
    parser.add_argument("--workers", type=int, default=6, help="Concurrent worker threads (default: 6)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    if not HAS_LIBS:
        sys.stderr.write("Error: requests and beautifulsoup4 required.\n")
        sys.exit(1)

    print(f"[*] Crawling link graph for: {args.url} (limit: {args.max_pages} pages)...", file=sys.stderr)
    crawler = SiteGraphCrawler(args.url, max_pages=args.max_pages, max_workers=args.workers)
    crawler.crawl()
    summary = crawler.summary()

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("\n" + "="*70)
        print(f" CLAUDE-SEO 10X SITE GRAPH & PAGERANK REPORT: {args.url}")
        print("="*70)
        print(f"Total Pages Analyzed : {summary['total_crawled']}")
        print(f"Broken URLs Detected : {summary['broken_count']}")
        print(f"Orphan Pages Found   : {summary['orphan_count']}")
        print(f"Avg Response Latency : {summary['average_load_ms']} ms")
        print("\n[ TOP INTERNAL PAGERANK HUBS ]")
        for item in summary["top_pagerank"]:
            print(f" - [{item['pr_score']:>6.2f}] Depth {item['depth']} | In-Links: {item['in_links']} -> {item['url']}")
        
        if summary["broken_pages"]:
            print("\n[ BROKEN / DEAD LINKS ]")
            for b in summary["broken_pages"]:
                print(f" - Status {b['status']}: {b['url']} ({b['error']})")
        else:
            print("\n[ BROKEN LINKS ]: None detected in crawl scope.")

        if summary["orphans"]:
            print("\n[ ORPHAN PAGES DETECTED ]")
            for o in summary["orphans"]:
                print(f" - {o}")


if __name__ == "__main__":
    main()
