# AGENT.md

# Cross-Platform Python LLM / Jupyter / Google Colab Development

이 문서는 Python 기반 LLM/ML 프로젝트를 Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab 및 Colab Local Runtime에서 개발하는 AI Agent를 위한 공통 개발 규칙이다.

## 1. 지원 범위

- Windows / Linux / macOS
- venv / virtualenv / conda / uv
- Jupyter / JupyterLab / VS Code Jupyter
- Google Colab / Colab Local Runtime
- CPU / CUDA / MPS 환경
- 로컬 GPU 및 제한된 시스템 메모리 환경

## 2. 핵심 원칙

1. 실제 실행 환경을 먼저 확인한다.
2. GPU, CPU, RAM, OS, Python, IDE/runtime을 하드코딩하지 않는다.
3. 재사용 가능한 로직은 `src/` 등에 분리하고 Notebook은 orchestration에 집중한다.
4. OS별 경로는 `pathlib.Path`를 사용한다.
5. 파일 입출력 encoding을 명시한다.
6. API key, token, password를 코드에 넣지 않는다.
7. 가용 VRAM/RAM을 먼저 확인하고 workload에 맞는 자원 사용량을 결정한다.
8. GPU/RAM을 100%까지 채우는 것을 목표로 하지 않는다.
9. 같은 설정으로 OOM을 무한 재시도하지 않는다.
10. 실험 코드는 명시적인 configuration object/section을 사용한다.
11. 장시간 학습에는 validation metric, Early Stopping, Checkpoint/Resume를 기본 적용한다.
12. 실험에는 reproducibility metadata와 resource usage를 기록한다.

## 3. 환경 탐지 → 측정 → 확정

모든 환경 의존적 작업은 다음 흐름을 따른다.

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

가능하면 먼저 공통 프로파일러를 실행한다.

```bash
python LLM/environment.py
```

프로파일 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

## 4. Environment Profile

`LLM/environment.py`의 `inspect_environment()`는 다음을 측정한다.

- OS / architecture
- Python version / executable
- IDE / Jupyter / Colab 상태
- CPU core count
- System RAM total / available
- NVIDIA GPU / VRAM total / free
- CUDA / MPS availability
- resolved device

그리고 측정값을 바탕으로 시작 runtime configuration을 계산한다.

- device
- batch size
- gradient accumulation steps
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

프로파일러 값은 시작점일 뿐이며 실제 모델/데이터의 Memory Smoke Test 결과가 최종 결정권을 가진다.

## 5. 환경 중립성

특정 장비, 메모리 용량, 운영체제 또는 IDE를 현재 실행 환경의 전제조건으로 문서화하지 않는다.

예를 들어 다음과 같은 고정 프로파일을 실행 규칙에 넣지 않는다.

```text
OS: <specific OS>
GPU: <specific GPU>
VRAM: <fixed VRAM>
RAM: <fixed RAM>
```

특정 장비의 과거 또는 개발용 참고 정보가 필요하면 별도의 backup/reference 문서에만 보존한다. 이러한 문서는 runtime decision에 사용하지 않는다.

## 6. Environment Lock

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

프로파일이 확정되면 학습/추론 전체에서 해당 configuration을 재사용한다.

매 cell 또는 함수에서 device, worker 수, precision 등을 임의로 다시 결정하지 않는다.

재사용 가능한 library가 여러 플랫폼을 공식 지원해야 하는 경우에는 detection과 execution을 분리하고 필요한 분기를 유지한다.

## 7. 최종 실행 코드 정리

환경이 확정되면 불필요한 OS/device branch를 제거한다.

삭제 권장:

- 사용하지 않는 CPU/CUDA/MPS 대체 경로
- 중복 environment detection
- 주석 처리된 이전 구현
- 실패한 임시 코드
- 사용하지 않는 import

단, 여러 플랫폼을 공식 지원하는 reusable library에서는 필요한 분기를 유지한다.

## 8. Notebook 표준 구조

권장 순서:

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

새 Notebook은 fresh kernel/runtime에서 top-to-bottom 실행 가능해야 한다.

## 9. Dependency

