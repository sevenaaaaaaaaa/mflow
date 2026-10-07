---
type: session-log
session_date: 2026-09-18
session_slug: three-modes
status: ready
---

# Session Log — 三模式工作体系（Pipeline / Flow / Loop）

## 设计

三种模式和谐共存，代表系统的自动化成熟度演进：

| 模式 | 自动化程度 | 适用场景 | 当前实现 |
|------|:---:|------|---------|
| **Pipeline** | 手动 | 用户自主操作空间 | 状态机 + 管线页 + 发布通道 |
| **Flow** | 半自动 | 预设+skills 自动流转，关键点人工授权 | 8 预设 + 批量执行器 + Agent + 链式发布 |
| **Loop** | 自治 | 周而复始自我运转/进化 | 自动排程 + GEO 探测 + 自我进化 |

## 交付
1. **`mode_report()`**：三模式状态报告（当前模式/升级判断/各模式任务数/能力清单）
2. **`mode_switch()`**：项目级模式切换（pipeline→flow→loop），记 approvals.log
3. **Flow→Loop 升级判断**：近 5 次运行 pass_rate ≥80% → 建议升级 Loop
4. **总览页模式选择器**：badge 显示当前模式 + 下拉切换 + 升级提示 + 任务计数
5. **API**：`GET /api/mode` · `POST /api/mode/switch` · `GET /api/mode/promote`

## 生命周期
```
Pipeline（手动）→ 用户在管线里发现/推动/发布
  ↓ 跑通预设后
Flow（自动）→ 预设自动展开/执行/发布（用户只管授权）
  ↓ 最近 5 次通过率 ≥80% 且零熔断
Loop（自治）→ 每日 GEO 探测 → 缺口自动选题 → 自动排程 → 生成→门禁→发布
  → QA 数据回流 → 自我进化（高频 BLOCK → gen_prompt 禁例）
```

## 实测
pipeline → flow → loop → pipeline 全部切换成功 ✅
