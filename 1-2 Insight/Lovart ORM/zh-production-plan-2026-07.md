---
type: strategy/production-plan
language: zh
version: 1.0
updated: 2026-07-15
status: draft
---

# 中文内容生产计划 — 2026年7-9月

> 本文件定义 344 个中文内容节点的生产排期、管线依赖、批量化方案。

---

## 一、架构总览：双管线并行

```
管线A（Landing Page → Sanity lovart.ai/zh/）
  批量生成 JSON → QA预检 → sanity import --missing → IndexNow
    
管线B（Blog → WordPress blogs.lovart.ai/zh/blog/）
  批量生成 Markdown → pick cover → QA预检 → WordPress publish

依赖：Blog 所引用的 LP 必须已发布
```

### 每周产能目标

| 资源 | LP/周 | Blog/周 | 总计 |
|------|:-----:|:-------:|:----:|
| 批量生成（脚本） | 30-40 | 15-20 | 45-60 |
| 人工精修（关键页） | 3-5 | 2-3 | 5-8 |
| **合计** | **35-45** | **17-23** | **50-68** |

---

## 二、批量化策略

### 2.1 Landing Page 批量生成管线

**核心思路**：已有 19 条故事线 + 33 模块 JSON 模板 + `image_pool.py`（支持 CJK），包装成一个批量脚本：

```
scripts/batch_gen_zh_lp.py
  --input zh-content-matrix.csv    ← 六维矩阵 CSV
  --storyline-dir .../Refresh-Page/ ← 故事线 SSOT
  --output-dir .../Pages/zh/       ← 输出目录
  --image-pool .../image_pool.py   ← 图片分配
  --dry-run                        ← 预览模式
```

每行的 CSV 字段：
```
page_type,slug,direction,storyline_id,h1,seo_title,seo_description,intents
topic,ai-image-generator,landing,landing-gallery-detail,AI图片生成器,...
tool,background-remover,tools,tools-A,在线去背景工具,...
```

**脚本逻辑**：
1. 读 `zh-content-matrix.csv`
2. 按 `page_type` 选模板（topic/tool/feature/solution/scenario）
3. 按 `storyline_id` 读对应的 `sections` 数组
4. 用中文内容填充每个 section 的 `copy` 字段
5. `image_pool.py` 按 section title 匹配分配图片
6. 组装完整 composite-v2 JSON → 写文件
7. `preflight-content.js` 验证

**预计**：写脚本 1 天，跑全量 344 个 LP < 10 分钟。

### 2.2 Blog 批量生成管线

**思路**：每篇 Blog 有固定结构，用模板 + 变量填充：

```
scripts/batch_gen_zh_blog.py
  --input zh-blog-matrix.csv
  --output-dir .../Blogs/zh/
```

Blog CSV 字段：
```
slug,blog_type,category,seo_title,seo_description,h1,keywords,target_lp_slug
ai-design-agent-guide,How-To,Branding,...,,,,/zh/ai-design-agent
```

**脚本逻辑**：
1. 按 `blog_type` 选结构模板（How-To / Comparison / 101 / Guide）
2. 填充标题/描述/关键词
3. 内链自动插入目标 LP 的链接（`target_lp_slug`）
4. 生成完整 Markdown + frontmatter
5. QA 预检

---

## 三、生产排期（9 周，分 5 批）

### Batch 0 — 基础设施（2026-07-16 ~ 07-18, 3 天）

| 任务 | 产出 | 关键路径 |
|------|------|---------|
| 写 `batch_gen_zh_lp.py` | 批量生成脚本 | 独立 |
| 写 `batch_gen_zh_blog.py` | 批量生成脚本 | 独立 |
| 编译 `zh-content-matrix.csv`（六维→CSV） | 全量输入数据 | 独立 |
| 编译 `zh-blog-matrix.csv` | 全量输入数据 | 依赖 LP CSV |
| 测试脚本：生成 3 个测试 LP + 2 篇 Blog | 验证管线 | 依赖以上 |
| QA 预检配置 | preflight 中文规则 | 独立 |

