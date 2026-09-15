# Lovart MFlow — codebox 部署 PRD

> **版本**: v1.0
> **日期**: 2026-07-23
> **目标平台**: codebox (内网 vibecoding 平台, `http://172.16.16.203:8080`)
> **项目名**: `lovart-mflow`

---

## 一、背景

Lovart MFlow 是一套全自动内容营销系统,目前完全运行在本地 macOS。现需部署到 codebox 平台,实现:

1. **7×24 可用**:定时任务不依赖本机开机
2. **多人协作**:团队成员通过飞书登录即可使用
3. **AI Agent 可调**:Claude Code / Cursor 通过 API Key 调用
4. **可观测**:Pipeline 状态、质量门禁、路由决策实时可见

---

## 二、架构设计

### 2.1 项目结构 (codebox mono-repo 分支)

```
lovart-mflow/
├── start.sh                    # 平台进程管理契约
├── go.mod                      # Go 模块
├── cmd/
│   └── server/
│       └── main.go             # HTTP 入口 (监听 $PORT)
├── internal/
│   ├── api/                    # HTTP handlers
│   │   ├── pipeline.go         # /api/pipeline/* (状态机 CRUD)
│   │   ├── router.go           # /api/router/* (路由决策)
│   │   ├── hooks.go            # /api/hooks/* (质量检查)
│   │   ├── skills.go           # /api/skills/* (Skill 管理)
│   │   └── health.go           # /health
│   ├── store/                  # MongoDB 数据层
│   │   ├── pipeline.go         # pipeline_items + events
│   │   ├── skills.go           # skills registry
│   │   ├── profiles.go         # profiles registry
│   │   └── decisions.go        # router decisions
│   └── engine/                 # 业务逻辑
│       ├── pipeline.go         # 状态机转换校验
│       ├── router.go           # 路由决策引擎
│       └── hooks.go            # Hook 执行器 (调 Python)
├── scripts/                    # Python/Shell 脚本 (从本地迁移)
│   ├── hooks/
│   │   ├── pre-write-check.sh
│   │   ├── post-write-check.sh
│   │   ├── pre-import-check.sh
│   │   └── post-generation-check.sh
│   ├── pipeline_state.py
│   ├── router.py
│   └── governance_check.py
├── skills/                     # SKILL.md 文件 (从 canonical 迁移)
│   ├── lovart-blog-signal-writer/
│   ├── lovart-landing-page/
│   ├── lovart-content-quality-gates/
│   └── ... (51 个)
├── web/                        # 前端 (无构建)
│   ├── index.html              # Dashboard
│   ├── pipeline.html           # Pipeline 状态板
│   ├── router.html             # 路由决策表
│   └── static/
│       ├── app.js
│       └── style.css
└── config/
    ├── rules/                  # RULES-00~60.md
    ├── profiles/               # 7 个 profile SOUL.md
    └── decisions.json          # 23 条路由决策
```

### 2.2 API 设计

#### Pipeline 状态机

```
GET    /api/pipeline/items              # 列表 (支持 ?phase=&stage= 过滤)
GET    /api/pipeline/items/{id}         # 详情
POST   /api/pipeline/items              # 创建 (upsert)
PATCH  /api/pipeline/items/{id}         # 更新字段
POST   /api/pipeline/items/{id}/advance # 推进到下一阶段
POST   /api/pipeline/items/{id}/run     # 记录 QA 结果
GET    /api/pipeline/items/{id}/check   # 检查是否可推进
GET    /api/pipeline/events             # 事件日志
GET    /api/pipeline/summary            # 汇总统计
GET    /api/pipeline/next               # 建议下一个待处理 item
```

#### Router 决策

```
POST   /api/router/decide               # 给定 stage + scenario → 返回 profile + skills
GET    /api/router/matrix               # 完整决策表 (23 条)
GET    /api/router/profiles             # Profile 注册表 (6 个)
POST   /api/router/validate             # 校验决策表完整性
```

