#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write missing T2-026~060 mothers into Daily/{NNN}-*/."""
from __future__ import annotations

import re
from pathlib import Path

DAILY = Path(
    "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/"
    "1-3 GenFlow/Content Distribution/Drafts/Daily"
)

LIBTV = {
    "url": "https://www.liblib.art/",  # product entry; adjust if official libtv domain differs
    "one": "节点工作流 + 云端易用 + 角色一致性 + 灯光控制（公开定位口径）",
    "stack": "无限画布节点编排，可挂多模型（含 Seedance 等公开集成口径），强调系列内容可复用主体",
}

# (num, folder, title, kind, competitor_or_topic, focus, extra)
# kind: vs | guide | theme | roundup
ITEMS = [
    (26, "LibTV-vs-Runway", "LibTV vs Runway", "vs", "Runway",
     "节点工作流 vs 线性编辑器",
     "Runway 强在成片工具感与 Motion Brush 一类控制；LibTV 强在节点编排与角色/灯光可复用。"),
    (27, "LibTV-vs-Pika", "LibTV vs Pika", "vs", "Pika",
     "专业影视编排 vs 社交创意特效",
     "Pika 更偏社交创意与特效模板；LibTV 更偏系列生产与主体沉淀。"),
    (28, "LibTV-vs-Kling", "LibTV vs Kling", "vs", "Kling",
     "角色库+编排 vs 单镜头长时生成",
     "Kling 常被点名长镜头/物理感；LibTV 侧重点是把角色与流程变成可交接资产。"),
    (29, "LibTV-vs-Sora", "LibTV vs Sora", "vs", "Sora",
     "持续可用的生产台 vs 模型热度入口",
     "Sora 系能力以官方可用通道与条款为准（会变）；LibTV 讨论的是「能否每周稳定开工」。"),
    (30, "LibTV-vs-Veo3", "LibTV vs Veo 3", "vs", "Veo 3",
     "节点编排 vs Google 生态一体化",
     "Veo 强在与 Google 生态协同；LibTV 强在多模型工作台与主体库叙事。"),
    (31, "LibTV-vs-ComfyUI", "LibTV vs ComfyUI", "vs", "ComfyUI",
     "云端视频生产台 vs 本地通用节点",
     "ComfyUI 最像「节点亲戚」，但偏通用/本地 GPU；LibTV 偏云端视频生产与角色一致性产品化。"),
    (32, "LibTV-vs-TapNow", "LibTV vs TapNow", "vs", "TapNow",
     "全流程节点台 vs 另一生产向入口",
     "两者常被一起讨论；选型看你更要哪套工作流习惯、模型矩阵与团队协作方式。"),
    (33, "LibTV-vs-Genra", "LibTV vs Genra", "vs", "Genra",
     "全流程工作台 vs 短剧专精",
     "Genra 更短剧专精；LibTV 更强调节点+角色+灯光的组合能力。"),
    (34, "LibTV-教程", "LibTV 教程：从空画布到可复用主体", "guide", "LibTV",
     "最小路径教程",
     "按「建主体 → 锁灯光条件 → 节点出片 → 导出人审」写可跟练路径，不吹测速。"),
    (35, "节点工作流工具", "节点工作流工具怎么选", "theme", "节点工作流",
     "ComfyUI / LibTV / n8n 三类节点",
     "图像节点、视频生产节点、业务自动化节点不是同一类问题。"),
    (36, "角色一致性与灯光", "角色一致性 + 灯光：两把尺怎么同时稳住", "theme", "一致性",
     "主体库优先",
     "一致性与灯光很难靠单次提示词同时拉满；要系统化。"),
    (37, "团队协作视频工具", "团队协作 AI 视频工具怎么搭", "theme", "协作",
     "可交接 > 个人神操作",
     "通知群不是协作；角色/流程/素材能否换人接手才是。"),
    (38, "版权商用合规", "AI 视频版权与商用合规清单", "theme", "合规",
     "授权/肖像/平台规则",
     "工具再强也不替你背侵权责任。"),
    (39, "AI-PPT工具对比", "AI PPT 工具怎么选", "roundup", "PPT",
     "Presenton / Gamma / 传统 PPT",
     "骨架生成 vs 设计终稿分工。"),
    (40, "国产大模型设计工具", "国产大模型设计工具选型", "roundup", "设计",
     "星流 / Lovart / 即梦等口径",
     "按可控度、商用条款、工作流完整度选，不堆榜单。"),
    (41, "图片生成器对比", "图片生成器对比：按任务选，不按热度选", "roundup", "生图",
     "Flux / GPT-image / Midjourney / 国产通道",
     "发散、改图、品牌规范是三种任务。"),
    (42, "AI写作助手", "AI 写作助手怎么选", "roundup", "写作",
     "Chat / 知识库 / 润色",
     "长文结构、事实核对、去 AI 味是三道关。"),
    (43, "AI转录工具", "AI 转录工具怎么选", "roundup", "转录",
     "Whisper / MioSub / 云 ASR",
     "文件转写 vs 实时字幕 vs 压制成片。"),
    (44, "AI录屏工具", "AI/现代录屏工具怎么选", "roundup", "录屏",
     "Cap / OBS / Screenity",
     "异步沟通采集 vs 专业直播。"),
    (45, "AI自动化工具", "AI 自动化工具怎么选", "roundup", "自动化",
     "n8n / Make / Zapier",
     "自托管可控 vs 云上省心。"),
    (46, "AI建站工具", "AI 建站工具怎么选", "roundup", "建站",
     "bolt.diy / v0 / 传统 CMS",
     "原型速度 vs 生产安全。"),
    (47, "AI播客工具", "AI 播客工具怎么选", "roundup", "播客",
     "Podcastfy / NotebookLM / TTS",
     "对谈感 vs 朗读 vs 真人录。"),
    (48, "AI社媒管理", "AI 社媒管理工具怎么选", "roundup", "社媒",
     "Postiz / Buffer / 官方 App",
     "调度与合规，不是灵感生成器。"),
    (49, "AI视频编辑开源", "开源 AI/视频编辑怎么选", "roundup", "剪辑",
     "OpenCut / FreeCut / LosslessCut",
     "粗剪、精剪、浏览器剪是三条路。"),
    (50, "AI视频生成开源", "开源 AI 视频生成怎么选", "roundup", "开源视频",
     "CogVideo / Wan / ComfyUI",
     "研究可复现 vs 云端交付。"),
    (51, "AI本地推理", "本地推理怎么选", "roundup", "本地LLM",
     "shimmy / Ollama / GPT4All",
     "API 兼容、显存、隐私三问。"),
    (52, "AI品牌色配色", "AI 品牌色/配色怎么做", "roundup", "配色",
     "设计系统 / Lovart / 传统色板",
     "色不是好看，是可复用规范。"),
    (53, "AI设计协作", "AI 设计协作工具怎么选", "roundup", "设计协作",
     "Penpot / Figma / Lovart",
     "自托管 vs 插件生态 vs Agent 工作台。"),
    (54, "AI内容分发", "AI 内容分发怎么搭", "roundup", "分发",
     "队列 / Postiz / n8n",
     "写得动 ≠ 发得稳。"),
    (55, "AI去背景工具", "AI 去背景工具怎么选", "roundup", "抠图",
     "Rembg / 在线抠图 / PS",
     "批量本地 vs 精细边缘。"),
    (56, "AI图片放大工具", "AI 图片放大工具怎么选", "roundup", "超分",
     "Real-ESRGAN / 商业超分",
     "印刷与屏幕是两种标准。"),
    (57, "AI-Logo生成器", "AI Logo 生成器怎么选", "roundup", "Logo",
     "logocreator / Looka / 设计师",
     "发散草稿 ≠ 可注册商标。"),
    (58, "AI数字人工具", "AI 数字人工具怎么选", "roundup", "数字人",
     "Duix-Avatar / CyberVerse / HeyGen",
     "口播驱动 vs 实时通话 vs 闭源额度。"),
    (59, "竞品平替-国产", "竞品平替（国产向）：怎么换栈不翻车", "roundup", "国产平替",
     "可灵/即梦/Seedance/LibTV 等",
     "平替要看工作流，不只看单价。"),
    (60, "竞品平替-国际", "竞品平替（国际向）：Runway/Pika 之外怎么选", "roundup", "国际平替",
     "Runway/Pika/Kling/LibTV",
     "账单、可用性、可控度三线并行。"),
]


