# How to Produce a Complete AI Short Drama: Full Workflow from Script to Final Cut

> [English version pending translation]

# T3-003 AI 短剧制作全流程：从剧本到成片，一套工具链跑到黑

> 2026 年 AI 短剧赛道彻底爆发。但大多数创作者卡在同一个问题上：**工具太多、链路太碎、不知道哪一步该用什么**。写剧本用 Claude，做分镜用 ComfyUI，生角色用 Midjourney，配音用 ElevenLabs，剪辑用剪映——每一步都是一个新软件、一笔新费用、一次新学习成本。这篇文章给你一条经过实战验证的工具链：**Toonflow 出剧本分镜 → Jellyfish 管角色一致性 → LibTV 做视频合成 → VoxCPM 出配音 → LosslessCut 精剪收尾**。五个工具、一条链路、全流程可跑通。

---

## 📊 工具链速览

| 工具 | 定位 | 类型 | Stars | 在链路中的角色 |
|------|------|------|-------|--------------|
| **Toonflow** | AI 短剧桌面创作工具 | 开源 / Electron | ⭐ 10.1k | 编剧改写 + 智能分镜 + 角色初稿 |
| **Jellyfish** | 短剧端到端生产工作台 | 开源 / Python | ⭐ 3.8k | 结构化分镜 + 跨镜头一致性管理 |
| **LibTV** | 节点式 AI 视频创作平台 | 云端平台 | — | 视频合成 + 运镜 + 转场 + 主体库 |
| **VoxCPM** | AI 语音合成引擎 | 开源 / Python | ⭐ 26.1k | 多角色配音 + 30 语种 + Voice Design |
| **LosslessCut** | 无损视频剪切工具 | 开源 / Electron | ⭐ 30k+ | 精剪 + 片段拼接 + 音轨对齐 |

---

## 一、AI 短剧制作全景图：五步六工具，一条链路

传统短剧制作需要编剧、分镜师、角色设计师、动画师、配音演员、剪辑师六个角色。AI 工具链把这个团队压缩成一个人 + 五个工具：

```
你的短剧剧本（文字/小说章节）
        │
        ▼
  ① 剧本拆解 ──── Toonflow / Jellyfish
     AI 编剧改写 → 场景切分 → 对话提取 → 角色识别
        │
   