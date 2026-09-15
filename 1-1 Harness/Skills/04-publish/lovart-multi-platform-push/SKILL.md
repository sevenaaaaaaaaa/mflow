# lovart-multi-platform-push

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-multi-platform-push/SKILL.md` |

Step 5+6 of Lovart Content Pipeline — 将审计通过的内容写入飞书 Bitable（content-distributor 命令中心），由 Node.js 分发引擎自动处理所有平台的分发。返回推送结果汇总。

## Triggers

- "推送内容" / "push content"
- "推送到所有平台" / "push to all platforms"
- Pipeline Orchestrator 调用 Step 5

## Prerequisites

- Step 4 审计 PASS 或 CONDITIONAL PASS
- Sanity 已发布（博客 URL 已知：`https://www.lovart.ai/blog/{slug}`）
- content-distributor 引擎已部署：`~/content-distributor/`（独立于 vault）
- 飞书 CLI 已登录：`lark-cli auth login --domain base`

---

## 架构

```
              Step 4 审计通过
                    │
                    ▼
         ┌─────────────────────┐
         │  Step 5: 写入飞书     │
         │  Lovart-Home 表格    │
         │                     │
         │  标题 / 博客链接      │
         │  封面图 / 标签 / 分类 │
         │  状态 = 待分发       │
         └─────────┬───────────┘
                   │
                   ▼ (content-distributor 每日 09:00 cron)
         ┌─────────────────────┐
         │  Node.js 分发引擎    │
         │                     │
         │  ① GA4 拉取着陆页    │
         │  ② LLM 分析+计划     │
         │  ③ 差异化改写        │
         │  ④ API 分发 22 平台  │
         │  ⑤ 回写飞书状态      │
         └─────────┬───────────┘
                   │
         ┌─────────┴───────────┐
         ▼                     ▼
  22 API 平台            16 手动平台
  (Medium/Reddit/        (Quora/G2/
   DEV.to/Pinterest/     小红书/CSDN/
   Hashnode/LinkedIn/    掘金/百度百科
   GitHub/X/YouTube/     ...)
   Product Hunt/...)     → 清单指引
```

## 飞书表格信息

| 属性 | 值 |
|------|-----|
| Base | Lovart-Home |
| Base Token | `ZLWgbi6VIaCRiNsb22jcNpPRnfh` |
| 主表 | 内容分发表 |
| Table ID | `tblfYkNiq83rotAh` |
| 链接 | https://resonate.feishu.cn/base/ZLWgbi6VIaCRiNsb22jcNpPRnfh |

## Workflow

### Phase 1: 收集已发布内容

从 Step 4 审计结果中提取本轮通过的内容清单，构建飞书记录：

```bash
# 确认 Sanity 博客 URL 可访问
curl -sI "https://www.lovart.ai/blog/{slug}" | head -1
# → HTTP/2 200
```

### Phase 2: 写入飞书 Bitable

对每条 PASS 的内容，映射字段后写入：

```
Pipeline 来源          →  飞书字段
─────────────────────────────────────
Blog frontmatter title →  标题
lovart.ai/blog/{slug}  →  博客链接
frontmatter cover_url  →  封面图链接
frontmatter author     →  作者
frontmatter tags       →  标签（映射到飞书多选）
frontmatter category   →  分类（映射到飞书单选）
固定 "改写转载"        →  分发策略
{today + 3 days}      →  计划分发日期
固定 "待分发"          →  状态
```

**字段映射规则**：

| Pipeline Tag | 飞书标签选项 |
|-------------|------------|
| AI video / video generation | AI视频 |
| prompt / tutorial / how-to | Prompt教程 |
| image generation / design | 图像生成 |
| product update / release | 产品更新 |
| insight / trend / industry | 行业洞察 |
| case study / showcase | 案例展示 |

| Pipeline Category | 飞书分类选项 |
|------------------|------------|
| Lovart 101 / How-To / Best Practice / Design / Branding / canvas | Lovart通用 |
| Video / AI Video Tools | Seedance |
| AI Image Tools / AI Image | GPT Image / Nano Banana |
| Insight & Trend / Better Design / Topics | 行业趋势 |

```bash
lark-cli base +record-create \
  --base-token ZLWgbi6VIaCRiNsb22jcNpPRnfh \
  --table-id tblfYkNiq83rotAh \
  --fields '{
    "标题": "{title}",
    "博客链接": "https://www.lovart.ai/blog/{slug}",
    "封面图链接": "{cover_url}",
    "作者": "{author}",
    "标签": ["{tag_1}", "{tag_2}"],
    "分类": "{feishu_category}",
    "状态": "待分发",
    "分发策略": "改写转载",
    "计划分发日期": "{yyyy-mm-dd}"
  }'
```

### Phase 3: 生成手动平台清单

16 个无 API 平台（Quora/G2/Capterra/Stack Overflow/Dribbble/Behance/CSDN/掘金/简书/百度百科/百度知道/豆瓣 等）无法自动化，生成操作指引：

```
Output/Push Reports/
└── manual-platforms-YYYY-MM-DD.md
```

```markdown
# 手动分发清单 — YYYY-MM-DD

| 平台 | 文章 | 操作说明 |
|------|------|---------|
| Quora | {title} | 搜索 "AI design tool" → 回答相关问题时引用链接 |
| G2 / Capterra | Lovart 产品页 | 检查评价数，引导用户评价 |
| 小红书 | {title} | 用 xiaohongshu-mcp 或手动发布图文笔记 |
| CSDN / 掘金 / 简书 | {title} | 复制中文版本 → 登录后粘贴发布 |
| 百度百科 | Lovart 词条 | 创建/更新产品词条 |
```

## Push Result Report (Step 6)

```
Output/Push Reports/
└── push-report-YYYY-MM-DD.md
```

```markdown
# Push Report — YYYY-MM-DD

## 📊 飞书写入

| Slug | 标题 | 飞书记录 | 计划分发 |
|------|------|---------|---------|
| {slug-1} | {title} | ✅ 已创建 | {date} |
| {slug-2} | {title} | ✅ 已创建 | {date} |

## 📋 手动平台 (16)

（见 manual-platforms-YYYY-MM-DD.md）

## 🔄 content-distributor 状态

| 引擎 | 状态 | 下次执行 |
|------|------|---------|
| content-distributor | cron 09:00 daily | 明天 09:00 |
| 飞书表格待分发记录 | {count} 条 | 引擎自动处理 |

📌 分发引擎每天 09:00 自动从飞书表格读取"待分发"内容并分发到各平台。
📌 无需手动干预——引擎回写飞书状态后可查看分发结果。
```

## 推送策略

```
P0 (自动): 写入飞书表格 → content-distributor 每日 cron 自动处理
P1 (清单): 手动平台操作指引 → Output/Push Reports/manual-platforms-{date}.md
```

## Downstream

完成后自动触发 → `lovart-sitemap-update` (Step 7)

## Related

- content-distributor 引擎: `~/content-distributor/`
- 全渠道分发 SOP: `Product Project Management/全渠道内容分发自动化SOP.md`
- 飞书表格: https://resonate.feishu.cn/base/ZLWgbi6VIaCRiNsb22jcNpPRnfh
- Notion Lovart-Home: `lovart-notion-config.md`
