# GitHub Discussions

| 项 | 值 |
|----|-----|
| 自动化 | **API** — `publish-github-discussions.js` |
| 轨道 | A 技术摘要帖；B 教程讨论 |
| canonical | 无原生字段 → 文末 footer 链主站 |

## 内容规格

- 类别：`General` 或 `Ideas`（按 repo 讨论区设置）
- Markdown 正文，开发者口吻
- 文末 footer：

  ```
  Full guide: https://lovart.ai/...?utm_source=github&utm_medium=syndication&utm_campaign=offsite_{slug}
  ```

## 配置

见 `scripts/setup-github-discussions.md`

```bash
GITHUB_TOKEN=
GITHUB_DISCUSSIONS_REPO=owner/repo
GITHUB_DISCUSSION_CATEGORY=General
```

## 发布

```bash
node scripts/publish-github-discussions.js --draft drafts/github-discussions-{slug}.md --dry-run
node scripts/publish-github-discussions.js --draft drafts/github-discussions-{slug}.md
```

或纳入 `queue/dispatch-*.json` → `global[]` → `dispatch-publish.js`

## 注意

- 选与 Lovart 品牌相关的 repo（开源工具 / 文档站 / 社区镜像仓）
- 勿在无关热门 repo 刷讨论（违反社区规范）
