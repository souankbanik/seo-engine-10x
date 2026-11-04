"""
Tests for Zero-Auth Keyword & Semantic Intent Engine (scripts/keyword_intel.py).
"""

import os
import sys
from unittest.mock import patch

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from keyword_intel import KeywordIntelEngine


def test_classify_intent_rules():
    engine = KeywordIntelEngine("crm software")
    assert engine.classify_intent("best crm software for startups") == "Commercial"
    assert engine.classify_intent("buy crm software annual license") == "Transactional"
    assert engine.classify_intent("how to configure crm software pipelines") == "Informational"
    assert engine.classify_intent("salesforce crm software login portal") == "Navigational"


def test_estimate_difficulty_scoring():
    engine = KeywordIntelEngine("analytics")
    # Short commercial query -> Hard
    score_hard, level_hard = engine.estimate_difficulty("best analytics")
    assert score_hard >= 60
    assert level_hard == "Hard"

    # Long-tail informational query -> Easy/Medium
    score_easy, level_easy = engine.estimate_difficulty("how to setup google analytics 4 for react applications")
    assert score_easy < score_hard
    assert level_easy in ("Easy", "Medium")


@patch.object(KeywordIntelEngine, "_fetch_google_suggest")
@patch.object(KeywordIntelEngine, "_fetch_duckduckgo_suggest")
def test_harvest_and_clustering(mock_ddg, mock_google):
    mock_google.return_value = ["best ai tools", "ai tools for coding", "buy ai tools"]
    mock_ddg.return_value = ["how to use ai tools", "ai tools alternatives"]

    engine = KeywordIntelEngine("ai tools")
    data = engine.harvest()

    assert data["seed"] == "ai tools"
    assert data["total_harvested"] >= 4
    assert len(data["clusters"]) > 0
