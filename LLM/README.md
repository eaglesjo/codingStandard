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
Cell 2  : UTF-8 Configuration
Cell 3  : Project Root Detection
Cell 4  : Dependency Bootstrap
Cell 5  : Imports
Cell 6  : Configuration
Cell 7+ : Experiment
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

# 12. Google Colab

Colab 여부:

```python
IS_COLAB = "google.colab" in sys.modules
```

Colab 기본 workspace:

```python
WORKSPACE = (
    Path("/content")
    if IS_COLAB
    else ROOT
)
```

Colab runtime의 파일은 영구 저장소가 아니므로 중요한 결과물은 별도의 영구 저장 위치에 export해야 합니다.

Google Drive가 필요한 경우에만 mount합니다.

```python
def mount_google_drive():
    if not IS_COLAB:
        return False

    from google.colab import drive
    drive.mount("/content/drive")
    return True
```

---

# 13. Colab Local Runtime

Colab Local Runtime에서는 Notebook이 사용자의 실제 PC에서 실행됩니다.

따라서 다음과 같은 동작이 로컬 PC에서 수행될 수 있음을 고려해야 합니다.

- 파일 읽기/쓰기
- subprocess
- package installation
- local network access
- GPU access

따라서 신뢰할 수 있는 Notebook만 실행하고 외부 Notebook을 그대로 실행하지 않습니다.

---

# 14. LLM 프로젝트 구조

권장 구조:

```text
project/
├── AGENT.md
├── SKILL.md
├── pyproject.toml
├── src/
│   └── ...
├── notebooks/
│   ├── 00_environment_check.ipynb
│   ├── 01_data_preparation.ipynb
│   ├── 02_model_loading.ipynb
│   ├── 03_experiment.ipynb
│   └── 04_evaluation.ipynb
├── prompts/
│   ├── system/
│   ├── user/
│   └── evaluation/
├── tests/
└── outputs/
```

Notebook은 orchestration과 실험에 집중하고, 재사용 가능한 로직은 `src/`로 이동합니다.

---

# 15. Prompt 관리

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

# 16. API Key / Secret

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

# 17. 재현성

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
```

LLM API의 서버 측 모델 업데이트나 비결정적 동작 때문에 완전한 재현성이 보장되지 않는 경우에는 해당 사실을 기록합니다.

---

# 18. Notebook Idempotency

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

# 19. Python Coding Standard

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

# 20. 테스트

재사용 가능한 코드는 `tests/`에서 검증합니다.

최소 테스트 대상:

```text
imports
environment bootstrap
UTF-8
path handling
핵심 inference
evaluation
```

Notebook은 가능하면 clean kernel에서 실행 검증합니다.

---

# 21. Agent 권장 작업 순서

LLM/Jupyter 프로젝트를 수정할 때 Agent는 다음 순서를 따릅니다.

```text
1. Repository 구조 확인
2. AGENT.md 확인
3. SKILL.md 확인
4. pyproject.toml / requirements / lock 확인
5. Notebook 구조 확인
6. Python kernel 확인
7. OS / runtime 확인
8. dependency 확인
9. reusable code 확인
10. bootstrap cell 확인
11. 코드 수정
12. UTF-8 / path / device 확인
13. 테스트
14. clean kernel Run All
15. 변경사항 보고
```

---

# 22. 새 Notebook 생성 예

Agent에게 다음처럼 요청할 수 있습니다.

```text
LLM SKILL을 적용해서 새로운 RAG 실험 Notebook을 만들어줘.
Jupyter와 Google Colab에서 모두 실행 가능해야 하고
Windows/Linux/macOS도 고려해줘.
상단에 environment detection, UTF-8, project root,
dependency bootstrap, device detection을 넣어줘.
```

결과 Notebook의 시작 부분은 대략 다음과 같은 구조가 됩니다.

```python
# 1. Environment
ENV = detect_environment()

# 2. UTF-8
configure_utf8()

# 3. Project Root
ROOT = detect_project_root()

# 4. Dependencies
ensure_package("numpy")
ensure_package("pandas")

# 5. Device
DEVICE = detect_device()

# 6. Experiment configuration
MODEL_ID = "..."
SEED = 42
```

---

# 23. 기존 Notebook 개선 예

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
```

---

# 24. 의존성 관리 권장 순서

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

# 25. 완료 조건

LLM Notebook 또는 관련 코드를 완료했다고 판단하기 전에 가능한 범위에서 다음을 확인합니다.

```text
[ ] OS detection
[ ] architecture detection
[ ] Python version detection
[ ] sys.executable detection
[ ] Jupyter detection
[ ] Colab detection
[ ] dependency detection
[ ] missing package installation
[ ] active kernel installation
[ ] UTF-8
[ ] Korean text
[ ] Korean matplotlib
[ ] project root detection
[ ] cross-platform path
[ ] CPU/CUDA/MPS
[ ] secret protection
[ ] notebook idempotency
[ ] Run All
[ ] reusable code separation
[ ] tests
[ ] reproducibility metadata
```

---

# 26. 다른 프로젝트에 복사할 때

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

# 27. 업데이트 방법

이 표준 repository의 `LLM/AGENT.md`, `LLM/SKILL.md`를 최신 버전으로 받은 후 프로젝트에 반영합니다.

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

# 28. 권장 운영 방식

이 문서를 단순한 Markdown 참고자료로만 사용하지 말고 **LLM 개발 프로젝트의 공통 계약(contract)**으로 취급합니다.

Agent가 Notebook을 만들거나 수정할 때 다음을 기본 질문으로 삼습니다.

```text
이 코드는 현재 OS에서만 동작하는가?
이 코드는 Jupyter와 Colab에서 동작하는가?
현재 kernel에 package를 설치하는가?
한글이 깨지지 않는가?
GPU가 없어도 실행 가능한가?
API key가 노출되지 않는가?
Kernel을 재시작하고 Run All할 수 있는가?
재사용 코드는 src로 분리되어 있는가?
실험 결과를 재현할 수 있는 metadata가 있는가?
```

이 질문에 문제가 없으면 LLM/Jupyter 개발 표준에 부합하는 것으로 판단합니다.

---

# 29. 관련 파일

- `AGENT.md` — Agent가 따라야 할 전체 개발 규칙
- `SKILL.md` — Jupyter/Colab LLM 작업 절차 및 실행 패턴
- `README.md` — 설치, 적용, 사용 및 운영 가이드
