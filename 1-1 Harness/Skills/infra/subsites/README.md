# infra/subsites · 子站（子项目）机制契约（v1.0 规划定稿）

> **背景决策**（品牌裁定 2026-10-04）：① WordPress 子站线从发布方案中**整体移除**（WP 方案不够系统，统一 Sanity+MFlow 方向）；② 子站改为**品牌内子项目**：与主项目共享知识库，其余能力按"继承 + 勾选覆盖 + 独立新增"配置。
> **首批对象**：Lovart blogs 子站（blogs.lovart.ai，原 WP 长文线，发布目标重新规划中）。Moodio 侧暂不启用。

## 一、继承模型（五项能力 × 三种模式）

子项目对五项能力逐项声明 `mode`：

| mode | 语义 | 示例 |
|---|---|---|
| `inherit` | 完全继承主项目，零独立配置 | kb（知识库全量共享）· geo（共享查询与探针） |
| `inherit+override` | 继承为主，勾选覆盖个别项 | strategy（共用词群地图，blogs 线单列长文条目）· orchestration（共用门禁/路由，blogs 排期独立 + 7500 词钩子参数） |
| `independent` | 完全独立新增 | site（域名/路由/CMS source 必然独立） |

**规则**：
1. `inherit+override` 必须写明 `inherit: [...]`（继承哪些）与 `override: {...}`（覆盖什么）——覆盖项可审计。
2. `independent` 的内容不回写主项目。
3. 共享资产（词群/知识库）修订在主文件进行，子站自动跟随；子站专属覆盖修订在子站声明内进行。
4. 新增独立内容（如子站专属选题线）走 `strategy.independent[]` 或子站 contentStrategy 增补节，主站策略文件不膨胀。

## 二、各能力子站化要点（Lovart blogs 为参照实现）

| 能力 | 子站化方式 |
|---|---|
| **知识库 kb** | inherit——kb_intent/事实白名单/表达红线全量共享；子站可加 `kb.extra` 追加目录，不可删减主库 |
| **策略 strategy** | 词群地图继承（词群加 `sites: ["blogs"]` 归属列即可分流）；选题计划 override——blogs 长文条目单列成节，排期与主站脱钩 |
| **站点 site** | independent——`run/sites/{subsite-id}.json` 独立档案（domain/sections/source）；project.meta.site 指向即完成绑定（现有 site_of 机制，零代码） |
| **体验 experience** | override——三张清单勾选（blogs 启用 weekly+monthly，长文校验、存量 URL 存活监控为子站专属覆盖项） |
| **GEO** | inherit——共享查询集与探针；子站 URL 计入 citations 归因（引用来源标注站点） |
| **编排 orchestration** | inherit+override——session-init/router/hooks/S0-S6 全继承；blogs 独立排期（weeklyDrip）与钩子参数（postWriteTargetWords=7500） |

## 三、WordPress 移除执行（品牌裁定落地）

1. `blog-writer/references/wp-publishing.md` → 状态改 **legacy-deprecated**（不再维护；历史方法仅作迁移参考）。
2. Lovart 生产侧 `publish-to-wp.py` 管线**冻结保留**：存量已发布内容不动、凭证不删、脚本不更新；恢复使用需品牌方重新裁定。
3. 链路上所有"发布到 blogs.lovart.ai"的表述改为"发布到 blogs 子站（目标待定）"。
4. presets/自动化/发布技能零 WP 污染（已核），无需清理。

## 四、blogs 子站待决清单（重新规划开放项）

| # | 待决 | 依赖 |
|---|---|---|
| 1 | 发布目标技术栈（候选：Sanity 同栈 blog section / MFlow 静态导出） | 子项目方案定稿 + 主站 Sanity 结构评估 |
| 2 | 7500 词长文线在新栈的形态（长文是 blogs 线核心资产） | #1 |
| 3 | 存量 WP 内容迁移评估（量/SEO 影响/301 方案） | #1 |
| 4 | 子站排期与主站日历的切分（PRODUCTION-PLAN 拆分） | #2 |
