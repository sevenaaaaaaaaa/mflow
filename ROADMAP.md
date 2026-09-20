# MFlow 产品化 ROADMAP

> 目标：让任何公司 clone 下来 30 分钟跑通第一个内容工作流，并随使用深度逐步扩展。
> 状态标记：✅ 已交付 · 🔄 进行中 · 📋 规划
> 更新：2026-09-20（覆盖至 Phase 22）。进行中的细粒度计划见 `docs/p1-plan.md`；能力现状与缺口见 `docs/capability-matrix.md`；一手记录见 `1-1 Harness/11-knowledge/sessions/`。

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

## Phase 2.5 · 平台化多项目（2026-09-15 ✅ 计划外提前交付）

- ✅ 去 Lovart 化：登录页/后台文案/生成提示词全部通用化（"提及你的产品/工具"），内部 skill ID 保留
- ✅ 多项目架构：项目 = `run/projects/{id}/` 独立数据命名空间（管线状态/事件/看板/Loop/生成物）
- ✅ 项目 API：新建（slug 化 + meta.json）/ 切换（session 上下文）/ 删除（admin → _trash 回收站）
- ✅ 前端：侧栏项目切换器 + ＋新建项目；总览问候显示登录名
- ✅ 隔离 e2e：main 继承存量（7 任务/3 管线条目）→ 新建项目 B 全空 → B 加任务 → 切回 main 不串 → 删 B 进回收站
- ✅ 共享平台能力：用户/LLM 配置/模板/知识中台/报告中心/调度
- 📋 项目级调度与知识源隔离（每个项目独立知识源挂载）→ Phase 4

## Phase 5 · 自动化执行（2026-09-16 ✅ 全部交付）

- ✅ P5.1 自动排程执行器：全局线程每 5 分钟扫描——项目配额未满且选题队列有货时，自动从队首取题创建 Loop（demo/真实 LLM 通用，token 记账照常），执行日志随项目落 run/projects/{id}/schedule.log
- ✅ P5.2 选题队列：每项目 topics.json + 工作台设置页管理（批量粘贴/逐条删除/计数）
- ✅ 排程状态 API：/api/schedule/status（今日已建/配额/运行中/排队/队列长度/日志尾）
- ✅ P5.3 排程报表：/api/schedule/all 跨项目一行一项目（配额进度条/运行/排队/选题队列/日志尾）进「调度与日志」页
- ✅ P5.4 Loop 终态通知：done/blocked/failed 推飞书（stopped 不打扰）；设置页 admin 配 webhook + 测试；run/notify.json 600
- ✅ P5.5 项目独立 LLM：meta.llm{provider/base/key/model} 覆盖全局（优先级 项目>全局>demo），生成与 Loop 同走；GET 全程打码，空 Key 即清除回退
- ✅ P5.6 插件市场：plugins/marketplace.json 内置可装包（rss-source/webhook-publisher）+ 粘贴安装（自动 plugin_check，失败进 _trash）+ 卸载

## Phase 4 · 放大项（2026-09-15/16 ✅ 首批交付）

- ✅ P4.1 多租户账号隔离：auth.json 用户绑定 projects（admin 全可见）；/api/projects 按用户过滤、switch 越权回落；create 自动绑定创建者；main 永远可见；设置页 admin 逐账号分配 UI；e2e 验证（受限用户只见绑定项目 + 无串扰）
- ✅ P4.2a 项目级知识源：meta.kb_extra（label/dir/glob，路径安全校验）→ 知识中台合并渲染 [项目] 源 + 域内搜索；知识中台页挂载表单
- ✅ P4.2b 项目调度配置：meta.schedule（daily_quota/auto_loop）存储 + 设置页当前项目配置卡；**自动排程执行器排 Phase 5**（当前保存意图）
- ✅ P4.3 报告可视化 R2（表格 → Chart.js 图表切换）/ R4（打印/PDF 样式与按钮）/ R3（双报告并排对比）/ R5（总览本周速览卡：新增报告/吞吐/token）
- ✅ P4.4 插件规范：docs/plugins.md（三类插件 + manifest + 权限模型）+ plugins/plugin_check.py 六项校验器（示例插件 PASS）+ sample-source 示例

## Phase 3 · 生态（2026-09-15 ✅ 全部交付）

