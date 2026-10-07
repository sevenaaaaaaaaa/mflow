# Stack × Stack 重新定位 v2 — 查证后的真实定位

> 基于 Lovart 官方权威来源查证后的真实能力清单
> 纠正之前的错误理解

---

## 一、查证来源汇总（权威性等级）

| 来源 | 权威性 | URL | 内容 |
|------|:---:|------|------|
| **Lovart 官方 changelog** | ⭐⭐⭐⭐⭐ | https://www.lovart.ai/changelog | 2026-04-10 OpenClaw 集成公告 |
| **Lovart 官方 docs（Sanity `docs` 类型）** | ⭐⭐⭐⭐⭐ | docs/getting-started/chat-tools | OpenClaw 集成完整说明 |
| **Lovart Custom Skills 指南** | ⭐⭐⭐⭐⭐ | `02-wiki-custom-skills-guide` | Skill API 端点示例 + Skill Definition Language |
| Lovart 官方首页 | ⭐⭐⭐ | https://www.lovart.ai | 能力概述 |
| 第三方文章 / 我之前的推断 | ❌ | — | **不可靠，已纠正** |

---

## 二、已验证的真实能力

### 2.1 OpenClaw 集成 ✅ 官方权威

**官方 changelog 2026-04-10 原文**：
> "**OpenClaw × Lovart：在你熟悉的聊天工具里直接创作。** Lovart 现已支持通过 OpenClaw 接入使用。完成简单配置后，你可以直接在 **Feishu、Slack、Discord** 等聊天平台中调用 Lovart 进行创作..."

**官方 docs（chat-tools/OpenClaw）原文**：
> "**OpenClaw**: Connect and use Lovart with your OpenClaw agent. **Install the Lovart Skill into your OpenClaw environment**, authenticate with your Lovart keys, and chat with your Lovart Agent wherever your OpenClaw runs. You can then generate AI images directly in your OpenClaw workspace using Lovart's creative Agent."

**认证方式**：
- Lovart 提供 `access_key` + `secret_key`
- 安装方式：GitHub CLI 或 ClawHub one-click installer

**OpenClaw 是什么**（基于 Lovart docs 的描述）：
- **OpenClaw 是第三方本地 agent 平台**（类似 Claude Code 的本地 AI agent）
- Lovart 在 OpenClaw 里作为可安装的 Skill
- **OpenClaw 不是 Lovart 自家的 API 协议**
- OpenClaw 是 Lovart 集成的**外部 agent 环境**

### 2.2 Lovart Skill API ✅ 官方权威

**Custom Skills 指南原文**：
> "Trigger: How you invoke it (**command, button, API, schedule**)"

**API 调用示例**（`02-wiki-custom-skills-guide`）：
```
curl -X POST https://api.lovart.ai/v2/skills/skill_abc123/execute \
  -H "Authorization: Bearer ***" \
  -d '{"inputs": {"source_image": "design_xyz.png", "platforms": ["instagram"]}}'
```

**Skill 触发方式**：command / button / API / schedule 四种

### 2.3 Custom Skills（Self-Created）✅ 官方权威

**官方 changelog 2026-04-09**：
> "**Create Your Own Skills：把工作流沉淀为可复用能力。** 现在，你可以将一轮完整的对话工作流一键保存为 Skill，并在新的对话或项目中随时复用..."

**SDL（Skill Definition Language）**：
> "Write skills in Lovart's Skill Definition Language (SDL), a **YAML-based configuration format** with embedded AI prompt instructions."

### 2.4 ChatCanvas / Brand Kit / 多格式导出 ✅ 官方权威

- ChatCanvas — 对话式设计界面（来自 docs/getting-started）
- Brand Kit — 品牌套件统一管理（changelog 2026-04-03）
- 导出格式：PNG / JPEG / SVG / WebP / TIFF / EPS / PDF（含 CMYK/RGB）
- PSD 分层导出（changelog 2026-03-30）

### 2.5 批量生成 ✅ 官方权威

**`02-wiki-batch-generation-best-practices` 文档**：
> "up to 10x faster but requires more **API credits** per second"

Lovart 有「API credits」概念，但**不是通用 API**——只用于 Skill 执行。

---

## 三、未验证 / 推断错误（已纠正）

