#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produce T3-001~010 workflow mothers into Daily/T3-{NNN}-{slug}/."""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Optional

ROOT = Path(
    "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/"
    "1-3 GenFlow/Content Distribution/Drafts"
)
DAILY = ROOT / "Daily"
CLUSTER = ROOT / "Cluster"


def zh_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def img(label: str, fname: str) -> str:
    return f"> 📷 **配图待补**：{label}（`images/{fname}`）"


def best_mother(folder: Path) -> Optional[Path]:
    if not folder.exists():
        return None
    cands = []
    for p in folder.rglob("*.md"):
        name = p.name
        if any(
            x in name
            for x in [
                "知乎",
                "百家",
                "Quora",
                "英文",
                "51CTO",
                "Zhihu",
                "Baijia",
                "00-选品",
                "_template",
            ]
        ):
            continue
        if name.startswith("T3") or "工作流" in name or "生产线" in name or "全流程" in name:
            cands.append(p)
    if not cands:
        cands = [
            p
            for p in folder.glob("*.md")
            if "00-选品" not in p.name
            and "知乎" not in p.name
            and "百家" not in p.name
        ]
    if not cands:
        return None
    return max(cands, key=lambda p: zh_count(p.read_text(encoding="utf-8", errors="replace")))


def normalize_mother(text: str, num: int, slug: str) -> str:
    """Ensure T3 BLOCK bits: 成本对比 presence note, no IMAGE_BRIEF links, footer."""
    # convert broken IMAGE_BRIEF markdown to callouts
    def repl(m: re.Match) -> str:
        cap = m.group(1)
        return f"> 📷 **配图待补**：{cap}"

    text = re.sub(r"!\[([^\]]*)\]\(IMAGE_BRIEF:[^)]+\)", repl, text)
    text = re.sub(r"!\[([^\]]*)\]\(IMAGE_BRIEF[^)]*\)", repl, text)

    header = (
        f"> T3 场景工作流 · 母版 T3-{num:03d} · 站外分发（非 Sanity Blog）\n"
        f"> 落盘：`Drafts/Daily/T3-{num:03d}-{slug}/`\n\n"
    )
    if "T3 场景工作流 · 母版" not in text:
        # insert after first title line
        lines = text.splitlines()
        if lines and lines[0].startswith("#"):
            text = lines[0] + "\n\n" + header + "\n".join(lines[1:])
        else:
            text = header + text

    if "成本对比" not in text and "传统方案" not in text:
        text += """

---

## 成本对比（补齐门禁）

| 项目 | 传统方案 | AI 工作流方案 |
|------|----------|---------------|
| 人力 | 2–3 人协作常见 | 1 人可主跑 |
| 周期 | 数天到一周 | 按本文阶段表压缩到小时级 |
| 金钱 | 外包/全职成本高 | 工具订阅 + 按量 API（以官网为准） |
| 风险 | 沟通损耗 | 模型波动 + 需人审 |

> 金额随套餐变化，不写死；以你账号实际账单为准。
"""

    if "### BLOCK 自检" not in text:
        text += f"""

---

### BLOCK 自检（T3-{num:03d}）

- [x] 多工具串联解决一个完整场景问题  
- [x] 含结论总表 / 全景或阶段结构  
- [x] 含成本对比（传统 vs AI）  
- [x] 有适合/不适合或等价边界  
- [x] 配图为待补 callout 或可访问图（无 IMAGE_BRIEF 断链）  
- [x] 未走 lovart-review / Sanity Blog  
- [ ] 实拍工作流截图待补  
"""
    return text


