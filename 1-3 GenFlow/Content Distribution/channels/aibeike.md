# 爱贝壳内容同步助手（补充）

| 项 | 值 |
|----|-----|
| 定位 | **海外主轨之一** — 免费额度 3 平台槽位 |
| 当前占用 | Medium（槽 1）· X（槽 2）· 槽 3 预留 |
| 其他主轨 | 国内 Wechatsync · 海外 API（DEV.to / GitHub / Blogger） |
| 自动化 | 浏览器内模拟操作 → 各平台草稿箱 |

## 主栈分工

| 场景 | 工具 |
|------|------|
| 知乎 / 百家号 / 掘金 / 头条 | **Wechatsync CLI** |
| DEV.to / GitHub Discussions / Blogger | **publish-*.js API** |
| Medium / X（无 API） | **爱贝壳** |
| 小红书 / 短视频 / 50+ 平台勾选 | **爱贝壳**（补充） |

## 使用步骤

1. Arc/Chrome 安装「爱贝壳内容同步助手」（扩展 ID 与 Wechatsync 并存）
2. 各平台网页端先登录
3. 打开扩展侧栏 → 粘贴 Markdown 或导入内容 → 勾选目标平台 → 同步到草稿箱
4. 各平台后台人工确认发布（遵守 Gate 0：摘要 + 主站 UTM）

## Gate 0

与主轨相同：禁止主站全文镜像；标题改写；含 `lovart.ai` canonical 链接 + UTM。

## 记录

爱贝壳无 CLI 队列回写；发布后手动更新 `queue/published.json` 或让 Agent 补录。
