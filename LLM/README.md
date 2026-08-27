# LLM Coding Standard

Python 기반 LLM/ML 개발을 위한 `AGENT.md`와 `SKILL.md` 사용 가이드입니다.

이 표준은 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, Colab Local Runtime을 대상으로 하며 Windows / Linux / macOS 및 다양한 CPU/GPU/RAM 환경을 고려합니다.

## 1. 구성

```text
LLM/
├── AGENT.md
├── SKILL.md
├── ENVIRONMENT.md
├── environment.py
├── LOCAL_HARDWARE_PROFILE_BACKUP.md
└── README.md
```

### AGENT.md

AI Agent가 프로젝트를 수정할 때 따라야 하는 상위 개발 규칙입니다.

### SKILL.md

LLM/Jupyter 작업을 수행할 때 실제 적용하는 실행 절차입니다.

### ENVIRONMENT.md

실행환경 확인, Profile Resolution, Environment Lock 및 최적화 규칙입니다.

### environment.py

현재 Python/IDE/Jupyter/Colab, CPU, RAM, GPU, VRAM, CUDA/MPS 상태를 측정하고 workload에 맞는 보수적인 runtime configuration을 계산하는 실행 가능한 프로파일러입니다.

### LOCAL_HARDWARE_PROFILE_BACKUP.md

특정 개발 장비의 과거 참고 프로파일을 보존하기 위한 백업 문서입니다. 현재 환경 판정이나 runtime 결정에는 사용하지 않습니다.

## 2. 설치

이 저장소를 clone한 뒤 대상 프로젝트에서 설치 스크립트를 실행합니다.

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

설치 스크립트는 AI 자동 진입점과 `LLM/` 표준 파일을 대상 프로젝트에 복사합니다.

## 3. 사용법

대상 프로젝트의 루트에서 환경 프로파일러를 실행합니다.

```bash
python LLM/environment.py
```

프로파일을 저장하려면:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

Notebook에서는 다음과 같이 resolved configuration을 가져옵니다.

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

## 4. AI 작업 흐름

```text
AI instruction 자동 로딩
        ↓
Repository / project 구조 확인
        ↓
실제 Python / IDE / runtime 확인
        ↓
CPU / RAM / GPU / VRAM / accelerator 확인
        ↓
환경 프로파일 생성
        ↓
Runtime Configuration 결정
        ↓
Memory Smoke Test
        ↓
Environment Lock
        ↓
불필요한 환경 / device branch 제거
        ↓
구현 / 학습 / 추론
        ↓
평가 / Early Stopping / Checkpoint
        ↓
Ablation / 결과 기록
```

환경이 확정되기 전에는 범용 코드를 유지하고, 확정 후에는 실제 사용하는 실행 경로를 기준으로 정리합니다.

## 5. 환경 최적화 원칙

프로파일러는 다음 정보를 측정합니다.

```text
OS / architecture
Python / executable
IDE / Jupyter / Colab
CPU count
System RAM total / available
GPU name
VRAM total / free
CUDA / MPS availability
resolved device
```

그리고 다음 설정의 보수적인 시작값을 계산합니다.

```text
device
batch_size
gradient_accumulation_steps
num_workers
pin_memory
FP16 / BF16
gradient_checkpointing
max_seq_length
```

권장값은 시작점이며 실제 Memory Smoke Test 결과가 최종 기준입니다. 특정 GPU/RAM/OS를 실행 전제조건으로 고정하지 않습니다.

## 6. Memory / OOM

본 학습 전에 다음 최소 workload를 검증합니다.

```text
load → forward → backward → optimizer step → validation → checkpoint
```

OOM이 발생하면 같은 설정을 반복하지 않고 다음 순서로 완화합니다.

```text
VRAM/RAM 기록
→ batch ↓
→ sequence/input ↓
→ workers ↓
→ AMP 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 학습
```

## 7. 학습 기본 원칙

장시간 학습에는 validation metric, Early Stopping, best checkpoint, Resume을 기본 적용합니다.

실험에는 configuration matrix를 사용하고 seed, model/dataset revision, metric, runtime, peak VRAM/RAM, resolved environment profile을 기록합니다.

## 8. 상세 문서

전체 개발 규칙: `LLM/AGENT.md`

실행 절차: `LLM/SKILL.md`

환경 최적화: `LLM/ENVIRONMENT.md`

환경 프로파일러: `LLM/environment.py`
