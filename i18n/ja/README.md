# AI Engineering Standard

<p align="center"><strong>AI 開発・学習・エージェントエンジニアリング標準</strong></p>

> **Language:** [English](../../README.md) · [한국어](../ko/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [简体中文](../zh-CN/README.md) · 日本語 · [Русский](../ru/README.md) · [Türkçe](../tr/README.md)
>
> このページは codingStandard の日本語ドキュメント入口です。実行時の Agent / Skill / Environment リソースは現在 English と Korean が正式対応で、他言語は翻訳と検証が完了した後に installer 対応へ追加します。

## AI Engineering Standard とは？

`codingStandard` は、AI 支援開発、モデル学習、実験、LLM/Vision ワークフロー、一般的な ML/DL ワークフロー、AI コーディングエージェント向けの再利用可能なエンジニアリング標準です。

統一されたプロジェクト指示、ML/DL ライフサイクル規約、LLM/Vision のルール、タスク別 Skills、環境検出、Colab の実行・復旧ポリシー、クロスプラットフォーム installer、検証スイート、再現可能な実験手順を提供します。

## クイックスタート

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/installers/install-domains.sh .
```

Windows / PowerShell：

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\installers\install-domains.ps1 -Target .
```

インストール引数の詳細は [English README](../../README.md) を参照してください。

## Colab

公開リポジトリには、標準全体、clean runtime、LLM QLoRA、RAG を検証するワンクリック Google Colab 入口があります。

## 多言語対応

ドキュメント入口は English、한국어、Français、Español、简体中文、日本語、Русский、Türkçe を提供します。実行時ポリシーは、実際に翻訳・検証された言語だけを installer の正式対応として扱います。
