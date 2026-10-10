# Lovart 复刻项目交接文档（方案 + 进度）

> 交接对象：Claude Code（接续开发）
> 交接时间：2026-10-10
> 仓库：`/Users/seveno/MFlow Dev/mflow`（main 分支）
> 工作目录：`mflow/dev/wordpress/`

---

## 一、项目目标

在 WordPress（`blogs.lovart.ai`，外部托管，**不在资产服务器上**）复刻 Lovart 官方 17 个落地页，
并在此之上建立两条可规模化的页面生产线：

1. **Faithful 线（原模块）**：源 HTML 整块嵌入 Elementor `widget-html` 微件，视觉 1:1。
2. **Native 线（新模块）**：`build-elementor-native.py` 把 faithful HTML 逐区块转换为
   原生 Elementor 微件（heading/image/button/container），转换失败的区块回退 HTML 嵌入，
   编辑器内可逐元素编辑。

配合 **LPagery** 批量建页插件 + CSV 字段契约，实现「CSV 一行 → 一页」的批量落地页生成。

---

## 二、架构总览

```
┌─ 源设计（lovart.ai Next.js SPA，17 页）
│    ↓ 抓取
├─ 资产服务器 nownexts.com（VPS 172.96.253.73，SSH 端口 28766，root）
│    /www/wwwroot/nownexts_com/lr-assets/
│      ├── pages/*.html                 # 17 页源 HTML（按 slug）
│      ├── lovart-replica.css?v=3       # 2.9MB tailwind + 源站样式（作用域化到 .lr）
│      ├── lovart-native.css?v=16       # shim：修 e-con chrome / 工具类解压制 / dark 变量注入
│      ├── lovart-faithful-mirror.css?v=1  # 未分层工具类镜像（压过 e-con chrome）
│      ├── lovart-replica.js?v=15       # 全部运行时行为（见 §四）
│      ├── elem/faithful/*.json         # faithful 模板（widget-html 嵌入）
│      ├── elem/native/*.json           # native 转换模板
│      └── elem/native-templates/*      # lr-native-*-full.json（LR Native 模板分类）
│    ↑ Cloudflare CDN（注意：边缘坏缓存是重大事故源，见 §六）
│
├─ WordPress（blogs.lovart.ai，另一台主机，只能经浏览器 REST/admin-ajax 操作）
│    ├── 主题 lovart-theme（本地副本可能滞后）
│    ├── Code Snippets 插件：
│    │     snippet 27 "Lovart Replica - Assets"（资产 enqueue + body 类 + sticky 重建 + lr_set_replica_flag 端点）
│    │     snippet 29 "LR Elem Bridge"（lr_elem_import / lr_elem_read / lr_elem_template 端点，secret=lrb-2026-x7k9）
│    ├── LPagery（CSV 批量建页，契约见 native-modules/csv-contract.md）
│    └── 页面两种形态：
│          17 页线上页（_lr_replica=1 + 模板 lovart-replica-template）
│          7 页 demo A/B（同上，本轮新增）
│
└─ 本地构建脚本（mflow/dev/wordpress/）
     build-elementor-native.py        # faithful → native 转换器
     build-lpagery-native-seed.py     # LPagery 种子模板 + 边界 CSV
     export-replica-pages.py / audit-*.py
```

### 渲染管线（理解它才能不踩坑）

- 页面 meta `_lr_replica=1` → snippet 27 给 body 加 `lr-replica-page` 类 + inline CSS 隐藏主题 header/footer，
  `_elementor_data` 含 `lr-native` 的页面额外加 `lr-native-page` 类（native 专用 CSS 作用域）。
- 页面模板 `lovart-replica-template` 由 `lr-replica-snippet.php` 的 `theme_page_templates` filter 注册
  （该 PHP 的部署位置在 WP 侧，本地仓库只有源码副本）。
- **REST API 不能设该模板**（Elementor 把 template enum 锁死为 3 种，返回 400）。
  正确路径：snippet 27 的 `admin-ajax action=lr_set_replica_flag`（写 `_lr_replica` + `_wp_page_template` 两个 meta）。
- 资产加载判定 `lr_replica_has_module()`：`_lr_replica` 或 `_elementor_data` 含 `class="lr` / `lr-native` / `lr-faithful`。

---

## 三、当前页面清单

### 线上 17 页（全部验收通过）
`https://blogs.lovart.ai/replica-homepage`、`replica-tool-directory`、`replica-comparison-hub`、
`replica-content-hub`、`replica-people-reviews`、`replica-product-launch`、`replica-showcase-gallery`、
`replica-solution-ai-design-for-fitness-wellness-hub`、`replica-solution-ai-design-for-small-business-hub`、
`replica-solution-ai-design-solution-for-agencies`、`...-for-creators`、`...-for-marketing-teams`、
`...-for-nonprofits`、`...-for-saas`、`...-for-shopify`、`replica-solution-good-design-for-business-owners`、
`...-for-marketers`

