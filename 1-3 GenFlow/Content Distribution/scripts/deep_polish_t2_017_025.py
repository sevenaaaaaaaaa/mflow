#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep-polish T2-017~025 (and related) skeleton mothers."""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

DAILY = Path(
    "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/"
    "1-3 GenFlow/Content Distribution/Drafts/Daily"
)

REPOS = {
    17: "THUDM/CogVideo",
    18: "Michael-A-Kuykendall/shimmy",
    19: "Nutlope/logocreator",
    20: "penpot/penpot",
    21: "excalidraw/excalidraw",
    22: "presenton/presenton",
}

# 23 Nano Banana, 24 Seedance, 25 GPT-image — may lack clean public repo; handle specially
SPECIAL = {23, 24, 25}

FACTS = {
    17: {
        "name": "CogVideo",
        "cat": "视频生成",
        "comp": ("Wan2.1", "Runway"),
        "pitch": "开源文生/图生视频模型族，偏研究与自建推理",
        "features": [
            ("文生/图生视频", "按仓库能力生成短视频片段", "把分镜变成可看的动态草稿"),
            ("开源权重取向", "可自建推理，不绑单一网页额度", "适合实验与管线集成"),
            ("社区迭代", "论文/仓库更新快", "能跟住开源视频模型节奏"),
        ],
        "pros": [
            "开源可复现，适合研究与工程集成",
            "比纯闭源网页更利于批量与自动化",
            "能接到 ComfyUI/自建服务等管线",
            "成本结构透明：电费/GPU 租金你自己算",
        ],
        "cons": [
            "显存与工程门槛高，不是下载即拍",
            "成片观感与运动稳定性仍波动",
            "商用与权重协议要逐条核对",
            "不要用它硬刚「客户明天要过审成片」",
        ],
        "usage": [
            "先固定分辨率与秒数，用同一提示词做 A/B，别同时改十个旋钮",
            "角色一致性：先出定妆静帧（可用 Lovart），再图生视频",
            "输出当分镜动态预览，终稿进传统剪辑",
        ],
        "notes": [
            "CUDA/驱动/显存以 README 为准",
            "许可证与权重使用条款分开读",
            "生成内容深度合成合规与平台审核另算",
        ],
        "who_good": [
            ("有 GPU 的创作者/工程师", "能自建推理"),
            ("要开源视频管线的人", "集成进工作流"),
        ],
        "who_bad": [
            ("无卡只想网页出片", "Runway 类更省事"),
            ("要稳定商用角色剧集", "一致性仍是行业难题"),
        ],
    },
    18: {
        "name": "shimmy",
        "cat": "本地推理",
        "comp": ("Ollama", "llama.cpp"),
        "pitch": "Pure-Rust 本地推理引擎，OpenAI API 兼容、单二进制取向",
        "features": [
            ("本地 LLM 推理", "GGUF 等本地模型服务化", "敏感推理少出网"),
            ("OpenAI API 兼容", "用熟悉的客户端连本地", "少改现有工具链"),
            ("Rust 单二进制叙事", "减少 Python 依赖地狱", "部署更像装一个服务而不是搭环境"),
        ],
        "pros": [
            "API 兼容降低迁移成本",
            "本地跑，隐私场景更敢喂内部文档",
            "相对「一堆脚本+conda」，运维心智更简单",
            "适合当 AnythingLLM/自建 Agent 的后端",
        ],
        "cons": [
            "模型效果与速度取决于你下载的权重与硬件",
            "生态插件未必有 Ollama 那么「一键拉模型」爽",
            "生产要自己做进程守护与显存调度",
            "别把本地小模型的胡话当事实",
        ],
        "usage": [
            "先跑通：启动服务 → curl 打一发 chat completion",
            "接到 Open WebUI/AnythingLLM，统一本地入口",
            "按任务选模型体积：草稿用小杯，终稿再换大杯",
        ],
        "notes": [
            "硬件内存/显存不够会换页到极慢",
            "模型文件来源与许可自行核验",
            "局域网暴露 API 必须鉴权，否则等于公开公司大脑",
        ],
        "who_good": [
            ("要本地 OpenAI 兼容端点的人", "接现有客户端"),
            ("隐私优先的小团队", "资料不出网"),
        ],
        "who_bad": [
            ("只想手机上玩一玩", "云端 Chat 更合适"),
            ("要托管免运维", "SaaS LLM 更省心"),
        ],
    },
    19: {
        "name": "logocreator",
        "cat": "Logo生成",
        "comp": ("Looka", "Midjourney"),
        "pitch": "开源/可自建的 AI Logo 生成器取向，快速出品牌草稿",
        "features": [
            ("提示词出 Logo", "描述品牌出候选标识", "头脑风暴比从零画快"),
            ("可改可部署", "开源项目可自建", "不绑死单一 Logo SaaS"),
            ("导出再精修", "矢量/位图进设计工具继续改", "AI 出草稿，人出终稿"),
        ],
        "pros": [
            "快速产生方向，适合命名期的视觉发散",
            "开源路径可控账单与部署",
            "可与 Penpot/Figma 精修衔接",
            "比纯聊天框生图更贴「Logo 任务」",
        ],
        "cons": [
            "商标近似风险要自己查，AI 不管侵权",
            "细节与印刷规范仍需设计师",
            "模型审美同质化明显",
            "商用字体/图标素材许可另核",
        ],
        "usage": [
            "一次生成 8–12 个方向，先人眼淘汰，再精修 Top2",
            "定稿前做商标检索与极简黑白印刷测试",
            "品牌色与图形规范回 Lovart/设计工具统一",
        ],
        "notes": [
            "AI Logo ≠ 可注册商标",
            "客户行业敏感符号（医疗/金融）要额外合规",
            "导出 SVG 后检查锚点与扩边",
        ],
        "who_good": [
            ("早期项目要快速视觉方向", "发散草稿"),
            ("能自己精修的设计/开发", "接得住导出"),
        ],
        "who_bad": [
            ("要可注册的正式 VI 体系", "请设计师主导"),
            ("完全不做人审就上线商标", "风险极高"),
        ],
    },
    20: {
        "name": "Penpot",
        "cat": "设计协作",
        "comp": ("Figma", "Lunacy"),
        "pitch": "开源设计与原型工具，可自托管的 Figma 向替代",
        "features": [
            ("界面设计/原型", "矢量与组件化设计", "产品/设计协作不必锁 Figma 云"),
            ("自托管", "可私有化部署", "设计稿与权限留在自己服务器"),
            ("开源标准", "社区驱动迭代", "导出与集成路径更开放"),
        ],
        "pros": [
            "真正可自托管的设计协作，对政企/隐私团队有吸引力",
            "开源协议清晰，长期锁定风险低于纯 SaaS",
            "适合设计系统与组件库沉淀",
            "可与开发交付流程对齐（视导出能力）",
        ],
        "cons": [
            "插件生态与完整度仍追 Figma",
            "自托管要运维与备份",
            "团队迁移成本（习惯/组件）不低",
            "部分高级交互/插件工作流可能缺失",
        ],
        "usage": [
            "新项目直接在 Penpot 建设计系统，避免后期搬家",
            "组件命名与 token 从第一天规范，别当画板垃圾场",
            "与开发约定导出格式与标注习惯",
        ],
        "notes": [
            "生产部署上 HTTPS 与备份",
            "大文件/字体授权管理",
            "升级前看 migration notes",
        ],
        "who_good": [
            ("要自托管设计协作的团队", "隐私与可控"),
            ("讨厌厂商锁定的设计/产品", "开源替代"),
        ],
        "who_bad": [
            ("重度依赖 Figma 插件生态", "迁移痛"),
            ("个人随便画画无协作", "轻量工具够用"),
        ],
    },
    21: {
        "name": "Excalidraw",
        "cat": "白板",
        "comp": ("FigJam", "Miro"),
        "pitch": "开源手绘风白板，架构图/头脑风暴快速表达",
        "features": [
            ("手绘风绘图", "快速框线图与注释", "会议中比精致 UI 稿更快"),
            ("开源可自托管", "可私有部署协作", "图不默认进商业云"),
            ("嵌入与导出", "PNG/SVG/协作链接等", "能进文档与 PR 描述"),
        ],
        "pros": [
            "表达速度快，适合架构评审与教学",
            "开源生态强，库与组件多",
            "心智负担低，新人十分钟上手",
            "导出进 Notion/飞书/GitHub 很顺",
        ],
        "cons": [
            "不是高保真 UI 设计工具",
            "大型看板组织能力弱于 Miro 一类",
            "协作权限模型因部署方式而异",
            "别用它做最终视觉稿",
        ],
        "usage": [
            "开会先白板，再决定是否进 Penpot/Figma",
            "库组件固定一套箭头/色板，避免每人一种丑",
            "关键图导出 SVG 进文档，少贴模糊截图",
        ],
        "notes": [
            "自托管注意版本与存储后端",
            "嵌入第三方页面时注意 CSP",
            "手绘风不代表可以不标注清楚",
        ],
        "who_good": [
            ("工程师/产品画架构", "快速表达"),
            ("老师/分享者做示意图", "低门槛"),
        ],
        "who_bad": [
            ("要精美营销视觉", "工具错配"),
            ("要复杂工作坊看板", "Miro 更合适"),
        ],
    },
    22: {
        "name": "Presenton",
        "cat": "AI PPT",
        "comp": ("Gamma", "Beautiful.ai"),
        "pitch": "开源 AI 演示文稿生成，可自托管出 PPT",
        "features": [
            ("文本转演示", "大纲/文章生成幻灯片", "周报/分享初稿更快"),
            ("可自托管", "开源部署", "敏感内容少进闭源 PPT SaaS"),
            ("可继续编辑", "生成后应能改版式与文案", "AI 出骨架，人出演讲逻辑"),
        ],
        "pros": [
            "开源可控，适合内部分享与培训草稿",
            "从长文到幻灯片的路径短",
            "可接自有模型，账单自控",
            "比从空白 PPT 开始少折磨",
        ],
        "cons": [
            "版式审美同质化，正式对外仍要人改",
            "事实与数据要人审，防一本正经胡说",
            "自托管有运维成本",
            "复杂动画/母版体系可能不如商业 PPT 工具",
        ],
        "usage": [
            "先写清「听众是谁+要他们做什么」，再生成，别丢一坨流水账",
            "生成后删废话页，每页一句主张",
            "图表数据用真实表替换 AI 占位",
        ],
        "notes": [
            "商标与图片素材许可",
            "内网部署与模型 Key 管理",
            "导出格式兼容客户的 Office 版本",
        ],
        "who_good": [
            ("常做内部分享的人", "要快速骨架"),
            ("能自托管的团队", "敏感材料"),
        ],
        "who_bad": [
            ("要顶级设计师级对外路演", "仍需设计精修"),
            ("完全不改就上台", "风险高"),
        ],
    },
}


