# 환경 최적화 Skill

실행환경 확인, 하드웨어 프로파일링, runtime 최적화 작업에 사용합니다.

## 작업 흐름

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize → Execute
```

가능하면 `python LLM/environment.py`를 실행하고 실제 capability 측정값을 source of truth로 사용합니다.

CPU, RAM, disk, accelerator, VRAM, CUDA/MPS/ROCm/DirectML, Python/runtime, IDE/Jupyter/Colab 상태를 확인합니다.

device, batch size, gradient accumulation, worker, pin memory, mixed precision, checkpointing, input length에 대한 보수적인 설정을 결정합니다.

장시간 학습 전 대표 workload로 Memory Smoke Test를 수행하고 실패하면 자원 요구량을 낮춘 후 다시 검증합니다.

Environment Lock 이후 애플리케이션/Notebook에서 사용하지 않는 실행 branch를 제거합니다. 여러 플랫폼을 공식 지원하는 reusable library는 필요한 branch를 유지합니다.
