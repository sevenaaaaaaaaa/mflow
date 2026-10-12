#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fill-demo-faq.py — 把 4 个 native demo 页的 FAQ 占位内容固化为真答案。

为什么：replica.js 的 initFaqFill 运行时填充的最后一个依赖就是这 4 页的
核心 accordion 占位（"Answer this question here…"）。答案写进 accordion
的 tab_content 后，initFaqFill + LR_FAQ_ANSWERS（约 470 行）即可从 replica.js
删除。答案文本与注入样式完全沿用 initFaqFill 的产物，视觉零变化。

用法：python3 fill-demo-faq.py [--write]
"""
import argparse
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location(
    "deploy_migrated", ROOT / "deploy-migrated.py")
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)

NATIVE_DEMOS = [  # (page_id, slug)
    (18867, "lr-demo-native-comparison-hub"),
    (18871, "lr-demo-native-product-launch"),
    (18875, "lr-demo-native-fitness"),
    (18879, "lr-demo-native-shopify"),
]

# 与 replica.js pageSlug() 相同的短别名 → LR_FAQ_ANSWERS 键
ALIAS = {
    "fitness": "ai-design-for-fitness-wellness-hub",
    "small-biz": "ai-design-for-small-business-hub",
    "small-business": "ai-design-for-small-business-hub",
    "shopify": "ai-design-solution-for-shopify",
    "saas": "ai-design-solution-for-saas",
    "agencies": "ai-design-solution-for-agencies",
    "creators": "ai-design-solution-for-creators",
    "marketing-teams": "ai-design-solution-for-marketing-teams",
    "nonprofits": "ai-design-solution-for-nonprofits",
    "business-owners": "good-design-for-business-owners",
    "marketers": "good-design-for-marketers",
}

ANSWER_MARKUP = ('<div class="lr-faq-answer pb-4 font-sans text-[14px] '
                 'leading-[1.65] text-text-secondary">{}</div>')


def answers_for(slug):
    key = slug.replace("lr-demo-native-", "")
    key = ALIAS.get(key, key)
    js = (ROOT / "assets-src" / "lovart-replica.js").read_text(encoding="utf-8")
    m = re.search(r"window\.LR_FAQ_ANSWERS\s*=\s*(\{)", js)
    if not m:
        raise SystemExit("✗ replica.js 里找不到 LR_FAQ_ANSWERS")
    i, depth, j, instr, esc = m.start(1), 0, m.start(1), False, False
    while j < len(js):
        ch = js[j]
        if instr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                instr = False
        else:
            if ch == '"':
                instr = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    table = json.loads(js[i:j + 1])
    answers = table.get(key)
    if not answers:
        raise SystemExit(f"✗ LR_FAQ_ANSWERS 里没有 '{key}'")
    return answers


def walk(nodes, fn):
    for n in nodes:
        fn(n)
        walk(n.get("elements") or [], fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    dm._pin_probe()
    op = dm.build_opener()
    dm.login(op)
    payloads = []
    for pid, slug in NATIVE_DEMOS:
        r = dm.admin_ajax(op, {"action": "lr_elem_read", "page_id": pid, "secret": dm.SECRET})
        data = (r.get("data") or {}).get("data") or []
        answers = answers_for(slug)
        filled, skipped = 0, 0

        def fn(node):
            nonlocal filled, skipped
            if node.get("widgetType") != "accordion":
                return
            tabs = (node.get("settings") or {}).get("tabs") or []
            for t, a in zip(tabs, answers):
                txt = re.sub(r"<[^>]+>", "", t.get("tab_content", ""))
                if "every word stays" in txt:
                    t["tab_content"] = ANSWER_MARKUP.format(a)
                    filled += 1
                else:
                    skipped += 1

        walk(data, fn)
        print(f"{slug} (id={pid})：填充 {filled} 个占位，跳过 {skipped} 个非占位")
        if args.write and filled:
            payloads.append((pid, slug, {"version": "3.35.7", "data": data}))

    if not args.write:
        print("\n（预演结束。加 --write 固化到线上）")
        return 0

    # 上传 + 导入（复用 deploy-migrated 的通道）
    import subprocess
    paths = []
    for ix, (pid, slug, payload) in enumerate(payloads, 1):
        p = Path(f"/tmp/lr-faqfix-{pid}.json")
        p.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                     encoding="utf-8")
        # 远程用全新文件名：原名 URL 已被 Cloudflare 负缓存（fetch:404），换名即绕开
        paths.append((p, f"faqfix-{ix}.json"))
    subprocess.run(
        ["ssh", "-p", dm.ASSETS_PORT, f"root@{dm.ASSETS_HOST}",
         f"rm -f {dm.ASSETS_DIR}/lr-demo-faq-*.json"], check=True)
    for p, remote in paths:  # 每个文件单独 scp
        subprocess.run(
            ["scp", "-P", dm.ASSETS_PORT, str(p),
             f"root@{dm.ASSETS_HOST}:{dm.ASSETS_DIR}/{remote}"], check=True)
    fails = []
    for (pid, slug, _), (_, remote) in zip(payloads, paths):
        r = dm.admin_ajax(op, {
            "action": "lr_elem_import", "page_id": pid,
            "url": f"{dm.ASSETS_URL}/{remote}", "secret": dm.SECRET})
        ok = isinstance(r, dict) and r.get("success")
        print(("  ✓ " if ok else "  ✗ ") + f"{slug} (id={pid})"
              + ("" if ok else " → " + json.dumps(r, ensure_ascii=False)[:300]))
        if not ok:
            fails.append(slug)
    if fails:
        print(f"✗ 失败：{fails}")
        return 1
    print("\n4 个 native demo 页 FAQ 已固化。现在可以删 replica.js 的 initFaqFill + LR_FAQ_ANSWERS。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
