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
- 제한된 GPU VRAM / System RAM 환경의 학습 및 추론
- reproducibility
- security
- notebook automation

## 1. 적용 대상

다음 작업에 이 Skill을 적용한다.

- `.ipynb` 생성/수정
- Jupyter/JupyterLab
- Google Colab
- Python LLM
- PyTorch
- Transformers
- Hugging Face
- embedding
- RAG
- vector database
- prompt engineering
- model evaluation
- ML/data experiment
- local GPU training / fine-tuning

## 2. 작업 시작 시 환경 확인

환경 의존적인 작업 전에 다음을 실행한다.

```python
import platform
import sys
from pathlib import Path

print("Python:", sys.version)
print("Executable:", sys.executable)
print("OS:", platform.system())
print("Architecture:", platform.machine())
print("CWD:", Path.cwd())
print("Jupyter:", "ipykernel" in sys.modules)
print("Colab:", "google.colab" in sys.modules)
```

패키지 설치 기준은 반드시 현재 notebook kernel의 `sys.executable`이다.

## 3. Bootstrap Cell 자동 삽입

새 Notebook을 만들면 experiment code보다 먼저 다음 셀을 자동으로 생성한다.

```text
Cell 0: Markdown - 목적
Cell 1: Environment Detection
Cell 2: Hardware / Memory Detection
Cell 3: UTF-8 Configuration
Cell 4: Project Root Detection
Cell 5: Dependency Bootstrap
Cell 6: Resource Configuration
Cell 7: Imports
Cell 8: Configuration
Cell 9+: Experiment
```

기존 Notebook에 bootstrap이 없으면 사용자 코드를 삭제하지 않고 상단에 추가한다.

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

for key, value in ENV.items():
    print(f"{key}: {value}")
```

## 5. UTF-8

```python
import sys

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

print("한글 UTF-8 테스트: 정상")
```

파일은 항상 encoding을 명시한다.

```python
from pathlib import Path

text = Path(path).read_text(encoding="utf-8")
Path(path).write_text(text, encoding="utf-8")
```

JSON/CSV에도 명시적인 UTF-8을 사용한다.

## 6. Project Root

```python
from pathlib import Path
import sys

ROOT = Path.cwd()

for parent in [ROOT, *ROOT.parents]:
    if (
        (parent / "pyproject.toml").exists()
        or (parent / ".git").exists()
        or (parent / "src").exists()
    ):
        ROOT = parent
        break

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

## 7. Dependency Bootstrap

핵심 함수:

```python
import importlib
import subprocess
import sys


def ensure_package(
    import_name: str,
    package_name: str | None = None,
):
    package_name = package_name or import_name

    try:
        return importlib.import_module(import_name)
    except ImportError:
        print(f"Installing missing package: {package_name}")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            package_name,
        ])
        return importlib.import_module(import_name)
```

예:

```python
ensure_package("numpy")
ensure_package("pandas")
ensure_package("matplotlib")
ensure_package("transformers")
ensure_package("sklearn", "scikit-learn")
```

매번 설치하지 않는다. 프로젝트의 dependency manifest가 기준이다.

## 8. Version-aware Dependency

재현성이 중요한 경우 버전을 지정한다.

```python
ensure_package(
    "transformers",
    "transformers==X.Y.Z",
)
```

가능하면 실제 버전은 `pyproject.toml` 또는 lock file과 일치시킨다.

## 9. OS 처리

```python
import platform

OS = platform.system()

if OS == "Windows":
    ...
elif OS == "Darwin":
    ...
elif OS == "Linux":
    ...
else:
    raise RuntimeError(f"Unsupported OS: {OS}")
```

가능하면 OS 분기보다 Python 표준 API를 사용한다.

## 10. Cross-platform Path

```python
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

고정 사용자 경로와 직접 만든 path separator를 사용하지 않는다.

## 11. Colab

```python
IS_COLAB = "google.colab" in sys.modules
WORKSPACE = Path("/content") if IS_COLAB else ROOT
```

Colab runtime filesystem은 임시 저장 공간으로 취급한다.

필요할 때만 Drive를 mount한다.

```python
def mount_google_drive():
    if not IS_COLAB:
        return False

    from google.colab import drive
    drive.mount("/content/drive")
    return True
