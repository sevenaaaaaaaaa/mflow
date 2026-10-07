---
title: "Aye：谷歌浏览器里的实习生"
slug: aye-ai-chrome-browser-intern
date: 2026-05-26
updated: 2026-05-29
tags: [Aye, AI浏览器, Chrome, 网页Agent, macOS, Windows, Skill]
categories: [AI工具]
summary: Aye 是 Oka Apps 推出的免费 AI 浏览器（Chrome 内核），内置网页总结、翻译、视频/图片批量下载与网页 Agent，并支持公众号、小红书、邮件等日常自动化；Mac/Windows 应用商店可直接安装，官方 Skill 征集有百元红包激励。
focus_keyword: Aye
source: https://x.com/okasupportgroup/status/2059177027245408672?s=20
author: 小七 (@okasupportgroup / Oka Apps)
status: draft
---

# Aye：谷歌浏览器里的实习生

> 免费 | Mac App Store + Microsoft Store | Chrome 内核 | 附 30 秒演示视频

## 这是什么

**Aye**（「谷歌浏览器里的实习生」）是 [@okasupportgroup](https://x.com/okasupportgroup)（小七 / [Oka Apps](https://okaapps.com)）于 2026-05-26 宣布上线的新产品。定位是带 AI 能力的桌面浏览器，而非单纯 Chrome 插件。

推文强调：

- **浏览器底座**：Chrome 内核；常见 Tab 管理、侧边栏 Tab、广告拦截已内置开启（作者注明目前尚不能完全替代 Chrome）。
- **AI 能力**：网页内容总结与翻译；视频下载、图片批量下载；网页 Agent 辅助。
- **日常自动化**：发布公众号、小红书，查看评论区，回复邮件等。
- **分发**：已上架 Mac 与 Windows 应用商店，商店内搜索「Aye」即可安装；当前**完全免费**，欢迎测试反馈。
- **社区激励**：若你创建的 **Skill** 被采纳进入官方 Skill 库，可获得**百元红包**（需私信作者）。

本条推文**未附 GitHub 仓库**；下载入口为应用商店链接（见下方）。作者同账号亦运营 VidHub 等 Apple 生态应用。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要「浏览器 + AI 总结/翻译」一体、不愿折腾插件的用户 | ✅ 推荐 | 商店一键安装，免费试用 |
| 常做公众号、小红书、邮件与评论区等网页内重复操作 | ✅ 推荐 | 推文明确覆盖这些场景 |
| 已有成熟 Chrome 工作流、只需 CLI/脚本自动化 | ⚠️ 酌情 | 见 [[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]、[[../03-效率生产力/让 AI 替你操作网页：x-cli + Scrapling 实战指南]] |
| 需要完全替代 Chrome 作为主浏览器 | ❌ 暂不推荐 | 作者自述目前还不能完全替换 Chrome |
| 依赖开源可审计代码或自托管 | ❌ 不适用 | 闭源桌面应用，无公开 repo |

## 安装与前置条件

- **平台**：macOS、Windows（应用商店分发）
- **费用**：当前免费（推文未说明后续定价）
- **网络**：需能访问各 AI/网页服务（具体模型与后端未在推文中披露）

```text
# Mac App Store
https://apps.apple.com/cn/app/id6760281977

# Microsoft Store (Windows)
https://apps.microsoft.com/detail/9ndw5t4cs476
```

也可在 Mac / Windows 应用商店内搜索 **Aye** 直接安装。

## 核心用法

### 浏览器与 Tab

- Chrome 内核浏览
- Tab 管理、侧边栏 Tab
- 内置广告拦截（默认开启）

### AI 与 Agent

| 能力 | 说明（据推文） |
|------|----------------|
| 网页总结 / 翻译 | 阅读外文或长文时的辅助 |
| 媒体下载 | 视频下载、图片批量下载 |
| 网页 Agent | 在页面内辅助完成多步操作 |
| 自媒体与沟通 | 公众号、小红书发布；评论区查看；邮件回复等 |

### 官方 Skill 征集

- 自认 Skill 质量不错的用户可**私信** @okasupportgroup
- 采纳进入**官方 Skill** 后，作者承诺**百元红包**奖励
- 与跨平台 Skill 管理工具 [[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]] 不同：此处为 Aye 产品内生态，非 Anthropic Agent Skills 规范

## 注意事项与风险

- **产品成熟度**：不能视为 Chrome 完整替代品；重度扩展/开发者工具用户需自行验证
- **隐私与合规**：浏览器可访问登录态与页面内容；自媒体、邮件自动化涉及账号安全与平台 ToS，使用前请确认各平台规则
- **Skill 激励**：红包与采纳标准以作者私信沟通为准，推文未写细则
- **信息来源**：正文来自 2026-05-26 推文与 fxtwitter 镜像解析；**无**公开 GitHub、技术白皮书或 API 文档链接
- **抓取说明**：Twitter 官方 syndication API 返回空对象；正文通过 **fxtwitter** 公共 API 获取（见文末「相关链接」）

## 与你现有工具的关系

| 场景 | 可衔接笔记 |
|------|------------|
| 登录态网页 CLI、订酒店/搜房等 | [[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]、[[../03-效率生产力/让 AI 替你操作网页：x-cli + Scrapling 实战指南]] |
| 全自动热点抓取 + 多平台发文（开源 Django） | [[AIMedia：全自动 AI 媒体创作与多平台发布]] |
| Cursor/OpenCode 等平台 Skill 文件管理 | [[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]]、[[../01-AI-Agent生态/codex-ppt-skill：图片式 PPT 生成 Skill]] |
| 桌面 Agent 工作台（另一路线） | [[../01-AI-Agent生态/DeepSeek GUI：桌面智能体工作台]] |

Aye 偏向**自带 AI 的浏览器壳**；x-cli 偏向**外部 Agent 驱动已有 Chrome**；AIMedia 偏向**后端流水线式自媒体**。按你是否愿意把主浏览入口换成 Aye 来选型。

## FAQ

### Q: Aye 有 GitHub 开源地址吗？
A: 本条推文未提供。已知入口为 Mac/Windows 应用商店与作者站点 [okaapps.com](https://okaapps.com)。

### Q: 和 Chrome + 插件方案有何不同？
A: Aye 是独立安装的 AI 浏览器（Chrome 内核），内置 Tab/广告拦截与 AI/Agent 能力；无需自行拼装多个扩展，但可定制性可能低于纯 Chrome 生态。

### Q: 官方 Skill 和 Cursor Skill 是一回事吗？
A: 不是。推文指 Aye 产品内的「官方 Skill」征集与红包激励；与 [[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]] 管理的 `~/.cursor/skills/` 等目录无直接关联。

### Q: 推文数据可信吗？
A: 正文经 fxtwitter API 校验（作者小七、发布时间 2026-05-26、含演示视频链接）。功能细节以安装后实际体验为准。

## 相关链接

- 推文原文：https://x.com/okasupportgroup/status/2059177027245408672?s=20
- Mac 下载：https://apps.apple.com/cn/app/id6760281977
- Windows 下载：https://apps.microsoft.com/detail/9ndw5t4cs476
- 作者站点：https://okaapps.com
- 本库相关笔记：[[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]、[[../03-效率生产力/让 AI 替你操作网页：x-cli + Scrapling 实战指南]]、[[AIMedia：全自动 AI 媒体创作与多平台发布]]、[[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]]
