# 全渠道内容分发 RUNBOOK

主站 canonical：**https://lovart.ai**

---

## Gate 0 — 防抢权重红线

发布前逐项确认（`preflight-distribution.js` 自动校验）：

1. **禁止**全文复制主站到站外（Medium / DEV.to / Hashnode / 百家号等）
2. **必须**含主站链接，格式：`https://lovart.ai/...?utm_source={platform}&utm_medium=syndication&utm_campaign=offsite_{slug}`
3. **canonical**（Medium / DEV.to / Hashnode）：指向主站完整 URL
4. **标题**：与主站 `<title>` 编辑距离 > 15% 或明显不同角度
5. **首 120 字**：必须重写，不得与主站 meta description 相同
6. **体量**：站外词数 ≤ 主站词数 × 40%（教程类）
7. **时效**：主站发布 ≥7 天（`/pricing`、首页、品牌 Top 页 ≥14 天）
8. **黑名单**：`/`, `/pricing`, `/en`, `/zh` 首页变体，GSC 品牌 Top10 对应 URL
9. **频率**：同一主站 URL 本月 ≤2 个平台

---

## 双轨流程

### 轨道 A — GA 优质页摘要再分发

```
Trident GA 快照
  → score-pages-for-distribution.py
  → 选 S/A 级（Top 5–10）
  → Agent 按 channels/{platform}.md 写摘要稿
  → preflight-distribution.js
  → 人工审核
  → publish-*.js 或手动后台
  → logs/ + published.json
```

### 轨道 B — 站外搜索原生内容

```
Trident GSC 竞品未覆盖词 / 站外意图选题
  → queue/offsite-briefs.json
  → Agent 用 templates/offsite-native.md
  → preflight（无 canonical 冲突，因主站无同题页）
  → 全文字数可完整发布
  → CTA 链 lovart.ai 相关工具页
```

---

## Trident 数据接入

### 环境变量

```bash
# .env
TRIDENT_ROOT=/path/to/Lovart Dev
# 或 1-4 Dev
```

### 评分命令（每周一）

```bash
cd ~/Projects/content-distribution
python3 scripts/score-pages-for-distribution.py --days 28
# 无快照时试跑：
python3 scripts/score-pages-for-distribution.py --days 28 --sample
```

输出：`queue/candidates-YYYY-MM-DD.json`

### 纳入评分的页面

- `/blog/`、`/tools/`、`/features/` 路径
- 排除 Gate 0 黑名单

### 评分公式

```
score = 0.35×norm(sessions) + 0.25×norm(engagement_time)
      + 0.20×norm(engagement_rate) + 0.10×norm(gsc_clicks_mom)
      + 0.10×norm(non_brand_share)
```

| Tier | 分数 | 动作 |
|------|------|------|
| S | ≥75 | 2–4 平台摘要 |
| A | 60–74 | 1–2 平台 |
| B | 45–59 | 仅轨道 B 改写 |
| C | <45 | 跳过 |

---

## 每周运营节奏

| 日 | 动作 |
|----|------|
| 周一 09:00 | 跑评分 → 更新 `queue/pending.json` |
| 周一–周二 | Agent 生成平台草稿 |
| 周三 | 人工审核 + 发布批次 |
| 周五 | 写 `logs/weekly-*.md` 复盘 UTM |

**配额**：每周站外 ≤6 条；同 URL ≤2 平台/月

---

## MVP 首发（Medium + DEV.to）

见 [MVP.md](./MVP.md)。

```bash
# 预检示例
node scripts/preflight-distribution.js \
  --draft drafts/medium-my-slug.md \
  --canonical https://lovart.ai/en/blog/my-slug \
  --platform medium \
  --source-title "Main Site Original Title" \
  --source-word-count 2500

# 发布（先 dry-run）
node scripts/publish-medium.js --draft drafts/medium-my-slug.md --dry-run
node scripts/publish-devto.js --draft drafts/devto-my-slug.md --dry-run
```

---

## 国内平台 — Wechatsync（15 平台，见 README）

知乎、百家号、掘金、头条、CSDN、豆瓣、思否、简书、什么值得买、博客园、51CTO、语雀、搜狐号、B站专栏。

扩展：**文章同步助手** v2（Arc 可用，与 Chrome 相同）。CLI 通过 WebSocket `9527` 桥接，使用浏览器已登录 Cookie，**默认发草稿**。

### 首次连接（Arc）

1. Arc 工具栏打开扩展 → **设置**（齿轮）
2. 开启 **「同步桥接」**（CLI / MCP 连接）— 未开启时 CLI 会一直超时
3. 复制弹窗里自动生成的 **Token** → 写入 `.env` 的 `WECHATSYNC_TOKEN`
4. **服务器地址留空**（默认 `ws://localhost:9527`）；本机勿填远程 IP
5. 保持 Arc 运行；若显示「等待连接」，点一下扩展图标唤醒 Service Worker
6. 终端验证：

```bash
export WECHATSYNC_TOKEN=<扩展里的 token>
bash scripts/check-wechatsync.sh          # 应显示 connected:true
wechatsync platforms --auth               # 查看知乎/百家号等登录态
```

### 发布（Gate 0 摘要稿）

```bash
bash scripts/publish-wechatsync.sh drafts/zhihu-my-slug.md zhihu,baijiahao
```

### 海外平台（主轨：content-distribution-mcp）

`dispatch-publish.js` → `queue/mcp-pending-*.json` → Cursor Agent `hints` + `publish`。

| tier | 平台 |
|------|------|
| auto | DEV.to、Hashnode、LinkedIn、Bluesky |
| manual | Medium、Reddit、X（草稿 + compose URL） |

补充：**crier**（MCP 兜底）、**fanout**（产品宣发）、**爱贝壳**（50+ 平台含小红书）。

完整说明：**[WORKFLOWS.md](./WORKFLOWS.md)** · **`config/stack.json`**

---

## Agent 写完后分发

```bash
cp queue/dispatch-manifest.example.json queue/dispatch-$(date +%Y-%m-%d).json

node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --dry-run
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json
```

- `cn[]` → Wechatsync 自动发
- `global[]` → MCP 待发布队列，由 Agent 执行

---

## 明确不做

- 与 Lovart Sanity 发布管线合并
- n8n（除非 SOP 后续要求）
- Reddit/HN 自动发帖
- 品牌词页面站外全文索引
