# GitHub Discussions 配置

## 1. 选仓库

- 用 Lovart 相关仓库（文档站 / 开源工具 / 社区镜像）
- **Settings → General → Features → Discussions** 勾选开启

## 2. 创建 Token

[GitHub → Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)

**Fine-grained token**（推荐）：

- Repository access：选目标 repo
- Permissions：`Discussions` = Read and write，`Metadata` = Read

或 **Classic token**：勾选 `repo`（私有仓）或 `public_repo`（公开仓）

## 3. 写入 `.env`

```bash
GITHUB_TOKEN=ghp_...
GITHUB_DISCUSSIONS_REPO=your-org/your-repo
GITHUB_DISCUSSION_CATEGORY=General
```

## 4. 验证

```bash
node scripts/publish-github-discussions.js --list-categories
node scripts/publish-github-discussions.js --draft drafts/github-discussions-ai-logo-design-guide.md --dry-run
```

## 5. 真发

```bash
node scripts/publish-github-discussions.js --draft drafts/github-discussions-{slug}.md
```
