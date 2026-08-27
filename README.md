# codingStandard

AI coding agent가 프로젝트를 일관된 규칙으로 개발하도록 돕는 공통 Coding Standard 저장소입니다.

Python / LLM / ML / Jupyter / Google Colab 개발을 중심으로 환경 확인, 자원 프로파일링, 실행 설정 결정, 메모리 검증, 학습 재현성을 표준화합니다.

## 설치

저장소를 clone한 뒤 **적용할 프로젝트의 루트 디렉터리에서** 설치 스크립트를 실행합니다.

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

설치 스크립트는 대상 프로젝트에 다음 자동 진입점과 표준 문서를 복사합니다.

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/copilot-instructions.md
.github/instructions/llm.instructions.md
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
LLM/environment.py
LLM/README.md
```

스크립트는 기존 대상 파일이 있으면 덮어쓸 수 있으므로 적용 전 변경사항을 확인합니다.

## 사용법

설치가 끝나면 대상 프로젝트 루트에서 환경 프로파일러를 실행합니다.

```bash
python LLM/environment.py
```

프로파일을 저장하려면:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

프로파일러는 현재 Python/IDE/Jupyter/Colab, OS, CPU, RAM, GPU, VRAM, CUDA/MPS 상태를 측정하고 보수적인 runtime configuration을 계산합니다.

주요 resolved 설정:

```text
device
batch_size
gradient_accumulation_steps
num_workers
pin_memory
fp16 / bf16
gradient_checkpointing
max_seq_length
```

특정 GPU, RAM, OS, IDE를 실행 전제조건으로 고정하지 않습니다. 실제 측정값과 workload를 기준으로 최종 설정을 확정합니다.

## AI 작업 흐름

AI coding agent는 대체로 다음 순서로 작업합니다.

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
Runtime Configuration Resolve
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
Ablation / Reproducibility / Resource 기록
        ↓
최종 Clean Run
```

즉, **환경을 먼저 측정하고 → 실행 설정을 결정하고 → 최소 workload로 검증한 뒤 → 구현과 실행을 진행**하는 구조입니다.

## 저장소 구조

```text
codingStandard/
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
│       └── llm.instructions.md
├── LLM/
│   ├── AGENT.md
│   ├── SKILL.md
│   ├── ENVIRONMENT.md
│   ├── environment.py
│   ├── LOCAL_HARDWARE_PROFILE_BACKUP.md
│   └── README.md
└── scripts/
    ├── install-coding-standard.ps1
    └── install-coding-standard.sh
```

`LOCAL_HARDWARE_PROFILE_BACKUP.md`는 특정 개발 장비의 과거 참고값을 보존하기 위한 백업입니다. 설치 대상 표준에는 포함하지 않으며 runtime 결정에도 사용하지 않습니다.

## 자동 로딩 구조

공통 규칙의 canonical source는 다음 세 파일입니다.

```text
LLM/AGENT.md
LLM/SKILL.md
LLM/ENVIRONMENT.md
```

제품별 자동 진입점은 이를 프로젝트에 연결하는 얇은 adapter 역할을 합니다.

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

## Environment Profiler

실행:

```bash
python LLM/environment.py
```

프로파일 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

환경 프로파일에는 실제 실행 환경과 resolved runtime configuration이 함께 기록됩니다. 권장값은 시작점이며 모델/데이터별 Memory Smoke Test 결과를 기준으로 최종 확정합니다.

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

전체 개발 규칙: `LLM/AGENT.md`

실행 절차: `LLM/SKILL.md`

환경 최적화: `LLM/ENVIRONMENT.md`

LLM/Jupyter 사용 가이드: `LLM/README.md`

환경 프로파일러: `LLM/environment.py`
