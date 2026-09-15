---
type: session-log
session_date: 2026-09-15
session_slug: console-workbench
status: ready
---

# Session Log — MFlow 交互式工作台上线

## 目标
用户问是否有可交互界面；没有则建工作台。此前仅有只读状态页（render-status.py），codebox Go 工作台停在骨架。

## 交付
- **入口**：http://172.96.253.73:8088/（密码认证，MFLOW_CONSOLE_PASSWORD 在 run/env.sh）
- **六个功能区**：管线看板（建条目/合法推进/事件流）· 路由决策器（23 条矩阵可视 + 即时 decide）· 质量门禁（四钩子对项目内文件手动执行）· 每日管线（一键触发 + 日志尾随 + 运行态）· 分发队列（只读，铁律）· 系统（timers/最新产出/快捷入口）
- **架构**：console.py stdlib 单文件服务直绑 8088（取代 Apache 静态页，vhost 已 disabled 保留）；前端单页 vanilla JS；零新依赖
- **安全**：密码 constant-time 比较 + HttpOnly session cookie；subprocess 无 shell 拼接；item id 正则白名单；hook 名白名单；文件路径限定项目内；发布类操作一律只读

## 验证（端到端真实执行）
登录 401/403/200 闭环 → upsert → 合法 advance → 非法跳步被状态机拒绝（exit 2 附允许列表）→ 终态推进 → router decide 返回真实 profile/skills/reason → 看板数据一致。mflow-status.timer 已停用（被 console 取代）。

## 踩坑
- systemd EnvironmentFile 不认 shell `export` 语法 → 密码变量静默丢失、认证被跳过（PASSWORD 空 = 放行）。修复：service 用 `bash -c "source env.sh && exec …"`。教训：认证代码要显式处理"配置缺失"为 fail-closed，而非 fail-open + 打 WARN。

## 待办
- 用户改密码（env.sh 改 MFLOW_CONSOLE_PASSWORD → systemctl restart mflow-console）
- 看板中 demo 条目 console-smoke-test（FINAL/failed）可在 UI 推进观察，或忽略

## v2 追加（同日）——从"工程面板"重做为"内容运营工作台"

用户反馈：没有知识库、任务清单、报告，"这个后台我怎么用"。v1 只覆盖了管线状态机，是 agent 视角不是运营者视角。

**重做内容**：
- 总览：待办/管线/分发计数卡 + 最新月报/周报/舆情日报一键阅读 + 当日管线结果摘要
- 任务看板：手动任务（待办/进行/完成三列，tasks.json 持久化）+ 管线/分发队列自动同步只读区；预置 4 条真实待办
- 报告中心：10 分类（月报 27/周报 95/舆情日报 35/审计 38/404 分析 70/会话日志 55 等，共 400+ 份），markdown 渲染在线阅读（含表格）
- 知识库：KB 55M 目录浏览 + 全文搜索（文件名优先 + 内容命中带上下文，400 文件扫描上限）
- 认证 fail-closed（无密码配置时全拒）；路径穿越防护（400）；reader HTML 注入面 = 本地可信文档 + esc 渲染
- 新依赖：markdown==3.10.3（服务器 venv via uv；uv venv 无 pip，用 uv pip install --python）

**验证**：overview/reports(10 类)/kb tree+search/read(月报 149K html 含表格)/tasks 增改删/穿越防护 400/外部 200 全部真实通过。

## v3 追加（同日）——照 OpenFlow 控制台基因重构交互

用户指路：参考 OpenFlow Dev 后台设计。解剖 openflow-console.html 提取设计基因：
oklch 暖灰色彩系统（明暗双主题）、玻璃拟态顶栏 + macOS 红绿灯、248px 分组侧边栏、
衬线斜体 display 标题 + mono kicker、metrics 涨跌卡、纯 CSS 柱图、漂浮光斑背景。

**信息架构升级**（用户点名"主要入口、报表规划起来"）：
- 总览 = 问候 + 4 metrics + 最新成果一键读 + 近 7 日管线活动柱图（events.jsonl 统计）+ 调度状态 + 活动流
- 我的工作：任务看板 / 内容管线（独立页）
- 情报与产出：报告中心 / 知识库 / 分发队列（从任务页只读区提升为独立页：pending + published + dispatch 单授权态）
- 系统：路由·门禁 / 调度与日志
- login.html 同风格重做（blob 背景 + 渐变 logo + 玻璃卡）