**P3.1 账号体系 · 角色 · 审批流（2026-09-15 ✅）**
- ✅ 多用户 bcrypt 登录（auth.json，OpenFlow 13 用户迁移）+ 角色分级落地：admin 全部 / marketing·sales·operator 创作与质检 / viewer 只读拦截；admin-only 白名单（LLM 配置/账号管理/审批/管线触发/删除）
- ✅ 发布审批流：dispatch 单 admin「批准发布」按钮 + approved_by/approved_at + run/approvals.log 审计
- ✅ 账号管理：admin 在设置页查看 13 账号与角色、重置任意账号密码（审计留痕）；root CLI `deploy/reset-account.sh` 免登录重置
- ✅ 二级目录入口 nownexts.com/mflow/ + 当前用户显示 + 卡片负责人默认当前用户
- ✅ 归属人过滤（"我的任务"视图）（2026-09-16 Phase 5 收官交付）

**P3.2 模板市场雏形（2026-09-15 ✅）**
- ✅ 模板包格式 v1：{id/name/version + workflow 定义 + prompt(audience/tone/structure/anti_slop_extra) + kb_sources_suggestion} 单 JSON，`templates/` 随仓库分发
- ✅ 内置 3 个行业模板：电商内容（广告法禁例）/ SaaS 增长（ROI 承诺禁例）/ 本地服务（NAP 一致性）
- ✅ 生成联动：创作中心选模板 → gen_prompt 应用行业 audience/tone/结构/附加禁例；Loop 记录 template_id
- ✅ 市场页：模板卡（版本/作者/描述/工作流链）+ 查看 JSON + 导出下载 + 粘贴/文件导入（校验三要素）+ 自定义模板删除（内置保护）
- ✅ e2e：列表 3 → 导入 4 → 删除回 3；带模板生成 hook PASS

**P3.3 报告可视化 R1 完整版（2026-09-15 ✅）**
- ✅ 通用结构解析器：/api/report/structure 把任意 md 报告解析为 H2 分节 + 段落 + 表格（月报 20 节 29 表 / 舆情日报 15 节 12 表验证）
- ✅ 「报告仪表」独立页：分类+报告选择 → 仪表渲染（首个数值表升格为指标卡组，全部表格带比例条），一键切换原文阅读

**P3.4 自我迭代仪表（2026-09-15 ✅）**
- ✅ QA 历史埋点：所有质检执行（手动钩子/生成/Loop）记录 run/qa-history.jsonl
- ✅ 「自我迭代仪表」页三曲线：BLOCK 率（近 14 日）/ Token 消耗 / 吞吐（30 日全项目状态机推进）+ 质检明细
- ✅ 月度自动回顾：一键生成 `MFlow-自我迭代回顾-YYYY-MM.md` 写入报告中心（含质量/Token/吞吐三段 + 洞察框架）

- ✅ 域名二级目录入口：`nownexts.com/mflow/`（Apache 双 vhost ProxyPass，见 session log v3.5）
- ✅ 子域名方案备用：`deploy/setup-domain.sh` + `docs/domain-setup.md`（DNS → 反代 → HTTPS 三步）
- ✅ Phase 5 收官（2026-09-16）：归属人过滤（"我的任务"）· 排程报表进调度页 · Loop 终态飞书通知（run/notify.json，admin 配置）· 项目独立 LLM Key（meta.llm，清空即回退全局）· 插件市场（marketplace.json + 安装/卸载/plugin_check 六项）· 钩子 PATH 修复（LOVART_PYTHON → 项目 venv 自动探测，smoketest 免 source 16/16）
- 📋 插件规范：第三方数据源/发布渠道按 §modules 协议贡献，TOOLS-REGISTRY 自动收录

## Phase 6 · GEO Content Loop（2026-09-16 ✅ 首批全链路）

- ✅ P6.2 GEO 门禁：`geo-check.sh`（可分块结构/统计密度/问答式标题/来源标注/墙式段落，--strict 升 BLOCK）接入 Loop 质检级联与单次生成；gen_prompt 注入 GEO_RULES（问答式 H2/数据点密度/自包含短段/来源链接）
- ✅ P6.1 引用感知：设置页配置品牌/竞品/目标查询 → 逐条走官方 OpenAI 兼容 API 问 AI 引擎，检测品牌/竞品提及与来源 URL → citations.jsonl；demo 模式 fail-clean 拒绝（演示稿不代表真实 AI 行为）
- ✅ P6.3 归因闭环：/api/impact 并入 geo（查询级提及率 + 竞品份额）
- ✅ P6.4 缺口自动选题：0 引用查询一键「→ 选题队列」→ 自动排程消化
- ✅ P6.5 改稿 Loop：0 引用查询一键「→ 改稿 Loop」（refresh-slug，brief 内置 GEO 重写指令，走既有 Loop 引擎）
- ✅ P6.6 GEO 仪表：设置页 GEO 卡——品牌提及率/竞品份额/近 14 日趋势迷你柱图/缺口清单

