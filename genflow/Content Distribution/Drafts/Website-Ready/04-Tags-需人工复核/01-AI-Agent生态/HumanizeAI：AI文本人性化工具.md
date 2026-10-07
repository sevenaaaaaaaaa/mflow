---
title: "Humanizer-zh：AI文本人性化工具"
slug: humanizer-zh
date: 2026-06-15
updated: 2026-06-15
tags: [AI写作, 人性化, Claude Code Skill]
categories: [AI工具]
summary: "Humanizer-zh：Claude Code 中文 AI 文本去痕 Skill，识别 24 种 AI 写作模式。平台：Claude Code。"
focus_keyword: "Humanizer-zh"
source: https://github.com/op7418/Humanizer-zh
status: draft
---

# Humanizer-zh：AI文本人性化工具

> 10.4k+ stars | Claude Code Skill | MIT | 消除 AI 生成痕迹，让文字有真正的人类声音

## 这是什么

Humanizer-zh 是一个 Claude Code Skills，核心功能是识别并修复 AI 生成文本中的"机械痕迹"，把生硬的 AI 输出改写得自然、鲜活、像真人写的。它是 [blader/humanizer](https://github.com/blader/humanizer) 的完整中文汉化版本，由 op7418 维护，目前已有 10.4k+ stars。

该项目基于维基百科的 [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 指南，系统性地总结了 24 种 AI 写作模式，分为四大类：内容模式（如过度强调意义、模糊归因）、语言语法模式（如"AI 词汇"高频使用、三段式法则）、风格模式（如破折号过度、表情符号滥用）、交流模式和填充词（如谄媚语气、通用积极结论）。

与 GPTZero 等 AI 检测器不同，Humanizer-zh 的目标不是"骗过检测器"，而是真正提升写作质量。它的核心理念是：好的写作需要观点、节奏变化、承认复杂性、适当使用第一人称，甚至允许一些"混乱"——因为完美的结构反而显得机械。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 经常用 AI 生成文章、报告、营销文案的写作者 | ✅ 推荐 | 一键消除"AI 味"，保留核心信息的同时注入真实人类风格 |
| 需要润色 AI 辅助写作内容的学生/研究者 | ✅ 推荐 | 帮助识别和修复常见的 AI 写作痕迹，避免学术不端风险 |
| Claude Code 重度用户 | ✅ 推荐 | 原生 Claude Code Skill，直接在对话中调用，无缝集成工作流 |
| 追求极致原创、从不用 AI 辅助写作的人 | ⚠️ 酌情 | 工具定位是"修复"而非"生成"，但如果你是纯手写派则无需此工具 |
| 非 Claude Code 用户 | ❌ 不推荐 | 目前仅以 Claude Code Skill 形式分发，其他平台需手动使用 SKILL.md 中的规则 |

## 安装

### 通过 npx 一键安装（推荐）

```bash
npx skills add https://github.com/op7418/Humanizer-zh.git
```

### 通过 Git 克隆

```bash
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh
```

### 手动安装

下载 ZIP 或将 `Humanizer-zh` 文件夹复制到 Claude Code 的 skills 目录：
- macOS/Linux: `~/.claude/skills/`
- Windows: `%USERPROFILE%\.claude\skills\`

安装后在 Claude Code 中输入 `/humanizer-zh` 验证是否激活成功。

## 核心用法

### 1. 直接调用技能

```
/humanizer-zh 请帮我人性化以下文本：
[粘贴你的 AI 生成文本]
```

### 2. 处理文件内容

```
/humanizer-zh 请人性化 article.md 文件中的内容
```

### 3. 改写示例

**改写前（典型 AI 味道）**：
> 坐落在风景如画的杭州市中心，这家咖啡馆拥有丰富的文化底蕴和令人叹为观止的装饰。它作为城市咖啡文化的焦点，为顾客提供无缝、直观和充满活力的体验。

**改写后**：
> 这家咖啡馆在杭州市中心开了三年，以手冲咖啡和老建筑改造的空间出名。

### 4. 手动参考 24 种模式

如果不使用 Claude Code，也可直接阅读仓库中的 `SKILL.md`，手动对照 24 种 AI 写作模式自查和修改文本。核心原则：有观点、变化节奏、承认复杂性、适当使用"我"、允许一些混乱、对感受要具体。

### 常见 AI 词汇警示

以下词在 AI 生成文本中出现频率异常高，发现后应替换或删除：此外、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、相互作用、复杂/复杂性、格局（抽象名词）、关键性的、展示、织锦（抽象名词）、证明、宝贵的、充满活力的。

## 注意事项与风险

- **不是"反检测"工具**：Humanizer-zh 的设计初衷是提升写作质量，而非绕过 AI 检测器。过度使用反而可能让文字显得刻意。
- **中文语境适配**：项目考虑了中文写作的特殊性（如标题大小写问题在中文中表现不同），但部分英文写作模式的检测规则在中文中可能不完全适用。
- **Claude Code 依赖**：目前仅以 Claude Code Skill 形式提供，如果 Claude Code 服务不可用或版本不兼容，工具无法运行。
- **代码体积很小**：整个项目只包含 `SKILL.md` 和 `README.md` 两个文件，本质上是一套精炼的规则和提示词，没有复杂的后端逻辑。

## 与你现有工具的关系

- 与 [[Claude Code + Obsidian：Claude Code + Obsidian Visual Skills 全自动]] 配合：可在 Obsidian 中撰写内容后，在 Claude Code 中调用 Humanizer-zh 进行润色。
- 与 [[Claude Code Skills：-last30days 找最近 30 天好用的 Prompt]] 并列：同属 Claude Code Skills 生态，可共同构成你的 AI 写作工作流。
- 与 [[../05-开发技术栈/Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本]] 互补：Privacy Filter 关注"发给 AI 前脱敏"，Humanizer-zh 关注"AI 输出后的润色"，一个管入口，一个管出口。
- 与 [[ReadPo：AI驱动的读写助手]] 协作：ReadPo 负责阅读和初步生成，Humanizer-zh 负责最终润色，形成完整的内容生产链。

## FAQ

### Q: Humanizer-zh 和 HumanizeAI 是同一个东西吗？
A: 不是。Humanizer-zh 是开源 Claude Code Skill（GitHub: op7418/Humanizer-zh），专注于文本去 AI 化。HumanizeAI 是一个商业在线工具（nownexts.com），功能类似但闭源且需要订阅。

### Q: 使用后 AI 检测器还会判定为 AI 生成吗？
A: 不一定。Humanizer-zh 的目标是提升写作质量而非"骗过检测器"。改写后的文字更自然、更具体、更有个人风格，客观上可能降低被检测的概率，但这并非工具的设计目标。

### Q: 除了 Claude Code，能在其他 AI 工具中使用吗？
A: 可以将 `SKILL.md` 中的规则复制为自定义 Prompt 在其他 AI 工具中使用，但无法获得 /humanizer-zh 的专属 Skill 级别集成。

## 相关链接

- GitHub：https://github.com/op7418/Humanizer-zh
- 原始英文版：https://github.com/blader/humanizer
- 实用工具参考：https://github.com/hardikpandya/stop-slop
- 维基百科 AI 写作指南：https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
