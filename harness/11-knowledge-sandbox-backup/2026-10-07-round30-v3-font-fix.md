# Round 30（2026-10-07）：v3 修复——主站 body 字体模块类 + 最新 CSS（用户反馈"比例/缩放/字体全不对"的根治）

**根因链（deep diff 定位）**：
1. 主站 body 挂 **8 个字体模块类**（poppins/barlowcondensed/inter/gtstandard/gtstandardmono/featuredeck/featuredisplay/notosanssc/notoserifsc/…module__variable）——Next.js 字体优化生成的 CSS 变量全挂这些类下。复刻页缺这些类 → 全部字体/变量失效（fallback 系统字体）。
2. 此前抓的 CSS 是旧版（无 .dark 块、无 --font-serif-deck）；主站 CSS 域名是 tic3.lovart.ai。

**修复**：① 主站最新 CSS 重提取（364KB，含 .dark 块 + serif-deck，资源绝对化）② 复刻内容包 wrapper：`<div class="lovart-replica-scope {主站8字体模块类} [+dark]">`——CSS 变量/字体按主站原样生效，WP 主题类被 scope 隔离 ③ 演示页 dark=True（深色组件底）、composite dark=False（浅色框架）。

**验证**：scope 类含 featuredeck 等 ✓；tool-directory 页 h1 色 rgb(245,244,239)（深色白字正确）✓；截图与主站 hero-mosaic 区一致（白 serif 大标题/深底/卡片网格/黄块）✓。

**部署**：7 页 v3 全部 200 publish。git 7785a0d6。

**git 结构真相**：MFlow Dev 的 `1-1 Harness` 是指向 `harness/` 的符号链接——git 只跟踪实体路径，"双树"实为单实体 + symlink 视图（此前部分文件消失的观感与此相关）。git 有 dev/Google Cloud Oath 等无关 staged 删除污染，commit 前需清理。
