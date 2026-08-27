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
│   └── README.md                     # LLM 표준 사용 가이드
└── scripts/
    ├── install-coding-standard.ps1   # Windows 설치
    └── install-coding-standard.sh    # Linux/macOS 설치
```

## AI 자동 로딩 구조

공통 규칙은 `LLM/AGENT.md`와 `LLM/SKILL.md`에 두고, AI 제품별 자동 탐색 파일은 얇은 adapter로 유지합니다.

```text
                LLM/AGENT.md
                     │
                LLM/SKILL.md
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

GitHub Copilot은 저장소 전체 지침으로 `.github/copilot-instructions.md`를 지원하고, VS Code/Copilot 및 Copilot CLI에서는 `AGENTS.md`를 Agent instruction으로 사용할 수 있습니다. Gemini CLI는 `GEMINI.md`, Claude Code는 프로젝트 루트의 `CLAUDE.md`를 자동으로 읽습니다.

## 다른 프로젝트에 적용하기

### Windows / PowerShell

먼저 standard repository를 clone합니다.

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
```

프로젝트 루트에서 다음을 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-coding-standard.sh .
```

설치 스크립트는 다음을 프로젝트 루트에 배치합니다.

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.github/copilot-instructions.md
.github/instructions/llm.instructions.md
LLM/AGENT.md
LLM/SKILL.md
LLM/README.md
```

기존 파일은 교체될 수 있으므로, 프로젝트별로 이미 수정한 파일이 있다면 먼저 백업하거나 diff를 확인합니다.

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
Environment Profile 확정
        ↓
불필요한 OS / device 분기 제거
        ↓
Dependency / UTF-8 / Path 확인
        ↓
Memory budget 적용
        ↓
구현 / 테스트
```

환경이 실제로 하나로 확정된 프로젝트에서는 해당 환경에 필요하지 않은 대체 실행 경로를 제거합니다. 여러 플랫폼을 공식 지원하는 reusable library는 필요한 분기를 유지합니다.

## LLM/ML 학습 기본 원칙

기본 로컬 프로파일은 다음을 기준으로 합니다.

```text
Windows
VS Code
NVIDIA RTX 3050 Ti Laptop GPU / 4 GB VRAM
System RAM / 16 GB
```

학습 코드는 다음을 기본 적용합니다.

- VRAM/RAM 사전 측정
- 보수적인 batch size
- gradient accumulation
- FP16 AMP
- 필요 시 gradient checkpointing / quantization / CPU offload
- Windows DataLoader worker 절제
- Validation metric
- Early Stopping
- Best checkpoint / Resume
- Ablation Study configuration
- Seed / model revision / dataset revision / metric / resource usage 기록
- OOM 단계별 recovery

상세 규칙은 `LLM/AGENT.md`, 실행 절차는 `LLM/SKILL.md`를 확인합니다.

## 관련 문서

- `AGENTS.md` — AI coding agent 공통 진입점
- `LLM/AGENT.md` — 전체 개발 규칙
- `LLM/SKILL.md` — 실제 작업 절차 및 실행 패턴
- `LLM/README.md` — LLM 표준 상세 사용 가이드
