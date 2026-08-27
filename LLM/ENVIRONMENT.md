# LLM Environment Profile & Optimization

`LLM/environment.py`와 함께 사용하는 실행환경 최적화 규칙이다.

## 실행 원칙

AI Agent는 코드를 작성하기 전에 실제 실행 환경을 확인하고, 측정 결과로 runtime configuration을 결정한다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

## 프로파일러 실행

```bash
python LLM/environment.py
```

resolved profile을 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 측정 대상

- Windows/Linux/macOS
- Python version / executable
- IDE / Jupyter / Colab
- CPU core count
- System RAM total / available
- NVIDIA GPU / VRAM total / free
- CUDA / MPS availability
- resolved device

## 자동 결정 대상

프로파일러는 보수적인 시작값을 계산한다.

- device
- batch size
- gradient accumulation steps
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

모델의 실제 peak memory를 알 수 없으므로 권장값은 시작점으로만 사용한다.

## Environment Lock

프로파일이 확정되면 아래 값을 학습/추론 전체에서 재사용한다.

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

각 cell에서 다시 device나 worker 수를 자동 결정하지 않는다.

## 현재 실행환경에 맞춘 코드 정리

환경이 하나로 확정된 프로젝트의 실행 코드에서는 사용하지 않는 branch를 제거한다.

예: Windows + CUDA 확정 후 CPU/MPS 전용 실행 코드를 유지하지 않는다.

단, 여러 플랫폼을 공식 지원하는 재사용 library는 분기를 유지하고 detection과 execution을 분리한다.

## 4GB VRAM / 16GB RAM 로컬 프로파일

기본 시작값:

```text
batch_size = 1
num_workers = 0
FP16 = on for CUDA when supported
gradient accumulation = use instead of large batch
sequence length = conservative
checkpointing = consider for low VRAM
```

VRAM과 RAM을 100% 사용하지 않는다.

## Smoke Test

본 학습 전 최소 workload로 다음을 검증한다.

```text
load → forward → backward → optimizer step → validation → checkpoint
```

peak VRAM/RAM을 기록하고 실패하면 configuration을 낮춘다.

## OOM Recovery

```text
VRAM/RAM 기록
→ batch ↓
→ input/sequence ↓
→ workers ↓
→ AMP 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 학습
```

같은 configuration을 무한 재시도하지 않는다.

## 결과 기록

모든 장시간 실험에는 resolved environment profile을 함께 기록한다.

```text
environment profile
runtime configuration
device
gpu name / VRAM
RAM available
CPU count
peak VRAM
peak RAM
runtime
```
