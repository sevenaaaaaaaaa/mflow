# MFlow 产品定位（SSOT v2）

> 口径：**轻量版 OpenFlow，专解内容生产、分发和触达；与 OpenFlow 是共生，不是切割。**
> v2 = v1 三句话经功能自评修正后的版本（自评见 §3），并新增联动设计（§4）。本文是定位的单一事实来源。

## 一、定位（保留用户口径，标注修正）

1. **专解内容生产、分发和触达**
   - ✅ 生产：状态机 + 质量门禁 + Loop 自动生成，10 语言，已真实运转
   - ✅ 分发：Sanity/WordPress/Webhook 适配器 + 四轨道外链（webhook 完整、wordpress 骨架——"极好"里最弱的一环，补齐见 §四）
   - 🔄 触达：GEO 引用感知闭环已上线（探测/缺口/改稿）；"触达"的传统含义（SEO 排名、社媒互动）依赖数据源接入深度，属持续增强而非已满格
2. **轻量版 OpenFlow** —— ✅ 成立：stdlib 单文件内核、文件即状态、同机并行部署。不是"迷你 OpenFlow"（功能子集），而是"同底座上的专用形态"。
3. **对 CDP、CMS 要求不高，对生成、分发兼容度极好** —— 基本成立。修正一处："极好"应表述为"**兼容度优先级最高的设计目标**"——分发端 wordpress/sanity 适配仍需逐家联调，兼容度是承诺方向，不是已盖棺的测试结论。

## 二、与 OpenFlow 的关系：共生，不是竞品

| 关系 | 事实 |
|------|------|
| 共享底座 | 同服务器、同域名（nownexts.com）、同一账号体系（OpenFlow users.json bcrypt 已直接继承） |
| 互补分工 | OpenFlow = 业务前台与后台（CDP/CMS/会员/交易）；MFlow = 内容产线（生产→质检→分发→触达回流） |
| 部署关系 | 硬隔离（目录/端口/进程/日志）是**运行安全**要求，不是产品隔绝——API 层随时可联 |

## 三、联动与 API 打通（设计承诺）

| # | 联动点 | 状态 |
|---|--------|------|
| L1 | **身份打通**：OpenFlow users.json bcrypt 直接登录 MFlow（已迁移 13 账号） | ✅ |
| L2 | **机器 API**：`X-MFlow-Token`（GET-only，写动作仍归真人）——OpenFlow 可拉取版本/状态/归因/引用缺口等只读数据 | ✅（今日实现） |
| L3 | **发布回流 OpenFlow**：publish_adapters/webhook + wordpress REST 骨架——OpenFlow 若提供内容端点即可直收 MFlow 成稿 | 📋 适配层就绪，逐家联调 |
| L4 | **业务信号→选题**：OpenFlow 的订单/咨询/FAQ 热词推入 MFlow topics 队列（机器 API 或 webhook） | 📋 规划 |
| L5 | **CDP 事件→归因**：OpenFlow 的 GA/CDP 转化事件作为 impact 数据源（plugins 规范 source 类型已预留） | 📋 规划 |
| L6 | **后台互链**：OpenFlow 面板嵌 MFlow 卡片（iframe nownexts.com/mflow/），MFlow 报告可回链 OpenFlow 报表 | 📋 规划 |

**边界（不因联动而松动）**：机器 API 仅 GET；发布类动作永远人工授权；凭证不入 git。

## 四、选型语义（替代 v1 的"切割式"矩阵）

- **内容产能是主要痛点** → MFlow 单独跑也成立（不依赖 OpenFlow 存在）。
- **已有 OpenFlow/业务后台** → MFlow 挂同机作内容产线，账号复用，业务信号经 L4/L5 喂给内容闭环。
- **需要完整 CDP/交易后台** → OpenFlow 为主，MFlow 为内容子系统。
- 两者不是"二选一"，是**同一台机器上的前台与产线**。
