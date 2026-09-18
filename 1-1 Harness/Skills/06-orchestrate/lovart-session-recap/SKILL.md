---
description: 会话回顾 skill。从最近会话日志提取关键决策、教训与后续待办，输出结构化回顾摘要。触发：用户要会话回顾、session recap、上次做了什么。
---

# lovart-session-recap — 会话回顾

## 流程

1. 读取 `11-knowledge/sessions/` 最近 N 篇会话日志（默认 5 篇）
2. 从每篇提取：交付物 / 关键决策 / 踩坑教训 / 待办
3. 汇总输出结构化回顾

## 输出格式

```
## 交付物
- [日期] xxx（状态）

## 关键决策
- [日期] 决策内容

## 踩坑
- 问题 → 解法

## 待办
- [ ] 待办项
```

## 触发

"回顾最近会话"、"session recap"、"这周做了什么"

## 路径

会话日志：`1-1 Harness/11-knowledge/sessions/*.md`
项目记忆：`11-knowledge/MEMORY-PROJECT.md`

## 预算

输出 ≤500 字（RULES-70），只提取关键信息不展开。


- 必须过质量门禁（post-write-check + geo-check + quota-check + lang-check）。


- 禁止绕过质量门禁直接发布。禁止删除 production 文档。
