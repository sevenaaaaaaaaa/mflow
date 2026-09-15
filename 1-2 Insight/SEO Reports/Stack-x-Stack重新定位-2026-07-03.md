# Stack × Stack 重新定位 + 写作策略

> 基于 Lovart 真实能力（OpenClaw API + Custom Skills）和竞品 MCP 生态调研
> 取代之前的「两个外部工具协作」定位

---

## 一、关键发现

### 1.1 Lovart 真实能力（已验证）

从官方文档、Sanity 数据库和 Custom Skills 指南综合：

| 能力 | 验证来源 |
|------|---------|
| **OpenClaw API** | 用户描述 + 具备面向 agent 的 API |
| **Custom Skills** | `02-wiki-custom-skills-guide` — Skill 可通过「command, button, API, schedule」触发 |
| **Brand Kit** | 多篇 Lovart 101 wiki 文档 |
| **ChatCanvas / Touch Edit / MCoT reasoning** | 官方 docs/getting-started |
| **多格式导出**（PNG/JPEG/SVG/WebP/TIFF/EPS/PDF，含 CMYK/RGB） | `03-wiki-export-formats-guide` |
| **批量生成**（Batch Generation 引擎） | `02-wiki-batch-generation-best-practices` |
| **图像 + 视频 + 品牌资产** 全品类产出 | 官方首页定位 "AI design agent" |

**关键能力翻译**：Lovart 已经具备 **Agent-friendly 接口**（API + Skill trigger），是设计工具里少数能直接被外部 agent 调用的。

### 1.2 行业标准：Model Context Protocol (MCP)

从 GitHub `modelcontextprotocol/servers` 仓库（88k 星）和官方文档确认：

- **MCP 是 AI agent 调用外部工具的标准协议**
- Claude Desktop、ChatGPT、Cursor、VS Code、Cline、Continue 等都已支持 MCP
- 任何工具只要实现 MCP server，就可以被任何 agent 直接调用
- Anthropic 官方 Skills 库（158k 星）已包含 **canvas-design、brand-guidelines、theme-factory** 等设计相关 skill

**结论**：Lovart 的 OpenClaw API 应该按 MCP 协议封装，作为设计领域的标准 MCP server。

### 1.3 竞品调研

| 竞品 | 集成能力 | 差距 |
|------|---------|------|
| **Runway** | 有 Agent 产品 + Act-Two（角色动作）+ Gen-4.5 + API | 主要面向视频，agent 是 Runway 自家的 |
| **Midjourney** | 仅有 Discord 接口，第三方 API 受限 | 无 MCP 集成 |
| **Adobe Firefly** | Creative Cloud 集成（Photoshop/Illustrator），企业 API | 集成在 Adobe 自家生态，不开放 MCP |
| **Figma** | 已有 MCP 服务（Figma MCP server）+ Dev Mode | 集成在 Figma 自家工作流 |
| **Canva** | Apps SDK + Connect API | 集成在 Canva 自家平台 |
| **Krea** | Realtime canvas + API | 小众，主要面向设计实验者 |
| **Lovart** | OpenClaw API + Custom Skills + Brand Kit + ChatCanvas | ✅ 唯一面向「被外部 agent 调用」的设计工具 |

**Lovart 的差异化定位**：在被 agent 调用的设计工具赛道，Lovart 是少数同时具备「生成能力 + 编辑能力 + 多格式输出」的开放平台。Midjourney/Canva 是孤岛，Figma 偏向 UI 不是视觉生产。

---

## 二、Stack × Stack 重新定义

### 旧定位（不准确）
「两个外部工具协作场景」——找外部标杆文章来证明，但 Lovart 没有相关界面或集成页面。

### 新定位（基于真实能力）

**Stack × Stack =「Lovart 作为被调用方，与 agent / 工具生态协作的实战场景」**