### P6 二批（2026-09-16 ✅）
- ✅ P6.7 每日自动探测：geo_scheduler 后台线程（每小时检查，09:30 后、当日无成功记录即探测）；设置页 GEO 卡「每日自动探测」开关；失败/记账行不阻塞当日重试
- ✅ P6.8 Perplexity sonar 真引用：providers 新增 perplexity（api.perplexity.ai）；GEO 卡选引擎 + 模型名（sonar/sonar-pro）；响应官方 citations 直接采信；llm_chat_full() 返回 (content, meta) 不走 demo 回退
- ✅ P6.9 citations × 已发布 URL 精确归因：canonical 路径归一化匹配（协议/子域/query/尾斜杠容错）→ GEO 卡「被 AI 引用的页面」（slug/平台/被引次数/命中查询）
- ✅ P6.10 GEO 曲线进自我迭代仪表：第四条曲线 = 品牌提及率 14 日（实心柱=被提及日）+ 缺口计数徽标

### P7 批次（2026-09-16 ✅）
- ✅ P7-B1 内容衰减监测：decay_analysis（发布≥30 天 × GSC Top20 无记录 × 无 AI 引用）→ 分发页衰减卡 + 一键改稿 Loop
- ✅ P7-B3 多引擎交叉探测：engines[] 任意 provider 直连（缺 Key 引擎级报错）+ per_engine 分拆 + 引擎分歧检测徽标
- ✅ P7-C 门禁固化：session-init GATE 5 console syntax（node --check JS × ast py × bash -n hooks）——4 处语法回归类事故自此有硬门禁；门禁自身 python 解析/glob 三 bug 顺修，服务器 5/5 PASS
- 📋 P7-B2 竞品引用源反向工程 · P7-B5 发布后自动复测 · P7-B6 GEO 综合分 · 衰减自动改稿 opt-in

### P7 二批（2026-09-16 ✅）
- ✅ P7-B2 竞品引用源反向工程：competitor_urls 按域聚合 + 一键对标选题
- ✅ P7-B5 发布后复测窗口：≤7 天新页 × 引用记录 → 复测状态卡（与每日自动探测联动）
- ✅ P7-B6 GEO 综合分：提及率40 + 缺口覆盖30 + 相对份额20 + 结构健康10 → 0-100（无数据不造假分）
- ✅ 衰减自动改稿 opt-in：auto_refresh 开关，每日 ≤2 篇 refresh Loop 自动排程（去重 + 审计）

## Phase 8 · OpenFlow 联动（2026-09-16 启动）

- ✅ L1 身份打通：OpenFlow users.json bcrypt 继承登录（P3.1 已交付）
- ✅ L2 机器 API：X-MFlow-Token GET-only（写动作仍归真人会话）——外部系统可拉版本/状态/impact/geo 缺口等只读数据
- 📋 L3 发布回流 OpenFlow：webhook/wordpress 适配器逐家联调
- 📋 L4 业务信号→选题：OpenFlow 订单/咨询/FAQ 热词 → topics 队列
- 📋 L5 CDP 事件→归因：转化事件作为 impact 数据源（plugins source 规范已预留）
- 📋 L6 后台互链：OpenFlow 面板嵌 MFlow 卡片 / 报告回链

## Phase 9 · MFlow Pay 变现闭环（2026-09-17 ✅ 首批）

- ✅ 临时支付链接：商品/数量/兑换码/有效期 → 不可枚举 token 链接（可过期清扫）
- ✅ 加密收款：USDT-TRC20 链上自动核验（TronGrid，金额+地址+时间窗三匹配）/ ERC20·BTC 手工确认 / 外部 webhook 回调
- ✅ 发卡系统：卡密池批量导入去重 → 确认到账自动发卡；库存不足挂 paid_no_stock 可重发
- ✅ 兑换券：抵扣金额 / 折扣 % / 免费兑换（0 元直发）+ 适用商品 + 次数 + 过期
- ✅ 公开收银台 /pay/{token}（无鉴权，token 即凭据）+ 工作台「支付 · 发卡」管理页
- ✅ 机器只读：X-MFlow-Token 可读订单/商品/统计（供 OpenFlow 联动）
- 📋 待用户：配置收款钱包地址（TRC20 填了才开启自动核验）；ERC20/BTC 链上核验（需 Etherscan Key）

## Phase 10 · 线上发布通道（2026-09-17 ✅ Sanity 上线）

