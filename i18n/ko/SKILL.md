# SKILL.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development Skill

Python 기반 LLM/ML, Jupyter, VS Code Jupyter, Google Colab 및 local GPU 작업에 적용합니다.

## 작업 시작

```text
1. Python / active kernel
2. OS / architecture
3. IDE / Jupyter / Colab runtime
4. GPU / accelerator / VRAM
5. CPU / system RAM / disk
6. dependency
7. project root
8. experiment requirements
```

가능하면 먼저 다음 프로파일러를 실행합니다.

```bash
python LLM/environment.py
```

## 환경 결정

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

실제 측정값을 기준으로 device, batch size, gradient accumulation, workers, precision, checkpointing, input size를 결정합니다.

## Environment Lock / 정리

환경과 workload가 검증되면 확정된 configuration을 전체 실행에서 재사용합니다.

사용하지 않는 OS/device branch, 중복 detection, dead code, 사용하지 않는 import, 주석 처리된 구식 구현은 제거합니다. 공식적으로 여러 플랫폼을 지원하는 reusable library에서는 필요한 branch를 유지합니다.

## Memory Smoke Test

장시간 학습 전에 작은 workload로 다음을 검증합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save/reload
```

실패하면 batch, input/sequence, workers, precision, checkpointing 등을 단계적으로 조정하고 다시 검증합니다.

## Training / Early Stopping

장시간 학습에는 validation metric, Early Stopping, best checkpoint, Resume을 기본 적용합니다.

```python
EARLY_STOPPING = {
    "enabled": True,
    "metric": "eval_loss",
    "mode": "min",
    "patience": 3,
    "min_delta": 0.0,
    "restore_best": True,
}
```

## Ablation Study

baseline과 variant를 명시적인 configuration matrix로 정의하고, split, metric, budget, Early Stopping policy, seed 등 통제 변수를 유지합니다.

각 실험에는 experiment id, 변경 파라미터, seed, metric, runtime, peak VRAM/RAM, checkpoint, environment profile을 기록합니다.

## 완료 조건

```text
[ ] environment profile
[ ] runtime configuration
[ ] memory smoke test
[ ] environment lock
[ ] unused branch cleanup
[ ] Early Stopping
[ ] best checkpoint / Resume
[ ] Ablation matrix
[ ] reproducibility/resource metadata
[ ] clean kernel Run All
```
