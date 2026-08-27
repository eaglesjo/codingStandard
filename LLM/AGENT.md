# AGENT.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development

## 1. 목적

이 문서는 Python 기반 LLM/ML 프로젝트를 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 개발하는 AI Agent를 위한 공통 개발 규칙이다.

지원 환경:

- Windows
- Linux
- macOS
- venv / virtualenv / conda / uv
- Jupyter Notebook / JupyterLab
- VS Code Jupyter
- Google Colab
- Google Colab Local Runtime
- 로컬 저사양 GPU 개발 환경

핵심 목표:

- OS 독립성
- Jupyter/Colab 호환성
- 활성 Python kernel 기준 패키지 설치
- UTF-8 및 한글 안전성
- CPU/CUDA/MPS 자동 감지
- 제한된 GPU/CPU 메모리에서도 안정적인 학습/추론
- GPU VRAM과 시스템 RAM의 사용량을 명시적으로 관리
- 메모리 부족(OOM)으로 학습이 중단되는 상황을 최대한 예방하고 자동 완화
- 재현 가능한 실험
- Secret 안전 관리
- Notebook과 재사용 코드의 분리

## 2. 기본 원칙

1. Python을 기본 언어로 사용한다.
2. Python 3.11+를 권장한다.
3. 재사용 가능한 로직은 `src/`에 둔다.
4. Notebook은 실험, 탐색, 시각화, 평가, 문서화에 사용한다.
5. OS별 경로를 하드코딩하지 않는다.
6. 파일 인코딩은 UTF-8을 명시한다.
7. API key, token, password를 코드에 넣지 않는다.
8. GPU나 특정 패키지가 설치되어 있다고 가정하지 않는다.
9. 새 Notebook에는 환경 Bootstrap 셀을 상단에 둔다.
10. 새 Kernel/Runtime에서 처음부터 끝까지 실행 가능해야 한다.
11. 로컬 학습에서는 가용 VRAM/RAM을 확인한 후 batch size, sequence length, worker 수 등의 자원 사용량을 결정한다.
12. 메모리 여유를 남겨두며, GPU/RAM을 100%까지 채우는 것을 목표로 하지 않는다.
13. OOM을 단순히 `torch.cuda.empty_cache()`로 해결하려 하지 말고 입력 크기, batch, activation, optimizer state 및 DataLoader 메모리부터 줄인다.

## 3. 기준 로컬 개발 환경

이 저장소의 로컬 LLM/ML 개발 기본 프로파일은 다음 하드웨어를 기준으로 한다.

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM: 4 GB
System RAM: 16 GB
```

이 환경은 **4 GB VRAM이 가장 중요한 제약 조건**이다. Agent는 이 환경에서 실행 가능한 보수적인 기본값을 우선 제안하고, 더 큰 GPU/메모리가 감지된 경우에만 자원 사용량을 단계적으로 늘린다.

권장 자원 예산:

- GPU VRAM: 모델/학습에 전체 4 GB를 모두 사용하지 않는다. 가능하면 약 3.0~3.5 GB 이하를 실사용 목표로 잡고 0.5~1.0 GB 정도의 여유를 둔다.
- System RAM: Windows와 VS Code/Jupyter/백그라운드 프로세스가 사용할 공간을 남긴다. 16 GB 전체를 Dataset/DataLoader cache에 할당하지 않는다.
- CPU: GPU가 작은 경우 CPU가 데이터 전처리/토크나이징/디스크 I/O를 담당하되, CPU worker를 과도하게 늘려 RAM을 소모하지 않는다.

위 숫자는 절대적인 안전 한도가 아니라 시작점이다. 실제 모델, CUDA/PyTorch 버전, Windows 상태, 백그라운드 프로그램 및 데이터 크기에 따라 조정한다.

## 4. Notebook 표준 구조

권장 순서:

1. 목적 Markdown
2. 환경 감지
3. 하드웨어/메모리 감지
4. UTF-8 설정
5. 프로젝트 루트 감지
6. 의존성 확인/설치
7. imports
8. resource configuration
9. configuration
10. data
11. model/client
12. experiment
13. evaluation
14. visualization
15. export
16. reproducibility metadata

재사용 가능한 함수와 클래스를 Notebook에 중복 작성하지 않는다.

## 5. 환경 자동 감지

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

for key, value in ENV.items():
    print(f"{key}: {value}")
```

