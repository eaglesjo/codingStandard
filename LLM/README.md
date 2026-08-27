# LLM Coding Standard

Python 기반 LLM 개발을 위한 `AGENT.md`와 `SKILL.md` 사용 가이드입니다.

이 폴더의 규칙은 **Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, Colab Local Runtime**을 하나의 개발 표준으로 묶고, **Windows / Linux / macOS**에서 동일한 Python 코드가 최대한 그대로 실행되도록 만드는 것을 목표로 합니다.

---

## 1. 구성

```text
LLM/
├── AGENT.md
├── SKILL.md
└── README.md
```

### AGENT.md

AI Agent 또는 코딩 Agent가 프로젝트를 수정할 때 따라야 하는 **상위 개발 규칙**입니다.

다음 내용을 정의합니다.

- Python 코딩 표준
- 프로젝트 구조
- Notebook 구조
- OS 호환성
- Jupyter / Colab 호환성
- dependency 관리
- UTF-8 / 한글 처리
- GPU 자동 감지
- Secret 관리
- 테스트
- 재현성
- Agent 작업 순서
- 완료 조건
- 로컬 GPU / RAM 자원 최적화
- OOM 예방 및 복구

### SKILL.md

LLM/Jupyter 관련 작업을 수행할 때 Agent가 실제로 적용하는 **작업 절차와 실행 패턴**입니다.

다음과 같은 상황에서 사용합니다.

- Notebook 신규 생성
- 기존 Notebook 수정
- Colab notebook 작성
- LLM inference
- Hugging Face / Transformers
- PyTorch
- embedding / RAG
- evaluation
- ML experiment
- 제한된 VRAM/RAM 환경의 학습

---

# 2. 설치

## 2.1 저장소 전체를 사용하는 경우

이 repository를 clone합니다.

```bash
git clone https://github.com/eaglesjo/codingStandard.git
cd codingStandard
```

이후 `LLM/` 디렉터리를 프로젝트의 Agent 규칙 위치에 복사하거나 링크합니다.

---

## 2.2 일반 Python 프로젝트에 적용

예를 들어 다음과 같은 프로젝트가 있다고 가정합니다.

```text
my-llm-project/
├── src/
├── notebooks/
├── tests/
├── pyproject.toml
└── README.md
```

`LLM/`의 두 파일을 프로젝트의 Agent 규칙 디렉터리에 배치합니다.

```text
my-llm-project/
├── AGENT.md
├── SKILL.md
├── src/
├── notebooks/
├── tests/
└── pyproject.toml
```

또는 프로젝트에서 별도 coding rule directory를 사용한다면:

```text
my-llm-project/
├── codingRules/
│   └── LLM/
│       ├── AGENT.md
│       └── SKILL.md
├── src/
└── notebooks/
```

프로젝트의 기존 Agent 규칙이 있다면 기존 규칙을 덮어쓰기보다 우선순위와 충돌 여부를 확인합니다.

---

# 3. AGENT.md 사용법

`AGENT.md`는 Agent가 Python/LLM 코드를 만들거나 수정하기 전에 읽는 기준 문서입니다.

Agent에게 다음과 같이 지시할 수 있습니다.

```text
이 프로젝트의 LLM 개발은 codingStandard/LLM/AGENT.md 규칙을 준수해.
Notebook은 Jupyter와 Google Colab에서 모두 실행 가능해야 하고,
Windows/Linux/macOS 호환성을 유지해.
```

핵심은 Agent가 코드를 작성하기 전에 다음을 확인하게 하는 것입니다.

```text
OS
 ↓
Python
 ↓
Jupyter / Colab
 ↓
Active Kernel
 ↓
Dependencies
 ↓
UTF-8
 ↓
Device
 ↓
Hardware / Memory
 ↓
Application Code
```

---

# 4. SKILL.md 사용법

`SKILL.md`는 LLM/Jupyter 개발 작업을 수행할 때 적용합니다.

예를 들어 Agent에게:

```text
SKILL.md의 Jupyter/Colab 개발 절차를 적용해서
새 LLM 실험 Notebook을 만들어 줘.
```

라고 요청하면 다음과 같은 Bootstrap 구조를 먼저 구성하는 것을 원칙으로 합니다.

