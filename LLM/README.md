# LLM Coding Standard

Python 기반 LLM/ML 개발을 위한 `AGENT.md`와 `SKILL.md` 사용 가이드입니다.

이 표준은 **Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, Colab Local Runtime**을 대상으로 하며, 실제 실행환경을 측정하여 그 환경에 맞는 실행 configuration을 결정하는 것을 원칙으로 합니다.

---

## 1. 구성

```text
LLM/
├── AGENT.md
├── SKILL.md
├── ENVIRONMENT.md
├── environment.py
├── LOCAL_HARDWARE_PROFILE_BACKUP.md
└── README.md
```

### AGENT.md

AI Agent가 프로젝트를 수정할 때 따라야 하는 상위 개발 규칙입니다.

### SKILL.md

LLM/Jupyter/ML 작업을 수행할 때 실제 적용하는 실행 절차입니다.

### ENVIRONMENT.md

실행환경 확인, Profile Resolution, Environment Lock 및 최적화 규칙입니다.

### environment.py

현재 PC/Runtime의 CPU, RAM, GPU, VRAM, CUDA/MPS 및 IDE/Jupyter 상태를 측정하고 실제 자원에 맞는 runtime configuration을 계산하는 실행 가능한 프로파일러입니다.

### LOCAL_HARDWARE_PROFILE_BACKUP.md

이전에 사용하던 특정 로컬 개발 장비 프로파일의 백업입니다. 현재 환경 판정의 source of truth가 아니며, 실제 환경은 항상 `environment.py`를 기준으로 합니다.

---

# 2. 개발환경 자동 확인 및 최적화

AI Agent는 개발 시작 시 특정 PC 사양을 가정하지 않고 현재 실행환경을 먼저 확인합니다.

```text
Detect
  ↓
Measure
  ↓
Resolve
  ↓
Memory Smoke Test
  ↓
Environment Lock
  ↓
Remove unused branches
  ↓
Optimized Execution
```

프로파일러 실행:

```bash
python LLM/environment.py
```

profile 저장:

```bash
python LLM/environment.py .codingstandard/environment-profile.json
```

측정 대상:

- OS / architecture
- Python version / executable / active kernel
- IDE / Jupyter / Colab
- CPU count
- System RAM total / available
- NVIDIA GPU / VRAM total / free
- CUDA / MPS availability
- resolved device

자동으로 계산하는 시작 설정:

- device
- batch size
- gradient accumulation
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

권장값은 시작점입니다. 모델과 데이터의 실제 peak memory는 Memory Smoke Test로 다시 검증합니다.

---

# 3. Environment Lock

환경이 확인되면 resolved configuration을 고정하고 이후 학습/추론에서 재사용합니다.

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

각 cell에서 다시 device, worker, precision을 임의로 결정하지 않습니다.

환경이 하나로 확정된 프로젝트의 실행 코드에서는 사용하지 않는 OS/device branch, dead code, 주석 처리된 이전 구현을 제거합니다.

단, 여러 플랫폼을 공식 지원하는 reusable library에서는 필요한 분기를 유지하고 detection과 execution을 분리합니다.

---

# 4. 저사양 GPU / 시스템 메모리 최적화

특정 GPU 모델이나 RAM 용량을 코드에 하드코딩하지 않습니다. 측정된 VRAM/RAM에 따라 보수적인 configuration을 계산합니다.

GPU:

```text
batch size ↓
sequence/input size ↓
gradient accumulation
FP16 AMP
gradient checkpointing
8-bit / 4-bit quantization 검토
optimizer memory / CPU offload 검토
```

CPU/RAM:

```text
전체 dataset RAM 적재 금지
streaming / chunking / memory mapping
DataLoader workers 보수적 설정
persistent workers 기본 비활성화
prefetch 과다 설정 금지
DataFrame/list/tensor 중복 복사 금지
CPU thread 무제한 증가 금지
```

전체 VRAM/RAM을 100%까지 채우는 것을 목표로 하지 않습니다.

---

# 5. Memory Smoke Test

본 학습 전에 최소 workload를 검증합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

peak VRAM, peak RAM, loss, runtime을 기록합니다.

Smoke Test가 실패하면 본 학습을 시작하지 않고 batch / input size / workers / precision / checkpointing 등의 resource configuration을 낮춘 후 다시 검증합니다.

---

# 6. OOM Recovery

CUDA OOM 또는 System RAM 부족이 발생하면 같은 설정을 무한 재시도하지 않습니다.

```text
VRAM/RAM 기록
→ batch ↓
→ sequence/input ↓
→ workers ↓
→ AMP 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 통과 시 학습
```

`torch.cuda.empty_cache()`만을 OOM 해결책으로 사용하지 않습니다.

---

# 7. 학습 / Early Stopping / Checkpoint

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

학습은 가능한 경우 다음을 함께 사용합니다.

- validation metric
- Early Stopping
- best checkpoint
- Resume
- 학습 상태 및 설정 metadata 저장

Hugging Face Trainer 사용 시 `EarlyStoppingCallback`, `metric_for_best_model`, `greater_is_better`, `load_best_model_at_end`를 일관되게 설정합니다.

---

# 8. Ablation Study

학습 구성 요소의 기여도를 검증할 때 baseline과 variant를 명시적인 matrix로 관리합니다.

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

가능하면 variant 사이에 다음을 동일하게 유지합니다.

```text
train/validation split
 test set
metric
Early Stopping policy
maximum training budget
checkpoint rule
seed set
resolved environment profile
```

결과에는 metric뿐 아니라 peak VRAM, peak RAM, runtime, checkpoint, early-stopped 여부와 configuration을 기록합니다.

---

# 9. AI 작업 표준 흐름

```text
1. Repository / instruction 읽기
2. environment.py 실행
3. 실제 환경 측정
4. runtime configuration 계산
5. Environment Lock
6. Memory Smoke Test
7. 구현
8. 학습 / 평가
9. Early Stopping / Checkpoint 확인
10. Ablation 실행
11. metric + resource 기록
12. dead branch / dead code 제거
13. clean kernel Run All
```

---

# 10. 다른 프로젝트에 적용

codingStandard를 clone합니다.

```bash
git clone https://github.com/eaglesjo/codingStandard.git
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\codingStandard\scripts\install-coding-standard.ps1 -Target .
```

Linux/macOS:

```bash
bash ./codingStandard/scripts/install-coding-standard.sh .
```

설치 후 AI 자동 진입점과 `LLM/` 표준을 함께 사용합니다.

---

# 11. 완료 조건

```text
[ ] 실제 OS / IDE / runtime 확인
[ ] Python / active kernel 확인
[ ] CPU / RAM 확인
[ ] GPU / VRAM / CUDA/MPS 확인
[ ] environment.py 실행
[ ] runtime configuration 확정
[ ] environment lock
[ ] 미사용 environment branch 삭제
[ ] Memory Smoke Test 통과
[ ] OOM recovery 전략
[ ] validation metric
[ ] Early Stopping
[ ] best checkpoint / Resume
[ ] baseline / Ablation matrix
[ ] 동일 조건 비교
[ ] metric / VRAM / RAM / runtime 기록
[ ] clean kernel Run All
```
