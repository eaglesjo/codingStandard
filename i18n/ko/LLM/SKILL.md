# SKILL.md

# Cross-Platform Python LLM / Jupyter / Google Colab 개발 Skill

이 Skill은 Python 기반 LLM/ML 개발을 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 수행할 때 적용합니다.

## 1. 적용 범위

- Windows / Linux / macOS
- venv / virtualenv / conda / uv
- Jupyter / JupyterLab / VS Code Jupyter
- Google Colab / Colab Local Runtime
- CPU / CUDA / MPS
- 제한된 GPU VRAM / System RAM
- 환경 자동 감지 및 runtime 최적화
- Environment Lock 및 불필요한 branch 정리
- Early Stopping / Checkpoint / Resume
- Ablation Study / Experiment Tracking
- reproducibility / security

## 2. 작업 시작 순서

환경 의존 작업 전에 다음을 확인합니다.

```text
Python / active kernel
→ OS / architecture
→ IDE / Jupyter / Colab runtime
→ GPU / CUDA / VRAM
→ CPU / RAM
→ dependencies
→ project root
→ experiment requirements
```

가능하면 공통 프로파일러를 실행합니다.

```bash
python LLM/environment.py
```

프로파일 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 3. Environment Resolution

환경 정보를 출력하는 것으로 끝내지 않고 실제 실행 설정으로 변환하고 검증합니다.

```text
Detect
→ Measure
→ Resolve
→ Smoke Test
→ Lock
→ Optimize
→ Execute
```

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

프로파일은 실제 장비와 runtime의 source of truth입니다. 특정 장비나 고정 하드웨어 프로파일로 대체하지 않습니다.

## 4. Environment Lock / 코드 정리

환경과 workload가 검증되면:

- resolved device/configuration을 재사용합니다.
- 애플리케이션/Notebook에서 사용하지 않는 OS/device branch를 제거합니다.
- 중복 environment detection을 제거합니다.
- dead import와 구식 주석 구현을 제거합니다.
- reusable library가 여러 플랫폼을 공식 지원하는 경우에만 필요한 branch를 유지합니다.

최종 Notebook에는 최소 진단, 확정 설정, 실제 실행 경로, 재현성 metadata만 남깁니다.

## 5. Notebook Bootstrap

권장 순서:

```text
목적
Environment Detection
Hardware / Memory Detection
Environment Profile Resolution
Environment Lock
UTF-8 / Path
Dependency Bootstrap
Imports
Resource Configuration
Experiment Configuration
Data
Model / Client
Training / Inference
Evaluation
Ablation
Visualization
Export
Reproducibility Metadata
```

새 Notebook은 fresh kernel/runtime에서 top-to-bottom 실행 가능해야 합니다.

## 6. Device / Precision

기본 우선순위는 CUDA → MPS → CPU입니다. 특정 accelerator를 무조건 가정하지 않고 resolved profile을 사용합니다.

실제 accelerator가 지원하면 mixed precision을 검토합니다. BF16은 하드웨어와 framework 지원 여부를 확인한 뒤 사용합니다.

## 7. Resource Optimization

GPU:

```text
batch size ↓
sequence/input size ↓
gradient accumulation
mixed precision
gradient checkpointing
quantization 검토
offload 검토
tensor/reference 정리
```

CPU/RAM:

```text
대용량 dataset 불필요한 전체 적재 금지
streaming / chunking / memory mapping
DataLoader worker 보수적 설정
prefetch / persistent worker 과다 사용 금지
중복 DataFrame/list/tensor 복사 금지
CPU/BLAS/OpenMP thread 제한 검토
```

GPU와 RAM을 100%까지 채우지 않습니다.

## 8. Memory Smoke Test

본 학습 전에 대표 workload를 작은 규모로 실행합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

다음을 기록합니다.

- peak VRAM
- peak RAM
- validation metric
- runtime
- resolved environment profile

Smoke Test 실패 시 본 학습을 시작하지 않고 resource configuration을 낮춘 후 재검증합니다.

## 9. OOM Recovery

```text
VRAM/RAM 기록
→ batch 감소
→ sequence/input 감소
→ workers 감소
→ precision 확인
→ gradient checkpointing
→ quantization/offload 검토
→ smoke test
→ 성공한 설정으로 실행
```

동일 실패 설정을 무한 재시도하지 않습니다.

## 10. Training Configuration

학습 설정은 하나의 명시적인 configuration에서 관리합니다.

```python
TRAIN_CONFIG = {
    **RUNTIME_CONFIG,
    "learning_rate": 2e-5,
    "num_train_epochs": 10,
    "eval_strategy": "epoch",
    "save_strategy": "epoch",
}
```

프로젝트의 실제 workload에 맞게 조정합니다.

## 11. Early Stopping

장시간 학습에는 validation 기반 Early Stopping을 기본 적용합니다.

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

필수:

- validation split/eval dataset
- metric과 방향
- patience
- best checkpoint 저장
- best checkpoint 복원
- early-stop 시점 기록

Hugging Face Trainer에서는 `EarlyStoppingCallback`, `metric_for_best_model`, `greater_is_better`, `load_best_model_at_end`를 일관되게 구성합니다.

## 12. Checkpoint / Resume

가능한 경우 다음을 저장합니다.

```text
model
optimizer
scheduler
AMP scaler
epoch / global step
best metric
Early Stopping counter
training config
seed
model revision
dataset revision
resolved environment profile
```

중단 후 resume 가능한 상태를 유지합니다.

## 13. Ablation Study

baseline을 먼저 정의하고 각 구성 요소를 독립적으로 제거/변경하는 variant matrix를 관리합니다.

```python
ABLATION_CONFIG = {
    "study_name": "components",
    "baseline": {
        "feature_a": True,
        "feature_b": True,
    },
    "variants": {
        "no_feature_a": {"feature_a": False},
        "no_feature_b": {"feature_b": False},
    },
    "seeds": [42, 43, 44],
    "primary_metric": "eval_loss",
    "metric_mode": "min",
}
```

가능한 한 data split, test set, metric, Early Stopping policy, maximum budget, checkpoint rule, seed set, resolved environment profile을 동일하게 유지합니다.

## 14. Experiment Tracking

각 실험에 다음을 기록합니다.

```text
experiment_id
variant
changed_parameters
seed
model_revision
dataset_revision
best_metric
best_epoch/step
early_stopped
peak_vram
peak_ram
runtime
checkpoint_path
resolved environment profile
```

## 15. Notebook Idempotency

반복 실행으로 결과가 무한 누적되지 않아야 합니다.

- 상태 초기화
- 결정적인 output path
- 임시 파일 정리
- overwrite 정책 명시

## 16. Validation Workflow

```text
1. Kernel/Runtime restart
2. Environment profiler 실행
3. Hardware / Memory 확인
4. Runtime configuration 생성
5. Memory Smoke Test
6. Environment Lock
7. 미사용 branch 정리
8. Baseline 학습/추론
9. Early Stopping 확인
10. Checkpoint save/resume 확인
11. Ablation 실행
12. metrics + resource 기록
13. dead code 제거
14. 최종 Run All
```

## 17. 완료 조건

```text
[ ] 실제 환경 감지
[ ] resource profile 생성
[ ] runtime configuration 확정
[ ] Memory Smoke Test 통과
[ ] Environment Lock
[ ] 미사용 environment branch 제거
[ ] OOM recovery 확인
[ ] validation metric
[ ] Early Stopping
[ ] best checkpoint / Resume
[ ] Ablation matrix
[ ] 동일 조건 비교
[ ] metric / VRAM / RAM / runtime 기록
[ ] clean kernel Run All
```
