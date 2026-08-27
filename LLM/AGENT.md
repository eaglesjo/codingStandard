# AGENT.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development

## 1. 목적

이 문서는 Python 기반 LLM/ML 프로젝트를 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 개발하는 AI Agent를 위한 공통 개발 규칙이다.

지원 환경:

- Windows / Linux / macOS
- venv / virtualenv / conda / uv
- Jupyter / JupyterLab / VS Code Jupyter
- Google Colab / Colab Local Runtime
- 로컬 저사양 GPU 개발 환경

핵심 목표:

- OS 독립성 및 재현 가능한 실행
- 활성 Python kernel 기준 dependency 관리
- UTF-8 / 한글 안전성
- CPU / CUDA / MPS 자동 감지
- 실제 환경 확인 후 불필요한 환경 분기 코드 제거
- 제한된 GPU VRAM / 시스템 RAM에서 안정적인 학습과 추론
- GPU VRAM / CPU / RAM 사용량 명시적 관리
- OOM 및 메모리 부족에 의한 학습 중단 최소화
- 모든 장시간 학습에 Early Stopping 및 Checkpoint/Resume 적용
- Ablation Study를 통한 구성 요소별 기여도 검증
- 재현 가능한 실험과 결과 기록
- Secret 안전 관리
- Notebook과 재사용 코드의 분리

## 2. 기본 원칙

1. Python 3.11+를 권장한다.
2. 재사용 가능한 로직은 `src/`에 둔다.
3. Notebook은 실험/탐색/시각화/평가 orchestration에 집중한다.
4. OS별 경로를 하드코딩하지 않고 `pathlib.Path`를 사용한다.
5. 파일 입출력 encoding은 명시한다.
6. API key, token, password를 코드에 넣지 않는다.
7. GPU/특정 패키지/특정 OS가 있다고 가정하지 않는다.
8. 새 Notebook에는 환경 Bootstrap을 상단에 둔다.
9. 새 Kernel/Runtime에서 `Run All`이 가능해야 한다.
10. 가용 VRAM/RAM을 먼저 확인하고 자원 사용량을 결정한다.
11. GPU/RAM을 100%까지 채우는 것을 목표로 하지 않는다.
12. `torch.cuda.empty_cache()`를 OOM의 1차 해결책으로 사용하지 않는다.
13. 같은 설정으로 OOM을 무한 재시도하지 않는다.
14. 실험 코드는 명시적인 configuration object/section을 사용한다.
15. 학습 코드에는 검증 지표, Early Stopping, Checkpoint가 기본적으로 포함되어야 한다.

## 3. 기준 로컬 개발 환경

기본 로컬 프로파일:

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM: 4 GB
System RAM: 16 GB
```

4 GB VRAM을 가장 중요한 제약으로 취급한다.

권장 시작 예산:

- GPU 실사용 목표: 약 3.0~3.5 GB 이하를 우선 목표로 하며 최소한의 여유 VRAM을 남긴다.
- RAM: Windows, VS Code, Jupyter, browser 및 백그라운드 프로세스가 사용할 공간을 남긴다.
- DataLoader: Windows에서는 `num_workers=0` 또는 `1`부터 시작한다.
- Batch: 기본 `batch_size=1`에서 시작하고 필요한 effective batch size는 gradient accumulation으로 확보한다.

이 수치는 고정 한도가 아니라 보수적인 시작점이다. 실제 모델과 runtime을 측정하여 조정한다.

## 4. 환경 탐지 → 환경 확정 → 코드 정리 원칙

개발 초기에만 환경 자동 탐지를 수행한다.

권장 흐름:

```text
환경 탐지
  ↓
실제 사용 환경 검증
  ↓
환경 profile 확정
  ↓
실행 경로 선택
  ↓
불필요한 OS/device 분기 제거
  ↓
