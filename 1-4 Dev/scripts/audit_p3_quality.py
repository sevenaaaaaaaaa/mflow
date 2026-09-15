#!/usr/bin/env python3
"""P3 blog quality audit — checks 55 expanded blogs against Anti-Slop + structure + brand rules.

Usage:
  python3 audit-p3-quality.py                    # audit all 55
  python3 audit-p3-quality.py --slug foo         # audit single slug
  python3 audit-p3-quality.py --report out.json  # machine-readable output
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Sanity infra
# ---------------------------------------------------------------------------

PROJECT_ID = "o11tm2qe"
DATASET = "production"
API_VERSION = "2024-01-01"
QUERY_URL = f"https://{PROJECT_ID}.api.sanity.io/v{API_VERSION}/data/query/{DATASET}"
BASE_URL = "https://www.lovart.ai"


def load_token() -> str:
    for p in (Path("/tmp/sanitytoken.txt"), Path("/tmp/sanity_token.txt")):
        if p.exists() and p.read_text().strip():
            return p.read_text().strip()
    raise SystemExit("Missing Sanity token")


def sanity_query(q: str, token: str) -> Any:
    r = requests.get(QUERY_URL, headers={"Authorization": f"Bearer {token}"},
                     params={"query": q}, timeout=30)
    r.raise_for_status()
    return r.json()["result"]


def fetch_blog(slug: str, token: str) -> dict[str, Any]:
    q = f'*[_type=="blog" && slug.current=="{slug}" && language=="en"][0]{{_id,title,seo,category,"slug":slug.current,body}}'
    return sanity_query(q, token) or {}


# ---------------------------------------------------------------------------
# Portable Text helpers
# ---------------------------------------------------------------------------

def pt_to_text(blocks: list[dict]) -> str:
    """Convert Portable Text to plain text for analysis."""
    lines = []
    for b in blocks:
        if b.get("_type") != "block":
            continue
        text = "".join(c.get("text", "") for c in b.get("children", []))
        style = b.get("style", "normal")
        if style in ("h1", "h2", "h3", "h4"):
            lines.append(f"[{style.upper()}] {text}")
        elif b.get("listItem"):
            lines.append(f"  - {text}")
        else:
            lines.append(text)
    return "\n".join(lines)


def pt_to_plain(blocks: list[dict]) -> str:
    """Extract plain text only (no style markers)."""
    parts = []
    for b in blocks:
        if b.get("_type") == "block":
            parts.append(" ".join(c.get("text", "") for c in b.get("children", [])))
    return " ".join(parts)


def count_internal_links(blocks: list[dict]) -> int:
    """Count internal /blog/ links in Portable Text blocks."""
    count = 0
    for b in blocks:
        if b.get("_type") != "block":
            continue
        for md in b.get("markDefs", []):
            if md.get("_type") == "link" and md.get("href", "").startswith("/blog/"):
                count += 1
    return count


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def get_h2_texts(blocks: list[dict]) -> list[str]:
    out = []
    for b in blocks:
        if b.get("_type") == "block" and b.get("style") == "h2":
            out.append("".join(c.get("text", "") for c in b.get("children", [])))
    return out


def get_h3_texts(blocks: list[dict]) -> list[str]:
    out = []
    for b in blocks:
        if b.get("_type") == "block" and b.get("style") == "h3":
            out.append("".join(c.get("text", "") for c in b.get("children", [])))
    return out


# ---------------------------------------------------------------------------
# Anti-Slop checks (from anti-slop-rules.js + RULES-30)
# ---------------------------------------------------------------------------

BANNED_EN = [
    (r"\bunlock(?:ing|ed)?\b", "unlock"),
    (r"\brevolutionize\b", "revolutionize"),
    (r"\bgame[- ]?changer\b", "game-changer"),
    (r"\bleverage[ds]?\b", "leverage"),
    (r"\bstreamline[ds]?\b", "streamline"),
    (r"\bempower[eds]?\b", "empower"),
    (r"\bseamless(?:ly)?\b", "seamless(ly)"),
    (r"\bdelve[ds]?\b", "delve"),
    (r"\btestament\b", "testament"),
    (r"\bunprecedented\b", "unprecedented"),
    (r"\bthe future of\b", "the future of"),
    (r"\bpave the way\b", "pave the way"),
    (r"\bin today'?s fast[- ]paced\b", "in today's fast-paced"),
    (r"\bcutting[- ]edge\b", "cutting-edge"),
    (r"\bAI[- ]powered platform\b", "AI-powered platform"),
    (r"\btransform(?:s|ing|ed)? your (?:workflow|business)\b", "transform your workflow/business"),
    (r"\bfoster(?:ing|ed)?\b", "foster"),
    (r"\btapestry\b", "tapestry"),
    (r"\bbeacon\b", "beacon"),
    (r"\brealm\b", "realm"),
    (r"\bjourney\b", "journey"),
    (r"\bstands as\b", "stands as"),
    (r"\bunderscores?\b", "underscores"),
    (r"\bvibrant\b", "vibrant"),
]

AI_TELLS = [
    (r"\bas an AI\b", "as an AI"),
    (r"\bI cannot\b", "I cannot"),
    (r"\bin this article\b", "in this article"),
    (r"\bI don'?t have personal\b", "I don't have personal"),
    (r"\bas a language model\b", "as a language model"),
]

PLACEHOLDER_PATTERNS = [
    (r"IMAGE PLACEHOLDER", "IMAGE PLACEHOLDER"),
    (r"\[TODO\]", "[TODO]"),
    (r"\[TBD\]", "[TBD]"),
    (r"\[待补充\]", "[待补充]"),
    (r"lorem ipsum", "lorem ipsum"),
    (r"xxx{3,}", "xxx"),
    (r"\(section_\w+\)", "(section_xx) marker"),
]

BAD_LINK_PATTERNS = [
    (r"\(/博客文章/", "/博客文章/ link"),
    (r"\(/cluster/", "/cluster/ link"),
    (r"\.md\)", ".md) link"),
    (r"\]\(#\)", "](#) anchor"),
    (r"\]\(/\)", "](/) link"),
]

GENERIC_H2 = [
    "benefits", "features", "conclusion", "summary", "introduction",
    "overview", "what is", "why use", "how it works", "getting started",
    "final thoughts", "wrap up", "in conclusion",
]


# ---------------------------------------------------------------------------
# Quality check runner
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, level: str, code: str, msg: str, ctx: str = ""):
        self.level = level  # BLOCK / WARN / INFO
        self.code = code
        self.msg = msg
        self.ctx = ctx

    def to_dict(self):
        return {"level": self.level, "code": self.code, "msg": self.msg, "ctx": self.ctx}


def audit_blog(doc: dict) -> list[Issue]:
    issues: list[Issue] = []
    body = doc.get("body") or []
    title = doc.get("title", "")
    slug = doc.get("slug", "")
    seo = doc.get("seo") or {}
    category = doc.get("category", "")

    plain = pt_to_plain(body)
    full_text = pt_to_text(body)
    words = count_words(plain)
    h2s = get_h2_texts(body)
    h3s = get_h3_texts(body)

    # --- STRUCT ---
    if words < 7500:
        issues.append(Issue("BLOCK", "STRUCT_WORDCOUNT", f"Word count {words} < 7500", f"slug={slug}"))

    if len(h2s) < 3:
        issues.append(Issue("WARN", "STRUCT_H2_COUNT", f"Only {len(h2s)} H2s (want ≥3)", f"slug={slug}"))

    # Check for Real Project / Week-in-the-life / When NOT to use
    h2_lower = [h.lower() for h in h2s]
    has_real = any("real project" in h for h in h2_lower)
    has_week = any("week-in-the-life" in h or "week in the life" in h for h in h2_lower)
    has_not = any("when this approach does not" in h or "when lovart is not" in h or "when not" in h for h in h2_lower)
    if not has_real:
        issues.append(Issue("WARN", "STRUCT_NO_REAL_PROJECT", "Missing 'Real Project' H2", f"slug={slug}"))
    if not has_week:
        issues.append(Issue("WARN", "STRUCT_NO_WEEK", "Missing 'Week-in-the-Life' H2", f"slug={slug}"))
    if not has_not:
        issues.append(Issue("WARN", "STRUCT_NO_NOT_FOR", "Missing 'When NOT to use' H2", f"slug={slug}"))

    # Generic H2 check
    for h in h2s:
        h_strip = h.strip().lower().rstrip(":")
        if h_strip in GENERIC_H2:
            issues.append(Issue("WARN", "STRUCT_GENERIC_H2", f"Generic H2: '{h}'", f"slug={slug}"))

    # FAQ check — look for "faq", "frequently asked", or "Q&A" in H2 text
    has_faq = any("faq" in h.lower() or "frequently asked" in h.lower() or "q&a" in h.lower() for h in h2s)
    if not has_faq:
        issues.append(Issue("WARN", "STRUCT_NO_FAQ", "No FAQ section found", f"slug={slug}"))

    # --- ANTI-SLOP ---
    for pattern, name in BANNED_EN:
        matches = re.findall(pattern, plain, re.IGNORECASE)
        if matches:
            issues.append(Issue("BLOCK", "SLOP_BANNED", f"Banned word '{name}' found {len(matches)}x", f"slug={slug}"))

    for pattern, name in AI_TELLS:
        matches = re.findall(pattern, plain, re.IGNORECASE)
        if matches:
            issues.append(Issue("BLOCK", "SLOP_AI_TELL", f"AI tell '{name}' found", f"slug={slug}"))

    for pattern, name in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            issues.append(Issue("BLOCK", "SLOP_PLACEHOLDER", f"Placeholder '{name}' found", f"slug={slug}"))

    # --- LINKS ---
    for pattern, name in BAD_LINK_PATTERNS:
        matches = re.findall(pattern, full_text)
        if matches:
            issues.append(Issue("BLOCK", "LINK_BAD", f"Bad link pattern '{name}' found", f"slug={slug}"))

    # Check for internal links (/blog/slug) — count from Portable Text markDefs
    internal_links = count_internal_links(body)
    if internal_links < 2:
        issues.append(Issue("WARN", "LINK_FEW_INTERNAL", f"Only {internal_links} internal /blog/ links", f"slug={slug}"))

    # --- CTA ---
    cta_patterns = [
        r"try\s+lovart\s+free",
        r"get\s+started",
        r"sign\s+up",
        r"start\s+free",
        r"start\s+with\s+lovart",
        r"lovart\.ai/signup",
        r"lovart\.ai/pricing",
    ]
    has_cta = any(re.search(p, plain, re.IGNORECASE) for p in cta_patterns)
    if not has_cta:
        issues.append(Issue("WARN", "UX_NO_CTA", "No CTA found (try lovart free / sign up)", f"slug={slug}"))

    # --- BRAND ---
    # Check Lovart spelling
    bad_brand = re.findall(r"\blovart\b", plain, re.IGNORECASE)
    correct_brand = re.findall(r"\bLovart\b", plain)
    # Also check for common misspellings
    misspellings = re.findall(r"\b(?:lovart|lovert|lavart|lavort|loveart)\b", plain, re.IGNORECASE)
    misspellings_correct = [m for m in misspellings if m != "Lovart"]
    if misspellings_correct:
        issues.append(Issue("BLOCK", "BRAND_MISSPELL", f"Brand misspelling: {misspellings_correct[:3]}", f"slug={slug}"))

    # Check product terms
    product_terms = ["MCoT", "ChatCanvas", "Touch Edit", "Brand Kit", "Identity Lock"]
    mentioned = sum(1 for t in product_terms if t in plain)
    if mentioned < 1:
        issues.append(Issue("WARN", "BRAND_NO_PRODUCT", "No product terms mentioned (MCoT/ChatCanvas/Touch Edit/Brand Kit)", f"slug={slug}"))

    # --- H2 DENSITY ---
    h2_count = len(h2s)
    h2_density = h2_count / max(words / 500, 1)
    if h2_density < 0.5:
        issues.append(Issue("WARN", "SEO_H2_DENSITY", f"H2 density {h2_density:.1f} (want ≥0.5 per 500 words)", f"slug={slug}"))

    # --- SEO ---
    if seo:
        seo_title = seo.get("title", "")
        if len(seo_title) > 70:
            issues.append(Issue("WARN", "SEO_TITLE_LONG", f"SEO title {len(seo_title)} chars > 70", f"slug={slug}"))
        seo_desc = seo.get("description", "")
        if len(seo_desc) > 170:
            issues.append(Issue("WARN", "SEO_DESC_LONG", f"SEO description {len(seo_desc)} chars > 170", f"slug={slug}"))
        if not seo.get("keywords"):
            issues.append(Issue("WARN", "SEO_NO_KEYWORDS", "No SEO keywords set", f"slug={slug}"))

    # --- SHRINKAGE (last 30% thinner than first 30%) ---
    blocks_with_text = [b for b in body if b.get("_type") == "block" and pt_to_plain([b]).strip()]
    if len(blocks_with_text) > 6:
        first_30 = blocks_with_text[:len(blocks_with_text)//3]
        last_30 = blocks_with_text[-len(blocks_with_text)//3:]
        first_words = count_words(pt_to_plain(first_30))
        last_words = count_words(pt_to_plain(last_30))
        if last_words < first_words * 0.5:
            issues.append(Issue("WARN", "SLOP_SHRINKAGE", f"Last 30% ({last_words}w) much thinner than first 30% ({first_words}w)", f"slug={slug}"))

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_audit(slugs: list[str], token: str) -> dict[str, Any]:
    results = {}
    all_issues = []
    summary = {"total": len(slugs), "pass": 0, "warn_only": 0, "block": 0, "errors": 0}

    for i, slug in enumerate(slugs):
        try:
            doc = fetch_blog(slug, token)
            if not doc:
                results[slug] = {"status": "not_found", "issues": []}
                summary["errors"] += 1
                continue

            issues = audit_blog(doc)
            blocks = [i for i in issues if i.level == "BLOCK"]
            warns = [i for i in issues if i.level == "WARN"]

            if blocks:
                status = "BLOCK"
                summary["block"] += 1
            elif warns:
                status = "WARN"
                summary["warn_only"] += 1
            else:
                status = "PASS"
                summary["pass"] += 1

            body = doc.get("body") or []
            words = count_words(pt_to_plain(body))
            h2s = get_h2_texts(body)

            results[slug] = {
                "status": status,
                "words": words,
                "h2_count": len(h2s),
                "issues": [i.to_dict() for i in issues],
            }
            all_issues.extend(issues)

        except Exception as e:
            results[slug] = {"status": "error", "error": str(e), "issues": []}
            summary["errors"] += 1

        if (i + 1) % 10 == 0:
            print(f"  Audited {i+1}/{len(slugs)}...")

    return {"summary": summary, "results": results, "all_issues": [i.to_dict() for i in all_issues]}


def main() -> int:
    parser = argparse.ArgumentParser(description="P3 blog quality audit")
    parser.add_argument("--slug", type=str, help="Audit a single slug")
    parser.add_argument("--report", type=str, help="Write machine-readable JSON report")
    args = parser.parse_args()

    token = load_token()

    if args.slug:
        slugs = [args.slug]
    else:
        slugs = json.loads(Path("/tmp/p3_55_slugs.json").read_text())

    print(f"Auditing {len(slugs)} blogs...")
    report = run_audit(slugs, token)

    # Print summary
    s = report["summary"]
    print(f"\n=== AUDIT SUMMARY ===")
    print(f"Total:  {s['total']}")
    print(f"PASS:   {s['pass']}")
    print(f"WARN:   {s['warn_only']}")
    print(f"BLOCK:  {s['block']}")
    print(f"ERROR:  {s['errors']}")

    # Print BLOCKs
    blocks = [i for i in report["all_issues"] if i["level"] == "BLOCK"]
    if blocks:
        print(f"\n=== BLOCKs ({len(blocks)}) ===")
        by_code = {}
        for i in blocks:
            by_code.setdefault(i["code"], []).append(i)
        for code, items in sorted(by_code.items()):
            print(f"\n{code} ({len(items)}):")
            for item in items[:5]:
                print(f"  {item['msg']}")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")

    # Print WARNs (top issues)
    warns = [i for i in report["all_issues"] if i["level"] == "WARN"]
    if warns:
        print(f"\n=== WARNs ({len(warns)}) — top issues ===")
        by_code = {}
        for i in warns:
            by_code.setdefault(i["code"], []).append(i)
        for code, items in sorted(by_code.items(), key=lambda x: -len(x[1]))[:10]:
            print(f"  {code}: {len(items)}")

    # Write report
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"\nReport written: {out}")

    return 1 if s["block"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
