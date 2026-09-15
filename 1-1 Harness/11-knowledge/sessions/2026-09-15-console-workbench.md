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
