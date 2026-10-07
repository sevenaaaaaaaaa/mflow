---
title: "Claude Code Humanizer：AI 写作去痕与文章可读性提升"
slug: claude-code-humanizer
date: 2026-06-15
updated: 2026-06-16
tags: [Claude Code, 文章润色, Humanizer, AI去痕]
categories: [AI工具]
summary: "Humanizer-zh 是 Claude Code Skills 的中文 AI 写作去痕工具，由 op7418 翻译自 blader/humanizer，可识别并修复 24 种 AI 写作痕迹，帮助将 AI 生成内容改写得更自然、更像人类书写的文本，10.4k Stars。"
focus_keyword: "Claude Code Humanizer"
source: https://github.com/op7418/Humanizer-zh
author: "op7418（原版：blader/humanizer）"
status: draft
---

# Claude Code Humanizer：AI 写作去痕与文章可读性提升

> 识别并修复 24 种 AI 写作痕迹 | 10.4k Stars | MIT | Claude Code Skill

## 这是什么

Humanizer-zh 是一个面向中文内容的 AI 写作去痕工具，以 Claude Code Skills 形态运行。它是 op7418 将 blader/humanizer（基于维基百科 Signs of AI writing 指南）汉化并适配中文写作习惯的版本，参考了 hardikpandya/stop-slop 的实用工具部分。

工具能够识别并修复 **24 种** AI 写作痕迹，分为四大类：内容模式（6 种，如过度强调意义和媒体报道）、语言和语法模式（6 种，如"此外""至关重要"等 AI 高频词汇）、风格模式（6 种，如破折号过度使用、表情符号滥用）、以及交流模式和填充词（6 种，如协作交流痕迹、谄媚语气）。

与 Grammarly、DeepL Write 等通用润色工具不同，Humanizer-zh 专门针对"AI 味"进行系统化检测和替换，它的核心理念不是欺骗 AI 检测器，而是真正提升写作质量——让文字有真实的人类思考、观点和声音。工具提供具体示例对比和常见 AI 词汇警示列表，帮助写作者同时做到"干净"和"鲜活"。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 用 AI 辅助写作的内容创作者/自媒体 | ✅ 推荐 | 系统化去除 AI 味，提升文章可读性和真实性 |
| 编辑 / 审校人员 | ✅ 推荐 | 作为 AI 内容审阅辅助，快速定位典型的 AI 写作模式 |
| 学习写作的 AI 使用者 | ✅ 推荐 | 通过 24 种模式的反面教材，学习什么是好的自然写作 |
| 已有 Claude Code 环境的用户 | ✅ 推荐 | 即装即用，`/humanizer-zh` 一键调用 |
| 需要改写为完全人类风格的学术论文 | ⚠️ 酌情 | 可辅助去痕，但学术论文需保持专业性和引用严谨性，过度"人性化"可能适得其反 |
| 不使用 Claude Code 的用户 | ⚠️ 酌情 | 需手动参照 SKILL.md 中的规则自行审阅 |
| 试图"欺骗"AI 检测器的人 | ❌ 不推荐 | 工具的目标是提升写作质量，不是为了绕过检测系统 |

## 安装与前置条件

- **前置条件**：已安装 Claude Code CLI
- **无需额外 API Key 或依赖**

```bash
# 方式一：npx 一键安装（推荐）
npx skills add https://github.com/op7418/Humanizer-zh.git

# 方式二：Git 克隆
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh

# 方式三：手动安装
# 下载 ZIP 后解压到 ~/.claude/skills/humanizer-zh/
```

## 核心用法

### 直接调用技能

```text
/humanizer-zh 请帮我人性化以下文本：
[粘贴你的 AI 生成文本]
```

### 处理文件内容

```text
/humanizer-zh 请人性化 article.md 文件中的内容
```

### 关键原则（来自 SKILL.md）

- **有观点**：不要只报告事实，要对它们做出反应
- **变化节奏**：混合使用长短句
- **承认复杂性**：真实的人有复杂感受，不总是简单立场
- **适当使用"我"**：第一人称是诚实的表现
- **允许一些混乱**：完美的结构反而显得机械
- **对感受要具体**：用具体细节替代抽象概括

### 常见 AI 词汇警示列表

检测时会标记的高频 AI 词汇：此外、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、相互作用、复杂/复杂性、格局（抽象名词）、关键性的、展示、织锦（抽象名词）、证明、强调、宝贵的、充满活力的。

### 效果示例

```
改写前（AI 味）：
新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验。

改写后（人性化）：
软件更新添加了批处理、键盘快捷键和离线模式。来自测试用户的早期反馈是积极的。
```

## 注意事项与风险

- **不能替代人工判断**：工具检测规则基于常见模式，但高质量 AI 生成内容可能绕过检测，人类审阅仍然是最终保障
- **中文适配仍在完善**：部分英文模式在中文中表现不同（如标题大小写问题），翻译团队已调整了示例和表达
- **不适合所有文体**：技术文档、法律文件等需要精确表述的文体，过度"人性化"可能引入歧义
- **更新频率**：项目仅 6 次提交，属于轻量维护，核心规则依赖上游 blader/humanizer 的更新

## 与你现有工具的关系

- 与 [[Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]] 属于同一生态（Claude Code Skills），可在同一工作流中组合使用
- 用 [[../05-开发技术栈/GEOFlow：开源自托管 AI 内容生产系统]] 生成的文章，可再经 Humanizer-zh 做去痕处理后发布
- 本 Tags 目录下多个 Claude Code Skills 工具可形成「获取→生成→去痕→发布」的完整 AI 内容工作流

## FAQ

### Q: 能百分百去除 AI 痕迹吗？
A: 不能，也不应追求这个目标。工具的定位是提升写作质量和可读性，让文字更自然，而非制造"完美绕过检测"的内容。

### Q: 支持英文吗？
A: Humanizer-zh 专门为中文写作优化。如需处理英文，请使用原版 blader/humanizer，安装方式相同：`npx skills add https://github.com/blader/humanizer.git`。

### Q: 安装后如何使用？
A: 重启 Claude Code 后在对话中输入 `/humanizer-zh`，看到技能激活即可使用。也可以直接说"请用 humanizer 帮我改写这段话"。

### Q: 和 stop-slop 有什么关系？
A: Humanizer-zh 的核心规则文件翻译自 blader/humanizer，实用工具部分（核心规则、快速检查清单、质量评分）参考了 hardikpandya/stop-slop。

## 相关链接

- 来源：https://www.ahhhhfs.com/79176/
- GitHub：https://github.com/op7418/Humanizer-zh
- 英文原版：https://github.com/blader/humanizer
- stop-slop 参考：https://github.com/hardikpandya/stop-slop
- Wikipedia Signs of AI writing：https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
