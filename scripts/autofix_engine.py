#!/usr/bin/env python3
"""
AST & Framework-Aware Autonomous SEO Auto-Fixer.
Part of the Claude-SEO 10X Engine (Nexus Web Studios / Souank Banik).

Capabilities:
  - Framework Awareness: Next.js App Router (metadata export/generateMetadata),
    Astro frontmatter blocks, React JSX/TSX Head components, and standard HTML5 DOM.
  - Generates: Valid Schema.org JSON-LD graphs, /llms.txt, OpenGraph, Canonical tags.
  - Safe Mutation Engine: Mandatory dry-run previews, automated git branch isolation
    (seo-autofix-<timestamp>), and automatic rollback backups.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


@dataclass
class MutationResult:
    target_path: str
    framework: str
    diff_preview: str
    applied: bool
    branch_name: Optional[str] = None
    backup_path: Optional[str] = None
    error: Optional[str] = None


class FrameworkDetector:
    @staticmethod
    def detect(file_path: str, content: str) -> str:
        p = file_path.lower()
        if p.endswith(".astro"):
            return "astro"
        if p.endswith((".tsx", ".jsx", ".ts", ".js")):
            if "metadata" in content or "layout." in p or "page." in p or "next" in content:
                return "nextjs"
            return "react"
        if p.endswith((".html", ".htm")) or content.lstrip().startswith("<!doctype html") or "<html" in content.lower():
            return "html"
        return "generic"


class AutoFixEngine:
    def __init__(self, target: str, title: str = "", description: str = "", canonical_url: str = ""):
        self.target = target.strip()
        self.is_remote = self.target.startswith(("http://", "https://"))
        self.raw_content = ""
        self.final_url = self.target if self.is_remote else canonical_url or "https://example.com"
        self.title = title
        self.description = description
        self.canonical_url = canonical_url or self.final_url
        self._load()

    def _load(self):
        if self.is_remote:
            if not HAS_LIBS:
                raise RuntimeError("requests and beautifulsoup4 required for remote URLs.")
            headers = {"User-Agent": "Claude-SEO-AutoFix/3.0 (Autonomous Bot)"}
            resp = requests.get(self.target, headers=headers, timeout=12)
            self.final_url = resp.url
            self.raw_content = resp.text
        else:
            with open(self.target, "r", encoding="utf-8", errors="ignore") as f:
                self.raw_content = f.read()

        # If title or desc not explicitly provided, extract from content
        if HAS_LIBS and ("<html" in self.raw_content.lower() or self.is_remote):
            soup = BeautifulSoup(self.raw_content, "html.parser")
            if not self.title and soup.title and soup.title.string:
                self.title = soup.title.string.strip()
            if not self.description:
                meta_desc = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
                if meta_desc and meta_desc.get("content"):
                    self.description = meta_desc["content"].strip()

        if not self.title:
            self.title = "High-Performance Optimized Page"
        if not self.description:
            self.description = "Production-grade, search-optimized page engineered for high conversion and AI citation."

    # ---------------------------------------------------------
    # Generator Routines
    # ---------------------------------------------------------
    def generate_llms_txt(self) -> str:
        """Generates /llms.txt compliant with the official llms.txt standard."""
        domain = urlparse(self.final_url).netloc or "example.com"
        lines = [
            f"# {self.title}",
            "",
            f"> {self.description}",
            "",
            "## Core Architecture & Resources",
            f"- [Primary Endpoint]({self.canonical_url}): Canonical service entrypoint.",
            f"- [API Documentation]({urljoin(self.final_url, '/docs')}): Complete machine-readable technical spec.",
            "",
            "## LLM Reasoning Context",
            f"- [Full Context]({urljoin(self.final_url, '/llms-full.txt')}): Unabridged documentation dump for generative models."
        ]
        return "\n".join(lines)

    def generate_schema(self, schema_type: str = "WebPage") -> Dict:
        """Generates Schema.org JSON-LD @graph structure."""
        domain = urlparse(self.final_url).netloc or "example.com"
        scheme = urlparse(self.final_url).scheme or "https"
        return {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "@id": f"{scheme}://{domain}/#organization",
                    "name": domain,
                    "url": f"{scheme}://{domain}"
                },
                {
                    "@type": schema_type,
                    "@id": f"{self.canonical_url}#{schema_type.lower()}",
                    "url": self.canonical_url,
                    "name": self.title,
                    "description": self.description,
                    "isPartOf": {"@id": f"{scheme}://{domain}/#organization"}
                }
            ]
        }

    # ---------------------------------------------------------
    # Framework Code Mutations
    # ---------------------------------------------------------
    def mutate_nextjs(self) -> Tuple[str, str]:
        """Injects or merges Next.js App Router metadata export."""
        content = self.raw_content
        metadata_block = f"""export const metadata: Metadata = {{
  title: "{self.title}",
  description: "{self.description}",
  alternates: {{
    canonical: "{self.canonical_url}",
  }},
  openGraph: {{
    title: "{self.title}",
    description: "{self.description}",
    url: "{self.canonical_url}",
    type: "website",
  }},
  twitter: {{
    card: "summary_large_image",
    title: "{self.title}",
    description: "{self.description}",
  }},
}};
"""
        import_next_meta = "import type { Metadata } from 'next';\n"

        if "export const metadata" in content:
            # Replace existing metadata block
            pattern = r"export\s+const\s+metadata\s*:\s*Metadata\s*=\s*\{[\s\S]*?\};"
            if re.search(pattern, content):
                mutated = re.sub(pattern, metadata_block.strip(), content)
            else:
                mutated = content + "\n\n" + metadata_block
        else:
            # Prepend import if missing, append metadata
            mutated = content
            if "import type { Metadata }" not in mutated and "from 'next'" not in mutated:
                mutated = import_next_meta + mutated
            # Place metadata before default export or at end
            if "export default" in mutated:
                idx = mutated.find("export default")
                mutated = mutated[:idx] + metadata_block + "\n" + mutated[idx:]
            else:
                mutated = mutated + "\n\n" + metadata_block

        diff = self._generate_diff(self.raw_content, mutated, self.target)
        return mutated, diff

    def mutate_astro(self) -> Tuple[str, str]:
        """Injects SEO frontmatter variables into Astro components."""
        content = self.raw_content
        seo_frontmatter = f"""const title = "{self.title}";
