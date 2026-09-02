# 共通 AI 開発 Skill

この Skill は、リポジトリ探索、環境検証、実装、テスト、セキュリティ、再現性のために使用します。

## ワークフロー

```text
Discover repository
→ Read project instructions
→ Detect runtime
→ Measure available resources
→ Resolve configuration
→ Run smallest meaningful smoke test
→ Lock validated configuration
→ Implement
→ Test
→ Record reproducibility/resource metadata
```

## ルール

- 仮定より計測済みの能力を優先する。
- 意図的に更新しない限り、既存のプロジェクト規約を維持する。
- 破壊的な変更は明示する。
- 設定を集中管理し、再現可能にする。
- シークレットを絶対に公開しない。
- 段階的な検証を行い、既知の失敗設定を繰り返さない。
