# 工具聚合站批量采集来源

## ahhhhfs.com（A姐分享）

**特点**：中文工具聚合站，文章格式固定为「工具名：描述 - A姐分享」
**访问**：curl 可用（web_extract 被拦截，Cloudflare IP 被误判为内网）
**处理流程**：
1. `curl -sL --max-time 10 "URL" | grep -o "<title>[^<]*</title>"`
2. `curl -sL --max-time 10 "URL" | grep -oE "https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+"` 提取 GitHub
3. 标题格式固定，`split("：")[0]` 提取工具名
4. 批量处理 38 个 URL，每批 terminal 调用 10s 超时
5. 按 Tags 模板创建笔记，标记 `status: draft`

**常见问题**：
- web_extract 报告 "Blocked: private/internal network" → 改用 curl
- 页面内容较长 → 只用 `head -50` 取头部即可
- 星数/平台信息需要从标题推理（如 「开源」「macOS」「免费」等关键词）

## nownexts.com（芭乐派 / NowX实验室）

**特点**：用户自有的 WordPress 站点，452 篇文章
**访问方式**：
- Sitemap: `post-sitemap.xml`（最可靠）
- WP REST API: 404（可能禁用）
- wp-admin: 需用户凭据
**处理流程**：
1. `browser_console` 从 sitemap 提取全部 URL（500+ 篇）
2. 关键词筛选：ai, open-source, tool, free, github, video, image, audio, design...
3. 排除：slg, rpg, game, adult, career, sales-theory 等
4. 与 Tags 交叉对比去重
5. 用 `browser_navigate` 逐页抓取正文（JS fetch 被 CORS 拦截）
6. 创建 Tags 模板，正文「待补充」

**实战结果**（2026-06-15）：452 篇→236 篇相关→35 篇全新

## Tags 模板格式

所有工具笔记统一使用 `_template.md` 格式：
- YAML frontmatter：title, slug, date, tags, categories, summary, focus_keyword, source, author, status
- 结构化章节：这是什么 → 适合谁 → 安装 → 核心用法 → 注意事项 → 与 Lovart/LibTV 的关系 → 相关链接
- 新工具 `status: draft`，待后续深测时填充