const description = "{self.description}";
const canonicalURL = new URL("{self.canonical_url}", Astro.site);
"""
        if content.startswith("---"):
            second_fence = content.find("---", 3)
            if second_fence != -1:
                mutated = content[:3] + "\n" + seo_frontmatter + content[3:]
            else:
                mutated = f"---\n{seo_frontmatter}---\n" + content
        else:
            mutated = f"---\n{seo_frontmatter}---\n" + content

        diff = self._generate_diff(self.raw_content, mutated, self.target)
        return mutated, diff

    def mutate_html(self) -> Tuple[str, str]:
        """Injects production tags into HTML5 DOM using BeautifulSoup."""
        if not HAS_LIBS:
            raise RuntimeError("BeautifulSoup required for HTML mutation.")
        soup = BeautifulSoup(self.raw_content, "html.parser")
        head = soup.find("head")
        if not head:
            head = soup.new_tag("head")
            if soup.html:
                soup.html.insert(0, head)
            else:
                soup.insert(0, head)

        # Update or create title
        title_tag = head.find("title")
        if not title_tag:
            title_tag = soup.new_tag("title")
            head.append(title_tag)
        title_tag.string = self.title

        # Canonical
        canon = head.find("link", rel=re.compile("canonical", re.I))
        if not canon:
            canon = soup.new_tag("link", rel="canonical", href=self.canonical_url)
            head.append(canon)
        else:
            canon["href"] = self.canonical_url

        # Meta description
        mdesc = head.find("meta", attrs={"name": re.compile("description", re.I)})
        if not mdesc:
            mdesc = soup.new_tag("meta", attrs={"name": "description", "content": self.description})
            head.append(mdesc)
        else:
            mdesc["content"] = self.description

        # OpenGraph
        og_tags = [
            ("og:title", self.title),
            ("og:description", self.description),
            ("og:url", self.canonical_url),
            ("og:type", "website")
        ]
        for prop, val in og_tags:
            existing = head.find("meta", attrs={"property": prop})
            if not existing:
                head.append(soup.new_tag("meta", attrs={"property": prop, "content": val}))
            else:
                existing["content"] = val

        # Schema JSON-LD
        schema_data = self.generate_schema()
        schema_tag = head.find("script", attrs={"type": "application/ld+json"})
        if not schema_tag:
            schema_tag = soup.new_tag("script", attrs={"type": "application/ld+json"})
            schema_tag.string = json.dumps(schema_data, indent=2)
            head.append(schema_tag)
        else:
            schema_tag.string = json.dumps(schema_data, indent=2)

        mutated = str(soup)
        diff = self._generate_diff(self.raw_content, mutated, self.target)
        return mutated, diff

    def _generate_diff(self, original: str, mutated: str, filename: str) -> str:
        orig_lines = original.splitlines(keepends=True)
        mut_lines = mutated.splitlines(keepends=True)
        import difflib
        diff = difflib.unified_diff(orig_lines, mut_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}")
        return "".join(diff)

    # ---------------------------------------------------------
    # Safe Git Isolation & Apply Engine
    # ---------------------------------------------------------
    def execute_safely(self, dry_run: bool = True, create_branch: bool = True) -> MutationResult:
        if self.is_remote:
            return MutationResult(
                target_path=self.target,
                framework="remote_url",
                diff_preview="[Notice: Target is a remote URL. Use fix commands to output files.]",
                applied=False,
                error="Cannot mutate remote URL on disk directly."
            )

        framework = FrameworkDetector.detect(self.target, self.raw_content)
        if framework == "nextjs":
            mutated_code, diff = self.mutate_nextjs()
        elif framework == "astro":
            mutated_code, diff = self.mutate_astro()
        elif framework == "html":
            mutated_code, diff = self.mutate_html()
        else:
            mutated_code, diff = self.mutate_html()

        if dry_run:
            return MutationResult(
                target_path=self.target,
                framework=framework,
                diff_preview=diff or "[No changes needed]",
                applied=False
            )

        # Apply with Git branch isolation
        branch_name = None
        backup_path = None
        try:
            # Check if in a git repository
            in_git = False
            try:
                res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
                in_git = res.returncode == 0
            except Exception:
                in_git = False

            if in_git and create_branch:
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                branch_name = f"seo-autofix-{timestamp}"
                subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True)

            # Create disk backup
            backup_path = f"{self.target}.bak.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            with open(backup_path, "w", encoding="utf-8") as bf:
                bf.write(self.raw_content)

            # Write mutated file
            with open(self.target, "w", encoding="utf-8") as f:
                f.write(mutated_code)

            return MutationResult(
                target_path=self.target,
                framework=framework,
                diff_preview=diff,
                applied=True,
                branch_name=branch_name,
                backup_path=backup_path
            )
        except Exception as exc:
            return MutationResult(
                target_path=self.target,
                framework=framework,
                diff_preview=diff,
                applied=False,
                error=str(exc)
            )


def main():
    parser = argparse.ArgumentParser(description="AST & Framework-Aware Autonomous SEO Auto-Fixer")
    parser.add_argument("target", help="Target source file (.tsx, .jsx, .astro, .html) or URL")
    parser.add_argument("--title", default="", help="Custom page title")
    parser.add_argument("--description", default="", help="Custom meta description")
    parser.add_argument("--canonical", default="", help="Canonical URL")
    parser.add_argument("--apply", action="store_true", help="Apply mutations to disk (default is dry-run)")
    parser.add_argument("--no-branch", action="store_true", help="Skip git branch creation when applying")
    parser.add_argument("--json", action="store_true", help="Output JSON result")
    args = parser.parse_args()

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
        return

    print("\n" + "="*70)
    print(f" CLAUDE-SEO 10X AUTO-FIXER: {res.target_path} [{res.framework.upper()}]")
    print("="*70)
    if res.applied:
        print(f"[STATUS] APPLIED MUTATION SUCCESSFULLY")
        if res.branch_name:
            print(f"[GIT SAFETY] Isolated on branch: {res.branch_name}")
        if res.backup_path:
            print(f"[BACKUP] Created rollback snapshot: {res.backup_path}")
    else:
        print(f"[STATUS] DRY-RUN PREVIEW (No files modified. Pass --apply to execute)")

    print("\n[ UNIFIED DIFF PREVIEW ]")
    print(res.diff_preview or "No modifications needed.")


if __name__ == "__main__":
    main()
