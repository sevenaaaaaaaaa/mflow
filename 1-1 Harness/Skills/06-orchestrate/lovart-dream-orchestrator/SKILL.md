---
name: lovart-dream-orchestrator
description: |
  Lovart 梦境编排 skill — 手动触发 / 监控系统整理（consolidation + audit）。
  触发：用户说"今晚先梦境跑一遍"、"新人入项，先 audit"、"换工具配置了，先看一致"、
  "上次 audit 出的错误修完了，再跑一次确认"、"换季度，需要刷 MEMORY-PROJECT.md"。
---

# lovart-dream-orchestrator

> 让"系统记账"流程可技能化触发。SSOT 在 `1-1 Harness/11-knowledge/dream/`。
> 工作线：`lovart-management`。

---

## When this skill loads

加载条件：

- 字符串触发："今晚梦境"、"先 audit"、"dream 一下"、"刷一下 memory"、"知识图同步"、"梦境跑过吗"
- 工作线触发：用户在 `lovart-management` Profile
- 阶段触发：用户做改动涉及跨文件（entities.yaml/relationships.yaml/AGENTS.md/CLAUDE.md 等）

不加载：单次问答、不修改代码、不变更配置。

---

## Process (3 阶段，按用户指令选)

### 默认 = 全跑（最常用）

```
bash 1-1 Harness/11-knowledge/dream/consolidate.sh
```

### 仅 emit（仅 regenerate JSONL）

```
bash 1-1 Harness/11-knowledge/dream/consolidate.sh --emit-only
# 等价于
bash 1-1\ Harness/11-knowledge/scripts/kg emit
```

### 仅 audit（不动 MEMORY-PROJECT.md）

```
bash 1-1 Harness/11-knowledge/dream/audit.sh --no-write-today
```

### 仅单维度 audit

```
bash 1-1 Harness/11-knowledge/dream/audit.sh --no-write-today A3
```

可选：`A1 A2 A3 A4 A5 A6`（参见 `audit/README.md`）。

### 仅强制 audit（写当日报告）

```
bash 1-1 Harness/11-knowledge/dream/audit.sh
```

---

## Output format

汇报：

- "consolidate ran N entities / M relationships; JSONL refreshed; audit 发现 A3 ERROR ×5 / A2 WARN ×1"
- 给出最近报告路径：`audit/reports/audit-report-{TODAY}.md`
- 给出 actions（"应手动改：AGENTS.md / CLAUDE.md / opencode.jsonc / Hermes MEMORY.md 全部加 11-knowledge 引用"）

如果用户问"哪些 entry-point 文件需要加 11-knowledge 引用"，直接读 audit 报告 → 列出具体路径。

---

## Hard rules

1. **梦境不自动改 entry 文件**；它只标记、不写。这条边界在 `dream/README.md` 已明示。
2. **审计失败 (rc=1)** 必须明确告诉用户 — 这是 cron 通知级别，不是能静默的。
3. **emit-only 路径不能替代 audit**；前者只刷新数据，后者检查孤立点 / 引用缺失 / 一致性。
4. **不要把 SSH/sanity/外部脚本**混入梦境 — 它是文件系统 + 元数据 + JSON 操作。
5. **如果用户问"插件干预梦境怎么办"** → 答："梦境是 launchd / 手动 + skill 三入口；可启可停；不要混到 cron 之内。"

---

## Failure modes (NEVER)

- 把 audit 当"全跑"的同义词 (audit 是子步骤)
- "反正最后总是写一堆报告，所以默认写报告"
- "auto-fix 错误" — 由用户决定

---

## Reference

- 梦境：`1-1 Harness/11-knowledge/dream/consolidate.sh` + `audit.sh`
- 梦境说明：`1-1 Harness/11-knowledge/dream/README.md`
- 同步：`1-1 Harness/11-knowledge/scripts/kg` (emit/query)
- launchd 配置：`1-1 Harness/11-knowledge/dream/lovart.dream.plist`（复制到 `~/Library/LaunchAgents/com.lovart.dream.plist` 后 load）
