# GitHub 仓库图片抓取流程

## 目标
为文章中每个 GitHub 项目获取一张主图（banner/screenshot/OG preview），用作文章介绍图。

## 抓取优先级（从高到低）

### 1. README 内嵌图片
```bash
# 用 GitHub API 获取 README HTML
curl -sL -H "Accept: application/vnd.github.v3.html" \
  "https://api.github.com/repos/{owner}/{repo}/readme"

# 提取 img src（含相对路径）
# 相对路径转绝对：https://raw.githubusercontent.com/{owner}/{repo}/main/{path}
```

### 2. assets/ 或 docs/ 目录
```bash
# 列出目录内容
curl -sL "https://api.github.com/repos/{owner}/{repo}/contents/assets"
curl -sL "https://api.github.com/repos/{owner}/{repo}/contents/docs"
curl -sL "https://api.github.com/repos/{owner}/{repo}/contents/public"

# 筛选图片文件：.png/.jpg/.jpeg/.gif/.webp/.svg
# 优先选择：banner > screenshot > architecture > logo
```

### 3. GitHub 社交预览图（OG Image）
当仓库没有 README 图片时，使用 OG 预览图：
```
https://opengraph.githubassets.com/1/{owner}/{repo}
```
这是 GitHub 自动生成的社交预览图，包含项目名+描述+Logo，质量稳定。

## 常见坑

| 坑 | 说明 |
|---|---|
| `raw.githubusercontent.com` 的 logo.png 可能 404 | 有些仓库的 docs/ 图片是通过 HTML `<img>` 引用的相对路径，但实际文件不在 main 分支。**始终先检查文件大小 > 1KB** |
| shields.io badges 不是项目图 | 过滤掉 `shields.io`、`badge`、`mobaicons`、`typing-svg`、`capsule-render` 等装饰性 URL |
| `.webp` 格式 | 部分平台（微信公众号、百家号）不支持 webp，需要转 png/jpg |
| OG 图片分辨率 | GitHub OG 图通常是 1280×640，适合作为文章头图 |

## 下载命令模板
```bash
curl -sL --max-time 20 -o "article-images/{slug}.{ext}" "{url}"
# 验证：wc -c < file （> 1000 bytes = 有效）
```

## 图片 URL 选择策略

发布到不同平台时，图片引用方式不同：

| 平台 | 图片引用方式 |
|------|------------|
| GitHub Issues / DEV.to / Medium | 直接用 GitHub raw URL（`raw.githubusercontent.com`） |
| Blogger / WordPress | 先下载，再上传到平台媒体库 |
| 知乎 / 掘金 / 51CTO | 上传到平台图片服务（有些不支持外链图片） |
| 百家号 / 大鱼号 | 必须上传到平台，不支持外链图片 |
| 什么值得买 | 支持外链图片 |
