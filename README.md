# codingStandard

AI coding agent가 프로젝트를 일관된 규칙으로 개발하도록 만드는 공통 Coding Standard 저장소입니다.

## 바로 사용하기

### 1. 이 저장소 자체를 clone해서 사용하는 경우

```bash
git clone https://github.com/eaglesjo/codingStandard.git
cd codingStandard
```

clone 후 별도 설치 없이 AI coding agent가 사용할 수 있도록 프로젝트 루트에 AI별 자동 진입점이 포함되어 있습니다.

```text
codingStandard/
├── AGENTS.md                         # 공통 Agent 진입점
├── CLAUDE.md                         # Claude Code 자동 진입점
├── GEMINI.md                         # Gemini CLI 자동 진입점
├── .github/
│   ├── copilot-instructions.md       # GitHub Copilot 저장소 전체 규칙
│   └── instructions/
│       └── llm.instructions.md       # Python/Notebook/ML 경로별 규칙
├── LLM/
│   ├── AGENT.md                      # Canonical 전체 개발 규칙
│   ├── SKILL.md                      # Canonical LLM/Jupyter 작업 절차
│   ├── ENVIRONMENT.md                # 환경 측정/최적화 규칙
│   ├── environment.py                # 실행환경 프로파일러
│   ├── LOCAL_HARDWARE_PROFILE_BACKUP.md # 이전 로컬 하드웨어 백업
│   └── README.md                     # LLM 표준 사용 가이드
└── scripts/
    ├── install-coding-standard.ps1   # Windows 설치
    └── install-coding-standard.sh    # Linux/macOS 설치
```

## AI 자동 로딩 구조

공통 규칙은 `LLM/AGENT.md`, `LLM/SKILL.md`, `LLM/ENVIRONMENT.md`에 두고, AI 제품별 자동 탐색 파일은 얇은 adapter로 유지합니다.

중요: 특정 PC의 GPU, RAM, OS를 현재 실행환경의 전제조건으로 사용하지 않습니다. 실제 환경은 `LLM/environment.py`가 측정한 결과를 source of truth로 사용합니다.

```text
                LLM/AGENT.md
                LLM/SKILL.md
             LLM/ENVIRONMENT.md
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    AGENTS.md     CLAUDE.md    GEMINI.md
        │             │            │
        └───────┬─────┴─────┬──────┘
                ↓           ↓
     .github/copilot-   .github/instructions/
       instructions.md    llm.instructions.md
```

## 다른 프로젝트에 적용하기

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

설치 스크립트는 AI 자동 진입점, `LLM/` 표준 문서 및 환경 프로파일러를 프로젝트에 배치합니다.

## 개발 시작 시 AI가 수행해야 하는 순서

```text
AI instruction 자동 로딩
        ↓
Repository / project 구조 확인
        ↓
OS / IDE / Python / Runtime 확인
        ↓
CPU / GPU / VRAM / RAM 확인
        ↓
LLM/environment.py 실행
        ↓
Environment Profile / Runtime Configuration 생성
        ↓
Memory Smoke Test
        ↓
Environment Lock
        ↓
불필요한 OS / device 분기 제거
        ↓
실행환경에 맞게 batch / sequence / workers / precision 최적화
        ↓
구현 / 테스트
```

환경이 실제로 하나로 확정된 프로젝트에서는 해당 환경에 필요하지 않은 대체 실행 경로를 제거합니다. 여러 플랫폼을 공식 지원하는 reusable library는 필요한 분기를 유지합니다.

## Environment Profiler

프로파일러는 현재 Python/IDE/Jupyter/Colab, CPU, RAM, GPU, VRAM, CUDA/MPS를 측정하고 보수적인 runtime configuration을 계산합니다.

```bash
python LLM/environment.py
```

profile을 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

주요 resolved 설정:

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

권장값은 시작점이며 실제 Memory Smoke Test 결과를 기준으로 최종 확정합니다.

## LLM/ML 학습 기본 원칙

특정 GPU/RAM을 고정하지 않고 실제 측정된 자원을 기준으로 보수적인 runtime profile을 구성합니다.

학습 코드는 다음을 기본 적용합니다.

- VRAM/RAM/CPU 사전 측정
- 보수적인 batch size
- gradient accumulation
- 지원되는 CUDA에서 FP16 AMP 검토
- 필요 시 gradient checkpointing / quantization / CPU offload
- DataLoader worker 절제
- Memory Smoke Test
- Validation metric
- Early Stopping
- Best checkpoint / Resume
- Ablation Study configuration
- Seed / model revision / dataset revision / metric / resource usage / environment profile 기록
- OOM 단계별 recovery

이전에 사용하던 특정 로컬 장비 프로파일은 `LLM/LOCAL_HARDWARE_PROFILE_BACKUP.md`에 보존되어 있으며 현재 환경 판정에는 사용하지 않습니다.

상세 규칙은 `LLM/AGENT.md`, 실행 절차는 `LLM/SKILL.md`, 환경 최적화는 `LLM/ENVIRONMENT.md`를 사용합니다.
