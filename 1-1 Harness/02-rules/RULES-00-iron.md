---
type: rule/iron
version: 1.0
updated: 2026-07-05
scope: "profile-iron-global"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-00-iron.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 00 全局铁律（所有会话必载）

> 本文件是唯一跨所有 Profile 加载的规则文件。任何会话、任何工作线，以下规则不可违反。

---

## Sanity 管道铁律

1. **禁止** `sanity deploy`
2. **禁止** `--replace`（必须用 `--missing` + patch 增量导入）
3. **禁止** 修改 `schemaTypes/`
4. **禁止** 删除 production 文档
5. 每次 import 前必须 preflight BLOCK=0
6. **修复优先于删除**：异常页面必须修复 section 结构，不能直接 delete
7. **多语言页面是需求不是垃圾**：de/fr/it/ja/ko/pt/ru/zh/zh-TW 版本是 SEO+UX 必要组成
8. **CLI > MCP**：正文不进 LLM 上下文（NDJSON 磁盘流），仅最小 GROQ 查询可用 MCP
9. **Blog 日期字段双写（2026-07-01 纠正）**：创建/更新 blog 文档时**必须同时设 `releaseDate` + `publishedAt`**（值保持一致）。前端读 `releaseDate`，只设 `publishedAt` → 前端无日期显示。旧数据（2026-06 前）两个字段都 null → 用 `_createdAt` 代替。

## 产出路由铁律（2026-06-29 制定）

1. 写入文件前必须回答四问：谁会读 / 多久后还有用 / 是结论还是中间产物 / 出问题时需要回溯
2. 任一答「人类/长期/结论/需回溯」→ **MindRe 1-2 Insight**（知识资产，永久保存）
3. 全部答「机器/临时/中间/不需」→ **Local Dev Output**（过程缓存）
4. `Output/SEO-Reports/` 目录已废弃，新 SEO 报告一律写入 MindRe
5. 所有产出 skill 必须内置路由判断，禁止第三次路径（规范文档：`1-1 Harness/10-config/产出路由规则.md`）

## 行为铁律（用户纠正 2026-06-22）

1. **不问用户要列表**——先查数据生成清单
2. **不请求审核**——直接按规范执行
3. **修复不删除**——从模板重建 patch
4. **多语言是需求**——翻译 ≠ 直译，品牌术语不翻译
5. **不问就干**："继续"=直接干，不确认 pilot，不先讲用哪些 skill
6. **先结论后数据**：优先给结论/建议/问题，再展示推理
7. **存量改造优先于新建**：GSC 零点击但排名 4-10 的页面，改 Title/Meta ROI 远高于开新页
8. **不禁用表格**：不用表格格式——用纯文字段落表述

## 内容质量铁律 — Anti-Slop

1. 每段内容必须回答：谁会读 / 为什么现在读 / 读完改变什么 / 下一步
2. 禁止编造产品数据、禁止可见占位符、禁止关键词堆砌
3. 多语言是**重写**而非逐句翻译
4. 写作质量是第一优先级，用户对 AI 味零容忍
5. BLOCK 条件出现即不可发布

## SEO 报告通用铁律

1. 所有报告、所有维度**必须有环比**（绝对变化 + 百分比），不允许只出当期快照
2. 天数不等对比时全部用**日均值**，不比较绝对数
3. 竞品词库 265 全量 + 36 核心（真实词库，不可编造）
4. 品牌词用 `lovart_brand_match.is_brand()` 精确分类
5. 地区分组：南亚(IN+PK+ID)、拉美(BR+MX)、中东非(IR+EG+DZ) 是主要区域
6. GSC 拉取需全维度（query/country/page/country×query/device）
7. 每节必须有 💡 洞察（问题/根源/缓解），三部分缺一不可

## 项目路径 SSOT

| 变量 | 值 |
|------|-----|
| `$LOVART_RESOURCE_ROOT` | vault 根（Obsidian MindRe） |
| `$LOVART_LOCAL_DEV_ROOT` | `~/Documents/Lovart Local Dev/` |
| Sanity project | `o11tm2qe` / `production` |
| Sanity token | `~/.config/sanity/config.json` → `/tmp/sanitytoken.txt` |
| Vault 脚本路径 | `1-4 Dev/`（非 `1-4 Dev/`，历史别名） |

## Memory 速查

- 文章写作禁止 delegate_task。子 agent 无法保持 voice 深度。
- 所有 API 已验证：Sanity/GSC/GA4/Bing/WP/Notion ✓
- Profiles: lovart-seo(deepseek-chat) lovart-content(deepseek-v4-pro)
- Gateway launchd 已装，12 cron deliver→origin
- Kanban lovart 板 6 任务 workspace 已配
