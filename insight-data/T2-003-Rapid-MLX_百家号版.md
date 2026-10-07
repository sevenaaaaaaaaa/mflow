# Rapid-MLX 深度评测：Apple Silicon 上最快的本地 AI 推理引擎，到底有多能打？

如果你有一台 Mac，你想跑本地 AI 模型，你一定听过 Ollama。但今天我们要聊的这个项目，用硬核基准测试告诉你：同样是本地跑模型，它可以比 Ollama 快 2.3 倍。它叫 Rapid-MLX，一个专为 Apple Silicon 打造的、开源的、OpenAI API 兼容的本地推理引擎。本文从安装体验、性能实测、工具链兼容性、功能深度等维度，做一次全面拆解。

项目速览：Rapid-MLX 托管在 GitHub（raullenchai/Rapid-MLX），已有约 2800+ Star 且增长极快。使用 Python 3.10+ 开发，Apache 2.0 协议开源，专为 Apple Silicon（M1/M2/M3/M4）平台优化。核心卖点是比 Ollama 快 2.3 倍，0.08 秒缓存首 token，17 种工具调用解析器，3300+ 测试用例。

一、它到底解决了什么问题？

Apple Silicon 的 MLX 框架是 Apple 官方推出的机器学习框架，专为 M 系列芯片优化。但在 Rapid-MLX 出现之前，用 MLX 跑大模型的门槛并不低：

第一，mlx-lm（Apple 官方工具）功能简陋，只提供最基础的 generate 和 serve，没有工具调用、没有 prompt cache、没有流式推理分离；

第二，Ollama 虽然好用，但底层基于 llama.cpp（GGUF 格式），本质上是跨平台的通用方案，无法充分利用 Apple Silicon 的统一内存架构和 Metal GPU 特性；

第三，更关键的是，市面上缺少一个同时具备高性能、OpenAI 兼容 API、丰富工具生态、且针对 MLX 深度优化的推理服务器。

Rapid-MLX 就是在这样的背景下诞生的。它的作者 raullenchai 做了一个非常聪明的决策：在 MLX 框架之上，搭建一个功能完整的、OpenAI API 兼容的推理服务器。这意味着你可以把任何兼容 OpenAI API 的应用（Cursor、Claude Code、Aider、LangChain 等）直接指向本地的 Rapid-MLX 服务，无需任何适配。

二、安装体验：三种方式，一行的功夫

Rapid-MLX 提供了三种安装方式，覆盖了不同用户的需求：第一种是 Homebrew 安装（推荐，自动处理 Python 版本问题），一行命令 brew install 即可；第二种是 pip 安装，需要 Python 3.10 以上；第三种是一键安装脚本，通过 curl 下载并执行。

我在一台 M3 Pro 的 MacBook Pro 上测试了 Homebrew 安装，整个过程约 2 分钟（含依赖下载），安装体积约 460MB（纯文本模型支持）。如果需要视觉/多模态能力，额外安装 vision 扩展会增加约 322MB。

安装完成后，一行命令即可启动对话：rapid-mlx chat。默认使用 qwen3.5-4b-4bit 模型，首次运行会自动下载（约 2.5GB），下载完成后直接进入 REPL 对话界面。整个过程丝滑流畅，不需要开第二个终端，不需要配置任何东西。

如果想作为服务运行供其他应用调用，执行 rapid-mlx serve 加上模型名，服务会在本地 8000 端口启动，输出熟悉的 Ready 提示。此时用 curl 或任何 OpenAI SDK 都能直接访问。

体验总结：安装体验可以打 9 分。Homebrew 方式对新手极其友好，唯一减分项是 brew 5.x 版本在安装时需要手动执行一次 tap 操作，文档里已经写清楚了。

三、性能实测：快，真的快

Rapid-MLX 团队在 Mac Studio M3 Ultra (256GB) 上做了一组非常扎实的横评对比，测试环境为 4 路并发流式推理（模拟真实多用户场景）：

