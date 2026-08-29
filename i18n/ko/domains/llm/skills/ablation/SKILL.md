# Ablation Study Skill

구성 요소 및 설정의 효과를 통제된 조건에서 비교하는 실험에 사용합니다.

`LLM/config/ablation.yaml` 또는 동등한 설정 파일에 baseline과 명시적인 variant matrix를 정의합니다.

가능하면 train/validation split, test set, metric 정의, Early Stopping 정책, 최대 budget, checkpoint 정책, 평가 절차를 variant 간 동일하게 유지합니다.

중요한 실험은 선언된 seed 집합으로 반복하고 experiment ID, 변경 파라미터, seed, Git commit, model/dataset revision, best metric, early-stopped 여부, peak VRAM/RAM, runtime, checkpoint, resolved environment profile을 기록합니다.

설명되지 않은 여러 요소를 한 variant에서 동시에 바꾸지 않습니다. 상호작용을 보기 위한 factorial design인 경우에는 실험 설계에 명시합니다.
