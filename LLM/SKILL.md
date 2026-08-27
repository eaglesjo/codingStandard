# SKILL.md

# Jupyter / Google Colab Cross-Platform LLM Development Skill

## 목적

이 Skill은 Python 기반 LLM/ML 개발을 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 수행할 때 적용한다.

반드시 고려할 범위:

- Windows / Linux / macOS
- Jupyter / JupyterLab / VS Code
- Google Colab / Colab Local Runtime
- 활성 Python kernel
- dependency bootstrap
- UTF-8 / 한글
- CPU / CUDA / MPS
- 제한된 GPU VRAM / System RAM
- 환경 확정 후 불필요한 분기 제거
- Early Stopping / Checkpoint / Resume
- Ablation Study / Experiment Tracking
- reproducibility / security

## 1. 적용 대상

- `.ipynb` 생성/수정
- Python LLM / PyTorch / Transformers / Hugging Face
- embedding / RAG / evaluation
- ML experiment
- local GPU training / fine-tuning
- ablation study

## 2. 작업 시작 순서

환경 의존적인 작업 전에 다음을 확인한다.

```text
1. Python / active kernel
2. OS / architecture
3. Jupyter / Colab
4. GPU / CUDA / VRAM
5. System RAM / CPU
6. dependency
7. project root
8. experiment requirements
```

환경이 확정되기 전에는 범용 코드를 유지할 수 있다. 환경이 확정되면 사용하지 않는 실행 경로는 삭제한다.

## 3. Bootstrap Cell

새 Notebook:

```text
Cell 0: 목적
Cell 1: Environment Detection
Cell 2: Hardware / Memory Detection
Cell 3: Environment Lock / Resource Profile
Cell 4: UTF-8
Cell 5: Project Root
Cell 6: Dependency Bootstrap
Cell 7: Imports
Cell 8: Resource Configuration
Cell 9: Experiment Configuration
Cell 10+: Data / Model / Training / Evaluation
```

기존 Notebook은 사용자 코드를 먼저 보존하고 bootstrap을 추가한 후 검증이 끝나면 정리한다.

## 4. Environment Detection

```python
from __future__ import annotations

import locale
import platform
import sys
from pathlib import Path

IS_JUPYTER = "ipykernel" in sys.modules
IS_COLAB = "google.colab" in sys.modules


def detect_environment():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "cwd": str(Path.cwd()),
        "preferred_encoding": locale.getpreferredencoding(False),
        "filesystem_encoding": sys.getfilesystemencoding(),
        "jupyter": IS_JUPYTER,
        "colab": IS_COLAB,
    }


ENV = detect_environment()
```

## 5. Environment Lock / Branch Cleanup

초기에는 자동 감지 코드를 사용한다. 실제 실행 환경이 검증되면 profile을 확정하고 핵심 실행 코드에서는 사용하지 않는 branch를 제거한다.

```text
Detect
 ↓
Validate
 ↓
Lock profile
 ↓
Remove dead branches
 ↓
Run confirmed configuration
```

예를 들어 Windows + CUDA 환경이 확정된 프로젝트라면 핵심 training path에서 CPU/MPS용 대체 실행 코드를 삭제할 수 있다.

단, 여러 OS/device를 공식 지원하는 reusable library에서는 분기를 유지한다. 이 경우 detection과 execution을 분리한다.

최종 코드에 남길 것:

- 최소 환경 진단
- 확정된 device / dtype / worker configuration
- 실제 사용하는 실행 경로
- 재현성 metadata

삭제 권장:

- 사용하지 않는 OS/device branch
- 주석 처리된 이전 구현
- dead code
- 사용하지 않는 import
- 중복 environment detection

## 6. UTF-8 / Path

파일은 `encoding="utf-8"`을 명시하고 경로는 `pathlib.Path`를 사용한다.

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

## 7. Dependency Bootstrap

현재 Notebook kernel을 기준으로 설치한다.

```python
import importlib
import subprocess
import sys


def ensure_package(import_name: str, package_name: str | None = None):
    package_name = package_name or import_name
    try:
        return importlib.import_module(import_name)
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name
        ])
        return importlib.import_module(import_name)
```

프로젝트 dependency는 `pyproject.toml`, `requirements.txt`, lock file을 기준으로 한다.

## 8. Device Detection

```python
def detect_device():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


DEVICE = detect_device()
```

우선순위는 CUDA → MPS → CPU이다.

## 9. 기준 로컬 환경

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
VRAM: 4 GB
System RAM: 16 GB
```

보수적인 시작값:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
NUM_WORKERS = 0
USE_FP16 = True
GRADIENT_CHECKPOINTING = True
```

4 GB VRAM 전체와 16 GB RAM 전체를 채우지 않는다. 실제 자원 측정 결과로 조정한다.

## 10. Hardware / Memory Detection

학습 전에 실제 자원을 확인한다.

