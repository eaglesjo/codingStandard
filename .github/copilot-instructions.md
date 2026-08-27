# Repository-wide Copilot Instructions

이 파일은 GitHub Copilot이 저장소 전체에서 자동 적용할 공통 지침이다.

@../AGENTS.md
@../LLM/AGENT.md
@../LLM/SKILL.md

반드시 실제 작업 환경을 먼저 확인하고, 환경이 확정되면 사용하지 않는 OS/device 실행 경로를 제거한다.

Python/LLM/ML 작업에서는 다음을 기본 적용한다.
- Windows + VS Code + RTX 3050 Ti 4GB + RAM 16GB를 보수적인 로컬 기본 프로파일로 사용한다.
- VRAM/RAM을 측정하고 batch size, sequence length, workers 등을 자원에 맞게 설정한다.
- 학습에는 validation metric, Early Stopping, best checkpoint, Resume를 적용한다.
- Ablation Study는 명시적 configuration matrix와 동일한 평가 기준으로 실행한다.
- 결과에는 metric뿐 아니라 seed, model/dataset revision, runtime, peak VRAM/RAM, early-stopped 여부를 기록한다.
