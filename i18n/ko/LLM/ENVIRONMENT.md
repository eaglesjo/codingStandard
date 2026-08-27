# LLM 실행환경 프로파일 및 최적화

`LLM/environment.py`를 사용해 실제 실행환경을 측정하고 workload에 맞는 안전한 runtime configuration을 결정합니다.

## 1. 기본 원칙

특정 PC, GPU, VRAM, RAM, OS, IDE를 실행 전제조건으로 고정하지 않습니다. 항상 현재 실행환경의 실측값을 기준으로 최적화합니다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

## 2. 프로파일러 실행

```bash
python LLM/environment.py
python LLM/environment.py .codingstandard/environment-profile.json
```

가능한 측정 항목:

- OS / architecture
- Python version / executable
- IDE / Jupyter / Colab
- CPU core count
- System RAM total / available
- GPU name / VRAM total / free
- CUDA / MPS availability
- resolved device

## 3. Runtime Configuration

프로파일러는 실제 자원과 workload를 기준으로 다음 설정의 보수적인 시작값을 계산합니다.

- device
- batch size
- gradient accumulation steps
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

이 설정은 고정값이 아닙니다. 실제 Memory Smoke Test 결과에 따라 조정합니다.

## 4. Environment Lock

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

환경이 검증되면 해당 profile과 runtime configuration을 학습/추론 전체에서 재사용합니다.

각 cell 또는 함수에서 device, worker, precision을 다시 임의 결정하지 않습니다.

## 5. 환경 확정 후 코드 정리

```text
Detect
→ Measure
→ Resolve
→ Smoke Test
→ Lock
→ 미사용 branch 제거
→ 실행
```

환경이 확정된 애플리케이션/Notebook에서는 사용하지 않는 OS/device branch, 중복 detection, dead code, 구식 import를 삭제합니다.

단, 여러 플랫폼을 공식 지원하는 reusable library는 필요한 branch를 유지합니다.

## 6. GPU 최적화

실제 free VRAM과 workload를 기준으로 다음 순서를 검토합니다.

```text
batch size ↓
sequence/input size ↓
gradient accumulation
mixed precision
gradient checkpointing
quantization
optimizer memory reduction / offload
tensor/reference 정리
```

VRAM을 100%까지 채우지 않고 runtime 및 다른 CUDA allocation을 위한 여유를 남깁니다.

## 7. CPU / RAM 최적화

```text
대용량 dataset 불필요한 전체 적재 금지
streaming / chunking / memory mapping
DataLoader worker 보수적 시작
prefetch / persistent worker 과다 사용 금지
DataFrame/list/tensor 중복 복사 금지
CPU/BLAS/OpenMP thread 제어
```

RAM 역시 OS, IDE, runtime 및 기타 프로세스를 위한 여유를 남깁니다.

## 8. Memory Smoke Test

장시간 학습 전에 대표 workload를 작은 규모로 검증합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

기록:

- peak VRAM
- peak RAM
- validation metric
- runtime
- resolved environment profile

Smoke Test가 실패하면 본 학습을 시작하지 않고 runtime configuration을 낮춘 뒤 재검증합니다.

## 9. OOM Recovery

```text
실패 내용과 메모리 기록
→ batch 감소
→ sequence/input 감소
→ workers 감소
→ precision 확인
→ checkpointing 검토
→ quantization/offload 검토
→ smoke test
→ 성공한 설정으로 실행
```

동일한 실패 configuration을 무한 반복하지 않습니다.

## 10. 결과 기록

장시간 실험에는 다음을 함께 저장합니다.

```text
environment profile
runtime configuration
device
gpu / accelerator
VRAM / RAM
CPU count
peak VRAM
peak RAM
runtime
```
