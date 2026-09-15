---
type: query-cookbook
version: 1.0
---

# Queries · 知识图常用查询

Quick answers to common questions an agent hits when working on Lovart MFlow.
Each recipe is a single bash/python invocation; results are plain text.

## 我是哪一条工作线的？哪些 skill 归我？

```bash
kg list --kind profile
kg related-to profile-lovart-reports --direction out | grep "uses"
```

## 改 X skill 之前搞清楚：(a) 谁在调用 (b) 谁的反向依赖是 supersede (c) 跨工具副本在哪儿

```bash
USE=$(kg related-to $SKILL_ID --direction in)
SUPER=$(kg start $SKILL_ID --hop 1 --type supersedes)
MIRR=$(kg related-to $SKILL_ID --direction out --type mirrors)
```

## 哪个 cron 在跑哪个 Profile？

```bash
kg list --kind cron
kg start <cron-id> --hop 1 --type runs_on
```

## 看 Hermes memory diff（这次会话记住了什么新东西）

```
# sleep-time 之后
diff ~/.hermes/memories/MEMORY.md "1-1 Harness/11-knowledge/MEMORY-PROJECT.md"
```

> 通常会出现两类 diff：项目专属事实（应跟随 MEMORY-PROJECT.md）和用户偏好（应跟随 USER.md）。

## 想看「我这么做有没有违反 RULES-00」的对应文件

```bash
# 列出必需规则
kg list --kind rule | head -10
# 专门查铁律
kg id rule-iron

# 看一个 Profile 加载哪些规则
kg related-to profile-lovart-quality --direction out --type requires
```

## 谁在我下一个会话之前会被这个改动影响？

```bash
kg start <changed-id> --hop 3  # 全域 3 跳
# 或限定
kg start <changed-id> --hop 3 --type requires
```

## 加新 skill / Profile / Cron 之后的必要动作清单

1. 编辑 `entities.yaml`（加 entity）
2. 编辑 `relationships.yaml`（加边：from 该 entity → to Profile/Rule/Skill 等）
3. `bash 1-1 Harness/11-knowledge/scripts/kg emit`
4. `bash 1-1 Harness/11-knowledge/dream/audit.sh --no-write-today`
5. 看 audit 报告（如有 ERROR，按建议修）
6. 触发 dream：`bash 1-1 Harness/11-knowledge/dream/consolidate.sh`

（不需要修改 `tree.yaml` —— 它是 derived 视图。）

## "5 个工具各自都在哪些 Profile 里活跃？"

```bash
KG_ID=tool-XXX
kg related-to $KG_ID --direction out --type runs_on
kg related-to $KG_ID --direction out --type owns
kg related-to $KG_ID --direction out --type bootstraps
```
