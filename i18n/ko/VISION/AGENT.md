# Vision AI Agent 규칙

이미지 분류, 검출, 세그멘테이션, OCR, 자세 추정, 이미지 생성, VLM 작업에 적용합니다.

1. 실제 실행환경을 먼저 측정합니다.
2. 특정 GPU/CPU/RAM/OS를 전제로 하드코딩하지 않습니다.
3. 이미지 해상도, 채널, 배치, feature-map/activation 메모리, augmentation worker, cache, prefetch를 주요 자원 변수로 관리합니다.
4. 장시간 학습 전에 대표 입력으로 Memory Smoke Test를 실행합니다.
5. validation, Early Stopping, best checkpoint, Resume을 기본 적용합니다.
6. baseline과 통제된 ablation variant를 명시적으로 정의합니다.
7. 이미지 크기, seed, model/dataset revision, metric, runtime, peak VRAM/RAM, environment profile을 기록합니다.
8. 환경 확정 후 불필요한 실행 branch와 dead code를 제거합니다.
9. lazy loading, streaming, bounded cache, 보수적 worker를 우선합니다.
10. 메모리 실패 시 해상도/배치/worker부터 단계적으로 낮추고 동일 실패 설정을 무한 반복하지 않습니다.
