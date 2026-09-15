# 海外平台栈（精简版）

| 平台 | 档位 | 工具 | 凭证 |
|------|------|------|------|
| **DEV.to** | API 自动 | `publish-devto.js` | `DEVTO_API_KEY` |
| **GitHub Discussions** | API 自动 | `publish-github-discussions.js` | `GITHUB_TOKEN` + repo |
| **Google Blogger** | API 自动 | `publish-blogger.js` | OAuth — `setup-blogger.md` |
| **Medium** | 爱贝壳手动 | 扩展草稿箱 | 浏览器登录 |
| **X** | 爱贝壳手动 | 扩展草稿箱 | 浏览器登录 |

已移除主栈：Hashnode、LinkedIn MCP、content-distribution-mcp。

## 配置速查

```bash
# DEV.to — 已有
DEVTO_API_KEY=

# GitHub — scripts/setup-github-discussions.md
GITHUB_TOKEN=
GITHUB_DISCUSSIONS_REPO=owner/repo

# Blogger — scripts/setup-blogger.md
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REFRESH_TOKEN=
BLOGGER_BLOG_ID=
```

## 分发

```bash
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --dry-run
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --global-only
```
