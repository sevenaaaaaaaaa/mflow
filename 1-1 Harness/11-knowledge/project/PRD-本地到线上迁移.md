# Lovart MFlow — 本地到线上迁移 PRD

> **版本**: v1.0
> **日期**: 2026-07-23
> **作者**: Lovart 内容工厂团队
> **状态**: Draft — 待研发评审

---

## 一、背景

Lovart MFlow 是一套基于 Obsidian + Hermes Agent 的全自动内容营销系统，目前**完全运行在本地 macOS**上。核心组件包括:

- **51 个 AI Skill** (SKILL.md + Python/Shell 脚本)
- **7 个 Agent Profile** (Hermes 档案，各装不同 Skill 子集)
- **4 个质量 Hook** (pre-write / post-write / pre-import / post-generation)
- **1 个状态机** (12-stage pipeline-state.json)
- **1 个路由器** (23 条决策，6 Profile 自动路由)
- **5 个定时任务** (launchd: dream / sentinel / qa-memo / sync-local-dev / sync-from-notion)
- **3 个同步脚本** (Notion ↔ Obsidian / Local Dev ↔ Obsidian / Profile 同步)
- **1 个知识图谱** (90 实体 + 88 边 + 图查询 CLI)
- **1 个治理检查器** (governance_check.py 6-gate)

**现状问题**:

1. **单机瓶颈**: 所有组件绑定在一台 macOS 上，无法多人协作，无法 7×24 运行
2. **手动触发多**: 虽然有 launchd 定时任务，但大部分工作流需要人工在终端操作
3. **无可观测性**: 管线状态、Hook 执行结果、Skill 调用记录散落在本地文件，无法统一监控
4. **无版本管理**: Skills / Rules / Hooks 虽然在 Obsidian vault，但没有 Git 管理的 CI/CD 流程
5. **凭证分散**: Sanity token / GSC API / GA4 / Bing / Notion API / 飞书 / DEV.to / Medium 等 12+ 凭证散落在 `~/.config/` 和 `.env` 文件

---

## 二、目标

| 维度 | 现状 | 目标 |
|------|------|------|
| 运行环境 | 单机 macOS | 云端容器化 (Docker / K8s) |
| 可观测性 | 本地文件 | Dashboard + 日志 + 指标 |
| 协作 | 单人 | 多人并行，角色隔离 |
| 定时任务 | launchd (本机) | 云端 Cron (Airflow / Temporal / Hermes Cron) |
| 凭证管理 | 本地文件 | Vault / AWS Secrets Manager / 环境变量 |
| 版本管理 | 手动 copy | Git + CI/CD |
| 触发方式 | 人工 + launchd | 事件驱动 (GSC 变化 / Sanity webhook / Cron) |

---

## 三、组件清单与迁移策略

### 3.1 可直接迁移的组件 (低风险)

| 组件 | 当前形态 | 迁移形态 | 工作量 |
|------|---------|---------|--------|
| **Skills** (51 个 SKILL.md) | `~/.hermes/skills/lovart/` | Git repo → Docker image | 1 天 |
| **Hooks** (4 个 .sh) | `1-4 Dev/scripts/hooks/` | 容器内可执行脚本 | 0.5 天 |
| **Pipeline State** | `pipeline_state.py` + JSON | 云数据库 (PostgreSQL / DynamoDB) | 2 天 |
| **Router** | `router.py` + 23 条决策 | 微服务 API 或 Lambda | 1 天 |
| **Governance Check** | `governance_check.py` | CI/CD pipeline pre-commit hook | 0.5 天 |
| **TOOLS-REGISTRY.md** | Markdown 文件 | 数据库表 + API | 1 天 |
| **Rules** (7 个 RULES-*.md) | Obsidian vault | Git repo + 版本管理 | 0.5 天 |

### 3.2 需要重构的组件 (中风险)

| 组件 | 当前形态 | 迁移形态 | 工作量 | 风险点 |
|------|---------|---------|--------|--------|
| **Notion 同步** | 本地 Python 脚本 | 云端定时任务 | 1 天 | API rate limit |
| **Local Dev 同步** | 本地 bash 脚本 | 不迁移(保持本地) | 0 | N/A |
| **Profile 同步** | 本地 bash 脚本 | 容器内一次性任务 | 0.5 天 | 路径变更 |
| **Knowledge Graph** | YAML + CLI | Neo4j / PostgreSQL | 3 天 | 查询性能 |
| **Dream / Memory** | 本地脚本 + launchd | 云端定时任务 | 1 天 | 路径变更 |

### 3.3 需要重新设计的组件 (高风险)

