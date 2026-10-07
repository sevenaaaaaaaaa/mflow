# infra/knowledge · 知识库基建（v1.0）

> **成熟度**：基建抽取第二批（与门禁并列最成熟）——目录规范/检索打分/kb_intent 防污染/RAG 由 Moodio 接入全流程验证（KB 0→9 份文档、检索 top-1 命中、RAG 1606 chunks）。
> **定位**：知识库是品牌无关机制，品牌差异 = **数据目录（`Knowledge Base/{Brand}/`）+ 一行 kb_intent 声明**。机制代码在 console.py（_kb_index / kb_search_for_ai / rag_build）；本目录是契约与接入规程。

## 契约：四层机制（继承 KB-SCHEMA.md 数据模型）

1. **数据层**：`insight-data/Knowledge Base/{Brand}/*.md`（frontmatter: type/topic/version/status/source_url/audience）——生成上下文与 RAG 的唯一事实源
2. **索引层**：`_kb_index` 按目录 mtime 缓存（推文件即生效，无需重启），打分 = 标题×3.0 + 路径×1.6 + 小标题×1.2 + 正文×0.7 + 短语精确匹配
3. **防污染层**：meta.json `kb_intent: ["BrandDir"]` → boost_dirs **+6 强加权**（多品牌共享 KB 时防跨品牌淹没；Moodio 实测 5 类查询 4 个 top-1 命中）
4. **融合层**：`rag_build` 向量索引（local backend, 512 维），检索 RRF 融合——KB 检索是主通道，RAG 缺失时纯关键词行为不变

## 检索消费方

- `ai_context`（生成上下文构建）——所有生成路径自动调用
- `kb_search_for_ai(query, k, intent_dirs, boost_dirs)`——可直调验证
- 全局十大 KNOWLEDGE_SOURCES（铁律/故事线/阶段手册/写作方法论/内容策略/关键词研究/UTM/质量案例/项目记忆）与品牌 KB 目录**并存**，品牌 kb_intent 保证本品牌文档优先

## 新品牌知识库接入 checklist（Moodio 验证过的五步）

1. 建 `insight-data/Knowledge Base/{Brand}/` 目录，写 KB units（官方文档 → 消化成 confirmed 知识文件；官方没说的标 draft 并列"待确认清单"）
2. 首批最少集：**品牌核心（00）/能力词表（01）/表达红线（03）/事实白名单（04）**——写作红线与数字白名单是质检依据，缺了生成会幻觉
3. 项目 meta.json 加 `"kb_intent": ["{BrandDir}"]`
4. `rag_build()` 重建索引（server: `.venv/bin/python -c "import console; console.rag_build()"`）
5. 验证：`kb_search_for_ai("品牌关键词", boost_dirs=["{BrandDir}"])` top-1 应命中品牌目录

## 写作约束（生成层联动）

- 品牌能力词只允许出自能力词表；数字只允许出自事实白名单；表达红线违反即 BLOCK（红线同时写进行业模板 anti_slop_extra，双保险）
- 品牌间术语隔离：写 A 品牌不得借用 B 品牌能力词（blog-writer/landing-writer SKILL 的按项目路由节）

## 演进记录

- 2026-10-03 kb_intent/boost_dirs 上线（console.py）——多品牌共享 KB 防污染，+6 强加权
- 2026-10-03 Moodio KB 0→9 份接入验证（检索/RAG/生成链路）
- 2026-10-04 晋升 infra 资产；品牌差异收敛为「数据目录 + kb_intent + 白名单文件路径」