확정된 환경에 최적화된 실행 코드 유지
```

### 4.1 환경이 확정된 후의 코드

환경 확인이 끝나고 실행 대상이 하나로 확정되면, 해당 실행 경로를 명시하고 사용하지 않는 대체 경로 코드는 삭제한다.

예:

```python
# 탐지 단계
DEVICE = detect_device()
```

탐지 결과가 실제로 `cuda`이고 프로젝트가 Windows + CUDA만을 대상으로 실행되는 것이 확정되었다면 이후 핵심 학습 코드에 다음과 같은 불필요한 분기를 남기지 않는다.

```python
if DEVICE == "cuda":
    ...
elif DEVICE == "cpu":
    ...
elif DEVICE == "mps":
    ...
```

대신 확정된 configuration을 적용한다.

```python
DEVICE = "cuda"
```

그리고 CUDA가 아닌 경로에만 존재하던 코드가 더 이상 필요하지 않다면 삭제한다.

단, **재사용 가능한 라이브러리/배포 코드**가 여러 플랫폼을 공식 지원해야 한다면 분기를 유지할 수 있다. 이 경우에도 탐지 로직과 실행 로직을 분리한다.

### 4.2 최종 Notebook에서 남겨야 할 것

- 현재 환경을 표시하는 최소 진단 코드
- 확정된 device / dtype / worker 설정
- 실제 사용하는 코드 경로
- 재현에 필요한 configuration

삭제 권장:

- 사용하지 않는 CPU/MPS/CUDA 대체 코드
- 실패한 실험용 임시 코드
- 이미 확정된 환경을 다시 판단하는 중복 분기
- 주석 처리된 오래된 구현
- 사용하지 않는 import

## 5. Notebook 표준 구조

권장 순서:

1. 목적 Markdown
2. Environment Detection
3. Hardware / Memory Detection
4. Environment Lock / Resource Profile
5. UTF-8
6. Project Root
7. Dependency Bootstrap
8. Imports
9. Resource Configuration
10. Experiment Configuration
11. Data
12. Model / Client
13. Training / Inference
14. Evaluation
15. Ablation
16. Visualization
17. Export
18. Reproducibility Metadata

## 6. 환경 자동 감지

```python
from pathlib import Path
import locale
import platform
import sys


def detect_environment():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "cwd": str(Path.cwd()),
        "is_jupyter": "ipykernel" in sys.modules,
        "is_colab": "google.colab" in sys.modules,
        "preferred_encoding": locale.getpreferredencoding(False),
        "filesystem_encoding": sys.getfilesystemencoding(),
    }


ENV = detect_environment()
```

## 7. 활성 Kernel 기준 dependency

Notebook에서는 가능하면 `sys.executable -m pip`를 사용한다.

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
            sys.executable,
            "-m",
            "pip",
            "install",
            package_name,
        ])
        return importlib.import_module(import_name)
```

정식 dependency source는 `pyproject.toml`, `requirements.txt`, lock file이다.

## 8. Cross-platform Path / UTF-8

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

파일 입출력에는 `encoding="utf-8"`을 명시한다.

Windows 전용 사용자 경로와 Unix 전용 shell command를 코드의 기본 경로로 사용하지 않는다.

## 9. CPU / CUDA / MPS

우선순위는 CUDA → MPS → CPU이다.

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
```

모델 코드에 `cuda`를 무조건 하드코딩하지 않는다. 다만 환경이 검증되고 특정 환경에 맞춘 프로젝트로 확정한 뒤에는 미사용 device 경로를 삭제할 수 있다.

## 10. GPU / RAM 자원 프로파일링

학습 전에 실제 자원을 측정한다.

```python
import os
import platform


def inspect_resources():
    result = {
        "cpu_count": os.cpu_count(),
        "os": platform.system(),
    }

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

`nvidia-smi`를 필수 dependency로 가정하지 않는다.

## 11. GPU 메모리 최적화

4 GB VRAM 환경에서는 다음 순서로 완화한다.

