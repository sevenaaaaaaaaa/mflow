# Lovart.ai 404 修复包 · 2026-11-05

数据源：GSC Coverage Drilldown 导出（2026-11-05，采样 1000 / 全站 10,236）× Sanity CMS 真值逐条核对（项目 `o11tm2qe`）。
结论：**980/1000 条可 301 挽回**；13 条整族缺失需决策；7 条垃圾路径忽略。

## 文件清单

| 文件 | 用途 |
|---|---|
| `Lovart-404分类处理-2026-11-05.xlsx` | 总览 + 四语言明细（优先级/规则/301 目标/建议动作），含筛选与冻结表头 |
| `redirect-map.csv` | 全量映射：`source_url, target_url, rule, last_crawled`（主数据，其他产物由它生成） |
| `nginx-redirect-map.conf` | nginx `map $uri $redirect_target {...}` 精确映射（980 条），可直接 include |
| `cf-bulk-redirects.csv` | Cloudflare Bulk Redirects 导入格式（source, target, 301, preserve query） |

## 规则分布（1000 条）

| 规则 | 条数 | 含义 |
|---|--:|---|
| R3-幽灵语言→en | 491 | 该语言版从未发布/已删，英文原版在线 |
| R1-zh迁移 | 308 | 旧中文 URL（`zh-*`/拼音），中文版已迁移至 `/zh/` 且在线 |
| R3-幽灵语言→it | 89 | `-it` 后缀意语内容误发他语言路径，it 版在线 |
| R3-幽灵语言→zh | 65 | 仅中文版存在（中国主题内容） |
| R2-前缀错位 | 11 | 文档存在但类别前缀发错（tools↔features 等），含 6 条更名救援 |
| R3-其他(de/fr/ja/ko/zh-TW) | 15 | 同上，指向其余语言版 |
| R4-整族缺失 | 13 | 全语言无文档 → 见「第4步」决策 |
| R5-垃圾 | 7 | `/404 /image /video /月 /年 /_next/static/ /upload/*.m3u8` |

## 第 1 步 · 部署 301（CDN/边缘层）

**方式 A · nginx**（自托管/反代层）：

```nginx
include /path/to/nginx-redirect-map.conf;   # map 块需位于 http 上下文

server {
    ...
    if ($redirect_target) {
        return 301 $redirect_target;
    }
}
```

可选加速规则（与 map 等价，覆盖 R1 大头，务必放在 map 之前或用 map 优先）：

```nginx
# zh 迁移族：语言前缀换 zh，slug 保留
# ~* ^/(en|es|de|fr|ko)/(blog|topics|solutions)/(zh-.+)$  →  /zh/$2/$3
# ROOT 中文残留：/blog|topics|solutions/zh-*.html 等 → /zh/$1/$2
```

**方式 B · Cloudflare**：Dashboard → Rules → Redirect Rules → Bulk Redirects，导入 `cf-bulk-redirects.csv`（List → Bulk Redirects，注意 Bulk Redirects 需要 URL List 配额；或用动态 Redirect Rule + map 表）。 lovart.ai 的 CF 账号不在本工作区（`deploy/cf.env` 是工作台自有域名 nownexts.com，且 token 已失效），需要 lovart 基础设施侧执行。

## 第 2 步 · 站内死链改指/拔链（Sanity，本工作区可执行）

```bash
cd mflow/ops
SANITY_PROJECT=o11tm2qe SANITY_DATASET=production python3 dead_links_audit.py audit   # 已跑，报告在 run/logs/
# 服务器上（MFLOW_ALLOW_LIVE_WRITES=1 才写库，本机默认 dry-run）：
MFLOW_ALLOW_LIVE_WRITES=1 SANITY_PROJECT=o11tm2qe SANITY_DATASET=production python3 dead_links_audit.py fix --report <audit报告路径>
```

说明：audit 已于 2026-11-05 运行（报告 `run/logs/dead-links-audit-*.json`）；fix 会把正文/CTA/bodyJson 中指向这批 404 的链接改指到本包映射目标或拔链（带 `ifRevisionID` 乐观锁）。

## 第 3 步 · hreflang 清理（站点代码仓库，需lovart前端）

实测复现：在线英文文章的 `<link rel="alternate" hrefLang="ja|de|...">` 仍指向已 404 的语言版，是 Google 持续发现死链的主入口（sitemap 已于 11-04 清理完毕，本次实测线上 sitemap 与 GSC 404 零重合）。要求：hreflang 仅输出「该语言文档真实存在」的 alternate。

## 第 4 步 · R4 13 条逐条决策

见 Excel「总览与行动方案」与各明细表（P2 行）。要点：
- `/zh/features/ai-video-generat`（截断 slug）、`ai-design-handoff`×3、`ai-lip-sync-generator`×2 等 → 无对应文档：301 到最近似 section 索引页或 410
- `hedra-ai-review-...`（已删竞品内容）、`promts-for-seedance` 等 → 确认无外链后 410
- 部署 301 后这批 URL 的抓取会自然衰减

## 第 5 步 · 验证收尾

```bash
# 部署后抽查（期望 301）
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://www.lovart.ai/es/blog/zh-menu-design-restaurant
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://www.lovart.ai/ja/blog/what-is-an-ai-design-agent
```

- GSC → 页面索引 → 未找到 (404) → 对已修 URL「验证修复」
- 观察 404 曲线 2-4 周（基线 10,236 @ 10-23）
