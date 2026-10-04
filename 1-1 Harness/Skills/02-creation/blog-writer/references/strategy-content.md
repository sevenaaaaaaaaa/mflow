# 选题策略（Content Strategy — blog-writer 内联版）

> **lineage**：2026-10-04 由 lovart-content-strategist + lovart-audience-ops 撤编并入；维度继承 `Content Strategy/00-09-*.md` 十份历史策略文档（每节标注来源）。本文件 = 博客选题策略 SSOT。
> **v1.0 首轮策略会（2026-10-04 · Moodio 轮）**：骨架值已按 Moodio 现状填充（内测期），值出处 = KB Moodio（02-personas/05-competitors v2.0/06-seo-keywords v1.1/08-team）+ 竞品实测调研。词群见 keyword-clusters.json v1.0（12 词群/4 KR）。品牌事实只出自 KB Moodio 目录。
> **铁律**：选题三重 trace = 词群（keyword-clusters.json）∩ 人群格（本文件 §漏斗）∩ 集群位置（§Silo）。缺一不写。

## 一、漏斗配比（← 01-漏斗内容矩阵）

四阶段覆盖度决定产能切分：

| 漏斗 | 形态 | 默认配比 | 说明 |
|---|---|---|---|
| TOFU | guide / insight / glossary / 定义式 | **50%** | 内测期抢词占位（空档词群 storyboard/shotlist 主力） |
| MOFU | howto / comparison / workflow | **30%** | 工作流内容（全流程主张落点） |
| BOFU | vs 页 / beta 申请页 / 导出互操作 | **20%** | 内测码转化；vs 遵守 05-competitors 对比规则；案例仅《了不起啊！朋友》可引用（复核上线状态） |
| Post-Purchase | 工作流指南 / changelog 解读 | 随 BoFu 摊 | 留存（← audience-ops 续费段触点） |

冷启动偏 TOFU，增长期调向 MOFU/BOFU——配比改动写回本节（版本递增）。

## 二、选题五轴（← 02/03/04/05/07 五份历史规划）

每轴独立开选题线，**每季度按轴复盘**一次优先级：

| 轴 | 来源文档 | 判定问题 | 落点形态 |
|---|---|---|---|
| 季节性 | 02-季节性内容日历 | 未来 6-8 周有什么行业节点/采购季？ | 提前 4 周发布的场景文 |
| 行业 | 03-行业深度规划 | 哪个行业 P0？该行业内容缺口？ | 行业解决方案文（Segment） |
| 职业 | 04-职业工作流规划 | 职业-产品匹配度高的职业？ | 职业工作流教程（persona 切片素材来源） |
| 企业级 | 05-企业级内容规划 | 采购决策链谁在看？安全合规懂不懂？ | 安全合规/团队协作/ROI 框架文 |
| 伦理与法律 | 07-AI 伦理法律 | 版权/伦理焦虑是否被回应？ | 权威回应文（E-E-A-T 强信号） |

### 五轴当前值（v1.0 · Moodio 内测期）

### 具体选题系列（v1.0 · 词群 → 条目，仿 Lovart 条目矩阵风格）

**SD 短剧系列（P0 楔子 · cluster-shortdrama）**
| ID | 条目 | 形态 | 优先级 |
|---|---|---|---|
| SD1 | Short Drama Storyboard Workflow: From Novel Script to Episode Board | How-To | P0 |
| SD2 | Keeping Characters Consistent Across 60 Episodes: The Asset Card Way | How-To | P0 |
| SD3 | Episode Review at Scale: Time-Stamped Feedback for Drama Teams | Best Practice | P1 |
| SD4 | Case: 《了不起啊！朋友》— AI 中剧的放映许可之路（复核上线后发布） | Case | P1 |

