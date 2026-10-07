# Round 28b（2026-10-06）：blogs.lovart.ai 生产部署完成（浅色版）+ 深色模式受挫记录

**部署突破**：blogs 站从**服务器侧可达**（本机被主机层 reset，172.96.253.73 侧 1 秒通）→ 凭证（Seven/wp-auth.local.env）登录会话 + REST nonce → **REST API 创建复刻页成功**：https://blogs.lovart.ai/composite-replica-all（id 18214, published, 33 组件 + 内嵌 <style> 全量 CSS + 双 Header/Footer）。

**wp:html 块方案确立**：非区块内容经 REST 写入会被 wpautop 破坏 CSS（换行插 <p>）——`<!-- wp:html -->` 块包裹绕过（CSS 单行化双保险）。CSS 完整存活验证（多位置抽查）。

**深色模式受挫（诚实记录）**：三轮尝试均失败——①body dark 类（diag 显示变量翻转但视觉未对齐）②.page-id-7 作用域深色变量（被未分层浅色定义覆盖）③字面值深色 overlay（灾难：浅色主题文字被染白→不可见）→ **已回滚**。根因认知：深浅色是整页级 token 体系，部分深色化必灾难；正确路径 = 主题级完整移植（lovart-theme-0.1.0.zip 含深色机制）但 blogs 站 DISALLOW/权限待解（update.php 403"链接已过期"实为权限/安全层拦截）。

**当前生产状态**：复刻页浅色模式可用（结构/内容/双 Header/Footer 1:1；深色模式待主题部署）。**部署通道已打通**（登录会话+REST，脚本 /tmp/deploy-update.sh 模式可复用）。
