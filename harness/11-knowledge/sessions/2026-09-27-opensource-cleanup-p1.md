# MFlow 会话日志 — 2026-09-27 开源化清洗 P1

- **日期**: 2026-09-27 22:00 – 23:59
- **状态**: draft（待用户确认）
- **仓库**: github.com/sevenaaaaaaaaa/mflow @ main（7f3eb5f）

## Context

用户阅读 README 后提出五点：①清除 Lovart/Sanity 痕迹 ②真正的 GEO Agent（信号→生产→分发→洞察→LOOP）③完全开源 ④表述框架参考 OpenFlow ⑤文末超详细附录（每模块截图+介绍+用法）。仓库已 PUBLIC 但无 LICENSE，README 还写着"私有仓库、Sanity 生产库 8,247 文档"。

## Solution

1. **侦察**：仓库 PUBLIC、无 LICENSE、1639 个文件名含 lovart、13.5 万处字符串、真实 CMS project ID（o11tm2qe）泄露在 67 个追踪文件、站点档案带真实域名+ID。
2. **UI 去品牌**：console.html/py 用户可见文案 Sanity→CMS、Lovart→示例品牌；API 枚举/路径等功能契约保留（迁移另议）。
3. **站点档案脱敏**：`run/sites/lovart-global.json` → `main.json`（示例值），真实档案移入 git-ignored secrets/sites/；代码默认站点改 `main`。
4. **ID 清除**：o11tm2qe → your-project-id（67 文件）。
5. **编排目录改名**：lovart-pipeline-state→pipeline-state、lovart-router→router（30 文件引用同步，session-init 门禁实测通过）。
6. **32 张截图**：浏览器自动化逐模块拍摄（发现合成器混帧问题：需禁动画+强制重绘+冷却）。
7. **README 重写**：GEO Agent 主线 + OpenFlow 框架 + 文末 31 模块附录；修 capability-matrix/USAGE-GUIDE/warmup 等。
8. **MIT LICENSE** + 运行时产物 gitignore。

## Files Changed（要点）

- README.md（重写）、LICENSE（新增）、docs/screenshots/*（32 新增）
- dev/console/console.{py,html}（去品牌+3 bug 修复）
- run/sites/{lovart-global→main}.json、67 文件 ID 清除、docs/* 若干、AGENTS/ROADMAP

## Decisions

1. **范围切分**：显示层本轮清零；1639 文件名/13.5 万字符串/LOVART_* 环境契约/com.lovart.* launchd 属 P2 迁移——牵动生产服务器（env.sh/systemd/launchd），不可单方面做，已向用户提案。
2. **git 历史不重写**：仓库已公开，历史里 8,247 文档数字与 ID 已暴露；结论是"改未来不洗历史"（历史重写会断掉所有 fork/clone 且无安全收益，泄露物是 ID 非凭证）。
3. **并行流协作**：远端有另一 session 的功能提交（MCP/Playbook/编辑器/USAGE-GUIDE）；rebase 合入，README 以本次 GEO Agent 版为准并补新能力链接。rebase 冲突时 `--ours` 是被基于方——搞反会拿错版本（已踩，reflog 救回）。

## Patterns

- 单页应用截图三件套：禁动画 CSS + `.page.on` 文本稳定轮询 + 主区 opacity 强制重绘 + 1.5s 冷却；否则拿到混帧/空白帧。
- 大量 sed 替换前先 `git ls-files -z`（带空格的中文路径会让 xargs/git grep 输出裂行）。

## Open Questions

- P2 全仓库迁移何时做、是否连同服务器一次切换？
- insight-data / genflow 的数千篇成品内容（大量 lovart 标题）建议归档出库而非改名，是否执行？
- 远端并行流是谁/在哪台机器，后续 console 改动如何协调？