---

### Batch 1 — 品牌 + 痛点 + 竞品（第 1-2 周）

**目标**：先打信任入口 + 流量入口。

| 类型 | 批量 | 人工精修 | 周 |
|------|:---:|:--------:|:-:|
| 品牌 LP（8 页） | 脚本生成 | H1/SEO title 润色 | W1 |
| 品牌 Blog（12 篇） | 脚本生成 | 品牌语调把控 | W1 |
| 痛点 LP top10（10 页） | 脚本生成 | 痛点命中率检查 | W1 |
| 痛点 Blog（15 篇） | 脚本生成 | 关键词嵌入检查 | W2 |
| 竞品对比 LP（12 页） | 脚本生成 | 竞品数据核实 | W2 |
| 竞品 Blog top8（8 篇） | 脚本生成 | 公正性检查 | W2 |
| **本批小计** | **65 节点** | | **W1-2** |

**发布后检查**：
- [ ] sanity import --missing → preflight BLOCK=0
- [ ] IndexNow 提交验证
- [ ] 48h 后 GSC 确认收录

---

### Batch 2 — 产品核心（第 3-4 周）

**目标**：让中国用户看到 Lovart 能做什么。

| 类型 | 批量 | 人工精修 | 周 |
|------|:---:|:--------:|:-:|
| 产品 LP core（20 页） | 脚本生成 | 产品术语翻译审核 | W3 |
| 产品 LP variants（16 页） | 脚本生成 | 差异化检查 | W3 |
| 产品 Blog（24 篇） | 脚本生成 | 产品描述准确性 | W4 |
| 痛点 LP remaining（8 页） | 脚本生成 | | W4 |
| 痛点 Blog remaining（15 篇） | 脚本生成 | | W4 |
| **本批小计** | **83 节点** | | **W3-4** |

---

### Batch 3 — 设计品类（第 5-7 周）

**目标**：覆盖所有设计品类搜索入口。

| 类型 | 批量 | 人工精修 | 周 |
|------|:---:|:--------:|:-:|
| 品类 LP 首批（20 页） | 脚本生成 | 品类术语审核 | W5 |
| 品类 LP 第二批（20 页） | 脚本生成 | 品类覆盖检查 | W6 |
| 品类 LP 第三批（20 页） | 脚本生成 | | W7 |
| 品类 Blog（30 篇） | 脚本生成 | 关键词密度检查 | W6-7 |
| **本批小计** | **90 节点** | | **W5-7** |

---

### Batch 4 — 行业 + 场景（第 8-9 周）

**目标**：行业纵深 + 季节性覆盖。

| 类型 | 批量 | 人工精修 | 周 |
|------|:---:|:--------:|:-:|
| 行业 LP（30 页） | 脚本生成 | 行业调研验证 | W8 |
| 场景 LP top10（10 页） | 脚本生成 | 场景真实性 | W8 |
| 行业 Blog（24 篇） | 脚本生成 | 行业术语 | W9 |
| 场景 Blog（20 篇） | 脚本生成 | 季节性时效性 | W9 |
| 场景 LP remaining（5 页） | 脚本生成 | | W9 |
| **本批小计** | **89 节点** | | **W8-9** |

---

### 总排期 Gantt

```
                    W1  W2  W3  W4  W5  W6  W7  W8  W9
Batch 0 (管线)      ██
Batch 1 (品牌+痛点)   ██  ██
Batch 2 (产品)           ██  ██
Batch 3 (品类)                 ██  ██  ██
Batch 4 (行业+场景)                    ██  ██
IndexNow 提交通道     ██  ██  ██  ██  ██  ██  ██  ██  ██
DataWorks 回流监控                             ██  ██  ██
```

---

## 四、质量控制

