# MFlow 快速上手（首次使用 8 步）

> 目标：30 分钟内从零跑通第一个内容工作流。没有大模型 API Key 也能先走完演示闭环。

---

## 第 1 步 · 安装

```bash
git clone https://github.com/sevenaaaaaaaaa/mflow.git && cd mflow
# 依赖：Python 3.10+，推荐 uv
uv venv .venv && uv pip install --python .venv/bin/python markdown pyyaml requests google-auth google-auth-httplib2 google-api-python-client
```

## 第 2 步 · 设置访问密码

```bash
echo 'export MFLOW_CONSOLE_PASSWORD=你的密码' > run/env.sh
echo 'export LOVART_PYTHON=$PWD/.venv/bin/python' >> run/env.sh
```

## 第 3 步 · 启动工作台

```bash
source run/env.sh && .venv/bin/python "1-4 Dev/console/console.py"
# 浏览器打开 http://127.0.0.1:8088，输入密码
```

## 第 4 步 · 打开「首次引导」

侧栏最下方「首次引导 · Setup」是配置检查清单，逐项点亮：

## 第 5 步 · 导入 Demo 数据（可选但推荐）

点「一键导入 Demo 数据」：看板出现演示任务、下方出现示例报告（体验表格可视化），
**创作中心无需 API Key 即可跑通完整闭环**（生成 → 质检 → 状态机推进）。

## 第 6 步 · 配置大模型 API

「设置 · LLM · Harness」→ 填 provider（DeepSeek / OpenAI / 任意 OpenAI 兼容网关）的 base + Key →
点「测试连通」。完成后删掉 demo 数据重新生成，即为真实输出。

## 第 7 步 · 发起第一个工作流

两条路（「创作中心」页）：
- **Loop · Agent 模式**：填主题 → 发起 → 系统自动「生成 → 质检 → 按反馈重写」≤3 轮，通过后入 S4-qa 等你审阅；
- **节点流水线**：逐步点执行（生成 → 质检 → 推进），每步真实调用。

## 第 8 步 · 接入自己的数据

- 知识库：把公司文档 md 放入 `1-2 Insight/Knowledge Base/`（或注册新知识源，见 modules.md）
- 数据源（GSC/GA4/Bing 已内置）：`deploy`/凭证目录放对应 token，见 modules.md 的数据源扩展指南
- CMS：见 modules.md 的 CMS 适配器章节

---

## 常见问题

**质量门禁 BLOCK 了怎么办？** 门禁输出会写明触发项；修正后重跑，或人工审阅放行。
**报告在哪？** 侧栏「报告中心」10 分类；把自己的报告 md 放进对应目录即自动收录。
**多人怎么协作？** 任务看板支持拖拽与卡片编辑（负责人/截止日）；操作者在卡片编辑里署名。
