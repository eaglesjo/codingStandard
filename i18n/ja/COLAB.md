# Google Colab 検証

このドキュメントでは、Google Colab で `codingStandard` を実行・検証する方法を説明します。

## Colab で開く

リポジトリ README の Colab リンクを使用するか、次の Notebook を直接開きます。

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

fork または移動したコピーを使用する場合は、そのコピーの Notebook を Colab で開き、最初のセルでリポジトリ URL を入力するか、環境変数 `CODINGSTANDARD_REPO_URL` を設定します。

## リポジトリの選択

Notebook は特定のリポジトリ URL に固定されません。次の優先順位で選択します。

1. `CODINGSTANDARD_REPO_URL` 環境変数
2. 対話形式のリポジトリ URL 入力
3. デフォルト値としての `eaglesjo/codingStandard` URL

## パブリック／プライベートリポジトリの認証

Notebook はまず認証なしで clone を試行します。

- **パブリックリポジトリ:** そのまま clone を続行し、token の入力は求められません。
- **プライベートリポジトリ:** 認証なしの clone が拒否された後、安全な `getpass` 入力を通じて **GitHub Personal Access Token** を要求します。
- Google Colab Secrets または環境変数に `GITHUB_TOKEN` がある場合は自動的に使用します。

Token は一時的な `GIT_ASKPASS` helper を使って Git に渡されます。clone URL、Notebook ソース、出力内容、保存された結果 JSON には token を含めません。テスト後は Colab セッションから token を削除してください。

## 検証内容

1. 選択したリポジトリを Colab runtime に clone します。
2. Python、PyTorch、CPU、RAM、accelerator、VRAM、CUDA/MPS capability、runtime 情報を検出します。
3. 共通 LLM environment profiler を実行します。
4. checkpoint の保存／再読み込みを含む小規模な LLM training smoke test を実行します。
5. image tensor を使った小規模な Vision training smoke test を実行します。
6. repository validation を実行します。
7. resource 情報と pass/fail 状態を JSON に記録します。
8. ローカル開発マシンに依存せず clean runtime で Notebook を実行できることを確認します。

clone の失敗や途中終了によって `/content/codingStandard` が残っている場合、Notebook は不完全なディレクトリを削除してクリーンに再試行します。

テストは意図的に小さく設計されています。Colab smoke test に合格することで開発標準と最小実行経路を検証できますが、任意の production model が利用可能な Colab runtime のリソースに収まることを保証するものではありません。

## 推奨する利用タイミング

environment profiler、memory smoke tests、training configuration、または Colab 関連の instructions を変更した後にこの Notebook を実行してください。

## 関連検証

- 完全検証：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
