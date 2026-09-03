# ML/DL 런타임 검증

이 문서는 `codingStandard` 설치 후 실제 실행 계약을 검증합니다.

## Agent 라우팅

저장소 루트에서 실행합니다.

```bash
python scripts/validation/validate_agent_routing.py
```

검증 대상은 네 가지 대표 요청입니다.

- 일반 PyTorch 학습 → common + ML lifecycle
- LLM QLoRA → common + ML + LLM fine-tuning/PEFT/quantization
- Vision detection → common + ML + Vision detection/evaluation
- Colab LLM training → common + ML + LLM + Colab checkpoint/resume 정책

또한 최소 시나리오에서 관계없는 도메인이 우발적으로 포함되지 않는지 확인합니다.

## Colab runtime

새 Colab runtime에서 `examples/colab/clean_runtime_validation.ipynb`를 열고 처음부터 끝까지 모든 셀을 실행합니다.

Notebook은 다음을 수행해야 합니다.

1. 활성 Python kernel과 실행 환경 식별
2. 가능한 경우 accelerator, RAM, disk 특성 보고
3. Agent routing 계약 테스트 실행
4. PyTorch가 있으면 작은 forward/backward smoke test 실행
5. 선택한 영속 디렉터리에 checkpoint 저장 및 복원
6. machine-readable runtime report 생성

Checkpoint를 Colab reset 이후에도 유지해야 한다면 연결된 영속 저장 위치를 사용합니다. Notebook VM 파일 시스템은 폐기 가능한 것으로 취급해야 합니다.

## 해석

검증 성공은 설치된 정책을 탐색할 수 있고, 선택한 runtime을 측정할 수 있으며, 대표 workload를 안전하게 시작하고 recovery artifact를 복원할 수 있음을 의미합니다. 모든 Colab accelerator 종류나 모든 모델 크기가 테스트되었다는 뜻은 아닙니다.