#### Hooks 质量检查

```
POST   /api/hooks/pre-write             # 文件名/路径/frontmatter/占位符
POST   /api/hooks/post-write            # H2 密度/词数/fluff/AI 自介
POST   /api/hooks/pre-import            # pipeline-state/qa BLOCKs/日期双写
POST   /api/hooks/post-generation       # 图片 404/SEO 字段/质量自降
POST   /api/hooks/governance            # 脚本合规检查
```

#### Skills 管理

```
GET    /api/skills                      # 列表 (支持 ?category= 过滤)
GET    /api/skills/{name}               # 详情 (SKILL.md 内容)
GET    /api/skills/{name}/references    # 引用文件列表
POST   /api/skills/sync                 # 触发 profile 同步
```

#### Dashboard

```
GET    /                                # 主仪表盘
GET    /pipeline                        # Pipeline 状态板 (Board view)
GET    /router                          # 路由决策表
GET    /hooks                           # 质量门禁历史
GET    /skills                          # Skill 浏览器
```

### 2.3 MongoDB Schema (TABLE_PREFIX=lovart_)

```javascript
// pipeline_items
{
  _id: "blog-magnific-vs-lovart-2026-07",
  category: "blog",
  target_type: "blog",
  stage: "S5-published",
  phase: "SHIP",
  agent: "lovart-creation",
  skill: "lovart-blog-signal-writer",
  artifact_path: "1-3 GenFlow/...",
  qa: { l1_block: 0, l2_block: 0, l7_block: 0, last_run: "2026-07-22T...", fix_count: 0 },
  publish: { sanity_id: null, imported_at: null, status: null },
  fix_count: 0,
  created_at: "2026-07-22T...",
  updated_at: "2026-07-22T..."
}

// pipeline_events (append-only)
{
  _id: ObjectId,
  ts: "2026-07-22T...",
  event: "advance",
  item_id: "blog-magnific-vs-lovart-2026-07",
  from: "S3-draft",
  to: "S3-done",
  reason: "7690 words, all gates passed",
  metadata: {}
}

// skills
{
  _id: "lovart-blog-signal-writer",
  description: "Lovart Blog 唯一创作 skill...",
  category: "lovart",
  owner_profile: "lovart-creation",
  status: "active",
  path: "skills/lovart-blog-signal-writer/SKILL.md",
  last_used: "2026-07-22T..."
}

// profiles
{
  _id: "lovart-creation",
  model: "deepseek-v4-pro",
  work_line: "S3-content-production",
  owns_stages: ["S0-todo", "S3-creating", "S3-draft", "S3-done"],
  key_skills: ["lovart-blog-signal-writer", "lovart-landing-page", ...],
  soul_md: "...",
  status: "active"
}

// decisions
{
  _id: ObjectId,
  stage: "S3-draft",
  scenario: "l1_fluff",
  profile_target: "lovart-quality",
  action: "reroute",
  skills: ["lovart-anti-slop"],
  reason: "L1 fluff → quality profile specializes in slop detection"
}
```

### 2.4 前端 Dashboard

**主仪表盘** (`/`):
- Pipeline 状态概览: QUEUE / CREATE / REVIEW / SHIP / FINAL 各多少 item
- 最近事件: 最近 10 条 advance / qa-run / import 事件
- 质量门禁: 最近 24h pass/fail 率
- 快捷操作: "下一个该做什么"按钮

**Pipeline 状态板** (`/pipeline`):
- Kanban 视图: 按 stage 分列 (S0-todo / S3-creating / S4-qa / S5-importing / ...)
- 每个卡片显示: id / category / agent / 最后更新时间
- 点击卡片: 详情 + 历史 + 操作按钮 (advance / run / check)

**路由决策表** (`/router`):
- 23 条决策的表格视图
- 每行: stage / scenario / profile_target / action / skills
- 实时 "Test Decision" 输入框: 输入 stage + scenario → 看路由结果

---

## 三、迁移步骤

