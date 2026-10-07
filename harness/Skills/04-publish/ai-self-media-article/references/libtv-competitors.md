# LibTV 竞品对比参考（2026 年 6 月）

## 竞品分类

### 国际商业平台

| 竞品 | 价格 | 核心差异 vs LibTV |
|------|------|------------------|
| **Runway** (Gen-4.5) | Free 125 credits, $15-95/mo | 线性编辑器，无节点工作流，无角色一致性，Motion Brush 提供部分控制 |
| **Pika** (2.5) | Free 80 credits, $8-76/mo | 社交创意导向，特效模板丰富，无节点/角色/灯光 |
| **Kling** (3.0) | Free 66 daily, $10-95/mo | 最长 3 分钟，原生音频同步，物理模拟，无节点/灯光 |
| **Sora 2** (OpenAI) | via ChatGPT $20-200/mo | 消费者版已停服(2026-04-26)，物理模拟领先，无节点 |
| **Veo 3.1** (Google) | AI Pro $20/mo, Ultra $250/mo | 原生音频生成，Google Cloud 集成，无节点/角色 |
| **Hailuo/MiniMax** | $10-200/mo | 性价比高，多模型聚合，无节点/角色/灯光 |
| **Invideo AI** | Free, $20-60/mo | 模板驱动（非生成式），适合营销短视频 |
| **Kapwing** | Free, $16-50/mo | 协作视频编辑器+AI 辅助，非生成式 |

### 开源方案

| 竞品 | Stars | 核心差异 vs LibTV |
|------|-------|------------------|
| **ComfyUI** | 170k+ | 最相似的节点概念，但是通用 SD 界面而非视频平台，需本地 GPU，无角色一致性/灯光/Skill API |
| **CogVideo** (清华) | 14k | Apache 2.0，文生视频，768×1360，研究级质量 |
| **Open-Sora** | 29k | Apache 2.0，可训练 11B 模型，研究框架 |
| **Wan Video** (阿里) | — | Apache 2.0，14B 参数，VBench 86.22%，最强开源 |
| **AnimateDiff** | — | SD 扩展，插件式，低显存(8-12GB) |

### 短剧专精

| 竞品 | 核心差异 vs LibTV |
|------|------------------|
| **Genra AI** | 角色锁定+竖屏优化，无节点工作流，短剧专精 |
| **Medeo** | 多模型聚合（Kling/Seedance/Sora），无节点 |
| **AIDrama Studio** (开源) | MIT，20+ 模型，小说转视频 |

## LibTV 差异化卖点矩阵

| 特性 | LibTV | Runway | Pika | Kling | ComfyUI | Genra |
|------|:-----:|:------:|:----:|:-----:|:-------:|:-----:|
| 节点工作流 | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| 角色一致性 | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 灯光控制 | ✅ | 部分 | ❌ | ❌ | ❌ | ❌ |
| Skill API | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| 云端运行 | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| 易用性 | 高 | 高 | 高 | 中 | 低 | 中 |

**一句话定位**：LibTV = ComfyUI 的节点灵活性 + 云端易用性 + 角色一致性 + 灯光控制。唯一同时具备这四点的平台。

## 对比文章写作要点

每篇对比母版聚焦 1 个核心差异点：
- vs Runway → 节点工作流 vs 线性编辑
- vs Pika → 专业影视 vs 社交创意
- vs Kling → 角色库+编排 vs 单镜头生成
- vs Sora → 持续可用 vs 已停服
- vs Veo → 节点编排 vs Google 生态
- vs ComfyUI → 云端易用 vs 本地灵活
- vs Genra → 全流程 vs 短剧专精
- vs Hailuo → 工作流编排 vs 单次生成
- vs Seedance → 角色库+灯光 vs 排队
- vs Invideo → AI 生成 vs 模板编辑