### 每批发布前检查清单

| 检查项 | 工具 | 通过条件 |
|--------|------|---------|
| LP JSON 结构完整 | `preflight-content.js` | BLOCK=0 |
| Blog Frontmatter 完整 | 手动检查 | 必填字段非空 |
| LP 故事线对齐 | 检查 storyline_id | 匹配 SSOT |
| Blog 内链存活 | 检查 target_lp_slug | LP 已发布 |
| 图片 URL 200 | HEAD 请求 | 0 404 |
| SEO title 截断 | 长度检查 | ≤75 chars |
| SEO description 截断 | 长度检查 | ≤160 chars |
| zh 字数 ≥ EN 单词×1.6 | 字数比例 | ≥1.6x |
| 禁用词检测 | Anti-Slop 规则 | 0 命中 |

---

## 五、批量化脚本技术方案速查

### batch_gen_zh_lp.py

```
依赖: json, csv, os, requests (HEAD check), sys
输入: zh-content-matrix.csv + Refresh-Page/ 下的 SSOT JSON 文件
输出: 每个 LP 一个 JSON 文件到 output/Pages/zh/{type}/{slug}.json
核心步骤:
  1. parse CSV row
  2. 根据 page_type 定位故事线文件 (landing-storylines.json / solution-storylines.json 等)
  3. 读 storyline_id 获取 sections 数组
  4. 从 CSV 的 copy 字段填充到 sections[i].copy.zh
  5. image_pool.match_title(title_zh) → 分配图片 URL
  6. 组装完整 composite-v2 结构（含 _id, slug, seo, language, category）
  7. 输出 JSON 文件
  8. preflight 调用
```

### batch_gen_zh_blog.py

```
依赖: yaml/frontmatter, csv, os, re
输入: zh-blog-matrix.csv + 可选的 writing-spec.md 模板
输出: 每个 Blog 一个 .md 文件到 output/Blogs/zh/{slug}.md
核心步骤:
  1. parse CSV row
  2. 按 blog_type 选模板结构（H2 序列、FAQ 数量）
  3. 填充标题/描述/正文大纲 + 内链
  4. 生成 frontmatter (slug, category, cover_url, image_briefs)
  5. cover：从 blogcover-011~065 池 stable hash 分配
  6. 输出 .md 文件
  7. 字数统计 + 质量门禁
```

---

## 六、关键数量汇总

| 批次 | 内容 | LP | Blog | 人天（人工精修） | 预计完成 |
|:----:|------|:--:|:----:|:--------------:|:--------:|
| 0 | 管线搭建 | - | - | 3 | 07-18 |
| 1 | 品牌+痛点+竞品 | 30 | 35 | 5 | 07-25 |
| 2 | 产品核心 | 44 | 39 | 4 | 08-01 |
| 3 | 设计品类 | 60 | 30 | 4 | 08-15 |
| 4 | 行业+场景 | 45 | 44 | 3 | 08-29 |
| **总计** | | **179** | **165** | **19** | **~6.5 周** |

按批量脚本产能 40 LP + 15 Blog/周，实际执行约 6.5 周（而非手动模式下的 20+ 周）。

---

## 七、风险与缓解

| 风险 | 概率 | 缓解 |
|------|:---:|------|
| 批量生成脚本开发延迟 | 中 | 先用手动模式生产 Batch 1（品牌页量小），脚本完成后切批量 |
| Sanity import 中文内容出 block | 低 | preflight 先跑，优先修复已知 block（AB-LP22/AB-LP23） |
| 中文内容质量不够（AI味/机翻感） | 中 | 每个 batch 抽 20% 人工精修；关键品牌页 100% 精修 |
| Google 中文收录慢 | 低 | IndexNow 即时提交；之前历史验证 24h 收录率 >80% |
| 中文 Blog 需要独立封面图 | 低 | blogcover 池 55 张图已够用，stable hash 分配不重复 |
