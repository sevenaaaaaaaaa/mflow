#!/usr/bin/env python3
"""查看 GSC 未映射国家 (其他 桶的构成)."""
import json
from collections import defaultdict

GSC = json.load(open("/tmp/gsc_windows.json"))
REGION_MAP = {
    "ind": "南亚", "pak": "南亚", "idn": "南亚", "bgd": "南亚", "lka": "南亚", "npl": "南亚",
    "bra": "拉美", "mex": "拉美", "arg": "拉美", "col": "拉美", "chl": "拉美", "per": "拉美",
    "irn": "中东非", "egy": "中东非", "dza": "中东非", "sau": "中东非", "nga": "中东非", "mar": "中东非", "tur": "中东非", "are": "中东非", "isr": "中东非", "kwt": "中东非",
    "irq": "中东非", "tun": "中东非", "yem": "中东非", "ago": "中东非", "ken": "中东非", "lby": "中东非", "pse": "中东非", "lbn": "中东非", "jor": "中东非", "qat": "中东非", "sdn": "中东非", "zaf": "中东非", "eth": "中东非", "gha": "中东非", "omn": "中东非", "bhr": "中东非", "dza": "中东非", "cmr": "中东非", "civ": "中东非", "uga": "中东非", "tza": "中东非", "zwe": "中东非", "som": "中东非", "mli": "中东非", "bfa": "中东非", "ner": "中东非", "sen": "中东非", "tgo": "中东非", "ben": "中东非", "mdg": "中东非", "mrt": "中东非",
    "ven": "拉美", "ecu": "拉美", "bol": "拉美", "pry": "拉美", "cri": "拉美", "pan": "拉美", "ury": "拉美", "dom": "拉美", "gtm": "拉美", "hnd": "拉美", "nic": "拉美", "slv": "拉美", "cub": "拉美", "hti": "拉美", "pry": "拉美",
    "usa": "北美", "can": "北美", "gbr": "北美", "aus": "北美", "nzl": "北美",
    "chn": "大中华", "twn": "大中华", "hkg": "大中华", "mac": "大中华",
    "jpn": "日本",
    "deu": "欧洲", "fra": "欧洲", "ita": "欧洲", "esp": "欧洲", "rus": "欧洲", "pol": "欧洲", "ukr": "欧洲", "nld": "欧洲", "bel": "欧洲", "che": "欧洲", "swe": "欧洲", "prt": "欧洲", "rou": "欧洲", "grc": "欧洲", "cze": "欧洲", "hun": "欧洲", "aut": "欧洲", "fin": "欧洲", "dnk": "欧洲", "nor": "欧洲", "irl": "欧洲", "bgr": "欧洲", "blr": "欧洲", "srb": "欧洲", "hrv": "欧洲", "svk": "欧洲", "svn": "欧洲", "ltu": "欧洲", "lva": "欧洲", "est": "欧洲", "alb": "欧洲", "mkd": "欧洲", "bih": "欧洲", "mne": "欧洲", "geo": "欧洲", "arm": "欧洲", "aze": "欧洲", "mda": "欧洲",
    "kor": "韩国", "vnm": "东南亚", "tha": "东南亚", "mys": "东南亚", "sgp": "东南亚", "phl": "东南亚", "khm": "东南亚", "mmr": "东南亚", "lao": "东南亚", "brn": "东南亚", "tls": "东南亚",
    "kaz": "中亚", "uzb": "中亚", "kgz": "中亚", "tkm": "中亚", "tjk": "中亚", "afg": "中亚",
}
rows = GSC["data"]["cur"]["country"]
other = []
for r in rows:
    c = r["keys"][0].lower()
    if c not in REGION_MAP:
        other.append((c, r["clicks"], r["impressions"]))
other.sort(key=lambda x: -x[1])
print("=== cur 未映射国家 Top25 ===")
tot_other = sum(x[1] for x in other)
print(f"其他桶总点击: {tot_other:,}")
for c, cl, im in other[:25]:
    print(f"  {c:<6} clicks={cl:>6,} impr={im:>8,}")

# 新加坡/韩国/越南等在东南亚桶
regs = defaultdict(lambda: {"clicks": 0, "impr": 0})
for r in rows:
    c = r["keys"][0].lower()
    reg = REGION_MAP.get(c, "其他")
    regs[reg]["clicks"] += r["clicks"]
    regs[reg]["impr"] += r["impressions"]
tot = sum(v["clicks"] for v in regs.values())
print("\n=== 修正后大区 (cur) ===")
for reg, v in sorted(regs.items(), key=lambda x: -x[1]["clicks"]):
    print(f"  {reg:<6} clicks={v['clicks']:>7,} ({v['clicks']/tot*100:5.1f}%) impr={v['impr']:>9,}")

# prev 同口径
rows_p = GSC["data"]["prev"]["country"]
regs_p = defaultdict(lambda: {"clicks": 0, "impr": 0})
for r in rows_p:
    c = r["keys"][0].lower()
    reg = REGION_MAP.get(c, "其他")
    regs_p[reg]["clicks"] += r["clicks"]
    regs_p[reg]["impr"] += r["impressions"]
tot_p = sum(v["clicks"] for v in regs_p.values())
print("\n=== 修正后大区 (prev) ===")
for reg, v in sorted(regs_p.items(), key=lambda x: -x[1]["clicks"]):
    print(f"  {reg:<6} clicks={v['clicks']:>7,} ({v['clicks']/tot_p*100:5.1f}%) impr={v['impr']:>9,}")