```

Colab Local Runtime은 로컬 시스템에서 코드를 실행할 수 있으므로 신뢰할 수 있는 Notebook만 실행한다.

## 12. GPU / Device

```python
def detect_device():
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"

        if (
            hasattr(torch.backends, "mps")
            and torch.backends.mps.is_available()
        ):
            return "mps"

    except ImportError:
        pass

    return "cpu"


DEVICE = detect_device()
print("Device:", DEVICE)
```

우선순위는 CUDA → MPS → CPU이다.

## 13. 기준 로컬 개발 환경: Windows / VS Code / RTX 3050 Ti 4 GB / RAM 16 GB

이 Skill의 로컬 LLM/ML 기본 프로파일은 다음 환경을 기준으로 한다.

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM: 4 GB
System RAM: 16 GB
```

4 GB VRAM을 최우선 제약으로 취급한다. 더 큰 GPU/RAM이 감지되더라도 기본 설정은 보수적으로 시작하고 실제 자원 사용량을 확인한 후 단계적으로 증가시킨다.

권장 시작 예산:

- VRAM: 전체 4 GB를 채우지 않는다. 가능하면 약 3.0~3.5 GB 이하를 실사용 목표로 하고 0.5~1.0 GB의 여유를 둔다.
- RAM: Windows, VS Code, Jupyter 및 백그라운드 프로세스용 공간을 남긴다. 16 GB 전체를 dataset/cache에 할당하지 않는다.
- CPU: 데이터 전처리/토크나이징/I/O에 활용하되 DataLoader worker를 과도하게 늘리지 않는다.

이 값은 절대적인 안전 한도가 아니라 시작점이다. 실제 모델과 데이터에 따라 조정한다.

## 14. Hardware / Memory Detection

학습 또는 대규모 추론 전에 실제 가용 자원을 확인한다.

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


RESOURCES = inspect_resources()
for key, value in RESOURCES.items():
    print(f"{key}: {value}")
```

가능하면 `nvidia-smi`가 아니라 PyTorch API를 이용해 코드 자체의 이식성을 유지한다.

## 15. GPU Memory Optimization

RTX 3050 Ti 4 GB에서는 다음 순서를 기본 전략으로 사용한다.

1. `batch_size=1`부터 시작한다.
2. effective batch size가 필요하면 gradient accumulation을 사용한다.
3. sequence length / block size / image resolution 등 입력 크기를 먼저 줄인다.
4. CUDA에서는 FP16 mixed precision을 우선 검토한다.
5. activation memory가 큰 모델은 gradient checkpointing을 검토한다.
6. Hugging Face/Transformers에서는 가능한 경우 8-bit/4-bit quantization을 검토한다.
7. optimizer state가 크면 메모리 효율적인 optimizer 또는 CPU offload를 검토한다.
8. 추론에서는 `model.eval()` + `torch.inference_mode()`를 사용한다.
9. 필요 없는 tensor reference를 유지하지 않는다.
10. 대형 결과를 Python list에 무한 누적하지 않는다.
11. 매 step마다 `torch.cuda.empty_cache()`를 호출하지 않는다.
12. CUDA OOM 발생 시 동일 설정을 무한 재시도하지 말고 resource profile을 낮춘다.

권장 시작 configuration:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
USE_FP16 = True
GRADIENT_CHECKPOINTING = True
```

모든 모델에 위 값을 강제하지 않는다. 실제 메모리 측정 결과를 기준으로 조정한다.

## 16. Mixed Precision

CUDA 학습에서는 FP32 전체 학습보다 mixed precision을 우선 검토한다.

```python
import torch

USE_AMP = DEVICE == "cuda"
AMP_DTYPE = torch.float16
```

```python
with torch.autocast(
    device_type="cuda",
    dtype=torch.float16,
    enabled=USE_AMP,
):
    loss = model(**batch).loss
```

RTX 3050 Ti 4 GB에서는 FP16을 기본 후보로 사용한다. BF16은 실제 GPU/PyTorch 지원 여부를 확인한 후 사용한다.

## 17. Gradient Accumulation

작은 VRAM에서 batch size를 키우지 않고 effective batch size를 확보한다.

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8

