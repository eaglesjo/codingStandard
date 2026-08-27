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
- 실제 실행 환경에 따른 runtime configuration 자동 결정
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
3. Jupyter / Colab / IDE
4. GPU / CUDA / VRAM
5. System RAM / CPU
6. dependency
7. project root
8. experiment requirements
```

가능하면 `LLM/environment.py`를 실행하여 실제 환경을 측정한다.

```bash
python LLM/environment.py
```

환경이 확정되기 전에는 범용 코드를 유지할 수 있다. 환경이 확정되면 resolved configuration을 만들고 사용하지 않는 실행 경로는 삭제한다.

## 3. Bootstrap Cell

새 Notebook:

```text
Cell 0: 목적
Cell 1: Environment Detection
Cell 2: Hardware / Memory Detection
Cell 3: Environment Profile Resolution
Cell 4: Environment Lock
Cell 5: UTF-8
Cell 6: Project Root
Cell 7: Dependency Bootstrap
Cell 8: Imports
Cell 9: Resource Configuration
Cell 10: Experiment Configuration
Cell 11+: Data / Model / Training / Evaluation
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

## 5. Environment Profile Resolution

환경 탐지 결과를 단순 출력으로 끝내지 않고 실제 실행 설정으로 변환한다.

```python
from pathlib import Path
import sys

LLM_STANDARD = Path("LLM")
if str(LLM_STANDARD) not in sys.path:
    sys.path.insert(0, str(LLM_STANDARD))

from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

필요한 경우 저장한다.

```python
from environment import save_profile

save_profile(PROFILE, ".codingstandard/environment-profile.json")
```

프로파일러가 권장하는 값은 시작값이며, 모델/데이터별 Memory Smoke Test 결과가 최종 결정권을 가진다.

## 6. Environment Lock / Branch Cleanup

```text
Detect
 ↓
Measure
 ↓
Resolve
 ↓
Smoke Test
 ↓
Lock profile
 ↓
Remove dead branches
 ↓
Run confirmed configuration
```

환경이 확정되면 매 cell에서 다시 device/worker/dtype을 판단하지 않는다.

최종 실행 코드에 남길 것:

- 최소 환경 진단
- 확정된 device / dtype / worker / batch configuration
- 실제 실행 경로
- resolved environment profile
- 재현성 metadata

삭제 권장:

- 사용하지 않는 OS/device branch
- 주석 처리된 이전 구현
- dead code
- 사용하지 않는 import
- 중복 environment detection

여러 플랫폼을 공식 지원하는 reusable library는 분기를 유지하되 detection과 execution을 분리한다.

## 7. UTF-8 / Path

파일은 `encoding="utf-8"`을 명시하고 경로는 `pathlib.Path`를 사용한다.

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

## 8. Dependency Bootstrap

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

## 9. Device Detection

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

우선순위는 CUDA → MPS → CPU이다. Profile Resolution 이후에는 `DEVICE = PROFILE.device`처럼 확정된 값을 재사용한다.

## 10. 기준 로컬 환경

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

## 11. Hardware / Memory Detection

학습 전에 실제 자원을 확인한다. `LLM/environment.py`의 `inspect_environment()`를 우선 사용한다.

## 12. GPU / CPU / RAM Optimization

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

## 13. Mixed Precision

CUDA에서는 FP16 AMP를 기본 후보로 검토한다.

```python
import torch

USE_AMP = PROFILE.device == "cuda"

with torch.autocast(
    device_type="cuda",
    dtype=torch.float16,
    enabled=USE_AMP,
):
    loss = model(**batch).loss
```

BF16은 실제 GPU/PyTorch 지원을 확인한 후 사용한다.

## 14. Gradient Accumulation

```python
BATCH_SIZE = RUNTIME_CONFIG["batch_size"]
GRADIENT_ACCUMULATION_STEPS = RUNTIME_CONFIG[
    "gradient_accumulation_steps"
]

loss = loss / GRADIENT_ACCUMULATION_STEPS
loss.backward()

if (step + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

effective batch size는 `batch_size × accumulation_steps × device_count`로 기록한다.

## 15. Memory Smoke Test

본 학습 전에 작은 workload로 다음을 검증한다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

peak VRAM, RAM, loss, runtime을 기록한다. 실패하면 본 학습을 시작하지 않고 `RUNTIME_CONFIG`를 낮춘다.

## 16. OOM / Memory Recovery

```text
1. VRAM/RAM 기록
2. batch size 감소
3. sequence/input size 감소
4. DataLoader workers 감소
5. AMP 활성화/검증
6. gradient checkpointing 검토
7. quantization/offload 검토
8. cache/reference 정리
9. 낮춘 configuration smoke test
10. 성공하면 재실행
```

동일 configuration으로 무한 retry하지 않는다.

## 17. Training Configuration

학습 configuration은 한 곳에서 관리한다.

```python
TRAIN_CONFIG = {
    **RUNTIME_CONFIG,
    "learning_rate": 2e-5,
    "num_train_epochs": 10,
    "eval_strategy": "epoch",
    "save_strategy": "epoch",
    "mixed_precision": "fp16" if PROFILE.recommended_fp16 else "no",
}
```

## 18. Early Stopping

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

## 19. Checkpoint / Resume

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
resolved environment profile
```

중단 후 resume이 가능해야 한다.

## 20. Ablation Study

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

## 21. 공정한 Ablation / Experiment Matrix

가능하면 다음을 동일하게 유지한다.

```text
train/validation split
test set
metric
Early Stopping policy
maximum budget
checkpoint rule
seed set
resolved environment profile
```

결과에는 다음을 기록한다.

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

## 22. Experiment Tracking

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

## 23. Notebook Idempotency

cell을 여러 번 실행해도 결과가 무한 누적되지 않아야 한다.

- state 초기화
- deterministic output path
- 임시 파일 정리
- overwrite 정책 명시

clean kernel에서 Run All이 가능해야 한다.

## 24. Validation Workflow

```text
1. Kernel/Runtime restart
2. Environment profiler 실행
3. Hardware/Memory 확인
4. Resource configuration 생성
5. Environment Lock
6. Memory Smoke Test
7. Baseline 학습
8. Early Stopping 동작 확인
9. Checkpoint save/resume 확인
10. Ablation 실행
11. metrics + resource 기록
12. dead code 제거
13. 최종 Run All
```

## 25. 완료 체크리스트

```text
Environment
[ ] OS / architecture
[ ] Python / active kernel
[ ] IDE / runtime
[ ] GPU / VRAM / CUDA
[ ] RAM / CPU
[ ] environment.py 실행
[ ] environment profile 생성
[ ] resolved runtime configuration 생성
[ ] environment lock
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
[ ] resolved environment profile 기록

Quality
[ ] clean kernel Run All
[ ] dead code 제거
[ ] reproducibility metadata
[ ] tests
```

## 26. Definition of Done

- 실제 실행 환경을 확인했다.
- environment.py 결과로 runtime configuration을 결정했다.
- 확정된 환경에서 필요한 코드만 남겼다.
- 4 GB VRAM / 16 GB RAM 제약을 반영했다.
- Memory Smoke Test를 통과했다.
- Early Stopping이 적용됐다.
- best checkpoint와 Resume이 가능하다.
- baseline과 Ablation variant를 동일 조건에서 비교할 수 있다.
- metric, seed, configuration, resource 사용량, environment profile을 기록한다.
- clean kernel/runtime에서 실행된다.
