---
session_date: 2026-10-09
session_topic: "Elementor 原生模块化、LPagery 种子与 18 页分批迁移"
session_slug: "elementor-native-modules"
tools_used: [Elementor, LPagery, Code Snippets, ego-browser]
status: complete
---

# Outcome
- 建立模块映射与 LPagery CSV v1 契约；复杂动画模块继续使用 HTML 回退。
- 18 个 Elementor 文档转换出 68 个原生区块、159 个 HTML 回退区块。
- Elementor 模板库新增并更新 86 个 `LR Native` 模板：18 个混合整页模板和
  68 个原生容器模板。
- `lp-lr-native-v1` 种子包含 Hero、Stats、Proof、Reviews、Portrait、FAQ、CTA
  七个原生容器；LPagery Free 用 3 列 CSV 实际生成 3 张草稿样本页。
- Free 版不提供 Bulk Update；保留 81 列 Pro 契约，并用可审计的物化 JSON 刷新样本。
- 三张样本均为 7 个原生容器、0 个 HTML 微件、0 个残留 token；桌面和 390px
  移动端通过，Elementor 编辑器可打开原生 heading/text/button/image/accordion。
- 迁移前为 18 页保存本地及远端回退快照；随后按 3 + 5 + 5 + 5 分批迁移。
- 全站公开回归审计：18/18 复刻页通过，562/562 历史页无 Replica/Native 资产泄漏，
  问题数 0。

# Important Fix
- 当前 Elementor 运行时使用 `css_classes` 输出自定义类；Bridge 写入新
  `_elementor_data` 后还必须删除 `_elementor_element_cache`，否则前端会继续使用旧的
  元素 HTML 缓存。Bridge 已同时清理元素缓存和 CSS 缓存。

# Rollback
- 本地：`dev/wordpress/native-rollout-backups/2026-10-09-pre-native/`
- 远端：`/lr-assets/elem/backups/2026-10-09-pre-native/`
- 每份快照都是 Bridge 可直接重新导入的 `{version,data}` 格式，并附页面元数据。

# Validation
- `python3 dev/wordpress/test-elementor-native.py`
- `python3 dev/wordpress/audit-native-pages.py`
- `python3 dev/wordpress/audit-replicas.py --workers 8`
