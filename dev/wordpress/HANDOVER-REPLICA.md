# Lovart 复刻项目交接文档（方案 + 进度）

> 交接对象：Claude Code（接续开发）
> 交接时间：2026-10-10 · **方案变更 2026-10-11（见 §零）**
> 仓库：`/Users/seveno/MFlow Dev/mflow`（main 分支）
> 工作目录：`mflow/dev/wordpress/`

---

## 零、方案变更（2026-10-11）——**先读这一节，它推翻了 §一 和 §八**

### 结论

`widget-html` 整块嵌入是这个项目所有问题的根因，而**不是**需要靠「Native 转换器」慢慢优化的权宜之计。
Elementor 生态里已经有现成微件覆盖绝大多数模块，而且**全在已安装的插件的免费层里**。

### 三个实测数字

1. **仓库里 1089 个微件实例，840 个是 `widget-html`（77%）。**
   其余只有 text-editor 108 / heading 75 / button 34 / image 15 / accordion 13 / video 4，全是 Elementor 核心微件。
   → `widget-html` 只有一个 `html` 字段装整块 DOM 字符串，**不可寻址**。这就是「不能批量改 JSON」
   「编辑器里不能编辑」「内容只能靠 replica.js 运行时注入」三件事的同一个根因。

2. **装了 7 个 Elementor 插件包，零个微件在用。**
   Essential Addons / ElementsKit Lite / HT Mega / HT Menu Lite / PowerPack Lite / Royal / UAE / Unlimited Elements
   —— 全部模板 JSON 里找不到任何一个它们的 widgetType。它们现在纯粹在前台加载 CSS/JS。
   **§六 第 2 条记的「40+ 主题/插件 CSS 污染」，大概率主要就是它们。**
   你为此发明了 `_lr_replica` 标记 + `faithful-mirror.css` 去对抗，而对抗的东西有一大半是自己装的、且没用的。

3. **33 个区块里：约 19 个有现成微件，12 个是纯布局（容器 + 核心微件即可），真正要自己做的 1–2 个。**
   而且真实 17 页只用到 31 种，其中 8 种只用过一次，`prompt-launcher` 和 `showcase-horizontal` 从没用过。

### 确定版映射（全部免费，不用再买插件）

| 模块 | 频次 | 用哪个微件 | 来自 |
|---|--:|---|---|
| cta-default | 16× | Call to Action | Essential Addons |
| faq | 12× | Advanced Accordion | Essential Addons |
| workflow-vertical / horizontal | 12× | Vertical Timeline | HT Mega |
| pricing-block | 11× | **Flip Switcher Pricing Table**（自带月/年切换） | HT Mega |
| capability-tabs | 11× | Advanced Tabs | Essential Addons |
| testimonial | 9× | Testimonials | Essential Addons |
| comparison-table | 8× | Advanced Data Table | Essential Addons |
| review-grid-3col / 4col | 4× | Testimonial Carousel | HT Mega |
| comparison-before-after | 4× | Image Comparison | HT Mega |
| stats | 2× | Counter | HT Mega |
| blog-grid / tool-grid | 2× | Post Grid | Essential Addons |
| portrait-grid-3/4、canvas-wall | 4× | Filterable Gallery | Essential Addons |
| logo-loop | 1× | Brand | HT Mega |
| media-marquee | 1× | Content Ticker / Scroll Image | EA / HT Mega |

EA 收费的那几个（Image Comparison / Counter / Logo Carousel / Content Timeline），**HT Mega 免费全有**。
主力只用 EA + HT Mega 两个包；其余 5 个可以先全停（反正零使用）。

纯布局的 12 个（5 个 hero 变体、proof-block、feature-detail、showcase ×2、cluster-block-dense、bento ×3）
用 Elementor 容器 + 核心微件拼，不需要任何插件，天生可编辑、天生可批量改。

### 版本提醒：**不要升 Elementor v4**

