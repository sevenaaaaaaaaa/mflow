---
profileName: NowX
postId: "3429"
postType: post
categories:
  - 69

tags: [AI, 视频]---
## Video Material GEN Workstation简介

**Video Material GEN Workstation** 是一个面向短视频创作者的本地化工作站，围绕“策划—生成—管理—预览”构建流程。整合 AI 文案、TTS 批量配音、(AI) 图片素材合成、ASR 字幕提取与自由创作等能力，帮助创作者在同一界面管理每期视频项目。

## Video Material GEN Workstation界面截图

### 模板化批量生成

按模板一键生成项目结构，脚本、图片素材（AI）、字幕与音频齐备，减少重复搭建与搬运。

### Gemini + TTS 合成

支持改写脚本与情绪化配音输出，满足解说类与剧情类短视频需求。

### 图文分轨管理与可视化预览

图片、字幕、音频分轨展示，可在前端替换元素并即时预览成片效果。

### 项目总览看板

以卡片管理批量项目，展示输出目录与创建时间，并提供快速删除与定位。

### 文案生成与提示词联动

结构化展示场景脚本，支持单条/整段复制；左侧勾选可联动右侧提示词面板。

### 字幕获取与 ASR

支持对接 **n8n-http-tools** 等工具实现字幕抓取；页面内置“字幕生成”按钮可调用第三方开源 ASR 代码产出剪辑所需的字幕文件。

### AI 图片生成与素材复用

集中管理角色/场景描述等提示词，勾选即可批量投入绘图任务；支持立绘、背景尺寸设置与历史记录复用。

### 提示词收藏与自由创作

收藏高频提示词，一键复制；提供自由创作面板进行自定义绘制。

### 素材生产与下游适配

已在 **NanoBanana** 与 **AIStudio 反向代理** 环境测试图像生成稳定，可作为如 *Sora* 等视频生成工具的上游素材来源。

## 快速上手

1. 复制 `env.example.yaml` 为 `env.yaml` ，填入 Gemini Key、Base URL、模型、TTS Key 与提示词等配置。
2. （可选）在 `env.yaml` 设置 `Default-Project-Root` ，用于存放自动生成的脚本、音频与图片文件。
3. 安装依赖： `npm install` 。
4. 启动服务： `npm start` 或双击 `start.bat` ，默认访问 `http://localhost:8765` 。

## 适用人群

- 短视频导演、编导、解说类创作者
- 新媒体/MCN 团队的脚本与素材生产岗
- 需要本地部署与批量管理能力的独立开发者

## 使用建议与限制

- 项目偏向项目与素材的 **管理与生产流程** ，成片质量取决于选题、脚本与镜头设计。
- 字幕抓取与部分文案流水线依赖 **n8n-http-tools** 等外部组件；ASR 为第三方开源实现。
- 请在遵守平台与版权规则前提下使用，避免上传或生成受版权保护的素材。
- 建议按项目建立清晰命名与版本规范，配合分轨预览提升修改效率。

## Video Material GEN Workstation开源与获取地址

GitHub地址： [https://github.com/Norsico/Video-Materials-AutoGEN-Workstation](https://github.com/Norsico/Video-Materials-AutoGEN-Workstation "Video Material GEN Workstation 开源地址")

本文链接： [https://www.ahhhhfs.com/77809/](https://www.ahhhhfs.com/77809/ "Video Material GEN Workstation｜AI短视频生成与项目管理一体化工作站")

### 相关

[ClipSketch AI：一键将视频瞬间转化为AI手绘故事板的创作神器](https://www.ahhhhfs.com/78072/ "ClipSketch AI：一键将视频瞬间转化为AI手绘故事板的创作神器")

[AI工具创意创作实操课程，AI短视频自媒体教程](https://www.ahhhhfs.com/77314/ "AI工具创意创作实操课程，AI短视频自媒体教程")

[船长AI原创+小红书教辅资料项目实操手册](https://www.ahhhhfs.com/74163/ "船长AI原创+小红书教辅资料项目实操手册")