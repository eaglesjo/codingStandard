# codingStandard

> **언어:** [English README](README.md) · 한국어 (현재 문서)

AI coding agent가 프로젝트를 일관된 규칙으로 개발하도록 돕는 공통 Coding Standard 저장소입니다.

Python / LLM / ML / Jupyter / Google Colab 개발을 중심으로 환경 확인, 자원 프로파일링, 실행 설정 결정, 메모리 안전 실행, 학습 재현성을 표준화합니다.

## 설치

저장소를 clone한 뒤 **적용할 프로젝트의 루트 디렉터리에서** 설치 스크립트를 실행합니다.

### Windows / PowerShell

언어를 설치 중에 선택하려면:

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

영문으로 명시적 설치:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language en
```

한글로 명시적 설치:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target . -Language ko
```

### Linux / macOS

언어를 설치 중에 선택하려면:

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

영문:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . en
```

한글:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh . ko
```

선택한 언어의 문서는 대상 프로젝트에서 AI 도구가 자동 탐색하는 표준 파일 이름으로 설치됩니다.

## 사용법

설치 후 대상 프로젝트 루트에서 실행환경 프로파일러를 실행합니다.

```bash
python LLM/environment.py
```

프로파일을 저장하려면:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

프로파일러는 현재 Python/runtime, OS, CPU, RAM, GPU, VRAM, CUDA/MPS, IDE/Jupyter/Colab 상태를 실제로 측정하고 workload에 맞는 보수적인 runtime configuration을 계산합니다.

특정 GPU, RAM, OS, IDE를 필수 전제조건으로 고정하지 않습니다. 실제 측정값과 workload를 기준으로 최종 설정을 결정합니다.

## AI 작업 흐름

```text
AI instructions 자동 로딩
        ↓
Repository / project 구조 확인
        ↓
Python / active kernel / IDE / runtime 확인
        ↓
CPU / RAM / GPU / VRAM / accelerator 측정
        ↓
Environment Profile 생성
        ↓
Runtime Configuration 결정
        ↓
Memory Smoke Test
        ↓
Environment Lock
        ↓
불필요한 OS / device branch 제거
        ↓
구현 / 학습 / 추론
        ↓
Evaluation / Early Stopping / Checkpoint
        ↓
Ablation / 재현성 / 자원 사용량 기록
        ↓
최종 Clean Run
```

## 저장소 구조

```text
codingStandard/
├── README.md                    # English default
├── README.ko.md                 # 한국어 안내
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── .github/
├── i18n/
│   ├── README.md
│   └── ko/
│       ├── AGENTS.md
│       ├── CLAUDE.md
│       ├── GEMINI.md
│       ├── .github/
│       └── LLM/
├── LLM/
│   ├── AGENT.md
│   ├── SKILL.md
│   ├── ENVIRONMENT.md
│   ├── environment.py
│   └── README.md
└── scripts/
    ├── install-coding-standard.ps1
    └── install-coding-standard.sh
```

## 자동 AI 지침 로딩

공통 규칙은 `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`를 기준으로 합니다.

설치 스크립트는 `en` 또는 `ko`를 선택하면 동일한 표준 파일 이름에 해당 언어의 문서를 배치합니다. 따라서 사용 중인 AI 도구는 별도의 수동 복사 없이 프로젝트의 표준 진입점을 읽을 수 있습니다.

## Environment Profiler

실행:

```bash
python LLM/environment.py
```

프로파일 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

환경 프로파일에는 실제 실행 환경과 resolved runtime configuration이 함께 기록됩니다. 권장값은 시작점이며 실제 Memory Smoke Test 결과를 기준으로 최종 확정합니다.

## ML / LLM 학습 원칙

- 제한된 VRAM/RAM을 고려해 batch, sequence length, workers, precision을 조정합니다.
- gradient accumulation으로 effective batch size를 확보합니다.
- 지원되는 accelerator에서는 mixed precision을 검토합니다.
- 필요 시 gradient checkpointing, quantization, CPU offload를 검토합니다.
- Memory Smoke Test를 통과한 설정으로 본 학습을 시작합니다.
- validation metric, Early Stopping, best checkpoint, Resume을 기본 적용합니다.
- Ablation Study는 명시적인 configuration matrix와 동일 평가 조건으로 수행합니다.
- seed, model/dataset revision, metric, runtime, peak VRAM/RAM, resolved environment profile을 기록합니다.
- OOM 발생 시 같은 설정을 반복하지 않고 단계별 memory recovery를 적용합니다.

## 문서

- 전체 개발 규칙: `LLM/AGENT.md`
- 실행 절차: `LLM/SKILL.md`
- 환경 최적화: `LLM/ENVIRONMENT.md`
- LLM/Jupyter 사용 가이드: `LLM/README.md`
- 환경 프로파일러: `LLM/environment.py`
- [영문 README](README.md)
