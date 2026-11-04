#!/usr/bin/env python3
"""
Automated Platform-Native Parasite Content Writer.
Part of the Claude-SEO 10/10 Parasite SEO Engine.

Generates complete, high-converting, native-formatted articles/posts
tailored specifically to the psychological and editorial norms of:
- Reddit (Conversational, skeptical, value-first, anti-shill formatting)
- LinkedIn Pulse (B2B executive breakdown, frameworks, bold bullets)
- Medium / Substack (Editorial narrative, data-driven teardown)
- Quora (High-authority problem-solver answer format)

Includes complete manual publishing guidelines for each platform.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict


def generate_reddit_post(keyword: str, offer_name: str, offer_url: str, angle: str) -> Dict[str, str]:
    title = f"Honestly tested every {keyword} so you don't have to — here's what actually worked (unfiltered comparison)"
    body = f"""I’ve spent the last 3 weeks testing and comparing pretty much every major tool/method for **{keyword}**. 

Most of the blog posts ranking on Google right now are completely sponsored affiliate garbage that copy-paste each other's feature lists without ever actually logging in. So I wanted to drop a completely unbiased breakdown of what actually held up under real conditions.

### The Problem Most People Hit
When searching for {keyword}, you usually run into two extremes:
1. Super bloated enterprise tools that cost an arm and a leg and take 3 weeks to onboard.
2. Cheap half-baked tools that break the moment you give them real work.

### What I Tested & My Notes:
* **Option A (The Big Legacy Player):** Name recognition is huge, but UI feels like 2014. Super clunky, slow customer support, and charges extra for basic features.
* **Option B (The Budget Alternative):** Looked promising on paper, but had serious reliability issues when scaling up. Fine if you're just dabbling, but not for serious setups.
* **{offer_name}:** This was honestly the surprise of the batch. Cleanest workflow, zero unnecessary bloat, and handled {keyword} without random hiccups. The learning curve was basically nonexistent compared to the legacy alternatives.

### The Real Pros & Cons of {offer_name}
**The Good:**
- Setup took under 5 minutes without needing complex setup guides.
- Speed and responsiveness were significantly faster than the competition.
- Transparent pricing without surprise tier gates.

**The Not-So-Good:**
- Mobile interface could use a little bit of polish.
- Documentation for advanced API edge-cases is still growing.

### Verdict
If you're looking for {keyword}, don't overcomplicate it with bloated legacy stacks. Take a look at [{offer_name}]({offer_url}) — it’s currently the best value-to-performance ratio out there right now.

Drop any questions below, happy to compare specific features if anyone is stuck on an edge case.
"""
    manual_guide = """
[REDDIT PUBLISHING CHECKLIST (WHAT YOU MUST DO)]:
1. Account Age & Karma: Post from an account with at least 30+ days age and 100+ comment karma (never a brand-new 0-karma burner).
2. Subreddit Match: Search for subreddits like r/software, r/tools, or your specific niche community (e.g. r/SaaS, r/marketing). Check sidebar rules!
3. Flair: Select 'Review', 'Discussion', or 'Guide' flair if available.
4. The Link: If the subreddit has strict automod rules banning links in OP, remove the direct link from the post and drop it as a polite reply when someone asks 'where can I find this?'.
5. Freshness Bump: Reply to the first 2-3 comments within 30 minutes to trigger Reddit's velocity algorithm.
"""
    return {"title": title, "content": body.strip(), "manual_checklist": manual_guide.strip()}


def generate_linkedin_post(keyword: str, offer_name: str, offer_url: str, angle: str) -> Dict[str, str]:
    title = f"The 2026 Executive Guide to {keyword.title()}: Benchmarks, Teardown & Strategic Takeaways"
    body = f"""# The 2026 Executive Guide to {keyword.title()}

In modern workflows, efficiency is determined by your stack. Yet when evaluating solutions for **{keyword}**, most decision-makers are bogged down by opaque pricing, technical debt, and fragmented legacy software.

Over the past quarter, we conducted an empirical evaluation of the leading architectures for {keyword}. Here is the executive summary.

---

### The Current Market Landscape

The market for {keyword} has shifted from feature quantity to **execution velocity**:

1. **Legacy Systems:** High switching costs, complex maintenance, and declining API agility.
2. **First-Generation SaaS:** Acceptable for baseline operations, but struggling with modern integration demands.
3. **Modern Purpose-Built Engines:** Streamlined data pipelines, instant deployment, and zero operational drag.

---

### Key Evaluation Criteria

