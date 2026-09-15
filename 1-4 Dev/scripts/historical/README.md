# 历史 SEO 报告批处理

在 DataWorks 不完整时先生成 **Draft v0** 月报/专题/季年报；补齐 xlsx 后升 **Final v1**。

## 快速开始

```bash
# 推荐（iCloud 可能锁 scripts/*.py，用 shell 入口）
cd "1-4 Dev/scripts"
./report_batch_runner.sh inventory

# 或直接进 historical/
cd "1-4 Dev/scripts/historical"

# 1. 盘点 16mo 数据覆盖
python3 report_batch_runner.py inventory

# 2. 回填月快照（GSC+GA4，耗时）
python3 report_batch_runner.py backfill-snapshots --from 2025-03 --to 2026-05

# 3. Draft 月报 + 水印
python3 report_batch_runner.py render-monthly --from 2025-03 --to 2026-05 --tier draft

# 4. 专题报告（依赖月报）
python3 report_batch_runner.py render-topics --from 2025-03 --to 2026-05

# 5. 季报 / 双月报 / 年报 / 整体史
python3 report_batch_runner.py render-quarterly --from 2025-Q1
python3 report_batch_runner.py render-bimonthly --from 2025-B3 --to 2026-B3 --skip-errors
python3 report_batch_runner.py render-annual --from-year 2025 --to-year 2026

# 6. 复盘周 / 自然周
python3 report_batch_runner.py render-weekly --type review --from-date 2026-01-01
python3 report_batch_runner.py render-weekly --type natural --from-date 2026-01-01

# 7. 日报（默认近 90 天）
python3 report_batch_runner.py render-daily --days 90

# 8. DataWorks 补齐后升 Final
python3 report_batch_runner.py finalize-monthly --from 2025-03 --to 2026-05
```

## 产出路径

| 类型 | 路径 |
|------|------|
| 盘点 | `reports/_inventory/history-coverage.json` |
| 月报 | `reports/monthly/Lovart-SEO-YYYY-MM.md` |
| 专题 | `reports/topics/Lovart-SEO-topic-{name}-YYYY-MM.md` |
| 季报 | `reports/quarterly/` |
| 双月报 | `reports/bimonthly/Lovart-SEO-YYYY-Bn.md`（V2 全结构；B1=1–2月 … B6=11–12月；需四月快照） |
| 年报 | `reports/annual/` |
| 整体史 | `reports/lifetime/` |
| 周报 | `reports/weekly/` |
| 日报 | `reports/daily/` |

## 模块

- `path_constants.py` — 路径 SSOT
- `seo_report_tier.py` — Draft/Full 水印与 §六 占位
- `monthly_with_tier.py` — 月报 + `--data-tier` 包装（主脚本不可写时的 CLI）
- `apply_draft_tier.py` — 月报 Markdown 后处理
- `report_batch_runner.py` — 主编排器
- `report_inventory.py` — 覆盖盘点
- `week_dates_local.py` — 周日期（iCloud 锁 scripts 时 fallback）
- `finalize_monthly.py` — Phase 6 升 Final

## iCloud 注意

若 `scripts/` 或 `reports/monthly/` 报 `Operation not permitted`，请在 Finder 中对该目录执行「立即下载」或暂停 iCloud 优化后再跑批处理。
