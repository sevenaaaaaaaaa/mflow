# Session Log · 2026-09-28 · MFlow × Composite Page 手册 / Blog PRD 差距分析

- **status**: draft
- **类型**: 只读差距分析（零代码改动）
- **标准输入**:
  - `Lovart MFlow/dev/Composite Page 组件开发手册.md`（v2.0，21 族 33 型 + Sanity 适配 + 故事线菜谱）
  - `Lovart MFlow/harness/01-project/PRD-Blog文章页面开发.md`（v1.2 draft，C1–C8 / F1–F8 / I1 / P0–P6）
- **方法**: 双 Explore 代理全仓扫描（53+51 次工具调用）+ 关键结论人工抽查复核（4/4 属实）

## 做了什么

对照两份标准审查 `~/MFlow Dev`（mflow 仓库 v1.2.0）的模块化能力与 blog 适配能力，产出差距清单。

## 关键发现（抽查复核过）

### 模块化（vs Composite Page 手册）
- **P0 × 3**：
  1. 无 33 型 type 注册表/逐型字段 schema 校验——语料实测 59 种 type 共存，preflight 只查骨架不查字段；MFlow 自己的 `md_to_sections()` 就在产出错配（faq 用 `[q,a]` 数对、proof-block 误用 `stats` 字段）——`sanity_publisher.py:298-308`
  2. 故事线顺序约束不在产品代码执行——console 不读 landing-storylines.json，且「故事线 SSOT」知识源指向不存在的 `harness/08-storyline`——`console.py:211-212`
  3. console 工作台唯一页面产物 = 固定五段骨架（hero-split→feature-detail→proof-block→faq→cta-default），33 型与变体选型在产线上不存在
- 已对齐最好的：Sanity 写入安全（dry-run / patch + ifRevisionID / createIfNotExists / 无草稿防呆 confirm_public）
- P1：verify L2 无脚本实现；图片 URL 校验缺口（品牌域跳过）；multilang 产线只覆盖 blog；预览只有 MD 渲染无 section 级

### Blog（vs PRD）
- **P0 × 6**：
  1. 三时间字段缺失（`displayedAt` 全仓 0 命中；releaseDate=publishedAt 双写合一）
  2. status 生命周期缺失（blog 硬编码 draft、compositePage 写入即上线，无 scheduled cron 翻转）
  3. `_id=slug` 无语言命名空间——（type, slug, language）唯一键在写入路径不成立，同 slug 多语言互撞——`sanity_publisher.py:156,409`
  4. 正文 image block 不存在（MD→PT 把图片降级为 `[Image: alt]` 文本）——`md_to_portable_text.py:548`
  5. aggregate/related 查询契约 0 命中
  6. og 三字段缺失 + JSON-LD 由管道整段生成（与 PRD「前端模板生成、禁止手写」反向）
- P1：图片本地化管道全缺（占位图被用 7,204 次即症状）；module-*/card-* 运营模块全缺；canonical/noindex/translations 缺失；P6 质检多项缺（引用完整性/大纲跳级/hreflang/死链扫描）
- 结构性认知：PRD 前端条款（F1–F8）大多属前端 repo 职责，MFlow 侧缺的是**数据契约与校验载体**（§6 对齐底线「内容模型 1:1、查询契约 1:1、渲染 token 1:1」中前两条在 MFlow 通道上不成立）

## Lessons
- 生成端（批量脚本/转换器）本身是字段错配的制造者——preflight 校验器必须先于生成器对齐手册字段表，否则「校验放行」等于「错配合法化」
- 内容库镜像（pt_to_md 压平）适合检索不适合作为编辑/预览载体，bodyJson 的有损压平让 section 级问题在 MFlow 侧不可见

## 待办（来自本次分析，未开工）
- [x] section type 注册表 + 逐型字段 schema 校验（preflight L1 升级）→ 2026-09-30 已交付 `publish_adapters/section_registry.py`
- [x] md_to_sections/md_to_portable_text 字段错配修复（faq/proof-block/image block）→ 2026-09-30 已交付
- [x] _id 加语言命名空间（type-slug-language）→ 2026-09-30 已交付（含三时间 + status 五态 + scheduled_flip.py）
- [ ] aggregate/related 查询 API、og 三字段、图片本地化管道（C6）→ 未开工，见 2026-09-30 开发 log 待办

> 开发轮详见同目录 `2026-09-30-content-contract-layer.md`（87 测试全绿）。
