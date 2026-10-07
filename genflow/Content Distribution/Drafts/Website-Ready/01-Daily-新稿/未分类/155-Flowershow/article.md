---
profileName: NowX
postId: "3431"
postType: post
categories:
  - 87

tags: [笔记]---
Flowershow 是一个基于 Obsidian 的整体发布服务，它可以将你的 Obsidian 笔记按照目录结构，转换为一个在线的数字花园网站。你可以借助 Vercel 来免费发布你的 Obsidian 中的内容。

[🔗 Flowershow 官网](https://flowershow.app/)

![
Flowershow 官网](https://cdn.utgd.net/assets/uploads/2024/04/FG-062355-C.png)

Flowershow 官网

相关阅读：如果你在找一个简单的“单篇笔记的发布方案”，你可以阅读这篇文章： [利用 Github Gist 快速分享 Obsidian 笔记](https://utgd.net/article/20163) 。

## 准备工作

- GitHub 账号
- Vercel 账号（ [Vercel 官网](https://vercel.com/) ）
- Obsidian 本地软件

GitHub 和 Obsidian 相信大家都很熟，而 Vercel 是一个针对前端的云服务，它实现了通过 Github 免服务器快速部署前端服务，每次提交内容都会触发一次自动部署。

更多的技术细节你不用了解，Flowershow 已经实现了大部分操作。

## 第一步：准备 Obsidian 仓库

要开始构建你的 Flowershow 网站，首先得有一个 Obsidian 库作为基础。

提示：虽然 Flowershow 对现有仓库没有什么破坏性操作，但我还是建议你在 Obsidian 中新建一个仓库进行部署和体验后，再决定要不要对现有的库进行发布。

![
创建一个新的库](https://cdn.utgd.net/assets/uploads/2024/04/FG-070001-X.png)

创建一个新的库

### Obsidian 目录结构要求

关于 Obsidian 库的目录结构，Flowershow 对仓库的结构要求并不高，可以称得上是自由。

在你的 Obsidian 库中，可以自由创建子文件夹以组织你的笔记和文件。这些文件夹的结构将会直接映射到你网站 URL 的路径上。例如，一个名为 `my-digital-garden/blog/hello.md` 的文件将会在你的网站以 `<网站网址>/blog/hello` 的形式展现。

每个文件夹中，你都可以创建一个 `index.md` 文件作为该目录的索引页。比如， `my-content/blog/index.md` 将作为博客目录的首页，网址将会是 `<网站网址>/blog` 。

### 关于附件的处理

为了让你的 Markdown 文件更加丰富，你可能需要嵌入图片或 PDF 文件。

为此，应在库的根目录下创建一个名为 `assets` 的文件夹，用于存放这些资源。Obsidian 允许你通过简单的拖放操作，将图片直接粘贴到笔记中。如果你希望这些图片自动保存到 `assets` 文件夹，可以在左侧边栏中右键点击 `assets` 文件夹，选择 “设置为附件文件夹” 的选项。

如果你之前习惯于直接将图片保存在库的根目录下或以其他形式保存，记得将它们移动到新建的 `assets` 文件夹中。

提示：Flowershow 表示，未来有计划支持“在库中任意位置保存图片”的功能，但现在仍然需要进行上述步骤。

## 第二步：复制 Flowershow 仓库，用 Vercel 部署

要将你的 Obsidian 仓库发布到网络上，首先需要将 Flowershow 仓库复制到你的 GitHub 账户中。

[🔗 Flowershow 模板仓库](https://github.com/datopian/flowershow)

这个仓库是一个应用模板，包含了构建网站所需的全部代码。未来你从 Obsidian 库中发布的所有笔记，都将被推送到这个仓库的 `/content` 目录下。

![
推荐使用 Vercel 一键部署](https://cdn.utgd.net/assets/uploads/2024/04/FG-070000-S.png)

推荐使用 Vercel 一键部署

具体操作方法如下：

1. 点击文档中的 Deploy 按钮，就会跳转到 Vercel 页面。Vercel 将会帮助你将仓库复制到 GitHub 账户中，并为你设置好持续部署。
2. 在 Vercel 页面用 Github 账号进行登录。
3. 之后，你可以选择你的 GitHub 账户作为范围，并为你的 Flowershow 网站仓库命名。
![
Vercel 部署](https://cdn.utgd.net/assets/uploads/2024/04/FG-070003-x.png)

Vercel 部署

完成点击 “Create” 后，耐心等待 GitHub 仓库创建并在 Vercel 上部署完成。

![
Vercel 部署成功](https://cdn.utgd.net/assets/uploads/2024/04/FG-070000-4.png)

Vercel 部署成功

部署成功后，你可以进入 Dashboard，点击 Visit 按钮，访问并查看你的网站。这个时候网站应该已经完成部署。

![
访问部署后的网页](https://cdn.utgd.net/assets/uploads/2024/04/FG-070000-t.png)

访问部署后的网页

只是由于没有内容，此时网站上还是一片空白，接下来就要从 Obsidian 仓库发布文章。

## 第三步：安装并配置 Flowershow 插件

当你的 Flowershow 仓库已经复制完成并且网站已经部署好之后，下一步就是确保你的 Obsidian 笔记能够与仓库中的 `/content` 文件夹保持同步。这时候，Obsidian 的 Flowershow 插件就发挥重要作用了。

要在你的 Obsidian 库中安装这个插件，首先点击 Obsidian 界面左侧边栏最上方的⚙️图标，进入设置界面，然后选择 “社区插件” 选项卡。（如果你之前没有启用社区插件，可能需要先进行启用才能继续）

在社区插件列表中，找到 “Flowershow” 插件，然后进行安装并启用。

![
下载并安装 Flowershow 插件](https://cdn.utgd.net/assets/uploads/2024/04/FG-070002-f.png)

下载并安装 Flowershow 插件

安装完成后，为了使插件能够访问你的 GitHub 上的 Flowershow 仓库，你需要一个 GitHub 个人访问令牌。

这个令牌可以通过访问你的 GitHub 账户设置中的“开发者设置”然后选择“个人访问令牌”来生成。点击“生成新令牌”按钮，为你的令牌命名，并确保选择了“repo”范围的权限。

你可以参考此文档找到更详细的步骤： [Personal access tokens (classic)](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#personal-access-tokens-classic)

![
获取 Github 令牌](https://cdn.utgd.net/assets/uploads/2024/04/FG-070001-h.png)

获取 Github 令牌

生成令牌后，将其复制并粘贴到 Obsidian 中 Flowershow 插件的设置里的 Github token 中，同时输入你的 GitHub 用户名、你的 Flowershow 网站仓库的名称。

![
填写 Github 地址信息](https://cdn.utgd.net/assets/uploads/2024/04/FG-070001-E.png)

填写 Github 地址信息

至此，Flowershow 插件已经与你的 Flowershow 网站仓库成功绑定。

## 第四步：发布你的笔记

使用 Flowershow 插件，你可以通过两种方式将你的笔记发布到网站上。

### 使用 Flowershow 命令

- 通过 Obsidian 命令面板中的 Flowershow 命令
- 在 Obsidian 的界面上方点击 `>_` 图标打开命令面板，然后搜索以“Flowershow”为关键词的命令。

你会看到两个选项：

- Flowershow: 发布所有笔记 - 顾名思义，这个命令将会发布你所有的笔记。
- Flowershow: 发布单个笔记 - 这个命令只会发布当前打开且处于激活状态的单个笔记。

### 使用 Flowershow 发布状态操作面板

点击 Obsidian 侧边栏最左侧的🌱图标，这将打开 Flowershow 发布状态操作面板。在这里，你可以看到你的所有笔记的发布状态，包括已发布、已更改但未更新发布、尚未发布以及已从库中删除但在网上仍显示的笔记。

你可以使用每个分类旁边的按钮来更新、发布或从你的网站上删除笔记。

![
发布状态操作面板](https://cdn.utgd.net/assets/uploads/2024/04/FG-070003-e.png)

发布状态操作面板

提示：目前 Flowershow 还不支持“按文件夹发布”的操作，未来可能会更新。目前可以通过本文最后一节的“避免发布某些文章的方法”章节来手动控制单篇文章是否发布。

发布成功后，你的笔记将会在你的 Flowershow 网站上实时显示。发布过程完成后，你的网站将会自动开始构建，这个过程可能会根据你的 Obsidian 库的大小消耗几秒到几分钟的时间。

到这一步为止，部署环节已经全部完成了！

**TIP：为什么我的首页还是显示 404？**

如果你已经全部按照前面的步骤执行了，但是访问链接时，只看到了一个纯色背景的 404 页面，那是因为你的文件目录位置不正确，参考本文的“Obsidian 目录结构要求”部分重新整理的你的 Obsidian 目录结构，然后再次进行发布。

在调试阶段，你也可以选择直接访问特定的网址先看看效果，比如通过“网站网址/blog/”来访问“blog/”目录中的内容。

## 第五步：配置网站

如果只是部署完成，还是会有不少不令人满意的细节，比如顶部没有任何导航栏、文章页没有作者和目录等问题。你一定想知道如何调整这些内容。

Flowershow 的结构是两个部分： **Github 仓库提供前端页面、Obsidian 提供内容** 。所以，对前端的修改，你需要在 Github 仓库内修改，对单篇内容的修改，你需要在 Obsidian 内修改和发布。

### 配置文件的修改方法

首先，Flowershow 的文档中多次提到一个 `config.mjs` 配置文件，很多对界面的自定义操作都是在这里完成的。

所以， **你应该在你自己的 Github 仓库中，在 content 位置找到 `config.mjs` 这个文件，进行修改和更新。**

![
config.mjs 配置文件的位置](https://cdn.utgd.net/assets/uploads/2024/04/FG-062354-P.png)

config.mjs 配置文件的位置

官方提供了一个配置示例如下，你需要根据自己的需要进行修改。

```js
const config = {

  title: "My Awesome Blog",

  description: "This is my awesome blog built with Flowershow",

  author: "John",

  logo: "/images/logo.svg",

  domain: "https://john.app/",

  // 链接到你想要显示的网页，这会显示在导航栏和页脚

  navLinks: [{ href: "/about", name: "About" }],

};

export default config;
```

所以你差不多可以得到这个样式的网页——

![
发布后的文章列表页](https://cdn.utgd.net/assets/uploads/2024/04/FG-062353-H.png)

发布后的文章列表页

- 本段扩展阅读： [Flowershow 基本信息配置的方法](https://flowershow.app/docs/config)

### 文章内容的修改方法

其次，本地的 Obsidian 仓库并不是实时展示到网页上的。

当你在 Flowershow 插件中点击“发布”后，实际上是做了一次 Github 的提交动作，将选中的文章推送到了“第二步中复制到你账户名下的 Flowershow 仓库”的 content 文件夹中。

由于 Flowershow 已经自动化处理了整个流程。所以， **如果你要修改网站的文章内容，应该在 Obsidian 中修改并发布，而不是在 Github 的 content 仓库中直接修改。**

网页中会显示你本地文章中的 frontmatter 元数据信息，你应该给需要发布的文章都加上这些信息，这样可以确保文章页面的美观性。

```
---
title: 【文章标题】
date: 2022-11-29
authors: [作者1, 作者2]
---

文章正文
```

最终的文章页大致是这个样子——

![
发布后的文章详情页](https://cdn.utgd.net/assets/uploads/2024/04/FG-062353-U.png)

发布后的文章详情页

## 可选：如何自定义页面

Flowershow 其实还支持很多细节设置，我更推荐你查阅 [Flowershow 官方文档](https://flowershow.app/docs) ，比如如何自定义主题、CSS、404 页面，甚至是支持 SEO、全文搜索、可视化数据等等。其中有些高级的操作是需要你有一定的开发能力的，但基础的操作只需要修改配置文件和修改文章的 Frontmatter 就可以实现了。

### 展示侧边栏的方法

在 Github 的 content 目录中，修改 `config.mjs` ，在其中添加这样的配置信息。

```js
// config.mjs

const config = {

  showSidebar: true,

};
```

对于单篇文章，可以用 frontmatter 进行修改。

```
---
showSidebar: false
---
```
- 本段扩展阅读： [Flowershow 展示侧边栏的方法](https://flowershow.app/docs/site-wide-toc)

### 配置默认作者的方法

对于大多数个人用户而言，个人 Obsidian 的作者都是一个人，那你可以在你自己名下的 Flowershow Github 仓库中，找到 `content/config.mjs` 文件，添加一行 `defaultAuthor` 配置，编辑并提交。

```
...
defaultAuthor: "【替换为作者名称】"
...
```

### 避免发布某些文章的方法

如果你想避免发布某篇文章，可以在单篇文章中，在 `frontmatter` 中添加 `isDraft: true` 进行修改。只有非草稿的文章才会被发布。

```
---
isDraft: true
---
```

### 更多的高级自定义功能

由于 Flowershow 是由 React 框架下的 Next.js 编写的，并且以源码形式提供给你。所以它的可扩展性非常强，如果你有前端开发的能力，应该很容易以这个项目为基础，进行大刀阔斧的自定义。

比如官方文档中提到的 [“可视化数据”功能](https://flowershow.app/docs/data-visualization) ，就是推荐你用前端开发的方式，引入一个 portaljs 的包，利用其中的 LineChart 组件来在前端展示数据。

### 了解 Flowershow 的一些隐性限制

最后，你可能还需要了解这个方案的限制，由于 Flowershow 完全依赖于 Github Action 和 Vercel，它们可能会对仓库和项目有多方面的限制，还有一些网络访问层面的问题。

由于目前 Flowershow 的插件本身也是依赖于 Github 的，所以无法完全脱离 Github，但你可以尝试自行改进 Action 部署的操作，改为部署在自己的服务器上。替换掉 Vercel 也许可以改进国内的访问速度。

## 小结

目前为止，Flowershow 还在持续开发中，但是整体的完成度已经相当不错了。

如果你希望把 Obsidian 的内容作为自己的数字花园发布出来，Flowershow 无论是观感和体验上都很值得一试。

本文的部署部分很大程度上参考了 [Flowershow 官方指南文档](https://flowershow.app/docs/publish-howto#prepare-your-obsidian-vault) ，因为它已经介绍的很全面了。 [官方文档页面](https://flowershow.app/docs) 也提供了更详细的自定义方法，如果你准备好好打理一下你的数字花园，可以详细阅读一下其中的内容，做更进一步的定制化。