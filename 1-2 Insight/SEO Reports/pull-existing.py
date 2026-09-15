#!/usr/bin/env python3
"""
Pull existing blog posts from Sanity CMS for refactoring.
Uses GROQ query to fetch blog content.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

# Configuration
SANITY_CONFIG = os.path.expanduser("~/.config/sanity/config.json")
PROJECT_ID = "o11tm2qe"
DATASET = "production"
API_VERSION = "v2024-01-01"
OUTPUT_DIR = Path(__file__).parent.parent / "01-existing"

def get_auth_token():
    """Get Sanity auth token from config file."""
    with open(SANITY_CONFIG) as f:
        return json.load(f)["authToken"]

def sanity_query(groq, token):
    """Execute GROQ query against Sanity."""
    url = f"https://{PROJECT_ID}.api.sanity.io/{API_VERSION}/data/query/{DATASET}"
    params = urllib.parse.urlencode({"query": groq})
    req = urllib.request.Request(
        f"{url}?{params}",
        headers={"Authorization": f"Bearer {token}"}
    )
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read().decode())["result"]

def extract_slug(obj):
    """Extract slug from Sanity object."""
    if isinstance(obj, dict):
        return obj.get("current", "")
    return str(obj or "")

def pull_blog_post(slug, token):
    """Pull a single blog post by slug."""
    groq = f'''
    *[_type == "blog" && slug.current == "{slug}" && !(_id in path("drafts.**"))][0]{{
        _id,
        title,
        "slug": slug.current,
        body,
        language,
        "cover": cover,
        description,
        seo,
        category,
        author,
        releaseDate,
        publishedAt,
        _updatedAt
    }}
    '''
    return sanity_query(groq, token)

def main():
    """Main entry point."""
    # Parse arguments
    batch_start = 0
    batch_size = 3
    
    if len(sys.argv) > 1:
        try:
            batch_start = int(sys.argv[1])
        except ValueError:
            # It's a file path
            slugs_file = sys.argv[1]
            with open(slugs_file) as f:
                slugs = [line.strip() for line in f if line.strip()]
    
    if len(sys.argv) > 2:
        batch_size = int(sys.argv[2])
    
    # Use TOP50 slugs if no file provided
    if 'slugs' not in locals():
        # TOP50 slugs by GSC impressions
        slugs = [
            "lovart-worlds-first-professional-ai-design-agent",
            "dreamina-ai-review",
            "the-best-ai-design-agent-for-beginners",
            "lovart-nano-banana-2-ai-design-agent",
            "imagefx-review",
            "wan-2.1-ai-review",
            "complete-guide-object-removal-inpainting-ai",
            "ai-animal-pet-generators-compared",
            "best-agent-for-sbos",
            "best-ai-design-tools-in-2025-complete-comparison-guide-for-creators-and-marketers",
            "ai-video-models-compared-2026",
            "ai-design-tools-2025",
            "amazon-requirements-ai-white-background-images",
            "lovart-ai-image-generator-create-stunning-images-with-ai",
            "responsible-ai-design-lovart",
            "complete-guide-ai-art-platform-selection-2026",
            "complete-guide-ai-video-model-selection-2026",
            "capcut-ai-review",
            "ai-design-global-adoption-trends-2026",
            "ai-image-models-compared-2026",
            "best-haiper-ai-alternatives-in-2025-video-generation-compared",
            "law-firm-branding-trust-authority-design-2027",
            "video-generators-review",
            "hailuo-ai-review-2025-cinematic-video-generation-tested-hands-on",
            "haiper-ai-review-2025-features-pricing-and-real-world-performance-test",
            "ultimate-guide-ai-design-agent-canvas-for-creators-business",
            "loveart-ai-business-creative-workflows",
            "step-by-step-ai-design-replace-photoshop-25-types",
            "02-wiki-batch-generation-best-practices",
            "freepik-ai-image-generator-review",
            "vidu-ai-review-2025-ai-video-generation-platform-features-and-verdict",
            "ai-powered-design-agent-for-creators",
            "small-business-design-tools-compared",
            "the-best-ai-agent-driven-canvas-for-digital-nomads-with-lovart-all-in-one-design-agent",
            "ai-floor-plan-tools-compared",
            "ai-commercial-license-country-comparison-2026",
            "content-refresh-ai-design-tool-reviews-2027",
            "shutterstock-ai-review",
            "adobe-firefly-review-2025-features-pricing-and-honest-hands-on-test",
            "lovart-account-enforcement",
            "best-ai-design-agent-for-e-book-author",
            "how-to-chat-generate-any-design-type-lovart-agent",
            "complete-guide-ai-background-wallpaper-pattern-design",
            "imagineart-review",
            "midjourney-character-reference-vs-lovart-nano-banana-consistency-test",
            "ai-design-freelance-pricing-guide-2026",
            "ai-design-contracts-freelancers-agencies-should-include",
            "seedance-2-orchestration-lovart-ai-agent",
            "figma-vs-ai-design-agents",
            "capcut-ai-review-2025-features-pros-cons-and-honest-verdict",
        ]
        # Slice to batch
        slugs = slugs[batch_start:batch_start + batch_size]

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get auth token
    print("Getting Sanity auth token...")
    token = get_auth_token()

    # Pull each blog post
    results = []
    for i, slug in enumerate(slugs, 1):
        print(f"[{i}/{len(slugs)}] Pulling: {slug}")
        try:
            post = pull_blog_post(slug, token)
            if post:
                output_file = OUTPUT_DIR / f"{slug}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(post, f, ensure_ascii=False, indent=2)
                results.append({"slug": slug, "status": "ok", "file": str(output_file)})
                print(f"  ✓ Saved to {output_file.name}")
            else:
                results.append({"slug": slug, "status": "not_found"})
                print(f"  ✗ Not found in Sanity")
        except Exception as e:
            results.append({"slug": slug, "status": "error", "error": str(e)})
            print(f"  ✗ Error: {e}")

    # Summary
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\nSummary: {ok}/{len(slugs)} posts pulled successfully")

    # Save manifest
    manifest_file = OUTPUT_DIR / "manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Manifest saved to {manifest_file}")

if __name__ == "__main__":
    main()