后端：+/api/dist（pending/published/dispatch）、overview.chart7d。
验证：dist 2/7/5、chart7d 正常（今日 3 次推进 = 本轮 smoke）、外部 200。

## v3.1 追加（同日）——补上生产核心

用户点名缺失：LLM API 配置、Harness/Skills 管理、Agent 模式、节点模式、Blog/落地页生成入口、Loop 统一管理。

**交付**：
- **设置页**：LLM providers（deepseek/openai/custom，OpenAI 兼容 base+key）+ profile→model 映射（lovart-creation→deepseek-chat 等）+ 连通测试；key 存 run/llm.json（git-ignore/600/读取打码）
- **创作中心**：Blog + 6 类落地页（tools/features/product/scenario/solution/topic）× 10 语言；prompt 内置 Anti-Slop 硬规则（四问/禁套话/[待考证]/语义分段）；两种发起方式——单次生成（同步）或 Loop
- **Loop · Agent 模式**：loop_engine 后台线程 = 生成 → post-write-check → BLOCK 则带反馈重写，≤3 轮（对应 quality-cascade）；PASS 自动推进 S3-draft→S3-done→S4-qa；同刻仅 1 个运行（防超支）；可停止；日志实时落 loops.json
- **节点流水线 · 节点模式**：生成/质检/推进三节点真实可执行 + 人工审只读节点；每节点真调后端动作
- **Harness 管理**：8 规则（可在线读）+ 45 Skills 清点（分组/描述）+ harness_sync 一键重同步运行时

**诚实边界**：工作台生成的是快速稿（1.2-1.8k 字/落地页文案），7500 词级长文仍铁律走 signal-writer 完整流程；发布永远停在人工授权。

**待用户动作**：设置页填入 LLM API Key（如 DeepSeek）→ 点"测试连通"→ 创作中心即可真实生成。端到端在无 key 状态验证了优雅失败（fail-clean 报"LLM 未配置"）。

## v3.2 追加（同日）——知识中台：约束文档也是知识

用户质疑："本地知识库只有这么一点点？约束条件说明文档也算知识库吧？"——判断正确。
原 KB 页只挂产品知识库一角。重做为 10 大知识源（749 份 md）：
产品知识库 106 / 铁律与规则 8 / 故事线 SSOT 4 / 阶段手册 S0-S6 54 / 写作方法论 11 /
内容策略 510 / 关键词研究 14 / UTM 与追踪规范 4 / 质量案例库 31 / 项目记忆与治理 7。
源感知列表 + 跨源全文搜索（文件名优先 + 上下文摘录 + 800 文件扫描上限）。
验证：铁律源列出 RULES-00..60；搜"故事线"跨源命中 RULES-20/STORYLINES 等 12 处。
遗留小提示：08-storyline 里 iCloud 冲突副本 FEATURES-PRODUCTION 2.md 仍在（原 vault 卫生轮标记过），会被一起索引。

## v3.2 追加（同日）——运营六缺口

用户点名六条：工作流的角色/skills/知识库不可见、token 开销不可见、内容日历缺失、外链无法导出、Trident 工作流缺失、报告纯文本不利展示。

全部落地：
1. 工作流地图页：6 条工作流（blog/landing/qa/publish/trident/daily）× 阶段链 + Profile + Skills（可点读 SKILL.md）+ 关联知识源（可跳知识中台）
2. llm_chat 记录真实 usage → llm-usage.jsonl；用量页（14 日柱图/profile 分摊/明细）
3. Content Calendar 3280 篇同步上服务器（踩坑：rsync 远端路径空格被远端 shell 拆分，落到了 /var/www/mflow/1-3，已 mv 归位）；日历页 = 语言统计 + 12 月分布柱图 + 过滤搜索阅读
4. /api/dist/export 导出全部已发布外链 CSV（date/platform/slug/canonical/offsite_url）
5. Trident 页：4 步骤手动触发 + Data Ingestion 产出健康
6. 报告阅读器 V1 增强：TOC（月报 63 条）+ 表格数值条（月报 3753 条）；v2 规划落 docs/report-vision.md（R1 类型化 dashboard → R2 Chart.js → R3 对比模式 → R4 PDF → R5 订阅摘要）