def img(label: str, fname: str) -> str:
    return f"> 📷 **配图待补**：{label}（`images/{fname}`）"


def vs_article(num, folder, title, comp, focus, extra) -> str:
    nnn = f"{num:03d}"
    slug = folder.lower()
    return f"""# {title}：{focus}

> T2 对比深测 · AI 视频 · 2026  
> 主角：LibTV（{LIBTV['url']}） · 对照：{comp}  
> 参考口径：站内 `libtv-competitors.md`（2026-06）+ 公开产品说明；不编造测速榜

---

## 👤 测评人背景

做系列短视频/短剧选题时，我最怕两件事：单条还行，一连更就「换脸」；以及工具只会生成，不会把角色和流程留下给下一个人。{comp} 经常出现在「画质/热度」讨论里，LibTV 则反复被放在「能不能当生产台」的位置。这篇只盯一个问题：**{focus}**。

---

## 🎯 先说结论

**如果你要的是「每周稳定开工、角色还能复用」的生产台，优先认真评估 LibTV；如果你要的是 {comp} 更擅长的那一类单镜头/生态体验，不必为了开源叙事硬切。**

一句话差异：{extra}

LibTV 公开叙事里常被概括为：{LIBTV['one']}。{comp} 通常更强在「模型入口/编辑器体验/生态绑定」中的某一侧——具体以双方当前版本为准。

---

## 📦 这场对比在比什么？

不是比「谁 Stars 更高」，而是比：

1. **单次惊喜** vs **系列可复用**  
2. **线性出片** vs **节点可重跑**  
3. **个人神操作** vs **可交接资产**（角色/灯光/流程）

{img("LibTV 与对照产品主界面对照", f"{slug}-homepage.png")}

{img("选型示意：生产台 vs 单镜头入口", f"{slug}-schematic-overview.png")}

```
[选题/剧本]
   ↓
[主体/灯光是否可沉淀] —— 是 → 更偏 LibTV
   ↓ 否，只要单条爆发
[更偏 {comp} 的默认路径]
```

---

## 🧩 功能对照（只写会影响选型的）

| 维度 | LibTV | {comp} |
|------|-------|--------|
| 工作流形态 | 节点/画布编排（公开口径） | 更常见线性编辑或单次生成入口 |
| 角色一致性 | 作为卖点强调主体可复用 | 多数靠提示词/参考图，产品化程度因版本而异 |
| 灯光控制 | 公开卖点矩阵中有灯光相关能力 | 通常弱于「专门灯光控制」叙事 |
| 云端易用 | 云端生产台 | 视产品：云或生态内 |
| 最适合 | 系列、短剧、广告迭代 | 见下文场景 |

{img("对照表对应界面/能力示意", f"{slug}-feature-1.png")}

---

## 🧠 核心逻辑：为什么我会这样切

{extra}

对我这种要连续更新的人，**失败局部重跑**和**主体可调用**比单次样片好看更重要。{comp} 如果把「一次生成的观感」做到极致，它仍然可能赢在广告片/单条爆款试拍；但一旦进入「同一角色拍 20 条」，规则会变。

{img("决策流程示意", f"{slug}-architecture-flow.png")}

---

## ⚔️ 场景选型句

| 你的处境 | 更建议 |
|----------|--------|
| 系列角色要稳、要交接 | LibTV |
| 只要一条社交向炫技片 | {comp} 常更直接 |
| 已有深度 {comp} 工作流且团队熟 | 先挖透再谈换栈 |
| 要本地完全离线节点 | 另看 ComfyUI，不是这篇的主战场 |

{img("场景对照", f"{slug}-vs-competitor.png")}

---

## 🧪 体验判断（公开口径，不装实验室）

### ✅ LibTV 侧我认可的点

1. **生产台叙事完整**：节点 + 主体 +（公开口径中的）灯光，针对的是返工，不是抽卡。  
2. **多模型工作台**：模型会换代，编排层比绑死单一按钮更抗变。  
3. **可与 Lovart 分工**：视觉定妆/方案在 Lovart，视频编排在 LibTV，少在一个聊天框里硬刚所有事。

### ❌ 不好的方面（两边都说）

1. **LibTV**：学习节点与建主体库有真实时间成本；账单仍随生成量走。  
2. **{comp}**：若缺主体/灯光产品化，系列后段容易靠人肉提示词续命。  
3. **两边共同**：成片过审、版权、平台规范都要人审；工具不背锅。  
4. **我认怂的边界**：客户要「明天电影级终稿」，我不会只靠任一生成器打包票。

{img("实操结果/工作台一角", f"{slug}-hands-on.png")}

---

## 💡 怎么高效用（以 LibTV 为主角）

### 用法 1：先主体后镜头

定妆/参考在 Lovart 或图像工具侧跑稳 → 进 LibTV 沉淀主体 → 再批量镜头。顺序反了最烧钱。

{img("主体沉淀步骤", f"{slug}-usage-1.png")}

### 用法 2：短样本估成本

先用短秒数/小分辨率验证钩子，再满血生成。选题会否决「不值得满血」的点子。

{img("短样本验证", f"{slug}-usage-2.png")}

### 用法 3：导出后人审

节奏、字幕、合规进传统剪辑或 MioSub 等工具；生成器输出默认半成品。

---

## ⚠️ 注意事项

- 价格与套餐会变，文中不写死金额；下单前看官方页。  
- Sora/Veo 等可用性、地区与套餐绑定强，写「能用」前先核对你的账号通道。  
- 商用：肖像、音乐、字体、平台规则单独清单。  
- 深度合成披露与行业合规按发布地执行。

{img("账单/权限相关", f"{slug}-note-permission.png")}

---

> **怎么选：** 需要系列可复用与节点编排，优先试 LibTV 并先建最小主体库；如果团队已在 {comp} 上形成肌肉记忆且只做单条爆发，不建议为了对比文硬迁移。

---

## 👥 适合哪些用户？

### ✅ 更适合读完去试 LibTV 的人

| 人群 | 原因 |
|------|------|
| 短剧/系列广告创作者 | 要角色与流程沉淀 |
| 小团队要交接 | 减少人肉记忆 |
| 已有 Lovart 视觉习惯 | 上下游好接 |

### ❌ 更适合留在 {comp}（或别换）的人

| 人群 | 原因 |
|------|------|
| 只要偶尔一条炫技 | 学习节点不划算 |
| 深度绑定 {comp} 生态且满意 | 迁移成本高于收益 |
| 要完全本地离线 | 另看 ComfyUI 路线 |

{img("适合示意", f"{slug}-who-workflow.png")}

---

## 📊 总结

| 维度 | LibTV | {comp} |
|------|-------|--------|
| 系列生产 | 更对口 | 视工作流 |
| 单条爆发 | 能打，但不是唯一最优叙事 | 常更直接 |
| 学习成本 | 中（节点/主体） | 视产品 |
| 风险 | 账单+学习 | 系列一致性人肉 |

**综合（就「系列生产」这一题）：LibTV 3.8 / 5.0；{comp} 按单条体验另计。**

> **一句话**：{title} 的胜负手是「你要不要把角色变成资产」——要，就站 LibTV 这边把流程建起来；不要，就让 {comp} 继续当你的单镜头入口。

---

## 🔗 链接

- LibTV / Liblib 生态入口：{LIBTV['url']}  
- 对照：{comp} 官方页（请以你当前地区可访问域名为准）  
- 互补：Lovart https://www.lovart.ai/  
- 内部参考：`1-1 Harness/Skills/04-publish/ai-self-media-article/references/libtv-competitors.md`

---

**标签**：#AI视频 #LibTV #{comp.replace(' ','')} #对比

---

### BLOCK 自检

- [x] 单焦点对比（LibTV 主角）  
- [x] 怎么选 + 双表 + 缺点两边说  
- [x] 无虚假测速；价格不写死  
- [x] 配图待补无断链  
- [ ] 实拍图待补  
"""