### Demo A/B 对照批（7 页，本轮产出，均已发布+验收）
| 主题 | Native 版 | Faithful 版 |
|---|---|---|
| Shopify | lr-demo-native-shopify (id 18879) | — |
| Fitness | lr-demo-native-fitness (18875) | lr-demo-faithful-fitness (18877) |
| Product Launch | lr-demo-native-product-launch (18871) | lr-demo-faithful-product-launch (18873) |
| Comparison Hub | lr-demo-native-comparison-hub (18867) | lr-demo-faithful-comparison-hub (18869) |

---

## 四、replica.js 运行时行为清单（v15）

| 模块 | 作用 |
|---|---|
| `initCssHeal` | 跨域 CSS link 自动升级 `crossorigin=anonymous` + `?r=` nonce——绕过 CDN no-cors 坏缓存（**裸样式回归的真根因**，见 §六） |
| `initLazyFix` | 还原懒加载插件没处理完的 `data-lazy-src`（src 是 0 尺寸 SVG 占位） |
| `initLinkFix` | ① CTA button（Get started/Get X now 等文案）→ 跳 `lovart.ai/canvas`；② `href="#"` 死链：试用意图→/canvas，指引意图→preventDefault+滚动到 workflow/capability/showcase 区块；③ 真站 404 外链改道（3 篇 blog→/blog、/nonprofit→solution 页）+ 清 `?cb=` 参数；④ 隐藏源模板设计说明泄漏（"cta · bgStyle:" 等）。**作用域仅 `.lovart-replica-scope, .lr` 内**，防止误绑 WP admin bar |
| `initFaqFill` | FAQ 空面板按 `LR_FAQ_ANSWERS[pageSlug()]` 注入真答案；目标 `[data-lp-section="faq"]` 或 `.lr-native-faq`；占位文案（/every word stays editable/i）清空重填 |
| `pageSlug` | 剥 `replica-solution-` / `lr-demo-(native\|faithful)-` 前缀 + 短别名映射（fitness→ai-design-for-fitness-wellness-hub 等 12 个） |
| `initCompareFill` | 对比表空壳按 `LR_COMPARE` 注入 + 补 Lovart 高亮列；目标兜底 `.lr-native-comparison-table` |
| `initPricingRender` | 源 HTML pricing 区是 animate-pulse 骨架（抓取时未 hydrate）→ 按真站实测数据重渲染：annual 默认态折扣价/划线价/徽标（Starter $16~~$19~~、Basic $27、Pro $45~~$90~~ 50% off、Ultimate $109~~$199~~）、monthly 态、Pro 卡 lime 边框 + Most popular 徽章、月/年切换联动 |
| `initAccordion/initTabs/initSlider/initChat/initTheme/initLang` | 手风琴/tabs/before-after 滑块/聊天/主题语言切换 |
| `initNoJump` | 锚点防跳顶（死链/空 hash preventDefault） |
| `initDragScroll` | 横向卡片列表拖拽滚动 |

---

## 五、已完成里程碑

1. ✅ 17 页 faithful 复刻上线，四维验收（功能/文案图片/动效/跳转）全绿
2. ✅ CSS 裸样式回归根因治愈（initCssHeal）
3. ✅ native.css 历轮修复：e-con chrome 压制（v12 拓扑修正）、workflow-vertical 换行（v13）、
   定价切换器（v14）、demo header 白条（v15）、native 独立容器白条（v16）
4. ✅ Native 转换器 + 转换报告（composite 10 native / 23 fallback；17 页逐页数据见
   `elem-native/conversion-report.json`）
5. ✅ LPagery 种子模板（lp-lr-native-v1）+ CSV 契约 + 3 行边界样本
6. ✅ Demo A/B 批次 7 页上线（本节上方清单）
7. ✅ 本轮修复合计 4 个 commit：
   - `18995f14` P0 体验对齐（CSS 自愈/手风琴/懒加载/字体）
   - `64a13a39` 定价对齐真站 + workflow-vertical 换行
   - `7c965c42` 链接与 CTA 生产化
   - `53173660` v15 demo FAQ/别名/白条
   - `4700748b` v16 native 独立容器白条

---

## 六、重大事故与教训（必读）

1. **CDN 坏缓存 → 全页裸样式**：`lovart-replica.css`（2.9MB）在 no-cors 模式命中 Cloudflare
   边缘坏缓存时，渲染引擎**静默弃用整份样式表**（无报错）。表现为页面裸文本。修复 = CORS 模式
   （crossorigin=anonymous）+ nonce 参数绕过。**任何"样式突然全丢"先怀疑这个**，别急着改 CSS。
2. **demo 页样式污染**：手工新建页面用 `elementor_header_footer` 模板会混入 40+ 主题/插件 CSS，
   压制 tailwind 工具类（w-full 失效→白缝）+ 缺 dark 变量（区块变浅色）。
   **LR 页面必须打 `_lr_replica` 标记**。
3. **验证必须看截图**：`page.evaluate` 数 DOM/字号不够，布局塌陷只有人眼看图才发现。
   ego-browser 视口是 2421px 宽，`clip:{width:1280}` 只能截到左半，别误判。
4. **WordPress 不在 172.96.253.73 上**：那台只是静态资产服务器。WP 一切操作走浏览器
   （REST + admin-ajax + code-snippets API）。
