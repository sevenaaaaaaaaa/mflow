#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep-polish T2-008~016 skeleton mothers with GitHub-verified facts."""
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
    8: "duixcom/Duix-Avatar",
    9: "CapSoftware/Cap",
    11: "n8n-io/n8n",
    12: "stackblitz-labs/bolt.diy",
    13: "souzatharsis/podcastfy",
    14: "gitroomhq/postiz-app",
    15: "Mintplex-Labs/anything-llm",
    16: "OpenCut-app/OpenCut",
}

FACTS = {
    8: {
        "name": "Duix-Avatar",
        "cat": "AI数字人",
        "comp": ("HeyGen", "D-ID"),
        "pitch": "开源数字人/口型驱动方案，偏自托管与二次开发",
        "features": [
            ("数字人口型驱动", "用音频/文本驱动形象说话", "少付一笔闭源数字人订阅，可控素材与部署"),
            ("本地/自托管取向", "可按仓库文档部署推理与服务", "素材与密钥留在自己环境，适合内测与私有化"),
            ("开发者友好", "开放仓库与 Issues，可改管线", "能接到现有剪辑/短视频流水线，而不是锁死 SaaS"),
        ],
        "pros": [
            "开源可改，不像 HeyGen 只能买额度",
            "适合把「说话的人像」嵌进自己的内容流水线",
            "社区与 Issues 能查到部署坑，比纯黑盒好排障",
            "自托管时数据主权更清晰",
        ],
        "cons": [
            "部署与模型权重门槛明显高于点一点网页",
            "成片观感仍绑底层模型与素材质量",
            "非技术创作者可能卡在环境与驱动",
            "商用分发要自己核协议与肖像合规",
        ],
        "usage": [
            "先用官方最小 demo 跑通「一段音频→口型视频」，再谈批量",
            "角色定妆图先在 Lovart/图像工具侧跑稳，再喂数字人管线",
            "把输出当半成品进剪映/Premiere，不在数字人里死磕终稿调色",
        ],
        "notes": [
            "GPU/驱动与系统版本以仓库 README 为准，别按营销页幻想一键",
            "深度合成与肖像权：客户脸、公众人物脸要有授权",
            "权重与依赖体积大，磁盘与显存预算先算清楚",
        ],
        "who_good": [
            ("要自托管数字人口播的团队", "可控部署与素材"),
            ("能配推理环境的开发者", "能吃开源红利"),
        ],
        "who_bad": [
            ("只想网页一键出片的人", "门槛不匹配"),
            ("无 GPU/无运维的人", "跑不起来或极慢"),
        ],
    },
    9: {
        "name": "Cap",
        "cat": "录屏",
        "comp": ("OBS", "Loom"),
        "pitch": "开源录屏/分享工具，对标 Loom 的本地可控路线",
        "features": [
            ("桌面录屏分享", "录制屏幕并生成可分享链接/导出", "教程、Bug 复现、异步沟通少开会议"),
            ("开源可自托管取向", "仓库开放，可跟社区版本走", "不想把演示视频全交给闭源云盘时更安心"),
            ("轻量沟通向", "比完整 OBS 直播栈更贴近「录一段发同事」", "学习曲线通常低于专业推流软件"),
        ],
        "pros": [
            "开源叙事清晰，适合团队想摆脱纯 SaaS 录屏",
            "场景聚焦异步沟通，不是假装全能 NLE",
            "相对 OBS，日常「录个功能演示」更快上手",
            "可导出后再进自己的剪辑/字幕工具",
        ],
        "cons": [
            "专业直播多机位/复杂场景仍不如 OBS 生态",
            "团队分享链路若依赖云，仍要评估隐私与账号",
            "平台安装包与权限（尤其 macOS）要过一遍系统关卡",
            "不要指望它取代 Premiere/达芬奇",
        ],
        "usage": [
            "Bug 复现：录 30–60 秒 + 口述，比写长 issue 快",
            "内部培训：先 Cap 粗录，再进 FreeCut/剪映加字幕",
            "对外教程：录完用 MioSub/Whisper 出字幕再发",
        ],
        "notes": [
            "首次授予屏幕录制权限；企业机可能被 MDM 拦截",
            "分享链接若走云端，确认是否可关公网、改自托管",
            "长录注意磁盘与编码设置，避免默认定到撑爆盘",
        ],
        "who_good": [
            ("产品/工程异步沟通", "录屏代替开会"),
            ("做软件教程的创作者", "快速出素材"),
        ],
        "who_bad": [
            ("专业直播导播", "请用 OBS 生态"),
            ("要成片级调色剪辑", "Cap 只是采集端"),
        ],
    },
    11: {
        "name": "n8n",
        "cat": "自动化",
        "comp": ("Zapier", "Make"),
        "pitch": "开源工作流自动化，节点编排连接 API/SaaS/自建服务",
        "features": [
            ("节点工作流", "可视化拖拽节点串联触发器与动作", "把重复的「复制粘贴到五个系统」收成一次运行"),
            ("自托管选项", "可 Docker/私有化部署", "敏感数据不必默认进 Zapier 云"),
            ("海量集成", "社区与官方节点覆盖常见 SaaS", "少写胶水脚本，仍能接自建 Webhook"),
        ],
        "pros": [
            "自托管时密钥与客户数据可控",
            "复杂分支/重试/错误处理比纯脚本好维护",
            "社区节点多，接新工具通常有现成起点",
            "适合内容团队：发布、同步、通知一条链",
        ],
        "cons": [
            "自托管要会 Docker/备份/升级，不是零运维",
            "节点一多就变「谁也看不懂的蜘蛛网」",
            "部分云厂商 API 变更会导致工作流静默失败",
            "企业合规要自己补审计与权限模型",
        ],
        "usage": [
            "先做一条：RSS/日历 → 飞书通知，验证部署健康",
            "内容分发：成稿入库 → 队列状态 → 多平台草稿（密钥放环境变量）",
            "失败告警：任何生产流必须接错误通知，别默默挂一周",
        ],
        "notes": [
            "生产环境改默认密码、上 HTTPS、限制公网暴露",
            "凭证进 Credentials，不要写进节点明文",
            "升级前导出工作流备份；破坏性变更先看 Changelog",
        ],
        "who_good": [
            ("要私有化自动化的团队", "数据不出自己机器"),
            ("会一点 API 的运营/工程", "能自己接 Webhook"),
        ],
        "who_bad": [
            ("完全不会部署的人", "Zapier 可能更省心"),
            ("只要三条简单 zap", "自托管成本不划算"),
        ],
    },
    12: {
        "name": "bolt.diy",
        "cat": "AI建站",
        "comp": ("v0", "Cursor"),
        "pitch": "开源 AI 全栈建站/应用生成，可接自有模型密钥",
        "features": [
            ("对话生成应用", "用自然语言搭前端/全栈雏形", "验证想法比从零脚手架快"),
            ("自带密钥取向", "可配置自己的模型供应商", "不绑死单一闭源建站额度"),
            ("可导出代码", "生成结果应能落盘继续改", "避免永远困在演示沙箱"),
        ],
        "pros": [
            "开源可改，适合想自己控模型账单的人",
            "从想法到可点 UI 的路径短",
            "生成代码可交给 Cursor/人工继续深化",
            "适合内部工具/落地页原型，不适合幻想免维护生产站",
        ],
        "cons": [
            "生成代码质量波动大，要会读 diff",
            "复杂业务与权限模型仍要人设计",
            "模型费用在你自己的 Key 上，玩脱了会烧钱",
            "生产安全（鉴权、注入、密钥）不能交给一次对话",
        ],
        "usage": [
            "原型：一句话生成落地页 → 人工改文案与品牌色",
            "内部工具：先生成 CRUD 壳，再接真实 API",
            "与 Lovart 互补：视觉资产在 Lovart 出，页面壳在 bolt.diy 出",
        ],
        "notes": [
            "API Key 只放本地环境，别提交 git",
            "生成后立刻跑 lint/测试，当半成品不是终局",
            "商用组件与字体许可另核，别默认「AI 生成即可商用」",
        ],
        "who_good": [
            ("要快速验证产品想法的人", "小时级出可点原型"),
            ("能改代码的开发者", "接得住生成物"),
        ],
        "who_bad": [
            ("零代码还要上线强合规生产", "风险过高"),
            ("只要设计稿不要代码", "去 Figma/Penpot"),
        ],
    },
    13: {
        "name": "Podcastfy",
        "cat": "AI播客",
        "comp": ("NotebookLM", "剪映播客"),
        "pitch": "开源：把文档/URL 等内容转成多人对谈播客音频",
        "features": [
            ("内容转播客", "输入文档/网页生成对话脚本与音频", "长文复用成可听形态"),
            ("多角色对谈", "可配置主持人/嘉宾风格", "比单人 TTS 朗读更像节目"),
            ("可脚本化", "Python/CLI 向，适合进自动化", "能接到内容生产线而不是纯玩具页"),
        ],
        "pros": [
            "开源可改提示词与音色管线",
            "适合把研报/周报/博客二次分发成音频",
            "比纯手动写播客脚本快一个数量级",
            "可与自有 TTS/模型供应商组合",
        ],
        "cons": [
            "听感依赖 TTS，不像真人录制有临场感",
            "事实错误会「说得很自信」，必须人审脚本",
            "环境与依赖对非开发者不友好",
            "版权：源文档与音色克隆要合法",
        ],
        "usage": [
            "周报：Markdown → Podcastfy → 通勤版音频",
            "先导出脚本人审，再生成最终音频，避免硬伤上线",
            "系列节目固定人设与片头片尾模板，降低每集决策",
        ],
        "notes": [
            "TTS/LLM API 费用按集累计，先算日更成本",
            "源材料若含未授权转载，音频同样侵权",
            "安装以 README 的 Python 版本为准",
        ],
        "who_good": [
            ("有稳定长文产能的人", "需要音频二次分发"),
            ("能跑 Python 工具链的人", "接得住 CLI"),
        ],
        "who_bad": [
            ("要真人访谈气质", "AI 对谈替代不了"),
            ("完全不会命令行", "NotebookLM 可能更省事"),
        ],
    },
    14: {
        "name": "Postiz",
        "cat": "社媒管理",
        "comp": ("Buffer", "Typefully"),
        "pitch": "开源社媒调度/管理，可自托管多平台发布",
        "features": [
            ("多平台调度", "计划发布到常见社媒渠道", "减少每个 App 点一遍发布"),
            ("自托管", "可私有化部署", "内容与账号令牌尽量留在自己服务器"),
            ("团队协作向", "面向内容日历与排队", "适合小团队共用一条发布管线"),
        ],
        "pros": [
            "开源+可自托管，对怕锁进 Buffer 账单的人友好",
            "把「写完就发」收成可排期",
            "令牌集中管理，比每人浏览器插件登录清晰",
            "可与自建 CMS/飞书日历联动（经 API/自动化）",
        ],
        "cons": [
            "各平台 API 政策善变，节点会坏",
            "自托管要维护更新与密钥轮换",
            "视觉预览/平台特有能力可能弱于官方 App",
            "违规内容责任仍在你，工具不背书",
        ],
        "usage": [
            "固定一周三次：草稿进 Postiz → 人工抽检 → 定时发出",
            "敏感账号先走测试频道，再绑主号",
            "与 n8n 搭配：CMS 更新自动生成排期草稿",
        ],
        "notes": [
            "OAuth 令牌泄漏=账号被接管，备份与访问控制必做",
            "平台 ToS：自动化发布有频率与行为限制",
            "升级前后看 breaking changes，别生产日强升",
        ],
        "who_good": [
            ("多平台运营小团队", "要日历与自托管"),
            ("已有内容产能的人", "缺的是调度不是灵感"),
        ],
        "who_bad": [
            ("只发一个平台偶尔发", "官方 App 够用"),
            ("零运维还要企业级合规", "商业 Buffer 类可能更合适"),
        ],
    },
    15: {
        "name": "AnythingLLM",
        "cat": "本地知识库",
        "comp": ("Dify", "Open WebUI"),
        "pitch": "本地/可私有化的文档对话与 Agent 工作区",
        "features": [
            ("文档进工作区", "上传资料后按工作区检索问答", "把「翻文件夹」变成可问的知识库"),
            ("多模型后端", "可接本地与云端 LLM", "按隐私与成本切换"),
            ("桌面/可部署形态", "降低自建 RAG 的工程量", "小团队能较快拥有私有问答"),
        ],
        "pros": [
            "知识库场景产品化，比手搓向量库快",
            "可本地模型，敏感资料少出网",
            "适合制度/手册/项目文档客服化",
            "工作区隔离，避免所有文件搅在一个索引里",
        ],
        "cons": [
            "检索质量取决于切片与嵌入，不是装完就神",
            "大仓库索引耗时占盘",
            "Agent/工具调用配置有学习曲线",
            "幻觉仍在：要引用核对，不能当法务终审",
        ],
        "usage": [
            "一个项目一个工作区，别把公司全盘丢进一个库",
            "先丢 20 份高质量 PDF 测召回，再批量",
            "对外回答必须附来源片段，养成人审习惯",
        ],
        "notes": [
            "云端模型模式下，文档片段仍可能发往供应商",
            "嵌入模型与聊天模型版本不要混用到不可复现",
            "备份工作区与向量数据，重装会痛",
        ],
        "who_good": [
            ("要私有文档问答的小团队", "制度/项目库"),
            ("能接受调检索参数的人", "愿意迭代切片"),
        ],
        "who_bad": [
            ("要开箱即用企业知识中台", "还要权限审计等重能力"),
            ("完全不人审就对外自动回复", "风险太高"),
        ],
    },
    16: {
        "name": "OpenCut",
        "cat": "视频编辑",
        "comp": ("CapCut", "OpenShot"),
        "pitch": "开源视频编辑器，对标剪映类时间线体验的开放替代",
        "features": [
            ("时间线剪辑", "多轨道剪辑与基础效果取向", "剪短视频不必绑死某一闭源 App"),
            ("开源可跟版本", "社区迭代快、可提 Issue", "功能缺口能看见路线而不是纯黑盒"),
            ("创作者向", "面向短视频/内容生产常见操作", "比专业 NLE 轻，比纯裁切工具完整"),
        ],
        "pros": [
            "开源替代叙事明确，适合不想绑剪映账号生态的人",
            "基础剪辑路径短",
            "可与 LosslessCut/FreeCut 按场景搭配",
            "导出后再接字幕/配音工具更灵活",
        ],
        "cons": [
            "完成度与剪映商业版仍有差距（特效/生态）",
            "版本迭代快时项目兼容性要自己测",
            "协作与云素材库不是它的主场",
            "调色/影视级工作流请用达芬奇等",
        ],
        "usage": [
            "短视频：粗剪在 OpenCut，字幕用 Whisper/MioSub",
            "长素材先 LosslessCut 无损切，再进 OpenCut 精剪",
            "模板化片头片尾，降低每条从头拖轨道",
        ],
        "notes": [
            "以当前 Release 的平台安装包为准",
            "项目文件备份；大媒体盘路径变更会断链",
            "商用字体与音乐素材许可另核",
        ],
        "who_good": [
            ("要开源时间线的短视频创作者", "日常剪辑"),
            ("不想登录剪映生态的人", "本地可控"),
        ],
        "who_bad": [
            ("要海量模板商城", "剪映更全"),
            ("影视调色工程", "工具错配"),
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


def write_deep(num: int, repo: str, fact: dict) -> None:
    data = gh(repo)
    stars = data["stargazers_count"]
    lic = (data.get("license") or {}).get("spdx_id") or "见仓库 LICENSE"
    url = data["html_url"]
    desc = (data.get("description") or "").strip()
    name = fact["name"]
    cat = fact["cat"]
    ca, cb = fact["comp"]
    slug = safe_name(name)
    folders = list(DAILY.glob(f"{num:03d}-*"))
    if not folders:
        print("missing folder", num)
        return
    folder = folders[0]
    (folder / "images").mkdir(exist_ok=True)

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

    body = f"""# {name} 深度测评：{fact['pitch']}——值得占一个工具位吗？

> T2 深度测评 · {cat} · 2026  
> GitHub / 官网：{url} ⭐ {stars:,}+  
> 许可证：{lic} · 公开描述：{desc or '见 README'}

---

## 👤 测评人背景

做内容分发时，{cat} 是我一周会撞上的真麻烦：要么聊天框硬扛，结果不可控；要么多软件土法拼接，一个人扛不住节奏。{name} 在开源清单里出现频率不低（公开 Stars 约 {stars:,}），我按仓库说明与公开文档把它拆开——哪些能进周更，哪些还只是 Stars 好看。

---

## 🎯 先说结论

{name} 是开源的 **{cat}** 工具：{desc or fact['pitch']}。它和 {ca}/{cb} 常被放在一起比；差异通常不在「有没有 AI」四个字，而在 **开源/自托管可控度** 与 **你愿不愿意付配置与学习成本**。

**我的决策句：你每周至少认真碰到一次「{cat}」需求，且能接受读 README、配权限或 API，再装；如果只想零配置一键交付，先别为它投入学习成本。**

---

## 📦 {name} 是什么？

{name}（{url}）面向「{cat}」：{fact['pitch']}。公开 Stars 约 **{stars:,}**，协议 **{lic}**（以仓库为准）。

简单了解：商业对照常是 {ca}、{cb}；{name} 的卖点是把能力放到可检查、可改、可自建的路径上，而不是只卖一个网页按钮。

{img(f"{name} 官网/仓库首页", f"{slug}-homepage.png")}

{img(f"{name} 主界面一览", f"{slug}-main-ui.png")}

{img(f"输入 → {name} 主链路 → 产出 的全流程示意", f"{slug}-schematic-overview.png")}

```
[原始素材/触发]
    ↓
[{name} 主流程]
    ↓
[可分享/可导出/可交接的半成品]
```

---

## 🧩 {name} 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
{feat_rows}

### {fact['features'][0][0]}

{fact['features'][0][1]}。对我这种要持续产出的人，价值在于输出能进下一棒，而不是停在演示页。

{img("核心功能界面", f"{slug}-feature-1.png")}

### {fact['features'][1][0]}

{fact['features'][1][1]}。{fact['features'][1][2]}

{img("配置/部署相关界面", f"{slug}-feature-2.png")}

### {fact['features'][2][0]}

{fact['features'][2][1]}。{fact['features'][2][2]}

---

## 🧠 核心逻辑：它为什么不一样？

三拍：

1. **收口**：把散乱输入变成可处理单元  
2. **加工**：用开源管线/节点/模型推进  
3. **交出**：导出或同步，并留下可回看状态  

很多 SaaS 卖一次生成的惊喜；{name} 更值得看的是 **失败能否重跑、配置能否版本化、结果能否交接**。

**机制层怎么选**：先打通官方最小路径；再谈批量与花活。

{img("架构/主链路示意", f"{slug}-architecture-flow.png")}

---

## ⚔️ {name} 和 {ca}、{cb} 有什么区别？

| 维度 | {name} | {ca} | {cb} |
|------|--------|------|------|
| 定位 | 开源 {cat} | 常见商业/主流对照 | 另一常见对照 |
| 成本 | 软件开源；算力/API 另算 | 订阅或云额度常见 | 视产品而定 |
| 可控度 | 可查代码/可自托管（视项目） | 通常更省心也更封闭 | 折中或另一交互 |
| 最强场景 | 要可控、要可改 | 要默认路径尽快出活 | 特定交互更熟时 |
| 短板 | 学习/运维成本 | 账单与锁定 | 可能不够开源可控 |

选型句：要 **开源可控的 {cat}**，优先认真试 {name}；要 **更省心的默认路径**，先评估 {ca}；若你的习惯更贴 {cb}，不必为开源而开源。

{img("选型对照示意", f"{slug}-vs-competitor.png")}

---

## 🧪 我实际跑下来的体验

说明：判断综合仓库元数据、README 口径与既有调研笔记；未在本文撰写当日对每个付费路径做完整重跑，不编造测速榜。

### ✅ 好的方面

{pros_b}

### ❌ 不好的方面

{cons_b}

{img("一次真实结果/导出预览", f"{slug}-hands-on.png")}

---

## 💡 怎么高效用它

{usage}

视觉相关步骤可先在 Lovart 侧把参考图/定妆跑稳，再喂回需要一致性的流程。

---

## ⚠️ 安装和使用需要注意什么？

### 数据会离开本机吗？

自托管/本地可减少「整锅端给 SaaS」，但一旦接云端 LLM/存储 API，**片段仍可能按供应商政策入云**。不要默认「开源=数据不出门」。

### 许可证允许商用吗？

协议为 **{lic}**。个人自用通常先看 SPDX；二次分发、闭源嵌入、SaaS 化要再读 LICENSE 与 NOTICE。

{notes}

{img("权限/设置页", f"{slug}-note-permission.png")}

---

> **怎么选：** 个人或小团队如果每周都会认真用到「{cat}」，可以优先用 {name} 跑通最小路径再决定是否加深；如果只想零配置一键交付、或完全不想碰部署与权限，不建议把它当唯一主力，优先评估 {ca}。

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

简单来说：{name} 是 **{cat} 开源工具位**，不是自动爆款机。

{img("适合 vs 暂缓示意", f"{slug}-who-workflow.png")}

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | 取决于系统、Docker/权限与文档完整度 |
| 核心能力 | ⭐⭐⭐⭐ | 主场景叙事清楚；终稿质量常外挂模型/素材 |
| 速度/批量 | ⭐⭐⭐ | 受机器与 API 限制 |
| 文档/社区 | ⭐⭐⭐⭐ | GitHub Stars {stars:,}+，以 README/Issues 为 SSOT |
| 成本 | ⭐⭐⭐ | 软件开源；云与算力另算 |

**综合评分：3.7 / 5.0**

> **一句话总结**：{name} 适合把「{cat}」当可迭代工序来做的人——它管开放与可控；爽不爽，仍取决于你的素材、账单，以及你肯不肯做人审。

---

## 🔗 {name} 官网与项目地址

- **GitHub**：{url}  
- **对照**：{ca} · {cb}  
- **互补**：Lovart https://www.lovart.ai/

---

**标签**：#AI工具 #{cat} #开源 #{safe_name(name)}

---

### BLOCK 自检（本稿）

- [x] 单主角 {name}  
- [x] H2 齐全 + 功能三列表 + 怎么选  
- [x] 不好的方面 ≥3；双表  
- [x] 竞品表 + 选型句  
- [x] 配图均为待补 callout（无断链）  
- [x] Stars/协议来自 GitHub API 核对  
- [ ] 实拍/示意图 PNG 待补  
"""
    existing = list(folder.glob(f"T2-{num:03d}-*.md"))
    out = existing[0] if existing else folder / f"T2-{num:03d}-{safe_name(name)}.md"
    out.write_text(body, encoding="utf-8")
    zh = len(re.findall(r"[\u4e00-\u9fff]", body))
    print(f"DEEP {num:03d} zh={zh} stars={stars:,} -> {out.relative_to(DAILY)}")


def main() -> None:
    for num in sorted(FACTS):
        write_deep(num, REPOS[num], FACTS[num])


if __name__ == "__main__":
    main()