Qwen3.5-4B 模型：Rapid-MLX 达到 261 tok/s，mlx-lm serve 只有 173，Ollama 只有 120。Rapid-MLX 比 Ollama 快 2.18 倍。
Qwen3.5-9B 模型：Rapid-MLX 达到 180 tok/s，mlx-lm serve 为 136，Ollama 为 84。快 2.14 倍。
Qwen3.5-27B 模型：Rapid-MLX 达到 66 tok/s，mlx-lm serve 为 55，Ollama 为 27。快 2.43 倍。
GPT-OSS 20B 模型：Rapid-MLX 达到 221 tok/s，mlx-lm serve 为 162，Ollama 为 97。快 2.29 倍。
Qwen3.6-35B-A3B 模型：Rapid-MLX 达到 176 tok/s，mlx-lm serve 为 129，Ollama 为 87。快 2.02 倍。

唯一 apples-to-apples 对比行是 GPT-OSS 20B（完全相同的权重），Rapid-MLX 比 Ollama 快 2.29 倍。

几个关键点值得关注：

3.1 并发场景下的碾压优势

Ollama 0.24 版本尚不支持 in-flight batching，多路请求实际上是串行执行的。而 Rapid-MLX 的 BatchedEngine 实现了真正的连续批处理（continuous batching），在 4 路并发场景下吞吐量优势显著。这对需要同时服务多个客户端的场景（比如团队共享一台 Mac Studio）至关重要。

3.2 Prompt Cache：DeltaNet 的杀手锏

Rapid-MLX 的 Prompt Cache 实现有两个层次：

标准 KV Cache 裁剪：对传统 Transformer 模型，将公共前缀的 KV 缓存持久化，跨请求复用。缓存命中后，TTFT（首 token 延迟）可降至 0.08-0.34 秒，某些模型比 mlx-lm serve 快 3.4 倍。

DeltaNet 状态快照：这是 Rapid-MLX 独有的技术。Qwen3.5 系列采用了 Gated DeltaNet 架构（75% RNN + 25% Attention），传统引擎无法对这种混合架构做 prefix cache，因为 RNN 层的隐状态无法像 KV cache 那样简单裁剪。Rapid-MLX 的做法是：在 system prompt 边界做 RNN 状态的 deep copy，后续请求直接恢复状态（约 0.1ms），从而绕过了对前数百个 token 的 RNN 层重复计算。

效果如下：Qwen3-Coder-Next 6bit 从冷启动 0.66 秒降到快照 0.16 秒，加速 4.3 倍；Qwen3.5-35B-A3B 8bit 从 0.49 秒降到 0.19 秒，加速 2.6 倍；Qwen3.5-27B 4bit 从 0.58 秒降到 0.27 秒，加速 2.1 倍。

这是一个被严重低估的特性——在多轮对话场景中，DeltaNet 快照意味着每轮对话的响应速度都接近缓存命中水平，极大地改善了交互体验。

3.3 DFlash 推测解码

Rapid-MLX 集成了 z-lab 的 DFlash 块扩散推测解码器，在 Qwen3.5/3.6 27B 8bit 模型上可获得 1.3-1.5 倍的平均加速，编程/数学/摘要场景下可达 1.5-2.7 倍。需要注意的是 DFlash 目前仅支持单用户模式，且暂不支持工具调用。

四、工具调用：17 种解析器，100% 恢复率

工具调用（Tool Calling / Function Calling）是 AI Agent 场景的核心能力。Rapid-MLX 在这方面投入了大量工程精力，支持 17 种工具调用解析器，覆盖市面上所有主流模型的工具调用格式：

Qwen3.5 用 hermes 解析器，工具调用成功率 100%；Qwen3.6 用 qwen3_coder_xml 解析器，成功率 100%；GLM-4.7 用 glm47 解析器，成功率 100%；GPT-OSS 用 harmony 解析器，成功率 100%；DeepSeek R1/V3 用 deepseek 系列解析器，成功率 100%；Gemma 4 用 hermes 解析器，成功率 100%。

