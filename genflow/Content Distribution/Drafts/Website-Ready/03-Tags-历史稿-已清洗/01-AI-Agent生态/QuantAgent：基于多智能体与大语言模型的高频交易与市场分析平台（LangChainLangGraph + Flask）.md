---
title: "QuantAgent：基于多智能体与大语言模型的高频交易与市场分析平台（LangChain/LangGraph + Flask）"
- "[[ahhhhfs]]"
published: 2025-11-29
created: 2025-12-08
description: "QuantAgent 是一款基于价格驱动的多智能体大语言模型高频交易系统，集成 RSI/MACD/随机振荡器、图形模式识别与趋势通道分析，提供 Flask 网页与程序化访问，支持雅虎财经实时数据、LangChain/LangGraph、TA-Lib 及多家 LLM API，用于构建可视化的量化研究与交易决策流程（不构成投资建议）。"
tags:
- "AI"
- "Agent"
---
## QuantAgent：基于多智能体与大语言模型的高频交易与市场分析平台（LangChain/LangGraph + Flask）

2025-11-29 AI工具 GitHub项目 0 0 0

- 详情介绍
- 常见问题
- 评论建议

## QuantAgent概览

QuantAgent 是一个面向量化研究与高频交易场景的多智能体分析平台。系统以价格为驱动，联合技术指标、图形模式与趋势通道三类信号，由决策智能体生成可执行的交易指令。平台基于 **LangChain / LangGraph** 构建智能体工作流，配备 **Flask** 网页端与 API 访问，支持来自 **雅虎财经** 的实时市场数据与多资产多周期分析。
开源地址： [https://github.com/Y-Research-SBU/QuantAgent](https://github.com/Y-Research-SBU/QuantAgent "QuantAgent 开源地址")

### 适用资产与周期

- 资产类型：股票、加密货币、商品、指数
- 时间周期：1 分钟—1 天多周期联动
- 动态可视化：自动生成带注释的 K 线与趋势通道图

## 功能亮点

### 指标智能体

- 在每根最新 K 线上计算核心技术指标： **RSI** （衡量动量极值）、 **MACD** （量化收敛/发散动态）、 **随机振荡器** （衡量收盘价相对近期波动区间），将 OHLC 行情转换为可交易的信号输入。


### 模式智能体

- 绘制近期价格图，识别主要高低点与总体走势，将图形与常见形态库比对，并返回 **最佳匹配的通俗描述** ，助力模式化解读。


### 趋势智能体

- 在带注释的 K 线上叠加 **拟合趋势通道** ，追踪上/下轨，量化方向、斜率与盘整区域，输出 **简洁而专业** 的趋势总结。


### 决策智能体

- 汇总指标、模式、趋势与 **风险智能体** 结果，形成 **可执行的交易指令** ：包含多/空方向、入场/出场点位、止损阈值与关键理由，便于策略落地与复盘说明。


### 网络界面与可视化

- **Flask** 驱动的现代化前端
- **雅虎财经** 实时数据接入
- 交互式资产选择与多周期切换
- 动态生成图表与 **API 密钥管理**

## 架构与依赖

- 智能体框架： **LangChain / LangGraph**
- 可视化与服务： **Flask** 网页端 + 程序化 API
- 数据与指标： **雅虎财经** 实时行情、 **TA-Lib** 技术指标库（可通过 conda-forge 安装）
- **重要说明** ：模型需要支持 **图像输入** ，用于解析系统生成的图表，以完成模式识别与趋势分析。

## 快速开始

### 环境准备

```
# 1) 创建并激活 Conda 环境
conda create -n quantagents python=3.11
conda activate quantagents

# 2) 安装依赖
pip install -r requirements.txt

# 若安装 TA-Lib 遇到问题，可尝试：
conda install -c conda-forge ta-lib
# 或参考 TA-Lib Python 仓库的安装说明
```

### 配置 LLM API 密钥（示例）

```bash
# OpenAI
export OPENAI_API_KEY="your_openai_api_key_here"

# Anthropic（Claude）
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# Qwen（DashScope，新加坡区域，可能存在延迟）
export DASHSCOPE_API_KEY="your_dashscope_api_key_here"
```

## 使用建议

- 以研究与教学为主，逐步验证信号稳定性与执行逻辑。
- 结合账户风控与仓位管理，仅在明确理解风险的前提下使用交易指令。
- 对接图像理解能力强的 LLM，可显著提升形态与通道识别效果。

## 常见问答

**Q：是否必须使用支持图像输入的 LLM？**
A：是。系统需解析生成的图表，图像输入能力为必要条件。

**Q：数据从哪里来？**
A：网页端使用来自 **雅虎财经** 的实时市场数据。

## 合规与声明

本项目仅用于学习、研究与策略原型验证，不构成投资建议。请根据当地法规合规使用，并自行承担交易风险。

本文链接：

### 相关

AITradingSimulator：基于大语言模型的加密货币AI交易模拟器｜自定义策略 · 实时行情 · 专业绩效分析

Craft-Agent：集AI深度研究助手与一键建站引擎于一体的开源智能体系统

股票投资入门30讲 完结

1. 转载请保留原文链接谢谢！
- 本站所有资源文章出自互联网收集整理，本站不参与制作，如果侵犯了您的合法权益，请联系本站我们会及时删除。
- 本站发布资源来源于互联网，可能存在水印或者引流等信息，请用户擦亮眼睛自行鉴别，做一个有主见和判断力的用户。
- 本站资源仅供研究、学习交流之用，若使用商业用途，请购买正版授权，否则产生的一切后果将由下载用户自行承担。
- 联系方式（#替换成@）：feedback#abskoop.com[上一篇

全球品牌数据库（Global Brand Database）权威指南：商标搜索与品牌查询一站式工具

]( "全球品牌数据库（Global Brand Database）权威指南：商标搜索与品牌查询一站式工具")[下一篇

手机修图系统实战课，掌握专业级修图技巧

]( "手机修图系统实战课，掌握专业级修图技巧")