When benchmarking {keyword}, assess these four non-negotiable vectors:
* **Time-to-Value (TTV):** Can teams deploy and see measurable output within 48 hours?
* **Integration Overhead:** Does it interface cleanly with existing infrastructure?
* **Cost Predictability:** Are unit economics linear, or are there hidden usage multipliers?
* **Data Security & Reliability:** Enterprise-grade reliability without downtime vulnerabilities.

---

### Strategic Benchmark: Why {offer_name} Stands Out

Among the tools evaluated, **{offer_name}** demonstrated the highest operational ROI for teams prioritizing speed and reliability in {keyword}.

**Core Strengths:**
* **Instant Deployment:** Zero redundant configuration steps.
* **Superior Architecture:** Purpose-built for modern technical requirements.
* **Cost Efficiency:** Delivers enterprise throughput at a fraction of legacy contract minimums.

For teams looking to modernize their approach to {keyword}, explore the full technical teardown at [{offer_name}]({offer_url}).

---

### Strategic Next Steps
Audit your current pipeline. Identify where legacy bottlenecks are costing developer hours, and replace manual overhead with automated precision.
"""
    manual_guide = """
[LINKEDIN PULSE PUBLISHING CHECKLIST (WHAT YOU MUST DO)]:
1. Publish Location: Go to your LinkedIn feed -> Click 'Write article' (this creates a LinkedIn Pulse longform article, NOT a short post).
2. Cover Image: Upload a 1200x644 high-resolution branded banner with the article title.
3. Tags/Hashtags: Add 3-5 relevant industry tags (e.g., #Tech #SaaS #Productivity).
4. Profile Authority: Ensure your personal profile has a professional headline and avatar—LinkedIn rankings favor established author entities.
5. Indexing Boost: Once published, share the article link as a regular feed post on LinkedIn with a 3-bullet summary to drive initial impressions.
"""
    return {"title": title, "content": body.strip(), "manual_checklist": manual_guide.strip()}


def generate_medium_post(keyword: str, offer_name: str, offer_url: str, angle: str) -> Dict[str, str]:
    title = f"I Analyzed the Best Solutions for {keyword.title()} in 2026: Here is the Breakdown"
    body = f"""# I Analyzed the Best Solutions for {keyword.title()} in 2026: Here is the Breakdown

Search engines are flooded with superficial listicles. If you search for **{keyword}**, 90% of the articles you find are written by people who never spent ten minutes actually testing the tools they recommend.

I decided to run a controlled test across the top platforms to see which solution actually delivers on its promises.

Here is what I discovered.

---

## 1. The Real Bottlenecks in {keyword.title()}

Most practitioners fail at {keyword} not because they lack effort, but because their tools work against them:
* **Feature Bloat:** 80% of features in legacy platforms are never used, but you still pay for them.
* **Latency & Friction:** Sluggish interfaces that add 15 minutes of friction to simple daily tasks.
* **Opaque Pricing Models:** Hidden charges that balloon the moment your volume increases.

---

## 2. The Contenders: A Transparent Comparison

### The Incumbent
Reliable, safe for corporate procurement, but painfully slow to evolve. If you enjoy endless email threads with enterprise sales reps just to get a demo, this is for you.

### The Open Source / DIY Route
Infinitely customizable, but requires hours of continuous maintenance, server patching, and debugging. If your time is worth zero dollars, go this route.

### The Modern Alternative: {offer_name}
**{offer_name}** solves the core friction point of {keyword} by focusing entirely on execution speed and simplicity.

Key highlights:
- **Instant onboarding:** Operates straight out of the box.
- **Modern UI:** Clean, distraction-free workflow.
- **Transparent economics:** You get exactly what you need without artificial paywalls.

You can inspect the platform and run your own tests here: [{offer_name}]({offer_url}).

---

## 3. Final Recommendation

If you need a battle-tested, high-efficiency setup for {keyword}, stop wasting time on bloated legacy suites. Take a look at [{offer_name}]({offer_url}) and streamline your workflow today.
"""
    manual_guide = """
[MEDIUM / SUBSTACK PUBLISHING CHECKLIST (WHAT YOU MUST DO)]:
1. Canonical Tag: If you cross-post this from your own blog, go to Story Settings -> Advanced -> Customize canonical URL and point to your site.
2. Publication Submission: Submit your story to a relevant Medium publication (e.g., Towards Data Science, Better Programming, Startups) for instant audience distribution.
3. Topic Tags: Add 5 targeted tags matching search intent.
4. Affiliate Disclosure: Medium TOS requires clear disclosure. Add a one-line disclaimer at the bottom: '(Disclosure: Some links in this article may be affiliate links).'
"""
    return {"title": title, "content": body.strip(), "manual_checklist": manual_guide.strip()}


def generate_quora_post(keyword: str, offer_name: str, offer_url: str, angle: str) -> Dict[str, str]:
    title = f"What is the most effective way or best tool for {keyword}?"
    body = f"""**What is the most effective way or best tool for {keyword}?**

Having worked extensively with different workflows for **{keyword}**, the biggest mistake I see people make is choosing a tool based on hype rather than real daily workflow efficiency.

Here is the straightforward breakdown of how to approach this:

### 1. Avoid Feature Overload
When you are evaluating options for {keyword}, ignore the massive marketing checklists. What actually matters is:
- How fast does it get you from point A to point B?
- Does it require extensive training or does it work immediately?
- Is customer support responsive when edge cases emerge?

### 2. My Direct Experience
I tested multiple options over several months. Most tools in this space fall short because they try to be everything to everyone and end up being clunky.

The one solution that consistently outperformed the rest for {keyword} was **{offer_name}**.

Why it works:
* Extremely lightweight and responsive.
* Eliminates repetitive manual configuration.
* Strongest price-to-performance ratio currently available.

If you want to review the exact specifications, check out [{offer_name}]({offer_url}).

### Summary Rule
Don't overpay for legacy brand names that haven't updated their UX in five years. Test [{offer_name}]({offer_url}) and judge the output for yourself.
"""
    manual_guide = """
[QUORA PUBLISHING CHECKLIST (WHAT YOU MUST DO)]:
1. Find an Existing High-Ranking Question: Never ask and answer your own question. Search Google: 'site:quora.com [keyword]' and find the question that already ranks on Google Page 1 or 2!
2. Answer Thoroughly: Quora's algorithm downranks short, spammy answers. Always provide 300+ words of real helpful context before mentioning any product.
3. Link Formatting: Place the link naturally near the middle or end of your answer.
"""
    return {"title": title, "content": body.strip(), "manual_checklist": manual_guide.strip()}


class ParasiteContentWriter:
    def __init__(self, keyword: str, offer_name: str, offer_url: str, platform: str = "reddit", angle: str = "review"):
        self.keyword = keyword.strip()
        self.offer_name = offer_name.strip()
        self.offer_url = offer_url.strip()
        self.platform = platform.lower().strip()
        self.angle = angle.strip()

    def generate(self) -> Dict[str, str]:
        if self.platform in ("reddit", "r"):
            return generate_reddit_post(self.keyword, self.offer_name, self.offer_url, self.angle)
        elif self.platform in ("linkedin", "linkedin_pulse", "pulse"):
            return generate_linkedin_post(self.keyword, self.offer_name, self.offer_url, self.angle)
        elif self.platform in ("medium", "substack"):
            return generate_medium_post(self.keyword, self.offer_name, self.offer_url, self.angle)
        elif self.platform in ("quora", "q"):
            return generate_quora_post(self.keyword, self.offer_name, self.offer_url, self.angle)
        else:
            return generate_reddit_post(self.keyword, self.offer_name, self.offer_url, self.angle)


def main():
    parser = argparse.ArgumentParser(description="Automated Native Parasite Content Writer")
    parser.add_argument("keyword", help="Target keyword (e.g. 'best ai coding assistant')")
    parser.add_argument("--offer-name", required=True, help="Name of product/offer to recommend")
    parser.add_argument("--offer-url", required=True, help="Affiliate or target destination URL")
    parser.add_argument("--platform", choices=["reddit", "linkedin", "medium", "quora", "substack"], default="reddit")
    parser.add_argument("--save", action="store_true", help="Save output to markdown file")
    args = parser.parse_args()

    writer = ParasiteContentWriter(args.keyword, args.offer_name, args.offer_url, args.platform)
    res = writer.generate()

    print("\n" + "="*70)
    print(f" NATIVE PARASITE CONTENT: [{args.platform.upper()}] FOR '{args.keyword.upper()}'")
    print("="*70)
    print(f"\n[SUGGESTED TITLE]\n{res['title']}\n")
    print("[POST BODY]")
    print(res["content"])
    print("\n" + "-"*70)
    print(res["manual_checklist"])
    print("-"*70)

    if args.save:
        filename = f"parasite_{args.platform}_{args.keyword.replace(' ', '_')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {res['title']}\n\n{res['content']}\n\n---\n\n{res['manual_checklist']}\n")
        print(f"\n[+] Saved to {filename}")


if __name__ == "__main__":
    main()
