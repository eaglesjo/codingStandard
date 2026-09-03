# ML/DL ランタイム検証

このガイドでは、`codingStandard` のインストール後に実際の実行契約を検証します。

## Agent ルーティング

リポジトリのルートから実行します。

```bash
python scripts/validation/validate_agent_routing.py
```

テストでは、次の4つの代表的なリクエストを確認します。

- 一般的な PyTorch トレーニング → common + ML ライフサイクル
- LLM QLoRA → common + ML + LLM fine-tuning/PEFT/quantization
- Vision detection → common + ML + Vision detection/evaluation
- Colab LLM training → common + ML + LLM + Colab checkpoint/resume ポリシー

また、これらの最小シナリオに無関係なドメインが誤って追加されていないことも確認します。

## Colab runtime

新しい Colab runtime で `examples/colab/clean_runtime_validation.ipynb` を開き、すべてのセルを上から順に実行します。

Notebook は次を満たす必要があります。

1. アクティブな Python kernel と実行環境を識別する。
2. 利用可能な場合、accelerator、RAM、disk の特性を報告する。
3. agent-routing 契約テストを実行する。
4. PyTorch が利用可能な場合、小さな forward/backward smoke test を実行する。
5. 選択した永続ディレクトリに checkpoint を保存し、復元する。
6. machine-readable な runtime report を生成する。

Colab のリセット後も checkpoint を残す必要がある場合は、マウント済みの永続ストレージを使用してください。Notebook VM のファイルシステムは使い捨てとして扱います。

## 解釈

検証成功は、インストール済みポリシーを発見でき、選択した runtime を測定でき、代表的な workload を安全に開始でき、復旧用 artifact を復元できることを意味します。すべての Colab accelerator 種類やすべてのモデルサイズがテストされたことを意味するものではありません。
