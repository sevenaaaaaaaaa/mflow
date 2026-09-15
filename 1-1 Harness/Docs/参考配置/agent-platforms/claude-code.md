# Claude Code

> Anthropic Claude Code：以 **CLAUDE.md** 为项目记忆，**无内置 cron**；定时任务仍用 Cursor Automations 或 shell cron。

## 工作目录

```bash
cd "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project"
claude   # 或 Claude Code IDE 打开该文件夹
```

## CLAUDE.md（建议放在 `1-Project/CLAUDE.md`）

```markdown
# Lovart — Claude Code

## 规则
- 读 `1-1 Harness/AGENTS.md` 与 `1-1 GEO Readme/AGENTS.md`
- Sanity：仅 `import --missing`；禁止 deploy / --replace / 删 production

## 常用命令
- Tools pull: `bash "1-4 Dev/automation/tools-pull/pull-tools-from-production.sh"`
- Health: `bash "1-4 Dev/automation/content-health/weekly-health-check.sh"`
- SEO weekly: `python3 "1-4 Dev/scripts/weekly_review_v3.py"`

## 路径
- Studio scripts: `1-4 Dev/lovart.sanity.studio/scripts/`
- Tools SSOT: `1-3 Content Gen/Page Gen/Pages/Tools/`
```

## settings（可选）

`1-Project/.claude/settings.json` 示例：

```json
{
  "permissions": {
    "allow": [
      "Bash(bash 1-4 Dev/automation/*)",
      "Bash(node scripts/*)",
      "Bash(python3 1-4 Dev/scripts/*)"
    ]
  }
}
```

（字段以 Claude Code 当前版本文档为准，按需调整。）

## 与 Cursor 分工

| 场景 | 用谁 |
|------|------|
| 每周无人值守 pull + 摘要 | **Cursor Automations** |
| 大段 Sanity 文案 / 多文件 refactor | **Claude Code** 交互 |

## 凭证

`ANTHROPIC_API_KEY` in `~/.zshrc`；Sanity token 同 Cursor。
