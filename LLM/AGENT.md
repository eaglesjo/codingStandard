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

핵심 목표:

- OS 독립성
- Jupyter/Colab 호환성
- 활성 Python kernel 기준 패키지 설치
- UTF-8 및 한글 안전성
- CPU/CUDA/MPS 자동 감지
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

## 3. Notebook 표준 구조

권장 순서:

1. 목적 Markdown
2. 환경 감지
3. UTF-8 설정
4. 프로젝트 루트 감지
5. 의존성 확인/설치
6. imports
7. configuration
8. data
9. model/client
10. experiment
11. evaluation
12. visualization
13. export
14. reproducibility metadata

재사용 가능한 함수와 클래스를 Notebook에 중복 작성하지 않는다.

## 4. 환경 자동 감지

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

## 5. 활성 Kernel 기준 패키지 설치

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

## 6. 프로젝트 루트 자동 감지

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

## 7. Cross-platform Path

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

## 8. Windows / Linux / macOS

### Windows

`rm`, `cp`, `mv`, `grep`, `sed`, `awk` 등 Unix 전용 명령에 의존하지 않는다.

### Linux

특정 배포판, 사용자 home, shell 또는 GPU가 있다고 가정하지 않는다.

### macOS

Intel과 Apple Silicon을 가정하지 않고 `platform.machine()`으로 architecture를 확인한다.

가능하면 OS별 분기 대신 Python 표준 API를 사용한다.

## 9. subprocess

가능하면 Python 표준 라이브러리를 사용한다.

```python
import subprocess

subprocess.run(command, check=True)
```

가능하면 `shell=True`를 사용하지 않는다.

## 10. Google Colab

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

## 11. UTF-8 / 한글

```python
import sys

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

print("한글 UTF-8 테스트: 정상")
```

파일 읽기/쓰기는 encoding을 명시한다.

```python
text = Path(path).read_text(encoding="utf-8")
Path(path).write_text(text, encoding="utf-8")
```

JSON:

```python
import json

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
```

CSV:

```python
import pandas as pd

df = pd.read_csv(path, encoding="utf-8")
```

BOM이 필요한 Excel/Windows 호환 CSV에 한해서 `utf-8-sig`를 사용한다.

## 12. Korean Matplotlib

OS별 한글 폰트를 단일 이름으로 고정하지 않는다.

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

사용 가능한 폰트가 없으면 warning을 출력하고 코드 자체는 계속 실행 가능하도록 만든다.

## 13. CPU / CUDA / MPS 자동 감지

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

## 14. LLM 코드 구조

다음 요소를 분리한다.

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

## 15. Prompt 관리

긴 prompt를 Notebook 여러 곳에 복사하지 않는다.

권장 구조:

```text
prompts/
├── system/
├── user/
└── evaluation/
```

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

`.env`, token, credential, private key 파일을 Git에 commit하지 않는다.

## 17. 재현성

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
- parameters
- seed
- prompt version
- metrics

## 18. Python Coding Standard

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

## 19. Notebook Idempotency

Notebook은 cell을 반복 실행해도 상태가 예기치 않게 누적되지 않아야 한다.

Kernel/Runtime 재시작 후 Run All이 가능해야 한다.

## 20. 테스트

재사용 가능한 `src/` 코드에는 `tests/`를 작성한다.

최소 검증:

- imports
- environment bootstrap
- UTF-8
- paths
- 핵심 inference/evaluation

## 21. Agent 작업 순서

1. repository 구조 확인
2. `pyproject.toml` / requirements / lock file 확인
3. Notebook 구조 확인
4. Python kernel 확인
5. OS/runtime 확인
6. dependency 확인
7. reusable code를 `src/`로 분리
8. bootstrap cell 추가/수정
9. UTF-8 및 cross-platform 문제 확인
10. 테스트
11. clean kernel에서 Notebook 실행
12. 변경 사항 보고

## 22. 완료 조건

```text
[ ] OS 감지
[ ] architecture 감지
[ ] Python version 감지
[ ] sys.executable 확인
[ ] Jupyter 감지
[ ] Colab 감지
[ ] dependency 확인
[ ] 없는 package만 설치
[ ] active kernel 기준 설치
[ ] UTF-8 설정
[ ] 한글 출력 테스트
[ ] 한글 matplotlib 처리
[ ] project root 감지
[ ] cross-platform path
[ ] CPU/CUDA/MPS 감지
[ ] secret 미노출
[ ] notebook top-to-bottom 실행
[ ] hidden state 없음
[ ] reusable code가 src에 있음
[ ] 테스트 실행
[ ] 재현성 metadata 기록
```
