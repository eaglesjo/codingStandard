# Vision AI Skill

이미지 기반 AI 구현·학습·추론·평가에 사용합니다.

환경 확인 → 가속기/메모리 측정 → 이미지 크기/배치 설정 → 데이터 파이프라인 설정 → Memory Smoke Test → Environment Lock → 구현/학습 → 평가 → Early Stopping/Checkpoint → Ablation → 자원/재현성 기록 순으로 작업합니다.

분류/검출/세그멘테이션/OCR/자세 추정/이미지 생성/VLM별 전용 Skill을 우선 적용합니다. 이미지 해상도와 feature-map 메모리를 주요 자원 변수로 취급하며 worker, prefetch, cache를 보수적으로 시작합니다.
