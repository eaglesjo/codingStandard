# 한국어 설치본에서도 사용하는 공통 실행환경 프로파일러입니다.
# 실행 코드이므로 언어에 의존하지 않으며 저장소 루트의 COMMON/environment.py와 동일하게 유지합니다.

from pathlib import Path
import importlib.util
import sys

_COMMON = Path(__file__).resolve().parents[2] / "COMMON" / "environment.py"
_spec = importlib.util.spec_from_file_location("codingstandard_common_environment", _COMMON)
if _spec is None or _spec.loader is None:
    raise ImportError(f"공통 환경 프로파일러를 불러올 수 없습니다: {_COMMON}")
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)

EnvironmentProfile = _module.EnvironmentProfile
inspect_environment = _module.inspect_environment
to_runtime_config = _module.to_runtime_config
save_profile = _module.save_profile
print_profile = _module.print_profile
