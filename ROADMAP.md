# MFlow 产品化 ROADMAP

> 目标：让任何公司 clone 下来 30 分钟跑通第一个内容工作流，并随使用深度逐步扩展。
> 状态标记：✅ 已交付 · 🔄 进行中 · 📋 规划

## Phase 0 · 产品化基座（2026-09-15 ✅）

- ✅ 首次引导向导：`首次引导 · Setup` 页，6 项检查清单（密码/LLM/知识库/日历/Demo/第一个工作流），每项一键跳转配置
- ✅ Demo 数据包：`docs/demo-reports/` 示例月报（数值条可视化）+ 示例舆情日报 + 一键注入演示任务
- ✅ Demo 生成回退：未配置 LLM Key 时自动出演示稿，完整跑通 生成→质检→状态机 闭环
- ✅ 部署文档三路径：`docs/deploy-guide.md`（本地 5 分钟 / systemd 生产 / Docker）
- ✅ 快速上手：`docs/quickstart.md`（首次使用 8 步）
- ✅ 模块扩展指南：`docs/modules.md`（四个注册点 / 数据源接入 / CMS 适配器 / 自我迭代）

## Phase 1 · 协作与日历（2026-09-15 ✅）

- ✅ Trello 式看板：卡片拖拽跨列、点击编辑（描述/负责人/截止日）、操作者署名（localStorage 轻协作）
- ✅ 看板 ↔ 内容日历打通：日历文章一键「加入看板」，卡片带 🔗 关联可跳回阅读
- ✅ 版本体系：`VERSION` + 侧栏版本号 + `/api/version`

## Phase 2 · 深度能力（2026-09-15 ✅ 全部交付）

- ✅ CJK 分词修复：post-write-check 词当量 = ASCII 词 + CJK 字符/2（perl unicode），680 汉字不再被记为 21 词，16/16 回归绿
- ✅ 质检可视化：hook 输出 ✓/✗/WARN 分项着色渲染（Loop 日志/质量钩子页复用 fmtHook）
- ✅ 媒体效果检验：分发页「效果归因」——已发布外链 canonical × GSC Top20 页面点击/曝光关联表（数据源可扩全量）
- ✅ CMS 适配器接口：`1-4 Dev/scripts/publish_adapters/`（接口约定 README + webhook 完整实现 + wordpress REST 骨架 + sanity 参考说明 + 统一 CLI）
- ✅ 报告可视化 R1 MVP：阅读器自动解析报告首个数值表 → 顶部指标卡仪表视图（月报即生效）
- ✅ Loop 并发与队列：移除单跑限制 → queued 状态 + 调度线程（并发上限 2）+ 每 Loop token 记账

## Phase 3 · 生态（已排期，下一轮开始）

**P3.1 账号体系 · 角色 · 审批流（1-2 天）**
- 基座已就绪：auth.json（OpenFlow bcrypt 迁移，13 用户）+ 登录名/密码 + 二级目录入口 `nownexts.com/mflow/`
- 角色分级：admin（全部）/ editor（创作+质检+推进）/ viewer（只读）——按 auth.json role 判定
- 卡片与 Loop 归属人过滤（"我的任务"视图）
- 发布审批流：approved 标志升级为 admin 审批动作（页面按钮 + 审计记录）

**P3.2 模板市场雏形（2-3 天）**
- 模板包格式：{工作流定义 + 提示词模板 + 知识源清单 + 质量钩子} 单 JSON
- 安装 / 导出 API + 模板管理页；内置 3 个行业模板（电商内容 / SaaS 增长 / 本地服务）

**P3.3 报告可视化 R1 完整版（2 天）**
- 月报 / 舆情日报 / 404 三个类型化 Dashboard 独立页（R1 MVP 已验证指标卡提取）

**P3.4 自我迭代仪表（1-2 天）**
- BLOCK 率 / token 成本 / 吞吐三曲线的月度自动回顾报告（写入报告中心）

- ✅ 域名二级目录入口：`nownexts.com/mflow/`（Apache 双 vhost ProxyPass，见 session log v3.5）
- ✅ 子域名方案备用：`deploy/setup-domain.sh` + `docs/domain-setup.md`（DNS → 反代 → HTTPS 三步）
- 📋 已知项：质检钩子调 python3 依赖环境 PATH（服务/管线已带 venv env；手动跑 smoketest 需先 source run/env.sh）
- 📋 报告可视化 R2-R5（Chart.js 趋势 / 双期对比 / PDF 导出 / 订阅摘要卡）
- 📋 插件规范：第三方数据源/发布渠道按 §modules 协议贡献，TOOLS-REGISTRY 自动收录

## 原则

1. 文件即状态：不引入数据库也能跑，规模化时才换 PG（接口已预留）
2. 发布人工授权是不可协商的边界
3. 每个新能力必须让未配置的新用户 5 分钟内看到效果
4. 错误只犯一次：踩坑必须沉淀为 hook 检查项或 RULES 条款