### Phase 1: 项目初始化 (1 天)

```bash
# 1. 在 codebox 创建项目
curl -H "Authorization: Bearer $CODEBOX_API_KEY" \
  -X POST http://172.16.16.203:8080/api/projects \
  -d '{"name":"lovart-mflow"}'

# 2. 初始化 Go 项目
curl -H "Authorization: Bearer $CODEBOX_API_KEY" \
  -X POST http://172.16.16.203:8080/api/projects/lovart-mflow/exec \
  -d '{"cmd":"rm -rf cmd web run logs && mkdir -p cmd/server internal/api internal/store internal/engine scripts hooks skills config/rules config/profiles web/static"}'

# 3. 写 go.mod + main.go + start.sh
# (通过 exec 逐个写入)
```

### Phase 2: 核心 API (3 天)

1. **Pipeline API** (`/api/pipeline/*`)
   - 从 `pipeline_state.py` 移植状态机逻辑到 Go
   - MongoDB 替换 JSON 文件
   - 保留相同的 12 stage + 4 phase + transition 规则

2. **Router API** (`/api/router/*`)
   - 从 `router.py` 移植 23 条决策到 Go
   - 决策表存 MongoDB `lovart_decisions`

3. **Hooks API** (`/api/hooks/*`)
   - Go handler 调 `exec` 跑 Python/Shell 脚本
   - 解析 exit code + stdout → 返回 JSON 结果

### Phase 3: 前端 Dashboard (2 天)

1. Pipeline 状态板 (Kanban)
2. 路由决策表
3. 质量门禁历史

### Phase 4: Skills 迁移 (1 天)

1. 复制 51 个 SKILL.md 到 `skills/` 目录
2. 复制 4 个 hook 脚本到 `scripts/hooks/`
3. 复制 pipeline_state.py / router.py / governance_check.py 到 `scripts/`
4. 通过 `exec` 写入文件

### Phase 5: 定时任务 (1 天)

通过 `exec` 跑 cron-like 脚本:
- Dream consolidation (daily)
- Sentinel data pull (daily)
- Notion sync (weekly)
- Profile sync (on skill update)

### Phase 6: 权限配置 (0.5 天)

```
项目 grants:
  /** + 任意登录用户        → 公司内公开 Dashboard
  /api/** + owner           → API 操作权限
  /api/hooks/** + quality   → QA 专用
  /api/pipeline/** + creator → 创作专用
```

---

## 四、API Key 管理

```
用途                  生成者        权限范围
──────────────────────────────────────────────
AI Agent (Claude)     owner        全部 API
AI Agent (Cursor)     owner        全部 API
Dashboard 前端        owner        只读 API
Cron 触发             owner        pipeline + hooks
```

安全提示:
- API Key 权限 = 生成者权限
- 不写入公开代码 / 群消息 / README
- 泄露即删 + 重新生成

---

## 五、验证清单

- [ ] Pipeline API: CRUD + 状态转换校验 + 事件日志
- [ ] Router API: `POST /decide` 返回正确 profile
- [ ] Hooks API: 4 个 hook 全部返回正确 exit code
- [ ] Dashboard: Pipeline 状态板 + 路由决策表
- [ ] Skills: 51 个 SKILL.md 全部可读
- [ ] 凭证: Sanity / GSC / Notion API key 可用
- [ ] 权限: owner / creator / quality 角色隔离
- [ ] AI Agent: Claude Code 通过 API Key 调用成功

---

## 六、里程碑

| 阶段 | 时间 | 交付物 |
|------|------|--------|
| Phase 1 | Day 1 | 项目创建 + Go 骨架 |
| Phase 2 | Day 2-4 | Pipeline/Router/Hooks API |
| Phase 3 | Day 5-6 | Dashboard 前端 |
| Phase 4 | Day 7 | Skills 迁移 |
| Phase 5 | Day 8 | 定时任务 |
| Phase 6 | Day 8.5 | 权限配置 + 验证 |

**总工期: 8.5 天**
