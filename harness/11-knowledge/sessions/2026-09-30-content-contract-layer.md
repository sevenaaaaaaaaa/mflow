# Session Log · 2026-09-30 · 内容契约层 P0 开发（注册表 / 故事线门禁 / PRD 内容模型）

- **status**: draft
- **类型**: 开发（新增 4 文件 + 修改 6 文件，未提交）
- **上游**: 2026-09-28 差距分析（同目录 2026-09-28-gap-analysis-composite-blog.md），用户指令「接下来开始开发」
- **验收**: `bash "dev/scripts/run-tests.sh"` → console 55 + 内容契约 32 = **87 全绿**；session-init 六道 GATE 全过

## 交付内容（对照 09-28 差距清单）

### P0-1 组件注册表（模块化）
- 新增 `dev/scripts/publish_adapters/section_registry.py`：34 型注册表（README 逐型枚举 34 = 演示 33 + feature-grid 共享底层）+ 逐型字段 schema 校验
  - BLOCK：未注册 type（含驼峰错写提示）/ legacy 旧 8 型 / faq `[[q,a]]` 数对 / proof-block 用 stats 字段 / pricing `plans` / icon 越白名单 / 非绝对图片 URL / 按钮缺 text、variant 非法
  - WARN：alt 缺省、缺 src 留白、canvas-wall <10 条、columns 越预设、openLogin 越位、按钮无 href
  - 逃逸口 `MFLOW_SKIP_REGISTRY=1`（应急）；独立 CLI `python3 section_registry.py x.json` exit 1=有 BLOCK
- `validate_sections()` 默认接入注册表 → console `_bh_publish_sanity` / CLI 发布链全部生效（零 console 改动受益）

### P0-2 故事线进代码（模块化）
- 新增 `storylines.py`：加载 Refresh-Page 三份 JSON + STORYLINES.md 表格（F/T/P/C/K/N）
- 顺序校验按**族**比较（hero/bento/portrait/showcase/workflow/compare/review），族内变体替换放行、跨族错位 BLOCK；`T-long` 无固定序列跳过；未注册故事线降级 warning
- 接入 `publish_landing`；console 故事线知识源从不存在的 `harness/08-storyline` 改指 Refresh-Page（md+json），知识中台 kb_tree/kb_list 放行 .json

### P0-3 生成端错配修复
- `md_to_sections()`：faq → `[{question, answer}]`；数字证据段 proof-block+stats 错配 → 正牌 `stats` 型；feature-detail items 补 media.alt

### Blog P0（PRD §1.3/I1/§6）
- `_id = (type, slug, language)`：blog `blog-{slug}-{lang}`、composite `{page_type}-{slug}-{lang}`（`MFLOW_LEGACY_DOC_ID=1` 回退）；patch/create 定位一律按 slug+language GROQ，旧 _id 文档可继续 patch
- 三时间：`publishedAt`（fm `published`）+ `displayedAt`（fm `date`，回落 publishedAt）+ JSON-LD datePublished 用 displayedAt；`createdAt` 留给系统 `_createdAt`
- status 五态（CLI `--status`，非法回落 draft）+ noIndex（fm）；新增 `scheduled_flip.py`（scheduled→published，ifRevisionID，默认 dry-run，待接 cron）
- blog `--mode patch`（同 slug+language create 拒绝并提示，不再静默跳过）
- `md_to_portable_text`：独立行图片 → PT image block（src/alt，不再降级 `[Image: alt]`）；行内图片 → 链接（embed→链接 降级规则）；PT 校验器补 image 规则；`library/pt_to_md.py` 镜像提取图片 URL

## 测试与门禁
- 新增 `dev/tests/test_content_contract.py`（32 用例）；`run-tests.sh` 改为跑全部 `test_*.py`
- 中途一次回归：注册表把「无封面草稿 media 空 src」判 BLOCK 打破 console 既有用例 → 重新分级：缺 src=留白 WARN，坏引用（相对路径）=BLOCK（事故形态是坏引用不是缺图）

## Lessons
- 校验分级要对着前端真实行为定级：未注册 type/坏引用是静默丢失必须 BLOCK；缺图只是留白，WARN 足够——分级错了校验器会打破正常流程
- patch 定位从 `_id` 换成 slug+language GROQ 后，_id 方案变化对存量文档零影响——身份查询和存储键解耦是对迁移期最友好的做法

## 部署（2026-09-30 同日）

- 提交 `f48f8e4`（内容契约层）+ `33d104d`（SSOT 守卫）+ `ea5c255`（sync.sh rsync 重试）→ 已推 GitHub
- 中途远端 main 有他机提交（20642b3 digest 修复，交集仅 console.py）→ rebase 干净，含其 2 个回归用例后本地 89 用例全绿
- **服务器第一轮 GATE6 挂**：开源版服务器不带 `genflow/` SSOT，`test_load_storylines_nonempty` 硬断言 F1 存在 → 修为 setUpClass SkipTest（load 空=合法降级）。教训：本地全仓跑绿 ≠ 服务器（零品牌部署）绿，SSOT 依赖必须显式降级
- **rsync 瞬态抖动**：22 组各自建 SSH 连接，三轮随机掉不同组（Skills/trident/...）→ sync.sh 每组重试 3 次（ea5c255）
- 最终 sync 全流程通过：22 组同步 ✓ · 服务 active · 服务端六道 GATE 全过 · 入口 200 ✓
- 待办新增：服务器给 `scheduled_flip.py` 挂 cron（`*/10 * * * * ... scheduled_flip.py --yes`）

## 待办（下一轮）
- [ ] scheduled_flip 接 systemd timer/cron（服务器侧）
- [ ] console blog 发布 patch 模式 UI/批量项透传（当前仅 CLI）
- [ ] aggregate/related 查询 API（C4）、og 三字段、图片本地化管道（C6）
- [ ] batch_gen_zh_* 历史脚本字段错配回改（注册表现已能拦）