loss = loss / GRADIENT_ACCUMULATION_STEPS
loss.backward()

if (step + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

effective batch size:

```text
effective_batch_size = batch_size × gradient_accumulation_steps × world_size
```

단일 RTX 3050 Ti에서는 일반적으로 `world_size=1`이다.

## 18. Gradient Checkpointing

activation memory가 병목일 때 gradient checkpointing을 사용한다.

```python
if hasattr(model, "gradient_checkpointing_enable"):
    model.gradient_checkpointing_enable()
```

계산량이 증가하므로 VRAM 절감이 실제로 필요한 경우 우선 적용한다.

## 19. Inference Memory

추론에서는 training graph를 만들지 않는다.

```python
model.eval()

with torch.inference_mode():
    outputs = model(**inputs)
```

`max_new_tokens`를 무제한으로 두지 않는다.

```python
MAX_NEW_TOKENS = 256
```

4 GB VRAM에서는 입력 길이와 생성 길이를 동시에 크게 설정하지 않는다.

## 20. CPU / System RAM Optimization

16 GB RAM 환경에서 RAM을 VRAM의 무제한 대체 공간처럼 사용하지 않는다.

규칙:

- 전체 dataset을 RAM에 무조건 로드하지 않는다.
- 가능하면 streaming, chunking, memory mapping을 사용한다.
- 대용량 pandas DataFrame을 불필요하게 복제하지 않는다.
- 대규모 `list(...)` 변환으로 데이터를 복사하지 않는다.
- DataLoader `num_workers`는 0 또는 1부터 시작한다.
- worker를 늘릴 때 RAM 사용량과 Windows 안정성을 확인한다.
- CUDA DataLoader에서 `pin_memory=True`는 전송 병목이 있고 RAM 여유가 있을 때 사용한다.
- `persistent_workers=True`는 worker RAM을 계속 점유하므로 작은 RAM 환경의 기본값으로 사용하지 않는다.
- `prefetch_factor`를 과도하게 높이지 않는다.
- CPU에서 큰 batch를 여러 개 미리 만들지 않는다.
- 불필요한 dataset cache를 삭제한다.
- 긴 문자열/토큰 배열을 Python object로 중복 보관하지 않는다.

권장 시작값:

```python
NUM_WORKERS = 0
PIN_MEMORY = DEVICE == "cuda"
PERSISTENT_WORKERS = False
```

데이터가 크면 `IterableDataset`, streaming, chunk 처리 또는 on-disk cache를 우선 검토한다.

## 21. CPU Usage Optimization

GPU가 작은 환경에서는 CPU 전처리가 병목이 될 수 있으므로 CPU를 활용하되 모든 core를 무조건 점유하지 않는다.

```python
import os

CPU_COUNT = os.cpu_count() or 1
CPU_WORKERS = min(2, CPU_COUNT)
```

실제 throughput을 측정한 후 worker 수를 증가시킨다.

Windows standalone script에서 multiprocessing을 사용할 경우:

```python
if __name__ == "__main__":
    main()
```

Notebook에서는 `num_workers=0`을 기본값으로 하여 spawn 관련 문제와 RAM 증가를 우선 방지한다.

## 22. GPU / RAM Monitoring

학습/추론 중 주기적으로 메모리를 확인한다.

```python
def gpu_memory_report():
    import torch

    if not torch.cuda.is_available():
        return

    allocated = torch.cuda.memory_allocated() / 1024**3
    reserved = torch.cuda.memory_reserved() / 1024**3
    free, total = torch.cuda.mem_get_info()
    free /= 1024**3
    total /= 1024**3

    print(
        f"GPU memory: allocated={allocated:.2f} GB, "
        f"reserved={reserved:.2f} GB, "
        f"free={free:.2f} GB, total={total:.2f} GB"
    )
```

RAM도 가능하면 `psutil.virtual_memory()`로 기록한다.

목표는 GPU utilization 100%가 아니라 **OOM 없이 안정적으로 학습/추론하는 것**이다.

## 23. OOM Prevention / Recovery

### CUDA OOM

다음 순서로 자원을 낮춘다.

1. batch size → 1
2. sequence length / input resolution 감소
3. `max_new_tokens` 감소
4. gradient accumulation 유지
5. FP16 AMP 활성화
6. gradient checkpointing 활성화
7. 8-bit/4-bit quantization 검토
8. optimizer/model CPU offload 검토
9. 더 작은 model/checkpoint 사용
10. 그래도 실패하면 4 GB VRAM 범위를 벗어나는 설정임을 명시적으로 보고

### System RAM 부족

1. DataLoader worker → 0
2. prefetch 감소
3. streaming/chunking 적용
4. batch size 감소
5. 중간 결과 cache/list 제거
6. 대형 DataFrame 복사 제거
7. disk-based dataset/cache 사용
8. dataset/model 규모 감소

`del`, `gc.collect()`, `torch.cuda.empty_cache()`는 보조적인 메모리 반환 수단일 뿐이며 모델/입력/optimizer 자체가 한도를 초과하는 문제를 해결하지 못한다.

## 24. Memory Smoke Test

실제 전체 학습 전에 작은 데이터와 짧은 step으로 메모리 검사를 수행한다.

권장 절차:

```text
1 batch
→ 1 forward
→ 1 backward
→ 1 optimizer step
→ memory report
→ 필요 시 configuration 축소
→ 짧은 multi-step test
→ full training
```

학습 설정을 한 번에 크게 잡지 않는다. 특히 4 GB VRAM에서는 첫 실행부터 full dataset/full sequence length로 시작하지 않는다.

## 25. Training Checkpoint / Resume

메모리 문제, Windows/Jupyter 종료 또는 장시간 학습 중단에 대비하여 checkpoint를 저장한다.

권장 구조:

```text
checkpoints/
├── latest/
├── best/
└── step-XXXX/
```

가능하면 model state, optimizer state, scheduler state, AMP scaler state, epoch/step, random state, training configuration, model/dataset revision을 저장한다.

checkpoint 저장 자체가 메모리를 폭증시키지 않도록 state를 순차적으로 디스크에 저장하고 불필요한 duplicate object를 만들지 않는다.

## 26. LLM 구조

```text
Configuration
    ↓
Resource Detection
    ↓
Prompt
    ↓
Data
    ↓
Model / API Client
    ↓
Inference / Training
    ↓
Evaluation
    ↓
Checkpoint
    ↓
Export
```

재사용 구현은 `src/`에 둔다.

## 27. Model Configuration

```python
MODEL_ID = "..."
TEMPERATURE = 0.2
MAX_NEW_TOKENS = 256
MAX_SEQ_LENGTH = 256
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
SEED = 42
```

magic number를 여러 cell에 분산하지 않는다.

## 28. Prompt 관리

```text
prompts/
├── system/
├── user/
└── evaluation/
```

재사용 prompt를 Notebook에 복사하지 않는다.

## 29. Secret 관리

금지:

```python
API_KEY = "sk-..."
```

권장:

```python
import os

API_KEY = os.getenv("OPENAI_API_KEY")
```

credential, token, private key, `.env`를 repository에 commit하지 않는다.

## 30. Reproducibility

```python
import random
import numpy as np

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

try:
    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
except ImportError:
    pass
```

실험 metadata에는 가능한 경우 Python version, OS, architecture, package versions, model ID/revision, dataset version, device, GPU/VRAM, RAM, batch size, gradient accumulation, sequence length, precision, quantization, gradient checkpointing, DataLoader worker 수, parameters, seed, prompt version, metrics를 기록한다.

## 31. Notebook Idempotency

cell을 여러 번 실행해도 예기치 않은 상태 누적이 없어야 한다.

```python
results = []
```

같은 결과에 반복적으로 append되는 hidden state를 피한다.

GPU tensor, model, optimizer, DataLoader 및 대형 dataset reference를 cell 실행마다 중복 생성하지 않는다.

## 32. Korean Matplotlib

OS별 한글 폰트를 고정하지 않는다.

```python
from matplotlib import font_manager


def find_korean_font():
    candidates = [
        "Malgun Gothic",
        "AppleGothic",
        "NanumGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR",
    ]

    installed = {
        font.name
        for font in font_manager.fontManager.ttflist
    }

    for candidate in candidates:
        if candidate in installed:
            return candidate

    return None
```

폰트가 없으면 warning을 표시하되 가능한 경우 전체 Notebook 실행을 중단시키지 않는다.

## 33. Error Handling

금지:

```python
try:
    ...
except:
    pass
```

명시적인 exception type과 actionable error message를 사용한다.

## 34. Code Quality

- PEP 8
- Ruff
- Black-compatible formatting
- type hints
- small functions
- explicit error handling
- reusable code in `src/`
- tests in `tests/`

## 35. Notebook 자동 생성 규칙

새 Notebook:

1. 목적 Markdown
2. Environment Detection
3. Hardware / Memory Detection
4. UTF-8
5. Project Root
6. Dependency Bootstrap
7. Resource Configuration
8. Imports
9. Configuration
10. Experiment

기존 Notebook:

- 사용자 코드를 삭제하지 않는다.
- bootstrap이 없으면 상단에 추가한다.
- `!pip install`은 active kernel 기준 설치로 정리한다.
- OS 고정 경로는 `Path`로 변경한다.
- encoding을 명시한다.
- `cuda` 하드코딩을 device detection으로 바꾼다.
- 중복 reusable code는 `src/` 분리를 검토한다.
- batch/sequence length/worker 수가 하드웨어에 맞는지 확인한다.
- 학습 전에 memory smoke test를 추가한다.

## 36. Validation Workflow

수정 후 가능하면:

1. Kernel/Runtime restart
2. Run All
3. dependency 확인
4. environment 확인
5. GPU/RAM 확인
6. UTF-8/한글 확인
7. memory smoke test
8. model inference 확인
9. visualization 확인
10. output 확인
11. relevant tests 실행
12. checkpoint/resume 확인

## 37. 완료 체크리스트

```text
Environment
[ ] OS
[ ] architecture
[ ] Python version
[ ] sys.executable
[ ] Jupyter
[ ] Colab
[ ] CPU
[ ] GPU
[ ] VRAM
[ ] System RAM

Dependencies
[ ] package detection
[ ] missing package installation
[ ] active kernel installation
[ ] version requirements

Hardware Optimization
[ ] RTX 3050 Ti 4 GB profile considered
[ ] RAM 16 GB profile considered
[ ] conservative VRAM budget
[ ] batch size starts at 1 when needed
[ ] gradient accumulation
[ ] sequence length limit
[ ] FP16/AMP review
[ ] gradient checkpointing review
[ ] quantization review
[ ] CPU offload review
[ ] DataLoader worker limit
[ ] prefetch limit
[ ] RAM cache limit
[ ] GPU/RAM monitoring
[ ] memory smoke test
[ ] OOM recovery strategy
[ ] checkpoint/resume

Compatibility
[ ] Windows
[ ] Linux
[ ] macOS
[ ] Jupyter
[ ] Colab
[ ] Colab Local Runtime

Encoding
[ ] UTF-8
[ ] Korean console
[ ] Korean files
[ ] Korean CSV
[ ] Korean visualization

Security
[ ] no hard-coded API keys
[ ] no credentials committed

Notebook
[ ] bootstrap cells
[ ] top-to-bottom execution
[ ] idempotency
[ ] no hidden state

Code Quality
[ ] PEP 8
[ ] type hints
[ ] error handling
[ ] reusable code in src
[ ] tests
[ ] reproducibility metadata
```

## 38. Definition of Done

- local Jupyter에서 동작
- VS Code Jupyter에서 동작
- Google Colab에서 동작
- Windows/Linux/macOS 고려
- active Python kernel 감지
- missing dependency를 해당 kernel에 설치
- UTF-8/Korean 보존
- cross-platform path 사용
- CPU/CUDA/MPS 자동 감지
- 실제 GPU VRAM/RAM 확인
- 4 GB VRAM 환경에서 보수적인 기본값 사용
- 16 GB RAM 환경에서 dataset/cache/worker 사용량 제한
- FP16/gradient accumulation/checkpointing/quantization을 필요에 따라 적용
- GPU/RAM memory smoke test 통과
- OOM 발생 시 완화 가능한 configuration 보유
- 장시간 학습은 checkpoint/resume 지원
- secret 보호
- fresh kernel/runtime에서 Run All 가능
- reusable code와 Notebook orchestration 분리
- 재현성 정보 기록
