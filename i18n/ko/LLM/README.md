# LLM Coding Standard

Python / LLM / ML / Jupyter 개발에 사용하는 한국어 표준입니다.

## 구성

- `AGENT.md` — AI Agent 개발 규칙
- `SKILL.md` — 실제 작업 절차
- `ENVIRONMENT.md` — 실행환경 확인 및 최적화
- `environment.py` — 실행환경 프로파일러

## 실행환경 확인

```bash
python LLM/environment.py
python LLM/environment.py .codingstandard/environment-profile.json
```

실제 OS, Python, IDE/runtime, CPU, RAM, GPU, VRAM, CUDA/MPS를 측정하고 workload에 맞는 runtime configuration을 계산합니다.

## 작업 흐름

```text
AI instruction 자동 로딩
→ 프로젝트 분석
→ 실행환경 측정
→ Runtime Configuration
→ Memory Smoke Test
→ Environment Lock
→ 미사용 branch 제거
→ 구현 / 학습 / 추론
→ Evaluation / Early Stopping / Checkpoint
→ Ablation / Resource 기록
→ Clean Run
```

## 메모리 최적화

제한된 자원에서는 batch와 input을 줄이고 gradient accumulation, mixed precision, gradient checkpointing, quantization, offload, worker/prefetch 조절 등을 순차 검토합니다.

VRAM/RAM을 100%까지 사용하지 않으며 OOM이 발생하면 단계별 recovery를 적용합니다.

## 학습

장시간 학습에는 validation metric과 Early Stopping을 기본 적용하고 best checkpoint와 Resume 가능한 checkpoint를 유지합니다.

## Ablation Study

baseline과 variant를 명시적인 configuration matrix로 관리하고, 가능한 한 동일한 split, metric, budget, seed 및 환경 조건에서 비교합니다.

결과에는 metric뿐 아니라 runtime, peak VRAM/RAM, configuration, seed, model/dataset revision, environment profile을 기록합니다.
