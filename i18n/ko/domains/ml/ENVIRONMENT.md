# ML 실행환경 계약

실제 실행 runtime을 source of truth로 사용합니다. 특정 기계 이름은 prerequisite가 아닙니다.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

가능하면 OS/architecture, Python, framework/accelerator capability, CPU/RAM/disk, GPU/VRAM, Jupyter/VS Code/Colab 상태를 측정합니다.

측정 결과와 workload에 따라 device, batch size, input/sequence size, workers/prefetch, precision, cache, checkpoint frequency를 보수적으로 결정합니다.

Linux는 지원 OS 계열이며 Ubuntu 24.04 LTS는 CI reference입니다. Colab은 client OS가 아니라 실행 중인 Python runtime 기준의 ephemeral cloud Linux 환경으로 분류합니다.

대표 smoke test가 통과하면 profile/configuration을 실험과 함께 저장하고 같은 run에서 재사용합니다.