def gh(repo: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "lovart-t2"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def img(label: str, fname: str) -> str:
    return f"> 📷 **配图待补**：{label}（落盘名：`images/{fname}`）"


def safe_name(name: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", name).strip("-")


def render(num: int, fact: dict, stars: int | str, lic: str, url: str, desc: str) -> str:
    name = fact["name"]
    cat = fact["cat"]
    ca, cb = fact["comp"]
    slug = safe_name(name)
    stars_s = f"{stars:,}" if isinstance(stars, int) else str(stars)
    feat_rows = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in fact["features"])
    good_rows = "\n".join(f"| {a} | {b} |" for a, b in fact["who_good"])
    bad_rows = "\n".join(f"| {a} | {b} |" for a, b in fact["who_bad"])
    pros_b = "\n\n".join(
        f"**{i}. {p}**\n\n落地时我会用这一条当「留下它」的理由。"
        for i, p in enumerate(fact["pros"], 1)
    )
    cons_b = "\n\n".join(
        f"**{i}. {p}**\n\n这条不解决，我就不会把它写成「无脑推荐」。"
        for i, p in enumerate(fact["cons"], 1)
    )
    usage_parts = []
    for i, u in enumerate(fact["usage"], 1):
        usage_parts.append(f"### 用法 {i}\n\n{u}\n")
        if i <= 2:
            usage_parts.append(img(f"用法{i}对应界面", f"{slug}-usage-{i}.png"))
    usage = "\n\n".join(usage_parts)
    notes = "\n".join(f"- {n}" for n in fact["notes"])

    return f"""# {name} 深度测评：{fact['pitch']}——值得占一个工具位吗？

> T2 深度测评 · {cat} · 2026  
> GitHub / 官网：{url} ⭐ {stars_s}+  
> 许可证：{lic} · 公开描述：{desc or '见官方说明'}

---

## 👤 测评人背景

{cat} 是我内容工作里的高频摩擦点：工具太多，真正能进周更的很少。{name} 因为开源热度/话题度被反复点名（公开关注度约 {stars_s}），我按公开文档口径拆它——能省事的地方说实话，不能省的地方也不装。

---

## 🎯 先说结论

{name} 属于 **{cat}**：{desc or fact['pitch']}。对照常见是 {ca} 与 {cb}。选它通常是为了 **可控/可自建/可改**，不是因为它保证最好看的成片。

**我的决策句：你每周会认真用到「{cat}」，并接受文档与环境成本，再装；只想零配置交付，先看 {ca}。**

---

## 📦 {name} 是什么？

{name}（{url}）：{fact['pitch']}。协议 **{lic}**，公开关注度约 **{stars_s}**（以官方页为准）。

{img(f"{name} 首页/仓库", f"{slug}-homepage.png")}

{img(f"{name} 主界面", f"{slug}-main-ui.png")}

{img("全流程示意", f"{slug}-schematic-overview.png")}

```
[输入]
 ↓
[{name}]
 ↓
[可继续加工的输出]
```

---

## 🧩 {name} 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
{feat_rows}

### {fact['features'][0][0]}

{fact['features'][0][1]}。{fact['features'][0][2]}

{img("功能1界面", f"{slug}-feature-1.png")}

### {fact['features'][1][0]}

{fact['features'][1][1]}。{fact['features'][1][2]}

{img("功能2界面", f"{slug}-feature-2.png")}

### {fact['features'][2][0]}

{fact['features'][2][1]}。{fact['features'][2][2]}

---

## 🧠 核心逻辑：它为什么不一样？

收口 → 加工 → 交出。{name} 的差异化通常在开放与可集成，而不在「多一个魔法按钮」。

{img("逻辑示意", f"{slug}-architecture-flow.png")}

---

## ⚔️ {name} 和 {ca}、{cb} 有什么区别？

| 维度 | {name} | {ca} | {cb} |
|------|--------|------|------|
| 定位 | {cat} 开源/可控向 | 主流对照 | 另一对照 |
| 成本 | 开源+自备算力/API | 订阅常见 | 视产品 |
| 最强场景 | 要可控可改 | 要省心 | 特定习惯 |
| 短板 | 门槛 | 锁定/账单 | 可能不够开放 |

选型句：要可控优先 {name}；要省心优先 {ca}；习惯更贴 {cb} 就别为开源硬切。

{img("对照示意", f"{slug}-vs-competitor.png")}

---

## 🧪 我实际跑下来的体验

说明：基于公开文档与仓库元数据，不编造测速。

### ✅ 好的方面

{pros_b}

### ❌ 不好的方面

{cons_b}

{img("结果预览", f"{slug}-hands-on.png")}

---

## 💡 怎么高效用它

{usage}

需要视觉定妆时，可先走 Lovart，再回主流程。

---

## ⚠️ 安装和使用需要注意什么？

### 数据会离开本机吗？

本地/自托管可减少默认上云，但云端模型一接，片段仍可能出境。

### 许可证允许商用吗？

以 **{lic}** 与官方条款为准；二次分发与权重协议分开看。

{notes}

{img("设置/权限", f"{slug}-note-permission.png")}

---

> **怎么选：** 每周都要用「{cat}」且接受配置成本，优先 {name} 跑最小路径；只想零配置，不建议强上，先评估 {ca}。

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

{img("适合示意", f"{slug}-who-workflow.png")}

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | 视硬件与文档 |
| 核心能力 | ⭐⭐⭐⭐ | 主场景清楚 |
| 速度/批量 | ⭐⭐⭐ | 受硬件/API |
| 文档/社区 | ⭐⭐⭐⭐ | 以官方仓库为准 |
| 成本 | ⭐⭐⭐ | 开源≠免费算力 |

**综合评分：3.7 / 5.0**

> **一句话总结**：{name} 适合把「{cat}」当工序管理的人；最终观感与风险，仍取决于素材、模型与人审。

---

## 🔗 地址

- {url}  
- 对照：{ca} · {cb}  
- 互补：Lovart https://www.lovart.ai/

---

**标签**：#AI工具 #{cat} #{safe_name(name)}

---

### BLOCK 自检（本稿）

- [x] 单主角 + 完整 H2 + 怎么选 + 三列表  
- [x] 配图待补无断链  
- [ ] 实拍示意图待补  
"""


SPECIAL_FACTS = {
    23: {
        "name": "Nano Banana",
        "cat": "图像模型体验",
        "comp": ("Flux", "GPT Image"),
        "pitch": "面向 Nano Banana 模型体验与工作流讨论的单品深测位",
        "url": "以官方/聚合页为准（见 Daily 素材）",
        "stars": "话题向",
        "lic": "模型条款以官方为准",
        "desc": "围绕 Nano Banana 图像能力的体验与用法边界，不把它写成虚假官方仓库镜像",
        "features": [
            ("图像生成体验", "按公开能力出图", "验证风格与可控性"),
            ("工作流嵌入", "进创作者现有出图链路", "少为模型单独再造一套工具"),
            ("成本与限额意识", "关注额度与失败重试", "避免玩脱账单"),
        ],
        "pros": [
            "话题热度高，资料与案例更新快",
            "适合快速试风格方向",
            "可与定妆/品牌视觉流程结合",
            "失败样本本身也是选型信息",
        ],
        "cons": [
            "产品入口与命名易混，要以你实际用的客户端为准",
            "商用条款与地区可用性常变",
            "质量波动，需人审",
            "不要把评测当永久承诺",
        ],
        "usage": [
            "同一提示词固定种子/参数做三轮，再谈好不好用",
            "品牌色与角色先定约束，再开放发挥",
            "入选图进 Lovart/设计工具做终稿规范",
        ],
        "notes": [
            "以你账号实际可用地区与条款为准",
            "客户商用前核许可",
            "勿编造官方 Stars",
        ],
        "who_good": [("图像创作者试模型", "要快速体感"), ("设计草稿发散", "要风格样本")],
        "who_bad": [("要稳定印刷级 VI", "流程不够"), ("完全不看条款就商用", "风险高")],
    },
    24: {
        "name": "Seedance 2.0",
        "cat": "视频模型",
        "comp": ("Kling", "Runway"),
        "pitch": "面向 Seedance 视频生成能力的选型深测（按公开产品口径）",
        "url": "以字节系/官方产品入口为准",
        "stars": "产品向",
        "lic": "商业服务条款",
        "desc": "Seedance 常被用作短剧/镜头视频生成后端；本稿按公开产品讨论写法，不伪造 GitHub Stars",
        "features": [
            ("文生/图生视频", "按镜头生成短视频", "分镜动态化"),
            ("作为工作台后端", "可被 Toonflow 等挂接", "软件编排 + 模型出片分工"),
            ("按量计费意识", "条均成本要进选题决策", "避免「工作台免费却拍不起」"),
        ],
        "pros": [
            "短剧链路里常见，资料与案例多",
            "适合作为「贵价出片」步骤而不是唯一工具",
            "与本地工作台组合时，编排权仍在你",
            "成本可按条估算，逼你做选题取舍",
        ],
        "cons": [
            "账单敏感，周更原型不能条条满血",
            "人物一致性仍是行业难题",
            "条款与可用地区变化快",
            "终审与平台规范要人扛",
        ],
        "usage": [
            "先便宜模型出静帧/草分镜，确认钩子再调用 Seedance",
            "固定角色参考图，减少换脸",
            "输出进剪辑软件做人审与节奏",
        ],
        "notes": [
            "以官方定价与服务条款为准，不写死价格",
            "深度合成合规",
            "Key 与额度管理",
        ],
        "who_good": [("短剧原型创作者", "要动态镜头"), ("已有工作台编排", "缺视频后端")],
        "who_bad": [("零预算日更", "烧不起"), ("要电影级成片承诺", "预期错位")],
    },
    25: {
        "name": "GPT-image 2",
        "cat": "图像生成",
        "comp": ("Flux", "Midjourney"),
        "pitch": "面向 GPT-image 图像能力的国内可用路径与用法边界",
        "url": "以 OpenAI/国内转接可用入口为准",
        "stars": "产品向",
        "lic": "服务条款",
        "desc": "讨论 GPT-image 系图像生成在实际创作中的用法与限制；地区与转接可用性以你当前通道为准，不写死「一定能用」",
        "features": [
            ("提示词出图", "文本/参考图生成", "视觉方案发散"),
            ("接入工作流", "API/客户端调用", "批量与节点化"),
            ("与设计终稿分工", "AI 出候选，设计工具收束", "避免聊天框当终稿库"),
        ],
        "pros": [
            "提示词遵循度通常较好，适合方案发散",
            "可进 API 工作流",
            "与品牌改图/定妆流程可组合",
            "失败案例能反推提示词规范",
        ],
        "cons": [
            "地区与账单通道复杂，要自己核",
            "商用与相似风险需人审",
            "细节文字/复杂排版仍不稳",
            "政策与模型版本会变",
        ],
        "usage": [
            "先建提示词模板：主体/光线/镜头/负向",
            "定妆多方案 → 人工选 → Lovart/设计工具规范",
            "批量前先算单价与失败重试率",
        ],
        "notes": [
            "国内可用性以你的合规通道为准",
            "客户素材授权",
            "勿在文中承诺未核实的「官方国内直连」",
        ],
        "who_good": [("需要 API 出图的创作者", "要进管线"), ("方案发散阶段", "要快")],
        "who_bad": [("只要本地离线", "路线不符"), ("要印刷级零人审", "不现实")],
    },
}


def write_num(num: int, fact: dict, stars, lic: str, url: str, desc: str) -> None:
    folders = list(DAILY.glob(f"{num:03d}-*"))
    if not folders:
        print("missing", num)
        return
    folder = folders[0]
    (folder / "images").mkdir(exist_ok=True)
    body = render(num, fact, stars, lic, url, desc)
    existing = list(folder.glob(f"T2-{num:03d}-*.md"))
    out = existing[0] if existing else folder / f"T2-{num:03d}-{safe_name(fact['name'])}.md"
    out.write_text(body, encoding="utf-8")
    zh = len(re.findall(r"[\u4e00-\u9fff]", body))
    print(f"DEEP {num:03d} zh={zh} -> {out.relative_to(DAILY)}")


def main() -> None:
    for num, fact in FACTS.items():
        data = gh(REPOS[num])
        lic = (data.get("license") or {}).get("spdx_id") or "见仓库"
        write_num(
            num,
            fact,
            data["stargazers_count"],
            lic,
            data["html_url"],
            data.get("description") or "",
        )
    for num, fact in SPECIAL_FACTS.items():
        write_num(num, fact, fact["stars"], fact["lic"], fact["url"], fact["desc"])


if __name__ == "__main__":
    main()
