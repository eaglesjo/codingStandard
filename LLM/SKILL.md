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
Cell 2: UTF-8 Configuration
Cell 3: Project Root Detection
Cell 4: Dependency Bootstrap
Cell 5: Imports
Cell 6: Configuration
Cell 7+: Experiment
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

## 13. LLM 구조

```text
Configuration
    ↓
Prompt
    ↓
Data
    ↓
Model / API Client
    ↓
Inference
    ↓
Evaluation
    ↓
Export
```

재사용 구현은 `src/`에 둔다.

## 14. Model Configuration

```python
MODEL_ID = "..."
TEMPERATURE = 0.2
MAX_NEW_TOKENS = 512
SEED = 42
```

magic number를 여러 cell에 분산하지 않는다.

## 15. Prompt 관리

```text
prompts/
├── system/
├── user/
└── evaluation/
```

재사용 prompt를 Notebook에 복사하지 않는다.

## 16. Secret 관리

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

## 17. Reproducibility

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

실험 metadata에는 가능한 경우 Python version, OS, architecture, package versions, model ID/revision, dataset version, device, parameters, seed, prompt version, metrics를 기록한다.

## 18. Notebook Idempotency

cell을 여러 번 실행해도 예기치 않은 상태 누적이 없어야 한다.

```python
results = []
```

같은 결과에 반복적으로 append되는 hidden state를 피한다.

## 19. Korean Matplotlib

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

## 20. Error Handling

금지:

```python
try:
    ...
except:
    pass
```

명시적인 exception type과 actionable error message를 사용한다.

## 21. Code Quality

- PEP 8
- Ruff
- Black-compatible formatting
- type hints
- small functions
- explicit error handling
- reusable code in `src/`
- tests in `tests/`

## 22. Notebook 자동 생성 규칙

새 Notebook:

1. 목적 Markdown
2. Environment Detection
3. UTF-8
4. Project Root
5. Dependency Bootstrap
6. Imports
7. Configuration
8. Experiment

기존 Notebook:

- 사용자 코드를 삭제하지 않는다.
- bootstrap이 없으면 상단에 추가한다.
- `!pip install`은 active kernel 기준 설치로 정리한다.
- OS 고정 경로는 `Path`로 변경한다.
- encoding을 명시한다.
- `cuda` 하드코딩을 device detection으로 바꾼다.
- 중복 reusable code는 `src/` 분리를 검토한다.

## 23. Validation Workflow

수정 후 가능하면:

1. Kernel/Runtime restart
2. Run All
3. dependency 확인
4. environment 확인
5. UTF-8/한글 확인
6. model inference 확인
7. visualization 확인
8. output 확인
9. relevant tests 실행

## 24. 완료 체크리스트

```text
Environment
[ ] OS
[ ] architecture
[ ] Python version
[ ] sys.executable
[ ] Jupyter
[ ] Colab
[ ] device

Dependencies
[ ] package detection
[ ] missing package installation
[ ] active kernel installation
[ ] version requirements

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

## 25. Definition of Done

- local Jupyter에서 동작
- Google Colab에서 동작
- Windows/Linux/macOS 고려
- active Python kernel 감지
- missing dependency를 해당 kernel에 설치
- UTF-8/Korean 보존
- cross-platform path 사용
- CPU/CUDA/MPS 자동 감지
- secret 보호
- fresh kernel/runtime에서 Run All 가능
- reusable code와 Notebook orchestration 분리
- 재현성 정보 기록