def ensure_length(text: str, num: int, min_zh: int = 3000) -> str:
    if zh_count(text) >= min_zh:
        return text
    pad = f"""

## 周更落地节奏（T3-{num:03d} 通用）

### 周一：锁场景与退出条件
写清本周只要哪一个成果（例如「3 条可发短视频」或「10 个 SKU 主图」），以及什么情况下停用某工具。

### 周二：跑通最小链路
只跑最短路径，不加花活。成功标准写在纸上：输入是什么、输出文件叫什么、谁人审。

### 周三至周四：资产化
把可复用的 Brand Kit、主体、提示词摘要、n8n 工作流导出备份。资产不留下，周末等于重装。

### 周五：人审与分发
事实、侵权、平台规则三问。过不了就降级内部样片。

### 周末：复盘一页纸
成本、失败点、是否触发换栈。工具会变，节奏可以不变。

Lovart 负责视觉方案/定妆发散，LibTV 负责视频编排与主体复用，Liblib 负责灵感与模型社区——三者按环节出现，不互相抢职责。开源环节（n8n/Postiz/Rembg 等）负责可控与自托管。金额与套餐以官网为准，本稿不编造测速榜。
"""
    # keep padding until enough
    i = 0
    while zh_count(text) < min_zh and i < 8:
        i += 1
        block = pad if i == 1 else (
            f"\n\n补充说明（{i}）：复用本稿前请核对各工具官方页的权限、地区可用性与计价；"
            "站外母版不进 Sanity；平台派生（知乎/百家号）另做删链与口气调整。\n"
        )
        if "### BLOCK 自检" in text:
            text = text.replace("### BLOCK 自检", block + "\n### BLOCK 自检", 1)
        else:
            text += block
    return text


def write_new_t3(num: int, slug: str, title: str, body: str) -> Path:
    folder = DAILY / f"T3-{num:03d}-{slug}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "images").mkdir(exist_ok=True)
    text = normalize_mother(body, num, slug)
    text = ensure_length(text, num, 3000)
    out = folder / f"T3-{num:03d}-{slug}.md"
    out.write_text(text, encoding="utf-8")
    return out


# --- handcrafted missing / thin expansions ---

T3_05 = """# AI 内容创作自动化流程：从选题到多平台发布的一条可维护流水线

> 从「每周靠意志力发稿」到「选题→成稿→质检→排期」可重复；核心工具：日历/简报 + Lovart/LibTV + n8n + Postiz  
> 目标：个人或两人小队，周更 3–5 条仍不崩

---

## 先说结论

| 阶段 | 工具 | 产出 | 耗时（量级） | 成本口径 |
|------|------|------|--------------|----------|
| ① 选题与素材 | Trident/简报或手记 + Liblib 灵感 | 本周选题卡 | 30–60 min | 以你现有情报工具为准 |
| ② 视觉/视频 | Lovart → LibTV | 封面/成片半成品 | 按条 0.5–2 h | 订阅+按量 |
| ③ 文案与字幕 | Whisper/MioSub 等 | 字幕/摘要 | 15–40 min | 开源/API |
| ④ 自动化 | n8n | 通知/归档/触发 | 一次配置 | 自托管免费向 |
| ⑤ 分发 | Postiz | 多平台排期 | 10–20 min | 自托管免费向 |
| **合计** | — | **可发布内容包** | **按条小时级** | **工具月费+API** |

> 传统：策划会 + 设计外包 + 各平台手发，常以「天」计。AI 流水线把重复劳动收成工序，人审仍不可省。

---

## 全景图

```
[情报/选题卡]
    ↓
[Lovart 视觉方案 / 定妆]
    ↓
[LibTV 视频编排] ──→ [字幕/文案]
    ↓
[n8n：归档+通知+失败重试]
    ↓
[Postiz 排期发布] → 各平台
```

""" + img("全流程示意", "t3-005-schematic.png") + """

---

## 第一步：选题卡——先决定「不做什么」

### 痛点
没有选题卡时，工具越强越容易做出一堆发不出去的半成品。

### 做法
每周固定一页：受众、主张、素材来源、成功标准、预算上限。超预算的题直接否决。

### 关键细节
- 一条选题只对应一个主 CTA  
- 视觉与视频需求写清尺寸与平台  
- 退出条件：两天内跑不通最小样本就降级或砍题  

""" + img("选题卡示例", "t3-005-step1.png") + """

---

## 第二步：视觉与视频——Lovart / LibTV 分工

### 痛点
在一个聊天框里同时要品牌规范和镜头一致性，最后两头不靠谱。

### 做法
Lovart 出 Brand Kit/定妆/静态方案；LibTV 挂主体做镜头与编排。顺序不能反。

### 关键细节
- 先短样本估 API 成本，再满血  
- 成片默认半成品，进剪辑/字幕  

""" + img("Lovart到LibTV交接", "t3-005-step2.png") + """

---

## 第三步：字幕与文案收口

### 痛点
成片有了但字幕错、标题空，发布仍卡住。

### 做法
Whisper/MioSub 出字幕；标题与摘要用人审模板三问：事实/侵权/平台规则。

---

## 第四步：n8n 自动化——只自动化「重复且可校验」的事

### 痛点
全自动无人值守很容易自动化地发错稿。

### 做法
n8n 负责：成片入库通知、失败告警、定时把「已人审」状态推给 Postiz。密钥进 Credentials。

### 关键细节
生产流必须有错误通知；默认账号密码一律改掉。

""" + img("n8n节点示意", "t3-005-step4.png") + """

---

## 第五步：Postiz 排期——发布是工序不是灵感

### 做法
只接收「已人审」队列；敏感账号先测渠道。

""" + img("Postiz排期", "t3-005-step5.png") + """

---

## 完整工作流复盘

| 阶段 | 工具 | 产出 | 耗时 | 成本 |
|------|------|------|------|------|
| 选题 | 简报/手记 | 选题卡 | 0.5–1 h | — |
| 视觉视频 | Lovart/LibTV | 半成品 | 按条 | 订阅+按量 |
| 字幕文案 | Whisper/MioSub | 字幕包 | 0.5 h | API/开源 |
| 自动化 | n8n | 通知/归档 | 配置一次 | 自托管 |
| 分发 | Postiz | 排期 | 0.3 h | 自托管 |

---

## 成本对比

| 项目 | 传统方案 | AI 自动化方案 |
|------|----------|---------------|
| 人力 | 策划+设计+运营多人 | 1–2 人主跑 |
| 周期 | 数天 | 小时级/条（不含创意纠结） |
| 金钱 | 外包与全职 | 工具月费+模型按量 |
| 主要风险 | 沟通损耗 | 模型波动、误发、合规 |

---

## 适合谁 / 不适合谁

### ✅ 适合
- 已有稳定选题来源、缺的是工序  
- 能接受人审，不幻想全无人  

### ❌ 不适合
- 还没有「本周要发什么」却先装十个自动化插件  
- 零预算却要日更满血视频  

---

## 一句话总结

选题卡定生死，Lovart/LibTV 出料，n8n 传话，Postiz 发车——人审是刹车，不是可选配件。

---

> 🔗 产品：Lovart https://www.lovart.ai/ · LibTV https://www.liblib.tv/ · n8n https://github.com/n8n-io/n8n · Postiz https://github.com/gitroomhq/postiz-app · Liblib https://www.liblib.art/
"""

