# AGENT.md

# Cross-Platform Python LLM / Jupyter / Google Colab 개발 Agent 규칙

이 문서는 Python 기반 LLM/ML 프로젝트를 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 개발하는 AI coding agent를 위한 공통 규칙입니다.

## 1. 지원 범위

- Windows / Linux / macOS
- venv / virtualenv / conda / uv
- Jupyter / JupyterLab / VS Code Jupyter
- Google Colab / Colab Local Runtime
- CPU / CUDA / MPS
- 로컬 GPU 및 제한된 시스템 메모리 환경

## 2. 핵심 원칙

1. 실제 실행 환경을 먼저 확인합니다.
2. GPU, CPU, RAM, OS, Python, IDE/runtime을 하드코딩하지 않습니다.
3. 재사용 로직은 `src/` 또는 적절한 모듈로 분리하고 Notebook은 orchestration에 집중합니다.
4. 경로에는 `pathlib.Path`를 사용합니다.
5. 파일 encoding을 명시합니다.
6. Secret을 소스 코드에 넣지 않습니다.
7. 가용 VRAM/RAM을 측정하고 workload에 맞는 자원량을 결정합니다.
8. GPU/RAM 100% 사용을 목표로 하지 않습니다.
9. 동일한 OOM 설정을 반복하지 않습니다.
10. 실험 설정은 명시적인 configuration object/section으로 관리합니다.
11. 장시간 학습에는 validation metric, Early Stopping, Checkpoint/Resume을 기본 적용합니다.
12. 재현성 metadata와 자원 사용량을 기록합니다.

## 3. 환경 처리 계약

모든 환경 의존 작업은 다음 순서를 따릅니다.

```text
Detect
  ↓
Measure
  ↓
Resolve
  ↓
Smoke Test
  ↓
Environment Lock
  ↓
Optimize
  ↓
Implement / Execute
```

가능하면 공통 프로파일러를 먼저 실행합니다.

```bash
python LLM/environment.py
```

프로파일 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 4. Environment Profile

`LLM/environment.py`는 가능한 범위에서 다음을 측정합니다.

- OS / architecture
- Python version / executable
- IDE / Jupyter / Colab 상태
- CPU core count
- System RAM total / available
- NVIDIA GPU / VRAM total / free
- CUDA / MPS availability
- resolved device

측정 결과로 다음의 보수적인 시작 설정을 계산합니다.

- device
- batch size
- gradient accumulation steps
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

권장값은 시작점이며 실제 workload의 Memory Smoke Test가 최종 결정권을 가집니다.

## 5. 완전한 환경 중립성

특정 개발 장비나 개인 PC를 필수 실행 환경으로 문서화하지 않습니다. 모든 runtime 결정은 실제 측정값과 workload 요구사항을 기반으로 합니다.

## 6. Environment Lock

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

환경 검증 후에는 확정된 configuration을 학습/추론 전체에서 재사용합니다. 각 cell이나 함수에서 device/worker/precision을 다시 임의 결정하지 않습니다.

여러 플랫폼을 공식 지원하는 reusable library는 필요한 branch를 유지하되 detection과 execution을 분리합니다.

## 7. 환경 확정 후 코드 정리

환경이 확정된 애플리케이션/Notebook 실행 코드에서는 사용하지 않는 대체 경로를 삭제합니다.

삭제 대상:

- 사용하지 않는 CPU/CUDA/MPS 경로
- 중복 environment detection
- 주석 처리된 구식 구현
- 실패한 임시 실험 코드
- 사용하지 않는 import

여러 플랫폼을 공식 지원하는 reusable library의 필요한 branch는 유지합니다.

## 8. Notebook 표준 구조

1. 목적 Markdown
2. Environment Detection
3. Hardware / Memory Detection
4. Environment Profile Resolution
5. Environment Lock
6. UTF-8 / Path
7. Dependency Bootstrap
8. Imports
9. Resource Configuration
10. Experiment Configuration
11. Data
12. Model / Client
13. Training / Inference
14. Evaluation
15. Ablation
16. Visualization
17. Export
18. Reproducibility Metadata

새 Notebook은 fresh kernel/runtime에서 top-to-bottom 실행 가능해야 합니다.

## 9. Dependency

Notebook에서는 가능한 경우 활성 kernel을 기준으로 설치합니다.

```python
import importlib
import subprocess
import sys


def ensure_package(import_name: str, package_name: str | None = None):
    package_name = package_name or import_name
    try:
        return importlib.import_module(import_name)
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name
        ])
        return importlib.import_module(import_name)
```

공식 dependency source는 `pyproject.toml`, `requirements.txt`, lock file입니다.

## 10. Path / UTF-8

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

## 11. Device Detection

기본 우선순위는 CUDA → MPS → CPU입니다.

```python
def detect_device():
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"
```

Profile Resolution 이후에는 확정된 device를 재사용합니다.

## 12. GPU / CPU / RAM 최적화

실제 측정값과 workload를 기준으로 검토합니다.

