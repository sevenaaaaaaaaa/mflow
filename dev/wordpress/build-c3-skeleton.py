#!/usr/bin/env python3
"""build-c3-skeleton.py — 从 elem-migrated 抽 capability-tabs 块的
tab 标签 + 面板 1 完整 HTML，生成 c3-tabs-content.json 骨架。用后即删。"""
import html as H
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = [
    "replica-solution-ai-design-for-fitness-wellness-hub",
    "replica-solution-ai-design-for-small-business-hub",
    "replica-solution-ai-design-solution-for-creators",
    "replica-solution-ai-design-solution-for-marketing-teams",
    "replica-solution-ai-design-solution-for-saas",
    "replica-solution-ai-design-solution-for-shopify",
    "replica-solution-good-design-for-business-owners",
    "replica-solution-good-design-for-marketers",
    "replica-tool-directory",
    "composite-replica-all",
    "replica-solution-ai-design-solution-for-agencies",
    "replica-solution-ai-design-solution-for-nonprofits",
]

RE_LABEL_BTN = re.compile(r"<button[^>]*>(.*?)</button>", re.S)
RE_PANEL_FLEX = re.compile(
    r'<div class=\\?"flex flex-col md:flex-row md:items-stretch[^"]*\\?"[^>]*>.*?</ul></div></div>', re.S)
RE_PANEL_LOOSE = re.compile(
    r'<h3[^>]*>.*?</h3>(?:(?!<button).)*?(?:</ul>|</p>)', re.S)

def unesc(x):
    return H.unescape(re.sub(r"<[^>]+>", "", x)).strip()

out = {}
for f in PAGES:
    s = (ROOT / "elem-migrated" / f"{f}.json").read_text()
    blocks = re.split(r'"widgetType":\s*"html"', s)
    for b in blocks[1:]:
        if 'data-lp-section=\\"capability-tabs\\"' not in b[:5000]:
            continue
        i = b.find('data-lp-section=\\"capability-tabs\\"')
        seg = b[i:i + 40000]
        labels, seen = [], set()
        for btn in RE_LABEL_BTN.findall(seg):
            t = unesc(btn)
            if t and len(t) < 60 and t.lower() not in seen:
                seen.add(t.lower())
                labels.append(t)
        labels = labels[:4]
        m = RE_PANEL_FLEX.search(seg) or RE_PANEL_LOOSE.search(seg)
        out[f] = {"labels": labels, "panel1_html": m.group(0) if m else ""}
        break

(ROOT / "c3-tabs-content.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in out.items():
    print(k.replace("replica-", ""), "|", v["labels"], "| 面板1:", len(v["panel1_html"]))