每篇聚焦一个具体场景：
1. **Lovart + Cursor/Claude/ChatGPT**：通过 MCP/API 在编程/对话 agent 里调用 Lovart
2. **Lovart + 自动化工作流（n8n / Zapier / Make）**：在低代码自动化里调用 Lovart 批量产出
3. **Lovart + 业务系统（Shopify / HubSpot / Salesforce）**：在 CRM/电商里按业务规则触发设计生成
4. **Lovart + 数据流（Figma / Notion / Airtable）**：把数据表/数据库变成批量视觉资产

每篇文章的回答：
- **哪个场景**（具体业务/工作流）
- **Lovart 在哪一环**（API 调用 / MCP server / 文件输出）
- **其他工具做什么**（数据源 / 触发器 / 后处理 / 分发）
- **完整代码示例或工作流配置**（让读者可以照搬）
- **对比不用的成本**（手动 vs 自动化的 ROI）

---

## 三、内容框架

### 3.1 单篇 Stack × Stack 文章结构

```markdown
# Lovart + [Tool]: [Specific Workflow Outcome]

## Hook（真实项目失败/翻车）
- 一个具体客户的真实场景
- 手动做的话需要 X 小时 / X 美元
- 用 Lovart + 工具组合之后只需要 Y

## The Workflow Architecture
- 完整架构图（哪个环节做什么）
- 数据流向（输入 → Lovart → 输出）

## Step-by-Step Setup
1. 注册账号 / 获取 API key
2. 配置 MCP server 或 API 调用
3. 编写调用代码（Python/JS 片段，或 no-code 配置）
4. 测试和调试

## Real Project: [Project Name]
- 客户场景 + 产出
- 时间/成本对比
- 学到的教训

## When This Stack Doesn't Work
- 反向推荐
- 边界条件
- 替代方案

## Master Stack: My Recommended Combinations
- 4-6 个核心 stack 推荐
- 每条配价格 + 学习曲线

## FAQ
- 5 个技术问答
```

### 3.2 首批 5 篇样板（基于新定位）

| # | 标题 | 目标读者 |
|---|------|---------|
| 1 | Lovart + Cursor: Generate Brand Assets Without Leaving Your IDE | 开发者 / 设计师开发者 |
| 2 | Lovart + n8n: Automate 100 Social Media Variants Per Day | 营销自动化 / 增长团队 |
| 3 | Lovart + Shopify: Auto-Generate Product Page Visuals from Your Catalog | 电商运营 |
| 4 | Lovart + Notion: Turn Your Brand Database into Visual Assets | 内容团队 / 品牌经理 |
| 5 | Lovart + ElevenLabs + Sora: Build a Full AI Spokesperson Pipeline | 视频营销 / 培训 |

### 3.3 每篇必须包含的元素

- 真实可运行代码（Python/JS）或可复制配置（n8n workflow JSON / Cursor .cursorrules）
- 量化 ROI（具体时间/成本数字）
- Lovart API 调用的具体代码示例（python `requests.post` 或 MCP server 配置）
- 至少 1 个失败模式 + 修复方法
- 与「不用这套 stack」的对比表

---

## 四、内容生产要求

### 4.1 一稿字数标准

**3,500-5,000 词**——比之前的 3,000 提升。每篇包含代码示例和真实配置，密度更高。

### 4.2 内容真实性标准

**所有 Lovart API 描述都要带 Lovart 内部文档知识**（Brand Kit / Custom Skills / ChatCanvas / Touch Edit / Batch Generation / MCoT / 多格式导出）。外部工具部分用常识+通用工作流事实，不编造 API 细节。

### 4.3 与 Lovart 已有文章去重

避免重复 `ai-design-for-social-media-managers-daily-workflow`（已 1,678 词）、`s28---ai-workflow-automation-guide`（已 1,892 词）等内部 wiki。新文章从「API/MCP 集成」切入，不重复讲 ChatCanvas 是什么。

---

## 五、立即行动

- **第 1 篇**（已存在 Lovart + Midjourney）：重新定位为「Midjourney + Lovart API 在批量生产中的应用」，增加 API 调用示例
- **第 2 篇新写**：Lovart + Cursor / Claude — 通过 MCP 在编程 agent 里调 Lovart
- **后续 3 篇**：根据首批反馈调整