```python
import os
import platform


def inspect_resources():
    result = {"cpu_count": os.cpu_count(), "os": platform.system()}

    try:
        import psutil
        memory = psutil.virtual_memory()
        result["ram_total_gb"] = round(memory.total / 1024**3, 2)
        result["ram_available_gb"] = round(memory.available / 1024**3, 2)
    except ImportError:
        pass

    try:
        import torch
        if torch.cuda.is_available():
            free, total = torch.cuda.mem_get_info()
            result["vram_total_gb"] = round(total / 1024**3, 2)
            result["vram_free_gb"] = round(free / 1024**3, 2)
            result["gpu_name"] = torch.cuda.get_device_name(0)
    except (ImportError, RuntimeError):
        pass

    return result
```

## 11. GPU / CPU / RAM Optimization

GPU:

```text
batch size ↓
sequence/input size ↓
gradient accumulation
FP16 AMP
gradient checkpointing
8-bit / 4-bit quantization 검토
optimizer memory / CPU offload 검토
```

CPU/RAM:

```text
전체 dataset RAM 적재 금지
streaming/chunking/memory mapping
num_workers=0 또는 1부터 시작
persistent_workers 기본 비활성화
prefetch 과다 설정 금지
DataFrame/list/tensor 중복 복사 금지
CPU thread 무제한 증가 금지
```

추론:

```python
model.eval()
with torch.inference_mode():
    outputs = model(**inputs)
```

매 step마다 `torch.cuda.empty_cache()`를 호출하지 않는다.

## 12. Memory Smoke Test

본 학습 전에 작은 workload로 다음을 검증한다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

peak VRAM, RAM, loss, runtime을 기록한다.

Smoke Test가 실패하면 본 학습을 시작하지 않고 configuration을 낮춘다.

## 13. OOM Recovery

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
통과 시 학습
```

동일 configuration으로 무한 재시도하지 않는다.

## 14. Training Configuration

```python
TRAIN_CONFIG = {
    "batch_size": 1,
    "gradient_accumulation_steps": 8,
    "max_seq_length": 256,
    "learning_rate": 2e-5,
    "num_train_epochs": 10,
    "eval_strategy": "epoch",
    "save_strategy": "epoch",
    "mixed_precision": "fp16",
}
```

한 곳에서 관리하고 실험별로 저장한다.

## 15. Early Stopping

장시간 학습에는 validation 기반 Early Stopping을 기본 적용한다.

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

필수 원칙:

- validation split/eval dataset
- metric과 방향 명시
- patience 명시
- best checkpoint 저장
- best checkpoint 복원
- early stop 시점 기록

Hugging Face Trainer를 사용하면 `EarlyStoppingCallback`, `metric_for_best_model`, `greater_is_better`, `load_best_model_at_end`를 일관되게 설정한다.

직접 loop를 작성하면 같은 정책을 명시적으로 구현하고 테스트한다.

## 16. Checkpoint / Resume

가능한 경우 checkpoint에 다음을 포함한다.

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

중단 후 resume이 가능해야 한다.

## 17. Ablation Study

baseline을 먼저 정의하고 구성 요소의 효과를 분리한다.

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

Ablation 대상 예:

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

한 실험에서 변경 요인을 명확히 기록한다.

## 18. 공정한 Ablation / Experiment Matrix

모든 variant는 가능하면 다음을 동일하게 유지한다.

```text
train/validation split
test set
metric
Early Stopping policy
maximum budget
checkpoint rule
seed set
```

예:

```python
EXPERIMENTS = [
    {"name": "baseline", "feature_a": True, "feature_b": True},
    {"name": "no_feature_a", "feature_a": False, "feature_b": True},
    {"name": "no_feature_b", "feature_a": True, "feature_b": False},
]
```

결과에는 최소한 다음을 기록한다.

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

## 19. Experiment Tracking

권장 구조:

```text
experiments/
└── <study_name>/
    ├── baseline/
    ├── no_feature_a/
    ├── no_feature_b/
    └── no_augmentation/
```

각 variant의 configuration, metrics, resource usage, checkpoint를 저장한다.

## 20. Notebook Idempotency

cell을 여러 번 실행해도 결과가 무한 누적되지 않아야 한다.

- state 초기화
- deterministic output path
- 임시 파일 정리
- overwrite 정책 명시

clean kernel에서 Run All이 가능해야 한다.

## 21. Validation Workflow

```text
1. Kernel/Runtime restart
2. Run All
3. Environment/Resource 확인
4. Environment Lock
5. Memory Smoke Test
6. Baseline 학습
7. Early Stopping 동작 확인
8. Checkpoint save/resume 확인
9. Ablation 실행
10. metrics + resource 기록
11. dead code 제거
12. 최종 Run All
```

## 22. 완료 체크리스트

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

## 23. Definition of Done

- 실제 실행 환경을 확인했다.
- 확정된 환경에서 필요한 코드만 남겼다.
- 4 GB VRAM / 16 GB RAM 제약을 반영했다.
- Memory Smoke Test를 통과했다.
- Early Stopping이 적용됐다.
- best checkpoint와 Resume이 가능하다.
- baseline과 Ablation variant를 동일 조건에서 비교할 수 있다.
- metric, seed, configuration, resource 사용량을 기록한다.
- clean kernel/runtime에서 실행된다.
