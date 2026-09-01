# ML / Deep Learning Skill

일반 ML/DL 구현, 학습, 평가, 실험, 추론, model lifecycle에 사용합니다.

```text
Discover → Data Contract → Environment → Runtime Resolve
→ Baseline → Smoke Test → Lock → Train/Infer
→ Evaluate → Compare → Lineage Record
```

학습 전 dataset schema/label/duplicate/leakage/split을 검증하고, baseline과 primary metric/direction을 정의합니다.

실험에는 hypothesis, changed/fixed parameters, seed, model/dataset revision, runtime, peak RAM/accelerator memory, artifact와 Git 상태를 기록합니다.

장시간 작업에는 validation, best checkpoint, Resume, 필요한 경우 Early Stopping을 적용하고 OOM은 단계적으로 자원 요구량을 낮춰 재검증합니다.