- ✅ Sanity 服务端发布器：`publish_adapters/sanity_publisher.py`（纯 Python HTTP API，无需 Node）+ MD→PortableText 转换器入仓
- ✅ 凭证上云：Mac sanity-cli token → 服务器 `run/secrets/sanity.json`（600/700，git-ignore）；三级解析（env → secrets → 本地）
- ✅ 发布 API + 工作台「发布通道」卡：连通探测 / dry-run（Sanity 原生 dryRun 不落库）/ 真实发布（status=draft，createIfNotExists 不覆盖）/ 发布历史审计
- ✅ 人工授权门禁：条目须 S4-qa 及之后 + qa BLOCK 全 0，admin-only，真实写库二次确认
- ✅ WordPress 通道就绪（待 `run/cms.json` 配置 base/user/app_password）；Webhook 通用出口可用
- 📋 待用户：提供 WordPress 站点与应用密码；确认首篇真实发布（Sanity draft）

## Phase 11 · 多站点内容库（2026-09-17 ✅）

- ✅ 站点档案机制：`run/sites/{site}.json`（domain/默认语言/数据源/sections: docType·pageType·dir·route）——**换站点只换档案，不改代码**
- ✅ Sanity → 库同步器：`1-4 Dev/scripts/library/sanity_pull.py`（分页/剔草稿/两种正文引擎）+ `pt_to_md.py`（Portable Text → Markdown）
- ✅ 首次全量镜像：17,535 篇 / 215MB（blog 8,864 · features 6,400 · tools 1,661 · topics 409 · solutions 120 · products 41 · scenarios 23 · news 17），3 分钟
- ✅ 工作台「内容库」页：站点/段落（计数）/语言/搜索/阅读/后台同步+进度（admin，审计）
- ✅ 默认项目更名 **Lovart Global**（id `lovart-global`，含存量管线/任务/Loop/GEO 数据迁移）
- ✅ 内容日历清空（归档 `run/_archive/content-calendar-20260917.tar.gz`，17MB；Sanity 为 SSOT）
- 📋 库 → GEO 闭环联动：缺口 × 库内已有 → 自动判定「改稿 / 新写」
- 📋 第二站点档案示例（验证多站点目录结构泛化）

## Phase 12 · 批量执行与物料（2026-09-17 进行中）

**P12.1 落地页与图片物料（✅ 已交付）**
- ✅ 物料台账：`asset_tools.py scan` → 17,538 页 / 208 素材 URL（反查谁在用）；`run/library/{site}/assets.json`
- ✅ 替换计划：exact/prefix/regex/url-map + 过滤（段落/语言/类型/slug）
- ✅ 批量应用：默认 dry-run（Sanity 原生）；真写带 `ifRevisionID` 并发保护、≤50/批、审计 approvals.log
- ✅ 工作台「内容库 → 图片物料」：扫描 / 台账 / 三步替换（计划→dry-run→应用）
- 📋 待用户：真实替换 pilot（需提供新图 URL 或素材替换规则）

**P12.3 批量任务执行器（✅ 2026-09-17 交付）**
- ✅ 任务模型：`run/batch/{id}.json`（items[] · 逐项状态 · attempts · 日志 · 原子写）
- ✅ 四类执行器：asset_replace（含 ifRevisionID）/ field_patch / gen（生成+门禁+状态机推进）/ rewrite（按指令改稿）
- ✅ 执行语义：并发 2 · 失败重试 · 暂停/继续/取消 · 断点续跑（重启自动续）· 审计
- ✅ 工作台「批量任务」页：创建（4 类型 + JSON items）/ 进度条 / 详情（条目级结果）/ 一键从物料计划建任务 / 暂停·重试·取消
- ✅ API `/api/batch/{list,detail,create,action}` + 文档 docs/batch.md
- 📋 待用户：真实批量任务的首次放量（物料替换 / 高曝光低 CTR 改稿）

**P12.2 Agent 任务台（✅ 2026-09-17 交付）**
- ✅ 对话链路：上下文组装（harness 规则摘要 + Top5 skills + 库命中 + GEO 缺口）→ LLM 规划器（严格 JSON: say/questions/spec）→ 规格门禁 → 批准 → 复用 P12.3 批量执行器
- ✅ 规格门禁 spec_guard：类型/字段白名单 · 规模上限（物料字段≤200、生成改稿≤20）· dry-run 默认 · 真实执行需 force
- ✅ 不确定即反问、不编造 doc_id（实测："帮我改落地页图片"→ 反问 2 条且 spec=null）
- ✅ 工作台「Agent 任务台」页：会话列表 / 对话线程 / 上下文可见（skills·库命中·规则字符数）/ 规格卡（批准 dry-run / 真实执行）/ 结果回流
- ✅ API `/api/agent/{sessions,session,chat,execute}` + 文档 docs/agent.md
- 📋 待办：长文 skill 流程深度接入（7500 词级）；会话删除/归档