| 组件 | 当前形态 | 迁移形态 | 工作量 | 风险点 |
|------|---------|---------|--------|--------|
| **Hermes Agent** | 本地 CLI + 7 Profiles | 云端 Agent 服务 (OpenAI API / Anthropic API) | 5 天 | Prompt 携带方式、Skill 加载机制 |
| **Sanity Import** | 本地 CLI (`sanity dataset import`) | 云端 API 调用 | 2 天 | NDJSON 流式处理 |
| **GSC/GA4/Bing 数据拉取** | 本地 Python 脚本 | 云端定时任务 | 2 天 | OAuth refresh token |
| **Sentinel 舆情** | 本地 Python 脚本 | 云端定时任务 | 1 天 | 数据源 API 变更 |
| **多平台分发** | 本地 Python 脚本 | 云端定时任务 | 1 天 | 平台 API 变更 |

---

## 四、技术架构

### 4.1 目标架构图

```
┌─────────────────────────────────────────────────────────┐
│                    用户界面层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Web Dashboard │  │ Notion   │  │ CLI      │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    API 网关层                              │
│  ┌──────────────────────────────────────────────┐      │
│  │ FastAPI / Express (统一入口)                    │      │
│  │ - /api/pipeline/* (状态机 CRUD)                │      │
│  │ - /api/router/* (路由决策)                      │      │
│  │ - /api/hooks/* (质量检查)                       │      │
│  │ - /api/skills/* (Skill 管理)                   │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    业务逻辑层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Pipeline  │  │ Router   │  │ Hooks    │              │
│  │ State Mgr │  │ Engine   │  │ Executor │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Governance│  │ Knowledge│  │ Dream    │              │
│  │ Checker   │  │ Graph    │  │ Engine   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    数据层                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ PostgreSQL│  │ Redis    │  │ S3/MinIO │              │
│  │ (状态/配置)│  │ (缓存)   │  │ (文件)   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    外部集成层                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│  │Sanity│ │ GSC  │ │ GA4  │ │Bing  │ │Notion│        │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘        │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│  │飞书  │ │DEV.to│ │Medium│ │GitHub│ │WP    │        │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘        │
└─────────────────────────────────────────────────────────┘
```

### 4.2 核心数据库 Schema

```sql
-- Pipeline Items
CREATE TABLE pipeline_items (
    id VARCHAR(80) PRIMARY KEY,
    category VARCHAR(20),
    target_type VARCHAR(20),
    stage VARCHAR(20) NOT NULL,
    phase VARCHAR(10) NOT NULL,
    agent VARCHAR(50),
    skill VARCHAR(50),
    artifact_path TEXT,
    qa_l1_block INT,
    qa_l2_block INT,
    qa_l7_block INT,
    qa_last_run TIMESTAMP,
    qa_fix_count INT DEFAULT 0,
    sanity_id VARCHAR(50),
    fix_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Events (append-only)
CREATE TABLE pipeline_events (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMP NOT NULL,
    event VARCHAR(20) NOT NULL,
    item_id VARCHAR(80) REFERENCES pipeline_items(id),
    from_stage VARCHAR(20),
    to_stage VARCHAR(20),
    reason TEXT,
    agent VARCHAR(50),
    metadata JSONB
);

-- Skills Registry
CREATE TABLE skills (
    name VARCHAR(64) PRIMARY KEY,
    description TEXT,
    category VARCHAR(30),
    owner_profile VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP
);

-- Profiles
CREATE TABLE profiles (
    name VARCHAR(50) PRIMARY KEY,
    model VARCHAR(50),
    work_line VARCHAR(50),
    owns_stages TEXT[],  -- array of stage names
    soul_md TEXT,        -- SOUL.md content
    status VARCHAR(20) DEFAULT 'active'
);

-- Decision Matrix (router)
CREATE TABLE decisions (
    id SERIAL PRIMARY KEY,
    stage VARCHAR(20) NOT NULL,
    scenario VARCHAR(30) NOT NULL,
    profile_target VARCHAR(50),
    action VARCHAR(30),
    skills TEXT[],  -- array of skill names
    reason TEXT,
    UNIQUE(stage, scenario)
);
```

---

## 五、迁移步骤

### Phase 1: 基础设施 (1-2 周)

1. **Git repo 初始化**
   - `lovart-mflow` monorepo: skills/ + hooks/ + rules/ + scripts/ + configs/
   - CI/CD: GitHub Actions → Docker build → push to registry

