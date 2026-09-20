# 正文编辑器 · 版本 · 改动对照（P2-1）

> 交付 2026-09-20。补的是一个结构性缺口：此前阅读器**全只读**，
> AI 出稿后人只能「通过」或「打回重跑」——**改一个词都要回 Sanity 或重跑一次 Loop**。

## 一条铁律

**编辑必须与门禁绑定。** 保存 = 快照旧版 → 原子写 → **重跑四道门禁**
（post-write / geo / quota / lang）。绕过门禁的编辑入口等于给 RULES 开后门。

门禁不通过时：
- 文件**照常保存**（用户的修改不该被吞），但结论落 `last-gate.json`；
- UI 明确标 BLOCK 并逐项给出 hook 输出；
- **发布链硬拦**：`publish_sanity` 遇到「最近一次人工编辑未过门禁」的稿子直接抛错，
  不给发。没编辑过的稿子无此记录 → 行为与之前完全一致，不引入回归。

## 能改什么

`editable_path()` 是唯一的写入闸门，白名单只有三处根目录：

| 可编辑 | 只读 |
|---|---|
| `run/projects/{id}/content/**.md`（生成稿） | `1-1 Harness/02-rules/**`（RULES 是 SSOT） |
| `run/library/{site}/**.md`（内容库镜像） | `docs/**`、`ROADMAP.md` |
| `1-3 GenFlow/**.md`（草稿池） | `1-2 Insight/**`（报告由脚本生成） |

非 `.md`、路径穿越（`..`）、白名单之外的一律拒绝。这几条有单测护着
（`TestContentEditor`），放宽它就是放宽整个系统的写入边界。

## 三个视图

阅读器右上角切换：

- **阅读** —— 原来的渲染视图（目录、报告仪表卡都保留）
- **编辑** —— 左边 markdown、右边实时预览。预览走 `POST /api/content/preview`，
  **与正式渲染同一个 renderer**，避免"编辑时看到的"和"发出去的"不一样。
  字数显示用**词当量**口径（ASCII 词 + CJK 字符 ÷ 2），与 `quota-check` 一致，否则字数会骗人。
  `⌘/Ctrl + S` 保存。
- **改动** —— 行级 diff，未改动的长段折叠成「⋯ 省略 N 行」。
  选历史版本即可与当前对比，并可一键「恢复这一版」（恢复前会把当前内容也存一版，不丢东西）。

## 版本

每次保存前自动快照，保留最近 **10** 版，存 `run/versions/<路径哈希>/`。
版本号是「微秒 + 碰撞计数」——秒级时间戳在连续保存时会互相覆盖，版本会**真的丢**
（`test_snapshot_rotation_keeps_n` 抓到的 bug）。

## 改稿任务的 diff

批量任务详情里，改稿类条目（`rewrite` / `landing_refresh`）直接给两个按钮：

- **↔ 看改动** —— 原稿 vs 新稿的逐行对照（`_bh_rewrite` 回传 `source_path` 才有）
- **✎ 编辑** —— 直接进编辑态改两句

改稿任务最该被看见的就是「改了什么」，此前要人自己去两个文件里对。

## 接口

| 方法 | 端点 | 说明 |
|---|---|---|
| GET | `/api/content/raw?path=` | 原文 + `editable` + 版本列表 |
| GET | `/api/content/versions?path=` | 版本列表 |
| GET | `/api/content/diff?path=&a=&b=&a_path=` | `a`=版本号，或用 `a_path` 跨文件比；`b` 默认 `current` |
| POST | `/api/content/preview` | `{text}` → html（生产 renderer） |
| POST | `/api/content/save` | `{path,text,type,lang}` → 门禁结果 + diff 统计 |
| POST | `/api/content/restore` | `{path,ts}` |

权限：viewer 只读（全局守卫已覆盖）；编辑不是 admin-only——它是内容团队的日常动作。
每次编辑与恢复都写 `approvals.log`（`CONTENT-EDIT` / `CONTENT-RESTORE`）。

## 还没做

- 编辑器只改**本地 md**。内容库镜像里改完，要发布才会回到 Sanity（走既有发布链）。
- 无协同编辑 / 无锁。多人同时改同一篇会后写覆盖先写——当前团队规模下先不做，
  真出现冲突再上「基于 mtime 的抢锁提示」。
