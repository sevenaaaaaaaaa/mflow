# 内容质量治理 — Anti-Slop 机制栈

> 从原则到上线后复盘的完整链路。按创作生命周期使用。

## 文档地图

| 阶段 | 文档 | 作用 |
|---|---|---|
| 原则 | [Anti-Slop.md](./Anti-Slop.md) | 什么是 AI slop、好内容标准 |
| 评分 | [Content-Quality-Rubric.md](./Content-Quality-Rubric.md) | 100 分 Rubric + BLOCK |
| 生成中 | [Content-Production-Ledger.md](./Content-Production-Ledger.md) | H2/section 台账、防缩水 |
| 发布前 | [Preflight-Anti-Slop-Gates.md](./Preflight-Anti-Slop-Gates.md) | 自动门禁 `AS_*` 错误码 |
| 锚定 | [Content-Sample-Library.md](./Content-Sample-Library.md) | 好稿/坏稿标注样本 |
| 上线后 | [Content-Feedback-Loop.md](./Content-Feedback-Loop.md) | GSC/舆情 → 改写与阈值回流 |

## 生命周期

```text
SERP brief
  → Ledger + Sample pair
  → 撰写
  → anti-slop-preflight + preflight-content
  → Rubric
  → 发布 → register.json
  → 月度 feedback-loop evaluate
  → 样本 / 规则 / Ledger 更新
```

## 脚本入口

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"

node sample-library-cli.js pair blog
node anti-slop-preflight.js --file draft.md --strict
node feedback-loop-cli.js evaluate
```
