# AI Engineering Standard

<p align="center">
  <strong>AI Development, Training & Agent Engineering Standards</strong>
</p>

> **언어:** [English README](README.md) · 한국어 (현재 문서) · [한국어 설치 가이드](i18n/ko/INSTALL.md)

AI Engineering Standard는 AI-assisted development, 모델 학습, 실험, LLM/Vision workflow, AI coding agent를 위한 재사용 가능한 엔지니어링 표준입니다.

## ✨ 주요 기능

- 공통 프로젝트 지침과 coding rules
- LLM 및 Vision domain guidance
- 작업별 Skills
- 실행 환경 및 resource detection
- Windows / Linux / macOS cross-platform installer
- English / Korean localization
- repository validation 및 installer test suite
- Manus Project Instructions 및 Skills
- 재현 가능한 training 및 experiment workflow

## 🚀 설치

저장소를 clone한 뒤 적용할 프로젝트의 루트에서 도메인 설치기를 실행합니다.

### Windows / PowerShell

```powershell
git clone https://github.com/eaglesjo/codingStandard.git
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target .
```

명시적으로 설치:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain vision
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-domains.ps1 -Target . -Language ko -Domain all
```

`-DryRun`으로 설치 전에 변경 대상을 확인하고, `-ConflictAction Ask|Merge|Overwrite|Skip`으로 기존 파일 처리를 지정할 수 있습니다.

### Linux / macOS

```bash
git clone https://github.com/eaglesjo/codingStandard.git
bash ./codingStandard/scripts/install-domains.sh .
```

명시적 설치:

```bash
bash ./codingStandard/scripts/install-domains.sh . ko vision ask false
bash ./codingStandard/scripts/install-domains.sh . ko all overwrite false
```

인자 순서는 `TARGET LANGUAGE DOMAIN CONFLICT_POLICY DRY_RUN`입니다.

## 🤖 지원하는 AI 개발 도구

| 도구 | 프로젝트 규칙 / 연동 |
| --- | --- |
| OpenAI Codex / 호환 Agent | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/` |
| Cursor | `.cursor/rules/coding-standard.mdc` |
| Windsurf | `.windsurf/rules/coding-standard.md` |
| Cline | `.clinerules/01-coding-standard.md` |
| Continue | `.continue/rules/coding-standard.md` |
| JetBrains Junie | `.junie/AGENTS.md` |
| Amazon Q Developer | `.amazonq/rules/coding-standard.md` |
| Aider | `CONVENTIONS.md` + `.aider.conf.yml` |
| Manus | `MANUS/PROJECT_INSTRUCTIONS.md` + `MANUS/SKILL.md` |

> 지원은 해당 도구를 위한 adapter, instruction file, Skill 또는 문서화된 integration path를 제공한다는 의미입니다. 실제 도구 기능과 연동 방식은 client/version에 따라 달라질 수 있습니다.

### Manus

Manus는 일반적인 coding agent와 다른 integration model을 사용합니다. `MANUS/PROJECT_INSTRUCTIONS.md`를 Manus Project Instructions에 넣고 `MANUS/SKILL.md`를 Manus Skills에서 사용합니다.

```text
MANUS/
├── PROJECT_INSTRUCTIONS.md
├── SKILL.md
└── README.md
```

## 🐍 지원하는 개발 환경

AI Engineering Standard는 로컬 Python 개발, interactive notebook, cloud notebook, AI-assisted IDE workflow를 함께 지원합니다.

| 환경 / 도구 | 지원 | 주요 용도 |
|---|---|---|
| 🐍 **Python** | ✅ Core | 환경 감지, 설정, training, inference, validation, automation |
| 📓 **Jupyter Notebook** | ✅ Supported | 실험, 분석, training, debugging, 재현 가능한 notebook workflow |
| ☁️ **Google Colab** | ✅ Validated | cloud Python/Jupyter, resource-aware experiment, GPU/accelerator workflow |
| 💻 **Visual Studio Code** | ✅ Supported | Python 개발, Jupyter, debugging, testing, AI-assisted development |
| 🧪 **VS Code + Jupyter** | ✅ Supported | notebook 편집/실행, Python interactive workflow, remote Jupyter |

