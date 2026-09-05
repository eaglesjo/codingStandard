# AI Engineering Standard

<p align="center"><strong>Стандарты инженерии для AI-разработки, обучения и агентов</strong></p>

> **Language:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · Русский · [Türkçe](../tr/README.md)
>
> Эта страница является русской точкой входа в документацию codingStandard. Русский входит в 20 runtime locale и проходит одинаковые проверки полноты ресурсов, семантического соответствия и согласованности runtime/документации.

`codingStandard` — это переиспользуемый инженерный стандарт для разработки с помощью AI, обучения моделей, экспериментов, LLM/Vision workflows, общего ML/DL lifecycle и AI coding agents.

Он предоставляет единые проектные инструкции, правила жизненного цикла ML/DL, доменные правила LLM/Vision, task-specific Skills, обнаружение окружения, политику запуска и восстановления Colab, кроссплатформенный installer и наборы проверок для воспроизводимых экспериментов.

## Быстрый старт

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell:

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target .
```

Подробные параметры установки доступны в [English README](../../README.md).

## Colab

Публичный репозиторий предоставляет быстрые Google Colab entrypoints для проверки полного стандарта, clean runtime, LLM QLoRA и RAG workflow.

## Многоязычность

Точки входа документации и runtime-ресурсы управляются отдельно, но все 20 runtime locale проходят одинаковые проверки качества и семантической паритетности.
