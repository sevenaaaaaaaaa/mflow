# Google Blogger

| 项 | 值 |
|----|-----|
| 自动化 | **API** — `publish-blogger.js` |
| 轨道 | A 摘要帖 |
| canonical | 无原生字段 → 文末 footer 链主站 |
| API | Blogger API v3 + OAuth2 |

## 内容规格

- 标题：不同于主站
- 长度：摘要轨 ≤ 主站 40%
- 文末含 UTM 主站链接
- HTML 由脚本从 Markdown 转换

## 配置

见 `scripts/setup-blogger.md`

```bash
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REFRESH_TOKEN=
BLOGGER_BLOG_ID=
```

## 发布

```bash
node scripts/publish-blogger.js --draft drafts/blogger-{slug}.md --dry-run
node scripts/publish-blogger.js --draft drafts/blogger-{slug}.md
```

纳入 `queue/dispatch-*.json` → `global[]`：

```json
{ "platform": "blogger", "draft": "drafts/blogger-{slug}.md" }
```

## 注意

- `blogspot.com` 子域对 Google 索引友好，但权重仍低于主站
- 与主站间隔 ≥7 天再发摘要
