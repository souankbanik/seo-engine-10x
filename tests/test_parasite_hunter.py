"""
Tests for Parasite SEO Hunter & Feasibility Engine (scripts/parasite_hunter.py).
"""

import os
import sys

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from parasite_hunter import PLATFORMS, ParasiteHunter


def test_platform_profiles_exist():
    required_platforms = ["reddit", "linkedin_pulse", "medium", "quora", "substack", "dev_to", "github_pages"]
    for p in required_platforms:
        assert p in PLATFORMS
        profile = PLATFORMS[p]
        assert profile.typical_dr >= 85
        assert profile.sra_risk in ("Low", "Low to Moderate", "Moderate")


def test_parasite_evaluation_scoring():
    # Review / comparison query should favor Reddit and LinkedIn
    hunter_review = ParasiteHunter("best vpn review 2026")
    data_review = hunter_review.evaluate()
    top_plat_review = data_review["recommended_platforms"][0]["platform"]
    assert top_plat_review in ("Reddit", "LinkedIn Pulse")

    # Developer query should favor Dev.to / Medium / GitHub
    hunter_dev = ParasiteHunter("python code optimizer api")
    data_dev = hunter_dev.evaluate()
    top_plat_dev = data_dev["recommended_platforms"][0]["platform"]
    assert top_plat_dev in ("Dev.to", "Medium", "GitHub Pages / Discussions")

    assert len(data_review["tactical_sop"]) == 5