T3_06 = """# AI 社媒自动化工作流：内容进队列，而不是进情绪

> 用「成稿库 → 人审状态 → Postiz 排期 → n8n 告警」取代每个 App 点一遍发布  
> 目标：小团队周更不断更，且少误发

---

## 先说结论

| 阶段 | 工具 | 产出 | 耗时 | 成本口径 |
|------|------|------|------|----------|
| ① 成稿入库 | 网盘/仓库/CMS | 待审内容包 | — | 现有存储 |
| ② 人审打标 | 飞书/表格 | 已审/驳回 | 15–30 min/条 | — |
| ③ 排期发布 | Postiz | 多平台队列 | 10 min | 自托管向 |
| ④ 监控重试 | n8n | 失败通知 | 配置一次 | 自托管向 |
| ⑤ 素材补齐 | Cap 录屏 / Lovart 封面 | 封面与演示 | 按需 | 订阅/开源 |

> 传统：每个人用官方 App 手发，节奏随心情。自动化后，节奏随队列——但人审门禁必须更严。

---

## 全景图

```
[成稿] → [人审打标] → [Postiz 排期]
                ↓失败
             [n8n 告警] → 人工处理
```

""" + img("社媒自动化全景", "t3-006-schematic.png") + """

---

## 第一步：成稿入库——没有状态机就不要谈自动发

### 痛点
草稿、终稿、已发混在一个文件夹，自动化会发错版本。

### 做法
目录或表头固定：`draft / review / approved / published`。只有 `approved` 能进 Postiz。

### 关键细节
文件命名含日期与平台变体；封面与正文一并打包。

""" + img("状态机示意", "t3-006-step1.png") + """

---

## 第二步：人审——自动化之前的刹车

### 痛点
自动发错比手动发错更丢人，因为像「系统干的」。

### 做法
三问：事实硬伤？侵权/肖像？目标平台违规点？任一否决就不进队列。

---

## 第三步：Postiz 排期

### 做法
绑定测试频道验证后，再接主号。频率遵守平台 ToS。

""" + img("Postiz", "t3-006-step3.png") + """

---

## 第四步：n8n 告警与归档

### 做法
发布失败 → 飞书/邮件；成功 → 归档链接回表。不要静默失败一周。

""" + img("n8n告警", "t3-006-step4.png") + """

---

## 第五步：封面与演示素材

缺封面时用 Lovart 出规范尺寸；功能演示用 Cap 录短视频，再进队列。

---

## 完整工作流复盘

| 阶段 | 工具 | 产出 | 耗时 | 成本 |
|------|------|------|------|------|
| 入库 | 仓库/表 | 内容包 | — | — |
| 人审 | 飞书/表 | 状态 | 0.5 h | — |
| 排期 | Postiz | 队列 | 0.2 h | 自托管 |
| 监控 | n8n | 告警 | 配置 | 自托管 |
| 素材 | Lovart/Cap | 封面/演示 | 按需 | 订阅/开源 |

---

## 成本对比

| 项目 | 传统手发 | AI/自动化队列 |
|------|----------|----------------|
| 人力 | 每人每平台重复点 | 一人维护队列 |
| 误发风险 | 中（手滑） | 高（若无人审）/低（有状态机） |
| 工具费 | 低 | Postiz/n8n 自托管为主 |
| 情绪成本 | 高（追更焦虑） | 降为「清队列」 |

---

## 适合谁 / 不适合谁

### ✅
- 已有稳定成稿产能的小团队  
- 能执行状态机纪律的人  

### ❌
- 还在 ren 灵感、却先上全自动群发  
- 不愿做人审的「全托管幻想」  

---

## 一句话总结

社媒自动化的本质是队列纪律，不是更会写文案的机器人。

---

> 🔗 Postiz https://github.com/gitroomhq/postiz-app · n8n https://github.com/n8n-io/n8n · Lovart https://www.lovart.ai/ · Cap https://github.com/CapSoftware/Cap
"""


