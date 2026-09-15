# OpenAI Codex

> Codex CLI / IDE 插件：以 **AGENTS.md** 为项目指令，适合 **cron / CI 单次 exec**，无内置 weekly scheduler。

## 工作目录

```bash
export LOVART_ROOT="/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault"
cd "$LOVART_ROOT/1-Project"
```

## 项目指令文件

在 **`1-Project/AGENTS.md`** 或 vault 根 **`AGENTS.md`** 中引用（若 Codex 从 vault 根打开，链到 Harness）：

```markdown
# Lovart Codex

- Rules: 1-Project/1-1 Harness/AGENTS.md
- Sanity pipeline: 1-Project/1-4 Dev/.cursor/rules/lovart-sanity-content-pipeline.mdc
- Weekly Tools pull: bash 1-4 Dev/automation/tools-pull/pull-tools-from-production.sh
- Never: sanity deploy, import --replace, delete production docs
```

## 定时（替代 launchd）

**macOS cron**（示例：周一 08:00 Tools pull，仅 shell、无 Agent 费）：

```cron
0 8 * * 1 cd "/Users/seveno/.../LifeOS Pro PARA Vault/1-Project" && bash "1-4 Dev/automation/tools-pull/pull-tools-from-production.sh" >> ~/Library/Logs/Lovart/codex-cron-tools-pull.log 2>&1
```

**Codex exec 单次**（需本机 API key）：

```bash
cd "$LOVART_ROOT/1-Project"
codex exec "Run bash 1-4 Dev/automation/tools-pull/pull-tools-from-production.sh and summarize pull-tools-latest.json"
```

（具体子命令以你安装的 Codex CLI 版本为准；无 `codex exec` 时直接用 bash。）

## Skills

Codex 不读 Cursor `SKILL.md` 路径；把关键 SOP 复制到 `AGENTS.md` 或 `@` 引用：

- `1-1 Harness/Skills/lovart-tools-sanity-publish/SOP-Lovart-Tools-Sanity-发布统合指南.md`

## 凭证

与全项目相同：`SANITY_API_TOKEN`、`OPENAI_API_KEY` 在 shell profile；Codex 继承终端环境。
