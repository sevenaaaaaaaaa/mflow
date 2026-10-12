# 微件样本（sample）

`migrate-widgets.py` 靠这里的 sample **反查目标微件的真实 settings key**，
不猜任何插件的键名。见交接文档 §十。

## ⚠️ 当前全是测试夹具，不是真结构

| 文件 | 状态 |
|---|---|
| `faq-sample.EXAMPLE.json` | 夹具 · `eael-adv-accordion` 的字段名是**编的** |
| `comparison-table-sample.EXAMPLE.json` | 夹具 · `eael-adv-data-table` 同上 |
| `pricing-block-sample.EXAMPLE.json` | 夹具 · `htmega-flip-switcher-pricing` 同上 |
| `cta-default-sample.EXAMPLE.json` | 夹具 · `eael-cta-box` 同上 |

它们只用来验证脚本机制（反查、构造、自检、链式）跑得通，
**用它们产出的 `elem-migrated/` 绝不能导入线上** —— 字段名对不上，会生成坏微件。

## 怎么换成真的

1. 在 Elementor 编辑器里手搭一个目标微件
2. 前两行用哨兵填：`__A1_1__` `__A1_2__` …（第 2 行 `__A2_1__` …）
   - 平铺字段的微件（如 CTA）只填第 1 行
   - 有两个重复器的（如月付/年付价格表）第二个用 `__B1_1__` …
3. 导出那段 JSON，存成 `<module>-sample.json`（去掉 `.EXAMPLE`）
4. 先 `--inspect` 确认字段反查对了，再 `--write`

```bash
python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --inspect
```
