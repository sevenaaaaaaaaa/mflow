---
slug: 02-wiki-custom-skills-guide

title: "创建自定义技能：在 Lovart 中自动化你的设计工作流"
date: 2027-07-21
author: "Lovart 文档团队"
category: "Wiki"
tags: ["自定义技能指南", "lovart 技能", "设计自动化", "AI 技能", "工作流自动化"]
keywords: ["自定义技能指南", "lovart 自定义技能", "设计自动化技能", "AI 设计工作流", "自定义设计管线", "lovart 自动化"]
description: "学习如何在 Lovart 中构建自定义技能——可复用的 AI 驱动工作流，自动化你最重复的设计任务。从自动图像背景移除到批量社交媒体尺寸调整，创建每周节省数小时的技能。"
image: "/assets/wiki/custom-skills-guide-hero.jpg"
reading_time: "8 分钟"
word_count: 1500
language: "zh"
---

# 创建自定义技能：自动化你的设计工作流

[图片 1 占位符 — 用户场景]

每个设计团队都有重复性任务——那些每周要做 50 次、累计消耗整个工作日的事情。自定义技能是 Lovart 的解决方案：可复用的 AI 驱动工作流，只需一次点击或一个简单的自然语言命令即可自动化这些任务。

可以把自定义技能想象成设计的宏���就像开发者编写脚本来自动化部署一样，你可以构建一个技能来自动化：“从这张主图生成 15 个社交媒体变体，应用我们的品牌套件，添加活动标签，并为每个平台导出为 @2x 的 PNG 文件。”一次点击，15 个文件，零手动工作。

本指南涵盖了完整的自定义技能系统——从简单的参数化命令到复杂的多步骤自动化管线。

---

## 什么是自定义技能？

[图片 2 占位符 — 概念图]

自定义技能是一个保存的设计操作序列，并集成了 AI 智能。技能可以：

- **接受输入：** 文本、图像、数据文件、品牌参考
- **应用转换：** 生成设计、修改元素、转换格式
- **遵循条件逻辑：** 基于输入特征的 if/then 分支
- **链式操作：** 按顺序执行多个步骤，每个步骤的输出作为下一步的输入
- **自动导出：** 保存到特定文件夹、格式和命名规则

### 自定义技能的构成

每个技能有四个组成部分：

```
技能: "社交媒体批量生成器"
├── 触发方式: 如何调用它（命令、按钮、API、计划任务）
├── 输入模式: 它需要哪些信息
├── 操作序列: 它做什么，一步步来
└── 输出配置: 它生成什么以及放在哪里
```

---

## 创建你的第一个技能

### 技能构建器界面

导航到 **技能 > 创建技能** 打开技能构建器。你有两种创建模式：

**可视化构建器（推荐初学者使用）：**
一个流程图风格的界面，你可以拖拽并连接操作块。每个块代表一个动作——生成、调整大小、添加文本、应用滤镜、导出等。

**代码构建器（高级用户）：**
使用 Lovart 的技能定义语言（SDL）编写技能，这是一种基于 YAML 的配置格式，嵌入了 AI 提示指令。

### 示例：“自动调整大小以适应 Instagram”

一个简单的技能，接受任何设计并为其调整大小以适应 Instagram 的三种格式。

**可视化构建器设置：**

```
块 1: "输入"
  类型: 图像上传
  标签: "上传你的设计"

块 2: "调整为信息流帖子尺寸"
  类型: 调整大小
  目标: 1080x1080
  适配: 覆盖
  位置: 居中
  应用品牌内边距: 是

块 3: "调整为快拍尺寸"
  类型: 调整大小
  目标: 1080x1920
  适配: 覆盖
  位置: 居中
  智能背景填充: 是（匹配品牌颜色）

块 4: "全部导出"
  类型: 导出
  格式: PNG-24 @2x
  命名: {{original_name}}_{{format}}.png
  目标: /Social/Instagram/

连接: 块 1 → 块 2 → 块 4
      块 1 → 块 3 → 块 4
```

**SDL 等效代码：**
```yaml
skill:
  name: "自动调整大小以适应 Instagram"
  description: "为 Instagram 信息流、快拍和 Reels 调整任何设计的尺寸"
  trigger:
    type: command
    phrase: "resize for instagram"
  inputs:
    - name: source_image
      type: image
      required: true
  operations:
    - id: resize_feed
      action: resize
      input: source_image
      params:
        width: 1080
        height: 1080
        fit: cover
        smart_padding: true
    - id: resize_story
      action: resize
      input: source_image
      params:
        width: 1080
        height: 1920
        fit: cover
        smart_background: brand_colors
  output:
    format: png
    scale_factors: [1, 2]
    naming: "{{source_name}}_{{operation_id}}"
    destination: "/Social/Instagram/"
```

---

## 技能触发方式

技能可以通过五种方式触发：

