"""
Tests for Claude-SEO 10X Master Orchestration Engine (seo_engine.py).
"""

import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for p in (SCRIPTS_DIR, ROOT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import seo_engine


def test_check_environment_structure():
    diag = seo_engine.check_environment()
    assert "python_version" in diag
    assert "git_available" in diag
    assert "packages" in diag
    assert "credentials" in diag
    assert "mode" in diag
    assert isinstance(diag["packages"], dict)
    assert isinstance(diag["credentials"], dict)


def test_build_parser_commands():
    import argparse
    parser = seo_engine.build_parser()
    subparsers_action = None
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparsers_action = action
            break
    assert subparsers_action is not None
    commands = list(subparsers_action.choices.keys())
    assert "doctor" in commands
    assert "audit" in commands
    assert "crawl" in commands
    assert "keywords" in commands
    assert "parasite" in commands
    assert "write" in commands
    assert "autofix" in commands
    assert "plan" in commands
    assert "index" in commands


def test_run_doctor_json(capsys):
    seo_engine.run_doctor(json_mode=True)
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "python_version" in data
    assert "all_core_installed" in data


@patch("requests.get")
@patch("requests.head")
def test_run_audit_success(mock_head, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.url = "https://example.com"
    mock_get.return_value.text = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>High Performance Cloud Infrastructure Solutions</title>
        <meta name="description" content="Deploy high-performance enterprise cloud infrastructure in seconds with automated scaling and zero downtime architecture." />
        <link rel="canonical" href="https://example.com" />
        <script type="application/ld+json">{"@context": "https://schema.org"}</script>
      </head>
      <body>
        <h1>Cloud Infrastructure</h1>
        <h2>Scalability</h2>
        <img src="banner.jpg" alt="Cloud Architecture Diagram" />
      </body>
    </html>
    """
    mock_head.return_value.status_code = 200

    logger = seo_engine.EngineLogger(json_mode=True)
    report = seo_engine.run_audit("https://example.com", logger=logger, json_out=False)

    assert report["url"] == "https://example.com"
    assert report["status_code"] == 200
    assert report["h1_count"] == 1
    assert report["schema_count"] == 1
    assert report["missing_alt_count"] == 0
    assert report["llms_txt_active"] is True
    assert report["score"] >= 80


@patch("requests.post")
def test_submit_indexnow(mock_post):
    mock_post.return_value.status_code = 200
    logger = MagicMock()
    seo_engine.submit_indexnow(["https://example.com/page1", "https://example.com/page2"], key="test_key", host="example.com", logger=logger)
    assert mock_post.called
    payload = mock_post.call_args[1]["json"]
    assert payload["host"] == "example.com"
    assert payload["key"] == "test_key"
    assert len(payload["urlList"]) == 2
    logger.success.assert_called()
