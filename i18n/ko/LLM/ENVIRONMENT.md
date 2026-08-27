# LLM 실행환경 프로파일 및 최적화

`LLM/environment.py`를 사용해 실제 실행환경을 측정하고 workload에 맞는 안전한 runtime configuration을 결정합니다.

## 기본 흐름

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

## 프로파일러

```bash
python LLM/environment.py
python LLM/environment.py .codingstandard/environment-profile.json
```

측정 항목:

- OS / architecture
- Python / executable
- IDE / Jupyter / Colab
- CPU
- System RAM total / available
- GPU / VRAM total / free
- CUDA / MPS
- resolved device

자동 결정 항목:

- device
- batch size
- gradient accumulation
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

권장값은 시작점이며 실제 workload별 Memory Smoke Test 결과가 최종 결정입니다.

## Environment Lock

프로파일 확정 후 학습/추론 전체에서 동일한 resolved configuration을 재사용합니다.

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

확정된 실행환경에서는 사용하지 않는 OS/device branch, dead code, 구식 import를 제거합니다. 여러 플랫폼을 공식 지원하는 library는 필요한 분기를 유지합니다.

## 메모리 최적화

VRAM:

```text
batch ↓
sequence/input ↓
gradient accumulation
mixed precision
gradient checkpointing
quantization 검토
offload 검토
tensor/reference 정리
```

RAM/CPU:

```text
전체 dataset RAM 적재 금지
streaming/chunking/memory mapping
worker 수 제한
prefetch 과다 사용 금지
중복 복사 방지
CPU thread 제한
```

VRAM/RAM을 100%까지 사용하지 않습니다.

## Memory Smoke Test

본 학습 전 다음을 작은 workload로 검증합니다.

```text
load → forward → backward → optimizer step → validation → checkpoint
```

peak VRAM, peak RAM, loss, runtime을 기록합니다. 실패하면 resource configuration을 낮춘 뒤 다시 검증합니다.

## OOM Recovery

```text
VRAM/RAM 기록
→ batch 감소
→ input/sequence 감소
→ workers 감소
→ mixed precision 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 재실행
```

동일 configuration을 무한 반복하지 않습니다.

## 결과 기록

장시간 실험에는 environment profile, runtime configuration, device, GPU/VRAM, RAM, CPU, peak VRAM/RAM, runtime을 함께 기록합니다.