### 1. 命令触发
通过在 Lovart 界面中键入命令来调用技能：
```
/resize-instagram
/social-batch
/export-client-assets
```
命令支持自动补全和参数传递：
```
/social-batch --platforms=instagram,facebook,linkedin --campaign=summer-launch
```

### 2. 按钮触发
将常用技能固定为工作区工具栏中的按钮。一键点击即可使用默认参数执行技能。

### 3. 上下文菜单触发
右键点击任何设计，然后从你的技能列表中选择。技能会自动将点击的设计作为输入接收。

### 4. API 触发
通过编程方式调用技能：
```bash
curl -X POST https://api.lovart.ai/v2/skills/skill_abc123/execute \
  -H "Authorization: Bearer $LOVART_API_KEY" \
  -d '{"inputs": {"source_image": "design_xyz.png", "platforms": ["instagram"]}}'
```

### 5. 计划任务触发
设置技能按计划自动运行。适用于商业版和企业版计划。

```
计划: 每周一上午 9:00（美国东部时间）
技能: "每周社交媒体批量处理"
输入: 来自 /Marketing/Content Calendar/this-week.csv 的 CSV 文件
```

---

## 高级技能功能

[图片 3 占位符 — 真实 UI 截图]

### 条件逻辑

技能可以根据条件进行分支：

```yaml
operations:
  - id: detect_content_type
    action: ai_analyze
    input: source_image
    prompt: "将此图像分类为：product_photo, lifestyle, text_graphic 或 illustration"

  - id: product_workflow
    action: resize
    input: source_image
    params:
      background: white
      padding: 5%
    condition: "detect_content_type.result == 'product_photo'"

  - id: lifestyle_workflow
    action: resize
    input: source_image
    params:
      background: smart_blur
      padding: 0%
    condition: "detect_content_type.result == 'lifestyle'"
```

### AI 驱动操作

除了基本转换外，技能还可以包含 AI 操作：

**智能裁剪：** “裁剪此图像以聚焦产品，而非背景”
**背景移除：** “移除背景并替换为品牌渐变”
**文本生成：** “为此产品图像撰写一个引人注目的标题”
**风格迁移：** “将我们的编辑摄影风格应用于此图像”
**智能布局：** “将这 4 个产品排列成最赏心悦目的网格”

示例：“产品列表生成器”技能：
```yaml
operations:
  - id: remove_bg
    action: ai_remove_background
    input: product_photo

  - id: generate_background
    action: ai_generate_image
    prompt: "干净的摄影棚背景，带有柔和阴影，{{brand_name}} 美学，产品摄影灯光"

  - id: composite
    action: composite
    layers:
      - generated_background
      - product_photo_isolated

  - id: add_overlay
    action: add_text
    text: "{{product_name}}"
    font: "{{brand_headline_font}}"
    position: bottom_center

  - id: add_badge
    action: add_badge
    text: "{{discount_percentage}}% 折扣"
    condition: "discount_percentage > 0"
    position: top_right
```

### 循环操作

处理多个项目：

```yaml
operations:
  - id: for_each_product
    action: loop
    items: "{{csv_data.rows}}"
    operations:
      - action: generate_design
        template: product_card_template
        variables: "{{item}}"
      - action: export
        format: png
        naming: "{{item.sku}}_product_card.png"
```

### 并行执行

同时运行独立操作以提高速度：

```yaml
operations:
  - id: generate_all_variants
    action: parallel
    operations:
      - action: resize
        params: {width: 1080, height: 1080, label: "instagram_feed"}
      - action: resize
        params: {width: 1080, height: 1920, label: "instagram_story"}
      - action: resize
        params: {width: 1200, height: 628, label: "facebook_link"}
      - action: resize
        params: {width: 1200, height: 627, label: "linkedin_post"}
```

---

## 技能库与共享

### 团队技能库

你创建的技能默认保存到你的个人库中。将其提升到**团队库**以与你的工作区共享：

- **私有：** 只有你可以使用和编辑
- **团队共享：** 所有团队成员可以使用；只有你可以编辑
- **团队维护：** 所有团队成员可以使用；指定的维护者可以编辑
- **团队只读：** 所有团队成员可以使用；无人可以编辑（锁定技能）

### 社区技能市场

浏览并安装由 Lovart 社区创建的技能。技能会被评分和评价：

- **已验证技能：** 由 Lovart 团队创建或验证。带有蓝色勾选标记。
- **社区技能：** 由 Lovart 用户创建。安装前查看评分和使用次数。
- **高级技能：** 来自专业设计师和机构的付费技能。一次性购买，终身使用。

热门社区技能（截至 2027 年第三季度）：
- “电商产品套件” — 12 产品工作流（2,300+ 安装，4.9 星）
- “LinkedIn 轮播图构建器” — 将博客文章转换为 LinkedIn 轮播图（1,800+ 安装，4.8 星）
- “品牌刷新助手” — 将新品牌指南应用于现有资产（950+ 安装，4.7 星）
- “无障碍检查器专业版” — 全面的 a11y 审计与修复（1,200+ 安装，4.9 星）

