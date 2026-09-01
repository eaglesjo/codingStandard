# Vision 실행환경 계약

공통 `core/common/environment.py` 프로파일러를 실제 실행환경과 자원 설정의 source of truth로 사용합니다.

Vision에서는 이미지/영상 resolution, channels, batch, activation/feature-map memory, decode/augmentation workers, cache, prefetch를 주요 resource variable로 취급합니다.

```text
Detect → Measure → Resolve → Vision Smoke Test → Lock → Optimize → Execute
```

장시간 학습 전 대표 workload로 다음을 검증합니다.

```text
load → preprocess → forward → backward → optimizer → validation → checkpoint
```

특정 GPU, CPU, RAM, OS, framework version을 prerequisite로 고정하지 않습니다. Colab이면 `platform/colab/`의 ephemeral runtime 정책도 적용합니다.