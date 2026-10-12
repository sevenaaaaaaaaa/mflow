#!/usr/bin/env python3
"""write-c3-content.py — 把 C3 内容（空 tab 面板 + agencies/nonprofits 整块）
写进 c3-tabs-content.json（panel1_html 保留骨架抽取的原样 HTML）。用后即删。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
F = ROOT / "c3-tabs-content.json"
data = json.loads(F.read_text(encoding="utf-8"))

# 面板 HTML 模板：tailwind 类复刻面板 1 的文本列样式（replica.css 全局在，类继续生效）
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" '
       'viewBox="0 0 24 24" class="size-4" aria-hidden="true">'
       '<path fill="currentColor" fill-opacity="0.9" d="M17.942 6.498a.75.75 0 0 1 1.116 1.004'
       'l-9 10a.75.75 0 0 1-1.088.028l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.94 3.94z"></path></svg>')


def panel(h3, p, points):
    lis = "".join(
        f'<li class="text-text-default flex gap-2 text-[14px] leading-snug">{SVG}<span>{x}</span></li>'
        for x in points)
    return (f'<h3 class="text-text-default font-serif-deck mb-4 line-clamp-2 text-[20px] '
            f'md:min-h-15 md:text-[24px]">{h3}</h3>'
            f'<p class="text-text-secondary line-clamp-4 text-[14px] leading-relaxed md:mb-4 '
            f'md:text-[15px]">{p}</p>'
            f'<ul class="mt-6 space-y-2" style="min-height:4.75rem">{lis}</ul>')


# slug → {"labels": [...]（可选，agencies/nonprofits 需要给）,
#         "panels": {tab序号(1-based): (h3, p, [要点×3])}}——只写要补/覆盖的
C3 = {
    "replica-solution-ai-design-for-fitness-wellness-hub": {
        "panels": {
            2: ("Turn trial passes into members",
                "Promo pages, offer emails, and retargeting ads that follow the trial week with the right nudge.",
                ["Offer landing pages", "Retargeting ad sets", "Win-back emails"]),
            3: ("Keep members coming back",
                "Seasonal challenge kits, milestone posts, and member newsletters generated from your class calendar.",
                ["Challenge kits", "Milestone posts", "Member newsletters"]),
            4: ("One studio look everywhere",
                "Lock your logo, colors, and tone into a Brand Kit that applies to every generation.",
                ["Studio Brand Kit", "On-brand templates", "One-click re-styling"]),
        }
    },
    "replica-solution-ai-design-for-small-business-hub": {
        "panels": {
            2: ("Show the space and the menu",
                "Photo-driven menus, gallery pages, and seasonal lookbooks that make the place feel real before people visit.",
                ["Photo menus", "Gallery pages", "Seasonal lookbooks"]),
            3: ("Bring regulars back",
                "Loyalty cards, birthday offers, and email newsletters that keep the regulars engaged between visits.",
                ["Loyalty offers", "Birthday promos", "Email newsletters"]),
            4: ("Run the week in one session",
                "Batch a week of posts, signage updates, and staff notices in a single design session.",
                ["Weekly post batches", "Signage updates", "Staff notices"]),
        }
    },
    "replica-solution-ai-design-solution-for-creators": {
        "panels": {
            2: ("Feed the algorithm consistently",
                "Series covers, clip graphics, and community posts generated on your upload cadence — never miss a slot.",
                ["Series covers", "Clip graphics", "Community posts"]),
            3: ("Package what sponsors want",
                "Sponsor decks, ad-read graphics, and merch drops rendered in your channel style.",
                ["Sponsor decks", "Ad-read graphics", "Merch mockups"]),
            4: ("A recognizable channel look",
                "Your colors, fonts, and thumbnail language locked into every asset automatically.",
                ["Channel brand kit", "Thumbnail language", "Consistent fonts"]),
        }
    },
    "replica-solution-ai-design-solution-for-marketing-teams": {
        "panels": {
            2: ("One brief, a week of assets",
                "Generate the full channel set from a single campaign brief — social, email, display, and landing heroes.",
                ["One-brief intake", "Full channel sets", "Same-day turnaround"]),
            3: ("Variants for every test cell",
                "Hooks, offers, and layouts as ready-to-run variants; ship the winner with Touch Edit.",
                ["Hook variants", "Offer matrices", "Fast Touch Edit"]),
            4: ("Spend hours on strategy",
                "Production runs itself; agency hours move from resizing to positioning and planning.",
                ["No resizing work", "Strategy-first hours", "Campaign-scale output"]),
        }
    },
    "replica-solution-ai-design-solution-for-saas": {
        "panels": {
            2: ("In-product moments that convert",
                "Onboarding checklists, empty states, and upgrade nudges designed from your UI context.",
                ["Onboarding flows", "Empty states", "Upgrade nudges"]),
            3: ("Sales collateral on demand",
                "Battlecards, one-pagers, and deck templates refreshed for every pitch without a design ticket.",
                ["Battlecards", "Pitch decks", "One-pagers"]),
            4: ("Global campaigns without the queue",
                "Localize winners per market and release; export locale-ready sets in minutes.",
                ["Per-market variants", "Locale-ready exports", "Release cadence"]),
        }
    },
    "replica-solution-ai-design-solution-for-shopify": {
        "panels": {
            2: ("Listing-ready product visuals",
                "Main shots, lifestyle scenes, and infographic callouts generated from the SKU context you uploaded.",
                ["Main shots", "Lifestyle scenes", "Infographic callouts"]),
            3: ("Ads built to convert browsers",
                "Meta and Google ad sets, PDP banners, and landing heroes tied to the offer calendar.",
                ["Meta & Google ad sets", "PDP banners", "Offer-linked landing heroes"]),
            4: ("Keep customers in the loop",
                "Email headers, SMS visuals, and post-purchase flows that match every drop.",
                ["Email headers", "SMS visuals", "Post-purchase flows"]),
        }
    },
    "replica-solution-good-design-for-business-owners": {
        "panels": {
            2: ("Ads and video that sell the product",
                "Meta and Google ad sets and product video storyboards generated from the same SKU context.",
                ["Meta & Google ads", "Video storyboards", "Seasonal refreshes"]),
            3: ("A brand worth remembering",
                "Logo refreshes, packaging mockups, and brand boards that scale from SKU one to a full shelf.",
                ["Logo refreshes", "Packaging mockups", "Brand boards"]),
            4: ("Campaigns across the calendar",
                "Prime Day, holiday, and launch campaigns planned and produced from one brief.",
                ["Prime Day kits", "Holiday campaigns", "Launch pushes"]),
        }
    },
    "replica-solution-good-design-for-marketers": {
        "panels": {
            2: ("Teach Lovart your playbook",
                "Encode your layout rules and review checklists as reusable skills the agent follows on every job.",
                ["Layout rules", "Review checklists", "Reusable skills"]),
            3: ("Motion without a motion team",
                "Turn static logos and key visuals into animated versions for social and ads.",
                ["Logo animation", "Social-ready motion", "Key visual loops"]),
            4: ("The right model per job",
                "Route each task to the best image or video model — GPT, Flux, Kling — from one canvas.",
                ["GPT · Flux · Kling", "One canvas, many models", "No extra subscriptions"]),
        }
    },
    "replica-tool-directory": {
        "panels": {
            2: ("Generate the product visual set",
                "Main shots, lifestyle scenes, and infographic callouts rendered from the context you uploaded.",
                ["Main shots", "Lifestyle scenes", "Infographic callouts"]),
            3: ("Edit anything in place",
                "Touch Edit swaps copy, crops, and colors; Text Edit tunes every headline — no re-prompting.",
                ["Touch Edit", "Text Edit", "Layer-level control"]),
            4: ("Video and variant sets",
                "Storyboard to clip, then spin channel variants sized for every placement.",
                ["Storyboard clips", "Channel variants", "Ad-ready exports"]),
        }
    },
    "composite-replica-all": {
        "panels": {
            2: ("Generate the product visual set",
                "Main shots, lifestyle scenes, and infographic callouts rendered from the context you uploaded.",
                ["Main shots", "Lifestyle scenes", "Infographic callouts"]),
            3: ("Edit anything in place",
                "Touch Edit swaps copy, crops, and colors; Text Edit tunes every headline — no re-prompting.",
                ["Touch Edit", "Text Edit", "Layer-level control"]),
            4: ("Video and variant sets",
                "Storyboard to clip, then spin channel variants sized for every placement.",
                ["Storyboard clips", "Channel variants", "Ad-ready exports"]),
        }
    },
    # agencies / nonprofits：整块重写（源块只有 h2 + 一句 p，0 个标签 0 个面板）
    "replica-solution-ai-design-solution-for-agencies": {
        "labels": ["Client brands", "Overflow briefs", "Pitch creative", "Deliver & bill"],
        "panels": {
            1: ("Switch brands in one click",
                "Each client's Brand Kit — colors, fonts, rules — applies automatically to every generation.",
                ["Brand Kit per client", "Auto-applied rules", "Zero style drift"]),
            2: ("Absorb overflow briefs",
                "On-demand capacity for the briefs you'd normally turn away — quality doesn't dip when volume spikes.",
                ["On-demand capacity", "No freelancer vetting", "Minutes, not weeks"]),
            3: ("Pitch with speculative creative",
                "Concept boards and mockups before the win — without burning pre-win agency hours.",
                ["Concept boards", "Mockup sets", "Low-cost speculation"]),
            4: ("Deliver in client formats",
                "Export in client-ready sizes and present in branded galleries; bill for strategy, not production.",
                ["Client-ready exports", "Branded galleries", "Margin-safe billing"]),
        }
    },
    "replica-solution-ai-design-solution-for-nonprofits": {
        "labels": ["Campaigns", "Donor trust", "Brand", "Launch"],
        "panels": {
            1: ("Describe the campaign once",
                "What's the appeal? Who's the audience? What's the ask? Generate campaign-appropriate visuals from the answers.",
                ["Appeal framing", "Audience fit", "Campaign visuals"]),
            2: ("Look credible to donors",
                "Studio-quality output every time — the polish that keeps donation pages and appeals credible.",
                ["Studio quality", "Trustworthy polish", "Consistent look"]),
            3: ("Apply the nonprofit's brand",
                "Logo, colors, typography — applied automatically to every generated asset.",
                ["Auto Brand Kit", "Typography rules", "Consistent identity"]),
            4: ("Launch appeals across channels",
                "Export for email, social, web, and print — campaigns ship faster and more budget reaches the mission.",
                ["Multi-channel exports", "Faster launches", "More for the mission"]),
        }
    },
}

n = 0
for slug, spec in C3.items():
    assert slug in data, slug
    if "labels" in spec:
        data[slug]["labels"] = spec["labels"]
    panels = {}
    for idx, (h3, p, pts) in spec["panels"].items():
        panels[str(idx - 1)] = panel(h3, p, pts)   # 0-based：0 = 面板1
        n += 1
    data[slug]["panels_html"] = panels

F.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"C3 内容写入：{len(C3)} 页 / {n} 段新面板")
