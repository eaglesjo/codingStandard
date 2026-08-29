# Python / LLM / Jupyter AI Agent 개발 규칙

이 문서는 Python 기반 LLM/ML, Jupyter, VS Code Jupyter, Google Colab 작업에 적용합니다.

## 핵심 원칙

- 실제 실행환경을 먼저 확인합니다.
- 활성 Python kernel과 프로젝트 dependency를 기준으로 작업합니다.
- OS별 경로는 `pathlib.Path`를 사용합니다.
- GPU/특정 OS/특정 패키지를 존재한다고 가정하지 않습니다.
- VRAM/RAM을 먼저 측정하고 workload에 맞는 자원 설정을 결정합니다.
- 장시간 학습에는 validation, Early Stopping, best checkpoint, Resume을 적용합니다.
- 실험은 명시적인 configuration과 Ablation Study matrix로 관리합니다.

## 환경 최적화 흐름

```text
환경 탐지
→ 자원 측정
→ Runtime Profile 계산
→ Memory Smoke Test
→ Environment Lock
→ 미사용 branch 제거
→ 최적화된 실행
```

`LLM/environment.py`를 우선 사용합니다.

```bash
python LLM/environment.py
```

환경이 확정된 실행 코드에는 실제 사용하는 device/dtype/worker/batch 경로만 남깁니다. 여러 플랫폼을 공식 지원하는 재사용 library는 detection과 execution을 분리합니다.

## 메모리 안전

- batch size를 무리하게 키우지 않습니다.
- 필요하면 gradient accumulation을 사용합니다.
- 지원되는 accelerator에서는 mixed precision을 검토합니다.
- 필요 시 gradient checkpointing, quantization, CPU offload를 검토합니다.
- DataLoader worker와 prefetch를 제한합니다.
- 대용량 데이터를 무조건 RAM에 적재하지 않습니다.
- inference/evaluation에서는 `torch.inference_mode()`를 사용합니다.
- OOM 발생 시 단계별 recovery를 적용하고 동일 설정을 무한 재시도하지 않습니다.

## Notebook

새 Notebook은 다음 순서를 권장합니다.

```text
목적
→ Environment Detection
→ Hardware / Memory Detection
→ Runtime Configuration
→ Environment Lock
→ Dependency
→ Data
→ Model
→ Training / Inference
→ Evaluation
→ Ablation
→ Reproducibility
```

clean kernel에서 Run All이 가능해야 합니다.

## 학습

- validation split/eval dataset을 사용합니다.
- metric과 방향을 명시합니다.
- Early Stopping patience와 최소 개선량을 설정합니다.
- best checkpoint를 저장하고 복원합니다.
- Resume 가능한 checkpoint를 유지합니다.

## Ablation

baseline과 variant를 명시적으로 정의합니다. 가능하면 data split, evaluation set, metric, Early Stopping, budget, seed를 동일하게 유지합니다.

결과에는 metric뿐 아니라 runtime, peak VRAM/RAM, configuration, seed, model/dataset revision, resolved environment profile을 기록합니다.
