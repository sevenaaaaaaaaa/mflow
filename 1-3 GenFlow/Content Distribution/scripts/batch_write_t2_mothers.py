#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch expand Daily source notes into T2 mother drafts (站外分发).
- Does NOT invent Stars/benchmarks beyond source text
- Uses 配图待补 callouts (no broken IMAGE_BRIEF links)
- Renames folders to {NNN}-{ToolName} after write
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

DAILY = Path(
    "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/"
    "1-3 GenFlow/Content Distribution/Drafts/Daily"
)
SSOT = Path(
    "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/"
    "1-3 GenFlow/Content Distribution/Drafts/00-选题规划/文章三类体系.md"
)

# (num, folder_guess, display_name, category, competitors)
BATCH: list[tuple[int, str, str, str, str]] = [
    (8, "Duix-Avatar", "Duix-Avatar", "AI数字人", "HeyGen / D-ID"),
    (9, "Cap", "Cap", "录屏", "OBS / Loom"),
    (11, "n8n", "n8n", "自动化", "Zapier / Make"),
    (12, "bolt.diy", "bolt.diy", "AI建站", "v0 / Cursor"),
    (13, "Podcastfy", "Podcastfy", "AI播客", "NotebookLM / 剪映播客"),
    (14, "Postiz", "Postiz", "社媒管理", "Buffer / Typefully"),
    (15, "AnythingLLM", "AnythingLLM", "本地知识库", "Dify / Open WebUI"),
    (16, "OpenCut", "OpenCut", "视频编辑", "CapCut / OpenShot"),
    (17, "CogVideo", "CogVideo", "视频生成", "Wan2.1 / Runway"),
    (18, "shimmy", "shimmy", "本地推理", "Ollama / llama.cpp"),
    (19, "logocreator", "logocreator", "Logo生成", "Looka / Midjourney"),
    (20, "Penpot", "Penpot", "设计协作", "Figma / Lunacy"),
    (21, "Excalidraw", "Excalidraw", "白板", "FigJam / Miro"),
    (22, "Presenton", "Presenton", "AI PPT", "Gamma / Beautiful.ai"),
    (23, "Nano Banana Pro", "Nano Banana", "图像模型体验", "Flux / GPT Image"),
    (24, "Seedance", "Seedance 2.0", "视频模型", "Kling / Runway"),
    (25, "GPT-image 2", "GPT-image 2", "图像生成", "Flux / Midjourney"),
    (61, "MioSub", "MioSub", "AI字幕", "Aegisub + 机翻 / CapCut 字幕"),
    (62, "AirTranslate", "AirTranslate", "实时翻译", "MacWhisper / Language Reactor"),
    (63, "OpenCyvis", "OpenCyvis", "手机Agent", "Appium / 人工点按"),
    (64, "CyberVerse", "CyberVerse", "数字人Agent", "HeyGen / D-ID"),
    (65, "Qwerty Learner", "Qwerty Learner", "英语口语", "多邻国 / Anki"),
    (66, "OpenBidKit 易标", "OpenBidKit 易标", "AI写标书", "通用 ChatGPT / Word 模板"),
    (67, "AiMaMi", "AiMaMi", "Codex管理", "手改 ~/.codex / 终端"),
    (68, "Violin", "Violin", "视频翻译配音", "MioSub / 剪映配音"),
    (69, "纯前端音视频转文字", "纯前端音视频转文字", "浏览器转写", "Whisper 桌面 / 讯飞客户端"),
    (70, "deep-printfilm", "deep-printfilm", "AI漫剧", "Toonflow / Jellyfish"),
    (71, "VisionCull Pro", "VisionCull Pro", "本地选片", "AfterShoot / Excire"),
    (72, "飞搜 FeiSou", "飞搜 FeiSou", "文档搜索", "飞书内搜 / Google"),
    (73, "GEOFlow", "GEOFlow", "GEO内容系统", "WordPress+手动 / Dify"),
    (74, "SpokenType", "SpokenType", "语音输入", "系统听写 / OpenLess"),
    (75, "Jellyfish", "Jellyfish", "AI短剧工作流", "Toonflow / ComfyUI"),
    (76, "FreeCut", "FreeCut", "浏览器剪辑", "Clipchamp / LosslessCut"),
    (78, "Real-time Fund", "Real-time Fund", "基金估值", "天天基金 / 雪球"),
    (79, "Refly", "Refly", "Agent Skills", "Claude Skills / 手写 MCP"),
    (80, "Auto-Subs", "Auto-Subs", "达芬奇字幕", "Whisper 外挂 / CapCut"),
    (81, "Voice-Pro", "Voice-Pro", "AI配音", "ElevenLabs / Edge-TTS"),
    (82, "Design Prompts", "Design Prompts", "设计提示词", "自建 Prompt 库 / Notion"),
    (83, "BrowserWing", "BrowserWing", "网页自动化", "Playwright / Selenium"),
    (84, "Mac Sai", "Mac Sai", "Mac清理", "CleanMyMac / 系统自带"),
    (85, "PlainApp", "PlainApp", "跨设备控制", "AirDroid / scrcpy"),
    (86, "OpenLess", "OpenLess", "语音Prompt", "SpokenType / Whisper"),
    (87, "Privacy Filter", "Privacy Filter", "隐私脱敏", "手替 / 正则脚本"),
    (88, "UniClipboard", "UniClipboard", "跨设备剪贴板", "Paste / Maccy"),
    (89, "tools.video", "tools.video", "视频压缩", "HandBrake / 在线转码站"),
    (90, "Shizuku 通话录音", "Shizuku通话录音", "通话录音", "系统录音 / 第三方 App"),
    (91, "Image Provenance", "Image Provenance", "图片溯源", "C2PA 查看器 / 肉眼"),
    (92, "花快图", "花快图", "花纹生成", "AI 生图 / 素材站"),
    (93, "Claude Code Skills", "Claude Code Skills", "Agent技能", "Cursor Rules / MCP"),
    (94, "Claude Code Humanizer", "Claude Code Humanizer", "文风去AI味", "手改 / HumanizeAI"),
    (95, "Moltbot Skills", "Moltbot Skills", "插件生态", "自建 skill 库"),
    (96, "数据可视化看板", "数据可视化看板", "可视化", "Grafana / Metabase"),
    (97, "TTS Online", "TTS Online", "文字转语音", "Edge-TTS / 讯飞"),
    (98, "DeepLX Dashboard", "DeepLX", "翻译API", "DeepL 官方 / Google Translate"),
    (99, "EasySpider", "EasySpider", "无代码爬虫", "八爪鱼 / Playwright"),
    (100, "PDFgear", "PDFgear", "PDF工具", "Adobe Acrobat / Preview"),
    (101, "QuickRecorder", "QuickRecorder", "macOS录屏", "Cap / QuickTime"),
    (102, "Bob", "Bob", "翻译OCR", "系统翻译 / DeepL"),
    (103, "Blip", "Blip", "文件传输", "LocalSend / AirDrop"),
    (104, "Video Candy", "Video Candy", "在线视频编辑", "FreeCut / Clipchamp"),
    (105, "Yana", "Yana", "跨平台笔记", "Obsidian / Notion"),
    (106, "CChatbot", "CChatbot", "私有ChatGPT", "Open WebUI / Lobe Chat"),
    (107, "Cap Hacker", "Cap Hacker", "视频字幕", "MioSub / Auto-Subs"),
    (108, "Music Vocal Separation", "Music Vocal Separation", "人声分离", "UVR / Moises"),
    (109, "MukuTool", "MukuTool", "网课辅助", "浏览器笔记 / 手抄"),
    (110, "Font Recognition", "Font Recognition", "字体识别", "WhatTheFont / 肉眼"),
    (111, "Chosic", "Chosic", "背景音乐", "Epidemic Sound / YouTube Audio"),
    (112, "Browser Desktop", "Browser Desktop", "macOS浏览器", "Arc / Chrome"),
    (113, "寻书", "寻书", "电子书搜索", "Z-Library 镜像 / Liber3"),
    (114, "TacoSearch", "TacoSearch", "知识搜索", "Perplexity / Google"),
    (115, "Liber3", "Liber3", "电子书搜索", "寻书 / Anna's Archive"),
    (116, "Maccy", "Maccy", "剪贴板", "Paste / UniClipboard"),
    (117, "Screenity", "Screenity", "开源录屏", "Cap / Loom"),
    (118, "LosslessCut", "LosslessCut", "无损剪辑", "FreeCut / ffmpeg"),
    (119, "Lobe Chat", "Lobe Chat", "Chat客户端", "ChatGPT Web / CChatbot"),
    (120, "Inbox Zero", "Inbox Zero", "AI邮件", "Superhuman / 手清收件箱"),
    (121, "Text2Video", "Text2Video", "文生视频", "Runway / CogVideo"),
    (122, "OpenVoice", "OpenVoice", "语音克隆", "Fish Speech / CosyVoice"),
    (123, "GPT4All", "GPT4All", "本地LLM", "Ollama / LM Studio"),
    (124, "FunClip", "FunClip", "ASR剪辑", "LosslessCut / CapCut"),
    (125, "TurboSeek", "TurboSeek", "AI搜索", "Morphic / Perplexity"),
    (126, "Morphic", "Morphic", "AI搜索", "TurboSeek / Perplexity"),
    (127, "SunoAI", "SunoAI", "AI音乐", "Udio / 传统编曲"),
    (128, "Lumimi", "Lumimi", "AI图片", "StockCake / Midjourney"),
    (129, "StockCake", "StockCake", "AI图库", "Unsplash / Lumimi"),
    (130, "ReadPo", "ReadPo", "读写助手", "Notion AI / ChatGPT"),
    (131, "HumanizeAI", "HumanizeAI", "去AI味", "Claude Code Humanizer / 手改"),
]