```text
Cell 0  : 목적 / 설명
Cell 1  : Environment Detection
Cell 2  : Hardware / Memory Detection
Cell 3  : UTF-8 Configuration
Cell 4  : Project Root Detection
Cell 5  : Dependency Bootstrap
Cell 6  : Imports
Cell 7  : Resource Configuration
Cell 8  : Configuration
Cell 9+ : Experiment
```

---

# 5. Notebook Bootstrap

모든 환경 의존적인 Notebook은 가능한 한 상단에서 실행 환경을 확인합니다.

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

이렇게 하면 다음을 확인할 수 있습니다.

- 실제 Python 버전
- 실제 실행 중인 Python executable
- 운영체제
- CPU architecture
- 현재 working directory
- Jupyter 여부
- Colab 여부

특히 패키지 설치에서는 `sys.executable`이 중요합니다.

---

# 6. 패키지 자동 설치

Notebook에서 일반적인:

```python
!pip install transformers
```

보다 다음 패턴을 권장합니다.

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

사용:

```python
ensure_package("numpy")
ensure_package("pandas")
ensure_package("transformers")
```

import 이름과 PyPI package 이름이 다른 경우:

```python
ensure_package(
    "sklearn",
    "scikit-learn",
)
```

## 중요한 점

이 함수는 **없는 패키지만 설치**합니다.

이미 설치된 패키지를 매번 다시 설치하지 않습니다.

또한 현재 Notebook kernel이 사용하는 Python에 설치하기 때문에 다음과 같은 문제가 줄어듭니다.

```text
Terminal Python
        ≠
Jupyter Kernel Python
```

단, 프로젝트의 정식 dependency 관리는 반드시 `pyproject.toml`, `requirements.txt`, lock file 등을 기준으로 합니다. `ensure_package()`는 Notebook의 bootstrap/개발 편의 기능입니다.

---

# 7. Windows / Linux / macOS

이 표준은 세 운영체제를 모두 고려합니다.

## Windows

Unix shell command에 의존하지 않습니다.

피해야 할 예:

```text
rm
cp
mv
grep
sed
awk
```

파일과 디렉터리 조작에는 Python 표준 라이브러리를 우선 사용합니다.

Windows의 Python multiprocessing/DataLoader 사용 시 worker를 늘리기 전에 안정성을 확인합니다. Notebook에서는 특히 `num_workers=0` 또는 `1`부터 시작하고, 안정성이 확인된 경우에만 증가시킵니다.

## Linux

특정 사용자 home directory나 Linux distribution을 가정하지 않습니다.

## macOS

Intel Mac과 Apple Silicon Mac을 가정하지 않습니다.

```python
import platform

print(platform.machine())
```

으로 architecture를 확인합니다.

---

# 8. Cross-platform Path

다음과 같은 경로는 사용하지 않습니다.

```python
"C:\\Users\\name\\project\\data"
"/home/name/project/data"
"/Users/name/project/data"
```

대신:

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
```

를 사용합니다.

---

# 9. 한글 / UTF-8

한국어 데이터, 파일명, prompt, 결과물, CSV, JSON 등을 안전하게 처리하기 위해 encoding을 명시합니다.

```python
text = Path(path).read_text(
    encoding="utf-8"
)
```

```python
Path(path).write_text(
    text,
    encoding="utf-8"
)
```

JSON:

```python
import json

with open(
    path,
    "r",
    encoding="utf-8",
) as f:
    data = json.load(f)
```

CSV:

```python
import pandas as pd

df = pd.read_csv(
    path,
    encoding="utf-8",
)
```

Windows/Excel 호환 때문에 BOM이 필요한 경우에만 `utf-8-sig`를 사용합니다.

---

# 10. 한글 Matplotlib

Windows에서는 `Malgun Gothic`, macOS에서는 `AppleGothic`, Linux/Colab에서는 `Noto Sans CJK KR` 또는 `NanumGothic` 등이 설치되어 있을 수 있습니다.

따라서 하나의 폰트만 고정하지 않고 설치된 폰트를 검색합니다.

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

폰트가 없더라도 전체 프로그램을 무조건 중단시키지 않고 warning을 표시하도록 설계합니다.

---

# 11. CPU / CUDA / MPS

LLM/ML 코드는 GPU가 있다고 가정하지 않습니다.

권장 우선순위:

```text
CUDA
  ↓
MPS
  ↓
