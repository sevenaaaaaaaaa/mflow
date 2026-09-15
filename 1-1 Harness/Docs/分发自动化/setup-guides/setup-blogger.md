# Google Blogger 配置

Blogger API v3 支持 OAuth2 自动发文，比 Medium 的 Integration Token 对新账号友好。

## 1. 创建 Blogger 博客

1. 打开 [blogger.com](https://www.blogger.com/) → 创建博客（可用子域名 `xxx.blogspot.com`）
2. 记下博客 URL

## 2. Google Cloud 项目

1. [Google Cloud Console](https://console.cloud.google.com/) → 新建项目
2. **APIs & Services → Library** → 搜索 **Blogger API** → Enable
3. **APIs & Services → Credentials → Create Credentials → OAuth client ID**
   - Application type：**Desktop app**
   - 下载或复制 Client ID / Client Secret

## 3. 获取 Refresh Token（一次性）

在终端运行（替换 `YOUR_CLIENT_ID`）：

```bash
open "https://accounts.google.com/o/oauth2/v2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&scope=https://www.googleapis.com/auth/blogger&access_type=offline&prompt=consent"
```

1. 浏览器登录 Google 账号并授权
2. 复制页面上的 **authorization code**
3. 换 token：

```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=PASTE_CODE_HERE" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob"
```

响应里的 `refresh_token` 只出现一次，务必保存。

## 4. 写入 `.env`

```bash
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REFRESH_TOKEN=...
BLOGGER_BLOG_ID=          # 下一步获取
```

## 5. 查 Blog ID

```bash
node scripts/publish-blogger.js --list-blogs
```

把 `id=` 填入 `BLOGGER_BLOG_ID`。

## 6. 验证 & 发布

```bash
node scripts/publish-blogger.js --draft drafts/blogger-ai-logo-design-guide.md --dry-run
node scripts/publish-blogger.js --draft drafts/blogger-ai-logo-design-guide.md
```

## Gate 0

- 发摘要稿，非主站全文
- 文末 canonical 链 `lovart.ai`（脚本自动追加 footer）
- Blogger 无原生 canonical 字段，靠 footer + 不同标题防抢权重
