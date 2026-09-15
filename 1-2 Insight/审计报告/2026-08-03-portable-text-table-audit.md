# 审计：Blog Portable Text 表格排版（2026-08-03）

## 结论

上一轮「五层 tableCell」修复方向与 Lovart 已部署 schema **相反**。真正会稳定渲染的形态是：

`table(_key) → tableRow(_key) → cells: string[]`

`tableCell` 类型在 `o11tm2qe` schema 中不存在；生产抽样可渲染表格（pillar ja/pt/ru 等）全部是 string cells。仍有一批文档用 `cells: block` 对象，属于历史污染，前端易丢格式。

## 证据

1. MCP `get_schema type=tableRow`：`cells` of `string`
2. MCP `get_schema type=tableCell`：Type not found
3. GROQ 生产样本：`cells: ["Workflow", "Best for", ...]`
4. 另有 object-cell 样本（ko/zh/zh-TW review 文）：`cells[0]._type == "block"`

## 本轮已做

1. 纠正 SSOT `md_to_portable_text.py` → string cells + `validate_portable_text_body` / `count_key_issues`
2. 纠正 `_md_table_repair.py` 的 `make_table_block`
3. 清除残留内联转换器：
   - `1-4 Dev/scripts/import_zh_product_blogs_to_sanity.py`
   - `1-2 Insight/SEO Reports/patch-sanity.py`
4. 5 个 batch-rewrite 脚本 `sys.path` 改指向 Local Dev SSOT
5. 新增 `validate_pt_body.py` 门禁
6. 固化：TOOLS-REGISTRY / RULE 9 / skill Pitfall #62 / portable-text-table-syntax.md

## 残留 HAND_PT 脚本（未改逻辑，已登记）

这些脚本手拼 block/span（多数不含表格），风险低于错误 table shape，但新工作禁止复制其模式：

- `Local Dev/Temp/generate_5_zh_articles.py`
- `Local Dev/scripts/active/_patch_zh_blogs.py`
- `Local Dev/Output/zh-blog-batch/patch_5_articles.py`
- `Local Dev/Output/gen_payloads.py`
- `Local Dev/Output/patch_articles.py`
- `Local Dev/Output/Lovart-Blog-Pipeline/.../articles.py`
- `1-3 GenFlow/Lovart-Blog-Pipeline/articles.py`
- `tmp/c_batch_group1_structure_fix.py`

处理原则：新写/改写时改走 `md_to_portable_text`；一次性脚本用完归档，不扩散。

## 生产存量清理（已完成）

- 脚本：`~/Documents/Lovart Local Dev/scripts/normalize_table_cells.py`
- 范围：16 篇（de/en/es/ja/ko/ru/zh/zh-TW）
- dry-run → apply：`patched=16 blocked=0`
- 复检：`object_cell_docs = 0`
- 报告：`~/Documents/Lovart Local Dev/Output/QA-Memo/table-cell-normalize-2026-08-03.json`

## table/row `_key` 补齐（2026-08-04 已完成）

- 脚本：`~/Documents/Lovart Local Dev/scripts/repair_table_keys.py`（`ifRevisionID` 防并发覆盖）
- 执行前排查：P0 改的是 `compositePage.bodyJson`，与 blog `body` 不冲突；face-swap EN 等活跃 body 写入默认 exclude
- 实际待修已从先前普查的 ~213 收缩到 **22**（其余期间已被其它 body 重写带走）
- apply：`patched=22 conflict=0 failed=0`
- 复检：`row_key_missing_docs=0` / `table_key_missing_docs=0`
- 报告：`~/Documents/Lovart Local Dev/Output/QA-Memo/table-key-repair-2026-08-04.json`

## 下一步（未做）

1. 上述修过的表格页若 CDN 仍缓存旧结构，主动 revalidate
2. 可选：pre-commit 阻断新增 `def md_to_pt`
3. ES 文 `2uHMXNBF8GsKL6QSzuprtD` 正文其它 block 仍缺 `_key`（与表格无关）

## 验收

```bash
python3 ~/Documents/Lovart\ Local\ Dev/scripts/md_to_portable_text.py <<'MD' | python3 -c 'import json,sys; from pathlib import Path; sys.path.insert(0,str(Path.home()/"Documents/Lovart Local Dev/scripts")); from md_to_portable_text import validate_portable_text_body; b=json.load(sys.stdin); print(validate_portable_text_body(b))'
| A | B |
|---|---|
| 1 | 2 |
MD
```
