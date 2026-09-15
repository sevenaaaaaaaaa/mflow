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
