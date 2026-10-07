---
profileName: NowX
postId: "3215"
postType: post
categories:
  - 69

tags: [AI, 工具, 开源]---
## PoPo简介

PoPo 是一个开源 AI 工具， 允许用户通过自然语言控制 MikuMikuDance（MMD）角色的骨骼动作和面部表情 。你只需输入文字描述，PoPo 就能生成精确的 MPL（MMD Pose Language）脚本，驱动骨骼动画和角色表情的实时渲染 。


## PoPo功能亮点

PoPo 支持“挥右手、大笑邀请晚餐”等语句输入，输出结构化的 MPL 代码，可直接控制胳膊、手指、面部 morph 等部位，生成可靠且一致的姿势。渲染快速流畅，专门针对日系角色骨骼结构和物理约束做了优化 。

## PoPo技术架构

- 前端采用 Next.js 与 shadcn/ui + TypeScript
- 渲染基于 Babylon.js 搭载 babylon‑mmd 插件
- 核心使用 GPT‑4o‑mini 模型 fine‑tune，将自然语言映射为 MPL 语义脚本
- 项目部署在 Vercel 平台

## MPL 语言优势

作为 MMD 专用的语义姿势描述语言，MPL 避免复杂的四元数数值训练，更具可读性和可调试性。这样训练的模型表现更稳定，姿势更符合人体运动规则，输出结果容易修改调试，并更具一致性 。

### 示例训练流程

训练数据使用如下结构：

```json
{
  "messages":[
    {"role":"system","content":"Generate MMD Pose Language (MPL) script from description."},
    {"role":"user","content":"Description: arms down"},
    {"role":"assistant","content":"arm_l bend forward 40;arm_r bend forward 40;"}
  ]
}
```

这种设计帮助模型快速收敛，保持输出一致，并让结果具备结构化语义的可调性 。


## PoPo社区与演进历程

PoPo 前身是 MiKaPo 项目，通过 MediaPipe 实时捕获人体姿势再映射到 MMD 骨骼；而 PoPo 则跳过中间步骤，直接从文本生成 MPL 脚本控制骨骼模型 。当前训练集约 160 个姿势样本，表现已较好，仍欢迎用户贡献更多高质量训练数据以进一步优化模型 。

## PoPo使用方式

用户可访问在线演示站点 popo.love，选择“深空之眼 三相·梵天『无间玩伴』”等示例模型，通过输入自然语言描述生成对应动作与表情。GitHub 上提供完整源码与贡献指南，采用 GPL‑3.0 开源协议 。

PoPo 将自然语言、AI 模型与 MMD 动画结合，通过语义语言 MPL 为用户提供直观且高效的动作创作体验。在不断扩展数据集与优化模型之后，它有望成为日系角色动画制作的重要工具。

体验地址： [https://popo.love/](https://popo.love/ "PoPo 体验地址")

GitHub地址： [https://github.com/AmyangXYZ/PoPo](https://github.com/AmyangXYZ/PoPo "PoPo GitHub地址")