`/content`, `/home`, `/Users`, `C:\\Users` 같은 경로만으로 환경을 판별하지 않는다.

## 6. 활성 Kernel 기준 패키지 설치

Notebook에서 `!pip install`을 무조건 사용하지 않는다. 현재 실행 중인 Python kernel의 `sys.executable -m pip`를 사용한다.

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

사용 예:

```python
ensure_package("numpy")
ensure_package("pandas")
ensure_package("transformers")
ensure_package("sklearn", "scikit-learn")
```

무조건 재설치하지 않는다. 프로젝트의 `pyproject.toml`, `requirements.txt`, lock file을 canonical dependency source로 사용한다.

## 7. 프로젝트 루트 자동 감지

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

## 8. Cross-platform Path

항상 `pathlib.Path`를 우선 사용한다.

```python
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

다음과 같은 경로를 하드코딩하지 않는다.

```text
C:\\project\\data
/home/user/project/data
/Users/name/project/data
```

## 9. Windows / Linux / macOS

### Windows

`rm`, `cp`, `mv`, `grep`, `sed`, `awk` 등 Unix 전용 명령에 의존하지 않는다.

Windows의 Python multiprocessing/DataLoader 사용 시 worker를 늘리기 전에 안정성을 확인한다. Notebook에서는 특히 `num_workers=0` 또는 `1`부터 시작하고, 안정성이 확인된 경우에만 증가시킨다.

### Linux

특정 배포판, 사용자 home, shell 또는 GPU가 있다고 가정하지 않는다.

### macOS

Intel과 Apple Silicon을 가정하지 않고 `platform.machine()`으로 architecture를 확인한다.

가능하면 OS별 분기 대신 Python 표준 API를 사용한다.

## 10. subprocess

가능하면 Python 표준 라이브러리를 사용한다.

```python
import subprocess

subprocess.run(command, check=True)
```

가능하면 `shell=True`를 사용하지 않는다.

## 11. Google Colab

```python
IS_COLAB = "google.colab" in sys.modules
WORKSPACE = Path("/content") if IS_COLAB else ROOT
```

Colab runtime filesystem이 영구 저장소라고 가정하지 않는다. 중요한 결과물은 Drive 또는 다른 영구 저장 위치에 저장한다.

필요할 때만 Google Drive를 mount한다.

```python
def mount_google_drive():
    if not IS_COLAB:
        return False

    from google.colab import drive
    drive.mount("/content/drive")
    return True
```

Colab Local Runtime은 로컬 컴퓨터의 파일과 프로세스에 접근할 수 있으므로 신뢰할 수 있는 코드만 실행한다.

## 12. CPU / CUDA / MPS 자동 감지

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

모델 코드에 `cuda`를 하드코딩하지 않는다.

## 13. 로컬 GPU/RAM 자원 프로파일링

RTX 3050 Ti 4 GB 환경에서는 학습 시작 전에 실제 VRAM/RAM을 확인한다.

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

`nvidia-smi`가 설치되어 있다고 가정하지 않는다. 가능하면 PyTorch API로 확인한다.

## 14. GPU 메모리 최적화 원칙

4 GB VRAM을 기준으로 다음 순서를 우선 적용한다.

1. `batch_size=1`부터 시작한다.
2. 필요한 경우 `gradient_accumulation_steps`로 effective batch size를 확보한다.
3. `max_seq_length` / `block_size` / image resolution 등 입력 크기를 먼저 줄인다.
4. CUDA에서 가능한 경우 FP16 mixed precision을 사용한다.
5. 학습 시 activation memory가 큰 모델은 gradient checkpointing을 검토한다.
6. Hugging Face/Transformers 모델은 가능한 경우 8-bit 또는 4-bit quantization을 검토한다.
7. optimizer state가 VRAM을 과도하게 사용하면 메모리 효율적인 optimizer 또는 CPU offload를 검토한다.
8. 추론만 할 때는 `model.eval()`과 `torch.inference_mode()`를 사용한다.
9. 필요 없는 tensor reference를 유지하지 않는다.
10. 큰 중간 결과를 Python list에 무한정 누적하지 않는다.
11. 매 step마다 `torch.cuda.empty_cache()`를 호출하지 않는다. 이는 근본적인 메모리 절약 방법이 아니다.
12. CUDA OOM 발생 시 같은 설정으로 무한 재시도하지 않고 resource profile을 낮춘다.

권장 시작 configuration 예:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
USE_FP16 = True
GRADIENT_CHECKPOINTING = True
```