2. **容器化**
   - Base image: Python 3.11 + Node.js 20 + Sanity CLI
   - 环境变量: `LOVART_RESOURCE_ROOT` / `LOVART_LOCAL_DEV_ROOT` / Sanity token 等
   - Volume mount: `1-3 GenFlow/` (创作产物) / `1-2 Insight/` (情报数据)

3. **数据库初始化**
   - PostgreSQL: pipeline_items + events + skills + profiles + decisions
   - Redis: session state cache
   - S3/MinIO: artifact storage (blog drafts, landing page JSON)

### Phase 2: 核心服务 (2-3 周)

4. **Pipeline State API** (`/api/pipeline/*`)
   - CRUD for pipeline_items
   - Event logging
   - Stage transition validation (same logic as `pipeline_state.py`)

5. **Router API** (`/api/router/*`)
   - `POST /decide` — same logic as `router.py decide`
   - `GET /matrix` — decision table
   - `GET /profiles` — profile registry

6. **Hooks API** (`/api/hooks/*`)
   - `POST /pre-write-check` — file validation
   - `POST /post-write-check` — quality check
   - `POST /pre-import-check` — import validation
   - `POST /post-generation-check` — unified quality gate

### Phase 3: 定时任务 (1 周)

7. **Cron Jobs**
   - Dream consolidation (daily 02:30)
   - Sentinel data pull (daily 08:00)
   - Notion sync (weekly Sunday 03:00)
   - Local Dev sync (weekly Sunday 03:00)
   - Profile sync (on skill update)

8. **Event-Driven Triggers**
   - GSC data change → auto-create pipeline item
   - Sanity webhook → auto-update pipeline state
   - Skill update → auto-sync to all profiles

### Phase 4: 可观测性 (1 周)

9. **Dashboard**
   - Pipeline state visualization (Board view)
   - Quality gate pass/fail rates
   - Skill usage metrics
   - Profile routing decisions

10. **Logging**
    - Structured JSON logs
    - Error alerting (PagerDuty / Slack)
    - Performance metrics (latency, throughput)

### Phase 5: 迁移验证 (1 周)

11. **Parallel Run**
    - 云端和本地同时运行 1 周
    - 对比输出一致性
    - 验证定时任务触发

12. **Cutover**
    - 本地停止定时任务
    - 云端接管全部工作流
    - 保留本地作为 fallback 1 个月

---

## 六、凭证管理

| 凭证 | 当前位置 | 迁移目标 |
|------|---------|---------|
| Sanity token | `~/.config/sanity/config.json` | AWS Secrets Manager |
| GSC API | OAuth refresh token | AWS Secrets Manager |
| GA4 API | OAuth refresh token | AWS Secrets Manager |
| Bing API | env var | AWS Secrets Manager |
| Notion API | `~/.config/notion/api_key` | AWS Secrets Manager |
| 飞书 webhook | env var | AWS Secrets Manager |
| DEV.to API | env var | AWS Secrets Manager |
| Medium API | env var | AWS Secrets Manager |
| GitHub token | env var | AWS Secrets Manager |
| WordPress | wp-auth.local.env | AWS Secrets Manager |

---

## 七、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| Sanity API 变更 | 所有发布流程停摆 | Pin Sanity CLI 版本 + 监控 API 版本 |
| GSC OAuth token 过期 | 数据拉取失败 | 自动 refresh token + 告警 |
| 云端 Agent 质量下降 | 内容质量降低 | A/B 测试 + 质量门禁兜底 |
| 路径变更导致脚本失败 | 流程中断 | 环境变量统一 + 容器内路径固定 |
| 多人同时编辑同一 item | 状态冲突 | Pipeline state 加乐观锁 |

---

## 八、里程碑

| 阶段 | 时间 | 交付物 |
|------|------|--------|
| Phase 1 | Week 1-2 | Git repo + Docker image + DB schema |
| Phase 2 | Week 3-5 | Pipeline/Router/Hooks API |
| Phase 3 | Week 6 | Cron jobs + event triggers |
| Phase 4 | Week 7 | Dashboard + logging |
| Phase 5 | Week 8 | Parallel run + cutover |

---

## 九、成功指标

| 指标 | 现状 | 目标 |
|------|------|------|
| 单篇 Blog 从创作到发布 | 2-4 小时 (手动) | <30 分钟 (自动) |
| 质量门禁通过率 | ~70% | >90% |
| 定时任务成功率 | ~80% (launchd) | >99% (云端 Cron) |
| 多人并行能力 | 1 人 | 3-5 人 |
| 7×24 可用性 | 否 (本机关机) | 是 |
| 可观测性 | 无 | 完整 Dashboard |
