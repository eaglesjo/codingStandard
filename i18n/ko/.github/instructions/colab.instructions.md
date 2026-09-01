---
applyTo: "**/*.ipynb"
---
# Notebook Runtime 지침

실행 중인 Python runtime이 Google Colab 또는 ephemeral hosted notebook이면 `platform/colab/AGENT.md`와 `platform/colab/SKILL.md`를 추가 적용합니다.

client OS가 아닌 실제 kernel/runtime으로 Colab 여부를 감지합니다. Colab 작업은 runtime reset/interruption을 전제로 reproducible dependency bootstrap, resource measurement, smoke test, durable checkpoint/artifact, Resume 검증을 적용합니다.

일반 Jupyter라면 공통 notebook/ML 규칙을 적용하고 Colab 전용 persistence 정책은 강제하지 않습니다.