验证：calendar 3280（en796/zh792/zhtw788/ja788/ru58/pt58）、workflows 6、trident 4 步、CSV 10 行、toc 63/numbar 3753、外部 200。

## v3.3 追加（同日）——产品化 Phase 0/1（面向所有公司可用）

用户要求产品化排期并全部解决。交付：
- **Setup 引导页**：6 项配置清单（密码/LLM/知识库/日历/Demo/首个工作流），徽标显示完成度，逐项跳转
- **Demo 模式**：seed API 注入演示任务 + 标记；llm_chat 无 Key 时回退演示稿 → 未配 Key 也能完整跑通 生成→质检→状态机 闭环（hook_rc=0 验证）；示例月报/舆情报告两份（docs/demo-reports/）
- **Trello 看板**：卡片拖拽跨列 + 编辑弹层（标题/描述/负责人/截止日）+ 操作者署名（localStorage）
- **日历↔看板**：日历页一键「加入看板」，卡片带 🔗 关联
- **版本体系**：VERSION 1.0.0 + /api/version + 侧栏版本号
- **文档**：quickstart（8 步）/ deploy-guide（本地/systemd/Docker）/ modules（模块四注册点/CMS 适配器/数据源扩展/自我迭代）/ ROADMAP（四阶段排期）/ README 补新用户入口

**踩坑新录**：post-write-check 词数按空格分词，CJK 长文被严重低估（680 汉字=21 词）——demo 模式豁免；正式中文稿需给 hook 加 CJK 字符当量逻辑（已列 Phase 2）。

**验证**：setup 5/6 绿（差 LLM Key 属预期）、seed 注入、demo generate 680 字 hook PASS、version 1.0.0、外部 200。

## v3.4 追加（同日）——Phase 2 全量交付

1. CJK 分词修复落地（perl unicode 词当量，服务器验证 1778 字符→261 词，smoke 16/16 with env）
2. 效果归因 /api/impact：published 外链 canonical path × GSC top20_pages；分发页表格渲染；数据边界注明（top20，可扩全量）
3. 报告仪表 MVP：/api/report/dashboard 解析首个数值表 → 阅读器顶部指标卡（demo 月报：指标/上月/本月/环比 ×5 行）
4. Loop 队列：queued + 调度线程（并发 2）+ loop.tokens_used 记账（LAST_USAGE 锁传递）
5. publish_adapters：webhook 实现 / wordpress 骨架 / sanity 参考 / 统一 CLI / 接口 README
6. 域名接入：setup-domain.sh（宝塔 Apache 基于域名 vhost 反代 8088，零影响既有站点）+ docs/domain-setup.md 三步（DNS→反代→HTTPS）；待用户提供域名即可生效
已知项：smoketest 需 source env.sh（系统 py3.6 不认 annotations）——服务与管线不受影响（均带 venv env）。

## v3.5 追加（同日）——二级目录入口 + OpenFlow 账号打通

用户反馈：域名方式打不开，改用现有站点二级目录；账号密码照搬 OpenFlow。

**发现**：真实站点域名 = nownexts.com（Cloudflare 代理 → 源站 172.96.253.73），OpenFlow 部署于 /www/wwwroot/nownexts_com/（非 /var/www/openflow）；用户库 data/users.json = 13 用户 PHP bcrypt（$2y$）。

**交付**：
- 入口：https://nownexts.com/mflow/ （80 强制 HTTPS → 443 双 vhost 注入 ProxyPass /mflow/ → console:8088；备份+configtest+graceful）
- 认证：console 登录改造为多用户 bcrypt 校验（run/auth.json 600），单密码模式向后兼容，fail-closed 保留；login 页加用户名；header 显示当前用户；卡片负责人默认当前用户
- 前端 48 处 API 调用全部改相对路径（子路径反代兼容）
- 公网验证：登录页 200 / 错误密码拒绝 / 未认证 API 401 / XMP 主站 200 零影响
- ROADMAP Phase 3 细化排期：P3.1 账号角色审批（1-2d）→ P3.2 模板市场（2-3d）→ P3.3 报告 Dashboard（2d）→ P3.4 自我迭代仪表（1-2d）

