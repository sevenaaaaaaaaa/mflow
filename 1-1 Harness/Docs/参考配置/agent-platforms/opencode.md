# OpenCode

> OpenCode 通过 **`~/.config/opencode/opencode.jsonc`** + **Skills 目录** 加载能力；与 vault 通过 `sync-skills.sh` 同步。

## 路径

| 项 | 路径 |
|----|------|
| 配置 | `~/.config/opencode/opencode.jsonc` |
| Skills | `~/.config/opencode/skills/`（软链到 vault `skills/`） |
| Harness Skills 实体 | `1-Project/1-1 Harness/Skills/` |
| 同步脚本 | `1-Project/1-1 Harness/Skills/sync-skills.sh` |

## opencode.jsonc 模板

保存到 `~/.config/opencode/opencode.jsonc`（按你本机 OpenCode 版本合并字段）：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-1 Harness/AGENTS.md",
    "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-1 GEO Readme/AGENTS.md"
  ],
  "skills": {
    "paths": [
      "~/.config/opencode/skills"
    ]
  },
  "mcp": {
    // 按需：Sanity MCP、Notion 等与 Cursor 相同 server 名需在 OpenCode 单独配置
  }
}
```

## Skills 同步

```bash
cd "/Users/seveno/.../1-Project/1-1 Harness/Skills"
bash sync-skills.sh              # opencode → vault
bash sync-skills.sh --to-opencode  # vault → opencode（覆盖原始 vault skills）
```

OpenCode 侧分组：`00-core`、`10-lark`、`20-hermes`、`30-clawx`。

## Lovart 相关 Skill 入口

| 任务 | Skill 目录 |
|------|------------|
| Tools 发布 | `lovart-tools-sanity-publish/` |
| Blog 发布 | `lovart-sanity-publish/` |
| Pipeline | `lovart-pipeline-orchestrator/` |
| Trident | `lovart-trident-data-engine/` |

## 定时任务

OpenCode **无** Cron Automations → 用 **Cursor Automations** 或 launchd/cron 跑 shell，OpenCode 只做 **import / 翻译 / 交互发布**。

## 工作目录

```bash
cd "/Users/seveno/.../1-Project/1-4 Dev/lovart.sanity.studio"
# 或 sanity-studio-copies/LovartPM-sanity-studio（若你 cwd 在那）
```

## 触发词（见 10-automation README 副本）

- 「Sanity push」/「同步 Blog 到 Sanity」
- 「preflight」/「发布前验证」
- 「运行完整 pipeline」
