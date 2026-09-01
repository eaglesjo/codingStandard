# Google Colab Agent 규칙

실행 중인 Python runtime이 Google Colab 또는 다른 ephemeral hosted notebook runtime이면 적용합니다.

- browser/client OS가 아니라 실제 Python runtime으로 환경을 판별합니다.
- accelerator 종류, VRAM/RAM, disk, uptime은 동적으로 변할 수 있는 capability로 취급합니다.
- session interruption/reset을 전제로 long-running 작업을 Resume 가능하게 만듭니다.
- checkpoint, experiment metadata, 중요 artifact는 적절한 durable storage에 저장합니다.
- dependency는 active kernel에 재현 가능하게 설치하고 import를 검증합니다.
- dependency setup 후 environment profile과 대표 smoke test를 실행합니다.
- batch/input/workers/precision은 측정된 resource에 따라 보수적으로 결정합니다.
- notebook은 fresh runtime에서 top-to-bottom 실행 가능해야 합니다.

```text
Detect → Bootstrap → Measure → Resolve → Smoke Test
→ Lock → Checkpoint Policy → Execute → Persist → Resume Validate
```