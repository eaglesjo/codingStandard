---
applyTo: "**/*.py,**/*.ipynb,**/notebooks/**,**/training/**,**/train/**,**/ml/**"
---
# LLM / ML Task Instructions

@../../AGENTS.md
@../../LLM/AGENT.md
@../../LLM/SKILL.md
@../../LLM/ENVIRONMENT.md

이 경로에서 Python/LLM/ML 코드를 수정할 때는 다음을 우선한다.

- 코드 작성 전에 가능하면 `python LLM/environment.py`로 실제 실행환경을 측정한다.
- OS, IDE/runtime, Python, CPU, GPU, VRAM, RAM을 기준으로 resolved runtime configuration을 만든다.
- Memory Smoke Test로 권장 설정을 검증한 뒤 학습/추론에 적용한다.
- Environment Lock 이후 매 cell에서 환경을 다시 판단하지 않고 확정된 configuration을 재사용한다.
- 확정된 환경에서 사용하지 않는 OS/device branch와 dead code를 정리한다.
- 4GB VRAM / 16GB RAM 환경에서는 memory budget을 우선한다.
- 학습에는 validation, Early Stopping, best checkpoint, Resume를 적용한다.
- Ablation Study는 configuration matrix 기반으로 반복 가능하게 만든다.
- 결과에 resolved environment profile과 peak VRAM/RAM/runtime을 기록한다.