지원 범위는 AI-agent adapter와 별개로, 해당 환경에서 standard의 rules, installer, runtime detection, validation 및 documented workflow를 사용할 수 있음을 의미합니다.

## 📦 설치 도메인

```text
common = Common만
llm    = Common + LLM
vision = Common + Vision
all    = Common + LLM + Vision
```

Common은 모든 프로젝트에 적용되는 기본 규칙입니다. LLM과 Vision은 작업 도메인에 맞는 Agent, Skill, Environment, 설정 및 Smoke Test를 추가합니다.

## 🧭 AI Engineering Workflow

```text
Load project instructions
        ↓
Detect installed domains
        ↓
Inspect repository and workload
        ↓
Measure runtime capabilities/resources
        ↓
Resolve runtime configuration
        ↓
Run domain-appropriate Memory Smoke Test
        ↓
Lock validated environment
        ↓
Apply task-specific Skills
        ↓
Implement / Train / Infer
        ↓
Validate / Early Stop / Checkpoint
        ↓
Ablation / Experiment Metadata
        ↓
Final clean run
```

## 🧠 실행 환경 최적화

환경은 특정 장비를 전제로 하지 않습니다. 실제 실행 환경을 측정하고 workload에 맞는 설정을 계산합니다.

CPU, RAM, GPU/accelerator, VRAM, disk, CUDA/ROCm/MPS/DirectML, FP16/BF16 capability와 Jupyter/Colab 상태 등을 확인하고 보수적인 시작 설정을 선택합니다.

`COMMON/environment.py`를 공통 environment source로 사용하며 LLM과 Vision은 이를 기반으로 adapter/policy를 제공합니다.

## 🧪 학습 / 실험

장시간 학습에는 validation, Early Stopping, best Checkpoint, Resume, Ablation Study, seed control, resource tracking, 환경/설정 metadata와 단계적 recovery를 적용합니다.

```text
LLM/config/training.yaml
LLM/config/ablation.yaml
VISION/config/training.yaml
VISION/config/ablation.yaml
```

실험 기록에는 environment profile, Git 상태, configuration hash, seed, model/dataset revision, metric, runtime, peak RAM/VRAM, checkpoint를 포함하는 것을 권장합니다.

## 🧪 플랫폼 및 검증

GitHub Actions는 실제 `windows-latest` runner에서 Windows PowerShell과 PowerShell 7을 사용해 영문/한글 및 Common/LLM/Vision/All 설치를 검증합니다. Dry-run, Merge, Unicode/공백 경로도 테스트합니다.

Google Colab용 검증 Notebook도 제공합니다.

[Colab 검증 Notebook 열기](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)

검증 명령:

```bash
python scripts/validate.py
python scripts/check_i18n.py
python scripts/test_installers.py
```

LLM/Vision workload에서는 장시간 training 전에 해당 Memory Smoke Test를 실행합니다.

## 📚 문서

- [영문 설치 가이드](INSTALL.md)
- [한글 설치 가이드](i18n/ko/INSTALL.md)
- [Common Agent](COMMON/AGENT.md)
- [LLM Agent](LLM/AGENT.md)
- [LLM Skill](LLM/SKILL.md)
- [LLM Environment](LLM/ENVIRONMENT.md)
- [Vision Agent](VISION/AGENT.md)
- [Vision Skill](VISION/SKILL.md)
- [Vision Environment](VISION/ENVIRONMENT.md)
- [Manus 연동](MANUS/README.md)
- [Colab 검증](tests/colab/README.md)

## 📄 라이선스

이 프로젝트는 [MIT License](LICENSE)로 배포됩니다.
