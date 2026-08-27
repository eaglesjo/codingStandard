---
applyTo: "**/*.py,**/*.ipynb,**/notebooks/**,**/training/**,**/train/**,**/ml/**"
---
# LLM / ML Task Instructions

@../../AGENTS.md
@../../LLM/AGENT.md
@../../LLM/SKILL.md

이 경로에서 Python/LLM/ML 코드를 수정할 때는 다음을 우선한다.

- 실제 실행 환경을 확인하고 Environment Profile을 확정한다.
- 확정 후 사용하지 않는 OS/device 분기와 dead code를 정리한다.
- 4GB VRAM / 16GB RAM 환경에서는 memory budget을 우선한다.
- 학습에는 validation, Early Stopping, best checkpoint, Resume를 적용한다.
- Ablation Study는 configuration matrix 기반으로 반복 가능하게 만든다.
