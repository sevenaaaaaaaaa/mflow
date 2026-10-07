# 补充发布工具（偶尔使用）

主轨固定：**国内 Wechatsync · 海外 content-distribution-mcp**。以下仅在特定场景启用。

## crier（Python CLI）

| 项 | 值 |
|----|-----|
| 安装 | `pip install crier` |
| 适合 | MCP 不可用时的海外 API 兜底；`audit` / `backfill` 登记已发平台 |
| 平台 | dev.to, Hashnode, Medium, Bluesky, LinkedIn（API）, X（复制粘贴） |

```bash
crier config set devto.api_key $DEVTO_API_KEY
crier publish drafts/devto-xxx.md --to devto --to hashnode
crier audit ./drafts --profile blogs
```

## fanout（Chrome 扩展 + 后端）

| 项 | 值 |
|----|-----|
| 适合 | 站外**原生产品宣发**；HN/Reddit 信号研究；LinkedIn/X **浏览器自动发** |
| 不适合 | GA 主站摘要再分发（易偏全文、运维重） |
| 仓库 | https://github.com/MukundaKatta/fanout |

需自建 Postgres + FastAPI；与 Lovart Gate 0 流程并行，不替代 `dispatch-publish.js`。

## 爱贝壳

见 [aibeike.md](./aibeike.md) — 小红书 / 视频 / 50+ 平台勾选。

## 选型速查

| 需求 | 工具 |
|------|------|
| Agent 写完后常规分发 | `dispatch-publish.js` |
| 海外 MCP 挂了 | crier |
| 产品发布公告 + 社媒研究循环 | fanout |
| 小红书 / 短视频矩阵 | 爱贝壳 |
