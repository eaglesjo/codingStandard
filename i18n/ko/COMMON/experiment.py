# 한국어 설치본에서 사용하는 공통 실험 metadata helper입니다.
# 실행 코드는 언어와 무관하며 저장소 루트 COMMON/experiment.py를 기준으로 유지합니다.

from __future__ import annotations
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
import sys

_COMMON = Path(__file__).resolve().parents[2] / "COMMON" / "experiment.py"
_spec = spec_from_file_location("codingstandard_common_experiment", _COMMON)
if _spec is None or _spec.loader is None:
    raise ImportError(f"공통 실험 helper를 불러올 수 없습니다: {_COMMON}")
_module = module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)

create_metadata = _module.create_metadata