CPU
```

예:

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

따라서 다음과 같은 코드는 피합니다.

```python
model.to("cuda")
```

대신:

```python
model.to(DEVICE)
```

처럼 환경을 반영합니다.

---

# 12. 로컬 개발 하드웨어 프로파일

로컬 Windows + VS Code 개발 환경에서는 다음 하드웨어를 기본 프로파일로 사용합니다.

```text
OS          : Windows
IDE         : VS Code + VS Code Jupyter
GPU         : NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM    : 4 GB
System RAM  : 16 GB
```

이 환경에서는 **4 GB VRAM이 가장 중요한 제약 조건**입니다. 따라서 Agent는 더 큰 장비가 확인되기 전까지 보수적인 설정을 우선 적용합니다.

### 권장 자원 예산

```text
GPU VRAM
  ├─ 전체 4 GB를 목표로 사용하지 않음
  ├─ 시작 목표: 약 3.0~3.5 GB 이하
  └─ 약 0.5~1.0 GB 여유 확보

System RAM
  ├─ Windows / VS Code / Jupyter를 위한 공간 확보
  ├─ Dataset 전체 cache를 메모리에 올리지 않음
  └─ DataLoader worker를 필요 이상으로 늘리지 않음
```

위 숫자는 절대적인 안전 한도가 아니라 시작점입니다. 실제 모델, CUDA/PyTorch 버전, 드라이버, 백그라운드 프로세스와 데이터 크기에 따라 실제 사용량을 측정한 후 조정합니다.

---

# 13. GPU / RAM 자원 확인

학습이나 대형 inference를 시작하기 전에 실제 가용 자원을 확인합니다.

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

`nvidia-smi`가 설치되어 있다고 가정하지 않습니다. 가능하면 PyTorch API로 확인합니다.

---

# 14. 4 GB VRAM 학습 최적화 규칙

4 GB VRAM 환경에서는 다음 순서로 메모리를 줄이는 것을 기본 전략으로 합니다.

```text
1. Batch Size 감소
        ↓
2. Sequence Length / Input Size 감소
        ↓
3. FP16 Mixed Precision
        ↓
4. Gradient Accumulation
        ↓
5. Gradient Checkpointing
        ↓
6. 8-bit / 4-bit Quantization 검토
        ↓
7. CPU Offload 검토
        ↓
8. Dataset / DataLoader 메모리 최적화
```

권장 시작값:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
USE_FP16 = True
GRADIENT_CHECKPOINTING = True
```

위 값은 모델에 따라 조정합니다. 작은 모델에서 무조건 모든 최적화를 강제하지 않고 실제 VRAM 사용량을 확인합니다.

### 특히 피해야 하는 패턴

```text
배치 크기를 먼저 크게 설정
긴 sequence length를 그대로 사용
FP32 전체 학습 고정
DataLoader worker 과다 사용
Dataset 전체를 RAM에 복제
불필요한 intermediate tensor 저장
매 step마다 empty_cache() 호출
OOM 후 같은 설정으로 무한 재시도
```

---

# 15. Mixed Precision

CUDA 학습에서는 FP32 전체 학습보다 mixed precision을 우선 검토합니다.

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

RTX 3050 Ti 4 GB 환경에서는 FP16을 기본 후보로 사용합니다. BF16은 실제 GPU/PyTorch 지원 여부를 확인한 후 선택합니다.

AMP 사용으로 수치 불안정성이 발생하면 해당 연산만 FP32로 처리하거나 AMP를 부분적으로 비활성화합니다.

---

# 16. Gradient Accumulation

작은 VRAM에서는 batch size를 올리는 대신 gradient accumulation으로 effective batch size를 확보합니다.

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
effective_batch_size = batch_size × gradient_accumulation_steps
```

---

# 17. Gradient Checkpointing

Activation memory가 큰 모델은 gradient checkpointing을 검토합니다.

```python
if hasattr(model, "gradient_checkpointing_enable"):
    model.gradient_checkpointing_enable()
```

메모리를 줄이는 대신 계산량이 증가할 수 있으므로 학습 속도와 메모리를 함께 측정합니다.

---

# 18. DataLoader / CPU / RAM 최적화

System RAM 16 GB 환경에서는 DataLoader가 RAM을 과도하게 사용하지 않도록 합니다.

권장 시작점:

```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=1,
    num_workers=0,
    pin_memory=True,
    persistent_workers=False,
)
```

GPU를 사용하는 경우 `pin_memory=True`를 검토하되 실제 성능 향상과 RAM 사용량을 함께 확인합니다.

Windows Notebook에서는 `num_workers=0` 또는 `1`부터 시작합니다. 안정성과 RAM 사용량을 확인한 후 증가시킵니다.

Dataset 전체를 `list`, `DataFrame`, tensor 등으로 중복 복사하지 말고 가능한 경우 streaming, lazy loading, chunking을 사용합니다.

---

# 19. 추론 메모리 최적화

학습이 아닌 inference에서는 gradient 계산을 비활성화합니다.

```python
model.eval()

