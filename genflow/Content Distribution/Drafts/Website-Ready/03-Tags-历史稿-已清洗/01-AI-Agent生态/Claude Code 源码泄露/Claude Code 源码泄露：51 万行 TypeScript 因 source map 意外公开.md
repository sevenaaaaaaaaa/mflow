---
title: "Claude Code 源码泄露：51 万行 TypeScript 因 source map 意外公开"
slug: claude-code-sourcemap-leak-v2188
date: 2026-06-01
updated: 2026-05-29
tags: [Claude Code, Anthropic, source-map, npm, AI Agent, 安全]
categories: [AI工具]
summary: 2026 年 3 月 31 日 @anthropic-ai/claude-code v2.1.88 误带 59.8MB cli.js.map，约 1900 文件、51.2 万行 TS 源码被还原。事件非官方开源，适合研究 Agent 架构与 npm 发布安全，普通用户无直接数据风险。
focus_keyword: Claude Code 源码泄露
status: draft
---

# Claude Code 源码泄露：51 万行 TypeScript 因 source map 意外公开

> 非官方开源 | @anthropic-ai/claude-code v2.1.88 | Bun + React 19 + Ink | 约 512k 行 TS

## 这是什么

2026 年 3 月 31 日，Anthropic 在 npm 发布 **Claude Code CLI** 的 `@anthropic-ai/claude-code@2.1.88` 时，误将约 **59.8 MB** 的 `cli.js.map`（Source Map）打进生产包。该文件在 `sourcesContent` 字段内嵌了完整未混淆的 **TypeScript 源码**，社区可在数小时内还原并镜像到 GitHub。

**这不是官方开源**：Claude Code 仍为 Anthropic 专有软件；泄露的是**客户端 CLI 实现**，不含模型权重、训练数据或用户对话内容。安全研究员 **Chaofan Shou（@Fried_rice）** 在 X 上率先披露；Anthropic 随后下架问题版本并回退发布流程，称系**打包人为失误**，非入侵式安全事件。

公众号原文（`mid=2247485583`）在 2026-06-01 前后传播，常见叙事为「意外开源」「.map 引发史诗级泄露」；与腾讯云开发者社区、36 氪、少数派等转载标题一致。**微信正文未能抓取**（见「注意事项」），下文步骤与架构要点来自 npm 包事实、公开技术分析与社区归档仓库。

### 泄露规模（社区统计，约）

| 项目 | 数值 |
|------|------|
| 问题版本 | v2.1.88 |
| Map 文件 | `cli.js.map` ≈ 59.8 MB |
| 源文件数 | ~1,900 |
| 代码量 | ~512,000 行 TypeScript |
| 技术栈 | Bun 构建、React 19 + Ink 终端 UI、Node ≥18 |

### 时间线（公开报道整理）

1. **2025-02**：v0.2.8 曾因 inline source map 发生过一次类似泄露，v0.2.9 修复
2. **2026-03-26**：Anthropic CMS 配置问题，曾曝光未发布模型相关草稿（另一起事件）
3. **2026-03-31 14:00 左右**：发布 v2.1.88 至 npm
4. **2026-03-31 傍晚**：@Fried_rice 披露 map 内含完整源码
5. **数小时内**：GitHub 出现大量归档/分析仓库，社区拆解 Agent 架构
6. **2026-03-31～04-01**：Anthropic 撤下 v2.1.88，推进 v2.1.89+；官方称无用户凭据泄露

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 做 AI Agent / CLI 产品的工程师 | ✅ 推荐 | 罕见机会对照「生产级 Agent  harness」实现 |
| 使用 Claude Code / Cursor 的开发者 | ✅ 了解即可 | 知悉事件性质与版本风险，无需自行还原源码 |
| 关注 npm 供应链与发布安全的团队 | ✅ 推荐 | `.npmignore` / `npm pack --dry-run` 教训典型 |
| 想 fork 商用或冒充官方发行版 | ❌ 不推荐 | 专有代码，无法律授权；可能违反 ToS |
| 期待拿到模型权重或 API 密钥 | ❌ 不适用 | 泄露范围仅为 CLI 客户端源码 |

## 安装与前置条件

### 普通用户（继续使用官方 Claude Code）

- 使用 **npm 上当前稳定版**（避免锁定已下架的 `2.1.88`）
- 官方包：`npm install -g @anthropic-ai/claude-code`
- 需 Anthropic 账号 / API 或订阅，与本次泄露无直接关系

### 研究还原（仅限学习，注意合规）

**前置**：Node.js 18+、理解 Source Map 与知识产权边界。

```bash
# 仅作技术说明：从曾发布的 tarball 中提取 map（版本可能已从 registry 移除）
npm pack @anthropic-ai/claude-code@2.1.88   # 若 registry 仍缓存则可行；多数环境已不可用
tar -xzf anthropic-ai-claude-code-2.1.88.tgz
# 解析 package/cli.js.map 中的 sourcesContent → 还原目录树
```

社区已提供还原脚本与镜像，例如（**非 Anthropic 官方**）：

