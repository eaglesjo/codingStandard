# LLM Coding Standard

Python 기반 LLM/ML 개발을 위한 `AGENT.md`와 `SKILL.md` 사용 가이드입니다.

이 표준은 **Jupyter Notebook, JupyterLab, VS Code Jupyter, Google Colab, Colab Local Runtime**을 대상으로 하며 **Windows / Linux / macOS** 호환성과 로컬 저사양 GPU에서의 안정적인 학습을 함께 고려합니다.

---

## 1. 구성

```text
LLM/
├── AGENT.md
├── SKILL.md
├── ENVIRONMENT.md
├── environment.py
└── README.md
```

### AGENT.md

AI Agent가 프로젝트를 수정할 때 따라야 하는 상위 개발 규칙입니다.

### SKILL.md

LLM/Jupyter 작업을 수행할 때 실제 적용하는 실행 절차입니다.

### ENVIRONMENT.md

실행환경 확인, Profile Resolution, Environment Lock 및 최적화 규칙입니다.

### environment.py

현재 PC/Runtime의 CPU, RAM, GPU, VRAM, CUDA/MPS 및 IDE/Jupyter 상태를 측정하고 보수적인 runtime configuration을 계산하는 실행 가능한 프로파일러입니다.

---

# 2. 기준 로컬 개발 환경

```text
OS: Windows
IDE: VS Code
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
GPU VRAM: 4 GB
System RAM: 16 GB
```

4 GB VRAM과 16 GB RAM을 제한 자원으로 보고 보수적으로 시작한 뒤 실제 사용량을 측정하여 확장합니다.

---

# 3. 개발환경 자동 확인 및 최적화

AI Agent는 코드를 작성하기 전에 실제 실행환경을 확인합니다.

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
- Python version / executable
- VS Code / Jupyter / Colab
- CPU count
- System RAM total / available
- NVIDIA GPU / VRAM total / free
- CUDA / MPS
- resolved device

자동으로 계산하는 시작 설정:

- batch size
- gradient accumulation
- DataLoader workers
- pin memory
- FP16 / BF16 후보
- gradient checkpointing
- maximum sequence length

프로파일러 결과는 권장 시작값이다. 실제 모델/데이터의 peak memory는 Memory Smoke Test로 다시 검증합니다.

---

# 4. Environment Lock

환경이 검증되면 resolved configuration을 고정합니다.

```python
from environment import inspect_environment, to_runtime_config

PROFILE = inspect_environment()
RUNTIME_CONFIG = to_runtime_config(PROFILE)
```

이후 각 cell에서 다시 device나 worker 수를 임의로 결정하지 않습니다.

환경이 하나로 확정된 프로젝트의 실행 코드에서는 사용하지 않는 OS/device branch를 제거합니다.

단, 여러 플랫폼을 공식 지원하는 reusable library에서는 분기를 유지하고 detection과 execution을 분리합니다.

---

# 5. 권장 GPU / CPU / RAM 최적화

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

RAM/CPU:

```text
전체 dataset RAM 적재 금지
streaming/chunking/memory mapping
Windows num_workers=0 또는 1부터 시작
persistent_workers 기본 비활성화
prefetch 과다 설정 금지
DataFrame/list/tensor 중복 복사 금지
CPU thread 무제한 증가 금지
```

전체 VRAM/RAM을 100%까지 채우지 않습니다.

---

# 6. Memory Smoke Test

본 학습 전에 최소 workload를 실행합니다.

```text
model load
→ forward
→ backward
→ optimizer step
→ validation
→ checkpoint save
```

peak VRAM, peak RAM, loss, runtime을 기록합니다.

Smoke Test 실패 시 본 학습을 시작하지 않고 resource configuration을 낮춥니다.

---

# 7. OOM Recovery

```text
VRAM/RAM 기록
→ batch ↓
→ sequence/input ↓
→ workers ↓
→ AMP 확인
→ checkpointing
→ quantization/offload 검토
→ smoke test
→ 학습
```

같은 설정으로 무한 재시도하지 않습니다.

---

# 8. 학습 / Early Stopping

장시간 학습에는 validation metric과 Early Stopping을 기본 적용합니다.

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

Best checkpoint를 저장하고 Early Stop 후 복원합니다. 학습 중단 후 Resume 가능한 checkpoint를 유지합니다.

---

# 9. Ablation Study

모든 주요 학습 구성은 명시적인 experiment matrix로 관리합니다.

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

variant간 동일 dataset split, evaluation set, Early Stopping 정책, 최대 budget, metric, seed set 및 resolved environment profile을 유지합니다.

결과에는 metric뿐 아니라 peak VRAM, peak RAM, runtime, checkpoint, early-stopped 여부를 기록합니다.

---

# 10. AI에게 요청하는 표준 작업 흐름

```text
1. Repository / instructions 읽기
2. environment.py 실행
3. 실제 환경 측정
4. runtime configuration 계산
5. Environment Lock
6. Memory Smoke Test
7. 구현
8. 학습/평가
9. Early Stopping / Checkpoint 확인
10. Ablation 실행
11. metric + resource 기록
12. dead branch / dead code 제거
13. 최종 clean Run All
```

---

# 11. 다른 프로젝트에 적용

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

# 12. 완료 조건

```text
[ ] 실제 OS / IDE / runtime 확인
[ ] Python / active kernel 확인
[ ] CPU / RAM 확인
[ ] GPU / VRAM / CUDA 확인
[ ] environment.py 실행
[ ] environment profile 생성
[ ] runtime configuration 확정
[ ] environment lock
[ ] 사용하지 않는 environment branch 삭제
[ ] Memory Smoke Test 통과
[ ] OOM recovery 전략
[ ] Early Stopping
[ ] Best checkpoint / Resume
[ ] Ablation matrix
[ ] 동일 조건 비교
[ ] metric / VRAM / RAM / runtime 기록
[ ] clean kernel Run All
```
