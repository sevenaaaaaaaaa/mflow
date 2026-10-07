---
title: "Portfolio Audit：143 位设计主管教你审作品集"
slug: portfolio-audit-design-skill
date: 2026-05-24
updated: 2026-05-29
tags: [作品集, 设计, 招聘, AI, portfolio-audit]
categories: [设计工具]
summary: Portfolio Audit 基于 Dive Club 143 期设计主管访谈提炼 8 维评分标准，一行命令用 headless 浏览器审计作品集网站。适合求职设计师，不应当作唯一教条。
focus_keyword: Portfolio Audit
source: https://github.com/hey-stefan/portfolio-audit
author: hey-stefan
status: draft
---

# Portfolio Audit：143 位设计主管教你审作品集

> 8 维度 × 5 分制 | 总分 40 | 数据来自真实访谈

## 这是什么

[Portfolio Audit](https://github.com/hey-stefan/portfolio-audit) 不是泛泛 AI 点评——**评分体系来自 [Dive Club](https://www.dive.club) 143 期设计主管访谈**（Figma、Stripe、Airbnb、Linear、Anthropic 等）关于作品集与招聘的逐字稿提炼。

> 不是「我觉得好的设计」——而是「这些人说过他们看重什么」。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 求职/UI/UX 设计师改作品集 | ✅ 推荐 | 可操作优先级列表 |
| 设计学生第一次做站点 | ✅ 推荐 | 10 秒直觉检查等维度清晰 |
| 非设计岗代码作品集 | ⚠️ 部分适用 | Builder 信号等维度仍有用 |
| 把分数当唯一标准 | ❌ 警惕 | 独特性本身是评分项 |

## 安装与前置条件

AI Agent Skill，支持 Claude Code、Codex、Cursor、OpenCode：

```bash
npx skills add hey-stefan/portfolio-audit
```

OpenCode 手动：

```bash
git clone https://github.com/hey-stefan/portfolio-audit.git \
  ~/.config/opencode/skills/portfolio-audit
```

使用：

```
/portfolio-audit https://你的作品集网址.com
```

全程本地：headless 打开站 → 截图首页与内页 → 提取文字链接 → 出报告。**数据不离开本机。**

## 核心用法

### 8 个维度

| 维度 | 权重 | 核心问题 |
|------|------|----------|
| 10 秒直觉检查 | **关键** | 排版、间距、配色、节奏 |
| 作品优先于文字 | **高** | 首页是否看到实际设计 |
| 严苛筛选 | **高** | 项目数是否拖后腿 |
| 故事讲述 | 中 | 文字是否有效叙事 |
| 野心与项目范围 | **高** | 是否感到「不计代价的用心」 |
| 灵魂与独特性 | 中 | 模板感 vs 个人风格 |
| 作品集即产品 | 中 | 导航、加载、信息架构 |
| Builder 信号 | 中 | 自研代码/原型/产品 |

**1** = 不及格，**3** = 及格，**5** = 卓越。

### 关键规则摘要

- **craft > process**：视觉工艺压倒一切；复杂流程留到面试聊。  
- **指标可有可无**：数字常不可信，能说清意义更重要。  
- **不罚「缺失公司项目」**：NDA 等合理原因不扣分。  
- **克制可以是风格**：极简若有自觉决策，可高分。

### 输出示例结构

```
# Portfolio Audit: example.com
## Overall Impression
## Scores（Overall: 32/40）
## What's Working
## What Needs Work
## Priority Fixes (Do These First)
## The Hiring Manager Gut Check
```

建议具体到「H1 与 H2 只差 4px」级观察，非空话。

## 注意事项与风险

- **趋同风险**：人人按同一标准优化可能模板化；评分明确 **cookie-cutter Framer 模板扣分**。  
- **作品集是个人表达**，不是考试答案。  
- **浏览器环境**：极复杂动效站可能截图不全。  
- **英文语料**：访谈以英文行业为主，国内平台作品需自行对照。

## 与你现有工具的关系

- 安装到与 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 相同的 opencode skills 目录。  
- 设计产出可用 [[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] 统一视觉后再审。

## FAQ

### Q: 没有设计背景能用吗？
A: 可以读报告学招聘视角；改稿仍建议设计师判断。

### Q: 会把我网址发到云端吗？
A: 仓库说明为本地运行；以你安装的 skill 版本为准。

### Q: 和 ChatGPT「_critique my portfolio_」区别？
A: 固定 8 维与 143 期访谈锚点，输出格式统一可对比。

## 相关链接

- GitHub：https://github.com/hey-stefan/portfolio-audit  
- Dive Club：https://www.dive.club
