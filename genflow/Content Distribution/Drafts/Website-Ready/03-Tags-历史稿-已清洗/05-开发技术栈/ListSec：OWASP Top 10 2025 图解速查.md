---

title: "ListSec：OWASP Top 10 2025 图解速查"
slug: listsec-owasp-top10-2025
date: 2026-06-01
updated: 2026-05-29
tags: [ListSec, OWASP, Web安全, 渗透测试, 安全基线]
categories: [安全]
summary: 公众号 ListSec 凉城发布的 OWASP Top 10:2025 图解长图（image_detail），梳理访问控制、供应链失效等十大 Web 风险及与 2021 版差异；微信正文未抓取，内容据官方中文版整理，适合开发与安服建立应用安全基线。
focus_keyword: OWASP Top 10 2025
status: draft

---

# ListSec：OWASP Top 10 2025 图解速查

> 安全公众号 ListSec | OWASP Top 10 第八版（2025）| 长图/图解类推送（image_detail）

## 这是什么

[ListSec](https://wechat.doonsec.com/wechat_echarts/?biz=MzIwMjUyNDM0OA==)（凉城）是面向**渗透测试、红蓝对抗、应急响应**的学习类公众号（简介：技术学习、愿你我共同成长）。你分享的链接为微信 **`image_detail` 长图页**（`from_masonry=1`，来自看一看信息流），`__biz=MzIwMjUyNDM0OA==` 对应账号 **ListSec**。

根据 [sec_profile](https://github.com/tanjiti/sec_profile) 等聚合源，该号近期推送标题为 **《owasp top10 2025版本》**（短链示例：` `mid=2247486353` 同属该号新发文时段，**高度可能为同一主题的图解速查**。因微信验证码拦截，**未能读取长图内 OCR 文字**，下文「核心用法」主要依据 [OWASP Top 10:2025 官方发布](https://owasp.org/Top10/2025/) 与 [中文版基准说明](http://cn-sec.com/archives/5019547.html) 整理，便于你对照原文长图核对。

**OWASP Top 10:2025** 是面向开发与 Web 应用安全的**意识型标准清单**（第八版），强调**根因**而非单一 CVE 症状；相对 2021 版：**新增 2 类、合并 1 类**，并调整多项排名（如安全配置错误升至 A02，注入降至 A05）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 开发 / 全栈 / 后端 | ✅ 推荐 | 建立编码与 Code Review 的安全检查清单 |
| 渗透测试、安服、蓝队 | ✅ 推荐 | 与日常漏扫、渗透项对齐业界共识优先级 |
| 安全架构 / 合规负责人 | ✅ 推荐 | 做 SDL、供应商评估、培训纲要的「共同语言」 |
| 仅做基础设施、不涉及应用层 | ⚠️ 酌情 | 可重点看 A02 配置、A03 供应链、A09 日志 |
| 需要 exploit / PoC 逐步教程 | ❌ 不适用 | 本文档是风险框架，非漏洞复现手册 |
| 期望替代官方英文细则 | ❌ 不适用 | 以 [owasp.org](https://owasp.org/Top10/2025/) 与各 A0x 专题页为准 |

## 安装与前置条件

本主题为**知识框架**，无安装步骤。建议准备：

- 可访问 [OWASP Top 10:2025](https://owasp.org/Top10/2025/)（英文）或社区 [中文版发布说明](http://cn-sec.com/archives/5019547.html)
- 团队现有 Web 应用清单（语言栈、是否上云、是否用第三方组件/CI）
- 可选：SAST/DAST、依赖扫描（SCA）、WAF/网关配置审计工具（与 A02/A03 对应）

在微信内打开原文长图时，建议**保存图片**或**转发到文件传输助手**，便于与下文列表对照标注。

## 核心用法

### 2025 版十大风险（中英对照）

| 编号 | 2025 | 中文常见译名 | 相对 2021 要点 |
|------|------|--------------|----------------|
| A01 | Broken Access Control | 访问控制失效 | 仍居首位；SSRF 等并入此类 |
| A02 | Security Misconfiguration | 安全配置错误 | 排名显著上升 |
| A03 | Software Supply Chain Failures | 软件供应链失效 | **新类别**（范围大于「脆弱组件」） |
| A04 | Cryptographic Failures | 加密机制失效 | 排名下降 |
| A05 | Injection | 注入 | 排名下降 |
| A06 | Insecure Design | 不安全的设计 | 排名下降 |
| A07 | Authentication Failures | 身份认证失败 | 名称简化 |
| A08 | Software or Data Integrity Failures | 软件或数据完整性失效 | 延续，强调完整性 |
| A09 | Security Logging and Alerting Failures | 安全日志与告警失效 | 强调可观测与响应 |
| A10 | Mishandling of Exceptional Conditions | 异常情况处理不当 | **新类别**（替代原 A10 SSRF 独立项） |

### 与 ListSec 往期内容的衔接

同号曾发《[保护性安全措施与预防性安全措施](https://zone.ci/secarticles/wx/528331.html)》等短文：预防（WAF、认证、修洞）→ 事中（**渗透测试、漏扫**）→ 保护（备份、应急、日志）。**Top 10 清单**适合作为「事中/设计阶段」要覆盖的**技术风险维度**，与那篇「措施分类」互补。

### 可落地的三步（团队）

1. **对照长图 / 官方页**：在需求评审或 Sprint 计划里，按 A01–A10 勾选本迭代涉及项（如含文件上传则标 A01/A05/A08）。
2. **映射到现有控制**：把公司已有能力填入矩阵（例：A03 → SCA + 私有源；A09 → SIEM 规则 + 留存策略）。
3. **与 AI 辅助开发结合**：若使用 Cursor/Codex 等生成代码，在 Review 时显式引用 A01/A05/A07（越权、注入、认证）；可参考 [[../01-AI-Agent生态/Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 减少 Agent 盲目改安全相关逻辑。

### 官方与延伸资源

- 主站：https://owasp.org/Top10/2025/
- 智能体方向（另册，勿与 Web Top 10 混淆）：OWASP Agentic Applications Top 10（2025 年底社区发布，见 ZONE.CI 等转载）

## 注意事项与风险

- **抓取限制（重要）**：WebFetch、curl、Jina Reader 均返回微信**环境异常 / 验证码**；`image_detail` 正文与长图 OCR **未获取**。标题「owasp top10 2025版本」来自 [sec_profile README](https://github.com/tanjiti/sec_profile/blob/master/README.md) 聚合，**未用 sn/mid 在可访问 HTML 中交叉验证**；若你本地打开标题不同，请以微信为准并改本笔记 `title`。
- **合规**：ListSec 内容为安全研究与教学向；漏洞利用须授权。
- **版本**：生产环境应以组织采纳的 OWASP 文档版本及内部基线为准，勿仅依赖公众号长图。
- **AI 生成代码**：Top 10 不能替代人工威胁建模；Agent 可能引入 A03（依赖）、A10（异常信息泄露）类问题。

## 与你现有工具的关系

- **知识管理**：可将本清单作为 Obsidian 安全标签下的检查表，与 [[../01-AI-Agent生态/LLM Wiki：让 AI 替你维护个人知识库]] 结合，把评审结论记入 vault。
- **AI 编码栈**：与 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]、[[../01-AI-Agent生态/Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 搭配——前者负责工具链，后者约束 Agent 改代码时的验证习惯，降低 A05/A07 类缺陷。
- **自动化与内容**：与 [[AIMedia：全自动 AI 媒体创作与多平台发布]]、[[../01-AI-Agent生态/html-anything：AI 时代的 HTML 编辑器]] 无直接竞争；若做安全公众号排版，需注意 A08（第三方脚本/完整性）。
- **Web 自动化**：[[x-cli：AI Agent 一句话操控网页的 CLI 工具集]] 用于已登录态操作，不替代针对 A01/A05 的专项测试。

## FAQ

### Q: 为什么链接是 image_detail，和普通文章不一样？
A: 微信「图片消息/长图详情」页，内容多在多张图里，爬虫难以提取文字。需要在微信客户端内查看或手动 OCR/摘录。

### Q: 2025 版和 2021 版最大的两个变化是什么？
A: 新增 **A03 软件供应链失效**、**A10 异常情况处理不当**；**A02 安全配置错误**排名上升，**A05 注入**排名下降（仍须重点防护）。

### Q: 和 OWASP AI/Agent 清单怎么区分？
A: **Web Top 10:2025** 针对传统 Web 应用；**Agentic Top 10** 针对自主智能体（目标劫持、工具滥用等），二者并列使用，不要混为一谈。

## 相关链接

- 微信原文（长图）：
- OWASP Top 10:2025：https://owasp.org/Top10/2025/
- 中文版发布参考：http://cn-sec.com/archives/5019547.html
- ListSec 账号索引（doonsec）：http://wechat.doonsec.com/wechat_echarts/?biz=MzIwMjUyNDM0OA==
- 本库相关笔记：[[../01-AI-Agent生态/Karpathy 编码行为准则：AI Agent 的 4 条铁律]]、[[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]