with torch.inference_mode():
    outputs = model(**batch)
```

큰 결과를 모두 RAM에 쌓지 말고 가능한 경우 즉시 파일이나 chunk 단위 결과물로 저장합니다.

---

# 20. `torch.cuda.empty_cache()` 사용 원칙

`torch.cuda.empty_cache()`는 메모리 최적화의 1차 해결책으로 사용하지 않습니다.

나쁜 예:

```python
for batch in loader:
    ...
    torch.cuda.empty_cache()
```

먼저 다음을 줄입니다.

```text
batch size
sequence length
model size
activation memory
optimizer state
temporary tensor/reference
```

`empty_cache()`는 실제로 더 이상 사용하지 않는 CUDA allocator cache를 반환해야 하는 제한적인 상황에서만 사용합니다.

---

# 21. OOM 예방 및 복구

학습 시작 전에 작은 subset으로 Memory Smoke Test를 수행합니다.

```text
1 batch
  ↓
forward
  ↓
loss
  ↓
backward
  ↓
optimizer step
  ↓
VRAM / RAM 확인
```

CUDA OOM이 발생하면 같은 설정으로 무한 재시도하지 않습니다.

권장 완화 순서:

```text
OOM
 ↓
BATCH_SIZE × 0.5
 ↓
MAX_SEQ_LENGTH 감소
 ↓
FP16 확인
 ↓
Gradient Checkpointing
 ↓
Quantization / Offload 검토
 ↓
더 작은 model 또는 input 사용
```

RAM 부족 시:

```text
RAM 부족
 ↓
DataLoader num_workers 감소
 ↓
prefetch / persistent workers 감소
 ↓
Dataset cache 제거
 ↓
streaming / chunking
 ↓
불필요한 DataFrame / tensor 복사 제거
```

메모리 부족을 감지한 경우 사용자에게 원인과 변경한 설정을 명시하고, 조용히 품질이나 데이터 크기를 변경하지 않습니다.

---

# 22. Checkpoint / Resume

장시간 학습은 중단될 수 있다는 전제로 설계합니다.

권장 checkpoint 정보:

```text
model state
optimizer state
scheduler state
scaler state
current epoch / step
best metric
training configuration
random seed
model / dataset revision
```

가능하면 일정 step마다 checkpoint를 저장하고 `resume_from_checkpoint` 또는 동등한 방식으로 이어서 학습할 수 있도록 합니다.

학습 완료 후 checkpoint가 정상적으로 생성되었는지 확인합니다.

---

# 23. VS Code 운영 규칙

Windows + VS Code 환경에서는 다음을 기본으로 합니다.

```text
VS Code
  ↓
Python Interpreter 확인
  ↓
Jupyter Kernel 확인
  ↓
CUDA / GPU 확인
  ↓
Memory Profile 확인
  ↓
Notebook 실행
```

Terminal에서 사용하는 Python과 VS Code Notebook kernel의 Python이 다를 수 있으므로 `sys.executable`을 항상 확인합니다.

GPU 학습 Notebook을 실행할 때는 VS Code 내부의 다른 Python 프로세스, Jupyter kernel, 디버거가 메모리를 점유할 수 있음을 고려합니다.

학습 중에는 불필요한 Notebook kernel을 종료하고, 큰 변수나 출력 셀을 무분별하게 유지하지 않습니다.

---

# 24. Prompt 관리

긴 prompt를 Notebook마다 복사하지 않습니다.

예:

```text
prompts/
├── system/
│   └── default.txt
├── user/
│   └── pet_tarot.txt
└── evaluation/
    └── judge.txt
