# Stack × Stack 重新定位 v3 — 基于完整官方 User Guide

> 三份权威来源全部查证完毕。本报告修正 v1/v2 的所有错误。
> 来源 1: Lovart 官方 changelog（已抓取）✅
> 来源 2: Lovart 官方 OpenClaw User Guide（用户提供完整文本）✅
> 来源 3: ~~Custom Skills 指南中的 API 描述~~ ❌ **不可用**——GPT 拼接的伪代码示例

---

## 一、来源查证状态

| # | 来源 | 状态 | 内容 |
|---|------|:---:|------|
| 1 | Lovart 官方 changelog https://www.lovart.ai/changelog | ✅ 已抓取 | 2026-04-10 「OpenClaw × Lovart」公告 |
| 2 | Lovart 官方 OpenClaw User Guide（用户提供的 Lovart 官方文档全文）| ✅ 全文 | 4 步安装指南（已保存到本地 `_lovart-openclaw-official-guide.md`）|
| 3 | Lovart Custom Skills 指南中的 API 调用示例（`api.lovart.ai/v2/skills/...` curl）| ❌ **不可用** | 这是 GPT 在对话中拼接出来的「看起来合理」的伪代码示例，文档实际内容是 SDL（YAML）+ Skill Builder 拖拽界面，**没有公开 REST API 示例** |

---

## 二、Lovart OpenClaw 真实集成路径（基于 User Guide）

### 2.1 用户安装步骤

1. **选择运行环境**（三种 host）：
   - **OpenClaw Desktop（本地）** — 最强大的本地运行方式
   - **Discord / Telegram Integrations** — 通过 OpenClaw Discord gateway 或 Telegram bot 包装器
   - **Slack Agent** — 优化用于专业 workspace 协作

2. **安装 Lovart Skill**（两种方式）：
   - **GitHub CLI**: `npx skills add lovartai/lovart-skills`
   - **ClawHub one-click installer**: `https://clawhub.ai/lovart-admin/lovart-skill`

3. **认证（access_key + secret_key）**：
   - 在 Lovart.ai 账号 Settings 页面获取
   - 设置环境变量：`LOVART_ACCESS_KEY` 和 `LOVART_SECRET_KEY`

4. **创建内容**：
   - 推荐模型：GPT-5.4 / Claude 4.6 / Gemini 3.1
   - 上传图片/视频作为参考

### 2.2 关键事实澄清

| 项目 | 真相 |
|------|------|
| **OpenClaw 是什么** | **第三方本地 agent 平台**——可作为 desktop、Discord gateway、Telegram bot、Slack agent |
| **Lovart 在 OpenClaw 中的角色** | **Skill 包**——通过 GitHub CLI 或 ClawHub 安装 |
| **认证方式** | access_key + secret_key（环境变量或 chat 输入）|
| **Lovart 公开 API** | ❌ **没有**——Lovart 不向 Skill 之外公开 REST API。能力通过 Skill 暴露给 OpenClaw 环境 |
| **Lovart 调用方式** | 用户在 OpenClaw 聊天中描述需求，Lovart Skill 解析并生成 |
| **推荐模型** | GPT-5.4 / Claude 4.6 / Gemini 3.1（OpenClaw 用这些模型 + Lovart Skill）|

### 2.3 集成架构

```
┌─────────────────────────────────────────────┐
│  OpenClaw Desktop / Discord / Telegram / Slack│
│  ┌──────────────────────────────────────────┐│
│  │  OpenClaw Agent (GPT-5.4 / Claude 4.6)  ││
│  └──────────────┬───────────────────────────┘│
│                 ↓ 解析需求                    │
│  ┌──────────────────────────────────────────┐│
│  │  Lovart Skill (installed from ClawHub) ││
│  │  - 图像生成 / 编辑                       ││
│  │  - 视频生成                              ││
│  │  - Brand Kit 应用                        ││
│  │  - 导出多格式资产                        ││
│  └──────────────┬───────────────────────────┘│
│                 ↓ 调用 Lovart 后端            │
└─────────────────┼─────────────────────────────┘
                  ↓
       Lovart 后端 (Lovart.ai)
       - 多模型 (Luma, GPT Image 2.0, Seedance 2.0, Kling 2.6, Nano Banana Pro)
       - Brand Kit 持久化
       - ChatCanvas 渲染
       - 多格式导出
```

---

## 三、Stack × Stack 内容方向（基于真实集成）

### 3.1 可写方向（有官方支持）

| 方向 | 真实可写性 | 数据来源 |
|------|:---:|------|
| **Lovart + Slack via OpenClaw Slack Agent** | ✅ | User Guide 明确「Slack Agent: Optimized for professional workspace collaboration」 |
| **Lovart + Discord via OpenClaw Discord gateway** | ✅ | User Guide 明确「Discord/Telegram Integrations」 |
| **Lovart + Telegram via OpenClaw Telegram bot wrapper** | ✅ | 同上 |
| **Lovart + Claude/GPT/Gemini via OpenClaw Desktop** | ✅ | User Guide 推荐 GPT-5.4 / Claude 4.6 / Gemini 3.1 |
| **Lovart Skill 输出 + 外部工具（基于多格式导出）** | ✅ | 官方导出 PNG/JPEG/SVG/WebP/TIFF/EPS/PDF/PSD |

