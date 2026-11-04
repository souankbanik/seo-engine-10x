#!/usr/bin/env python3
"""
Automated SEO Auto-Fixer & Generator Engine.
Part of the 10/10 Claude-SEO Engine upgrade.

Generates production-grade /llms.txt, structured JSON-LD schemas,
and missing meta/social tags directly from any target URL or HTML file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


class AutoFixEngine:
    def __init__(self, target: str):
        self.target = target.strip()
        self.soup = None
        self.final_url = target
        self._load()

    def _load(self):
        if not HAS_LIBS:
            raise RuntimeError("requests and beautifulsoup4 required.")
        if self.target.startswith("http://") or self.target.startswith("https://"):
            headers = {"User-Agent": "Claude-SEO-AutoFix/2.0 (Compatible)"}
            resp = requests.get(self.target, headers=headers, timeout=10)
            self.final_url = resp.url
            self.soup = BeautifulSoup(resp.text, "html.parser")
        else:
            with open(self.target, "r", encoding="utf-8") as f:
                self.soup = BeautifulSoup(f.read(), "html.parser")

    def generate_llms_txt(self) -> str:
        """Generate standard /llms.txt file."""
        title = self.soup.title.string.strip() if self.soup.title and self.soup.title.string else urlparse(self.final_url).netloc
        meta_desc = self.soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
        desc_text = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else f"Comprehensive documentation and resources for {title}."

        links = []
        for a in self.soup.find_all("a", href=True):
            href = urljoin(self.final_url, a["href"])
            text = a.get_text(strip=True)
            if text and len(text) > 2 and urlparse(href).netloc == urlparse(self.final_url).netloc:
                if href not in [l[0] for l in links]:
                    links.append((href, text))

        lines = [
            f"# {title}",
            "",
            f"> {desc_text}",
            "",
            "## Overview",
            f"This site provides structured information, tools, and technical documentation regarding {title}.",
            "",
            "## Core Resources",
        ]

        for href, text in links[:12]:
            lines.append(f"- [{text}]({href})")

        lines.extend([
            "",
            "## Optional / Deep Context",
            f"- [Full LLM Context]({urljoin(self.final_url, '/llms-full.txt')}): Complete uncensored context dump for agent reasoning."
        ])

        return "\n".join(lines)

    def generate_schema(self, schema_type: str = "auto") -> Dict:
        """Generate production-ready Schema.org JSON-LD graph."""
        title = self.soup.title.string.strip() if self.soup.title and self.soup.title.string else "Untitled"
        meta_desc = self.soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
        desc = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
        domain = urlparse(self.final_url).netloc

        # Detect schema type if auto
        if schema_type == "auto":
            h1 = self.soup.find("h1")
            h1_text = h1.get_text(strip=True).lower() if h1 else ""
            if "faq" in title.lower() or self.soup.find_all(class_=re.compile("faq", re.I)):
                schema_type = "FAQPage"
            elif any(w in h1_text for w in ["tool", "software", "api", "app"]):
                schema_type = "SoftwareApplication"
            else:
                schema_type = "WebPage"

        graph = [
            {
                "@type": "Organization",
                "@id": f"{self.final_url}#/schema/organization",
                "name": domain,
                "url": f"{urlparse(self.final_url).scheme}://{domain}"
            },
            {
                "@type": schema_type,
                "@id": f"{self.final_url}#/schema/{schema_type.lower()}",
                "url": self.final_url,
                "name": title,
                "description": desc,
                "isPartOf": {
                    "@id": f"{self.final_url}#/schema/organization"
                }
            }
        ]

        return {
            "@context": "https://schema.org",
            "@graph": graph
        }

    def generate_meta_tags(self) -> str:
        """Generate missing standard & social OpenGraph / Twitter meta tags."""
        title = self.soup.title.string.strip() if self.soup.title and self.soup.title.string else "Page Title"
        meta_desc = self.soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
        desc = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else "Add concise 150-character description here."

        tags = [
            f'<title>{title}</title>',
            f'<meta name="description" content="{desc}">',
            f'<link rel="canonical" href="{self.final_url}">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<meta property="og:title" content="{title}">',
            f'<meta property="og:description" content="{desc}">',
            f'<meta property="og:url" content="{self.final_url}">',
            '<meta property="og:type" content="website">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{title}">',
            f'<meta name="twitter:description" content="{desc}">'
        ]
        return "\n".join(tags)


def main():
    parser = argparse.ArgumentParser(description="Automated SEO Generator & Auto-Fixer")
    parser.add_argument("target", help="Target URL or local HTML file")
    parser.add_argument("--action", choices=["llms-txt", "schema", "meta", "all"], default="all")
    parser.add_argument("--save", action="store_true", help="Save files directly to disk")
    args = parser.parse_args()

    engine = AutoFixEngine(args.target)

    if args.action in ("llms-txt", "all"):
        llms_content = engine.generate_llms_txt()
        print("\n" + "="*60)
        print(" GENERATED /llms.txt (AI Search & Agent Optimization)")
        print("="*60)
        print(llms_content)
        if args.save:
            with open("llms.txt", "w", encoding="utf-8") as f:
                f.write(llms_content)
            print("\n[+] Saved to llms.txt successfully.")

    if args.action in ("schema", "all"):
        schema_json = engine.generate_schema()
        print("\n" + "="*60)
        print(" GENERATED SCHEMA.ORG JSON-LD GRAPH")
        print("="*60)
        print(f'<script type="application/ld+json">\n{json.dumps(schema_json, indent=2)}\n</script>')

    if args.action in ("meta", "all"):
        meta_tags = engine.generate_meta_tags()
        print("\n" + "="*60)
        print(" GENERATED META & OPENGRAPH DIRECTIVES")
        print("="*60)
        print(meta_tags)


if __name__ == "__main__":
    main()