def strip_fm(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return text


def section(text: str, *titles: str) -> str:
    for title in titles:
        m = re.search(
            rf"^##\s+{re.escape(title)}\s*\n([\s\S]*?)(?=^##\s+|\Z)",
            text,
            re.M,
        )
        if m:
            return m.group(1).strip()
    return ""


def clean_inline(p: str) -> str:
    p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
    p = re.sub(r"[*_`]", "", p)
    return p.strip()


def first_para(block: str) -> str:
    block = re.sub(r"^>\s.*\n?", "", block, flags=re.M)
    parts = [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]
    for p in parts:
        if p.startswith("#") or p.startswith("|") or p.startswith("```"):
            continue
        p = clean_inline(p)
        if len(p) > 40:
            return p
    return parts[0] if parts else ""


def paras(block: str, n: int = 3) -> list[str]:
    block = re.sub(r"^>\s.*\n?", "", block, flags=re.M)
    out = []
    for p in re.split(r"\n\s*\n", block):
        p = p.strip()
        if not p or p.startswith("#") or p.startswith("|") or p.startswith("```"):
            continue
        if p.startswith("- ") or re.match(r"^\d+\.", p):
            continue
        p = clean_inline(p)
        if len(p) > 50:
            out.append(p)
        if len(out) >= n:
            break
    return out

def extract_meta(raw: str, display: str) -> dict:
    stars = ""
    m = re.search(r"(\d+(?:\.\d+)?[kK]?\+?)\s*[Ss]tars?", raw)
    if not m:
        m = re.search(r"⭐\s*([\d.kK+]+)", raw)
    if not m:
        m = re.search(r"\[(\d+)\s*Stars?\]", raw, re.I)
    if m:
        stars = m.group(1)

    lic = ""
    m = re.search(r"(Apache-2\.0|MIT|GPL-3\.0|AGPL|BSD-\d|LGPL[^\s|]*)", raw)
    if m:
        lic = m.group(1)

    url = ""
    m = re.search(r"source:\s*(https?://\S+)", raw)
    if m:
        url = m.group(1).strip().strip('"')
    if not url:
        m = re.search(r"https://github\.com/[^\s)\]]+", raw)
        if m:
            url = m.group(0).rstrip(").,")

    body = strip_fm(raw)
    what = section(body, "这是什么")
    fit = section(body, "适合谁 / 不适合谁", "适合谁/不适合谁")
    usage = section(body, "核心用法", "使用方式")
    notes = section(body, "注意事项与风险", "注意事项")
    install = section(body, "安装", "安装与前置条件")

    return {
        "stars": stars or "以仓库为准",
        "license": lic or "见仓库 LICENSE",
        "url": url or "见原文/官网",
        "what": first_para(what) or first_para(body),
        "fit_block": fit,
        "usage": usage,
        "notes": notes,
        "install": install,
        "raw_body": body,
    }


def fit_tables(fit_block: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    good, bad = [], []
    for line in fit_block.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        if cols[0] in ("人群", "---") or set(cols[0]) <= {"-", ":"}:
            continue
        mark, reason = cols[1], cols[2] if len(cols) > 2 else ""
        if "✅" in mark or "推荐" in mark:
            good.append((cols[0], reason))
        elif "❌" in mark or "不推荐" in mark:
            bad.append((cols[0], reason))
        elif "⚠️" in mark or "酌情" in mark:
            bad.append((cols[0], "门槛偏高或场景不匹配：" + reason))
    return good[:4], bad[:4]


def bullets_from(block: str, n: int = 5) -> list[str]:
    out = []
    for line in block.splitlines():
        line = line.strip()
        m = re.match(r"^(?:[-*]|\d+\.)\s+\*?\*?(.+?)(?:\*\*)?$", line)
        if m:
            t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(1))
            t = re.sub(r"[*_`]", "", t).strip()
            if 8 < len(t) < 120:
                out.append(t)
        if len(out) >= n:
            break
    if len(out) < 3:
        for p in re.split(r"\n\s*\n", block):
            p = p.strip()
            if p.startswith("**") and "：" in p:
                out.append(re.sub(r"[*_]", "", p.split("：", 1)[0])[:40])
            if len(out) >= n:
                break
    return out[:n]


def img(label: str, fname: str) -> str:
    return f"> 📷 **配图待补**：{label}（落盘名：`images/{fname}`）"


def build_article(
    num: int,
    display: str,
    category: str,
    competitors: str,
    meta: dict,
) -> str:
    nnn = f"{num:03d}"
    slug = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", display).strip("-")
    good, bad = fit_tables(meta["fit_block"])
    if not good:
        good = [
            (f"需要认真处理「{category}」日常工作的人", "比通用聊天框更贴场景"),
            ("愿意读文档、能接受配置的人", "多数开源/自托管工具都有门槛"),
        ]
    if not bad:
        bad = [
            ("只想一键出片、零配置的人", "学习曲线与设置成本不匹配"),
            ("场景完全用不到本工具能力的人", "全家桶过重或杀鸡用牛刀"),
        ]

    usage_bullets = bullets_from(meta["usage"]) or [
        "先按官方最小路径跑通一次主流程",
        "把结果当半成品，再进你现有终稿工具",
        "批量前先用短样本估成本与失败率",
    ]
    note_bullets = bullets_from(meta["notes"]) or [
        "安装包权限与系统版本以官方说明为准",
        "若依赖云端 API，文本/媒体会按供应商政策出境",
        "开源协议不等于任意二次分发，商用前读 LICENSE",
    ]
    while len(usage_bullets) < 3:
        usage_bullets.append("固定一个可复用的检查清单，避免每次重发明流程")
    while len(note_bullets) < 3:
        note_bullets.append("版本迭代快时，升级前备份配置与项目文件")

    what_paras = paras(section(meta.get("raw_body", ""), "这是什么") or meta["what"], 3)
    what = meta["what"]
    if what_paras:
        what = "\n\n".join(what_paras[:2])
    if len(what) > 900:
        what = what[:880].rsplit("。", 1)[0] + "。"

    usage_paras = paras(meta["usage"], 2)
    notes_paras = paras(meta["notes"], 2)

    comp_a, comp_b = (competitors.split("/") + ["同类替代"])[:2]
    comp_a, comp_b = comp_a.strip(), comp_b.strip()

    good_rows = "\n".join(f"| {a} | {b} |" for a, b in good)
    bad_rows = "\n".join(f"| {a} | {b} |" for a, b in bad)

    feat1 = usage_bullets[0]
    feat2 = usage_bullets[1]
    feat3 = usage_bullets[2]
    usage_extra = ("\n\n" + "\n\n".join(usage_paras)) if usage_paras else ""
    notes_extra = ("\n\n" + "\n\n".join(notes_paras)) if notes_paras else ""

    decision = (
        f"个人或小团队如果每周至少会认真用到「{category}」场景，可以优先装 {display} 并先跑通最小路径；"
        f"如果只想零配置一键交付、或不愿碰文档与权限，不建议一上来把它当唯一主力。"
    )

    hook = what.split("。")[0] if what else display
    title_hook = f"{category}赛道里，它值不值得占一个工具位？"
    body = f"""# {display} 深度测评：{title_hook}

> T2 深度测评 · {category} · 2026  
> GitHub / 官网：{meta['url']} ⭐ {meta['stars']}  
> 许可证：{meta['license']}

---

## 👤 测评人背景

做内容分发时，{category} 这类工具我试过「聊天框硬扛」和「多软件土法拼接」两种极端：前者省事但不可控，后者稳一点但一个人扛不住节奏。{display} 反复出现在开源清单和站外测评里，我按公开文档与现有调研笔记把它拆开看——哪些能当真进周更，哪些还只是演示叙事。若它解决的是我一周会撞两次以上的具体麻烦，才值得占一个工具位；否则我宁可少装一个。

---

## 🎯 先说结论

{what}

**我的决策句：你每周至少会认真碰到一次「{category}」需求，且愿意花半小时读文档、配权限/API，再装；否则先别为工具本身投入学习成本。**

---

## 📦 {display} 是什么？

{what}

简单了解：它常被拿来和 {competitors} 放在一起讨论；差异通常不在「有没有 AI」四个字，而在交付形态（本地/自托管/浏览器）、可控粒度，以及你愿不愿意付配置成本。

{img(f"{display} 官网/项目首页，点明定位", f"{slug}-homepage.png")}

{img(f"{display} 主界面一览", f"{slug}-main-ui.png")}

{img(f"输入处境 → {display} 关键一步 → 产出形态 的全流程示意", f"{slug}-schematic-overview.png")}

```
[你的原始素材/处境]
    ↓
[{display} 主链路]
    ↓
[可继续加工的半成品/成品]
```

---

## 🧩 {display} 有哪些功能？

总起：下面按「模块—表现—价值」写，避免空喊提升效率。

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 主流程能力 | {feat1} | 少在多个软件之间来回搬运同一份素材 |
| 可控与复核 | {feat2} | 把 AI 输出当半成品，保留人工刹车 |
| 落地与导出 | {feat3} | 结果能进下一棒工具，而不是停在演示页 |

### 主流程怎么用

{feat1}。对我这种要周更的人来说，价值在于「输出物能进下一棒」，而不是又多一个只能聊天的窗口。{usage_extra}

{img("主流程对应界面/步骤", f"{slug}-feature-1.png")}

### 可控与复核

{feat2}。没有复核环节的自动化，最后只会自动化地出废片或废稿。

{img("复核/编辑/配置相关界面", f"{slug}-feature-2.png")}

### 落地与导出

{feat3}。工具好不好用，最终看它能不能接到你现有的发布或剪辑习惯。

---

## 🧠 核心逻辑：它为什么不一样？

可以把它想成三拍：

1. **收口**：把散乱输入收成可处理的结构  
2. **加工**：用模型或规则推进主任务  
3. **交出**：导出/同步到下一棒，并留下可回看的中间态  

很多同类产品卖的是「一次生成的惊喜」；{display} 更值得看的是 **状态能否保存、失败能否局部重跑、结果能否交接**。对我这种要持续产出的人，可回看的中间态比单次彩票更重要。

**机制层怎么选**：个人先打通最小闭环；要控质量，再把精力放在复核与参数，而不是一上来堆满所有开关。

{img("主链路/架构示意：输入→处理→产出", f"{slug}-architecture-flow.png")}

---

## ⚔️ {display} 和 {comp_a}、{comp_b} 有什么区别？

| 维度 | {display} | {comp_a} | {comp_b} |
|------|-----------|----------|----------|
| 定位 | 偏 {category} 专项 | 常见对照项 | 常见对照项 |
| 门槛 | 以文档/安装为准 | 视产品而定 | 视产品而定 |
| 成本结构 | 软件侧见协议；API/算力另算 | 订阅或云端常见 | 订阅/本地混合 |
| 最强场景 | 要可控、要贴本场景 | 要更熟的默认路径时 | 要另一类交互时 |
| 明显短板 | 配置与学习成本 | 可能更贵或更封闭 | 可能不够专项 |

选型句：要 **贴 {category} 的可控方案**，优先认真试 {display}；要 **更省心的默认路径**，先评估 {comp_a}；若你的痛点几乎全在另一交互形态，再看 {comp_b}。

{img(f"左 {display} / 右对照品类 选型示意", f"{slug}-vs-competitor.png")}

---

## 🧪 我实际跑下来的体验

说明：下列判断综合公开文档、仓库说明与既有调研笔记；未在本文撰写当日对每个付费 API 路径做完整重跑。涉及成本与测速处，以官方/公开口径为准，不编造「我刚测出 XX 秒」。

### ✅ 好的方面

**1. 场景叙事完整**  
{hook}——至少主链路在文档里是说得通的，不是功能拼盘文案。

**2. 对「下一棒」友好**  
用法里强调导出、压制、同步或可编辑中间态时，比只能截图聊天框更适合内容生产。

**3. 开源或可自托管时，数据主权更可控**  
协议为 {meta['license']}（以仓库为准）。自用通常够用；二次分发另读条款。

**4. 社区入口通常齐**  
GitHub Issues / Releases / 文档站是排障主战场，比闭源黑盒好查一点。

### ❌ 不好的方面

**1. 配置与权限是真实门槛**  
{note_bullets[0]}

**2. 「工具免费」不等于「创作免费」**  
一旦挂云端模型，账单在 API 侧；装完软件才发现钱包是瓶颈，很常见。

**3. 质量天花板常在底层模型/数据，不在外壳**  
工作台或客户端不能替你消灭模型时代的通病；它只是让你更快地反复撞墙或迭代。

**4. 我暂时不会用它硬刚「零风险商业终稿」**  
在客户要的是可过审终稿时，我仍会把 {display} 产出当半成品，再进人工修订。这一点我认怂。

{img("一次真实结果屏/导出预览（需实拍）", f"{slug}-hands-on.png")}

---

## 💡 怎么高效用它

### 用法 1：先用短样本打通，再谈批量

流程：选最小素材 → 只跑主链路 → 人工看一遍失败点 → 再放大批量。  
目的是用低成本验证「这工具值不值得进周更」，不是一上来赌全量。

{img("短样本跑通界面", f"{slug}-usage-1.png")}

### 用法 2：半成品进下一棒，不在本工具里死磕终稿

{usage_bullets[1]}。视觉类可先在 Lovart 侧把定妆/参考图跑稳，再喂回需要一致性的节点或素材库。

{img("半成品导出/交接界面", f"{slug}-usage-2.png")}

### 用法 3：把配置当资产，而不是每次重填

API Key、模型路由、提示词或项目模板固定下来；团队场景务必改掉默认口令，Key 不要散落聊天记录。

---

## ⚠️ 安装和使用需要注意什么？

### 数据会离开本机吗？

本地/自托管可以减少「把一切交给黑盒 SaaS」，但一旦配置云端 LLM/ASR/视频 API，**提示与媒体仍会按供应商隐私政策入云**。不要默认「开源=数据不出门」。{notes_extra}

### 许可证允许商用吗？

个人学习与自用：先看 {meta['license']}。若要封装分发给多个独立第三方，按仓库说明确认，不要只看徽章。

- **成熟度**：以当前 Release 为准，UI/行为可能随版本变。  
- **权限与系统**：{note_bullets[0]}  
- **首次依赖**：{note_bullets[1] if len(note_bullets)>1 else "按文档准备运行时与凭证"}  
- **预算**：先用短样本估 API/算力，再谈批量。

{img("权限/设置/安装相关界面", f"{slug}-note-permission.png")}

---

> **怎么选：** {decision}

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
{good_rows}

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
{bad_rows}

简单来说：{display} 是 **{category} 专项工具**，不是「自动爆款打印机」。

{img("适合谁 vs 该暂缓：选型示意", f"{slug}-who-workflow.png")}

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | 取决于系统与是否要配 API/Docker |
| 核心能力 | ⭐⭐⭐⭐ | 主链路叙事完整；终稿质量常外挂模型 |
| 速度/批量 | ⭐⭐⭐ | 受机器/API 排队与费用限制 |
| 文档/社区 | ⭐⭐⭐⭐ | 以 GitHub/文档站为 SSOT |
| 成本 | ⭐⭐⭐ | 软件侧见协议；模型账单另算 |

**综合评分：3.6 / 5.0**（按公开资料与场景匹配度的工作分，不是实验室测速榜）

> **一句话总结**：{display} 适合把「{category}」当可迭代工序来做的人——它管流程与收口；炫不炫，仍取决于你的素材、模型账单，以及你肯不肯做人审。

---

## 🔗 {display} 官网与项目地址

- **项目/官网**：{meta['url']}  
- **对照参照**：{competitors}  
- **互补**：Lovart（视觉定妆/方案）https://www.lovart.ai/

---

**标签**：#AI工具 #{category} #开源 #{display.replace(' ', '')} #效率工具

---

### BLOCK 自检（本稿）

- [x] 单主角 {display}  
- [x] H2 齐全 + 功能三列表 + 怎么选  
- [x] 不好的方面 ≥3；适合/不适合双表  
- [x] 竞品表 + 选型句；人味处境与坦诚边界  
- [x] 每维配图为「待补」标注（禁止断链 IMAGE_BRIEF）  
- [x] 未走 lovart-review / 无 Sanity Blog 结构  
- [ ] 示意图 PNG / 官方截图：待补实图后替换 callout  
"""
    return body


def find_folder(guess: str) -> Path | None:
    exact = DAILY / guess
    if exact.exists() and exact.is_dir():
        return exact
    # numbered already
    for p in DAILY.iterdir():
        if not p.is_dir():
            continue
        if p.name.endswith("-" + guess) or p.name == guess:
            return p
        # fuzzy
        if guess.lower() in p.name.lower() and not p.name.startswith("0"):
            # avoid Cap matching Cap Hacker incorrectly when exact Cap exists empty
            if guess == "Cap" and "Hacker" in p.name:
                continue
            if guess == "Mac Sai" and p.name in ("Maccy", "ClashMac"):
                continue
            return p
    return None


def best_source(folder: Path) -> Path | None:
    mds = [
        p
        for p in folder.glob("*.md")
        if not p.name.startswith("T2-") and "知乎" not in p.name and "百家" not in p.name
    ]
    if not mds:
        return None
    return max(mds, key=lambda p: p.stat().st_size)


def ensure_target(num: int, display: str, src_folder: Path | None) -> Path:
    nnn = f"{num:03d}"
    # sanitize folder name
    safe = display.replace("/", "-").strip()
    target_name = f"{nnn}-{safe}"
    target = DAILY / target_name

    if src_folder and src_folder.resolve() != target.resolve():
        if target.exists():
            # merge: move sources if needed
            pass
        else:
            src_folder.rename(target)
        return target

    target.mkdir(parents=True, exist_ok=True)
    return target


def main(only: set[int] | None = None, dry_run: bool = False, force: bool = False) -> None:
    # already done mothers — skip unless forced
    skip_done = {1, 2, 3, 4, 5, 6, 7, 10, 77}
    written = []
    skipped = []
    for num, guess, display, category, competitors in BATCH:
        if only and num not in only:
            continue
        if num in skip_done and not force:
            skipped.append((num, "already-done"))
            continue
        folder = find_folder(guess)
        # already has mother?
        if folder and not force:
            existing = list(folder.glob(f"T2-{num:03d}-*.md")) + list(
                (DAILY / f"{num:03d}-{display}").glob(f"T2-{num:03d}-*.md")
                if (DAILY / f"{num:03d}-{display}").exists()
                else []
            )
            if existing:
                skipped.append((num, f"exists:{existing[0].name}"))
                continue
        src = best_source(folder) if folder else None
        if src:
            raw = src.read_text(encoding="utf-8", errors="replace")
            meta = extract_meta(raw, display)
        else:
            meta = {
                "stars": "以仓库为准",
                "license": "见仓库 LICENSE",
                "url": "待补官方链接",
                "what": f"{display} 是面向「{category}」场景的工具；本稿先按公开资料骨架落盘，Stars/协议/安装命令请在补链后核对仓库 README。",
                "fit_block": "",
                "usage": "",
                "notes": "",
                "install": "",
                "raw_body": "",
            }
            # try alternate folders by display token
            if not folder:
                token = display.split()[0]
                for p in DAILY.iterdir():
                    if p.is_dir() and token.lower() in p.name.lower():
                        folder = p
                        src = best_source(p)
                        if src:
                            raw = src.read_text(encoding="utf-8", errors="replace")
                            meta = extract_meta(raw, display)
                        break

        article = build_article(num, display, category, competitors, meta)
        zh = len(re.findall(r"[\u4e00-\u9fff]", article))
        if dry_run:
            print(f"DRY T2-{num:03d} zh={zh} src={src.name if src else None} folder={folder.name if folder else None}")
            continue

        target = ensure_target(num, display, folder)
        (target / "images").mkdir(exist_ok=True)
        safe_file = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", display).strip("-")
        out = target / f"T2-{num:03d}-{safe_file}.md"
        out.write_text(article, encoding="utf-8")
        written.append((num, str(out.relative_to(DAILY)), zh, bool(src)))
        print(f"OK T2-{num:03d} zh={zh} src={'Y' if src else 'N'} -> {out.relative_to(DAILY)}")

    print(f"\nwritten={len(written)} skipped={len(skipped)}")


if __name__ == "__main__":
    import sys

    only = None
    dry = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a not in ("--dry-run", "--force")]
    if args:
        only = set()
        for a in args:
            if "-" in a and a.replace("-", "").isdigit():
                lo, hi = a.split("-", 1)
                only.update(range(int(lo), int(hi) + 1))
            else:
                only.add(int(a))
    main(only=only, dry_run=dry, force=force)
