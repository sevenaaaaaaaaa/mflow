"""replication-core v0.1 — 设计复刻引擎（平台无关核心）。

从 lovart.ai composite-page-all → WordPress 复刻实战（2026-10-06 全链路验证）抽象而来。
五环节 + IR 构建，平台无关；目标平台映射（Gutenberg/WebFlow/…）由各产品适配器消费 IR 完成。

模块：
  probe          源探测（可达性 / SSR 判定 / 资源形态）
  extract_css    设计资产提取（编译 CSS 合并 / tokens / 字体栈 / 断点）
  split_sections 结构切分（锚点切分 / 修边 / 平衡闭合）
  extract_tokens CSS 变量提取与分组
  ir             中间表示构建与校验（IR v1.0）
  qa_compare     静态断言（组件覆盖 / 关键词 / 无脚本）

约定（lineage）：所有函数均为实战验证逻辑的函数化；修改需附实战依据。
"""
__version__ = "0.1.0"
IR_VERSION = "1.0"
DEFAULT_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