5. **REST 限制**：页面 template 参数被 Elementor 锁 enum；改模板走 `lr_set_replica_flag`。
6. **本机 curl 到 nownexts.com 会 404**（DNS 污染），`--resolve nownexts.com:443:172.96.253.73`
   可绕过；浏览器内不受影响。

---

## 七、操作手册（常用命令）

### 部署资产
```bash
node --check <js 文件>   # 必须先过
scp -P 28766 <file> root@172.96.253.73:/www/wwwroot/nownexts_com/lr-assets/<file>
```

### bump 版本号（snippet 27 内的 URL query）
经浏览器运行 /tmp/snippet-update.js 模式：GET/PUT `/wp-json/code-snippets/v1/snippets/27`（字段 `code`），
nonce 从 wp-admin 页面 script 抓 `"nonce":"..."` 或 `admin-ajax?action=rest-nonce`。
当前线上版本：replica.css v3 / native.css v16 / mirror.css v1 / replica.js v15。

### 建新 demo 页（单页一个脚本，规避 evaluate 15s 超时；env 变量不传入 ego-browser，需内联）
1. REST 建页（title/slug/status=publish/template=elementor_header_footer）
2. `admin-ajax action=lr_elem_import&page_id=<id>&url=<模板 json>&nomark=1&secret=lrb-2026-x7k9`
3. `admin-ajax action=lr_set_replica_flag&page_id=<id>&secret=lrb-2026-x7k9`（模板接管 + body 类）
4. 模板 json 可放 `elem/faithful/`（faithful）或 `elem/native/`（native），先 scp 上传

### 浏览器自动化
`ego-browser nodejs < script.js`；`await taskSpace(32)` + `task.page("p1")`；
`page.evaluate` 硬超时 15s（单次只做一小件事）；page.on / page.$ / setViewportSize 不可用；
Node 侧 fetch 测外链（页面内跨域 fetch 会 ERR）；`page.screenshot` 可用（clip 全宽注意视口 2421）。

### 验证脚本（/tmp 下，ego-browser nodejs 运行）
- `verify-final2.js` — 17 页全量回归（taskSpace 已改 32）
- `verify-fix15.js` — demo 页 FAQ/header/破图
- `verify-env.js` — 接管环境检查（CSS 集合/body 类/白缝）
- `shot-demos.js` / `shot-compare.js` — 截图自查
- `/tmp/lr-demo-build.js`（建页模板脚本，`__ITEM__` 内联替换）

---

## 八、遗留事项（按优先级）

### P1 — Native 转换器内容增强（下一阶段主线）
现状：转换器只把 **FAQ、CTA** 等简单区块转成真原生微件（带 `lr-native-*` 类），
**hero/bento/stats/pricing 等复杂区块全部 fallback**（widget-html 整块 HTML，前端视觉一致但编辑器内不可逐元素编辑）。
- 转换报告：`elem-native/conversion-report.json`（17 页 native/fallback 统计）
- 转换器：`build-elementor-native.py`（区块级 build_hero/build_stats/build_faq/build_cards；
  HTML 解析用 BeautifulSoup；语义 IR 见 `native-modules/module-map.json`）
- 验收：转换后区块在 Elementor 编辑器中可编辑 + 前端截图与 faithful 版逐区块对照
- 批量转换命令：`python3 build-elementor-native.py --src elem-src --out elem-native`

### P2 — LPagery 批量生产线
- 契约：`native-modules/csv-contract.md`（LPagery 单花括号占位符；一行一页；先生草稿后发布）
- 种子：`lp-lr-native-v1-pro.json` / `lp-lr-native-v1-free.json`（含占位符的 Elementor 模板）
- 样本：`lp-lr-native-v1-sample.csv`（bakery/saas/wellness 3 行边界样本，含超长文案边界）
- 待做：用真实行业内容批量生成页（demo 页的 lr_set_replica_flag 流程需并入 LPagery 生成后处理）

### P3 — 小项
- 定价卡内 "Hot Models" 模型价格小字表（真站卡内有，目前省略）
- people-reviews 页无 `.lovart-replica-scope`（另一种导出形态，渲染正常仅结构不一致）
- replica.js 里 initCssHeal 的 `?r=` nonce 每次刷新变化——观察 CDN 坏缓存轮换情况，稳定后可简化
- 源 HTML 里 6 页的设计说明文字泄漏已在 DOM 层隐藏，根治可在 export-replica-pages.py 导出时过滤

---

## 九、环境备忘

- 资产服务器：`ssh -p 28766 root@172.96.253.73`，资产根 `/www/wwwroot/nownexts_com/lr-assets/`
- 浏览器自动化 TaskSpace：**32**（28 已过期）
- 用户规则：**始终简体中文回复**；不问就干（自主推进）
- 用户验收标准（四维）：①功能完整 ②标题文案/图片美观 ③动效完整 ④点击跳转正常
- git：仓库根 `mflow/`（注意不是 MFlow Dev 根）；commit 风格 `fix(replica): ...`
- 本机直连 nownexts.com 会 DNS 污染 404，验证走浏览器或 `--resolve`
