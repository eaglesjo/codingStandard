# LLM Coding Standard

Python 기반 LLM/ML 개발을 위한 `AGENT.md`와 `SKILL.md` 사용 가이드입니다.

이 표준은 **Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, Colab Local Runtime**을 대상으로 하며 **Windows / Linux / macOS** 호환성과 로컬 저사양 GPU에서의 안정적인 학습을 함께 고려합니다.

---

## 1. 구성

```text
LLM/
├── AGENT.md
├── SKILL.md
└── README.md
```

### AGENT.md

AI Agent가 프로젝트를 수정할 때 따라야 하는 상위 개발 규칙입니다.

주요 내용:

- Python / Notebook / project 구조
- OS / Jupyter / Colab 호환성
- CPU / CUDA / MPS
- GPU VRAM / System RAM 최적화
- 환경 탐지 및 확정
- 확정 환경에서 dead branch 제거
- Early Stopping
- Checkpoint / Resume
- Ablation Study
- Experiment Tracking
- 재현성 / 보안 / 테스트

### SKILL.md

LLM/Jupyter 작업을 수행할 때 실제 적용하는 실행 절차입니다.

주요 작업:

- Notebook 생성/수정
- PyTorch / Transformers / Hugging Face
- local GPU training / fine-tuning
- inference
- evaluation
- memory smoke test
- OOM recovery
- Early Stopping
- Ablation Study

---

# 2. 기준 로컬 개발 환경

이 표준의 기본 로컬 프로파일은 다음과 같습니다.

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM: 4 GB
System RAM: 16 GB
```

핵심 원칙은 **4 GB VRAM과 16 GB RAM을 제한 자원으로 보고 보수적으로 시작한 뒤 실제 사용량을 측정하여 확장하는 것**입니다.

권장 시작점:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
NUM_WORKERS = 0
USE_FP16 = True
GRADIENT_CHECKPOINTING = True
```

전체 VRAM/RAM을 100% 사용하도록 설정하지 않습니다.

---

# 3. 환경 탐지 → 확정 → 코드 정리

개발 초기에는 여러 환경을 자동 감지합니다.

```text
Environment Detection
        ↓
Hardware / Runtime Validation
        ↓
Environment Profile Lock
        ↓
사용 device / dtype / workers 확정
        ↓
불필요한 branch 및 dead code 삭제
        ↓
확정 환경에 최적화된 코드 실행
```

예를 들어 실제 개발 환경이 Windows + CUDA로 확정되었다면 핵심 training path에 필요 없는 CPU/MPS 실행 코드를 남기지 않습니다.

최종 Notebook에는 다음만 남기는 것을 원칙으로 합니다.

- 최소 환경 진단
- 확정된 configuration
- 실제 사용하는 코드
- 재현성 metadata

단, library가 여러 플랫폼을 공식 지원해야 한다면 분기를 유지할 수 있습니다. 그 경우 detection과 execution을 분리합니다.

---

# 4. Notebook Bootstrap

권장 구조:

```text
Cell 0  : 목적
Cell 1  : Environment Detection
Cell 2  : Hardware / Memory Detection
Cell 3  : Environment Lock / Resource Profile
Cell 4  : UTF-8
Cell 5  : Project Root
Cell 6  : Dependency Bootstrap
Cell 7  : Imports
Cell 8  : Resource Configuration
Cell 9  : Experiment Configuration
Cell 10+: Data / Model / Training / Evaluation
```

Clean kernel에서 `Run All`이 가능해야 합니다.

---

# 5. GPU / CPU / RAM 최적화

## GPU

4 GB VRAM 환경에서는 다음 순서를 우선합니다.

```text
batch size ↓
sequence/input size ↓
gradient accumulation
FP16 AMP
gradient checkpointing
8-bit / 4-bit quantization 검토
optimizer memory / CPU offload 검토
```

## CPU / RAM

16 GB RAM 환경에서는 다음을 지킵니다.

- 전체 dataset의 무조건적 RAM 적재를 피합니다.
- streaming / chunking / memory mapping을 우선 검토합니다.
- DataLoader `num_workers=0` 또는 `1`부터 시작합니다.
- `persistent_workers=True`는 기본값으로 사용하지 않습니다.
- prefetch를 과도하게 높이지 않습니다.
- DataFrame/list/tensor 중복 복사를 피합니다.
- CPU thread를 무제한으로 증가시키지 않습니다.

추론:

```python
model.eval()
with torch.inference_mode():
    outputs = model(**inputs)
```

---

# 6. Memory Smoke Test

본 학습 전에 작은 workload로 다음 흐름을 검증합니다.

```text
model load
  ↓
forward
  ↓
backward
  ↓
optimizer step
  ↓
validation
  ↓
checkpoint save
```

이 단계에서 peak VRAM, RAM, loss, runtime을 기록합니다.

