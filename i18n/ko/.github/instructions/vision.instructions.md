---
applyTo: "**/VISION/**,**/vision/**,**/cv/**,**/ocr/**,**/detection/**,**/segmentation/**"
---
# Vision / Computer Vision 작업 지침

@../../AGENTS.md

Vision 작업에서는 설치된 `VISION/AGENT.md`, `VISION/SKILL.md`, `VISION/ENVIRONMENT.md`를 적용합니다.

자원에 민감한 작업 전 다음을 수행합니다.

- 실제 Python/runtime, CPU, RAM, accelerator, VRAM, disk 측정
- 이미지 해상도, 채널, batch, activation/feature-map 메모리, worker, cache, prefetch 고려
- 대표 입력을 이용한 Vision Memory Smoke Test 실행
- 장시간 학습 전 검증된 configuration 고정

특정 장비나 고정 자원 용량을 하드코딩하지 않습니다. 환경 확정 후 미사용 실행 branch와 obsolete code를 제거합니다.

학습에는 validation, Early Stopping, best Checkpoint, Resume, 통제된 Ablation Study, 재현성/자원 사용량 기록을 적용합니다.
