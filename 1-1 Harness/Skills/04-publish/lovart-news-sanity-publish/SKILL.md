---
description: 将本地 News 页面 JSON（composite-v2，category news）安全同步到 Sanity production。
---

# lovart-news-sanity-publish

> 将本地 News 页面 JSON 安全同步到 Sanity production。用于 News 发布、sync、页面上线。

## 流程

1. 从内容库 `run/library/lovart-global/news/` 读取目标页面
2. 验证 composite-v2 结构（pageType=news）
3. --dry-run 确认 → --missing 增量导入
4. preflight BLOCK=0
5. 记入 approvals.log

## 安全边界

- 禁止全量 import（必须 --missing）
- 禁止修改 Sanity schema
- 禁止删除 production 文档
- 发布永远停在人工授权


## 预算（RULES-70 强制）

本 skill 产出同样受 RULES-70 数量预算约束。


## 触发

用户提到 news sanity publish、sync、上线。
