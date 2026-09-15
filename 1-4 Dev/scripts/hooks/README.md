# Hooks — 铁律执行器

> **Why these exist**: RULES-00 写的是"禁止 `sanity deploy`" / "禁止 `--replace`" /
> "必须 BLOCK=0 才能 import" / "必须日期双写" —— 但 LLM Agent 看到的是文本规则,会
> 解释、会偷懒、会"善意绕过"。这套 hooks 把铁律变成 **exit-code 检查器**:
> 不通过 = 进程退出非 0 = Agent **物理上没法继续**。

## 三个 hook

| hook | 调用时机 | 检查的规则 | 退出码 |
|------|---------|-----------|--------|
| `pre-write-check.sh` | 写文件前 | 文件名格式 / 路径 / 必备 frontmatter / 无占位符 | 0=pass, 1=BLOCK |
| `post-write-check.sh` | 写完文件后 | H2 密度 / 词数 vs 目标 / 反 fluff / 反 AI 自介 / 无残留模板 | 0=pass, 1=BLOCK |
| `pre-import-check.sh` | Sanity import 前 | pipeline-state 在 S4-ready/S5-importing / qa BLOCK 全 0 / 日期双写 / 多语言覆盖 | 0=pass, 1=BLOCK |

## 何时调用

### pre-write-check.sh — 在 write_file / patch 之前

```bash
# 在 1-3 GenFlow/ 下写任何 .md 之前
bash 1-4\ Dev/scripts/hooks/pre-write-check.sh --file "/path/to/draft.md"
```

### post-write-check.sh — 写完一篇 Blog 后立刻

```bash
# EN Blog 标准
bash 1-4\ Dev/scripts/hooks/post-write-check.sh \
  --file "/path/to/blog-en.md" \
  --type blog \
  --lang en \
  --target-words 7500
```

### pre-import-check.sh — Sanity import 命令之前

```bash
bash 1-4\ Dev/scripts/hooks/pre-import-check.sh \
  --id "blog-firefly-2026-07" \
  --state-path "1-3 GenFlow/.pipeline/pipeline-state.json" \
  --artifact "/path/to/blog-en.md"
```

## 集成方式

### 方式 1:Agent 自调用（推荐）

在 S3 / S4 / S5 skill 的 SOP 步骤里加一句"在写完/import 前必须先跑 hook"。

### 方式 2:Hermes cron 调度

加到 `~/.hermes/profiles/content-gen-lovart/cron/preflight-hourly.sh`:

```bash
#!/usr/bin/env bash
# 每小时跑一次所有 hook 的 dry-run,产出问题清单
LOVART_HOOKS="<vault>/1-Project/Lovart MFlow/1-4 Dev/scripts/hooks"
VAULT="<vault-root>  # 即 LOVART_RESOURCE_ROOT，Obsidian MindRe 根目录"
"$LOVART_HOOKS/pre-write-check.sh" --file "$VAULT/1-3 GenFlow/.pipeline/sentinel.md"
```

### 方式 3:Git pre-commit hook (TODO)

未来可加 `.git/hooks/pre-commit` 自动跑 pre-write + post-write。

## 退出码语义

| rc | 含义 | 调用者应该 |
|----|------|-----------|
| 0 | pass | 继续 |
| 1 | BLOCK — 有错误必须修 | 修问题，重跑 |
| 2 | engine error — 参数错/文件找不到 | 修参数 |

## 验证

```bash
bash 1-1\ Harness/Skills/06-orchestrate/lovart-pipeline-state/smoketest.sh  # 39 tests
cd 1-4\ Dev/scripts/hooks/tests && bash ./smoketest_hooks.sh                    # 16 tests
```

## 已知误报（false positive）

| 误报场景 | 当前状态 | 处理 |
|---------|---------|------|
| `cutting-edge` 在标题里 | warn 不 block | 后续可用 `--strict` 强化 |
| `unlock the power` 在引语里 | warn 不 block | 同上 |
| 多语言覆盖只 check en | warn 不 block | 全量检查需查 Sanity 多语言文档，TODO |

## 不要做的事

- **不要**改 hook 的 exit code 语义（0=pass / 1=block 是契约）
- **不要**在 hook 里改文件——hook 只读不写
- **不要**绕过 hook 直接 import——这是质量保证的根，绕过 = 回到 RULES-00 之前的混乱

## 与 pipeline-state 的关系

| 流程 | hook 角色 |
|------|---------|
| S3 写稿 | `pre-write-check` → 写 → `post-write-check` → `pipeline_state advance --to S3-done` |
| S4 QA | `post-write-check` 再跑 → `pipeline_state run --qa-result` → `advance --to S4-ready` |
| S5 import | `pre-import-check`（含 pipeline-state check）→ import → `advance --to S5-published` |

`pre-import-check` 内部已经调 `pipeline_state.py check`,所以两层串接自动。