---

## 技能调试与测试

### 测试模式

在生产环境中使用技能之前，先在测试模式下运行：

- **单步执行：** 一次运行一个操作，检查中间输出
- **样本数据：** 使用数据子集进行测试（5 个项目而非 500 个）
- **模拟运行：** 模拟执行而不实际生成文件。查看会发生什么。
- **操作日志：** 显示每个步骤输入/输出的详细日志

### 错误处理

定义技能在出现问题时如何表现：

```yaml
error_handling:
  on_image_load_failure: skip_and_continue
  on_ai_generation_failure: retry 3 times, then skip
  on_export_failure: halt_and_notify
  notification_channel: "#design-alerts"
```

### 技能分析

跟踪技能随时间推移的性能：
- 总执行次数（每日、每周、每月）
- 平均执行时间
- 成功/失败率
- 与手动执行相比节省的时间（估算）
- 每次执行消耗的 API 积分成本

---

## 技能示例库

### 示例 1：“客户交付包”
```
触发方式: 按钮（“准备客户交付”）
输入: 选中的设计（任意数量）
操作:
  1. 检查品牌合规性（标记违规）
  2. 将所有文件转换为客户偏好的格式
  3. 添加客户水印
  4. 生成交付清单 PDF
  5. 压缩所有文件
  6. 上传到客户门户
  7. 发送 Slack 通知
输出: 客户门户中的交付包 + 通知
```

### 示例 2：“广告创意 A/B 测试生成器”
```
触发方式: 命令: "/ab-test --headlines=headlines.csv --images=images/"
输入: 标题变体的 CSV 文件 + 图像文件夹
操作:
  1. 对于每个标题 × 图像组合：
     - 使用广告模板生成广告设计
     - 应用品牌套件
     - 添加 UTM 参数作为元数据
  2. 生成 A/B 测试矩阵报告
  3. 导出所有变体，命名规则：{{headline_id}}_{{image_id}}_variant.png
输出: 所有组合 + 测试矩阵 CSV
```

### 示例 3：“每周报告图表”
```
触发方式: 计划任务（每周五下午 4:00）
输入: Google Sheets 数据源（每周指标）
操作:
  1. 从 Google Sheets API 获取数据
  2. 生成 5 种图表类型（柱状图、折线图、环形图、对比图、指标卡片）
  3. 应用品牌图表样式
  4. 编译成演示就绪的幻灯片
  5. 导出为 PNG 集合 + PDF 文档
  6. 发布到 Slack #weekly-report 频道
输出: Slack 中的图表 + PDF 文档
```

---

## 入门指南

1. **识别一个重复性任务** — 记录你每周做 10 次以上的事情
2. **记录步骤** — 写下每一个动作，无论多小
3. **构建技能** — 从可视化构建器开始，在测试模式下迭代
4. **在影子模式下运行** — 让技能与你的手动工作并行运行一周
5. **比较输出** — 如果技能产生同等或更好的结果，则切换过去
6. **与团队共享** — 验证后提升到团队库

### 技能构建最佳实践

- **从小处着手** — 你的第一个技能应该有 3-5 个步骤，而不是 20 个

[图片 4 占位符 — 品牌行动号召]

- **命名清晰** — “Instagram 尺寸调整器”而不是“图像处理工具 v1”
- **添加描述** — 每个操作都应该有一个人类可读的目的
- **记录输入** — 指定技能期望什么数据以及以何种格式
- **为技能设置版本** — 升级时使用“社交批量 v2”并附上发布说明
- **测试边缘情况** — 空输入、错误格式、1,000 个项目 vs. 10 个项目

---

*自定义技能在专业版及以上计划中可用。社区技能市场对所有用户开放。高级技能需单独购买，不包含在计划定价中。技能执行会根据执行的操作消耗 API 积分。请参阅 docs.lovart.ai/skills 获取完整的 SDL 参考。*

### 附录：图片提示

**图片 1 — 用户场景**：
一位专业且平易近人的人坐在办公桌前，看着电脑屏幕试图创建设计时略显沮丧——温暖的自然光线，纪实风格

**图片 2 — 概念图**：
手绘草图，展示使用 AI 创建设计的逐步工作流——网格纸上的干净线条画，箭头连接每一步，极简风格

**图片 3 — 真实 UI 截图**：
[需要真实截图：Lovart ChatCanvas 界面，展示本文描述的关键功能——干净的 UI，不杂乱，带有可见结果]

**图片 4 — 品牌行动号召**：
Lovart AI 设计代理的专业品牌视觉——展示创建自定义技能：自动化你的设计工作流中描述的最终美丽设计结果——现代、有抱负、电影级灯光