线上是 **Elementor Pro 3.35.0，属 v3 线**。
v4（2026-04）的 Variables / Global Classes 需要升大版本 + 手动开启 Atomic Editor，
且官方明确：Classes/Variables **不作用于 v3 微件**，Grid/Loop 还不是原子元素。
**现阶段用 v3 的 Global Colors / Fonts 就够**——它存在 Kit post 里，微件通过 `__globals__`
引用 `globals/colors?id=...`，本来就可批量改。把 lovart.ai 的色板与字体阶梯灌进去，
就是「全局主题复刻」该有的形态（而不是 29k 条 `.lr` 作用域规则 + 2.9MB 下载）。
等模块替换完、页面不再依赖那份巨型 CSS，再在 staging 评估 v4。

### 视觉统一的正确做法

与主站保持视觉统一**没有任何问题，是正确目标**。错的是把还原做在 **DOM 层**而不是 **token 层**。
抽 lovart.ai 的设计 token（颜色/字号/间距/圆角/阴影）→ 落进 Elementor Global Colors/Fonts
→ 所有微件引用 token。改一次品牌色全站跟着变，且不跟主题打架、不需要 mirror.css 压制、
不会被 CDN 坏缓存整页搞崩。

---
## 一、项目目标

> ⚠️ **本节的「Faithful / Native 双生产线」框架已于 2026-10-11 废弃，见 §零。**
> 下文保留作立项背景，不再是执行方案。

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

> ⚠️ **这张表应当持续变短。** 表里的 `initFaqFill` / `initCompareFill` / `initPricingRender`
> 是在运行时把内容塞回空壳——模块换成原生微件后要逐个删掉（见 §八 P1）。
> 剩下的 `initCssHeal` / `initLazyFix` / `initLinkFix` 等是真正的运行时行为，保留。

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

## 八、遗留事项（2026-10-11 重排）

### ⛔ 已取消：原 P1「Native 转换器内容增强」

**不要做。** 原计划是把 fallback 的 hero/bento/stats/pricing 逐块转成 Elementor 原生微件。
但自动转换只能把 HTML 拆成「能点的 div」，**不会凭空长出内容模型**——转完依然没有
可寻址的字段，CSV 批量线依然无从映射。生态里现成的微件才是答案（见 §零）。

`build-elementor-native.py` 与 `elem-native/` 保留作历史记录，不再演进。

### P1 — 按频次把 widget-html 换成生态微件（新主线）

工具已就绪：**`migrate-widgets.py`**（见 §十）。顺序按频次，一次一个模块：

```
cta-default(16×) → faq(12×) → workflow(12×) → pricing-block(11×)
→ capability-tabs(11×) → testimonial(9×) → comparison-table(8×) → 其余
```

**每替换一个模块，必须同步删掉 replica.js 里对应的运行时注入**
（faq → `initFaqFill`，comparison-table → `initCompareFill`，pricing-block → `initPricingRender`）。

> **验收硬指标：`lovart-replica.js` 的行数单调下降。**
> 现在 803 行。它不降，说明只是换了个壳，内容还在运行时注入 —— 那就没走对。

