---
type: session-log
session_date: 2026-09-17
session_slug: multi-site-library
status: ready
---

# Session Log — 多站点内容库 + 默认项目更名 + 内容日历清空

## 需求（用户四点）
1. 清空服务器内容日历
2. 默认项目改为 Lovart Global
3. 同步 Sanity 各类落地页/Blog 到服务器库
4. MFlow 需兼容不同网站的目录结构（此前未考虑页面分类）
后续用户将**从 MFlow 跑任务**，不再用本地 Agent。

## 关键发现
- 内容日历 3,280 篇 = **历史生产稿多语言快照 + 排期表**（抽查 40 slug 100% 命中 Sanity；线上存活性混杂；含未来日期 358、占位符 1,009）→ 非新内容、非待发队列
- Sanity 类型：`blog` 8,884 + `compositePage` 8,864（按 pageType：feature 6,438 / tool 1,682 / topic 410 / scenario 397 / solution 120 / product 45 / landing 1）
- 落地页路由规律：/{lang}/{features|tools|topics|scenarios|solutions|product}/{slug}；en 不带前缀 → 这就是"网站目录结构"

## 交付
1. **内容日历清空**：归档 `run/_archive/content-calendar-20260917.tar.gz`（17MB）后清空（Sanity 为 SSOT，可回取）
2. **默认项目更名**：创建 `lovart-global`（旧 `main` 全部数据迁移：管线/事件/任务/Loop/内容/GEO/引用），`DEFAULT_PROJECT="lovart-global"`，UI 显示 **Lovart Global**；顺带补回 geo 配置（brand/竞品/4 查询/probe_daily）
3. **站点档案机制（核心）**：`run/sites/{site}.json` 描述 domain/默认语言/数据源/sections（docType·pageType·dir·route/engine）→ 换站点只换档案
4. **Sanity → 库同步器**：`1-4 Dev/scripts/library/sanity_pull.py`（分页 100、剔 drafts、两引擎）+ `pt_to_md.py`（Portable Text→MD）+ `bodyjson_to_md`（版块 JSON→可读文本）；URL 按档案规则本地化生成
5. **首次全量镜像 17,535 篇 / 215MB / 3 分钟**：blog 8,864 · features 6,400 · tools 1,661 · topics 409 · solutions 120 · products 41 · scenarios 23 · news 17
6. **工作台「内容库」页**：站点选择 / 段落计数 chips / 语言过滤 / 全文搜索 / 阅读 / 后台同步 + 进度轮询（admin，审计 approvals.log）
7. `.gitignore` 收口：run/ 下的数据（library/secrets/pay/projects/…）全部不入库；`run/sites/*.json` 档案入库

## 验证（线上）
- 同步器试跑（blog max20）→ 修正批次超发 bug → 全量 17,535 篇无错误
- API：sites / tree（段落计数）/ list（tools/en 200 条）/ status 全通
- 镜像质量抽样：frontmatter 完整、URL 本地化正确（`/zh/blog/{slug}`）、正文可读
- 当前项目 = lovart-global（Lovart Global）

## 待办（下一步）
- 库 × GEO 联动：引用缺口 × 库内已有 → 自动判定「改稿 / 新写」（用户接下来跑任务的入口）
- 第二站点档案（验证泛化）
- 内容日历页在清空后应显示"空"（或改造为直接指向内容库）