### 3.2 不写方向（无官方支持）

| ❌ 方向 | 原因 |
|------|------|
| Lovart + Cursor（直接集成）| ❌ 没有 Cursor MCP server 证据 |
| Lovart + n8n / Zapier（直接 API 集成）| ❌ Lovart 没有公开 REST API |
| Lovart + Shopify（产品页自动生成）| ❌ 没有 API 集成证据 |
| Lovart + Notion（数据库→视觉）| ❌ 没有 API 集成证据 |
| Lovart MCP server | ❌ 没有证据 |

### 3.3 改写样板 1 方向（替换第一篇样板）

第一篇样板「Lovart + Midjourney 草图 → 可编辑资产」**保留**——这个方向是用户用 Midjourney 生成概念图，导出 JPG，导入 Lovart ChatCanvas 精修，全程不依赖 Lovart 公开 API。Lovart 在该工作流中只承担「精修 + 导出」职责，**完全符合实际能力**。

### 3.4 样板 2 方向（新建）

**标题候选**：

1. **Lovart + Slack via OpenClaw: Generate Design Assets Directly in Your Team Chat**
2. **Lovart + Claude Desktop: How to Install Lovart Skill Locally via OpenClaw**
3. **Lovart + Discord for Creative Teams: Set Up a Design Bot in 10 Minutes**

**推荐样板 2**：`Lovart + Claude Desktop: How I Run Lovart Locally via OpenClaw`

写作角度（基于真实步骤）：
1. **Hook**：远程 AI 设计工具的数据隐私问题（客户品牌资产上传到 Lovart 云端的担忧）
2. **Why OpenClaw Desktop**：本地运行，数据不出本机
3. **4 步安装**（完全照搬 User Guide）：
   - Step 1: 装 OpenClaw Desktop（机器要求：GPU/CPU/Memory）
   - Step 2: `npx skills add lovartai/lovart-skills` 或 ClawHub
   - Step 3: 设置 LOVART_ACCESS_KEY / LOVART_SECRET_KEY 环境变量
   - Step 4: 聊天生成，第一个项目（推荐模型 Claude 4.6）
4. **真实案例**：本地运行 vs 云端的速度/隐私/成本对比
5. **When NOT to use**：需要云端协作、需要分享、不在本地时
6. **Master Stack**：OpenClaw Desktop / Slack Agent / Discord gateway 三种 host 选择

### 3.5 样板 3 方向（新建）

**Lovart + Discord for Creative Teams: A Design Bot in 10 Minutes**

写作角度：
- Discord 团队频道装 Lovart Skill 的实际步骤
- 在 Discord 频道用 chat 描述需求，团队成员共同看到生成过程
- 与 Slack Agent 对比：Discord 适合社区/创意社区，Slack 适合企业

---

## 四、内容写作纪律（v3 更新）

### 4.1 三级证据等级

| 等级 | 可写引用 | 来源 |
|:---:|:---:|------|
| A | ✅ 直接引用 | Lovart 官方 changelog / 官方 docs / OpenClaw User Guide |
| B | ⚠️ 谨慎引用 | Lovart 内部 wiki（Sanity blog `02-wiki-*` 系列）|
| C | ❌ 不引用 | 第三方文章 / 我推断 / 用户口述 |

### 4.2 禁止事项

- ❌ 引用 `api.lovart.ai/v2/skills/...` 这样的 REST 端点——User Guide 里没有此示例，是伪造的
- ❌ 引用 MCP server / 通用 API——没有证据
- ❌ 引用 ChatGPT 通用做法说成 Lovart 官方推荐

### 4.3 必须包含的事实

每篇 Stack × Stack 必须引用：
1. **OpenClaw 集成方式**（GitHub CLI `npx skills add lovartai/lovart-skills` 或 ClawHub）
2. **认证方式**（access_key + secret_key + 环境变量）
3. **真实运行环境**（OpenClaw Desktop / Discord / Telegram / Slack 四选一）
4. **Lovart 真实能力**（多模型集成、Brand Kit、多格式导出）

---

## 五、立即行动

1. ✅ User Guide 已保存到 `Output/SEO-Reports/Blog List/_lovart-openclaw-official-guide.md`
2. ✅ 之前发布的样板 1（Lovart + Midjourney）不需要修改——它不依赖 Lovart 公开 API
3. 🔜 样板 2（新建）：Lovart + Claude Desktop via OpenClaw
4. 🔜 样板 3（新建）：Lovart + Discord for Creative Teams
5. ⏸️ 模板定制 skill（`lovart-stack-x-stack`）待 User Guide 信息整合后写

**用户确认后开始样板 2 写作。**