每替换一轮还要确认：对应的硬编码数据表（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`）可以删掉。
内容应该在 Elementor 里，不在 JS 里。

### P1.5 — 停掉没用的插件包

7 个包零使用。保留 Essential Addons + HT Mega，其余在 staging 先停、截图回归、再上生产。
预期收益：前台 CSS/JS 大幅减少，`faithful-mirror.css` 这类压制层可能直接不再需要。

### P2 — 建 token 层

抽 lovart.ai 设计 token → Elementor Global Colors / Fonts（v3，立即可用）。
替换后的原生微件全部引用全局色/字，而不是依赖 `.lr` 作用域规则。

### P3 — LPagery 批量线（依赖 P1）

有了原生微件的具名 settings key，CSV 一列 → 一个字段才真正成立。
契约 `native-modules/csv-contract.md` 需要按新的微件字段重写。

### P4 — 小项（原 P3 保留）

- 定价卡内 "Hot Models" 小字表
- people-reviews 页无 `.lovart-replica-scope`
- `initCssHeal` 的 `?r=` nonce 稳定后可简化
- 源 HTML 的设计说明泄漏，根治在 `export-replica-pages.py` 导出时过滤

## 九、环境备忘

- 资产服务器：`ssh -p 28766 root@172.96.253.73`，资产根 `/www/wwwroot/nownexts_com/lr-assets/`
- 浏览器自动化 TaskSpace：**32**（28 已过期）
- 用户规则：**始终简体中文回复**；不问就干（自主推进）
- 用户验收标准（四维）：①功能完整 ②标题文案/图片美观 ③动效完整 ④点击跳转正常
- git：仓库根 `mflow/`（注意不是 MFlow Dev 根）；commit 风格 `fix(replica): ...`
- 本机直连 nownexts.com 会 DNS 污染 404，验证走浏览器或 `--resolve`

---

## 十、migrate-widgets.py（widget-html → 原生微件）

### 零猜测原则

脚本**不猜任何插件的 settings key**。你在 Elementor 编辑器里手搭一个目标微件，
用哨兵文本填前两行，导出那段 JSON 当 sample，脚本靠哨兵反查真实字段路径。
对 EA / HT Mega / 任何第三方包通用，也不会因为键名记错而产出废数据。

**哨兵格式**：`__<组><行>_<列>__`

```
__A1_1__  __A1_2__  __A1_3__ …     ← A 组第 1 行的第 1、2、3 列
__A2_1__  __A2_2__  …              ← A 组第 2 行（填两行才能确认是重复器）
__B1_1__  …                        ← B 组（第二个重复器，如年付价格表 / 表头）
```

一个微件最多两个重复器（A / B）。FAQ 那种两列的旧写法 `__T1__/__C1__/__T2__/__C2__` 仍然兼容。

**平铺字段**（CTA 这类一块只有一组字段、没有重复器的微件）：哨兵只填第 1 行
（`__A1_1__` `__A1_2__` …），脚本自动识别为平铺组，直接写字段而不造重复器行。

### 用法

```bash
# 1) 看 sample 被解析成什么（不产出文件）
python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --inspect

# 2) 预演：报告将替换多少块 + 首页内容预览（核对列是否对齐）
python3 migrate-widgets.py --module faq --sample samples/faq-sample.json

# 3) 真产出到 elem-migrated/（不碰 elem-src，不碰线上）
python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --write

# 4) 链式：同一个 --out 连跑多个模块，自动接续上一轮成果
python3 migrate-widgets.py --module comparison-table --sample samples/cmp.json --write
python3 migrate-widgets.py --module pricing-block     --sample samples/pri.json --write
```

产出仍走既有 `lr_elem_import` 流程导入。**脚本不连任何站点。**

**前置步骤**：那 5 个 cta 块吞了页脚的页面，先跑一次 `split-footer.py --write`
（同一个 `elem-migrated/` 目录，链式衔接），再跑 `--module cta-default`。

其他开关：`--only-group A|B`（目标微件只有一个重复器时用）、
`--allow-truncate`（抽取列数多于 sample 字段槽时，明确接受丢列）、`--src` / `--out`。

### 已实现的三个抽取器

| 模块 | 内容从哪来 | 产出 |
|---|---|---|
| `faq` | 问题在 HTML 的 `<h3>`，答案在 `LR_FAQ_ANSWERS` | A 组 2 列（问题/答案） |
| `comparison-table` | **表头**在 HTML 的 `<th>`，**表体**在 `LR_COMPARE` | A 组=表头 1 列，B 组=表体 4 列 |
| `pricing-block` | **整份都在 `LR_PRICING`**（源 HTML 是 `animate-pulse` 骨架，一个价格数字都没有） | A 组=月付 8 列，B 组=年付 8 列 |
| `cta-default` | 全在 HTML 里，但**主按钮没有 href** —— 目标由 `LR_CANVAS` 给 | A 组=平铺 5 列 |

CTA 的 5 列：标题 / 主按钮文案 / 主按钮链接 / 次链接文案 / 次链接链接。
抽取时会固化 `replica.js` 做过的链接处理（`LR_LINK_REDIRECT` 重定向 + 清 `?cb=`），
否则那段 JS 删掉后链接会退回抓取时的旧值。

定价的 8 列：档名 / 现价 / 原价(划线) / 折扣 / 计费说明 / 省钱说明 / 功能清单(换行分隔) / 推荐徽章。
**定价是全站共用一份（非按页），12 页会填成同样内容**——与真站一致。

### 实测结果（2026-10-11，用测试夹具跑通）

| 模块 | 命中 | 替换 | 跳过 | 行数 |
|---|--:|--:|--:|--:|
| faq | 13 页 | 12 | 1 | 76 |
| comparison-table | 9 页 | 6 | 3 | 54 |
| pricing-block | 12 页 | 12 | 0 | 96 |
| cta-default | 17 页 | 10 | 7 | 10 |

跳过的都是**真的没数据**，不是故障：
- faq 跳过 `composite-replica-all`（大杂烩页在 `LR_FAQ_ANSWERS` 里无条目）
- comparison-table 跳过 3 页（`comparison-hub` / `small-business-hub` / `composite`
  在 `LR_COMPARE` 里无条目 —— **这三页的对比表线上就是空壳，需要先补数据**）

cta-default 跳过的 7 页全是**真实的线上缺陷**，不是迁移问题（见 §十一）。

四模块叠加后，这 13 页的 `widget-html` 从 **194 个降到 154 个**（消灭 40 个，20%），
换上 12 个 accordion + 12 个 pricing + 10 个 cta + 6 个 data-table。

### 安全设计

- 默认预演；`--write` 才落盘；只写真替换过的页面（out 目录里的文件 = 已迁移的文件）
- **预览**：预演会打印首个成功页面的逐列内容——N 列很容易错位，写盘前必须肉眼能核
- 数量不一致（问题数≠答案数、表头列数≠表体列数）**直接跳过并报原因**，不截断配对
- `--write` 后自动自检：哨兵残留 / 原 html 块未清除 / 微件 id 重复 / 重复器 `_id` 重复 / 空首列，
  任一不过即非零退出。**自检只检查本轮替换过的页面**（链式迁移时全目录扫会误报）
- 幂等：已迁完的模块再跑一次是「命中 0 页」

### 踩过的三个坑（都在代码注释里标了）

1. 自检曾用 `json.dumps` 后的字符串匹配 `data-lp-section="faq"` —— JSON 里引号被转义成 `\"`，
   **永远不中，静默报通过**。改为匹配原始 html 字符串。
