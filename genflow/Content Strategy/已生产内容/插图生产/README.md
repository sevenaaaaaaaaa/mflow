# Lovart 博客插图生产项目

> 项目状态：提示词已导出，待设计师生产 | 最后更新：2026-05-11

---

## 一、项目概况

| 指标 | 数量 |
|------|------|
| 博客文章总数 | 705 篇 |
| 需 AI 生成图片 | **2,115 张**（每篇 3 张） |
| 需人工截屏 | **705 张**（每篇 1 张 REAL UI） |
| 图片总量 | **2,820 张** |

### 三种图片类型

| 类型 | 数量 | 说明 | 生产方式 |
|------|------|------|---------|
| **IMAGE 1 — Persona Scenario** | 705 张 | 文章目标读者的真实工作场景图 | AI 生成（Nano Banana Pro） |
| **IMAGE 2 — Conceptual Diagram** | 705 张 | 手绘风格的工作流/概念草图 | AI 生成（Nano Banana Pro） |
| **IMAGE 3 — Real UI Screenshot** | 705 张 | Lovart 产品界面截图 | **人工截屏** |
| **IMAGE 4 — Brand CTA** | 705 张 | 品牌视觉/CTA 图 | AI 生成（Nano Banana Pro） |

---

## 二、文件位置

```
LifeOS Pro PARA Vault/
└── 1-Project/Content Marketing/Content Calendar/已生产内容/
    └── opencode-Lovart-内容日历/
        └── 已生产内容/
            ├── 博客文章/                          ← 705 篇（已含占位符）
            ├── 落地页与资源/                      ← 129 篇（不需插图的落地页）
            │
            ├── 插图生产/                          ← 设计师从这里开始
            │   ├── IMAGE_PROMPTS_ALL_2115.csv    ← 全部提示词（CSV）
            │   ├── IMAGE_PROMPTS_BY_TYPE.md       ← 按类型分组预览
            │   └── README.md                      ← 本文件（待复制）
            │
            ├── 已生产图片/                         ← 设计师产图放这里
            │   └── (待放入图片文件)
            │
            └── insert_images.py                   ← 批量回插脚本
```

---

## 三、设计师工作流

### 3.1 准备

1. 打开 `插图生产/IMAGE_PROMPTS_ALL_2115.csv`
2. 在 CSV 中按 `image_type` 列筛选，同类图片可连续生产（风格更统一）
3. 推荐生产顺序：**Brand CTA**（风格最统一，最快）→ **Persona Scenario** → **Conceptual Diagram**

### 3.2 生产每张图

1. 从 CSV 中复制 `prompt` 列的内容
2. 粘贴到 Lovart **Nano Banana Pro** 的 ChatCanvas 中输入框
3. 生成，用 Touch Edit 微调（如需要）
4. 导出为 PNG，**命名格式**：

```
{filename}__IMAGE_{N}.png
```

| CSV 列 | 示例值 | 对应文件名 |
|--------|--------|-----------|
| filename | `how-to-create-logos-with-ai.md` | — |
| image_num | `IMAGE_1` | `how-to-create-logos-with-ai.md__IMAGE_1.png` |

5. 将图片文件放入 `已生产图片/` 目录
6. 在 CSV 中将该行的 `status` 改为 `✅`，`produced_file` 填入实际文件名

### 3.3 IMAGE 3 处理

IMAGE 3 标注为 `[REAL SCREENSHOT REQUIRED]`，不包含在 CSV 中。需要：
1. 打开对应的博客文章，找到 `[IMAGE 3 PLACEHOLDER]` 位置
2. 在 Lovart 中操作到文章描述的功能界面
3. 截取屏幕截图，按同样命名规则保存

---

## 四、回插流程

### 4.1 预览模式（推荐先运行）

```bash
cd "已生产内容/"
python3 insert_images.py --dry-run
```

会显示哪些图片匹配到了文章，哪些没有，不修改任何文件。

### 4.2 正式插入

```bash
cd "已生产内容/"
python3 insert_images.py
```

脚本自动：
1. 扫描 `已生产图片/` 中的所有 `.png/.jpg` 文件
2. 按 `文件名__IMAGE_{N}` 格式解析
3. 在对应文章的 `[IMAGE N PLACEHOLDER]` 位置替换为 `![描述](图片名.png)`
4. 输出处理结果

### 4.3 验证

插入后，文章的占位符会变成实际图片引用：

```
原来：  [IMAGE 1 PLACEHOLDER — Persona Scenario]
插入后：![IMAGE 1 PLACEHOLDER — Persona Scenario](how-to-create-logos-with-ai.md__IMAGE_1.png)
```

---

## 五、提示词格式说明

CSV 中每条 prompt 遵循 Lovart 图片生成的通用公式：

```
[Subject & Action] + [Environment/Context] + [Style/Medium] + [Lighting & Color] + [Technical]
```

示例：
```
A professional yet approachable person at their desk, frustrated at their screen 
while trying to create a design — warm natural lighting, candid documentary style
```

设计师可根据需要微调提示词，但请保持：
- 图片风格与文章主题匹配
- 同一 `image_type` 的图片风格尽量统一
- 避免在图中出现具体文字（文字用 HTML/CSS 叠加）

---

## 六、进度追踪

| 图片类型 | 总量 | 已生产 | 剩余 | 进度 |
|---------|------|--------|------|------|
| Persona Scenario | 705 | 0 | 705 | 0% |
| Conceptual Diagram | 705 | 0 | 705 | 0% |
| Brand CTA | 705 | 0 | 705 | 0% |
| **AI 生成合计** | **2,115** | **0** | **2,115** | **0%** |
| Real UI Screenshot | 705 | 0 | 705 | 0% |

*进度请设计师在 CSV 中更新 status 列*

---

## 七、批量生产建议

### 7.1 效率优化

1. **Brand CTA 图**：可先做一个模板 prompt，微调后批量生成变体（705 张中很多主题相似，可用 Lovart Batch 功能）
2. **Conceptual Diagram**：手绘风格相对统一，可固定开头 prompt 模板，只换主题词
3. **Persona Scenario**：最费时，但最具价值——建议优先完成高流量文章（见 CSV 按行号靠前的文章）

### 7.2 Lovart 批量技巧

- 在 ChatCanvas 中，第一个 prompt 生成满意后，**不要清空画布**
- 用 Touch Edit 只修改场景细节（换人/换环境/换色调）
- 这样可以保持整体风格一致，且大幅提升效率

---

## 八、联系人

- **内容策略与文章**：opencode 生成
- **图片生产**：设计师（待分配）
- **技术回插**：opencode 脚本 `insert_images.py`
- **进度管理**：CSV 文件 `IMAGE_PROMPTS_ALL_2115.csv`
