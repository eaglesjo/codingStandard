# AI Engineering Standard

<p align="center"><strong>AI 开发、训练与智能体工程标准</strong></p>

> **Language:** [English](../../README.md) · [한국어](../ko/README.md) · 简体中文 · [日本語](../ja/README.md) · [Русский](../ru/README.md)
>
> 本页面是 codingStandard 的简体中文文档入口。运行时 Agent / Skill / Environment 资源目前正式本地化到 English 与 Korean；其他语言会在资源完成并通过验证后加入 installer 支持。

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

文档入口提供 English、한국어、简体中文、日本語、Русский。运行时策略资源仍按实际翻译完成度标记，避免误导使用者。
