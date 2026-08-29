# Vision 실행환경 최적화

비전 작업에서는 이미지 해상도, 채널, 배치, feature-map/activation 메모리, 이미지 디코드/augmentation worker, cache, prefetch가 주요 자원 변수입니다.

```text
해상도 ↓
→ batch ↓
→ worker/prefetch/cache ↓
→ mixed precision
→ checkpointing
→ gradient accumulation
→ model/optimizer memory reduction
→ tiling/cropping/offload
```

장시간 학습 전 대표 이미지 크기와 배치로 `load → preprocess → forward → backward → optimizer → validation → checkpoint` 흐름을 검증하고 peak VRAM/RAM 및 throughput을 기록합니다.

특정 GPU, CPU, RAM, OS, framework 버전을 가정하지 않고 실제 환경 profile과 workload 요구사항을 기준으로 결정합니다.