**待用户**：用 OpenFlow 同款用户名密码登录（如超管 Seven）验证 bcrypt 实际匹配；若 CF 有缓存可在 CF 刷新 /mflow/*。

## v3.5 追加（同日）——二级目录入口 + OpenFlow 账号打通

用户反馈：域名子域名方式打不开（无域名/DNS 未做），改用现有站点二级目录；账号密码照搬 OpenFlow。

**发现**：真实站点域名 = nownexts.com（Cloudflare 代理 → 源站 172.96.253.73）；OpenFlow 部署于 /www/wwwroot/nownexts_com/（非 /var/www/openflow）；用户库 data/users.json = 13 用户 PHP bcrypt（$2y$），含超管 Seven。

**交付**：
- 入口：https://nownexts.com/mflow/（80 强制 HTTPS → 80/443 双 vhost 注入 ProxyPass /mflow/ → console:8088；备份+configtest+graceful，零影响 XMP）
- 认证：console 登录改造为多用户 bcrypt 校验（run/auth.json 0600），单密码向后兼容，fail-closed 保留；login 页加用户名字段；header 显示当前用户；任务负责人默认当前用户
- 前端 48 处 API 调用全部改相对路径（子路径反代兼容，绝对路径引用归零）
- 公网验证：登录页 200 / 错误密码拒绝 / 未认证 API 401 / XMP 主站 200
- ROADMAP Phase 3 细化排期：P3.1 账号角色审批（1-2d）→ P3.2 模板市场（2-3d）→ P3.3 报告 Dashboard（2d）→ P3.4 自我迭代仪表（1-2d）

**待用户**：用 OpenFlow 同款用户名密码登录实测 bcrypt 匹配（如超管 Seven）；若 CF 缓存可在 CF 刷新 /mflow/*。

## v3.6 追加（同日）——P3.1 账号角色与审批流

**登录失败排查结论**：hash 完整（60 字符 $2y$）、PHP↔Python bcrypt 互认实测等价（PHP password_hash → Python checkpw True/False 正确）、迁移源正确（admin/login.php 确读 users.json + password_verify + 可选 TOTP/验证码，无 TOTP 用户）。"密码错误"为后端真实响应——最可能是输入凭证与 users.json 不匹配。解法=重置通道，非代码缺陷。

**P3.1 交付**：
- 角色分级落地（OpenFlow 角色直继承）：admin 全部；marketing/sales/operator=editor 级；viewer 只读 POST 拦截；admin-only 白名单（LLM 配置/账号管理/审批/管线触发/任务删除）
- 发布审批流：dispatch 单 admin「批准发布」按钮 → approved/approved_by/approved_at + run/approvals.log 审计
- 账号管理：设置页 admin 查看账号角色表 + 应用内重置任意账号密码（bcrypt，审计）；root CLI deploy/reset-account.sh（免登录重置，服务自动重启）
- ROADMAP P3.1 标记完成；"我的任务"归属人过滤移入下一小批

**给用户的登录修复路径**：root 执行 `bash /var/www/mflow/deploy/reset-account.sh Seven 新密码` → 用 Seven+新密码登录 → 设置页可重置其他账号。

## v3.7 追加（同日）——P3.2 模板市场

- 模板包 v1 schema：id/name/version/author/description + workflow{flow/profiles/skills/kb} + prompt{audience/tone/structure/anti_slop_extra} + kb_sources_suggestion；templates/ 目录随仓库分发
- 内置：ecommerce-content（绝对化用语/原价编造/虚假销量禁例）、saas-growth（无出处 ROI 承诺禁例）、local-service（NAP/资质/价格区间约束）
- gen_prompt 模板化：structure 替换默认结构 + audience/tone 注入 + anti_slop_extra 追加；{TOPIC} 占位符
- API：/api/templates（列表）、/api/templates/import（三要素校验 + id 规范化）、/api/templates/export（下载）、/api/templates/delete（内置保护）；generate/loop 接受 template_id
- 前端：创作中心「行业模板」chips（默认 MFlow 标准）；模板市场页（卡片/JSON 查看/导出/导入/删除）；导航徽标
- e2e：templates 3 → import 4 → delete 3；ecommerce 模板 + demo 回退生成 hook PASS
- 教训：console 重启清空内存 session——旧 cookie 401 会被误读为路由缺失；测临时账号用 venv python 清理（系统 py3.6 ascii 编码读中文 auth.json 会炸）
