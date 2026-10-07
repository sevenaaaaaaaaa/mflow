# 如何找到 HASHNODE_PUBLICATION_ID

Publication ID **不是**你的用户名，也 **不是**博客域名，而是一串内部 ID。

## 方法 1：从 Dashboard URL 复制（最简单）

1. 登录 [https://hashnode.com](https://hashnode.com)
2. 右上角头像 → **Blogs**（或打开 [https://hashnode.com/dashboards](https://hashnode.com/dashboards)）
3. 点你要发文的那本博客的 **Dashboard**
4. 看浏览器地址栏：

```
https://hashnode.com/6f8a9b2c1d4e5f6789012345/dashboard
                      ^^^^^^^^^^^^^^^^^^^^^^^^
                      这就是 HASHNODE_PUBLICATION_ID
```

5. 写入 `.env`：

```bash
HASHNODE_PUBLICATION_ID=6f8a9b2c1d4e5f6789012345
```

## 方法 2：博客设置里查看

部分账号在 **Blog settings → General** 底部会显示 Publication ID。

## 注意（2026）

Hashnode 已将 GraphQL API 改为 **Pro 付费** 才能读写。若 API 调用失败，需在该博客 Dashboard → **Billing → Upgrade to Pro**。

没有 Pro 时，可暂时用 **crier** 或 **手动** 发 Hashnode，或先从工作流去掉 hashnode。