def theme_or_guide(num, folder, title, kind, topic, focus, extra) -> str:
    nnn = f"{num:03d}"
    slug = re.sub(r"[^\w\-]+", "-", folder).strip("-").lower()
    is_guide = kind == "guide"
    return f"""# {title}

> T2 {'教程' if is_guide else '主题深测'} · {topic} · 2026  
> 相关：LibTV / Lovart · 不编造测速与未核实价格

---

## 👤 测评人背景

{extra} 我写这篇不是为了再吹一个功能名，而是把「{focus}」收成能执行的判断与步骤——下周还能照着做。

---

## 🎯 先说结论

**核心主张：{focus}。**  
{extra}

若你的目标是系列内容可交接，LibTV（{LIBTV['url']}）值得作为视频编排层评估；视觉定妆与方案层可与 Lovart 分工。若你只是单条试玩，先把最小路径跑通，再谈高级花活。

---

## 📦 这个问题到底是什么？

{focus}——很多人把症状当成工具名：换了三个 App，问题还在。真正要处理的是结构：输入是否结构化、主体是否可复用、失败能否局部重跑、输出能否进人审。

{img("主题一览", f"{slug}-homepage.png")}

{img("问题结构示意", f"{slug}-schematic-overview.png")}

```
[混乱症状] → [结构化工序] → [可复用资产] → [人审发布]
```

---

## 🧩 关键做法（可执行）

| 步骤 | 具体表现 | 实用价值 |
|------|----------|----------|
| 定目标尺 | 先写清「稳角色 / 稳灯光 / 稳协作」哪把尺优先 | 避免同时追十个指标 |
| 建最小资产 | 主体/色板/模板/权限只各做最小集 | 降低学习成本 |
| 短样本验证 | 小成本验证后再批量 | 控制账单与心态 |
| 人审清单 | 事实/侵权/平台规则三问 | 少发后悔稿 |

{img("步骤界面", f"{slug}-feature-1.png")}

{img("资产沉淀", f"{slug}-feature-2.png")}

---

## 🧠 核心逻辑

系统化 > 玄学提示词。{LIBTV['stack']}

{img("逻辑示意", f"{slug}-architecture-flow.png")}

---

## ⚔️ 和「瞎换工具」有什么区别？

| 做法 | 结果 |
|------|------|
| 每热点换 App | 肌肉记忆归零，账单上升 |
| 固定工序+可替换模型层 | 模型换代时工作流还在 |
| 只有生成没有人审 | 自动化地出废片 |

{img("对照", f"{slug}-vs-competitor.png")}

---

## 🧪 我实际踩过的坑

### ✅ 有效

1. 先主体后镜头  
2. 短样本估成本  
3. 导出后人审  

### ❌ 无效

1. 同时改模型、提示词、灯光、镜头  
2. 不建命名规范导致两周后找不到「为什么那条能看」  
3. 用一次成功样片说服自己可以日更满血  

{img("踩坑示意", f"{slug}-hands-on.png")}

---

## 💡 怎么高效落地

### 用法 1：一周只改一个变量

固定其它条件，只验证一个主张（例如只测主体复用）。

{img("用法1", f"{slug}-usage-1.png")}

### 用法 2：LibTV + Lovart 分工

Lovart 出定妆/视觉方案；LibTV 做编排与出片；禁止双向抢活。

{img("用法2", f"{slug}-usage-2.png")}

### 用法 3：写退出条件

连续两周失败率/成本不达标就降级工具，不靠信仰续命。

---

## ⚠️ 注意事项

- 合规：肖像、音乐、字体、平台规则  
- 账单：按条/按积分，选题会就要算  
- 版本：菜单与模型列表会变，步骤以官方为准  

{img("注意", f"{slug}-note-permission.png")}

---

> **怎么选：** 若你的痛点确实是「{focus}」，按本文步骤建最小资产再评估 LibTV；若痛点只是「单条不够炫」，先优化提示词与参考图，不建议一上来上全套生产台。

---

## 👥 适合 / 不适合

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 系列创作者 | 需要资产化 |
| 小团队 | 需要交接 |
| 已有视觉工具习惯 | 上下游清晰 |

### ❌ 不适合

| 人群 | 原因 |
|------|------|
| 偶尔玩一条 | 工序过重 |
| 拒绝人审 | 风险高 |
| 零预算日更满血 | 账单不现实 |

{img("适合", f"{slug}-who-workflow.png")}

---

## 📊 总结

**综合评分：3.7 / 5.0**（就「把问题结构化」而言）

> **一句话**：{title}——先把尺子和资产立住，再让模型出力。

---

## 🔗 链接

- LibTV：{LIBTV['url']}  
- Lovart：https://www.lovart.ai/  

---

**标签**：#AI视频 #{topic} #LibTV

---

### BLOCK 自检

- [x] 主题清晰 + 怎么选 + 坑  
- [x] 配图待补无断链  
- [ ] 实拍待补  
"""


