# 微件样本（sample）

`migrate-widgets.py` 靠这里的 sample **反查目标微件的真实 settings key**，
不猜任何插件的键名。见交接文档 §十。

## 真实样本（字段名经插件源码核对 + 线上渲染实证，2026-10-12）

| 文件 | 微件 | widgetType | 状态 |
|---|---|---|---|
| `faq-sample.json` | EA Advanced Accordion | `eael-adv-accordion` | ✅ 可用 · 重复器 `eael_adv_accordion_tab`，2 槽：`eael_adv_accordion_tab_title` / `eael_adv_accordion_tab_content` |
| `cta-default-sample.json` | EA CTA Box | `eael-cta-box` | ✅ 可用 · 平铺 5 槽：`eael_cta_title` / `eael_cta_btn_text` / `eael_cta_btn_link.url` / `eael_cta_secondary_btn_text` / `eael_cta_secondary_btn_link.url` |

字段名来源：wp.org 插件源码 `includes/Elements/Adv_Accordion.php`、`Cta_Box.php` 的
controls 定义（非猜测）。线上实证：`?elementor_library=` 被主题覆盖，改由
`lr-sample-render-*` 验证页承载渲染（哨兵位置、折叠样式、按钮均正确），
验证页已删，elementor_library 模板 `lr-sample-ea-accordion` / `lr-sample-ea-cta` 保留作参照。

### 零猜测流程的自动化（2026-10-12 起不再需要人工手搭）

人工「编辑器手搭 → 填哨兵 → 导出」已由以下流程取代：

1. 从 wp.org SVN 拉微件源码（`plugins.svn.wordpress.org/<pkg>/trunk/includes/...`）
2. 读 `get_name()`（widgetType）与 `add_control(...)` 的字段名 / repeater 的 `fields`
3. 手写哨兵 JSON（settings 用真实键名填 `__A1_1__` …）
4. `lr_elem_template` 导入 elementor_library + `lr_elem_import` 放到临时页，前台截图实证
5. 通过后把 JSON 存为本目录正式 sample

## ⚠️ 仍是测试夹具的两个

| 文件 | 状态 |
|---|---|
| `comparison-table-sample.EXAMPLE.json` | 夹具。且**模型错配**：EA Advanced Data Table 静态模式的数据是一个 `ea_adv_data_table_static_html`（HIDDEN 控件，整块 `<thead>…<tbody>` HTML 字符串）或 `ea_adv_data_table_csv_string`，**没有表头/表体重复器**——`extract_comparison` 的 A/B 组行/列模型填不进去。需脚本支持「多行/列 → 单 HTML/CSV 槽」的渲染模式，或改用其它表微件 |
| `pricing-block-sample.EXAMPLE.json` | 夹具。且**模型错配**：HT Mega 月/年切换微件真实 widgetType 是 `htmega-2026-pricing`（非 `htmega-flip-switcher-pricing`），单重复器 `plan_items`（子字段 `plan_name`/`price_monthly`/`price_annual`/`period`/`tagline`/`features`(换行分隔)/`cta_text`/`cta_variant`/`is_featured`/`featured_badge`，顶层 `show_billing_toggle`），**不是「月付 A 组 / 年付 B 组」两个重复器**——`extract_pricing` 的 A/B 组模型填不进去。需脚本支持「A 组填字段列、B 组列映射到同一重复器的另一字段」，或 `--only-group A`（年价丢失，不推荐） |

## 用法

```bash
# 先 inspect 确认字段反查对了，再 --write
python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --inspect
python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --write
```