更值得一提的是自动工具调用恢复（Auto Tool Recovery）功能。量化模型（尤其是 4-bit 量化）在多轮工具调用后容易输出损坏的工具调用文本。Rapid-MLX 会自动检测这些"坏掉的"文本格式工具调用，并将其转换回结构化的 tool_calls 格式，恢复率 100%。这个特性在实际使用中非常关键——它意味着你不会因为一次工具调用解析失败而中断整个 Agent 工作流。

Tool Logits Bias（跳跃解码）是另一个性能优化技术。在工具调用场景下，Rapid-MLX 可以有偏向性调整 logits，加速结构化 token 的生成速度。通过命令行参数开启。

五、Agent 生态兼容性：几乎覆盖所有主流框架

Rapid-MLX 最让我惊喜的是它的 Agent 集成测试矩阵。团队不是在 README 里写一句"兼容 OpenAI API"就完事，而是对每个 Agent 框架都做了端到端集成测试：

Hermes Agent（62 tools）通过测试；PydanticAI 框架通过；LangChain 框架通过；smolagents 框架通过；Codex CLI（OpenAI Rust）通过；Claude Code 通过；Aider 通过；Cursor IDE 兼容；Open WebUI 在 Docker 环境通过；LibreChat 在 Docker 环境通过；OpenCode TUI Agent 兼容。

这意味着你可以把 Rapid-MLX 当作一个通用的 AI 推理后端，无缝接入你的现有开发工作流。更贴心的是，它还提供了 rapid-mlx agents 命令来自动配置对应的 Agent 客户端。

MHI（Model-Harness Index）模型-框架适配指数是另一个亮点。它从工具调用（50%）、编码能力 HumanEval（30%）、通用知识 MMLU（20%）三个维度，量化模型与 Agent 框架的匹配度。例如 Qwopus 27B + Hermes Agent 组合拿到了 92 分，是所有组合中的最高分。

六、支持的模型矩阵：72 个别名，从 0.6B 到 158B

Rapid-MLX 的模型阵容非常丰富，覆盖 13 个模型家族、72 个正式别名：

Qwen3.5 系列从 4B 到 122B，采用 DeltaNet 混合架构，是主力推荐；Qwen3.6 系列 27B 到 35B，支持 262K 上下文和 256 MoE 专家；Gemma 4 系列 12B 到 31B，具备视觉能力和 QAT 变体；DeepSeek 系列从 R1-8B 到 V4 Flash 158B，涵盖推理模型和前沿 MoE；GPT-OSS 20B 原生支持 Harmony，100% 工具调用成功率；DiffusionGemma 26B 是全新非自回归块去噪语言模型；此外还覆盖 Llama、Hermes、GLM、Mistral、Phi 等几乎所有主流架构。

特别值得一提的是 DiffusionGemma 26B-A4B——一个非自回归语言模型，通过块去噪的方式并行生成 token。在 256 token 输出时，端到端速度约 43 tok/s，且不需要修改客户端代码——它完全兼容 OpenAI Chat Completions API。

模型选择建议（以 Mac 配置为基准）：

16GB MacBook Air：推荐 qwen3.5-4b-4bit，2.4GB 内存占用，147 tok/s。
24GB MacBook Pro：推荐 qwen3.5-9b-4bit，5.1GB 内存占用，101 tok/s。
32GB Mac Mini/Studio：推荐 qwen3.5-27b-4bit 或 qwen3.6-35b-4bit（MoE 架构）。
48GB 以上：推荐 qwen3.5-35b-8bit，口碑最好的甜点区。
96GB 以上：推荐 qwen3.5-122b-mxfp4，前沿级智能。

七、智能云路由：本地不够快时自动切云端