2. 链式迁移时第二个模块从 `elem-src` 读，会用源文件**覆盖掉第一个模块的成果**。
   改为：`out/<同名文件>` 存在就接着改它。
3. 自检扫 out 全目录，会把「上一轮迁过、本轮跳过」的页面误报成失败。改为只检查本轮替换过的。

### 扩展到别的模块

在 `MODULES` 字典里加一个抽取器：

```python
def extract_xxx(html, page_file):
    """返回 ({"reps": {"A": [[列1, 列2, …], …]}, "labels": {"A": ["列名1", …]}}, "")
       或 (None, "跳过原因")"""
    ...
MODULES["xxx"] = extract_xxx
```

注意每个模块的内容来源都不一样，先查清楚再写——别假设内容在 HTML 里。

### 测试夹具

`samples/*.EXAMPLE.json` 是**测试夹具**，用来验证脚本机制，**不是真实的插件字段结构**。
真跑之前必须用编辑器手搭的真 sample 替换它。

---

## 十一、线上内容缺陷清单（2026-10-12 实测发现）

做 cta-default / capability-tabs 抽取器时查出来的，**都是线上真实问题，迁移解决不了，需要人工补内容或改配置**。

### C1 — 5 个页面的 CTA 块吞进了整个站点页脚　🔴

`comparison-hub` · `content-hub` · `product-launch` · `showcase-gallery` · `tool-directory`

这些页的 `data-lp-section="cta-default"` 块有 **23.5KB、19 个链接**，除 CTA 本身还包含：

```
Pricing · Changelog · Docs · News · Terms of Use · Privacy Policy
Explore · Blog · Tools · Features · Solutions · Topics
X · YouTube · LinkedIn · Instagram · TikTok
```

抓取时块边界切错了。**直接把这块换成 CTA 微件 = 这 5 页的页脚整个消失。**

**工具已就位**（2026-10-12）：`split-footer.py`

```bash
python3 split-footer.py            # 预演
python3 split-footer.py --write    # 写出到 elem-migrated/（与迁移脚本同目录，可链式）
```