**P12.4 QA → 修复编排（✅ 2026-09-17 交付）**
- ✅ 批量扫描：`qa` 执行器（kind=sanity 字段规则确定性检查 / kind=md 跑门禁钩子）；范围展开 `kind=sanity-filter|drafts`
- ✅ findings 结构化：`{target, rule, severity, detail, fix{type,set}}`——规则：seoTitle 缺失/超长 · description 缺失/超长 · cover.alt 缺失 · 草稿 block/warn
- ✅ 一键编排：字段→field_patch · alt→asset_replace · 草稿 block→rewrite（复用批量执行器；dry-run 默认）
- ✅ 复检闭环：同目标新建 QA 任务（parent 关联）→ `/api/qa/delta` 输出已解决/新增；实测 dry-run 下如实报告"未闭环"（不伪造）
- ✅ 工作台「QA 编排」页 + API `/api/qa/{create,tasks,findings,cycles,delta,orchestrate,recheck}` + docs/qa.md
- 📋 待用户：真实修复放量（实测 84 项待修：60 补 seoTitle + 24 截断 description）

## Phase 13 · Harness 治理（2026-09-17 ✅）

- ✅ 审计：`docs/harness-audit.md`（规则硬条款密度 / 45 skills 体量与描述覆盖 / 故事线噪音 / 语言规则缺口）
- ✅ RULES-70 数量限制与防注水（20 条硬规则）；RULES-80 十语言生成规则
- ✅ 钩子 quota-check.sh（字数/H2/FAQ/重复句/列表灌水/过渡词）+ lang-check.sh（简繁/字形/标点/残留）→ 接入生成链（loop/batch/generate 四门禁）
- ✅ 提示词注入 CONTENT_BUDGET + LANG_RULES
- ✅ 任务拆批次 + 上下文摘要传递（batch_size 默认 5；gen/rewrite 批次摘要注入下一批）
- ✅ 17 个 skill 补 frontmatter（45/45 有描述）；iCloud 冲突副本归档
- ✅ A1-A5（2026-09-17 第二轮）：RULES-30 硬条款化 15 条 · RULES-10/50 重构（10+10 硬条款）· 参考样式统一索引 REFERENCE-INDEX.md · 16 skills 预算段 · 长文预算豁免贯通（profile+声明+RULES-70 §五）
- ✅ 附带：批量生成内部重试（门禁反馈 ≤3 轮）· pipeline-state 并发锁 PS_LOCK · iCloud 副本去噪 5 个

## Phase 14 · 0 门槛与稳定性（2026-09-17 ✅）

**P14.1 预设工作流（0 门槛）**
- ✅ `templates/presets.json` 7 个预设：GEO 缺口改稿 / 高曝光低 CTR 刷新 / 衰减页刷新 / QA 字段修复 / 封面 alt 补齐 / 例行 QA 扫描 / 多语言批量产出
- ✅ 服务端按真实数据展开（geo gaps / impact / decay / assets / Sanity 过滤 / 主题×语言）；`POST /api/presets/run`（默认 dry-run，审计）
- ✅ 工作台「批量任务 → 预设工作流」chips + 参数弹层（点一下就能跑）

**P14.2 健康与降噪治理（稳定性）**
- ✅ `GET /api/health`（依赖/队列/噪音/级别）+ 总览页健康卡
- ✅ `POST /api/housekeeping/run` + **每日 03:20 自动**：终态条目 >14 天归档 · 僵尸条目标记 · 旧批量任务/会话归档 · citations 轮转（留 200）· 孤儿草稿只报数；dry-run 可预览、幂等、审计
- ✅ 设置页「维护 · 降噪治理」区（预览/立即清理/历史）

**P14.3 上下文预算（防 Agent 越用越噪）**
- ✅ 规则按意图相关性注入（≤4 文件 / ≤1200 字符，必含 RULES-00·70）；库命中 ≤3；会话历史 ≤6 轮
- ✅ 文档 `docs/onboarding.md`（0 门槛 3 步）+ `docs/stability.md`（噪音分类与治理、上下文预算、执行侧稳定性）

## Phase 15 · 熔断与配额（2026-09-17 ✅）

- ✅ T3 熔断：任务级连续失败（默认 5）→ tripped 暂停；致命错误（401/403/key/余额）→ 立即熔断并触发**全局熔断 30 分钟**（worker 停止领单，冷却后半开，可手动解除）；飞书通知 + 审计
- ✅ T5 按用户配额与用量：`run/users-usage.json` 月度计量（tasks/items/tokens/writes，tokens 取真实 usage）；`run/quotas.json` 默认 500/500k/200，admin 不限，逐人覆盖；**建任务前拦截（429）**；设置页配额表 + 一键改配额
- ✅ 实测：错误 Key → 任务 tripped + 全局熔断（reason=HTTP 401）；恢复后解除正常；admin 不受限；dry-run 不计写入

