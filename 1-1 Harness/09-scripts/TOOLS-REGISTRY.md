# TOOLS-REGISTRY.md — 项目内所有合规脚本/工具的清单 (SSOT)

> **用途**：任何会话创建新脚本前，必须先搜本文件确认是否有已有实现。
> **维护**：新增脚本走 `lovart-new-tool-governance` skill → governance_check.py PASS → 本文件追加一行。
> **最后更新**：2026-09-14

---

## Blog Portable Text 铁律（2026-08-03）

1. **唯一转换入口**：`~/Documents/Lovart Local Dev/scripts/md_to_portable_text.py`
2. **表格 schema**：`table → tableRow → cells:string[]`；禁止 `tableCell` / block-cell
3. **任何生成 blog body 的新脚本必须**：
   ```python
   sys.path.insert(0, str(Path.home() / "Documents/Lovart Local Dev/scripts"))
   from md_to_portable_text import md_to_portable_text
   ```
4. **禁止**内联 `def md_to_pt` / `def markdown_to_portable_text`
5. **import 前**：`python3 validate_pt_body.py --ndjson <file>` 必须 `BLOCK=0`
6. 规范详情：`1-1 Harness/Skills/02-creation/lovart-blog-signal-writer/references/portable-text-table-syntax.md`

| path | purpose | created | owner | status | smoke |
|------|---------|---------|-------|--------|-------|
| `~/Documents/Lovart Local Dev/scripts/md_to_portable_text.py` | MD→PT SSOT（含 string-cell 表格） | 2026-07 / 2026-08-03 纠正 | lovart-ops | active | validate PASS |
| `~/Documents/Lovart Local Dev/scripts/validate_pt_body.py` | body `_key` + table shape 门禁 | 2026-08-03 | lovart-quality | active | BLOCK=0 |
| `~/Documents/Lovart Local Dev/scripts/normalize_table_cells.py` | 生产 object-cell → string[] 归一化 | 2026-08-03 | lovart-ops | active | 16/16 patched |
| `~/Documents/Lovart Local Dev/scripts/repair_table_keys.py` | 补齐 table/tableRow 缺失 `_key`（ifRevisionID） | 2026-08-04 | lovart-ops | active | 22/22 patched |

---

## 核心工具 (1-4 Dev/scripts/)

| path | purpose | created | owner | status | smoke |
|------|---------|---------|-------|--------|-------|
| `lovart_brand_match.py` | 品牌词分类器 (is_brand()) | 2026-06-04 | lovart-reports | active | G1-G5 |
| `brand_keyword_inventory.py` | 品牌词布局清单生成（还原全部品牌词变体） | 2026-08-17 | lovart-reports | active | G1-G6 |
| `lovart_indexing_metrics.py` | 索引率指标计算 | 2026-06-04 | lovart-reports | active | G1-G5 |
| `lovart_seo_geo_metrics.py` | SEO+GEO 综合指标 | 2026-07-17 | lovart-reports | active | G1-G5 |
| `seo_monthly_v2.py` | 月度 SEO 报告生成 | 2026-07-17 | lovart-reports | active | G1-G5 |
| `seo_monthly_extras.py` | 月度报告补充数据 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `seo_report_standards.py` | SEO 报告格式标准 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `competitor_deep_match.py` | 竞品关键词深度匹配 | 2026-06-07 | lovart-reports | active | G1-G5 |
| `report_inventory.py` | 报告清单生成 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `report_week_dates.py` | 周报日期计算 | 2026-06-12 | lovart-reports | active | G1-G5 |
| `comprehensive_may_report.py` | 5月综合报告 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `report_batch_runner.py` | 批量报告运行器 | 2026-06-12 | lovart-reports | active | G1-G5 |
| `audit_p3_quality.py` | P3 质量审计 | 2026-07-06 | lovart-quality | active | G1-G5 |
| `audit_pillar_fleet.py` | Pillar 内容审计 | 2026-07-17 | lovart-quality | active | G1-G5 |
| `generate_pillar_battle_cards.py` | Pillar 竞品卡片生成 | 2026-07-17 | lovart-creation | active | G1-G5 |
| `backdate_landing_categories.py` | 落地页分类回填 | 2026-07-17 | lovart-ops | active | G1-G5 |
| `harness_auto_optimize.py` | Harness 自动优化 | 2026-07-17 | lovart-management | active | G1-G5 |
| `harness_patch_paths.py` | 路径修补 | 2026-07-17 | lovart-management | active | G1-G5 |
| `harness_sync.py` | 跨 profile 同步 | 2026-07-17 | lovart-management | active | G1-G5 |

