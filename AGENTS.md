# Project Agent Instructions

이 저장소를 AI coding agent가 작업할 때 사용하는 최상위 진입점이다.

## Instruction Source

`LLM/AGENT.md`는 전체 개발 규칙의 canonical source이다.

`LLM/SKILL.md`는 실제 LLM/Jupyter/ML 작업 절차와 실행 규칙의 canonical source이다.

작업을 시작할 때 다음 순서로 읽고 적용한다.

1. 이 `AGENTS.md`
2. `LLM/AGENT.md`
3. `LLM/SKILL.md`
4. 작업 대상 디렉터리에 더 구체적인 지침 파일이 있으면 해당 지침
5. 프로젝트의 기존 `README.md`, `pyproject.toml`, lock file 및 테스트 규칙

## Mandatory Behavior

- 코드 작성 전에 현재 OS, Python, IDE/runtime, CPU, GPU, VRAM, RAM, CUDA/MPS/CPU device를 확인한다.
- 실제 실행 환경을 확정한 뒤 사용하지 않는 OS/device 분기, dead code, 주석 처리된 구식 구현, 사용하지 않는 import를 제거한다.
- 단, 재사용 library 또는 공식적으로 여러 환경을 지원해야 하는 코드는 필요한 분기를 유지한다.
- RTX 3050 Ti 4GB / RAM 16GB 로컬 환경에서는 보수적인 memory budget을 우선한다.
- 학습에는 validation metric, Early Stopping, best checkpoint, resume 가능한 checkpoint를 기본 적용한다.
- 실험에는 명시적인 configuration과 Ablation Study matrix를 사용하고 seed/metric/resource usage를 기록한다.
- OOM 발생 시 같은 설정을 반복하지 말고 단계별 memory recovery 절차를 적용한다.
- 새 Notebook은 fresh kernel/runtime에서 top-to-bottom 실행 가능해야 한다.

전체 구현 규칙과 예제는 반드시 `LLM/AGENT.md`와 `LLM/SKILL.md`를 기준으로 한다.
