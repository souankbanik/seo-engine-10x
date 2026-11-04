"""
Tests for Autonomous Parasite Content Writer (scripts/parasite_post_writer.py).
"""

import os
import sys

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from parasite_post_writer import (
    ParasiteContentWriter,
    generate_linkedin_post,
    generate_medium_post,
    generate_quora_post,
    generate_reddit_post,
)


def test_reddit_post_generation():
    res = generate_reddit_post("best ai code assistant", "Antigravity", "https://antigravity.google", "review")
    assert "tested every" in res["title"].lower()
    assert "Antigravity" in res["content"]
    assert "The Real Pros & Cons of Antigravity" in res["content"]
    assert "Karma" in res["manual_checklist"]
    assert "Subreddit Match" in res["manual_checklist"]


def test_linkedin_post_generation():
    res = generate_linkedin_post("enterprise crm software", "Nexus CRM", "https://example.com/crm", "teardown")
    assert "Executive Guide" in res["title"]
    assert "Time-to-Value (TTV)" in res["content"]
    assert "Strategic Benchmark" in res["content"]
    assert "LinkedIn Pulse" in res["manual_checklist"]


def test_medium_and_quora_generation():
    writer_med = ParasiteContentWriter("data pipelines", "NexusFlow", "https://example.com/flow", platform="medium")
    res_med = writer_med.generate()
    assert "NexusFlow" in res_med["content"]
    assert "Medium" in res_med["manual_checklist"]

    writer_q = ParasiteContentWriter("best crm", "Nexus CRM", "https://example.com/crm", platform="quora")
    res_q = writer_q.generate()
    assert "Quora" in res_q["manual_checklist"]
    assert "What is the most effective way" in res_q["title"]