Notebook에서는 가능하면 활성 kernel 기준으로 설치한다.

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

정식 dependency source는 `pyproject.toml`, `requirements.txt`, lock file을 기준으로 한다.

## 10. Path / UTF-8

```python
from pathlib import Path

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

Windows 전용 사용자 경로나 Unix 전용 shell command를 기본 경로로 사용하지 않는다.

## 11. Device Detection

기본 우선순위는 CUDA → MPS → CPU이다.

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

모델 코드에서 특정 device를 무조건 가정하지 않는다. Profile Resolution 이후에는 확정된 `PROFILE.device`를 사용한다.

## 12. GPU / RAM 최적화

실제 측정값과 workload를 기준으로 다음을 조정한다.

```text
batch size ↓
sequence/input size ↓
gradient accumulation
AMP / mixed precision
gradient checkpointing
quantization 검토
offload 검토
```

CPU/RAM은 다음 원칙을 따른다.

```text
전체 dataset RAM 적재 금지
streaming / chunking / memory mapping 검토
worker 수 최소값부터 시작
persistent workers 남용 금지
prefetch 과다 설정 금지
불필요한 DataFrame/list/tensor 복제 금지
CPU thread 무제한 증가 금지
```

## 13. Mixed Precision

CUDA에서 지원되는 경우 FP16 AMP를 기본 후보로 검토한다.

```python
USE_AMP = PROFILE.recommended_fp16
```

BF16은 실제 GPU와 PyTorch 지원 여부를 확인한 후 사용한다.

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

effective batch size는 `batch_size × accumulation_steps × device_count`로 기록한다.

## 15. Memory Smoke Test

본 학습 전에 최소 workload를 실행한다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

다음 정보를 기록한다.

- peak VRAM
- peak RAM
- loss / validation metric
- runtime
- resolved environment profile

실패하면 configuration을 낮춘 후 다시 smoke test한다.

## 16. OOM / Memory Recovery

```text
VRAM/RAM 기록
→ batch 감소
→ sequence/input 감소
→ workers 감소
→ AMP 확인
→ checkpointing 검토
→ quantization/offload 검토
→ 낮춘 설정으로 smoke test
→ 성공한 설정으로 실행
```

동일 configuration을 무한 retry하지 않는다.

## 17. Training / Early Stopping

장시간 학습에는 validation 기반 Early Stopping을 기본 적용한다.

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

필수 원칙:

- validation split 또는 eval dataset
- metric과 방향 명시
- patience 명시
- best checkpoint 저장
- best checkpoint 복원
- early stop 시점 기록

Hugging Face Trainer를 사용하는 경우 `EarlyStoppingCallback`, `metric_for_best_model`, `greater_is_better`, `load_best_model_at_end`를 일관되게 설정한다.

## 18. Checkpoint / Resume

가능한 경우 checkpoint에 다음을 포함한다.

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

중단 후 resume이 가능해야 한다.

## 19. Ablation Study

baseline을 먼저 정의하고 구성 요소의 효과를 분리한다.

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

가능하면 다음 조건을 variant 간 동일하게 유지한다.

```text
train/validation split
test set
metric
Early Stopping policy
maximum budget
checkpoint rule
seed set
resolved environment profile
```

## 20. Experiment Tracking

결과에는 다음을 기록한다.

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

cell을 여러 번 실행해도 결과가 무한 누적되지 않아야 한다.

- state 초기화
- deterministic output path
- 임시 파일 정리
- overwrite 정책 명시

## 22. 검증 흐름

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
[ ] GPU / VRAM / CUDA/MPS 확인
[ ] environment.py 실행
[ ] environment profile 생성
[ ] resolved runtime configuration 생성
[ ] environment lock
[ ] 미사용 environment branch 삭제
[ ] Memory Smoke Test 통과
[ ] OOM recovery 전략 확인
[ ] validation metric
[ ] Early Stopping
[ ] best checkpoint / Resume
[ ] Ablation matrix
[ ] 동일 조건 비교
[ ] metric / VRAM / RAM / runtime 기록
[ ] clean kernel Run All
```
