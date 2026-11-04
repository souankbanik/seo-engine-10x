#!/usr/bin/env python3
"""
Parasite SEO Hunter & Platform Feasibility Engine.
Part of the 10/10 Claude-SEO Engine upgrade.

Evaluates high-authority host platforms (Reddit, LinkedIn Pulse, Medium,
Quora, Substack, Dev.to, GitHub Pages), calculates Parasite Opportunity Index (POI),
assesses Google Site Reputation Abuse (SRA) policy exposure, and generates
tactical execution playbooks for target keywords.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class PlatformProfile:
    name: str
    root_domain: str
    typical_dr: int
    indexing_speed: str
    link_type: str
    sra_risk: str  # Low, Moderate, High
    best_intent: List[str]
    moderation_strictness: str
    tactical_notes: str


PLATFORMS: Dict[str, PlatformProfile] = {
    "reddit": PlatformProfile(
        name="Reddit",
        root_domain="reddit.com",
        typical_dr=94,
        indexing_speed="Minutes (< 30 min)",
        link_type="nofollow / ugc",
        sra_risk="Low",
        best_intent=["Commercial Investigation", "Reviews", "Comparisons", "User Experiences"],
        moderation_strictness="Very High (Requires aged accounts + karma)",
        tactical_notes="Google prioritizes Reddit threads in SERPs under 'Discussions and Forums'. Focus on conversational, non-salesy value with indirect brand mentions."
    ),
    "linkedin_pulse": PlatformProfile(
        name="LinkedIn Pulse",
        root_domain="linkedin.com/pulse",
        typical_dr=98,
        indexing_speed="Hours (1-4 hrs)",
        link_type="nofollow",
        sra_risk="Low to Moderate",
        best_intent=["B2B SaaS", "Agency Services", "Career", "Enterprise Software"],
        moderation_strictness="Low",
        tactical_notes="Excellent for B2B keywords and enterprise tool comparisons. High authority bypasses sandbox effortlessly."
    ),
    "medium": PlatformProfile(
        name="Medium",
        root_domain="medium.com",
        typical_dr=93,
        indexing_speed="Fast (2-6 hrs)",
        link_type="nofollow",
        sra_risk="Moderate",
        best_intent=["Tech Tutorials", "Programming", "Crypto/Web3", "Productivity"],
        moderation_strictness="Moderate (Automated spam filters flag affiliate links)",
        tactical_notes="Rankings hold well for developer and tech queries. Keep affiliate links masked or push to a bridge page."
    ),
    "quora": PlatformProfile(
        name="Quora",
        root_domain="quora.com",
        typical_dr=92,
        indexing_speed="Hours (2-12 hrs)",
        link_type="nofollow",
        sra_risk="Low",
        best_intent=["Problem-solving", "Medical/Legal/General Advice", "How-to"],
        moderation_strictness="High (Aggressive link deletion)",
        tactical_notes="Great for long-tail question queries. Answer established questions that already rank in top 20 of Google."
    ),
    "substack": PlatformProfile(
        name="Substack",
        root_domain="substack.com",
        typical_dr=91,
        indexing_speed="Same-day (4-12 hrs)",
        link_type="dofollow / mixed",
        sra_risk="Low",
        best_intent=["Long-form Analysis", "Finance/Investing", "Deep Dives", "Editorial"],
        moderation_strictness="Low",
        tactical_notes="Substack newsletters have high topical authority and clean domain reputation. Can capture newsletter subscribers while ranking."
    ),
    "dev_to": PlatformProfile(
        name="Dev.to",
        root_domain="dev.to",
        typical_dr=88,
        indexing_speed="Fast (< 2 hrs)",
        link_type="nofollow (supports canonical)",
        sra_risk="Low",
        best_intent=["Software Tools", "Open Source", "Developer APIs", "Libraries"],
        moderation_strictness="Moderate",
        tactical_notes="High SERP affinity for programming, API reviews, and tech stacks. Allows setting custom canonical URLs."
    ),
    "github_pages": PlatformProfile(
        name="GitHub Pages / Discussions",
        root_domain="github.com",
        typical_dr=96,
        indexing_speed="Minutes to Hours",
        link_type="dofollow (in repos/readmes)",
        sra_risk="Low",
        best_intent=["Developer Tools", "Cheatsheets", "Awesome-lists", "Documentation"],
        moderation_strictness="High (TOS strictly bans commercial spam)",
        tactical_notes="Awesome-lists and documentation pages rank top-3 for dev queries. Must provide genuine utility."
    )
}


class ParasiteHunter:
    def __init__(self, keyword: str):
        self.keyword = keyword.strip()

    def evaluate(self) -> Dict:
        scored = []
        kw_lower = self.keyword.lower()

        for key, p in PLATFORMS.items():
            score = 70  # Base score
            reasons = []

            # Match keyword intent to platform strengths
            if any(term in kw_lower for term in ["best", "review", "vs", "alternative"]):
                if key in ["reddit", "linkedin_pulse"]:
                    score += 15
                    reasons.append("High alignment with comparison/review SERP features")
            elif any(term in kw_lower for term in ["how to", "guide", "code", "python", "tool", "api"]):
                if key in ["dev_to", "medium", "github_pages"]:
                    score += 15
                    reasons.append("High alignment with technical/developer intent")
            elif any(term in kw_lower for term in ["b2b", "crm", "enterprise", "marketing", "business"]):
                if key in ["linkedin_pulse", "substack"]:
                    score += 15
                    reasons.append("High B2B professional audience relevance")

            if p.sra_risk == "Low":
                score += 10
                reasons.append("Minimal risk under Google Site Reputation Abuse policy")
            elif p.sra_risk == "Moderate":
                score += 5

            score = min(98, score)

            scored.append({
                "platform": p.name,
                "domain": p.root_domain,
                "domain_rating": p.typical_dr,
                "opportunity_score": score,
                "indexing_speed": p.indexing_speed,
                "sra_risk": p.sra_risk,
                "moderation": p.moderation_strictness,
                "notes": p.tactical_notes,
                "advantages": reasons
            })

        scored.sort(key=lambda x: x["opportunity_score"], reverse=True)

        return {
            "target_keyword": self.keyword,
            "recommended_platforms": scored,
            "tactical_sop": [
                "1. Choose top 2 recommended platforms based on niche match.",
                "2. Match native formatting (Reddit: raw & skeptical, LinkedIn: structured framework, Dev.to: markdown code).",
                "3. Optimize H1 and first 100 words with exact/secondary keyword variants.",
                "4. Route traffic to a clean lead capture or direct affiliate link (avoid spammy anchor blasts to money site).",
                "5. Seed initial engagement (comments, upvotes, reactions) within first 3 hours to trigger crawler freshness."
            ]
        }


def main():
    parser = argparse.ArgumentParser(description="Parasite SEO Hunter & Platform Feasibility Engine")
    parser.add_argument("keyword", help="Target keyword to hunt parasite opportunities for")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    hunter = ParasiteHunter(args.keyword)
    data = hunter.evaluate()

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print("\n" + "="*75)
    print(f" PARASITE SEO OPPORTUNITY MATRIX: '{args.keyword.upper()}'")
    print("="*75)

    print("\n[ TOP RECOMMENDED HOST PLATFORMS ]\n")
    for item in data["recommended_platforms"][:4]:
        print(f"Platform: {item['platform']} (DR {item['domain_rating']}) | Score: {item['opportunity_score']}/100")
        print(f" - Indexing Speed : {item['indexing_speed']}")
        print(f" - SRA Risk Level : {item['sra_risk']}")
        print(f" - Moderation     : {item['moderation']}")
        print(f" - Tactical Edge  : {item['notes']}")
        print()

    print("[ 5-STEP EXECUTION SOP ]")
    for step in data["tactical_sop"]:
        print(f" {step}")


if __name__ == "__main__":
    main()
