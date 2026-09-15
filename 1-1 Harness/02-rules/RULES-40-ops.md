---
type: rule
version: 1.0
updated: 2026-07-05
scope: "profile-op-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-40-ops.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 40 运维类（Ops）

> 适用路线：Sitemap 生成、IndexNow、CRO 专项、页面素材质量
> 加载 Profile：`lovart-ops`

---

## Sitemap 生成与 IndexNow

- IndexNow：POST 到 `api.indexnow.org`，单次上限 10,000 URL
- 英文路径 `/blog/{slug}`，中文路径 `/zh/blog/{slug}`
- Cron：`lovart-indexnow-daily` 09:00 (全量)
- Cron：`lovart-sitemap-weekly` 周一 02:00

## 国内搜索引擎爬虫

- Cron：`lovart-china-crawler-trigger` 09:30
- 4 引擎 UA 模拟：百度/360/搜狗/神马
- shift 轮转 13 天覆盖，delay 2.5s
- **Bytespider 被 Cloudflare 拦截 HTTP 403**（即使 robots.txt Allow）→ 跳过，IndexNow 已覆盖
- **XML-RPC ping 全部死亡**：百度 500/搜狗 404/神马超时 → 不要建议使用

## CRO 专项

- CRO 优先扩量，竞品对比客观公正
- 多语言必须翻译 body（禁 EN 壳子）
- 小批验证再扩量
- 审计优先验证正确性（"担心的不是同一张图，而是是否用了我给的图片"）
- icon URL 残留必须 = 0

## 页面素材质量

### 图片 7 分类语义池
| 分类 | 用途 | 关键字 |
|------|------|--------|
| video | 视频生成相关 | storyboard, Seedance, Veo, Kling |
| avatar | 角色/IP/虚拟人 | avatar, presenter, 角色 |
| image_gen | 文生图相关 | text to image, Flux, nano banana |
| design | 设计/风格参考 | style reference, brand consistency |
| edit | 编辑/排版 | text edit, typography |
| ecommerce | 电商/广告 | facebook ad, mockup |
| generic | 通用/批量 | batch, chatcanvas, agent |

### 图片审计
- 每次批次后跑 `audit-blog-covers` + `audit-composite-images-404`
- 精确 URL 匹配（禁止 strip .png 模糊匹配 → AB-I01）
- 装饰图 bg-line 不作 composite 替换图（AB-I02）
- 同页 sibling 图片优先替换（AB-I06）
- 新稿封面只用 blog-cover-pool.js 已验证 200 URL（AB-I08）

### 落地页 SEO 体检维度（7 大维度）
BAD_TEMPLATE / TITLE_LENGTH / SLUG_MISMATCH / H1_TITLE_MISMATCH / DESCRIPTION_LENGTH / TEMPLATE_LANGUAGE / DUPLICATE_TITLE

### 内链规则（6 类）
- 站内链接仅 `/blog/{slug}`、`/features/{slug}`、`/tools/{slug}`
- 禁止 `/博客文章/`、`/cluster/`、`.md)`、`#` 占位
- preflight `MD_LINK` BLOCK

## 收录指标口径

- 主收录率：有搜索曝光 URL / 语料库 20,000（≈46%）
- 禁止 `len(pages@1000) / sitemap_submitted`（固定 ~1.43%）
- 辅指标：`sitemap_indexed / sitemap_submitted`（仅脚注）
