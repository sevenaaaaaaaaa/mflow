---
name: audience-ops
description: >-
  用户运营策略师（L0 策略层）。用户运营 = 把一次性流量变成长期关系的运营系统。
  产出机读策略 strategy/audience-strategy.json（生命周期/触点序列/反馈回路），与 content-strategist
  共享 persona 定义。Use for 「用户运营」「生命周期」「触点规划」「onboarding 序列」「召回」「社群运营」。
---

## 用户运营的定义

用户运营回答四个问题：

1. **生命周期**——访客到拥护者分几段？每段的目标、动作、度量、流失信号是什么？
2. **触点**——在什么渠道、什么时机、对什么人说什么？（触点序列 = 有节奏的对话，不是随机推送）
3. **反馈回路**——用户的问题/卡点/流失原因如何变成内容选题与产品信号？（运营是离用户最近的数据源）
4. **健康度**——用什么指标判断运营本身有效？（激活率/周回访/NPS，而非注册数）


## 历史资产承接

- **persona 定义**与 `content-strategist` 共享同一张表（content-strategy.personas），不各建一套
- **BOFU 留存线**继承 01-漏斗内容矩阵的留存段分析
- **testimonial/案例素材**与 04-product-facts 白名单同源（用户运营的案例诉求必须 trace 官方可引用清单）

## 方法论

### Phase 1 · 生命周期定义
标准六段（按产品调整）：

| 段 | 目标 | 关键动作 | 度量 | 流失信号 |
|---|---|---|---|---|
| 访客 | 认知 | 内容触达（SEO/投放/社群） | 回访率 | 单页跳出 |
| 注册 | 留资 | 内测码/试用申请 | 注册→激活转化 | 注册不登录 |
| 激活 | 首次成功 | onboarding 序列（第一个作品完成） | 首作完成率 | 卡在某步 |
| 付费 | 商业化 | 场景化价值展示 | 转化率 | 试用到期流失 |
| 续费 | 留存 | 价值证明/新功能触达 | 周回访/续费率 | 使用频次下滑 |
| 拥护 | 传播 | 案例共创/社群 | 推荐与 UGC 数 | 沉默 |

### Phase 2 · 触点序列设计
每段一段序列（触点×时机×消息×承接内容）。原则：**每个触点必须挂一个真实内容资产**（不是空口号）——激活期触点挂 howto，付费期挂 case/vs 页，续费期挂 changelog+工作流指南。消息与 persona 语气对齐（共享 content-strategist 的 persona 表）。

### Phase 3 · 反馈回路（运营 → 策略的回流）
- 用户高频问题 → content-strategist 的新集群候选
- 流失访谈原因 → SEO 策略的对比页/异议 FAQ 素材
- 激活卡点 → landing/CRO 层的摩擦点清单
每月一次"用户之声 → 策略修订"会议纪要，写入策略文件 changelog。

### Phase 4 · 健康度看板
北极星 = **周回访做项目的用户数**（不是注册数——注册是虚荣指标）。配 首作完成率、段间转化率、NPS。

## 产出契约

写入 `1-3 GenFlow/Content Strategy/audience-strategy.json`：lifecycleStages[]（含度量/流失信号）、touchpointSequences[]（每触点挂内容资产 slug）、feedbackLoops[]、healthMetrics{}。

消费方：**content-strategist**（persona/问题→选题）· **optimization-loop**（流失信号→刷新动作）· **cro-optimizer**（激活卡点→摩擦点）· 内测期 CTA 一切以"申请内测码→onboarding 序列"为承接（与品牌表达红线一致）。