| ❌ 我之前的说法 | 真相 |
|--------------|------|
| 「Lovart 有面向 OpenClaw 的 API」 | **错误**。OpenClaw 是 Lovart 集成的第三方 agent 平台，Lovart 在其中作为 Skill 安装 |
| 「Lovart 应该按 MCP 协议封装」 | **未验证**。没有找到 Lovart 实现 MCP server 的证据。MCP 是行业趋势，但 Lovart 是否实现不明 |
| 「Lovart 与 Cursor/Claude/ChatGPT 通过 MCP 集成」 | **未验证**。OpenClaw 是 Lovart 的集成目标，但具体支持哪些 IDE / agent 工具需要进一步查证 |
| 「Lovart 通用 API（生成图像、Brand Kit 调用）」 | **未找到证据**。已知只有 Skill API（`api.lovart.ai/v2/skills/{id}/execute`） |

---

## 四、Stack × Stack 重新定位 v2

### 旧定位（基于错误推断）
「MCP 协议让 Lovart 被各种 agent 工具调用」

### 新定位（基于查证事实）

**Stack × Stack = 「Lovart 与 OpenClaw 生态工具 + 已验证的第三方协作场景」**

Lovart 的真实「被调用」路径：
1. **OpenClaw Skill**：Lovart 通过 Skill 集成到 OpenClaw
2. **OpenClaw 用户群**：Feishu / Slack / Discord 聊天平台用户
3. **第三方协作**（基于 Lovart 现有能力，**不是 API**）：
   - 多格式导出（PNG/JPEG/SVG/WebP/TIFF/EPS/PDF）
   - ChatCanvas 对话式输出（可被外部工具截图/OCR/链接）
   - Batch Generation（用户手动导出后可被其他工具批处理）
   - Brand Kit 共享（团队可下载 .lovart-brand-kit 文件）

### 新方向：4 篇样板 Stack × Stack

| # | 标题 | 真实可写性 |
|---|------|:---:|
| 1 | **Lovart + Slack/Discord/Feishu via OpenClaw：在聊天群里调用 Lovart 生成设计** | ✅ 有官方支持 |
| 2 | **Lovart + Premiere/Final Cut：导出 PSD 分层 + 多格式视频帧** | ✅ 有官方导出 |
| 3 | **Lovart + Figma：导出 SVG 矢量，导入 Figma 继续设计** | ✅ 有官方导出 |
| 4 | **Lovart + Zapier/Make：手动导出后批处理自动化** | ⚠️ 部分可行 |

**不写**（除非用户能提供 Lovart 通用 API 文档）：
- ❌ Lovart + Cursor（没有 Lovart 通用 API 证据）
- ❌ Lovart + Shopify API 直连（没有证据）
- ❌ Lovart + n8n API 直连（没有证据）

---

## 五、写作纪律（来自这次教训）

### 5.1 严禁无证据推断

- **MCP、Cursor、通用 API** 等说法**必须先查证 Lovart 官方文档 / changelog / GitHub**
- 查不到证据就**老实写「未找到公开文档，需向 Lovart 团队确认」**
- 不要为了「听起来合理」就编造 API 端点、命令、协议

### 5.2 每篇 Stack × Stack 写作前必须确认

1. **Lovart 这一端的官方能力**（changelog/docs/wiki 三选一）
2. **外部工具那一端的官方能力**（官方文档/GitHub）
3. **两者的集成点是 Lovart 提供还是外部工具提供**（导入/导出/插件/Skill/API）
4. **真实可运行的步骤**（如果 Lovart 没有 API，就只能写「手动导出 + 外部工具批处理」，不能编造 `curl https://api.lovart.ai/...`）

### 5.3 数据来源等级

| 等级 | 来源 |
|:---:|------|
| A | Lovart 官方 changelog / 官方 docs（Sanity `docs` 类型） |
| B | Lovart 内部 wiki 文档（Sanity `blog` 02-wiki 系列） |
| C | Lovart 官方首页 / 定价页 |
| D | 用户口述 / 我推断 |

只有 A/B/C 级来源可以直接引用到 Stack × Stack 文章。D 级来源必须标注「未官方确认」或绕过不写。

---

## 六、立即行动

### 6.1 修订 Stack × Stack 样板 1（已发布）

`lovart-midjourney-brand-asset-workflow` —— 这篇**没有引用未验证的 Lovart API**，是写「Midjourney 概念 + Lovart ChatCanvas/Touch Edit 精修」的工作流，方向没问题，可以保留。

### 6.2 重写样板 2 方向

原计划：Lovart + Cursor（MCP）—— ❌ 取消，没有证据
新方向：**Lovart + Slack via OpenClaw —— 在 Slack 群里通过 OpenClaw 调用 Lovart 生成设计**

这是有官方 changelog 支持的真实集成场景。

---

**结论**：OpenClaw 是 Lovart 的真实集成路径，不是 API 协议名。Stack × Stack 内容必须围绕 OpenClaw + 官方支持的导出格式展开，不编造 MCP/通用 API 调用。