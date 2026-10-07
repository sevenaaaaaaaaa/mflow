---
type: session-log
session_date: 2026-09-17
session_slug: landing-loop-p18
status: ready
---

# Session Log — Phase 18 落地页闭环（改稿 → 发布）

## 交付
1. **`landing_refresh` 执行器**：读 Sanity 现有页面（bodyJson→文本）→ 按落地页结构重写（H1 + 3-4 非问句 H2 含数据点 + FAQ + CTA）→ 四门禁 + composite 结构校验 → **内部重试 ≤3 轮（带门禁/结构反馈）** → 落盘
2. **通用任务链** `chain_next_task`：父任务完成后按 `params.chain` 生成下一步（publish_sanity）；**只链通过门禁与结构校验的产出**；链式发布默认 dry-run；审计 `CHAIN-CREATE` / `CHAIN-SKIP`
3. **预设 #8「🔁 落地页闭环（改稿→发布）」**：section/lang/条数 → landing_refresh（chain=publish_sanity patch）
4. **两处修复**：
   - `publish_sanity` 失败不再"假 done"（抛错 → 条目 failed）
   - 链式 patch 用真实 Sanity `_id`（库内 `sanity_id` 是 UUID，slug≠_id）
5. 单测：+2（链只链通过项 / 预设存在且链默认 dry-run）→ 共 **28 用例**，GATE 6 通过

## 实测（线上，dry-run）
```
landing_refresh 1 项 → ready=True（四门禁 + 结构校验全过）
  → 自动链出 publish_sanity（patch 模式）
  → patch dry-run tx=NngiCiCmzwd6fOe1vYPa7V（对真实 UUID 文档）
```
不合格项：`CHAIN-SKIP`（审计），不进入发布链。

## 闭环暴露并修掉的两个环境 bug（重要）
1. **新钩子用系统 `python3`（py3.6）**：打印非 ASCII（em dash 等）直接崩 → `lang-check.sh` 恒挂 → 所有英文稿都被拦。
   修：quota-check/lang-check 走 `LOVART_PYTHON` → 项目 venv，并加 `sys.stdout.reconfigure(utf-8)` 兜底。
   教训：**新写 bash 钩子的 python 调用必须走 LOVART_PYTHON 链**（这是第三次同类问题）。
2. **校验口径不一致**：`validate_sections` 用原始字符数（英文 3000+ 必超 1200）而 quota-check 用词当量 → 永远打回。
   修：统一为**词当量**（CJK 字符 + 拉丁词 ×1.5）。

## 意义
"内容更新"现在是一条可收敛的自动链路：**存量落地页 → 改稿（自愈重试）→ 门禁+结构校验 → 只发布合格项 → 人工确认真实上线**。
下一步真实放量时，只需把预设的 dry-run 关掉并勾选确认公开可见。
