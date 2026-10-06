# Round 26（2026-10-06）：比例修复 + 真实 Header/Footer 复刻完成

用户反馈：比例/缩放有问题；Header 导航与 Footer 没复刻。

**根因与修复**：
1. **比例问题** = 复刻页被 WP block theme constrained 布局（contentSize 800px）夹住，主站是 1400px 宽幅 → 新建 `templates/page-composite-replica-all.html`（slug 模板自动匹配），全宽布局 contentSize=1480px。
2. **Header/Footer** = 从 composite-page-all SSR 提取真实 HTML（header 10KB：sticky 导航 logo/Home/Solutions▾/Explore/Pricing/Get started；footer 11.7KB：三列链接+版权+深色切换+语言切换器），内嵌进模板文件（block 模板裸 HTML 原样输出），资源 URL 绝对化、script 剥离。
3. **细节**：header/按钮下划线清除（WP 默认 a 下划线，主站无）。

**验证**：真实 header 输出 ✓（lovart-site-header/Home/Get started）；Footer 三列完整 ✓；宽幅 hero 与主站同构 ✓。遗留：WP 导航 Solutions▾ 下拉交互为主站 JS（静态展示）；header 内 a 下划线在部分链接仍残留（hover 态），下批统一。
