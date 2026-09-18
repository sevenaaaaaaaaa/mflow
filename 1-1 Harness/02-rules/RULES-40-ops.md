---
type: rule
version: 2.0
updated: 2026-07-05
scope: "profile-op-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-40-ops.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 40 运维类（Ops）

> 适用路线：Sitemap 生成、IndexNow、CRO 专项、页面素材质量
> 加载 Profile：`lovart-ops`

---


## 一、硬条款（违反即 BLOCK）

1. **必须**使用 `LOVART_LOCAL_DEV_ROOT` 作为输出根目录（禁止硬编码绝对路径）
2. **禁止**写入 `.venv/` 或 `secrets/` 目录
3. **必须**所有报告含环比（禁止只出 snapshot）
4. **必须**每次真实发布记入 approvals.log
5. **禁止**绕过 dry-run 直接执行生产写入
6. **必须**每月归档终态管线条目（降噪治理）
7. **禁止**在 production 数据集上使用 --replace
8. **必须**在 import 前跑 preflight BLOCK=0
9. **禁止**修改其他 RULES 文件（harness_auto_optimize 只能在禁用词区块内追加）
10. **必须**遵守 RULES-00-iron.md 的全部全局铁律

## 二、参数表

### 机器约定

| 项 | 说明 |
|---|------|
| 输出根 | `LOVART_LOCAL_DEV_ROOT` → Output/ |
| 备份 | `LOVART_LOCAL_DEV_ROOT` → Backup/ |
| Sanity | `LOVART_LOCAL_DEV_ROOT` → Sanity/production-pulls |
| WordPress | `LOVART_LOCAL_DEV_ROOT` → WordPress/readonly-pulls |
| Git | `LOVART_LOCAL_DEV_ROOT` → Git/ |

### 定时任务

launchd 三任务：daily 08:00 / weekly 周一 07:00 / dream 02:30
定义：`1-4 Dev/automation/automation-manifest.json`

### GSC 数据量
月报 5000 词 / 周报 2000 词 / 日报 200 词
维度：query/country/page/country×query/device；有 2 天延迟
