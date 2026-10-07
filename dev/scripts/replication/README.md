# replication-core · 设计复刻引擎 v0.1

> **来源**：lovart.ai composite-page-all → WordPress 复刻实战（2026-10-06 全链路验证）的函数化抽象。
> **定位**：平台无关核心（环节 1-4+7-8），产出平台无关 IR；目标映射由各产品适配器完成（产品化规划见 `docs/PRODUCTIZATION-REPLICATION.md`）。

## 模块

| 模块 | 职责 | 实战依据 |
|---|---|---|
| `probe` | 源探测：可达性 / SSR 判定（文本密度）/ 样式表清单 | composite-page-all 752KB 全量 SSR 判定 |
| `extract_css` | 编译 CSS 合并（资源绝对化）/ tokens / 断点 / 字体栈 | lovart.ai 4 CSS 合并 364KB → 33 组件视觉一致 |
| `split_sections` | 锚点切分 / 修边（脚本剥离、尾部杂物、div 平衡、开标签补全） | 33 组件按 data-lp-section 锚点切分；VARIANTS 工具面板移除 |
| `extract_tokens` | CSS 变量提取与语义分组、hex 色板 | 381 tokens → theme.json |
| `ir` | IR v1.0 构建与校验 | 33 片段 + 381 tokens + 12 GEO 查询 |
| `qa_compare` | 静态断言（组件覆盖 / 关键词 / 无脚本 / CSS 加载） | 渲染 8 项断言的函数化 |

## IR（中间表示 v1.0）

```json
{
  "irVersion": "1.0",
  "source": {"url": "...", "ssr": true},
  "darkMode": "class|prefers|none",
  "design": {"css": "合并 CSS", "tokens": {...}, "breakpoints": {...}, "fonts": {...}},
  "sections": [{"order": 0, "type": "hero-split", "html": "...", "assets": [...]}],
  "meta": {}
}
```

Schema：`ir-schema.json`。**IR 变更 = major 版本**。

## CLI

```bash
# 探测
python cli.py probe --url https://www.lovart.ai/internal/composite-page-all
# 全流程复刻 → IR + 组件片段 + 报告
python cli.py replicate --url <源页> --base <资源基准> --out <目录> \
    [--anchor <正则>] [--dark class] [--trim-tail '<marker>']
# IR → WordPress 主题区块
python cli.py to-wordpress --ir <ir.json> --theme-dir <主题目录> [--page-slug xxx]
```

## 适配器

- `adapters/wp_blocks.py`（MFlow）：IR → Gutenberg `lovart/{type}` 区块 + lovart-site.css + tokens + 深色 body_class 片段
- WebFlow 适配器：待场景信息（目标输出形态 / 源站类型 / 内容治理需求）

## 已知边界（v1 不做）

CSR 站点需 headless 渲染 · 交互 JS 不移植 · 私有字体 fallback · 防盗链资源需媒体本地化 · 源页预览工具剥离 · 深色机制需探测（class vs prefers）