```

Prompt version도 가능하면 실험 metadata에 기록합니다.

---

# 25. API Key / Secret

절대로 다음처럼 작성하지 않습니다.

```python
OPENAI_API_KEY = "sk-..."
```

대신 환경변수 또는 해당 플랫폼의 Secret 기능을 사용합니다.

```python
import os

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)
```

다음 파일은 repository에 commit하지 않습니다.

```text
.env
*.pem
*.key
credentials.json
service-account.json
```

---

# 26. 재현성

실험에는 가능한 한 seed를 사용합니다.

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

가능하면 다음 metadata를 저장합니다.

```text
Python version
OS
Architecture
Package versions
Model ID / revision
Dataset version
Device
Parameters
Seed
Prompt version
Metrics
Resource profile
Peak VRAM
Peak RAM
```

LLM API의 서버 측 모델 업데이트나 비결정적 동작 때문에 완전한 재현성이 보장되지 않는 경우에는 해당 사실을 기록합니다.

---

# 27. Notebook Idempotency

Notebook은 가능한 한 여러 번 실행해도 안전해야 합니다.

나쁜 예:

```python
results.append(result)
```

초기화가 없는 경우 실행할 때마다 결과가 중복될 수 있습니다.

좋은 예:

```python
results = []
```

또는 명시적인 state 관리 방식을 사용합니다.

새 Kernel/Runtime에서 `Run All`이 가능해야 합니다.

---

# 28. Python Coding Standard

기본 기준:

- PEP 8
- Ruff
- Black-compatible formatting
- type hints
- 작은 함수
- 명확한 변수명
- explicit error handling

금지:

```python
try:
    ...
except:
    pass
```

명시적인 exception을 사용합니다.

```python
try:
    import package
except ImportError as exc:
    raise RuntimeError(
        "Required package is unavailable."
    ) from exc
```

---

# 29. 테스트

재사용 가능한 코드는 `tests/`에서 검증합니다.

최소 테스트 대상:

```text
imports
environment bootstrap
UTF-8
path handling
핵심 inference
evaluation
memory smoke test
checkpoint / resume
```

Notebook은 가능하면 clean kernel에서 실행 검증합니다.

---

# 30. Agent 권장 작업 순서

LLM/Jupyter 프로젝트를 수정할 때 Agent는 다음 순서를 따릅니다.

```text
1. Repository 구조 확인
2. AGENT.md 확인
3. SKILL.md 확인
4. pyproject.toml / requirements / lock 확인
5. Notebook 구조 확인
6. Python kernel 확인
7. OS / runtime 확인
8. GPU / VRAM / RAM 확인
9. dependency 확인
10. reusable code 확인
11. bootstrap cell 확인
12. memory budget 설정
13. 코드 수정
14. UTF-8 / path / device 확인
15. Memory Smoke Test
16. 테스트
17. clean kernel Run All
18. checkpoint / output 확인
19. 변경사항 보고
```

---

# 31. 새 Notebook 생성 예

Agent에게 다음처럼 요청할 수 있습니다.

```text
LLM SKILL을 적용해서 새로운 RAG 실험 Notebook을 만들어줘.
Jupyter와 Google Colab에서 모두 실행 가능해야 하고
Windows/Linux/macOS도 고려해줘.
상단에 environment detection, hardware/memory detection,
UTF-8, project root, dependency bootstrap, device detection을 넣어줘.
로컬 GPU가 4 GB VRAM이면 batch size 1과 메모리 절약 설정부터 시작해줘.
```

결과 Notebook의 시작 부분은 대략 다음과 같은 구조가 됩니다.

```python
# 1. Environment
ENV = detect_environment()

# 2. Resources
RESOURCES = inspect_resources()

# 3. UTF-8
configure_utf8()

# 4. Project Root
ROOT = detect_project_root()

# 5. Dependencies
ensure_package("numpy")
ensure_package("pandas")

# 6. Device
DEVICE = detect_device()

# 7. Resource configuration
BATCH_SIZE = 1
MAX_SEQ_LENGTH = 256
USE_FP16 = DEVICE == "cuda"

# 8. Experiment configuration
MODEL_ID = "..."
SEED = 42
```

---

# 32. 기존 Notebook 개선 예

기존 코드:

```python
!pip install transformers

model.to("cuda")

df = pd.read_csv("C:\\data\\input.csv")
```

개선 방향:

```python
ensure_package("transformers")

model.to(DEVICE)

df = pd.read_csv(
    DATA_DIR / "input.csv",
    encoding="utf-8",
)
```

추가로 로컬 4 GB GPU에서 학습하는 경우:

```python
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 8
MAX_SEQ_LENGTH = 256
USE_FP16 = DEVICE == "cuda"
```

즉:

```text
!pip
 ↓