1. `batch_size=1`
2. sequence length / image resolution 축소
3. gradient accumulation
4. FP16 AMP
5. gradient checkpointing
6. 8-bit / 4-bit quantization 검토
7. optimizer memory 축소 또는 CPU offload 검토
8. 불필요한 tensor/reference 제거
9. validation/inference 중 `torch.inference_mode()` 사용
10. 중간 결과 무제한 누적 금지

권장 시작값:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
USE_FP16 = True
GRADIENT_CHECKPOINTING = True
```

모델에 따라 실제 측정 후 조정한다.

## 12. CPU / RAM 최적화

- Windows Notebook의 DataLoader는 `num_workers=0` 또는 `1`에서 시작한다.
- `pin_memory=True`는 CUDA에서 필요성이 확인된 경우 사용한다.
- `persistent_workers=True`는 worker 증가로 RAM이 충분히 남는 경우에만 사용한다.
- 대용량 dataset을 한 번에 RAM에 복제하지 않는다.
- pandas DataFrame 복사, Python list 중복, tokenized cache 중복을 피한다.
- 가능하면 streaming / chunking / memory-mapped 구조를 사용한다.
- CPU thread 수와 BLAS/OpenMP thread 수를 무제한으로 늘리지 않는다.

## 13. Mixed Precision

CUDA에서는 FP16 AMP를 기본 후보로 검토한다.

```python
import torch

USE_AMP = DEVICE == "cuda"

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
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8

loss = loss / GRADIENT_ACCUMULATION_STEPS
loss.backward()

