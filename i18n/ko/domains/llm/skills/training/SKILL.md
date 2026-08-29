# 학습 Skill

모델 학습 및 파인튜닝 작업에 사용합니다.

학습 설정은 고정된 하드웨어 가정이 아니라 확정된 환경 프로파일을 사용해야 합니다.

장시간 학습 필수 항목:

- validation dataset 및 명시적인 primary metric
- metric, 방향, patience, 최소 개선량을 가진 Early Stopping
- best checkpoint 저장 및 복원
- 중단 후 Resume 가능한 상태 저장
- peak VRAM/RAM 및 runtime 기록

본 학습 전에 model load, forward, backward, optimizer step, validation, checkpoint save를 포함하는 Memory Smoke Test를 수행합니다.

OOM 발생 시 단계적으로 자원 요구량을 낮추고 smoke test를 반복합니다. 동일한 실패 설정을 무한 재시도하지 않습니다.