- [Hyper66666/claude-code-sourcemap](https://github.com/Hyper66666/claude-code-sourcemap)（中文说明 + 提取脚本）
- [Exhen/claude-code-2.1.88](https://github.com/Exhen/claude-code-2.1.88)（从 npm 包提取的归档）
- [soufianebouaddis/claude-code](https://github.com/soufianebouaddis/claude-code)（事件分析与备份）

**不要**将还原代码用于二次分发闭源产品或绕过官方更新渠道。

## 核心用法

### 1. 理解泄露成因（发布侧）

典型链条（多家技术分析一致）：

1. Claude Code 使用 **Bun** 打包（Bun 默认可生成 Source Map）
2. 生产发布未在 `.npmignore` 排除 `*.map`，或 `package.json` 的 `files` 未收紧
3. `cli.js.map` 含 `sourcesContent` → 下载 npm 包即可还原全部 TS

**防护检查清单（任何 TS/JS 库发布可参考）**：

```bash
# 发布前在 CI 中执行
npm pack --dry-run 2>&1 | grep -E '\.map$' && echo 'FAIL: map in tarball' && exit 1
```

```toml
# bunfig.toml 示例：生产禁用 sourcemap
[build]
sourcemap = "none"
```

### 2. 从泄露源码能学到什么（架构向）

社区逆向与论文式综述（基于 v2.1.88 快照）普遍提到：

| 模块 | 要点 |
|------|------|
| Agent 主循环 | `query.ts` 等实现的流式 async generator：组上下文 → 调模型 → 并发执行工具 |
| 工具系统 | 数十个内置工具（Bash、读写文件、子 Agent 等），统一 schema（如 Zod） |
| 权限与安全 | `permissions.ts` deny-first；`yoloClassifier.ts` 小模型辅助自动批准低风险命令 |
| 上下文压缩 | 多阶段 compaction（snip / micro-compact / auto-compact 等）应对长会话 |
| 扩展 | MCP、Plugins、Skills 发现；大量 **feature flag**（GrowthBook 等）控制灰度能力 |
| UI | React 19 + Ink 终端渲染 |

这些洞察用于**学习 Agent 工程设计**，不代表未来官方 API 仍与泄露快照一致。

### 3. 与普通开发者的关系

- **无需**为了日常写代码去克隆泄露仓库；继续用官方 CLI + [[Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 约束 Agent 行为即可。
- **建议**检查本机/CI 是否误锁 `2.1.88`；企业镜像 npm 时应屏蔽该版本。
- **可选**阅读社区架构笔记（Gist / 博客园复盘）替代直接啃 51 万行源码。

## 注意事项与风险

- **微信抓取限制**：`WebFetch` 超时；`curl`（含 MicroMessenger UA）与 [r.jina.ai](https://r.jina.ai/) 均返回验证码/环境异常页；`mp/appmsgshow` 对该 `__biz` 无 JSON 响应；搜狗微信未索引该 `sn`。**本文主题依据**：分享日期（`srcid=0601`）、同期全网热文与 npm 可验证事实；**公众号具体标题、排版与独家评论请在微信客户端打开原文核对**。
- **法律与合规**：源码属 **Anthropic 专有**；研究、归档在多地可能触及许可与 DMCA；勿商用或冒充官方分支。
- **安全**：不含用户数据与 API Key；但泄露的权限逻辑、未发布 feature flag 名称等可被攻击者研究**客户端行为**（非云端模型）。
- **误传**：X 上曾出现「发布工程师被解雇」等帖，有媒体指部分账号**非 Anthropic 员工**，勿当作官方声明。
- **重复踩坑**：公开时间线显示约 13 个月内 **两次** source map 类失误，说明发布流水线仍需自动化拦截 `.map`。

## 与你现有工具的关系

- **Claude Code 用户**：与 [[skills-manage：20+ 平台 Agent Skills 中央统一管理]] 中 Claude Code Skills 目录（`~/.claude/skills/`）同一工具链；泄露不改变 Skill 安装方式。
- **Codex 生态**：[[codex-plusplus：给你的 Codex 装上插件系统]]、[[codex-ppt-skill：图片式 PPT 生成 Skill]] 面向 OpenAI Codex；可对比两家 **CLI Agent 壳层** 设计差异（泄露的是 Claude 侧）。
- **Agent 人格库**：[[The Agency：105k Star 的 AI Agent 专家库]] 提供 prompt/人格；泄露代码展示的是 **运行时 harness**（工具、权限、压缩），二者互补。
- **规范**：[[Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 适用于任何编码 Agent，包括 Claude Code。
- **枢纽**：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]。

## FAQ

### Q: 这次算 Claude Code 开源了吗？
A: 不算。没有开源许可证，Anthropic 未授权再分发；属于**意外泄露的专有客户端源码**，npm 问题版本已下架。

### Q: 我需要卸载 Claude Code 吗？
A: 一般不需要。确保使用 **2.1.88 之后**的官方 npm 版本即可；泄露不意味着你的本机被植入恶意代码。

### Q: 能从源码里拿到免费 API 或绕过订阅吗？
A: 不能。CLI 仍需正常鉴权；泄露的是本地客户端逻辑，不是云端模型或计费系统。

## 相关链接

- 微信原文（需在微信内打开）：
- 官方 npm（请用当前版本）：https://www.npmjs.com/package/@anthropic-ai/claude-code
- 披露帖（X）：https://x.com/fried_rice/status/2038894956459290963
- 社区归档示例：https://github.com/Hyper66666/claude-code-sourcemap
- 技术分析（腾讯云社区转载）：https://cloud.tencent.com/developer/article/2653742
- 本库相关笔记：[[Karpathy 编码行为准则：AI Agent 的 4 条铁律]]、[[skills-manage：20+ 平台 Agent Skills 中央统一管理]]、[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
