---
session_date: 2026-10-09
session_topic: "blogs 复刻页根治：共享作用域化资产替换逐页 2.7MB 内联 payload"
session_slug: "replica-shared-assets"
profiles_used: [profile-lovart-management]
tools_used: [scope-css.py, merge-live-css.py, build-payload.py, deploy-shared.sh, audit-replicas.py, ego-browser]
agents: [cursor]
duration_min: 180
files_changed_count: 7
kb_units_added: 0
schema_bumps: 0
related_sessions: ["2026-10-07-round32-full-css", "2026-10-08-round33"]
status: ready
---

# Context
- 用户指出复刻四毛病：丢样式、配色与博客互踩、点击 bug、页面多发现不了不兼容。
- 根因实锤：每页内联 2.5MB 序列化 CSS（每页一份副本，修一处漂一处）；深色覆盖块
  `:root,.dark{...}` 无条件挂 :root 与博客主题互踩；10 个 solutions 页完全没有 JS；
  序列化 CSS 里混入博客插件样式（Elementor/HFE/WP blocks）。

# Solution
CSS/JS 收敛为共享资产（https://nownexts.com/lr-assets/，`?v=N` 版本化），
payload 从 2.7MB 内联缩到 60–267KB 引用式：
`<link css> + <div class="lr dark">SSR HTML</div> + <link 兜底注入 script> + <script js defer>`。
- `scope-css.py`（tinycss2）：`:root/html/body→.lr`、`.dark→.lr.dark`、`@layer` 递归，
  全部规则作用域化，自检零泄漏；手写解析器在 @layer 引号嵌套处失步（吞掉 343KB
  utilities 层）——必须用 tinycss2。
- `merge-live-css.py`：ego-browser 宽视口现场抓 lovart.ai CSS 补缺（prompt-to-images
  组件样式 +365 规则）；剩余 32 个"缺失"类经 DOM 实测在现网同样无样式（死类/内联
  style），复刻行为与现网一致。
- `audit-replicas.py`：REST search 轻量分类全站 585 页 → 复刻/博客分类深检（不下载
  旧页 2.7MB×N）。
- 已部署 18 个复刻页（11 首批 + 7 从线上转换），审计全 OK、博客页零泄漏。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| dev/wordpress/scope-css.py | add | tinycss2 作用域化工具 |
| dev/wordpress/merge-live-css.py | add | 现场 CSS 合并补缺 |
| dev/wordpress/build-payload.py | add | 旧 payload→新格式；--from-live 按 ID 现场转换 |
| dev/wordpress/deploy-shared.sh | add | 按 slug 查 ID 更新部署 |
| dev/wordpress/audit-replicas.py | add | 全站复刻页审计 |
| dev/wordpress/assets-src/ | add | lovart-replica.css (2.9MB) / .js (4.3KB) |
| harness/11-knowledge/sessions/ | add | 本日志 |

# Decisions Made
- D1: CSS 作用域化到 `.lr` 包裹类，深色由 `class="lr dark"` 显式控制（根治配色互踩）
- D2: 共享资产托管 nownexts.com/lr-assets/（一处修改全站生效）；路径避开 `.htaccess`
  的 `RedirectMatch 410 ^/wp-.*$`（旧 WP 路径清理规则会 410 掉 /wp-assets/）
- D3: `javascript:void(0)` 链接统一替换为 `#`——Aliyun WAF XSS 评分拦截 REST POST
  （405），且共享 JS 的 initNoJump 对两者行为一致，纯防御性替换
- D4: 共享 JS 采用 replica-homepage 已验证的 4KB IIFE 原样抽出不改写
- D5: 6 个 gpt_image_2 旧测试页（id=17633/17646/17659/17807/17874/17887）保持旧格式，
  待用户决定删除或转换

# Patterns Observed
- P1: blogs.lovart.ai 前面有 Aliyun WAF：REST POST 内容含 `javascript:` URL 计分触发
  405（阿里 CDN 错误页、zh-cn、data-spm 可识别）；出问题时先看是不是 WAF 拦截
- P2: 手写 CSS 解析器永远别信——@layer 内引号嵌套会让深度失步；用 tinycss2
- P3: 序列化 CSS 快照抓取时机敏感：组件 chunk 懒加载与否决定覆盖率；比对类覆盖率
  必须用转义形态（`.md\:px-\[32px\]`）且先 unescape HTML 实体
- P4: nownexts.com 实际由 Apache 服务（nginx 未运行），改配置要看 /www/server/panel/vhost/apache/
- P5: 站点 .htaccess 有 `RedirectMatch 410 ^/wp-.*$`——新增静态路径别用 wp- 前缀

# Open Questions
- Q1: 6 个 gpt_image_2 测试页去留？
- Q2: ego-browser 对 17k px 高动效重页截图超时（合成器卡），审计靠 computed style 替代
- Q3: 共享 CSS 里的博客插件样式（Elementor 等）是否值得清洗减重（当前 2.9MB）

# Cross-References
- entities: replica-pipeline, blogs-wordpress-site
- decisions: MEMORY-PROJECT.md § 5 (不问就干)
- skills: wordpress-design-replication

# Tags
- relevant-tags: #wordpress #replica #css-scoping #waf #shared-assets