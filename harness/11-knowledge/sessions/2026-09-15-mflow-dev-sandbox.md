---
type: session-log
session_date: 2026-09-15
session_slug: mflow-dev-sandbox
status: ready
---

# Session Log — MFlow Dev 沙箱建立 + 私有仓库化

## 目标
用户指令：不在原 vault 动手；在用户目录开 "MFlow Dev" 全量复制做调试；密码/env 可迁移；服务器与 GitHub 信息取自 OpenFlowDev。

## 完成
1. **沙箱建立**：`~/MFlow Dev`，rsync 因 4 个非法 UTF-8 文件名两度中断，改 `ditto` 完成全量 21,112 文件 / 1.7G，与源零差异。
2. **服务器/GitHub 接线**（来自 ~/OpenFlowDev）：服务器 `root@172.96.253.73:28766`（私钥在 OpenFlowDev/.ssh，不入库）；GitHub 账号 sevenaaaaaaaaa（gh CLI 已登录）。
3. **凭证隔离**：secrets/（git-ignored）收纳 Sanity token + Notion token 真值；推送前扫描逮住 2 处真泄漏（Notion ntn_ token 明文在 10-config 文档 + notion-sync/sync-queue.jsonl）——文档已 redacted，notion-sync 整目录排除，multi_seo/credentials 排除；三轮扫描后唯一命中为文档占位符 sk-xxx。
4. **私有仓库**：github.com/sevenaaaaaaaaa/mflow-dev（PRIVATE），3,080 tracked 文件，两次提交（initial import + layout-agnostic fixes）。
5. **沙箱验证逮住真 bug**（这正是建沙箱的意义）：5 个脚本硬编码 Obsidian `vault/1-Project/Lovart MFlow` 嵌套层级（session-init / hooks smoketest / sync-local-dev / pre-import-check 注释 / batch_gen_zh_design_topic_pages），平铺布局下全断。已全部改为项目根相对推导 → 沙箱 smoke（39+16+15）与 session-init 4 门禁全绿。
6. **deploy/server.md**：登记服务器目标 + systemd timer 部署形态 + 国内轨不上服务器的约束；未执行任何部署。

## 关键事实
- 原 vault 保持生产（launchd 三任务指向它），沙箱独立 .pipeline 状态。
- .gitignore 边界：secrets/、bulk data（From Datawork 1.1G 等）、内容池（Calendar/Page Gen/Drafts）、生成物（.cursor/rules 等）。
- 内容池与大数据在沙箱磁盘上保留（调试可见），只是不入 git。

## Lessons
- macOS rsync 遇非法 UTF-8 文件名会整体中断（不只是跳过），ditto 是可靠替代。
- "路径自推导"修复若仍锚定目录嵌套（而非脚本相对层级），换布局即碎——本次 5 处全是这种"修了一半"的可移植性债。
- 私有仓库化前必须扫 staged diff 而非工作区：notion token 就藏在"配置文档"和"同步队列数据"两类意外位置。

## 下一步（待用户指令）
- 内核抽取（kernel/brand-pack 两层拆分）在沙箱进行
- 服务器部署（需明示授权）
- 原 vault 侧的 session-init/smoketest 同款嵌套修复（本沙箱修法可直接回移）
