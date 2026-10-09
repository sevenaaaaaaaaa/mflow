---
session_date: 2026-10-09
session_topic: "复刻模块 → Elementor 模板库（245 个 lr-* 模板）+ 模块级资产按需加载 + 五类代表页形态研究"
session_slug: "replica-elementor-templates"
profiles_used: [profile-lovart-management]
tools_used: [build-elementor-templates.py, lr-elem-bridge.php(lr_elem_template 端点), lr-assets-snippet.php(模块级检测), ego-browser]
agents: [cursor]
duration_min: 150
files_changed_count: 4
kb_units_added: 0
schema_bumps: 0
related_sessions: ["2026-10-09-round35-elementor-native"]
status: ready
---

# Context
- 用户指定 5 类站点代表页面（需学习复刻的形态基准）并下达新指令：
  "你现在的模块都需要成为 elementor 的一个模板"——复刻模块必须进入 Elementor
  模板库（elementor_library），与站点现有模板体系（Header/Footer/FAQ/LPagery 种子等
  36 个）并列，可插入任意 Elementor 文档。

# 五类代表页形态（研究结论）
1. **博客首页** /（page-id-126）：elementor_canvas，21 容器/52 微件，纯 Elementor 搭建。
2. **seedance2_0**（id 15695，elementor_canvas）：代码模块（HTML 微件）+ 固定顶底，
   9 容器，首个容器 sticky:top —— **与复刻页架构完全同构**（其原生 sticky 正常，
   复刻页导入路径的 sticky 引擎损坏 → 兜底重建仍是必要补丁）。
3. **纯 Elementor 模块页**：原生微件（heading/text-editor/button/video）搭建，
   bakery 页即此类。
4. **bakery 页**（id 17034，LPagery 批量）：12 容器 + 原生微件（elementskit-blog-posts、
   ucaddon_image_accodion 等），由 lp-template-new 种子模板 + CSV 批量生成。
5. **博客详情页**（post 18199）：Gutenberg 正文 + Elementor Pro 主题头
   （data-elementor-type=header）。
- 站点现有模板库惯例：template_type=page（lp-template-new、e-commerce 均为"1 容器
  +1 HTML 微件"）、container（faq 等小模块）、header/footer（主题构建器）。

# Solution
**245 个 LR 模板入库**（18 整页 page 型 + 227 单区块 container 型）：
- `build-elementor-templates.py`：读 18 页 elem JSON → 每页整页模板 + 每区块
  container 模板（短名从 HTML 微件首个 h1/h2/h3 提取），产出 245 JSON + manifest。
- Bridge 新端点 `lr_elem_template`：admin-ajax + secret，WP 侧从 nownexts.com 拉取
  JSON，按 post_name upsert elementor_library 帖子（写 _elementor_data/
  template_type/version），WAF 零暴露。浏览器 cookie+nonce 循环调用，245/245 成功。
- **模块级资产按需加载**（lr-assets-snippet.php 升级）：`lr_replica_has_module()`
  = _lr_replica 整页 OR _elementor_data 含 `class=\"lr`（JSON 转义形态）。命中即
  enqueue CSS v2/JS/sticky 重建脚本；隐藏主题头尾与 lr-replica-page body class
  仍仅限 _lr_replica 整页——插入单模块的页面保留自身主题头尾。
- Bridge `lr_elem_import` 加 `nomark=1`（写数据不标 _lr_replica，供模块页/测试）。

# 验证
- 模块插入测试页（无 _lr_replica，2 模块）：.lr 渲染、css v2/JS/sticky 重建自动
  加载、无 lr-replica-page body class、主题头保留可见（截图 /tmp/module-test-page.png）。
- 历史页零泄漏复查：seedance2_0 / bakery / blog 详情均无 lr-css。
- 复刻页回归：homepage/comparison 全项通过。
- 模板 meta 抽查：lr-homepage-01 type=container、1 元素，与现有 faq 模板同构。
- 测试页已删，module-test.json 已清。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| dev/wordpress/build-elementor-templates.py | add | 245 模板生成器（manifest 驱动） |
| dev/wordpress/lr-elem-bridge.php | upgrade | +lr_elem_template 端点 +nomark 参数 |
| dev/wordpress/lr-assets-snippet.php | upgrade | +lr_replica_has_module 模块级检测 |
| dev/wordpress/elem-src/, elem-templates/ | add | 18 页源 JSON + 245 模板产物（manifest.json） |
| harness/11-knowledge-sandbox-backup/ | add | 本日志 |

# Decisions Made
- D1: 模板命名对齐现有库惯例（短英文 slug + Title Case），前缀 lr- 防撞：
  lr-{short}-full（page）/ lr-{short}-{nn}（container）
- D2: 整页模板（18）与单区块模板（227）并存：整页可一键铺页，区块可任意混搭
- D3: 资产加载判定从"仅 _lr_replica"扩为"整页 OR 模块内容检测"，保证模板插入
  任意 Elementor 文档（页面/文章/LPagery 生成页）即用
- D4: 主题头尾隐藏与 body class 保持 _lr_replica 专属——单模块页面不破坏其主题
- D5: 模板 upsert 按 post_name 去重，重跑幂等（断点续传用 REST 列表预查）
- D6: seedance 页原生 sticky 正常 → 复刻页 sticky 引擎损坏根因在批量导入路径
  而非全局 Pro bug；兜底重建脚本保留

# Patterns Observed
- P9: ego-browser page.fetch 受页面 CORS 限制（跨域 nownexts.com 抓 manifest 被
  拦）；跨域资源用 Node 原生 fetch()，同站管理操作才用 page.fetch
- P10: elementor_library 有 show_in_rest（REST 可列/可读），meta 写入走自建通道；
  Elementor 模板类型判定 = _elementor_template_type meta（page/container/header），
  与现有模板完全同构即可被编辑器模板库识别
- P11: 245 个小文件 scp 走单 SSH 连接约 5 分钟；后续大批量先 tar 打包再传
- P12: WP 里 _elementor_data 的 JSON 引号转义形态是 `class=\"lr`（检测匹配用）

# Open Questions
- Q1: 227 区块模板与现有库 36 模板混列，是否需要给 LR 模板建独立分类 term
  （elementor_library_category）便于筛选
- Q2: 区块模板内容仍是"整段 HTML"，未来是否逐块拆成原生微件（bakery 式）以支持
  LPagery 字段替换——当前 HTML 微件内文字无法被 LPagery 占位符替换
- Q3: gpt_image_2 六页去留（用户已答：不动）

# Cross-References
- entities: replica-pipeline, elementor-template-library, lr-assets
- decisions: MEMORY-PROJECT.md § 5 (不问就干)
- skills: wordpress-design-replication

# Tags
- relevant-tags: #wordpress #elementor #template-library #modularity #lpagery