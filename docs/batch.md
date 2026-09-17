# 批量任务执行器（Batch Tasks）

> 用途：把「批量生成 / 批量改稿 / 物料替换 / 字段改写」变成可排队、可暂停、可续跑、可审计的任务。
> 位置：工作台「批量任务」页；执行器常驻 console（systemd 守护，重启自动续跑）。

## 任务模型

```json
{
  "id": "batch-YYMMDD-xxxxxx",
  "type": "asset_replace | field_patch | gen | rewrite",
  "title": "人类可读标题",
  "status": "queued | running | paused | done | failed | cancelled",
  "dry_run": true,
  "concurrency": 2,
  "created": "…", "created_by": "…", "started": "…", "finished": "…",
  "params": {"max_attempts": 2},
  "items": [{"i":0,"status":"pending|running|done|failed|skipped","attempts":1,"result":{},"error":""}],
  "stats": {"total":n,"done":n,"failed":n,"skipped":n},
  "log": ["[HH:MM:SS] …"]
}
```
存储：`run/batch/{id}.json`（原子写：临时文件 + rename）。

## 四类执行器

| type | items 字段 | 行为 | dry-run |
|------|-----------|------|:---:|
| `asset_replace` | `doc_id, kind(cover/media), idx, field, old, new_url, new_alt` | Sanity patch（cover.url/alt、coverUrl、bodyJson 版块 media），`ifRevisionID` 并发保护 | ✅ |
| `field_patch` | `doc_id, set:{"seoTitle":…,"description":…}` | 任意字段改写（Sanity patch） | ✅ |
| `gen` | `item_id, type, lang, topic, brief, template_id?` | LLM 生成 → 落盘 → post-write + geo 门禁 → 状态机推进（S3-creating→S3-draft→S3-done→S4-qa） | 不适用（产出草稿，天然安全） |
| `rewrite` | `item_id, lang, topic, instruction, source_path?` | 读既有内容 → 按指令改写 → 同上（用于衰减页/高曝光低 CTR 页刷新） | 不适用 |

> 状态机顺序很关键：`S0-todo` 不可直达 `S3-draft`，必须先 `S3-creating`（踩过）。`advanced` 字段按真实 rc 判定，不再假报成功。

## 执行语义

- **并发**：任务内 `ThreadPoolExecutor(concurrency=2)`；同一时刻只跑一个任务（避免资源争抢）
- **重试**：单条失败按 `params.max_attempts`（默认 2）自动回到 pending
- **暂停/继续/取消**：worker 每 5s 轮询任务状态；暂停后不再领新条目；继续时把 running 条目重置 pending
- **断点续跑**：任务文件持久化，console 重启后自动接着跑未完成条目
- **审计**：创建与动作写 `run/approvals.log`（BATCH-CREATE / …）

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/batch/list` | 任务列表（含进度） |
| GET | `/api/batch/detail?id=` | 任务详情（条目级状态/结果/错误 + 日志） |
| POST | `/api/batch/create` | `{type,title,items,dry_run,site?,params?}`；`asset_replace` 且 items 为空 → 自动取内容库的物料替换计划 |
| POST | `/api/batch/action` | `{id, action: pause\|resume\|cancel\|retry_failed}` |

## 典型用法

**① 图片物料批量替换**（推荐路径）
1. 内容库 → 图片物料 → 生成计划（匹配 + 过滤）
2. 批量任务 → 「从图片物料计划一键建任务」→ 勾 dry-run 跑一遍看结果
3. 核对后去掉 dry-run 重建任务 → 真写（带 ifRevisionID）

**② 高曝光低 CTR 页面批量改稿**
```json
{"type":"rewrite","dry_run":false,"items":[
  {"item_id":"refresh-text-to-image","lang":"en","topic":"text to image generator",
   "instruction":"重写 Title/首段/FAQ，提升 CTR；补数据点与来源链接",
   "source_path":"run/library/lovart-global/blog/en/xxx.md"}]}
```

**③ SEO 字段批量改写（title/description）**
```json
{"type":"field_patch","dry_run":true,"items":[
  {"doc_id":"…","set":{"seoTitle":"…","description":"…"}}]}
```

**④ 批量生成新稿**（等下再发布）
```json
{"type":"gen","dry_run":false,"items":[
  {"item_id":"geo-gap-x","type":"blog","lang":"zh","topic":"…","brief":"…"}]}
```

## 实测（2026-09-17）

| 场景 | 结果 |
|------|------|
| field_patch dry-run（2 条 SEO 标题） | 2/2 done |
| asset_replace（内容库计划 3 处 cover）dry-run | 3/3 done |
| gen（1 篇中文稿） | 1/1 done → hook PASS + geo PASS → 推进 S4-qa |
| 暂停→继续（4 项 gen） | 暂停时 0/4 → 继续后 4/4 done |
| 断点续跑 | 任务文件持久化，重启后自动续（实现层保证） |