## Phase 16 · 预警与测试（2026-09-17 ✅）

- ✅ T6 配额预警：用量记账时 80% ⚠ / 100% ⛔ 飞书通知（每用户×指标×每月去重）；健康报告 `quota_alerts` → 总览健康卡；设置页配额表 80%/100% 标黄标红
- ✅ T4 自动化测试：`1-4 Dev/tests/test_console_units.py` 21 用例（护栏/熔断/配额/降噪/上下文/预设），纯 stdlib 离线 3 秒；`run-tests.sh` 一键跑；接入 **GATE 6**（失败挡发布）

## Phase 17 · 落地页整页发布（T1，2026-09-17 ✅）

- ✅ `compositePage` 生成：md → composite-v2 版块（hero-split / feature-detail / proof-block / faq / cta-default），自动去重（903 字符合规）
- ✅ 结构校验 `validate_sections`：hero 必备 · 内容版块 ≥2 · FAQ ≤8 · cta 必备 · 文案 200–1200（RULES-70 落地页档）
- ✅ 两种写入模式：`create`（createIfNotExists）· `patch`（ifRevisionID，只改指定字段，更新既有页首选）
- ✅ **安全闸**：compositePage 无草稿态（实测 9,303 篇无 status 字段）→ 真实写入必须显式 `confirm_public`，否则拒绝
- ✅ 批量执行器 `publish_sanity`（blog/composite 通吃）+ 发布通道 UI（文档类型/模式/封面/确认框）+ 5 个新单测（共 26）
- ✅ 落地页闭环（Phase 18）：`landing_refresh` 执行器（读 Sanity 现有页→按落地页结构重写→四门禁+结构校验→**带反馈重试≤3轮**）+ 通用**任务链**（只链通过项，链式发布默认 dry-run）+ 预设「🔁 落地页闭环（改稿→发布）」
- ✅ 闭环实测：ready=True → 自动链出 publish_sanity(patch) → tx 返回；不通过项记 CHAIN-SKIP
- ✅ 顺手修两个环境 bug：新钩子用系统 py3.6（非 ASCII 打印崩→lang-check 恒挂）→ 走 LOVART_PYTHON/venv；校验口径与 quota-check 统一为**词当量**（英文页不再被原始字符数误伤）

## Phase 18 · 落地页闭环（2026-09-17 ✅）

- ✅ `landing_refresh` 执行器：读 Sanity 现有内容 → 落地页结构化重写 → 四门禁 + composite 结构校验 → **内部重试 ≤3 轮（带门禁/结构反馈）**
- ✅ 通用**任务链**：`params.chain` 在父任务完成后自动生成下一步（只链通过门禁的产出；链式发布默认 dry-run；审计 CHAIN-CREATE/CHAIN-SKIP）
- ✅ 预设「🔁 落地页闭环（改稿→发布）」（第 8 个预设）：section/lang/条数 → landing_refresh → publish_sanity(patch)
- ✅ 修复：`publish_sanity` 失败如实标记 failed；patch 用真实 Sanity `_id`（UUID，非 slug）
- ✅ 环境修复：quota-check/lang-check 走 `LOVART_PYTHON`（venv）避免 py3.6 非 ASCII 崩溃；校验口径统一**词当量**
- 实测：**真实闭环上线 2 篇**（`ai-storefront-designer` + `ai-image-to-sketch`）→ 改稿 ready=True → 链出 patch → **tx 确认写入 Sanity**
- ⚠ 暴露 4 个生产 bug（hero.title 变 UUID / slug.current 被覆盖→404 / console.py 被误写 / 前端预存 500）→ 已全部修复（patch 不改 slug / H1 标题提取 / git 恢复 / 确认为预存问题）

## Phase 19 · 知识治理 · Anti-Slop · 三模式（2026-09-18 ✅）

**P19.1 首次真实发布闭环**
- ✅ 2 篇真实工具落地页走完 改稿→四门禁→ready→链出 patch→**tx 真写 Sanity**（`ai-storefront-designer` / `ai-image-to-sketch`）
- ✅ 代价是抓出 4 个生产级 bug 并全部修复：hero.title 变 UUID · **slug.current 被覆盖致前台 404** · console.py 被编辑脚本误写 · 前端 500（经查为 lovart.ai 预存问题，非 MFlow）
- ✅ 沉淀铁律：**patch 模式永远不写 slug**；不要用 `_id` 当 title；大改前先 dry-run 并抽检前台渲染

