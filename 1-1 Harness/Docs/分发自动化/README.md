# Lovart 全渠道内容分发（GA 驱动）

主站：**https://lovart.ai** · 数据源：**Lovart Trident** GA4/GSC 管道

## Canonical SOP

SSOT 文档（Obsidian，需本机可读）：

`LifeOS Pro PARA Vault/2-Area/Product Project Management/全渠道内容分发自动化SOP.md`

本目录为**可执行工作副本**。iCloud 权限恢复后，将 `content-distribution/` 同步到上述路径旁。

---

## 快速开始

```bash
cd ~/Projects/content-distribution

# 1. 从 Trident 快照评分（或 --sample 试跑）
python3 scripts/score-pages-for-distribution.py --days 28

# 2. Agent 按 channels/*.md 生成平台稿 → drafts/

# 3. 发布前检查
node scripts/preflight-distribution.js --draft drafts/devto-example.md \
  --canonical https://lovart.ai/en/blog/example \
  --platform devto --source-title "Original Main Site Title"

# 4. 统一分发
node scripts/dispatch-publish.js --manifest queue/dispatch-2026-06-07.json --dry-run
```

---

## 主轨

| 类型 | 工具 | 平台 |
|------|------|------|
| **主站** | lovart.ai | SSOT |
| **国内** | Wechatsync CLI | 15 平台（知乎、百家号、掘金、头条、CSDN、豆瓣、思否、简书、什么值得买、博客园、51CTO、语雀、搜狐号、B站专栏，见下表） |
| **海外 API** | `publish-*.js` | DEV.to、GitHub Discussions、Blogger |
| **海外扩展** | 爱贝壳（3 免费槽） | Medium、X |

详见 **[WORKFLOWS.md](./WORKFLOWS.md)** · **`config/stack.json`** · 编辑规范 **[EDITORIAL.md](./EDITORIAL.md)**（国内中文 / 海外英文 · 发布前人工审核）

---

## 文章同步助手（Wechatsync）支持平台

> 来源：[wechatsync/Wechatsync v2 README](https://github.com/wechatsync/Wechatsync/blob/v2/README.md) · 扩展 **v2.0.9**（2026-03-24）  
> 安装：[Chrome 应用店](https://chrome.google.com/webstore/detail/hchobocdmclopcbnibdnoafilagadion) · CLI：`npm i -g @wechatsync/cli`

扩展 + CLI 共用同一套平台 ID。`wechatsync sync article.md -p zhihu,juejin` 中的 `-p` 即下表 **ID** 列。

### Lovart 主栈已接入（`dispatch-publish.js` → Wechatsync）

在 `queue/dispatch-*.json` 的 `cn[]` 中按平台添加 `{ "platform": "<id>", "draft": "drafts/<id>-{slug}.md" }` 即可。

| 平台 | ID | 类型 |
|------|-----|------|
| 知乎 | `zhihu` | 主流自媒体 |
| 百家号 | `baijiahao` | 通用 |
| 掘金 | `juejin` | 技术社区 |
| 头条号 | `toutiao` | 通用 |
| CSDN | `csdn` | 技术社区 |
| 豆瓣 | `douban` | 通用 |
| 思否 | `segmentfault` | 技术社区 |
| 简书 | `jianshu` | 通用 |
| 什么值得买 | `smzdm` | 通用 |
| 博客园 | `cnblogs` | 技术社区 |
| 51CTO | `51cto` | 技术社区 |
| 语雀 | `yuque` | 技术社区 |
| 搜狐号 | `sohu` | 通用 |
| B站专栏 | `bilibili` | 通用 |

```bash
# 一次同步多个国内平台（CLI 直调）
wechatsync sync drafts/zhihu-slug.md -p zhihu,csdn,segmentfault,jianshu
```

### 扩展已支持、主栈未接入（可按需扩展）

| 平台 | ID | 类型 | 备注 |
|------|-----|------|------|
| 微信公众号 | `weixin` | 主流自媒体 | |
| 微博 | `weibo` | 主流自媒体 | |
| 小红书 | `xiaohongshu` | 主流自媒体 | 也可用爱贝壳 |
| 抖音图文 | `douyin` | 主流自媒体 | v2.0.8+ |
| 雪球 | `xueqiu` | 财经 | |
| 人人都是产品经理 | `woshipm` | 产品 | |
| 大鱼号 | `dayu` | 通用 | |
| 一点号 | `yidian` | 通用 | |
| 慕课网 | `imooc` | 技术社区 | |
| 开源中国 | `oschina` | 技术社区 | |
| 搜狐焦点 | `sohufocus` | 房产 | |
| 东方财富 | `eastmoney` | 财经 | v2.0.6+ |
| 网易号 | `netease` | 通用 | v2.0.7+ |
| X (Twitter) | `x` | 海外 | 主栈走爱贝壳 |

### 建站 / CMS

| 平台 | ID | 说明 |
|------|-----|------|
| WordPress | `wordpress` | MetaWeblog API |
| Typecho | `typecho` | MetaWeblog API |
| Hexo | `zip-download` | Markdown 压缩包下载 |
| Hugo | `zip-download` | Markdown 压缩包下载 |

### 近期版本新增平台（changelog 摘要）

| 版本 | 日期 | 新增 / 变更 |
|------|------|-------------|
| v2.0.9 | 2026-03-24 | CLI/MCP 同步 HTML 保留样式；文章识别增强 |
| v2.0.8 | 2026-03-17 | **抖音图文** `douyin` |
| v2.0.7 | 2026-03-10 | **什么值得买** `smzdm`、**网易号** `netease`；简书 Markdown |
| v2.0.6 | 2026-02-25 | **东方财富** `eastmoney` |

完整 changelog：[wechatsync.com/changelog](https://www.wechatsync.com/changelog)

### CLI 常用命令

```bash
# .env 中 WECHATSYNC_TOKEN 与扩展「同步桥接」一致
export WECHATSYNC_TOKEN="..."

# 查看全部平台及登录态（需扩展桥接在线）
wechatsync platforms --auth

# 同步到指定平台（默认草稿箱）
wechatsync sync drafts/zhihu-example.md -p zhihu,baijiahao,csdn

# 或通过项目脚本
bash scripts/publish-wechatsync.sh drafts/zhihu-example.md zhihu,baijiahao
bash scripts/check-wechatsync.sh
```

**连接要点**：扩展设置开启「同步桥接」→ Token 写入 `.env` → Arc 保持运行 → `bash scripts/wechatsync-wait-connect.sh 45`

---

## 目录

| 路径 | 用途 |
|------|------|
| `WORKFLOWS.md` | 分发架构与操作说明 |
| `RUNBOOK.md` | Gate 0 + 每周节奏 |
| `config/stack.json` | 主轨定义 |
| `config/platforms.json` | 平台 → 发布器路由 |
| `channels/` | 各平台内容规格 |
| `templates/` | 轨道 A/B 母模板 |
| `queue/` | 待发布清单 / 已发布登记 |
| `scripts/` | 评分、预检、`dispatch-publish.js` |
| `automations/` | 每周调度说明 |
