#!/usr/bin/env python3
"""Apply the single broken-target fix and align all generated artifacts."""
import csv, re, shutil, openpyxl
from pathlib import Path

BASE = Path("/Users/seveno/MFlow Dev/mflow/run/404-remediation-20261105")
OLD_SRC = "https://www.lovart.ai/es/tools/ai-logo-design-free"
OLD_TGT = "https://www.lovart.ai/tools/ai-logo-design"
NEW_TGT = "https://www.lovart.ai/features/ai-logo-design"

bak = BASE / "_backup_20261105_2359"
bak.mkdir(exist_ok=True)
for f in ["redirect-map.csv", "cf-bulk-redirects.csv", "nginx-redirect-map.conf",
          "Lovart-404分类处理-2026-11-05.xlsx", "README.md"]:
    shutil.copy2(BASE / f, bak / f)

# 1) redirect-map.csv
rows = list(csv.DictReader(open(BASE / "redirect-map.csv")))
for r in rows:
    if r["source_url"] == OLD_SRC:
        assert r["target_url"] == OLD_TGT, r
        r["target_url"] = NEW_TGT
with open(BASE / "redirect-map.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["source_url", "target_url", "rule", "last_crawled"])
    w.writeheader(); w.writerows(rows)

# 2) cf-bulk-redirects.csv
cf = list(csv.DictReader(open(BASE / "cf-bulk-redirects.csv")))
for r in cf:
    if r["source url"] == OLD_SRC:
        assert r["target url"] == OLD_TGT, r
        r["target url"] = NEW_TGT
with open(BASE / "cf-bulk-redirects.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["source url", "target url", "status code",
                                       "preserve query string", "preserve path suffix"])
    w.writeheader(); w.writerows(cf)

# 3) nginx map
p = BASE / "nginx-redirect-map.conf"
txt = p.read_text()
old_line = "/es/tools/ai-logo-design-free /tools/ai-logo-design;"
new_line = "/es/tools/ai-logo-design-free /features/ai-logo-design;"
assert old_line in txt, "nginx line not found"
p.write_text(txt.replace(old_line, new_line))
print("csv/cf/nginx updated")

# 4) Excel: row target + overview notes
xp = BASE / "Lovart-404分类处理-2026-11-05.xlsx"
wb = openpyxl.load_workbook(xp)
changed = 0
for ws in wb.worksheets:
    if ws.title == "总览与行动方案":
        continue
    hdr = None; idx = {}
    for row in ws.iter_rows():
        vals = [c.value for c in row]
        if hdr is None:
            if vals and vals[0] == "优先级":
                hdr = vals; idx = {v: i for i, v in enumerate(vals) if v}
            continue
        if not vals or not vals[0]:
            continue
        if vals[idx["404 URL"]] == OLD_SRC:
            assert vals[idx["301 目标"]] == OLD_TGT, vals
            row[idx["301 目标"]].value = NEW_TGT
            act = row[idx["建议动作"]]
            act.value = str(act.value).replace(OLD_TGT, NEW_TGT)
            changed += 1
print("excel rows changed", changed)
assert changed == 1

ov = wb["总览与行动方案"]
# step-1 note
for row in ov.iter_rows():
    v = row[0].value
    if isinstance(v, str) and v.startswith("第1步"):
        row[1].value = str(row[1].value).replace(
            "需 lovart.ai 基础设施权限。",
            "需 lovart.ai 基础设施权限。980 条目标已实测可访问（见「301目标验证」表）。")
    if isinstance(v, str) and v.startswith("第3步"):
        row[1].value = ("线上在营页面 hreflang 仍声明已删语言版（实测复现）。改为仅输出「该语言文档真实存在」的 alternate。"
                        "本次 1000 条 404 样本与线上 sitemap 零重合；sitemap 存量 URL 仍需按 11-05 audit 清单另行清理。")
    if isinstance(v, str) and v.startswith("第4步"):
        row[1].value = str(row[1].value).replace("R4 21 条", "R4 13 + R5 7 共 20 条")
# verification line appended after last non-empty row
last = max((c.row for row in ov.iter_rows() for c in row if c.value is not None), default=46)
ov.cell(row=last + 2, column=1, value="验证结果")
ov.cell(row=last + 2, column=2, value="301 目标 980/980 实测 HTTP 200（2026-11-05 抓测，无跳转链）；1 条错配已修正：/es/tools/ai-logo-design-free → /features/ai-logo-design")
wb.save(xp)
print("excel saved; overview last row", last)