위 값은 모델에 따라 조정한다. 작은 모델에서도 무조건 checkpointing/quantization을 강제하지 않고 실제 메모리 사용량을 확인한다.

## 15. Mixed Precision 규칙

CUDA 학습에서는 FP32 전체 학습보다 mixed precision을 우선 검토한다.

```python
import torch

USE_AMP = DEVICE == "cuda"
AMP_DTYPE = torch.float16
```

예:

```python
with torch.autocast(
    device_type="cuda",
    dtype=torch.float16,
    enabled=USE_AMP,
):
    loss = model(**batch).loss
```

RTX 3050 Ti 4 GB 환경에서는 FP16을 기본 후보로 사용하고, BF16은 실제 GPU/PyTorch 지원 여부를 확인한 후 사용한다. AMP 사용으로 수치 불안정성이 발생하면 해당 연산만 FP32로 처리하거나 AMP를 부분적으로 비활성화한다.

## 16. Gradient Accumulation

작은 VRAM에서는 batch size를 올리는 대신 gradient accumulation을 사용한다.

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8

loss = loss / GRADIENT_ACCUMULATION_STEPS
loss.backward()

if (step + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

effective batch size는 다음처럼 계산한다.

```text
effective_batch_size = batch_size × gradient_accumulation_steps × world_size
```

단일 RTX 3050 Ti에서는 일반적으로 `world_size=1`이다.

## 17. Gradient Checkpointing

모델 activation이 VRAM을 많이 차지하는 경우 gradient checkpointing을 사용한다.

```python
if hasattr(model, "gradient_checkpointing_enable"):
    model.gradient_checkpointing_enable()
```

gradient checkpointing은 계산량을 증가시키므로 VRAM 부족이 실제 병목일 때 우선 적용한다.

## 18. Inference 메모리 규칙

추론에는 training graph를 만들지 않는다.

```python
model.eval()

with torch.inference_mode():
    outputs = model(**inputs)
```

Hugging Face generate에서도 `max_new_tokens`를 무제한으로 두지 않는다.

```python
MAX_NEW_TOKENS = 256
```

4 GB VRAM에서는 입력 길이와 `max_new_tokens`가 동시에 커지지 않도록 관리한다.

## 19. CPU / System RAM 최적화

16 GB RAM 환경에서는 RAM을 GPU VRAM의 대체 공간처럼 무제한 사용하는 설계를 금지한다.

규칙:

- 전체 dataset을 RAM에 무조건 로드하지 않는다.
- 가능하면 streaming, chunking, memory mapping을 사용한다.
- pandas에서 대용량 데이터를 한 번에 복제하지 않는다.
- `list(df.itertuples())` 같은 대규모 복사 패턴을 피한다.
- DataLoader `num_workers`는 0 또는 1부터 시작한다.
- worker 수를 증가시킬 때 RAM 사용량과 Windows 안정성을 확인한다.
- `pin_memory=True`는 CUDA DataLoader에서 CPU→GPU 전송 병목이 있을 때만 사용하고 RAM 여유를 확인한다.
- `persistent_workers=True`는 worker RAM을 계속 점유하므로 작은 RAM 환경에서 기본값으로 사용하지 않는다.
- DataLoader `prefetch_factor`를 과도하게 높이지 않는다.
- CPU에서 생성한 큰 batch를 여러 개 미리 쌓지 않는다.
- 불필요한 dataset cache를 삭제한다.
- 긴 문자열/토큰 배열을 Python object로 중복 보관하지 않는다.

권장 시작값:

```python
NUM_WORKERS = 0  # Windows/Notebook 안정성 우선
PIN_MEMORY = DEVICE == "cuda"
PERSISTENT_WORKERS = False
```

데이터가 크면 `IterableDataset`, streaming, chunk 단위 처리 또는 on-disk cache를 우선 검토한다.

## 20. CPU 사용 최적화

GPU가 작은 환경에서는 CPU 전처리가 병목이 될 수 있으므로 CPU를 사용하되 무조건 모든 CPU core를 사용하지 않는다.

```python
import os

CPU_COUNT = os.cpu_count() or 1
CPU_WORKERS = min(2, CPU_COUNT)
```

토크나이징/전처리에서는 작은 worker 수로 시작하고 실제 throughput을 측정한 뒤 증가시킨다.

Windows에서는 multiprocessing을 사용하는 standalone Python script에 다음 보호를 적용한다.

```python
if __name__ == "__main__":
    main()
```

Notebook에서는 `num_workers=0`을 기본값으로 하여 spawn 관련 문제를 우선 피한다.

## 21. 메모리 모니터링

학습/추론 중 주기적으로 자원 사용량을 확인한다.

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

필요하면 `psutil.virtual_memory()`로 RAM도 기록한다.

목표는 단순히 GPU utilization 100%가 아니라 **OOM 없이 안정적인 throughput**이다.

## 22. OOM 방지 및 자동 완화 전략

CUDA OOM 또는 RAM 부족이 발생하면 다음 순서로 자원을 줄인다.

### GPU OOM

1. batch size를 1로 낮춘다.
2. sequence length / input resolution을 줄인다.
3. `max_new_tokens`를 줄인다.
4. gradient accumulation은 유지하여 effective batch size를 보존한다.
5. FP16 AMP를 활성화한다.
6. gradient checkpointing을 활성화한다.
7. model quantization(8-bit/4-bit)을 검토한다.
8. optimizer state/activation을 CPU로 offload하는 방법을 검토한다.
9. 더 작은 model/checkpoint를 사용한다.
10. 그래도 실패하면 해당 학습 설정이 4 GB VRAM 범위를 벗어났음을 명시적으로 보고한다.

### RAM 부족

1. DataLoader worker를 0으로 낮춘다.
2. prefetch를 줄인다.
3. dataset을 streaming/chunking으로 변경한다.
4. batch size를 낮춘다.
5. 중간 결과 cache/list를 비운다.
6. 대형 DataFrame 복사본을 제거한다.
7. 필요하면 dataset을 디스크 기반 format으로 변경한다.
8. 그래도 부족하면 dataset/model 규모를 줄인다.

**중요:** `del` + `gc.collect()` + `torch.cuda.empty_cache()`는 이미 참조가 해제된 메모리를 반환하는 보조 수단일 뿐이다. 입력/모델/optimizer 자체가 VRAM/RAM 한도를 초과하는 문제를 해결하지 못한다.

## 23. 학습 재시작 가능성

메모리 문제나 Windows/Notebook 종료로 학습이 중단되어도 처음부터 다시 학습하지 않도록 checkpoint를 저장한다.

권장:

```text
checkpoints/
├── latest/
├── best/
└── step-XXXX/
```

checkpoint에는 가능한 경우 다음을 포함한다.

- model state
- optimizer state
- scheduler state
- scaler state
- epoch/step
- random seed/state
- training configuration
- dataset/model revision

단, 16 GB RAM/4 GB VRAM 환경에서 checkpoint 저장 때문에 메모리가 급증하지 않도록 state를 CPU/디스크로 순차 저장한다.

## 24. LLM 코드 구조

다음 요소를 분리한다.

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

## 25. Prompt 관리

긴 prompt를 Notebook 여러 곳에 복사하지 않는다.

권장 구조:

```text
prompts/
├── system/
├── user/
└── evaluation/
```

## 26. Secret 관리

금지:

```python
API_KEY = "sk-..."
```

권장:

```python
import os

API_KEY = os.getenv("OPENAI_API_KEY")
```

`.env`, token, credential, private key 파일을 Git에 commit하지 않는다.

## 27. 재현성

가능하면 seed를 설정한다.

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

가능하면 다음 metadata를 저장한다.

- Python version
- OS / architecture
- package versions
- model ID/revision
- dataset version
- device
- GPU name / VRAM
- system RAM
- batch size
- gradient accumulation
- sequence length
- precision
- quantization
- gradient checkpointing
- DataLoader worker 수
- device
- parameters
- seed
- prompt version
- metrics

## 28. Python Coding Standard

준수:

- PEP 8
- Ruff
- Black-compatible formatting
- type hints
- 의미 있는 변수명
- 작은 함수
- 명시적인 error handling

금지:

```python
try:
    ...
except:
    pass
```

bare `except`를 사용하지 않는다.

## 29. Notebook Idempotency

Notebook은 cell을 반복 실행해도 상태가 예기치 않게 누적되지 않아야 한다.

Kernel/Runtime 재시작 후 Run All이 가능해야 한다.

특히 GPU tensor, model, optimizer, DataLoader 및 대형 dataset reference를 cell 실행마다 중복 생성하지 않는다.

## 30. 테스트

재사용 가능한 `src/` 코드에는 `tests/`를 작성한다.

최소 검증:

- imports
- environment bootstrap
- UTF-8
- paths
- device detection
- resource detection
- 핵심 inference/evaluation
- 작은 synthetic dataset을 이용한 training smoke test

학습 코드에는 가능하면 실제 dataset 전체를 사용하기 전에 작은 batch/짧은 step으로 memory smoke test를 수행한다.

## 31. Agent 작업 순서

1. repository 구조 확인
2. `pyproject.toml` / requirements / lock file 확인
3. Notebook 구조 확인
4. Python kernel 확인
5. OS/runtime 확인
6. CPU/GPU/RAM/VRAM 확인
7. dependency 확인
8. reusable code를 `src/`로 분리
9. bootstrap cell 추가/수정
10. resource configuration 설정
11. UTF-8 및 cross-platform 문제 확인
12. 작은 데이터/짧은 step으로 memory smoke test
13. 필요 시 batch/sequence length/precision/worker를 단계적으로 조정
14. 테스트
15. clean kernel에서 Notebook 실행
16. 가능하면 checkpoint/resume 확인
17. 변경 사항 보고

## 32. 완료 조건

```text
[ ] OS 감지
[ ] architecture 감지
[ ] Python version 감지
[ ] sys.executable 확인
[ ] Jupyter 감지
[ ] Colab 감지
[ ] CPU 확인
[ ] GPU 확인
[ ] VRAM 확인
[ ] System RAM 확인
[ ] dependency 확인
[ ] 없는 package만 설치
[ ] active kernel 기준 설치
[ ] UTF-8 설정
[ ] 한글 출력 테스트
[ ] 한글 matplotlib 처리
[ ] project root 감지
[ ] cross-platform path
[ ] CPU/CUDA/MPS 감지
[ ] batch size가 자원에 맞음
[ ] sequence length가 자원에 맞음
[ ] mixed precision 검토
[ ] gradient accumulation 검토
[ ] gradient checkpointing 검토
[ ] quantization/offload 검토
[ ] DataLoader worker 제한
[ ] RAM cache 제한
[ ] GPU/RAM memory smoke test
[ ] OOM 완화 전략 존재
[ ] checkpoint/resume 가능
[ ] secret 미노출
[ ] notebook top-to-bottom 실행
[ ] hidden state 없음
[ ] reusable code가 src에 있음
[ ] 테스트 실행
[ ] 재현성 metadata 기록
```