```text
batch size ↓
sequence/input size ↓
gradient accumulation
mixed precision
gradient checkpointing
quantization
offload
불필요한 tensor/reference 제거
```

CPU/RAM:

```text
대용량 dataset 전체 적재 금지
streaming / chunking / memory mapping
worker 수 보수적 시작
persistent workers / prefetch 과다 사용 금지
DataFrame/list/tensor 중복 복사 금지
CPU/BLAS/OpenMP thread 무제한 증가 금지
```

## 13. Mixed Precision

실제 accelerator가 지원하는 경우 mixed precision을 검토합니다.

```python
USE_AMP = PROFILE.recommended_fp16
```

BF16은 실제 GPU/framework 지원을 확인한 후 사용합니다.

## 14. Gradient Accumulation

```python
BATCH_SIZE = RUNTIME_CONFIG["batch_size"]
GRADIENT_ACCUMULATION_STEPS = RUNTIME_CONFIG[
    "gradient_accumulation_steps"
]

loss = loss / GRADIENT_ACCUMULATION_STEPS
loss.backward()

if (step + 1) % GRADIENT_ACCUMULATION_STEPS == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

effective batch size를 기록합니다.

## 15. Memory Smoke Test

본 학습 전에 최소 대표 workload를 실행합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

peak VRAM, peak RAM, metric, runtime, resolved environment profile을 기록합니다. 실패하면 configuration을 낮춘 뒤 다시 검증합니다.

## 16. OOM / Memory Recovery

```text
VRAM/RAM 기록
→ batch 감소
→ sequence/input 감소
→ workers 감소
→ AMP 확인
→ checkpointing 검토
→ quantization/offload 검토
→ smoke test
→ 성공한 설정으로 실행
```

동일한 실패 설정을 무한 재시도하지 않습니다.

## 17. Training / Early Stopping

장시간 학습에는 validation 기반 Early Stopping을 기본 적용합니다.

```python
EARLY_STOPPING = {
    "enabled": True,
    "metric": "eval_loss",
    "mode": "min",
    "patience": 3,
    "min_delta": 0.0,
    "restore_best": True,
}
```

필수:

- validation split 또는 eval dataset
- metric과 방향 명시
- patience 명시
- best checkpoint 저장
- best checkpoint 복원
- early stop 시점 기록

Hugging Face Trainer에서는 `EarlyStoppingCallback`, `metric_for_best_model`, `greater_is_better`, `load_best_model_at_end`를 일관되게 구성합니다.

## 18. Checkpoint / Resume

가능한 경우 다음을 저장합니다.

```text
model
optimizer
scheduler
AMP scaler
epoch / global step
best metric
Early Stopping counter
training config
seed
model revision
dataset revision
resolved environment profile
```

중단 후 resume이 가능해야 합니다.

## 19. Ablation Study

baseline을 먼저 정의하고 구성 요소별 variant를 명시합니다.

```python
ABLATION_CONFIG = {
    "study_name": "components",
    "baseline": {
        "feature_a": True,
        "feature_b": True,
    },
    "variants": {
        "no_feature_a": {"feature_a": False},
        "no_feature_b": {"feature_b": False},
    },
    "seeds": [42, 43, 44],
    "primary_metric": "eval_loss",
    "metric_mode": "min",
}
```

가능한 한 train/validation split, test set, metric, Early Stopping policy, maximum budget, checkpoint rule, seed set, resolved environment profile을 동일하게 유지합니다.

## 20. Experiment Tracking

다음을 기록합니다.

```text
experiment_id
variant
changed_parameters
seed
model_revision
dataset_revision
best_metric
best_epoch/step
early_stopped
peak_vram
peak_ram
runtime
checkpoint_path
resolved environment profile
```

## 21. Notebook Idempotency

cell 반복 실행으로 결과가 무한 누적되지 않아야 합니다.

- 상태 초기화
- 결정적인 output path
- 임시 파일 정리
- overwrite 정책 명시

## 22. 검증 Workflow

```text
1. Kernel/Runtime restart
2. Environment profiler 실행
3. Hardware / Memory 확인
4. Runtime configuration 생성
5. Environment Lock
6. Memory Smoke Test
7. Baseline 학습/추론
8. Early Stopping 확인
9. Checkpoint save/resume 확인
10. Ablation 실행
11. metrics + resource 기록
12. dead code 제거
13. 최종 Run All
```

## 23. 완료 조건

```text
[ ] 실제 OS / Python / runtime 확인
[ ] CPU / RAM 확인
[ ] GPU / VRAM / accelerator 확인
[ ] environment.py 실행
[ ] environment profile 생성
[ ] runtime configuration 확정
[ ] environment lock
[ ] 미사용 environment branch 삭제
[ ] Memory Smoke Test 통과
[ ] OOM recovery 확인
[ ] validation metric
[ ] Early Stopping
[ ] best checkpoint / Resume
[ ] Ablation matrix
[ ] 동일 조건 비교
[ ] metric / VRAM / RAM / runtime 기록
[ ] clean kernel Run All
```