if (step + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

effective batch size는 `batch_size × accumulation_steps × device_count`로 기록한다.

## 15. OOM / Memory Recovery

OOM 발생 시 순서:

```text
1. 현재 VRAM/RAM 기록
2. batch size 감소
3. sequence/input size 감소
4. DataLoader worker 감소
5. AMP 활성화/검증
6. gradient checkpointing 검토
7. quantization/offload 검토
8. 필요 없는 cache/reference 제거
9. 낮춘 설정으로 smoke test
10. 성공하면 해당 configuration으로 재실행
```

같은 configuration으로 무한 retry하지 않는다.

## 16. 학습은 Early Stopping을 기본값으로 한다

모든 장시간 학습에는 validation metric과 Early Stopping을 적용한다.

원칙:

- `eval_dataset` 또는 별도 validation split을 사용한다.
- 모니터링할 metric을 명시한다.
- metric 방향(`minimize` / `maximize`)을 명시한다.
- `patience`를 설정한다.
- `min_delta` 또는 동등한 최소 개선량 기준을 사용한다.
- 가장 좋은 checkpoint를 저장한다.
- Early Stop 발생 후 best checkpoint를 복원한다.
- 학습 중 validation metric, epoch/step, LR, loss를 기록한다.

권장 시작 예:

```python
EARLY_STOPPING = True
EARLY_STOPPING_METRIC = "eval_loss"
EARLY_STOPPING_MODE = "min"
EARLY_STOPPING_PATIENCE = 3
EARLY_STOPPING_MIN_DELTA = 0.0
SAVE_BEST_CHECKPOINT = True
RESTORE_BEST_CHECKPOINT = True
```

Hugging Face Trainer를 사용하는 경우 해당 Trainer의 EarlyStoppingCallback과 metric 설정을 활용한다. 직접 training loop를 작성하는 경우 Early Stopping 상태를 명시적으로 구현하고 테스트한다.

## 17. Checkpoint / Resume

학습은 중단되어도 재개할 수 있어야 한다.

Checkpoint에는 가능한 경우 다음을 저장한다.

- model weights
- optimizer state
- scheduler state
- scaler state
- current epoch / global step
- best metric
- Early Stopping counter
- training configuration
- seed
- model/dataset revision

16 GB RAM / 4 GB VRAM 환경에서는 checkpoint를 지나치게 자주 저장하여 I/O와 디스크 사용량을 증가시키지 않는다.

## 18. Ablation Study 설정

학습에 영향을 주는 구성 요소는 명시적인 configuration으로 관리하여 동일한 실험을 반복 가능하게 만든다.

Ablation 대상 예:

- base vs proposed feature
- prompt component on/off
- retrieval on/off
- reranker on/off
- augmentation on/off
- loss component on/off
- quantization on/off
- context length
- embedding model
- optimizer
- learning rate
- batch/effective batch
- gradient checkpointing

모든 실험은 하나의 baseline에서 시작하고 **한 번에 하나 또는 사전에 정의한 소수의 요인만 변경**한다.

권장 configuration 예:

```python
ABLATION_CONFIG = {
    "enabled": True,
    "study_name": "model_components",
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
    "secondary_metrics": ["accuracy", "f1"],
}
```

Ablation 결과에는 반드시 다음을 기록한다.

```text
experiment_id
variant
changed_parameters
seed
model_revision
dataset_revision
device
training_steps / epochs
best_epoch / step
early_stopped
best_metric
secondary_metrics
VRAM peak
RAM peak
runtime
checkpoint path
```

### 18.1 공정한 비교

- 동일 dataset split
- 동일 evaluation set
- 가능한 동일 seed 집합
- 동일 Early Stopping 정책
- 동일 최대 epoch/step budget
- 동일 metric 정의
- 동일 checkpoint selection 규칙

을 유지한다.

Ablation 결과를 단순 평균 하나로 끝내지 말고 variant별 metric과 자원 사용량을 함께 비교한다.

## 19. Experiment Tracking

최소한 다음 구조를 권장한다.

```text
experiments/
└── <study_name>/
    ├── baseline/
    ├── no_feature_a/
    ├── no_feature_b/
    └── no_augmentation/
```

각 실험은 configuration을 파일로 저장하고 결과 이름에 variant/seed를 포함한다.

## 20. Notebook Idempotency

cell을 여러 번 실행해도 결과가 무한 누적되지 않아야 한다.

- 명시적인 state 초기화
- deterministic output path
- 임시 파일 정리
- 기존 결과 overwrite 여부 명시

새 Kernel/Runtime에서 `Run All`이 가능해야 한다.

## 21. Secret 관리

```python
import os
API_KEY = os.getenv("OPENAI_API_KEY")
```

`.env`, token, credential, private key는 Git에 commit하지 않는다.

## 22. 재현성

```python
SEED = 42
```

가능하면 Python, OS, architecture, package versions, model/dataset revision, device, training parameters, seed, prompt version, metrics, checkpoint 정보를 저장한다.

## 23. Agent 작업 순서

```text
1. repository 구조 확인
2. AGENT.md / SKILL.md 확인
3. dependency manifest 확인
4. 환경 감지
5. GPU/RAM 측정
6. 환경 profile 확정
7. 불필요한 환경 분기 제거
8. resource configuration 확정
9. baseline 정의
10. training/evaluation metric 정의
11. Early Stopping + checkpoint 설정
12. Ablation matrix 정의
13. 구현
14. memory smoke test
15. clean kernel Run All
16. baseline 실행
17. ablation 실행
18. 결과 및 자원 사용량 검증
19. 변경사항 보고
```

## 24. 완료 조건

```text
[ ] OS / architecture 확인
[ ] Python / active kernel 확인
[ ] GPU / VRAM 확인
[ ] RAM 확인
[ ] 확정된 환경 profile 기록
[ ] 불필요한 환경 분기 제거
[ ] cross-platform path
[ ] UTF-8
[ ] CPU/CUDA/MPS 확인
[ ] resource budget 설정
[ ] batch / sequence / workers 설정
[ ] AMP 여부 결정
[ ] OOM recovery 전략 존재
[ ] validation metric 존재
[ ] Early Stopping 적용
[ ] best checkpoint 저장
[ ] Resume 가능
[ ] baseline 정의
[ ] Ablation matrix 정의
[ ] 동일 조건 비교
[ ] experiment metadata 기록
[ ] memory/runtime 기록
[ ] clean kernel Run All
[ ] tests 실행
```