## Hooks (1-4 Dev/scripts/hooks/)

> 2026-09-14：完整 4-hook 清单见文末「Hooks — 4 个」段（此处旧 3-hook 表已并入）。

## Sentinel (1-4 Dev/scripts/sentinel/)

| path | purpose | created | owner | status | smoke |
|------|---------|---------|-------|--------|-------|
| `sentinel/collect.py` | 舆情数据采集 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `sentinel/daily.py` | 每日舆情运行 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `sentinel/report.py` | 舆情报告生成 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `sentinel/generate_historical.py` | 历史数据生成 | 2026-07-05 | lovart-reports | active | G1-G5 |

## Trident (1-4 Dev/scripts/trident/)

| path | purpose | created | owner | status | smoke |
|------|---------|---------|-------|--------|-------|
| `trident/gsc_fetch.py` | GSC 数据拉取 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/ga4_fetch.py` | GA4 数据拉取 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/bing_fetch.py` | Bing 数据拉取 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/gsc_auth.py` | GSC 认证 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/ga4_auth.py` | GA4 认证 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/credential_paths.py` | 凭证路径管理 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/trident_paths.py` | Trident 路径管理 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/push_to_feishu.py` | 推送到飞书 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/push_to_warehouse.py` | 推送到数据仓库 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/unified_brief.py` | 统一简报生成 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/run-all.sh` | 全量运行入口 | 2026-07-05 | lovart-reports | active | G1-G5 |
| `trident/benchmark_fetch_0508.py` | 固定区间曝光侧补数（GSC/GA4/Bing 日粒度 + 口径审计 + _RUN-NOTES） | 2026-09-13 | lovart-reports | active | G1-G6 |

## Pipeline Skills (1-1 Harness/Skills/06-orchestrate/)

| path | purpose | created | owner | status | smoke |
|------|---------|---------|-------|--------|-------|
| `lovart-pipeline-state/pipeline_state.py` | 流水线状态机 | 2026-07-20 | lovart-management | active | 39/39 |
| `lovart-router/router.py` | 跨档案路由决策 | 2026-07-20 | lovart-management | active | 15/15 |
| `lovart-new-tool-governance/governance_check.py` | 新工具合规校验 | 2026-07-20 | lovart-management | active | TBD |

## 统计

- 核心工具: 19 个
- Hooks: 4 个
- Sentinel: 4 个
- Trident: 12 个
- Pipeline Skills: 3 个
- **总计: 42 个合规脚本**

> **运行环境契约（2026-09-14）**：GSC/GA4 API 脚本用 `~/Documents/Lovart Local Dev/trident-venv/bin/python`（google-auth + googleapiclient + pyyaml + requests）。管线统一经 `LOVART_PYTHON`（定义在 `1-4 Dev/automation/local-dev-env.sh`）取解释器，新数据脚本不要 import stdlib 之外的库除非先装入该 venv 并在本文件注记。

## 归档记录

2026-07-20 归档 51 个一次性脚本（原计划路径 `1-4 Dev/scripts/.archive/2026-07-20/`；实测该目录已不在 vault，推测随 2026-08-01 大归档移至 Local Dev Backup——查重时以本文件为准，不必再找归档实体）
- wave/patch/cleanup 一次性脚本: 36 个
- batch/gen 脚本: 4 个
- legacy/残留: 11 个
- 保留率: 39/90 = 43%

## Hooks (1-4 Dev/scripts/hooks/) — 4 个

| path | purpose | created | owner | status | smoke |
|------|---------|---------|-------|--------|-------|
| `hooks/pre-write-check.sh` | 写文件前5维检查 | 2026-07-20 | lovart-quality | active | 16/16 |
| `hooks/post-write-check.sh` | 写完后5维检查 | 2026-07-20 | lovart-quality | active | 16/16 |
| `hooks/pre-import-check.sh` | Sanity import 前检查 | 2026-07-20 | lovart-ops | active | 16/16 |
| `hooks/post-generation-check.sh` | 统一质量门禁(图片404/SEO/质量/批量脚本) | 2026-07-23 | lovart-management | active | 20/20 |
