# Portable Text 表格语法（Lovart SSOT）

> 2026-08-03 对照 `o11tm2qe` / `production` 已部署 schema 纠正。
> 转换入口：`~/Documents/Lovart Local Dev/scripts/md_to_portable_text.py`

## Schema 真相

`tableRow.cells` 的类型是 **`string[]`**。

- schema 里有：`table`、`tableRow`
- schema 里**没有**：`tableCell`
- 生产里能正常渲染的表格（如 pillar ja/pt/ru）全部是 string cells

## 唯一合法结构

```json
{
  "_type": "table",
  "_key": "<random>",
  "rows": [
    {
      "_type": "tableRow",
      "_key": "<random>",
      "cells": ["列1", "列2", "列3"]
    }
  ]
}
```

硬规则：

1. `table`、`tableRow` 必须有 `_key`
2. `cells` 必须是纯字符串数组
3. 禁止 `tableCell` / `block` / `span` 树塞进 cells
4. 单元格内 Markdown（`**bold**`、链接）在转换时剥成纯文本

## 历史错误（禁止再犯）

| 错误形态 | 来源 | 后果 |
|---|---|---|
| cells = `_type:block` 对象 | 旧 RULE 9 / `patch-sanity.py` / `_md_table_repair.py` | schema 不符，前端丢格式 |
| cells = `_type:tableCell` 五层树 | 误读通用 Sanity 文档后写进 SSOT | schema 无此类型，必炸 |
| 缺 `_key` 的 table/row | 早期转换器 | Sanity 强校验下渲染失败 |
| 脚本内联 `def md_to_pt` | 批量发布脚本各写一份 | 一处修了别处继续污染 |

## 验证

```python
from md_to_portable_text import md_to_portable_text, validate_portable_text_body

blocks = md_to_portable_text(md)
result = validate_portable_text_body(blocks)
assert result["ok"], result["issues"]
```

CLI：

```bash
python3 ~/Documents/Lovart\ Local\ Dev/scripts/validate_pt_body.py path/to/body.json
# 或对 NDJSON 每行 body 字段：
python3 ~/Documents/Lovart\ Local\ Dev/scripts/validate_pt_body.py --ndjson import.ndjson
```

## 脚本铁律

任何生成 / patch blog `body` 的脚本：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "Documents/Lovart Local Dev/scripts"))
from md_to_portable_text import md_to_portable_text
```

禁止：

- 内联 `def md_to_pt` / `def markdown_to_portable_text`
- 手拼 `_type: "table"` 且 cells 用对象
- 从其他项目复制「五层 tableCell」模板
