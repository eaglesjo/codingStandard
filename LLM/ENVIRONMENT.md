# LLM Environment Profile & Optimization

`LLM/environment.py`와 함께 사용하는 실행환경 최적화 규칙이다.

## 1. 실행 원칙

AI Agent는 코드를 작성하기 전에 실제 실행 환경을 확인하고, 측정 결과로 runtime configuration을 결정한다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

## 2. 프로파일러 실행

```bash
python LLM/environment.py
```

resolved profile 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 3. 측정 대상

프로파일러는 가능한 범위에서 다음을 확인한다.

- Windows / Linux / macOS
- Python version / executable
- IDE / Jupyter / Colab
- CPU core count
- System RAM total / available
- GPU name
- VRAM total / free
- CUDA / MPS availability
- resolved device

## 4. 자동 결정 대상

환경과 가용 자원을 기준으로 다음의 보수적인 시작값을 계산한다.

- device
- batch size
- gradient accumulation steps
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

프로파일러 결과는 시작점이며 실제 모델/데이터의 peak memory를 보장하지 않는다.

## 5. Environment Lock

프로파일이 확정되면 학습/추론 전체에서 같은 resolved configuration을 재사용한다.

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

각 cell에서 device, worker 수, precision 등을 다시 임의로 판단하지 않는다.

## 6. 환경 중립성

특정 GPU, VRAM, RAM, OS, IDE를 기본 실행 조건으로 고정하지 않는다.

특정 개발 장비의 과거 설정을 보존할 필요가 있으면 별도의 backup/reference 문서에만 저장한다. backup/reference 문서는 runtime decision에 사용하지 않는다.

## 7. 환경 확정 후 코드 정리

환경이 하나로 확정된 프로젝트의 실행 코드에서는 사용하지 않는 OS/device branch를 제거한다.

예:

```text
Detect
 ↓
Measure
 ↓
Resolve
 ↓
Smoke Test
 ↓
Lock
 ↓
Remove unused branches
 ↓
Execute
```

단, 여러 플랫폼을 공식 지원하는 reusable library는 필요한 분기를 유지하고 detection과 execution을 분리한다.

## 8. Resource Optimization

실제 측정값과 workload를 기준으로 다음 순서로 자원 사용량을 완화하거나 확장한다.

```text
batch size
→ sequence/input size
→ gradient accumulation
→ mixed precision
→ checkpointing
→ quantization/offload 검토
```

CPU/RAM:

```text
worker 수 최소값부터 시작
→ prefetch 과다 설정 방지
→ persistent workers 필요성 검토
→ dataset 중복 복제 방지
→ streaming/chunking/memory mapping 검토
→ CPU thread 과다 증가 방지
```

가용 VRAM/RAM을 100%까지 사용하지 않는다.

## 9. Smoke Test

본 학습 전에 최소 workload로 다음을 검증한다.

```text
load → forward → backward → optimizer step → validation → checkpoint
```

다음 정보를 기록한다.

```text
resolved environment profile
runtime configuration
peak VRAM
peak RAM
loss / validation metric
runtime
```

실패하면 본 학습을 시작하지 않고 configuration을 낮춘 뒤 다시 검증한다.

## 10. OOM Recovery

OOM 발생 시 같은 configuration을 반복하지 않고 다음 순서로 완화한다.

```text
VRAM/RAM 기록
→ batch ↓
→ sequence/input ↓
→ workers ↓
→ AMP 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 성공 configuration으로 실행
```

## 11. 결과 기록

장시간 실험에는 다음을 함께 기록한다.

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
seed
model revision
dataset revision
```