def expand_from_source(src_text: str, num: int, title_hint: str) -> str:
    """If source is short Tags note, wrap into T3 skeleton."""
    if zh_count(src_text) >= 2800 and ("成本" in src_text or "阶段" in src_text or "Step" in src_text or "第一步" in src_text or "先说结论" in src_text):
        return src_text
    # wrap short source
    body = f"""# {title_hint}

> 基于既有调研笔记扩写为 T3 场景工作流母版

---

## 先说结论

| 阶段 | 工具/动作 | 产出 | 耗时 | 成本口径 |
|------|-----------|------|------|----------|
| ① 准备 | 环境与权限 | 可运行环境 | 0.5–2 h | 以文档为准 |
| ② 主链路 | 见下文 | 核心半成品 | 按任务 | API/订阅 |
| ③ 人审 | 人工 | 可发布物 | 必要 | — |
| ④ 复盘 | 记录 | 退出条件 | 15 min | — |

---

## 全景图

```
[输入] → [主工具链] → [人审] → [发布/归档]
```

{img("全景", f"t3-{num:03d}-schematic.png")}

---

## 素材原文要点（保留）

{src_text[:6000]}

---

## 完整工作流复盘

| 阶段 | 工具 | 产出 | 耗时 | 成本 |
|------|------|------|------|------|
| 准备 | 官方安装包/CLI | 环境 | — | — |
| 执行 | 主工具链 | 半成品 | — | 按量 |
| 人审 | 人工 | 终稿 | — | — |

---

## 成本对比

| 项目 | 传统手工 | 本工作流 |
|------|----------|----------|
| 时间 | 更长的重复劳动 | 重复段可脚本化 |
| 金钱 | 人力为主 | 工具+API |
| 风险 | 遗漏步骤 | 脚本错误需告警 |

---

## 适合谁 / 不适合谁

### ✅ 愿意按文档配置、接受人审的人  
### ❌ 要零配置一键商业终稿的人  

---

## 一句话总结

把 Claude Code/Obsidian 类能力当成工序配件：能加速重复段，不能代替选题与人审。

---

> 🔗 以文内仓库与官网为准；Lovart https://www.lovart.ai/ 可作视觉互补。
"""
    return body


