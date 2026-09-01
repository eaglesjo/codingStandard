# LLM 실행환경 계약

공통 `core/common/environment.py` 프로파일러를 실제 실행환경과 자원 설정의 source of truth로 사용합니다.

```bash
python core/common/environment.py
python core/common/environment.py .codingstandard/environment-profile.json
```

## LLM resource controls

```text
model size
context length
batch size
gradient accumulation
precision
KV/cache behavior
gradient checkpointing
quantization/offload
```

VRAM/RAM과 workload를 측정해 보수적으로 설정하고, representative load/forward/backward smoke test를 장시간 학습의 gate로 사용합니다.

환경이 확정되면 같은 run에서 resolved device, workers, precision, batch configuration을 재사용하며 각 cell에서 독립적으로 재탐지하지 않습니다.

## Colab

Google Colab이면 `platform/colab/AGENT.md`와 `platform/colab/SKILL.md`를 추가 적용합니다. Runtime reset/interruption을 전제로 durable checkpoint/artifact와 Resume 검증을 사용합니다.