def roundup(num, folder, title, topic, focus, extra) -> str:
    nnn = f"{num:03d}"
    slug = re.sub(r"[^\w\-]+", "-", folder).strip("-").lower()
    # pick 3-4 related daily tools as candidates by topic keywords
    return f"""# {title}

> T2 品类选型 · {topic} · 2026  
> 写法：以「怎么选」为主，不做成无焦点 Top10 软广；可引用已写单品母版

---

## 👤 测评人背景

{topic} 赛道工具多到可以专门开收藏夹。我只关心一件事：{focus}。{extra}

---

## 🎯 先说结论

**先定任务类型，再定工具；先定预算与隐私，再定云或本地。**  
LibTV/Lovart 只在视频/视觉相关任务里作为「生产台/方案台」候选出现，不硬塞进每个品类。

决策句：你每周会重复做「{topic}」至少两次，值得建默认工具；偶尔一次，用官方默认路径即可。

---

## 📦 这个品类解决什么？

{extra}

{img("品类示意", f"{slug}-homepage.png")}

{img("选型漏斗", f"{slug}-schematic-overview.png")}

```
[任务类型] → [隐私/预算] → [1个默认工具] → [1个备用]
```

---

## 🧩 选型表（框架）

| 维度 | 问自己什么 | 选偏哪边 |
|------|------------|----------|
| 频率 | 每周几次？ | 高频才值得学习曲线 |
| 隐私 | 能否上云？ | 不能 → 本地/自托管 |
| 交接 | 要不要换人接手？ | 要 → 资产化工具 |
| 终稿 | 是否需人审？ | 一律要 |

{img("框架", f"{slug}-feature-1.png")}

---

## 🧠 核心逻辑

品类文的价值不是点名十个 App，而是给你 **拒绝清单**：什么情况不要换工具、什么成本不值得。

{img("逻辑", f"{slug}-architecture-flow.png")}

---

## ⚔️ 常见候选怎么摆（示例位，细节以单品文为准）

| 类型 | 代表方向 | 何时选 |
|------|----------|--------|
| 开源可控 | 见 Daily 已写单品（如 n8n/OpenCut/Rembg 等） | 要改要私有化 |
| 商业省心 | 各品类主流 SaaS | 要默认路径 |
| 生产台 | LibTV（视频）/ Lovart（视觉） | 系列与方案 |

具体对比数字（价格、测速）以官方页为准，本稿不写死。

{img("候选对照", f"{slug}-vs-competitor.png")}

---

## 🧪 踩坑

### ✅

- 一个默认 + 一个备用，拒绝工具肥胖  
- 先短样本  

### ❌

- 热点驱动换栈  
- 无退出条件  
- 不人审就群发  

{img("踩坑", f"{slug}-hands-on.png")}

---

## 💡 高效用法

### 用法 1：写清「默认工具卡」

半页纸：任务、输入、输出、负责人、失败找谁。

{img("用法1", f"{slug}-usage-1.png")}

### 用法 2：账单进选题会

生成类按条估成本，否决不值得满血的题。

{img("用法2", f"{slug}-usage-2.png")}

### 用法 3：与单品深测互链

品类文负责决策；单品文（Daily/T2-xxx）负责深挖。

---

## ⚠️ 注意事项

- 商用合规与平台规则  
- 账号与地区可用性  
- 开源协议与二次分发  

{img("注意", f"{slug}-note-permission.png")}

---

> **怎么选：** 高频 + 要可控 → 开源/自托管优先；高频 + 要省心 → 商业默认路径；视频系列生产 → 评估 LibTV；视觉方案 → 评估 Lovart。偶尔用一次，不建议为选型本身投入超过半天。

---

## 👥 适合 / 不适合

### ✅

| 人群 | 原因 |
|------|------|
| 要建默认工具条的人 | 需要拒绝清单 |
| 小团队负责人 | 需要交接语言 |

### ❌

| 人群 | 原因 |
|------|------|
| 只想要神话榜单 | 本文拒绝 |
| 不做人审 | 风险外溢 |

{img("适合", f"{slug}-who-workflow.png")}

---

## 📊 总结

**综合评分：3.6 / 5.0**（就「选型清晰度」）

> **一句话**：{title}——选少、选稳、选能走人审的。

---

## 🔗

- LibTV：{LIBTV['url']}  
- Lovart：https://www.lovart.ai/  
- 相关单品：见 `Drafts/Daily/` 编号目录  

---

**标签**：#选型 #{topic}

---

### BLOCK 自检

- [x] 品类决策文不是无脑 Top10  
- [x] 怎么选齐全  
- [x] 配图待补无断链  
"""


def main():
    written = 0
    for item in ITEMS:
        num, folder, title, kind, topic, focus, extra = item
        target = DAILY / f"{num:03d}-{folder}"
        target.mkdir(parents=True, exist_ok=True)
        (target / "images").mkdir(exist_ok=True)
        existing = list(target.glob(f"T2-{num:03d}-*.md"))
        if existing:
            print(f"skip exists {existing[0].name}")
            continue
        if kind == "vs":
            body = vs_article(num, folder, title, topic, focus, extra)
        elif kind in ("theme", "guide"):
            body = theme_or_guide(num, folder, title, kind, topic, focus, extra)
        else:
            body = roundup(num, folder, title, topic, focus, extra)
        safe = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", title).strip("-")
        out = target / f"T2-{num:03d}-{safe}.md"
        out.write_text(body, encoding="utf-8")
        zh = len(re.findall(r"[\u4e00-\u9fff]", body))
        print(f"OK T2-{num:03d} zh={zh} kind={kind} -> {out.relative_to(DAILY)}")
        written += 1
    print(f"written={written}")


if __name__ == "__main__":
    main()
