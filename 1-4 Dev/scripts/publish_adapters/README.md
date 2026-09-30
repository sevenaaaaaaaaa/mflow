# CMS 发布适配器（Phase 2）

接口约定：每个适配器实现 `publish(item, cfg) -> {"ok": bool, "url": str, "cms_id": str, "error": str}`。
item 字段：id / title / body_md / lang / meta(dict)。成功后调用方把返回的 url 追加到
`1-3 GenFlow/Content Distribution/queue/published.json`，外链 CSV 导出即自动带上。

**铁律**：适配器只被"人工授权后"的流程调用；工作台 UI 不提供一键外发。

## 内置
- `webhook.py` —— 通用 Webhook（POST item JSON 到你配置的 URL，返回体含 url 即成功）。零依赖可用。
- `wordpress.py` —— WP REST `POST /wp-json/wp/v2/posts`（Application Passwords 认证）。需 `requests`。
- `sanity_reference.md` —— Sanity 增量发布的参考实现说明（NDJSON + --missing + preflight BLOCK=0）。

## CLI 用法
```bash
python3 cli.py --adapter webhook --item-id my-post --title "标题" --body-file draft.md \
  --cfg run/cms.json
```
cfg 示例（run/cms.json，git-ignore）：
```json
{"webhook": {"url": "https://your-backend/publish"},
 "wordpress": {"base": "https://blog.example.com", "user": "bot", "app_password": "xxxx"}}
```

## 内容契约层（2026-09-30，对齐 Composite 手册 + Blog PRD）

- `section_registry.py` —— composite-v2 section 注册表（34 型）+ 逐型字段 schema 校验。
  BLOCK 拦：未注册 type（前端渲染为空）、legacy 旧 8 型、faq `[[q,a]]` 数对、pricing `plans`、
  icon 越白名单、非绝对图片 URL；WARN 提示：alt 缺省、canvas-wall <10 条、缺 src 留白等。
  发布链 `validate_sections()` 已默认接入；`MFLOW_SKIP_REGISTRY=1` 应急跳过。
  独立命令行：`python3 section_registry.py sections.json`（exit 1 = 有 BLOCK）。
- `storylines.py` —— 故事线 SSOT 加载（`1-3 GenFlow/Page Gen/Refresh-Page/` 的 3 份 JSON +
  STORYLINES.md 表格）+ 顺序校验。**族内变体可替换**（bento-2→bento-6），跨族错位 BLOCK。
  已接入 `publish_landing`：known 故事线错位拦发布；未注册故事线降级 warning；`T-long` 无固定序列跳过。
- `scheduled_flip.py` —— 定时发布翻转：blog `status=="scheduled"` 且 `publishedAt<=now()` → patch 为
  `published`（ifRevisionID）。默认 dry-run，`--yes` 真实执行；建议 cron 每 10 分钟。
- **文档 _id =（type, slug, language）**：blog → `blog-{slug}-{lang}`、compositePage →
  `{page_type}-{slug}-{lang}`。patch/create 定位一律按（slug, language）GROQ 查询，旧 _id 文档可继续 patch。
  `MFLOW_LEGACY_DOC_ID=1` 临时回退旧行为。
- **blog 三时间 + status**（PRD C3/§1.3）：`publishedAt`（frontmatter `published`）/ `displayedAt`
  （frontmatter `date`，缺省回落 publishedAt）；status 五态 draft/scheduled/published/unpublished/archived
  （CLI `--status`，非法值回落 draft）；`noIndex`（frontmatter `no_index`）。
  blog publish `--mode patch` 按（slug,language）定位更新（`create` 遇同键已存在会拒绝并提示，
  不再静默跳过）。
- MD→PT：独立行图片不再降级为 `[Image: alt]` 文本，保留为 PT image block（`src`/`alt`）；
  行内图片降级为链接（embed→链接 降级规则）。`library/pt_to_md.py` 镜像同步提取图片 URL。