**P19.2 知识库治理**
- ✅ `GET /api/kb/gaps` 缺口扫描 → 6 个缺口（竞品分析/用户画像/案例库/行业样式/竞品对比/i18n）
- ✅ 清理 67 篇垃圾（34 TDK + 5 iCloud 副本 + 18 重复 docs + 6 一次性文件）→ 归档不删，**136 → 48 篇有效知识**
- ✅ 知识库扩充：OpenClaw 指南 / 18 篇 lovart.ai docs / 海外媒体报道 / 竞品 26 家流量 + 12 词簇零覆盖

**P19.3 Anti-Slop Strong 与语言规则**
- ✅ ANTI_SLOP_STRONG 注入 gen_prompt：29 禁用词 + 8 条 AI 味模式 + 四问自检 + 「删掉后读者不受影响就删」
- ✅ 实测：生成 647 词 blog → 29 禁用词 **0 命中** → hook PASS
- ✅ RULES-20/40/60 硬条款化（0% → 100%）；悬空引用 7→0；Harness 目录瘦身 13→10
- ✅ 关键词情报管道 `GET /api/keyword/intel`（6 源：GSC/Sentinel/竞品词/SERP/GA4/DataWorks）

**P19.4 三模式工作体系**
- ✅ **Pipeline（手动）→ Flow（半自动）→ Loop（自治）**，代表自动化成熟度演进
- ✅ `mode_report()` / `mode_switch()` 项目级切换（记 approvals.log）+ 总览页模式选择器
- ✅ Flow→Loop 升级判断：近 5 次 pass_rate ≥80% 且零熔断 → 建议升级

**P19.5 插件生态与治理面板**
- ✅ plugin_check 扩到 6 类型（source/publisher/gate/transform/analyzer + manifest）；7 个标准插件注册
- ✅ `GET /api/governance` 治理面板 API（知识库缺口 + Skills 覆盖 + 规则健康 + 语言/配额/Anti-Slop + 自我进化）
- ✅ Skills 覆盖审计：发现 topics/solutions/products/news 4 类无专属生成 skill（靠 landing-page 泛化）
- ✅ 48/48 skill 有 frontmatter 描述；补 3 个 publish skill
- ✅ UI：116 处 alert 换 Toast + 暗色模式 11 条规则

## Phase 20 · Agent 化与可用性（2026-09-19 ✅ 93 commits）

**P20.1 Agent 底座（P0）**
- ✅ Agent 记忆接线 + 会话压缩 / 上下文可视化 + 角色 Profile + 失败自愈重规划
- ✅ **Agent 工具循环 + 执行画布（Run）**：能力不输本地 agent，且全程可视、可取消、可重试
- ✅ 会话持久化 + Cloudflare 缓存旁路（复用 OpenFlow CF 凭证）

**P20.2 P1 六项**
- ✅ P1-1 多语言覆盖盘点与补齐（`/api/multilang/coverage|fill`）
- ✅ P1-1b **记忆审阅 UI**：288 条事实 / 98 实体可「更正」或「标为过时」，叠加 `run/memory-overrides.json`，Agent 立即生效
- ✅ P1-2 执行器心跳（`run/worker-heartbeat.json`，5s）+ 恢复可解释 + 顶栏状态灯
- ✅ P1-3 **审阅子代理**：与规划器共享上下文 · 必须引依据（RULES-xx/skill/记忆§）· **只判断不动笔** · **只能收紧** · 不确定即 pass。block 时执行需二次确认
- ✅ P1-4 内链建议批量化（只读分析 + markdown 报告 + 按站点语言的 token 索引，20 项从"卡住"降到 <8s）
- ✅ P1-6 插件市场一键安装 + 全 5 类可执行类型 + 启停 + Skills 目录浏览

**P20.3 统一执行方式**
- ✅ 任务 / 批量 / 编排 / Agent / 自动化 五种入口**可自由互转**：`POST /api/work/convert`

**P20.4 可用性七件套**
- ✅ 全局命令面板 ⌘K（含 ★收藏 + 最近使用）· 全局快捷键 `g+字母` · 帮助浮层
- ✅ 变更审计 + 一键回滚（`run/audit-changes.jsonl`，字段级；发布类不自动回滚）
- ✅ 统一收件箱（系统阻断/待办/失败任务/待授权发布/待执行方案）+ nav 角标
- ✅ 失败摘要（按原因归类 + 人话建议）+ 一键重试全部失败项
- ✅ 空状态 CTA 全覆盖（17+ 处）· 窄屏/移动端适配 · 出站 Webhook（可选 HMAC）

**P20.5 RAG 底座**
- ✅ 可插拔 embedding（配了走远程，未配走本地 TF-IDF）+ 混合检索 RRF + `semantic_search` 工具
- ✅ 知识中台可视化重构（左筛选 + 右宽结果 + 检索底座状态卡）

