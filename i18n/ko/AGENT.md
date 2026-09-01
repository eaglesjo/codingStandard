# 한국어 AI Agent 공통 규칙

이 파일은 한국어 배포 환경의 보조 Agent entrypoint입니다. 정책의 원본은 `AGENTS.md`와 `core/common/`입니다.

적용 순서:

```text
AGENTS.md
→ core/common/
→ domains/ml/ + 관련 LLM/Vision domain
→ Colab이면 platform/colab/
→ task-specific Skills
```

일반 ML/DL에서는 Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps lifecycle을 적용합니다.

실제 Python/runtime과 CPU/RAM/disk/accelerator/VRAM을 측정하고 smoke test 후 configuration을 lock합니다. 장시간 학습에는 validation, best checkpoint, Resume, 필요한 경우 Early Stopping을 적용합니다.

Notebook은 fresh kernel/runtime에서 top-to-bottom 실행 가능해야 합니다. Colab은 ephemeral runtime으로 취급하고 durable checkpoint/artifact 및 Resume 검증을 사용합니다.
