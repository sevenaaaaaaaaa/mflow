# Agent 规则注入 — 部署指南

> 本文档说明如何将生成的配置文件部署到各 Agent 平台。
> 所有待部署文件位于 `deploy/` 目录下。

---

## 部署清单

### ✅ 已自动部署（无需手动操作）

| 文件 | 目标位置 | 状态 |
|------|---------|------|
| `lovart-seo-report-iron-rules.mdc` | `1-4 Dev/.cursor/rules/` | ✅ 已部署 |
| `lovart-content-anti-slop.mdc` | `1-4 Dev/.cursor/rules/` | ✅ 已部署 |

### ⚠️ 需手动部署（沙箱限制，请复制）

| # | 源文件 | 目标位置 | 平台 | 操作 |
|---|--------|---------|------|------|
| 1 | `deploy/opencode.jsonc` | `~/.config/opencode/opencode.jsonc` | OpenCode + Hermes | **替换**现有文件（已备份为 .bak） |
| 2 | `deploy/CLAUDE.md` | `1-Project/CLAUDE.md` | Claude Code | **新建** |
| 3 | `deploy/trae-project-rules.md` | `1-Project/.trae/rules/project_rules.md` | Trae Work | **新建**（需先创建 `.trae/rules/` 目录） |

### 📋 无需文件部署（应用内配置）

| 平台 | 操作 |
|------|------|
| **DeepSeek GUI** | 在应用内"系统提示"框粘贴 `deploy/deepseek-system-prompt.md` 内容 |
| **OpenClaw** | 在 `~/.openclaw/openclaw.json` 中添加 memory 配置（见下方） |
| **micode (MiMo Code)** | 在项目目录执行 `/init`，然后将生成的 AGENTS.md 替换为 SSOT 引用 |

---

## 详细部署步骤

### 1. OpenCode（影响 OpenCode + Hermes）

```bash
# 备份现有配置
cp ~/.config/opencode/opencode.jsonc ~/.config/opencode/opencode.jsonc.bak.$(date +%Y%m%d)

# 复制新配置
cp deploy/opencode.jsonc ~/.config/opencode/opencode.jsonc

# 验证
cat ~/.config/opencode/opencode.jsonc
```

**变更内容**：
- 新增 `instructions` 字段，指向 AGENTS.md 和 WORKFLOWS.md（每会话自动加载）
- `skills.paths` 新增 Lovart Harness Skills 目录

### 2. Claude Code

```bash
# 复制到项目根目录
cp deploy/CLAUDE.md "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/CLAUDE.md"
```

**变更内容**：
- 使用 `@path` 语法自动导入 AGENTS.md 和 WORKFLOWS.md（非"请读 XX"）
- 包含操作前必检清单

### 3. Trae Work

```bash
# 创建规则目录
mkdir -p "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/.trae/rules"

# 复制规则文件
cp deploy/trae-project-rules.md "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/.trae/rules/project_rules.md"
```

### 4. DeepSeek GUI

在 DeepSeek GUI 的"系统提示"输入框中粘贴以下精简版铁律（50 行以内）：

```
你是 Lovart SEO 内容营销项目的 AI 助手。必须遵守以下铁律：

【Sanity 管道】
- 禁止 sanity deploy
- 禁止 --replace（必须 --missing + patch）
- 禁止修改 schemaTypes
- 禁止删除 production 文档

【SEO 报告】
- 所有报告所有维度必须有环比（绝对变化 + 百分比）
- 月报 V2 固定 13 章节，每节末有洞察 + 年均对比
- 竞品词库 265 全量 + 36 核心（不可编造）

【内容质量】
- 每段内容必须回答：谁会读 / 为什么读 / 读完改变什么 / 下一步
- 禁止编造数据、禁止占位符、禁止关键词堆砌
- 多语言是重写而非翻译
- BLOCK 条件出现即不可发布

详细规则见项目目录下 AGENTS.md。
```

### 5. OpenClaw

在 `~/.openclaw/openclaw.json` 中添加 memory 配置（如果文件不存在则创建）：

```json
{
  "memory": {
    "enabled": true,
    "flush": true,
    "search": true
  }
}
```

OpenClaw 会自动读取工作区中的 `AGENTS.md`，无需额外配置。

### 6. micode (MiMo Code)

```bash
# 进入项目目录
cd "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project"

# 初始化（自动生成 AGENTS.md + MEMORY.md）
mimo
# 然后输入 /init

# 将生成的 AGENTS.md 替换为指向 SSOT 的引用
```

---

## 验证清单

部署完成后，按以下清单验证：

| 平台 | 验证方式 | 预期结果 |
|------|---------|---------|
| OpenCode | 新建会话，问"铁律有哪些" | Agent 能回答 Sanity 禁令 + 环比总则 |
| Claude Code | 新建会话，问"月报结构是什么" | Agent 能回答 13 章节结构 |
| Cursor | 新建会话，问"Anti-Slop 是什么" | Agent 能回答 7 种 AI 泔水表现 |
| Trae Work | 新建会话，问"项目规则" | Agent 能列出铁律 |
| DeepSeek GUI | 发送"帮我写篇博客" | Agent 应先确认读者角色和搜索意图 |
| OpenClaw | 新建会话，检查 memoryFlush | 长对话后 MEMORY.md 有新条目 |
| micode | 新建会话，检查 MEMORY.md | 项目知识已持久化 |
| Hermes | 发送"weekly ops" | Agent 遵循系统提示中的行为规则 |

---

## 后续优化（P2-P3）

- [ ] 安装 agentmemory MCP 服务（跨平台统一记忆）
- [ ] AGENTS.md 拆分为总控 + 子文件（提高长文件遵循率）
- [ ] Skill SKILL.md 加入强制前置检查（按需精准加载）
- [ ] DeepSeek GUI 系统提示定期更新（跟随 AGENTS.md 变更）
