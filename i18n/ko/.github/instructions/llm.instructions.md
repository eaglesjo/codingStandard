---
applyTo: "**/*.py,**/*.ipynb,**/notebooks/**,**/training/**,**/experiments/**"
---

# LLM/ML 경로별 지침

- 실제 Python kernel과 실행환경을 먼저 확인합니다.
- 가능하면 `python LLM/environment.py`를 실행합니다.
- VRAM/RAM/CPU 실측값으로 runtime configuration을 정합니다.
- Memory Smoke Test를 통과하기 전 장시간 학습을 시작하지 않습니다.
- 환경이 확정되면 사용하지 않는 OS/device branch와 dead code를 제거합니다.
- 제한된 자원에서는 batch 축소, gradient accumulation, mixed precision, checkpointing, quantization/offload, worker 조절을 순차 검토합니다.
- 장시간 학습에는 validation metric, Early Stopping, best checkpoint, Resume을 적용합니다.
- Ablation Study는 명시적 matrix로 관리하고 동일 평가 조건과 seed를 유지합니다.
- metric, runtime, peak VRAM/RAM, resolved environment profile을 기록합니다.
