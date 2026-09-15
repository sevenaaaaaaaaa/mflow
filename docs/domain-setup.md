# 通过域名访问 MFlow

> 前提：你拥有一个域名（如在 Cloudflare/阿里云/Namecheap 管理的 `yourdomain.com`）。
> 目标：`https://mflow.yourdomain.com` 访问工作台（自动 HTTPS）。

## 三步接入

### 第 1 步 · DNS 解析（你来做，约 1 分钟生效-24h 不等）

在域名的 DNS 管理里加一条 A 记录：

```
主机记录: mflow
类型:     A
记录值:   172.96.253.73
```

验证：`dig +short mflow.yourdomain.com` 返回 `172.96.253.73` 即生效。

### 第 2 步 · 服务器配置反代（一条命令）

SSH 到服务器后执行（把域名换成你的）：

```bash
bash /var/www/mflow/deploy/setup-domain.sh mflow.yourdomain.com
```

脚本做的事：在宝塔 Apache 加一个 **基于域名的虚拟主机**（不影响现有站点与 8088 直连端口），
把 `http://mflow.yourdomain.com` 反向代理到 MFlow 工作台。

### 第 3 步 · HTTPS 证书（二选一）

- **宝塔面板**（推荐，点几下即可）：面板 → 网站 → 对应站点 → SSL → Let's Encrypt 申请 → 开启强制 HTTPS
- **acme.sh 命令行**：
  ```bash
  curl https://get.acme.sh | sh -s email=you@example.com
  ~/.acme.sh/acme.sh --issue -d mflow.yourdomain.com -w /www/server/apache/htdocs
  ~/.acme.sh/acme.sh --install-cert -d mflow.yourdomain.com \
    --key-file /www/server/apache/conf/ssl-key-mflow.pem \
    --fullchain-file /www/server/apache/conf/ssl-crt-mflow.pem \
    --reloadcmd "/www/server/apache/bin/apachectl -k graceful"
  ```
  然后取消 `deploy/setup-domain.sh` 生成文件里 443 段的注释。

## 安全提醒

公网域名 + HTTPS 后，工作台任何人可触达（有密码保护）。建议：
1. 立即把 `run/env.sh` 的 `MFLOW_CONSOLE_PASSWORD` 换成强密码并 `systemctl restart mflow-console`
2. 若只给自己用，可在宝塔对该站点再加一层 Basic Auth（网站 → 配置 → 密码访问）

## 没有域名？

现状 `http://172.96.253.73:8088` 已可用（有密码保护）。建议至少：改强密码 + 仅在可信网络使用。