Smoke Test가 실패하면 본 학습을 시작하지 않고 batch / input / worker / precision 등의 자원 설정을 낮춥니다.

---

# 7. OOM Recovery

CUDA OOM 또는 RAM 부족이 발생하면 같은 configuration을 무한 재시도하지 않습니다.

```text
OOM 감지
 ↓
VRAM/RAM 기록
 ↓
batch size 감소
 ↓
sequence/input 감소
 ↓
workers 감소
 ↓
AMP 확인
 ↓
checkpointing / quantization / offload 검토
 ↓
smoke test
 ↓
통과 시 본 학습
```

`torch.cuda.empty_cache()`만으로 문제를 해결하려 하지 않습니다.

---

# 8. Early Stopping

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

필수 조건:

- validation split 또는 eval dataset
- monitoring metric
- minimize/maximize 방향
- patience
- best checkpoint
- best checkpoint 복원
- Early Stop 시점 기록

Hugging Face Trainer 사용 시 `EarlyStoppingCallback`, `metric_for_best_model`, `greater_is_better`, `load_best_model_at_end`를 일관되게 설정합니다.

---

# 9. Checkpoint / Resume

학습은 중단되어도 재개할 수 있어야 합니다.

가능한 경우 checkpoint에 다음을 저장합니다.

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
```

---

# 10. Ablation Study

Ablation은 하나의 baseline을 기준으로 구성 요소의 기여도를 검증하기 위해 사용합니다.

권장 설정:

```python
ABLATION_CONFIG = {
    "study_name": "components",
    "baseline": {
        "feature_a": True,
        "feature_b": True,
        "augmentation": True,
    },
    "variants": {
        "no_feature_a": {"feature_a": False},
        "no_feature_b": {"feature_b": False},
        "no_augmentation": {"augmentation": False},
    },
    "seeds": [42, 43, 44],
    "primary_metric": "eval_loss",
    "metric_mode": "min",
}
```

대상 예:

- model component / feature
- prompt component
- retrieval / reranker
- augmentation
- loss component
- optimizer
- learning rate
- context length
- embedding model
- quantization

가능하면 variant마다 한 가지 주요 요인만 변경합니다.

---

# 11. 공정한 Ablation

모든 variant는 가능하면 동일 조건으로 비교합니다.

```text
same train/validation split
same test set
same metric
same Early Stopping policy
same maximum budget
same checkpoint rule
same seed set
```

결과에 다음을 기록합니다.

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
```

단순 metric뿐 아니라 **VRAM / RAM / 실행시간**도 함께 비교합니다.

---

# 12. Experiment Matrix

Ablation은 코드에 흩어진 magic number가 아니라 명시적인 matrix로 관리합니다.

```python
EXPERIMENTS = [
    {"name": "baseline", "feature_a": True, "feature_b": True},
    {"name": "no_feature_a", "feature_a": False, "feature_b": True},
    {"name": "no_feature_b", "feature_a": True, "feature_b": False},
]
```

권장 결과 구조:

```text
experiments/
└── <study_name>/
    ├── baseline/
    ├── no_feature_a/
    ├── no_feature_b/
    └── no_augmentation/
```

---

# 13. Agent에게 요청하는 방법

예:

```text
이 프로젝트의 LLM 개발에 codingStandard/LLM/AGENT.md와
SKILL.md 규칙을 적용해.

현재 환경을 먼저 확인하고 Windows + VS Code + RTX 3050 Ti
4GB VRAM + RAM 16GB에 맞게 resource profile을 확정해.
환경이 확정되면 사용하지 않는 OS/device 분기와 dead code는 제거해.

학습에는 validation 기반 Early Stopping과 best checkpoint/
Resume을 적용하고, 실험 비교가 필요하면 baseline과
Ablation matrix를 만들어 동일 조건으로 실행해.
본 학습 전에 memory smoke test도 수행해.
```

---

# 14. 완료 조건

```text
Environment
[ ] OS / architecture
[ ] Python / active kernel
[ ] GPU / VRAM
[ ] RAM / CPU
[ ] environment profile 확정
[ ] 미사용 environment branch 삭제

Memory
[ ] batch size
[ ] sequence/input size
[ ] workers
[ ] AMP
[ ] gradient accumulation
[ ] checkpointing/quantization 검토
[ ] memory smoke test
[ ] OOM recovery

Training
[ ] validation metric
[ ] Early Stopping
[ ] best checkpoint
[ ] Resume

Ablation
[ ] baseline
[ ] variants
[ ] controlled variables
[ ] seed matrix
[ ] primary/secondary metrics
[ ] VRAM/RAM/runtime 기록

Quality
[ ] clean kernel Run All
[ ] dead code 제거
[ ] reproducibility metadata
[ ] tests
```

---

# 15. 관련 파일

- `AGENT.md` — Agent 상위 개발 규칙
- `SKILL.md` — 실행 절차 및 개발 패턴
- `README.md` — 설치, 적용, 운영 가이드