它用 **解析器**（BeautifulSoup）摘掉 `<footer>`，不是字符串切 ——
实测朴素按 `html[:index]` 切会留下 3 个不闭合的 `<div>`。

同时产出：
- `footer-spec.md` —— 3 栏 / 17 个链接 / 版权 的完整内容规格，Theme Builder 照着搭，不用人肉重抄
- `footer-raw.html` —— 原始页脚（12,337 字符），作视觉比对基准

实测 5 页页脚 **md5 完全一致**，一份全站模板即可。

**顺带记一笔**：原始 cta 块本身 `<div>` 就比 `</div>` 多 1 个（抓取产物自带的不平衡），
摘页脚后这个差值原样保留 —— 不是拆分引入的。页脚内部自身是平衡的。

**拆完页脚 ≠ 这 5 页能迁 CTA 了。** 实测跳过原因从 C1 变成了 C2（见下），
两道闸是独立的，C2 还得人工定文案。

### C2 — 7 个页面的 CTA 文案跑错主题，且链接是死的　🔴

`composite` · `comparison-hub` · `content-hub` · `people-reviews` · `product-launch` ·
`showcase-gallery` · `tool-directory`

全都是同一段 Shopify 文案：

> **Ready to turn one SKU into a full Shopify launch system?**
> [Design a Shopify launch] → `#`　[See the workflow] → `#`

Shopify 的 CTA 出现在**工具目录页、人物评价页、内容中心页**上。
两个链接都是 `#`，`replica.js` 的死链规则把它们变成「滚动到某个区块」，**点了不跳转**。

这是转化漏洞。**需要定这 7 页各自该写什么文案和目标**，之后抽取器会自动放行。

**C1 处理完后，这是 CTA 迁移唯一剩余的阻塞**（实测：5 个页脚页摘掉页脚后，
跳过原因全部从 C1 转为 C2）。各页主题供定文案参考：

| 页面 | 页面主题（hero 标题） |
|---|---|
| `comparison-hub` | Turn one product brief into… |
| `content-hub` | Design for every step… |
| `product-launch` | From product drop to… |
| `showcase-gallery` | Start anywhere in the stack… |
| `tool-directory` | Fix the creative leaks… |
| `people-reviews` | （无 hero h1） |
| `composite` | 大杂烩页，可不管 |

定好文案后直接改 `elem-src` 里对应块的 `<h2>` 与链接，或在 `extract_cta` 里加一张
按页覆盖表 —— 后者更干净，不污染源。

### C3 — capability-tabs 在 12 个页面上 3/4 是空的，且 tab 点不动　🔴

| | 全 12 页一致 |
|---|---|
| tab 标签 | 4 个（`agencies` / `nonprofits` 这两页 0 个，整块只有标题） |
| hidden 面板 | 5 个 |
| **hidden 面板里的字符数** | **全部 0** |
| `role="tab"` / `role="tablist"` 属性 | **一个都没有** |

两个独立问题：

1. **只有第 1 个 tab 的内容存在**，另外 3 个面板是空的。
   又是 React 没 hydrate —— tab 2–4 点击才渲染，抓取时不在 DOM 里。和 pricing 骨架同一个病因。
2. **`initTabs` 根本不触发**。它查 `[role="tablist"]`，而这些块里没有任何 role 属性。

所以线上现状：**4 个点不动的标签 + 1 屏固定内容**。
而且不像 FAQ / 对比表 / 定价，`replica.js` 里**没有给 tabs 写兜底数据表**，什么都没有。

**结论：capability-tabs 不进迁移清单，进内容缺口清单。**
要迁必须先补 11 页 × 3 个面板 = **33 段内容**。这是内容生产任务。

### C4 — 3 个页面的对比表是空壳

`comparison-hub` · `ai-design-for-small-business-hub` · `composite`
在 `LR_COMPARE` 里没有条目，线上就是空表。同 C3，需先补内容。

### 一个贯穿始终的模式

C3、C4 和定价骨架是**同一个根因**：抓的是未 hydrate 的 SPA DOM。
区别只在于 FAQ / 对比表 / 定价后来有人用 JS 兜底把内容补回去了，capability-tabs 没有。

**每迁一个模块前先问：这个模块的内容到底存在吗？** 别假设它在 HTML 里。