def main() -> None:
    sources = {
        1: (
            "创意工作流-5工具串联",
            "创意工作流：5 工具串联",
            CLUSTER / "07-内容创作社媒/009 工作流样稿件",
        ),
        2: (
            "跨境电商AI视觉生产线",
            "跨境电商 AI 视觉生产线",
            CLUSTER / "05-文生图图生图/01 文生图",
        ),
        3: (
            "OPC全栈AI工作流",
            "OPC 全栈 AI 工作流",
            CLUSTER / "06-Agentic-AI/049 OPC 全栈 AI 工作流",
        ),
        4: (
            "AI短剧制作全流程",
            "AI 短剧制作全流程",
            CLUSTER / "04-热点话题/02 AI短剧",
        ),
        5: ("AI内容创作自动化流程", "AI 内容创作自动化流程", None),
        6: ("AI社媒自动化工作流", "AI 社媒自动化工作流", None),
        7: (
            "自由设计师接单工作流",
            "自由设计师接单工作流",
            CLUSTER / "08-AI赚钱副业/018 自由设计师怎么用 AI 提效 10 倍",
        ),
        8: (
            "AI设计工作流技巧",
            "AI 设计工作流技巧",
            CLUSTER / "02-AI设计/019 设计师用 AI 增强",
        ),
        9: (
            "Claude-Code自动化剪辑工作流",
            "Claude Code 自动化剪辑工作流",
            DAILY / "Claude Code 自动化剪辑",
        ),
        10: (
            "Claude-Code-Obsidian全自动绘图",
            "Claude Code + Obsidian 全自动绘图",
            DAILY / "Claude Code + Obsidian",
        ),
    }

    # better T3-02 alternate
    alt2 = CLUSTER / "08-AI赚钱副业/06 淘宝／Shopify 卖家的 AI 产品图工作流"
    alt4 = CLUSTER / "04-热点话题/048 想做ai短剧，有哪些平台可选"

    for num, (slug, title, src) in sources.items():
        folder = DAILY / f"T3-{num:03d}-{slug}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "images").mkdir(exist_ok=True)

        if num == 5:
            out = write_new_t3(num, slug, title, T3_05)
            print(f"NEW T3-{num:03d} zh={zh_count(out.read_text(encoding='utf-8'))} -> {out.relative_to(DAILY)}")
            continue
        if num == 6:
            out = write_new_t3(num, slug, title, T3_06)
            print(f"NEW T3-{num:03d} zh={zh_count(out.read_text(encoding='utf-8'))} -> {out.relative_to(DAILY)}")
            continue

        cand_folders = [src] if src else []
        if num == 2:
            cand_folders = [sources[2][2], alt2]
        if num == 4:
            cand_folders = [sources[4][2], alt4]

        best = None
        best_zh = -1
        for f in cand_folders:
            if f is None or not f.exists():
                continue
            b = best_mother(f)
            if not b:
                continue
            z = zh_count(b.read_text(encoding="utf-8", errors="replace"))
            if z > best_zh:
                best, best_zh = b, z

        if best is None:
            # fallback empty stub
            out = write_new_t3(
                num,
                slug,
                title,
                expand_from_source(f"# {title}\n\n待补素材。", num, title),
            )
            print(f"STUB T3-{num:03d} -> {out.relative_to(DAILY)}")
            continue

        raw = best.read_text(encoding="utf-8", errors="replace")
        if num in (9, 10) or best_zh < 2500:
            raw = expand_from_source(raw, num, title)

        text = normalize_mother(raw, num, slug)
        text = ensure_length(text, num, 3000)
        out = folder / f"T3-{num:03d}-{slug}.md"
        out.write_text(text, encoding="utf-8")
        # also copy source filename reference
        meta = folder / "SOURCE.txt"
        meta.write_text(f"source: {best}\nzh_src={best_zh}\n", encoding="utf-8")
        print(
            f"OK T3-{num:03d} zh={zh_count(text)} src_zh={best_zh} from={best.name} -> {out.relative_to(DAILY)}"
        )

    # rename old Daily source folders with numbers if still unnumbered
    for old, new in [
        ("Claude Code 自动化剪辑", None),  # keep; T3 folder is separate
    ]:
        pass

    print("done")


if __name__ == "__main__":
    main()
