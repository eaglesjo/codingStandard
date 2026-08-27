# Jupyter / LLM 개발 Skill

Python LLM/ML, Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 local GPU 학습 작업에 적용합니다.

## 작업 시작

```text
1. Repository / instructions 확인
2. Python / active kernel 확인
3. OS / IDE / runtime 확인
4. CPU / RAM / GPU / VRAM / accelerator 측정
5. environment.py 실행
6. Runtime Configuration 계산
7. Memory Smoke Test
8. Environment Lock
9. 구현 / 실행
```

프로파일러:

```bash
python LLM/environment.py
```

프로파일은 실제 환경의 source of truth입니다. 특정 장비나 OS를 고정하지 않습니다.

## Environment Lock

환경이 확정되면 resolved `device`, `batch_size`, `gradient_accumulation_steps`, `num_workers`, `pin_memory`, precision, checkpointing, input size 등을 전체 실행에서 재사용합니다.

환경 확정 후 사용하지 않는 OS/device branch, dead code, 구식 구현, 중복 detection을 제거합니다. 여러 환경을 공식 지원하는 reusable library는 필요한 분기를 유지합니다.

## 메모리 최적화

```text
batch 감소
→ sequence/input 감소
→ gradient accumulation
→ mixed precision
→ gradient checkpointing
→ quantization/offload 검토
→ tensor/reference 정리
```

CPU/RAM은 dataset streaming/chunking, worker 제한, prefetch 제한, 중복 복사 방지, CPU thread 제한을 기본으로 합니다.

## Memory Smoke Test

본 학습 전에 `load → forward → backward → optimizer step → validation → checkpoint`를 작은 workload로 실행합니다.

실패하면 batch/input/workers/precision 등을 낮춰 다시 검증한 뒤 본 학습을 시작합니다.

## Training

학습 configuration은 한 곳에서 관리합니다.

필수:

- validation metric
- Early Stopping
- best checkpoint
- Resume 가능한 checkpoint
- seed 및 experiment configuration 기록

## Early Stopping

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

baseline과 variant를 명시적인 configuration matrix로 정의합니다. data split, evaluation set, metric, budget, Early Stopping 정책, seed 등 통제 변수를 유지합니다.

각 실험에는 experiment id, changed parameters, metrics, runtime, peak VRAM/RAM, checkpoint, environment profile을 저장합니다.

## Validation

```text
fresh kernel/runtime
→ environment profile
→ smoke test
→ baseline
→ early stopping 확인
→ checkpoint/resume 확인
→ ablation
→ resource/metric 기록
→ dead code 정리
→ clean run
```
