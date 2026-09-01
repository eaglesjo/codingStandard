# ML / Deep Learning Domain

`domains/ml/`은 LLM/Vision에 공통으로 필요한 ML lifecycle 정책을 담당합니다.

```text
data/                         dataset 검증
experiment/                   실험 설계와 baseline/effective comparison
evaluation/                   metric, regression gate, error analysis
training/                     일반 학습 계약
distributed-training/         multi-GPU/multi-node
hyperparameter-optimization/  체계적 tuning
inference/                    재현 가능한 추론과 latency/memory 검증
mlops/                        model/artifact lineage
```

필요한 Skill만 로드합니다. LLM과 Vision은 이 lifecycle을 상속하고 도메인별 task 규칙을 추가합니다.