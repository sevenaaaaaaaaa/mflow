---
title: "Rotato：Mac 3D 设备样机与动效工具"
slug: rotato-mac-3d-mockup-tool
date: 2026-05-29
updated: 2026-05-29
tags: [Rotato, Mac, 3D, 样机, 动效, 设计工具]
categories: [设计工具]
summary: Rotato 是 macOS 上的 3D 设备样机与动效工具，用于 App 展示图与宣传短视频。已从官网 DMG 安装至应用程序，Pro 约 $239/年；与 ClipSketch、html-anything 等创作链互补。
focus_keyword: Rotato
source: https://rotato.app
author: Morten Just (mortenjust)
status: draft
---

# Rotato：Mac 3D 设备样机与动效工具

> 已安装 v154 | 官网 DMG | Apple 公证 | 非开源

## 这是什么

[Rotato](https://rotato.app) 是面向 **Mac** 的 **3D mockup / 动效** 工具：把 App 界面、截图或设计稿放进 iPhone、MacBook 等 3D 设备模型，导出高质量**静态图**或**短视频**，用于 Product Hunt、App Store 预览、社媒宣传。

另有在线端：[app.rotato.app](https://app.rotato.app)

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 独立开发者、设计师做 App 宣传素材 | ✅ 推荐 | 比 AE/Blender 上手快 |
| 需要快速出设备样机视频 | ✅ 推荐 | 内置动效与导出 |
| Windows / Linux 用户 | ❌ 不适用 | 仅 macOS 桌面端 |
| 预算为零且只需静态截图 | ⚠️ 酌情 | Pro 付费；可先试用应用内免费能力 |
| 开源可脚本化批量 | ❌ 另选 | 闭源商业软件 |

## 安装与前置条件

- **平台**：macOS（Apple Silicon / Intel）
- **Homebrew**：无官方 `rotato` cask
- **官方渠道**：https://rotato.app/download → `https://download.rota.to/Rotato-latest.dmg`

```bash
# 等价于：下载 DMG → 挂载 → 拖入「应用程序」
curl -fL -o /tmp/Rotato-latest.dmg "https://download.rota.to/Rotato-latest.dmg"
# 在 Finder 中打开 DMG 安装，或 ditto 到 /Applications/Rotato.app
open -a Rotato
```

**本机状态（2026-05-29）：** 已从官方 DMG 安装至 `/Applications/Rotato.app`，版本 **154**，Bundle ID `com.mortenjust.Rendermock`，已通过 **Notarized Developer ID** 公证。

## 核心用法

1. 打开 Rotato，选择设备模型（iPhone / Mac 等）
2. 导入 App 截图或录屏素材
3. 调整角度、背景、动效曲线
4. 导出 PNG / MP4 等格式用于落地页与社媒

具体功能以应用内为准；Pro 计划含更多设备与导出选项。

## 注意事项与风险

- **许可**：Pro 等方案为**付费订阅/买断**（官网 [Pricing](https://rotato.app/pricing) 可见例如 **约 $239/年** 等档位，以官网实时价格为准）
- **首次启动**：可能需在应用内登录/购买；若被拦截请到「系统设置 → 隐私与安全性」允许打开
- **非开源**：无法审计或自托管；素材版权自行负责
- **与 AI 生成**：Rotato 不做 AI 绘图；可配合 [[../01-AI-Agent生态/ClipSketch AI：视频瞬间转手绘故事板]]、[[../01-AI-Agent生态/html-anything：AI 时代的 HTML 编辑器]] 的产出再套样机

## 与你现有工具的关系

| 工具 | 关系 |
|------|------|
| [[../01-AI-Agent生态/ClipSketch AI：视频瞬间转手绘故事板]] | AI 分镜/封面 → Rotato 套设备样机发布 |
| [[../01-AI-Agent生态/html-anything：AI 时代的 HTML 编辑器]] | HTML 长文/卡片 → 截图进 Rotato |
| [[../01-AI-Agent生态/3DCellForge：AI 驱动的 3D 模型工作室]] | AI 生成 3D 资产；Rotato 偏**设备 mockup 模板** |
| [[DESIGN.md：AI 写前端的新语法——用 Markdown 定义视觉风格]] | 先定视觉规范再导出进样机 |

## FAQ

### Q: 能用 Homebrew 装吗？
A: 目前无官方 cask，请用官网 DMG。

### Q: 和 Screen Studio / CleanShot 区别？
A: Rotato 专注**3D 设备外壳 + 动效**；录屏工具不做 mockup 场景。

### Q: 已安装但打不开？
A: 检查公证与「隐私与安全性」；或 `open -a Rotato` 从终端启动看报错。

## 相关链接

- 官网：https://rotato.app  
- 下载：https://rotato.app/download  
- 定价：https://rotato.app/pricing  
- 在线版：https://app.rotato.app