Rapid-MLX 有一个独特的功能叫 Smart Cloud Routing。当你发送一个超长上下文请求，本地的 prefill 阶段可能需要很长时间时，Rapid-MLX 可以自动将这个请求路由到云端 LLM。只需在启动服务时指定云端模型和阈值，当新 token 数量超过设定值时自动切换到 GPT-5 等云端模型处理。这个设计非常实用——对于偶尔的长文档分析任务，你不需要为了那 5% 的场景而升级硬件，让云端兜底即可。

八、高级特性一览

除了核心的推理性能，Rapid-MLX 还提供了大量生产级特性：KV Cache TurboQuant 可实现 V cache 压缩 86% 节省，支持 3-4 bit，可选开启；推理分离功能将思维链 reasoning_content 与最终文本 content 干净分离，默认支持；结构化输出支持 response_format JSON Schema，生产可用；多模态支持视觉（图片/视频理解）和音频（TTS/STT），通过 pip extras 安装；MCP 集成支持通过配置文件接入外部工具；Embeddings 端点可用；远程分享功能可一键生成公网 URL，内置支持；Telemetry 匿名使用统计默认关闭，需显式 opt-in。

九、缺点与不足：诚实的部分

没有任何工具是完美的。以下是我实际体验中发现的 Rapid-MLX 的局限性：

9.1 仅限 Apple Silicon

这是最大的限制。如果你用的是 Intel Mac、Windows 或 Linux，Rapid-MLX 完全不可用。这是 MLX 框架本身的限制，不是 Rapid-MLX 能解决的。

9.2 低熵场景下 DFlash 可能减速

DFlash 推测解码在编程/数学等高熵任务中表现出色，但在创意写作等低熵/高随机性任务中，drafter 的预测准确率下降，可能导致 0.6-0.9 倍的实际吞吐量（即比不用反而慢）。好在这个问题在论文中已有讨论，且 DFlash 是可选的，不影响默认使用。

9.3 社区仍在早期

相比 Ollama 的庞大社区和模型库生态，Rapid-MLX 虽然已有 2800+ star，但 issue 和 PR 数量还处于早期阶段。部分模型（尤其是小众模型）可能因为缺少 MLX 格式的权重而无法使用。

9.4 视觉/Audio 能力需要额外安装

虽然基础安装只有 460MB，但视觉、音频、embeddings 等功能分别需要额外安装扩展包，全量安装约 1.1GB。这对存储空间有限的低配 Mac 来说是个小负担。

十、总结：谁应该用 Rapid-MLX？

Mac 用户需要本地跑模型作为日常助手：五星推荐，比 Ollama 快 2 倍以上，安装更简单。
开发者需要本地 Agent 后端：五星推荐，17 种工具解析器，12 个 Agent 框架集成测试。
需要视觉/多模态能力的用户：四星，需额外安装但功能完整。
团队共享 Mac 推理服务器：五星推荐，连续批处理加云路由，并发天花板更高。
Windows/Linux 用户：一星，不可用，等 MLX 跨平台支持。
需要极大量预训练模型生态：三星，Ollama 的模型库更大。

最终评价：

Rapid-MLX 是 Apple Silicon 生态下目前最强的开源本地推理引擎，没有之一。它在性能、功能完整度、Agent 兼容性三个维度上都做到了同类工具的领先水平。2800+ star 的项目质量远超预期——3300+ 测试用例、详细的基准测试报告、扎实的工程实现，说明这个项目的团队有明确的工程品味和质量标准。

如果你用的是 Mac，并且对本地 AI 推理有超出"玩玩"的需求，Rapid-MLX 值得你花 5 分钟安装试用。一道命令就能让你感受到 MLX 原生推理的速度。

评测环境：macOS 27.0，M3 Pro MacBook Pro。基准测试数据来自 Rapid-MLX 官方基准测试（Mac Studio M3 Ultra 256GB, v0.6.83, 2026-06-09），部分性能数据在低配设备上会有差异。
