---
profileName: NowX
postId: "3455"
postType: post
categories:
  - 69

tags: [下载]---
## Stacks 是什么

Stacks 是一款专为 **Anna’s Archive** 打造的下载队列管理器，通过简洁的 Web 控制台完成电子书的排队、管理与自动下载。它支持 Anna’s Archive 的高速下载 API，并在不可用时自动切换镜像站，保持下载过程稳定顺畅。

系统以容器化方式运行，几乎不需要维护，适合自托管用户、重度电子书读者与数字资料收集者。


---

## 核心亮点

### 🖥 Web 操作面板

提供密码保护的管理界面，可查看任务、进度、历史与系统状态，并支持会话管理与自动登录保护。

### 📚 下载队列管理

浏览器中一键加入下载任务，自动排序、自动重试，中断后可继续，减少人工干预。

### ⚡ 快速下载支持

适配 Anna’s Archive 会员的高速下载 API，让电子书以更快的速度获取。

### 🔄 自动镜像切换

当高速下载不可用时自动切换到镜像，下载不中断。

### 📊 实时监控

使用 Dracula 主题界面呈现队列、进度与历史记录，下载状态清晰可见。

### 🔌 浏览器集成

提供 Tampermonkey 脚本，在 Anna’s Archive 页面上直接生成下载按钮，省去手动复制链接。

### 🐳 Docker 随时部署

通过 Docker Compose 或 Docker CLI 一键启动，无需复杂配置。

---

## 通过 Docker 快速部署

### 使用 docker-compose（推荐）

创建 `docker-compose.yaml` ：  
（文本已在原文给出，内容无需重复演示）

修改路径、端口后执行：

```
docker compose up -d
```

安装完成后可通过 [http://localhost:7788](http://localhost:7788/) 访问 Web 控制台。

---

## 使用 Docker CLI

手动创建所需目录并运行：

```bash
docker run -d \
  --name stacks \
  -p 7788:7788 \
  -v /path/to/config:/opt/stacks/config \
  -v /path/to/download:/opt/stacks/download \
  -v /path/to/logs:/opt/stacks/logs \
  -e USERNAME=admin \
  -e PASSWORD=stacks \
  -e TZ=UTC \
  --restart unless-stopped \
  zelest/stacks:latest
```

用户名与密码仅首次生效；后续可通过配置文件修改。

---

## 初次使用指南

- 浏览器访问 Web UI 并登录
- 更改默认密码
- 复制 API 密钥，用于 Tampermonkey
- 配置高速下载 Key（如有）
- 设置下载延迟、重试次数等
- 保存设置即可开始使用

---

## 安全机制

Stacks 在自托管环境加入了多层安全保护：

- Bcrypt 密码加密
- HTTPOnly Cookie + SameSite
- 登录失败锁定机制
- 32 位安全 API Key
- 自动生成会话密钥
- 不建议暴露到公网，如需远程访问建议搭配 VPN 或反向代理 + HTTPS

---

## Stacks开源链接地址

GitHub地址： **[https://github.com/zelestcarlyone/stacks](https://github.com/zelestcarlyone/stacks "Stacks")**

适用于希望高效下载电子书、批量管理任务和提升资料获取效率的用户。