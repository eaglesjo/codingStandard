# AI Engineering Standard

<p align="center"><strong>AI 开发、训练与智能体工程标准</strong></p>

> **Language:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · 简体中文 · [日本語](../ja/README.md) · [Русский](../ru/README.md) · [Türkçe](../tr/README.md)
>
> 本页面是 codingStandard 的简体中文文档入口。简体中文属于 20 个 runtime locale，并接受统一的资源完整性、语义一致性以及 runtime/文档一致性验证。

## 什么是 AI Engineering Standard？

`codingStandard` 是一套可复用的 AI 工程标准，用于 AI 辅助开发、模型训练、实验、LLM/Vision 工作流、通用 ML/DL 工作流以及 AI 编程智能体。

它提供统一项目指令、ML/DL 生命周期规范、LLM/Vision 领域规则、任务 Skills、环境检测、Colab 执行与恢复策略、跨平台安装器，以及验证与可复现实验规范。

## 快速开始

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell：

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target .
```

完整安装参数请参阅 [English README](../../README.md)。

## Colab

公共仓库提供一键 Google Colab 验证入口，用于完整标准、clean runtime、LLM QLoRA 与 RAG 路径。

## 多语言支持

文档入口提供 20 个 runtime locale。所有 runtime 策略资源都经过相同的资源完整性、语义一致性和 runtime/文档一致性检查。
