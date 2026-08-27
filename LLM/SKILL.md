# SKILL.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development Skill

이 Skill은 Python 기반 LLM/ML 개발을 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 수행할 때 적용한다.

## 1. 적용 범위

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

가능하면 공통 프로파일러를 먼저 실행한다.

```bash
python LLM/environment.py
```

환경이 확정되기 전에는 범용 코드를 유지한다. 환경이 확정되면 resolved configuration을 만들고 사용하지 않는 실행 경로를 제거한다.

## 3. Bootstrap Cell

새 Notebook 권장 구조:

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

환경 탐지 결과를 실제 실행 설정으로 변환한다.

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

프로파일러 권장값은 시작점이며 모델/데이터별 Memory Smoke Test 결과가 최종 결정권을 가진다.

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

환경이 확정되면 각 cell에서 다시 device/worker/dtype을 임의로 결정하지 않는다.

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

## 7. 환경 중립성

특정 GPU, VRAM, RAM, OS, IDE를 기본 실행 환경으로 고정하지 않는다.

특정 개발 장비의 과거 설정이 필요하면 별도의 backup/reference 문서에만 보존한다. 그 문서는 runtime decision에 사용하지 않는다.

## 8. UTF-8 / Path

파일은 `encoding="utf-8"`을 명시하고 경로는 `pathlib.Path`를 사용한다.

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

사용자 컴퓨터의 절대 경로와 OS 전용 경로를 기본 코드에 하드코딩하지 않는다.

## 9. Dependency Bootstrap

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

## 10. Device Detection

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

## 11. Hardware / Memory Detection

학습 전에 실제 자원을 확인한다. `LLM/environment.py`의 `inspect_environment()`를 우선 사용한다.

측정 대상:

```text
OS
architecture
Python / executable
IDE / Jupyter / Colab
CPU count
System RAM total / available
GPU name
VRAM total / free
CUDA / MPS availability
resolved device
```

## 12. GPU / CPU / RAM Optimization

실제 측정값과 workload를 기준으로 다음을 조정한다.

```text
batch size ↓
sequence/input size ↓
gradient accumulation
AMP / mixed precision
gradient checkpointing
quantization 검토
offload 검토
```

CPU/RAM:

```text
전체 dataset RAM 적재 금지
streaming / chunking / memory mapping
worker 수 최소값부터 시작
persistent workers 남용 금지
prefetch 과다 설정 금지
DataFrame/list/tensor 중복 복제 금지
CPU thread 무제한 증가 금지
```

가용 VRAM/RAM을 100%까지 사용하지 않는다.

## 13. Mixed Precision

CUDA에서 실제 지원 여부가 확인된 경우 FP16 AMP를 기본 후보로 검토한다.

```python
USE_AMP = PROFILE.recommended_fp16
```

BF16은 실제 GPU와 PyTorch 지원 여부를 확인한 후 사용한다.

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

peak VRAM, peak RAM, loss, runtime 및 resolved environment profile을 기록한다. 실패하면 `RUNTIME_CONFIG`를 낮춘 후 다시 검증한다.

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

같은 configuration으로 무한 retry하지 않는다.

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

예시는 시작점이며 실제 모델/데이터/자원에 따라 조정한다.

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

## 21. 공정한 Experiment Matrix

가능하면 다음을 variant 간 동일하게 유지한다.

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

## 22. Notebook Idempotency

cell을 여러 번 실행해도 결과가 무한 누적되지 않아야 한다.

- state 초기화
- deterministic output path
- 임시 파일 정리
- overwrite 정책 명시

## 23. Validation Workflow

```text
1. Kernel/Runtime restart
2. Environment profiler 실행
3. Hardware / Memory 확인
4. Runtime configuration 생성
5. Environment Lock
6. Memory Smoke Test
7. Baseline 학습/추론
8. Early Stopping 동작 확인
9. Checkpoint save/resume 확인
10. Ablation 실행
11. metrics + resource 기록
12. dead code 제거
13. 최종 Run All
```

## 24. 완료 체크리스트

```text
Environment
[ ] OS / architecture
[ ] Python / active kernel
[ ] IDE / runtime
[ ] GPU / VRAM / CUDA/MPS
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

## 25. Definition of Done

- 실제 실행 환경을 확인했다.
- `LLM/environment.py` 결과로 runtime configuration을 결정했다.
- 특정 장비를 실행 전제조건으로 가정하지 않는다.
- 확정된 환경에서 필요한 코드만 남겼다.
- Memory Smoke Test를 통과했다.
- Early Stopping이 적용됐다.
- best checkpoint와 Resume이 가능하다.
- baseline과 Ablation variant를 동일 조건에서 비교할 수 있다.
- metric, seed, configuration, resource 사용량, environment profile을 기록한다.
- clean kernel/runtime에서 실행된다.
