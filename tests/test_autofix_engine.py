"""
Tests for AST & Framework-Aware Auto-Fixer (scripts/autofix_engine.py).
"""

import json
import os
import sys

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from autofix_engine import AutoFixEngine, FrameworkDetector


def test_framework_detector():
    assert FrameworkDetector.detect("page.tsx", "export default function Page() {}") == "nextjs"
    assert FrameworkDetector.detect("layout.jsx", "export const metadata = {}") == "nextjs"
    assert FrameworkDetector.detect("index.astro", "---\nconst x = 1;\n---") == "astro"
    assert FrameworkDetector.detect("index.html", "<!DOCTYPE html><html></html>") == "html"
    assert FrameworkDetector.detect("script.py", "print('hello')") == "generic"


def test_autofix_nextjs_dry_run(tmp_path):
    nextjs_file = tmp_path / "page.tsx"
    nextjs_file.write_text("""import React from 'react';

export default function Page() {
  return <h1>Dashboard</h1>;
}
""", encoding="utf-8")

    engine = AutoFixEngine(str(nextjs_file), title="SaaS Dashboard Pro", description="Enterprise real-time analytics.")
    result = engine.execute_safely(dry_run=True)

    assert result.framework == "nextjs"
    assert result.applied is False
    assert "export const metadata: Metadata" in result.diff_preview
    assert "SaaS Dashboard Pro" in result.diff_preview
    # Ensure original file untouched in dry-run
    assert "metadata" not in nextjs_file.read_text(encoding="utf-8")


def test_autofix_astro_dry_run(tmp_path):
    astro_file = tmp_path / "index.astro"
    astro_file.write_text("""---
const welcome = "Hello World";
---
<html>
  <body><h1>{welcome}</h1></body>
</html>
""", encoding="utf-8")

    engine = AutoFixEngine(str(astro_file), title="Astro Docs Hub", description="Fast static documentation.")
    result = engine.execute_safely(dry_run=True)

    assert result.framework == "astro"
    assert result.applied is False
    assert "Astro Docs Hub" in result.diff_preview
    assert "const canonicalURL" in result.diff_preview


def test_autofix_html_mutation(tmp_path):
    html_file = tmp_path / "index.html"
    html_file.write_text("<!DOCTYPE html><html><head></head><body><h1>Test</h1></body></html>", encoding="utf-8")

    engine = AutoFixEngine(str(html_file), title="HTML Production Title", description="Valid meta description.", canonical_url="https://example.com/test")
    mutated_code, diff = engine.mutate_html()

    assert "<title>HTML Production Title</title>" in mutated_code
    assert 'content="Valid meta description."' in mutated_code
    assert 'href="https://example.com/test"' in mutated_code
    assert "application/ld+json" in mutated_code
    assert len(diff) > 0


def test_generate_llms_txt():
    engine = AutoFixEngine("https://example.com", title="Nexus Web Platform", description="Autonomous SEO Engine")
    llms_text = engine.generate_llms_txt()
    assert "# Nexus Web Platform" in llms_text
    assert "> Autonomous SEO Engine" in llms_text
    assert "## Core Architecture & Resources" in llms_text
    assert "## LLM Reasoning Context" in llms_text


def test_generate_schema_json():
    engine = AutoFixEngine("https://example.com", title="Nexus Platform", description="High performance AI tools.")
    schema = engine.generate_schema("SoftwareApplication")
    assert schema["@context"] == "https://schema.org"
    assert len(schema["@graph"]) == 2
    types = [node["@type"] for node in schema["@graph"]]
    assert "Organization" in types
    assert "SoftwareApplication" in types
