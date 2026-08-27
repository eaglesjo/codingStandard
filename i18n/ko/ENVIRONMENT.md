# LLM 실행환경 프로파일 및 최적화

실제 실행환경을 측정하고 workload에 맞는 안전한 runtime configuration을 결정합니다.

## 기본 흐름

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

## 프로파일러

```bash
python LLM/environment.py
python LLM/environment.py .codingstandard/environment-profile.json
```

측정 대상:

- OS / architecture
- Python / executable
- IDE / Jupyter / Colab
- CPU
- System RAM
- Disk total / free
- GPU / accelerator / VRAM
- CUDA / MPS / ROCm / DirectML capability
- FP16 / BF16 지원 여부
- resolved device

자동 결정 대상:

- device
- batch size
- gradient accumulation
- DataLoader workers
- pin memory
- mixed precision
- gradient checkpointing
- maximum sequence length

## Environment Lock

검증된 profile과 runtime configuration을 학습/추론 전체에서 재사용합니다.

환경 확정 후 사용하지 않는 OS/device branch, 중복 detection, dead code, 구식 import를 제거합니다. 여러 플랫폼을 공식 지원하는 reusable library는 필요한 분기를 유지합니다.

## GPU / RAM 최적화

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

CPU/RAM은 streaming, chunking, memory mapping, 보수적인 worker, 제한된 prefetch, 중복 복사 방지, CPU thread 제한을 우선합니다.

## Memory Smoke Test

장시간 학습 전에 `LLM/memory_smoke_test.py`를 사용합니다.

```bash
python LLM/memory_smoke_test.py --cpu --steps 2
```

본 모델을 학습할 때는 실제 모델/configuration으로도 동일한 `load → forward → backward → optimizer step → validation → checkpoint save/reload` 흐름을 검증합니다.

## OOM Recovery

```text
memory 기록
→ batch 감소
→ input/sequence 감소
→ workers 감소
→ precision 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 검증된 설정 실행
```

동일한 실패 설정을 무한 반복하지 않습니다.

## Reproducibility

환경 profile, runtime configuration, device, accelerator, VRAM/RAM, CPU, peak memory, runtime, coding-standard version을 실험 결과와 함께 기록합니다.
