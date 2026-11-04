"""
Tests for Concurrent Site Graph & PageRank Crawler (scripts/site_graph_crawler.py).
"""

import os
import sys
from unittest.mock import patch

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from site_graph_crawler import PageNode, SiteGraphCrawler


def test_url_normalization():
    crawler = SiteGraphCrawler("https://example.com", max_pages=10)
    assert crawler.normalize_url("/about", "https://example.com") == "https://example.com/about"
    assert crawler.normalize_url("https://example.com/blog#section", "https://example.com") == "https://example.com/blog"
    # External URLs should be rejected
    assert crawler.normalize_url("https://google.com/test", "https://example.com") is None
    # Media assets should be excluded
    assert crawler.normalize_url("/image.png", "https://example.com") is None
    assert crawler.normalize_url("/doc.pdf", "https://example.com") is None


def test_compute_pagerank_deterministic():
    crawler = SiteGraphCrawler("https://example.com", max_pages=10)
    # Construct a triangular link graph: A -> B, B -> C, C -> A, and D pointing to A
    crawler.graph = {
        "https://example.com/a": PageNode(url="https://example.com/a", out_links=["https://example.com/b"]),
        "https://example.com/b": PageNode(url="https://example.com/b", out_links=["https://example.com/c"]),
        "https://example.com/c": PageNode(url="https://example.com/c", out_links=["https://example.com/a"]),
        "https://example.com/d": PageNode(url="https://example.com/d", out_links=["https://example.com/a"]),
    }
    crawler.compute_pagerank(damping=0.85)

    # Page A should have the highest PageRank because both C and D link to it
    assert crawler.graph["https://example.com/a"].pagerank == 100.0
    assert crawler.graph["https://example.com/d"].pagerank < crawler.graph["https://example.com/a"].pagerank


def test_crawler_summary_diagnostics():
    crawler = SiteGraphCrawler("https://example.com", max_pages=10)
    crawler.graph = {
        "https://example.com": PageNode(url="https://example.com", status_code=200, pagerank=100.0, in_links=[]),
        "https://example.com/orphan": PageNode(url="https://example.com/orphan", status_code=200, pagerank=10.0, in_links=[]),
        "https://example.com/broken": PageNode(url="https://example.com/broken", status_code=404, pagerank=5.0, in_links=["https://example.com"])
    }
    summary = crawler.summary()
    assert summary["total_crawled"] == 3
    assert summary["broken_count"] == 1
    assert summary["orphan_count"] == 1
    assert "https://example.com/orphan" in summary["orphans"]
    assert summary["broken_pages"][0]["status"] == 404
