# 分发架构：主站 + 国内 + 海外 API + 爱贝壳

```
lovart.ai（SSOT）
       ↓ 延迟 7–14 天
Agent 写摘要稿 → drafts/ → preflight
       ↓
dispatch-publish.js
  ├─ 国内 Wechatsync     15 平台（见 README）
  ├─ 海外 API 脚本       DEV.to · GitHub Discussions · Blogger
  └─ 爱贝壳（免费 3 槽）  Medium · X
```

栈定义：`config/stack.json` · 平台路由：`config/platforms.json`

---

## 主轨 1 — 国内：Wechatsync

**触发**：`dispatch-publish.js` 的 `cn` 清单项。

| 平台 | wechatsync id |
|------|---------------|
| 知乎 | `zhihu` |
| 百家号 | `baijiahao` |
| 掘金 | `juejin` |
| 头条号 | `toutiao` |
| CSDN | `csdn` |
| 豆瓣 | `douban` |
| 思否 | `segmentfault` |
| 简书 | `jianshu` |
| 什么值得买 | `smzdm` |
| 博客园 | `cnblogs` |
| 51CTO | `51cto` |
| 语雀 | `yuque` |
| 搜狐号 | `sohu` |
| B站专栏 | `bilibili` |

前置：`.env` 中 `WECHATSYNC_TOKEN` + Arc 扩展「同步桥接」已连接。

```bash
bash scripts/wechatsync-wait-connect.sh 45   # dispatch 会自动调用
```

---

## 主轨 2 — 海外 API 脚本

**触发**：`dispatch-publish.js` → `global[]` 中 `primary_publisher: api` 的平台。

| 平台 | 脚本 | 配置 |
|------|------|------|
| DEV.to | `publish-devto.js` | `DEVTO_API_KEY` |
| GitHub Discussions | `publish-github-discussions.js` | `GITHUB_TOKEN` + `GITHUB_DISCUSSIONS_REPO` |
| Blogger | `publish-blogger.js` | Google OAuth — `scripts/setup-blogger.md` |

```bash
node scripts/dispatch-publish.js --manifest queue/dispatch-xxx.json --global-only
```

## 主轨 3 — 爱贝壳（Medium / X）

无 API 的海外平台走扩展：粘贴草稿 → 勾选平台 → 同步草稿箱 → 人工确认发布。

`dispatch-publish.js` 会打印逐步操作说明。

| 平台 | MCP tier |
|------|----------|
| DEV.to / Hashnode / LinkedIn / Bluesky | auto |
| Medium / Reddit / X | manual（草稿 + compose URL） |

LinkedIn 首次：`npx -y @automatelab/content-distribution-mcp linkedin install`

---

## 统一入口（Agent 写完后）

```bash
cd ~/Projects/content-distribution
cp queue/dispatch-manifest.example.json queue/dispatch-$(date +%Y-%m-%d).json
# 编辑 cn[] 与 global[]

node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --dry-run
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json

# 只发国内
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --cn-only

# 只生成海外 MCP 队列
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --global-only

# 复制 Agent 提示词（粘贴到 Cursor 执行海外 publish）
bash scripts/mcp-flush-prompt.sh
```

**真发**：将 manifest 中 `dry_run` 改为 `false` 或去掉 `--dry-run`。

---

## 补充工具

### 爱贝壳内容同步助手（付费扩展）

- **角色**：小红书、短视频、播客、50+ 平台可视化勾选
- **不是主轨**：与 Wechatsync / MCP 并存，手动在浏览器操作
- 说明：`channels/aibeike.md`

### crier（偶尔）

MCP 不可用或需要 `audit` 登记时：

```bash
pip install crier
crier publish drafts/devto-xxx.md --to devto --to hashnode
```

### fanout（偶尔）

站外原生产品宣发、HN/Reddit 研究循环、浏览器自动 LinkedIn/X：

- 仓库：https://github.com/MukundaKatta/fanout
- 不替代 GA 摘要主流程

---

## Agent 提示词模板

```
已完成 {canonical_url} 的多平台摘要稿，清单见 queue/dispatch-XXX.json。

1. 对每份 draft 跑 preflight
2. 运行: node scripts/dispatch-publish.js --manifest queue/dispatch-XXX.json --dry-run
3. 国内：确认 Wechatsync 连接后真发（--cn-only 或全量）
4. 海外：读取生成的 queue/mcp-pending-*.json，用 content-distribution MCP 完成 publish
5. 小红书等：提醒我用爱贝壳扩展手动同步
```

---

## 平台 → 主轨速查

| 平台 | 主轨 | 补充 |
|------|------|------|
| 知乎 / 百家号 / 掘金 / 头条 | Wechatsync | 爱贝壳 |
| DEV.to / Hashnode / LinkedIn / Bluesky | MCP | crier |
| Medium / Reddit / X | MCP（草稿档） | crier / fanout / 爱贝壳 |
| 小红书 / 微信（复杂流） | — | 爱贝壳 / Wechatsync |
| HN / Pinterest / DeviantArt | 人工 | fanout |

---

## 遗留脚本

`publish-medium.js` / `publish-devto.js` / `batch-publish.js` 保留作 **MCP 未配置时的 fallback**，新任务请用 `dispatch-publish.js`。