**AD 广告系列（P1 楔子 · cluster-ads）**
| ID | 条目 | 形态 | 优先级 |
|---|---|---|---|
| AD1 | TVC Storyboard in a Day: Agency Workflow with AI Previz | How-To | P1 |
| AD2 | From Brief to Board: Aligning Clients on References Before Shooting | Best Practice | P1 |
| AD3 | In-Feed Ads That Don't Look Generated: Taste as a Workflow | Insight | P2 |

**ST 分镜/Shot List 系列（P0 空档 · cluster-shotlist+storyboard）**
| ID | 条目 | 形态 | 优先级 |
|---|---|---|---|
| ST1 | Shot List Template for Short Films（已生成，S4-qa） | How-To | P0 |
| ST2 | Storyboard vs Shot List: What Professional Crews Actually Use | Comparison | P0 |
| ST3 | Script to Shot List: The Agent-Assisted Breakdown | How-To | P0 |
| ST4 | Searching References by Camera Movement: A Director's Guide | How-To | P1 |

**DEF 定义系列（P1 GEO · cluster-definitions）**
DEF1 What Is an AI-Native Film Set（GEO 定义锚）· DEF2 AI Filmmaking Terms Glossary · DEF3 What Is FDX and Why It Matters · DEF4 Previz Explained（P1）

**VS 对比系列（P1 BOFU · cluster-vs）**
VS1 Moodio vs Runway · VS2 vs Sora/Kling/LTX（场景化判断框架；遵守 05-competitors 实测数据规则）

**EX 交付系列（P2 · cluster-export）**
EX1 Export to DaVinci Resolve · EX2 FDX → Final Draft · EX3 Final Cut 工程交接

> 配比落位：SD/AD/ST = MOFU 主力（工作流）；DEF = TOFU（GEO）；VS/EX = BOFU（转化）。

## 三、Silo 内链（← 00-内容日历全景清单）

- 集群结构：pillar 长文 + spokes 教程/对比 + hub 聚合入口（spokes ≥5 才建 hub，hub 交给 hub-writer）
- 链接路由：spoke → pillar → hub 全互链；跨集群只经 hub
- 每篇新文发布时声明：`content_cluster` + 在集群中的位置（pillar/spoke）+ 本篇的出链清单（≥2 条集群内链）

## 四、复用链（← 06-内容复用与分发策略）

长文发布即触发衍生计划：长文 → 摘要稿（≤600）→ 社媒卡 → newsletter 段。分发执行走 content-distribution / multi-platform-push（UTM 按 AD-Tracking SSOT）。渠道优先级按 06 §渠道矩阵。

## 五、用户运营触点（← lovart-audience-ops 撤编并入）

内容在生命周期里的位置 = 运营视角的同一张图：

| 生命周期段 | 触点挂什么内容 | 度量 |
|---|---|---|
| 访客 | TOFU（本表漏斗） | 回访率 |
| 注册 | beta/howto | 注册→激活 |
| 激活 | 首作教程序列（D0/D3/D7） | **首作完成率** |
| 付费 | case / vs 页 | 转化率 |
| 续费 | 工作流指南 / changelog | 周回访 |
| 拥护 | 案例共创 / UGC 征集 | 推荐数 |

北极星 = **周回访做项目的用户数**（不是注册数）。用户高频问题/流失原因回流 §一 作为新选题（反馈回路）。

### 触点当前值（v1.0 · Moodio 内测期）

- 唯一转化出口 = **申请内测码**（app.moodio.art；全站 CTA 统一口径，禁写免费注册/购买）
- Onboarding 北极星 = **首作完成率**（带想法进来 → 完成第一部短片）——激活序列内容：D0 灵感检索上手、D3 剧本→分镜、D7 资产一致性、D14 导出交付
- 用户之声回流：内测创作者高频问题 → 词群评审（keyword-clusters.json 月度修订）

## 六、使用规则

1. 排期执行仍由 lovart-content-calendar 落地（本文件定节奏与配比，calendar 写日历）。
2. 信号驱动的临时选题（舆情/GSC/优化循环）也必须补三重 trace 后才入队。
3. 本文件修订 = 版本递增 + 在此记录一行 changelog。