active kernel 기준 pip

"cuda"
 ↓
auto device

OS-specific path
 ↓
pathlib.Path

implicit encoding
 ↓
explicit UTF-8

unbounded memory usage
 ↓
resource budget + monitoring
```

---

# 33. 의존성 관리 권장 순서

프로젝트 수준에서는 다음 우선순위를 권장합니다.

```text
1. pyproject.toml / lock file
2. requirements.txt
3. Notebook bootstrap
4. ensure_package()
```

`ensure_package()`를 이용해 프로젝트 dependency 관리를 전부 Notebook으로 옮기지 않습니다.

Notebook에서는 **환경이 처음 준비되지 않은 경우에도 실험을 시작할 수 있도록 보조**하는 용도로 사용합니다.

---

# 34. 완료 조건

LLM Notebook 또는 관련 코드를 완료했다고 판단하기 전에 가능한 범위에서 다음을 확인합니다.

```text
Environment
[ ] OS detection
[ ] architecture detection
[ ] Python version detection
[ ] sys.executable detection
[ ] Jupyter detection
[ ] Colab detection
[ ] device detection

Dependencies
[ ] package detection
[ ] missing package installation
[ ] active kernel installation
[ ] version requirements

Hardware / Memory
[ ] GPU name / VRAM 확인
[ ] System RAM 확인
[ ] CPU worker 수 확인
[ ] memory budget 설정
[ ] batch size 보수적 시작
[ ] sequence length 확인
[ ] mixed precision 검토
[ ] gradient accumulation 검토
[ ] gradient checkpointing 검토
[ ] quantization / offload 검토
[ ] Memory Smoke Test
[ ] OOM recovery strategy
[ ] checkpoint / resume

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

---

# 35. 다른 프로젝트에 복사할 때

최소 구성은 다음 두 파일입니다.

```text
AGENT.md
SKILL.md
```

README는 사용법 설명용이므로 반드시 복사할 필요는 없습니다.

프로젝트별 규칙이 추가되는 경우에는 이 표준을 기반으로 project-specific rule을 추가합니다.

예:

```text
AGENT.md
SKILL.md
PROJECT_RULES.md
```

프로젝트 규칙이 이 표준과 충돌하면 명시적으로 우선순위를 정의합니다.

---

# 36. 업데이트 방법

이 표준 repository의 `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/README.md`를 최신 버전으로 받은 후 프로젝트에 반영합니다.

```bash
git pull origin main
```

프로젝트에 직접 복사한 경우:

```bash
cp LLM/AGENT.md /path/to/project/AGENT.md
cp LLM/SKILL.md /path/to/project/SKILL.md
```

Windows에서는 파일 탐색기나 PowerShell을 사용해도 됩니다. OS에 종속되지 않는 Python script를 이용하는 방법도 권장합니다.

---

# 37. 권장 운영 방식

이 문서를 단순한 Markdown 참고자료로만 사용하지 말고 **LLM 개발 프로젝트의 공통 계약(contract)**으로 취급합니다.

특히 제한된 로컬 하드웨어에서는 다음 질문을 기본 점검 항목으로 삼습니다.

```text
이 코드는 현재 OS에서만 동작하는가?
이 코드는 Jupyter와 Colab에서 동작하는가?
현재 kernel에 package를 설치하는가?
한글이 깨지지 않는가?
GPU가 없어도 실행 가능한가?
현재 GPU VRAM과 RAM을 확인했는가?
현재 설정이 4 GB VRAM / 16 GB RAM 환경에서 합리적인가?
학습 전에 Memory Smoke Test를 수행하는가?
OOM 또는 RAM 부족 시 낮출 설정이 정의되어 있는가?
checkpoint로 학습을 재개할 수 있는가?
API key가 노출되지 않는가?
Kernel을 재시작하고 Run All할 수 있는가?
재사용 코드는 src로 분리되어 있는가?
실험 결과를 재현할 수 있는 metadata가 있는가?
```

이 질문에 문제가 없으면 LLM/Jupyter 개발 표준에 부합하는 것으로 판단합니다.

---

# 38. 관련 파일

- `AGENT.md` — Agent가 따라야 할 전체 개발 규칙
- `SKILL.md` — Jupyter/Colab LLM 작업 절차 및 실행 패턴
- `README.md` — 설치, 적용, 사용, 하드웨어 최적화 및 운영 가이드