## Phase 21 · 自动化剧本 · 开放 · 自愈自进化（2026-09-20 ✅）

**P21.1 Playbook 自动化剧本**
- ✅ 多步 + 条件 `guard` + 触发器（schedule / event / manual），执行走 Run 画布；`run/playbooks.json` + 6 个模板
- ✅ **分支 if/else**：步骤 `id` + `on_true`/`on_false`/`next` 取 `next|stop|goto:ID`（**仅前向，防死循环**）；未走分支标 skipped
- ✅ **步骤级重试/超时**：`retry_max`/`retry_delay_sec`/`timeout_min`（重试排在 run_replan 之前）
- ✅ **单剧本硬闸** `limits{每日次数/并发/冷却/步数}`（默认 50/2/5/12），覆盖手动/定时/事件全部触发路径，被拦发 `playbook.blocked`
- ✅ **僵尸 run 回收** `run_gc()`：>30 分钟 running 且批量任务已不在跑 → 标 failed（执行器每 5 分钟巡检）
- ✅ 可视化编辑器（拖拽 + ↑↓ 排序、类型化字段、触发器、硬闸）+ **试运行预览**（零副作用，先看要动多少条）
- ✅ **统一**：automations 合并进 Playbook（单一"定时工作"模型），幂等迁移 + 兼容层 + 单一调度链路

**P21.2 事故与护栏（同日发生并修复）**
- ⚠→✅ **剧本每 5s 重复触发**：`playbook_run` 用带校验的 `playbook_save` 写 `last_run` 被拒 → 从未落盘 → 每周期都判定"到期未运行"。修复 `playbook_patch` 局部更新 + tick 最小间隔 10 分钟；清理 11 个重复任务
- ⚠→✅ **系统配额自锁**：系统执行者按普通用户计配额被 500 条上限打满 → health=bad 且自动化被自己的配额拒绝。修复 `SYSTEM_ACTORS` 豁免

**P21.3 开放接入（MCP）**
- ✅ `1-4 Dev/scripts/mcp_server.py` 纯标准库 stdio JSON-RPC，**17 个工具**；动作类工具**强制 dry-run**
- ✅ HTTP 传输 `POST /api/mcp`（JSON-RPC，协议 2025-06-18）+ `GET /api/mcp/sse`（有界心跳）——远程客户端无需本地进程
- ✅ 设置页「开放接入」卡 + `docs/mcp.md`；安全边界：**只读 + dry-run，写生产库必须真人会话**

**P21.4 自愈与自我进化**
- ✅ `selfcheck_autofix()` 一键修复带安全动作的自检项（熔断/卡住任务/维护/RAG 索引/失败重试）；`selfheal_tick()` 每 ~10 分钟静默自愈（仅白名单）
- ✅ `learn_from_failures()` 失败按类别聚合 → 学习项落 `run/learnings.json`；`apply|ignore`，**review 类拒绝自动应用**
- ✅ **OPC** `POST /api/playbooks/enable_recommended` 一键装启 4 个推荐剧本

**P21.5 实测澄清（能力边界）**
- ✅ **DeepSeek 无 embeddings**（`/embeddings` 对任何模型 404）→ 改用**词法召回 + LLM 重排**，无需新厂商
- ✅ 邮件改走本机 postfix/sendmail（零凭证），SMTP 降级为可选增强
- ✅ RAG 语料补入 harness RULES + Skills（1,430 → **1,538 块**）——此前质量类提问召不回规则

## Phase 22 · 开工预热（2026-09-20 ✅）

- ✅ `1-4 Dev/scripts/warmup.py`（纯标准库）：用**真实只读 / dry-run** 动作，把 Lovart Global 六个板块的历史记录、findings、缺口清单、报告一次性跑出来，让后台开箱即有内容而非满屏空状态
- ✅ 安全边界：**不提供 `--real` 开关**，写生产库仍走人工授权；幂等；skip/fail 如实记录，**不补数**
- ✅ 报告落 `run/logs/warmup-*.md`；文档 `docs/warmup.md`；已纳入 `deploy/sync.sh`
- ✅ 顺修：**单测污染生产审计日志**——`import console` 即写 `run/approvals.log`（实测一天 92 条噪音）。`RUN_DIR` 改为可由 `MFLOW_RUN_DIR` 覆盖，`run-tests.sh` 强制指向临时目录，并补 3 个隔离用例（**42/42 绿**）

## 原则

1. 文件即状态：不引入数据库也能跑，规模化时才换 PG（接口已预留）
2. 发布人工授权是不可协商的边界
3. 每个新能力必须让未配置的新用户 5 分钟内看到效果
4. 错误只犯一次：踩坑必须沉淀为 hook 检查项或 RULES 条款
