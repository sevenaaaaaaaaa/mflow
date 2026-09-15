# MFlow 模块扩展指南（新模块 · CMS 打通 · 数据源 · 自我迭代）

> MFlow 的每个能力都是一个可组合模块。本文讲四件事：怎么加新模块、怎么接 CMS、怎么接新媒体数据源、系统怎么自我迭代。

---

## 一、模块的四个注册点

一个完整模块 = 以下一至多项的组合，全部是"文件即注册"：

| 注册点 | 位置 | 作用 |
|--------|------|------|
| Skill | `1-1 Harness/Skills/<组>/<名>/SKILL.md` | 该模块的 SOP、提示词、检查清单（agent 与工作台共用） |
| 知识源 | `1-1 Harness/11-knowledge` 或工作台 `console.py KNOWLEDGE_SOURCES` | 模块依赖的参考知识，进知识中台索引 |
| 质量钩子 | `1-4 Dev/scripts/hooks/*.sh` | 模块产出前的硬约束检查 |
| 工作流定义 | 工作台 `console.py WORKFLOW_MAP` | 阶段链 / 角色 / Skills / 知识源的可视化地图 |

新增后跑 `python3 1-4 Dev/scripts/harness_sync.py` 同步到各 agent 运行时，并在
`1-1 Harness/09-scripts/TOOLS-REGISTRY.md` 注册新脚本（防重复创建）。

## 二、如何接入新的媒体 / 线上数据源（检验内容效果）

数据源分两类：

**效果类（发布后回看）**——挂进 Trident 步骤注册表 `console.py TRIDENT_STEPS`：

```python
{"id": "gsc", "name": "GSC 日拉", "cmd": [PYTHON, ".../gsc_fetch.py", "--daily"], "desc": "..."},
# 新增一个源 = 加一行 + 写一个拉数脚本（OAuth 凭证放 credentials/，git-ignore）
{"id": "reddit-ads", "name": "Reddit 广告效果", "cmd": [PYTHON, "1-4 Dev/scripts/sources/reddit_ads.py"], "desc": "..."},
```

脚本约定：输出 JSON 到 `$LOVART_LOCAL_DEV_ROOT/Output/Data Ingestion/`，文件名含日期。
工作台「数据管线 Trident」页会自动出现新步骤与产出健康度。

**舆情类（发布前监测）**——参考 `1-4 Dev/scripts/sentinel/sources/*.py` 的 collect() 协议：
返回 dict、单源失败不阻塞其他源，加入 `collect.py` 的 source 列表即被每日 22 源管线带动。

效果检验的标准问法："这条外链/这篇文章带来了多少点击？"——把发布外链表
（分发页 CSV 导出）与 GSC 页面数据按 URL 关联即是 MVP 归因。

## 三、如何与 CMS / 技术栈打通

发布环节做成适配器接口（与 Lovart 的 Sanity 实现解耦）：

```python
# 1-4 Dev/scripts/publish_adapters/my_cms.py
def publish(item: dict, cfg: dict) -> dict:
    """item 含 id/title/body_md/lang/meta；返回 {ok, url, cms_id}"""
    ...
```

- **Sanity（参考实现）**：见 `lovart-sanity-publish` skill——NDJSON + `--missing` 增量导入 + preflight BLOCK=0 前置
- **WordPress**：REST `POST /wp-json/wp/v2/posts`（Application Passwords），参考 OpenFlow 项目的 wp 集成
- **通用 Webhook**：POST item JSON 到你的后端，返回 `{url}` 即回写外链表
- 工作台"分发队列"读的是 `queue/published.json`——适配器成功后按既有 schema 追加，
  外链 CSV 导出自动带上新渠道

铁律不变：**发布动作永远停在人工授权之后**，工作台不提供一键外发。

## 四、如何像 OpenFlow 一样自我迭代

OpenFlow 的迭代飞轮 = 版本化交付 + 使用数据回流。MFlow 对应四件事：

1. **VERSION + 变更日志**：根 `VERSION` 一行版本号；每轮功能在 `CHANGELOG.md` 追加（含动机与效果数字）
2. **运行数据回流**：`run/llm-usage.jsonl`（成本）、`events.jsonl`（吞吐）、质检 BLOCK 率（质量）——月度回顾这三条曲线，找到该优化的环节
3. **Lessons 机制**：每轮会话写 session log（`11-knowledge/sessions/`），踩坑沉淀为 RULES 或 hook 新增检查项——自我迭代的本质是"错误只犯一次"
4. **Demo 驱动的验收**：每个新能力必须让"未配置的新用户"也能在 5 分钟内看到效果（本工作台的 onboarding 即按此标准迭代）

## 五、看板与内容日历（协作模型）

- 看板 = 执行视图（`run/tasks.json`，支持拖拽、负责人、截止日、操作者署名）
- 日历 = 资产视图（`1-3 GenFlow/Content Calendar/`）
- 打通：日历页「→ 加入看板」把文章变成卡片（卡片带 🔗 关联），卡片流转即内容生产进度；
  多人协作 MVP = 共享密码 + 卡片署名，正式账号体系在 ROADMAP Phase 3
