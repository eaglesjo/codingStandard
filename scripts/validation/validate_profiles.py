from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES = ROOT / "profiles"
REQUIRED_PROJECT_KEYS = {"id", "profile_version", "project_type", "architecture_profile", "policy_profile", "runtime", "delivery", "scalability"}
REQUIRED_ARCH_KEYS = {"id", "profile_version", "project_type", "layers", "path_roots", "dependency_direction", "forbidden_dependencies", "boundaries", "scalability_profile"}
REQUIRED_POLICY_KEYS = {"id", "profile_version", "scope", "rules", "inheritance"}
ID_RE = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
SENSITIVE_PATTERNS = (
    re.compile(r"password\s*[:=]\s*[^\s,}\]]+", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]\s*[^\s,}\]]+", re.IGNORECASE),
    re.compile(r"token\s*=\s*[^\s,}\]]+", re.IGNORECASE),
    re.compile(r"/(?:Users|home)/[^\s\"']+", re.IGNORECASE),
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid profile {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"profile must be an object: {path}")
    return value


def check_keys(value: dict, required: set[str], path: Path) -> None:
    missing = sorted(required - value.keys())
    if missing:
        fail(f"missing keys in {path}: {', '.join(missing)}")


def check_id(value: dict, path: Path) -> None:
    if not isinstance(value.get("id"), str) or not ID_RE.fullmatch(value["id"]):
        fail(f"invalid profile id in {path}")
    if value.get("profile_version") != 1:
        fail(f"unsupported profile_version in {path}")


def check_project(path: Path, value: dict, architecture_ids: set[str], policy_ids: set[str]) -> None:
    check_keys(value, REQUIRED_PROJECT_KEYS, path)
    check_id(value, path)
    if value["architecture_profile"] not in architecture_ids:
        fail(f"unknown architecture_profile '{value['architecture_profile']}' in {path}")
    if value["policy_profile"] not in policy_ids:
        fail(f"unknown policy_profile '{value['policy_profile']}' in {path}")
    runtime = value["runtime"]
    if not isinstance(runtime, dict) or not {"os", "reference", "python"} <= runtime.keys():
        fail(f"runtime contract incomplete in {path}")
    oses = runtime.get("os")
    if not isinstance(oses, list) or not {"linux", "macos", "windows"} <= set(oses):
        fail(f"project profile must declare cross-platform support in {path}")
    delivery = value["delivery"]
    if not isinstance(delivery, dict) or delivery.get("validation_required") is not True:
        fail(f"delivery.validation_required must be true in {path}")


def check_architecture(path: Path, value: dict) -> None:
    check_keys(value, REQUIRED_ARCH_KEYS, path)
    check_id(value, path)
    layers = value["layers"]
    if not isinstance(layers, dict) or not layers:
        fail(f"architecture layers must be a non-empty object in {path}")
    allowed = set(layers)
    path_roots = value["path_roots"]
    if not isinstance(path_roots, dict) or set(path_roots) != allowed:
        fail(f"architecture path_roots must declare every layer exactly once in {path}")
    seen_roots: set[str] = set()
    for layer, roots in path_roots.items():
        if not isinstance(roots, list) or not all(isinstance(root, str) and root for root in roots):
            fail(f"architecture path_roots must contain non-empty string arrays in {path}: {layer}")
        for root in roots:
            if root in seen_roots:
                fail(f"architecture path root is assigned to multiple layers in {path}: {root}")
            seen_roots.add(root)
    directions = value["dependency_direction"]
    forbidden = value["forbidden_dependencies"]
    if not isinstance(directions, list) or not isinstance(forbidden, list):
        fail(f"dependency contracts must be arrays in {path}")
    for edge in [*directions, *forbidden]:
        if not isinstance(edge, str) or " -> " not in edge:
            fail(f"invalid dependency edge in {path}: {edge!r}")
        source, target = edge.split(" -> ", 1)
        if source not in allowed or target not in allowed:
            fail(f"dependency edge references unknown layer in {path}: {edge}")
    overlap = set(directions) & set(forbidden)
    if overlap:
        fail(f"dependency edge is both allowed and forbidden in {path}: {sorted(overlap)[0]}")
    if not isinstance(value["boundaries"], list) or not value["boundaries"]:
        fail(f"architecture boundaries must be a non-empty array in {path}")


def check_policy(path: Path, value: dict) -> None:
    check_keys(value, REQUIRED_POLICY_KEYS, path)
    check_id(value, path)
    if value["scope"] != "repository":
        fail(f"repository policy must have scope=repository in {path}")
    if not isinstance(value["rules"], dict) or not value["rules"]:
        fail(f"policy rules must be a non-empty object in {path}")
    inheritance = value["inheritance"]
    required_inheritance = {"child_scopes_may_add_restrictions", "child_scopes_may_not_weaken_parent", "conflict_resolution"}
    if not isinstance(inheritance, dict) or not required_inheritance <= inheritance.keys():
        fail(f"policy inheritance contract incomplete in {path}")
    if inheritance["child_scopes_may_not_weaken_parent"] is not True:
        fail(f"policy inheritance must prevent weakening parent rules in {path}")
    if inheritance["conflict_resolution"] != "stricter-wins":
        fail(f"policy conflict resolution must be stricter-wins in {path}")


def check_sensitive_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            fail(f"potential secret or machine-specific reference in {path}: {pattern.pattern}")


def layer_for_path(path: Path, path_roots: dict[str, list[str]]) -> str | None:
    relative = path.relative_to(ROOT).as_posix()
    matches = [layer for layer, roots in path_roots.items() if any(relative == root or relative.startswith(root + "/") for root in roots)]
    if len(matches) > 1:
        fail(f"path belongs to multiple architecture layers: {relative}")
    return matches[0] if matches else None


def local_module_exists(module: str) -> bool:
    if not module or module.split(".", 1)[0] in sys.stdlib_module_names:
        return False
    base = ROOT / Path(module.replace(".", "/"))
    return base.with_suffix(".py").is_file() or (base / "__init__.py").is_file() or base.is_dir()


def resolve_local_module(module: str) -> Path | None:
    if not module or module.split(".", 1)[0] in sys.stdlib_module_names:
        return None
    base = ROOT / Path(module.replace(".", "/"))
    if base.with_suffix(".py").is_file():
        return base.with_suffix(".py")
    init = base / "__init__.py"
    if init.is_file():
        return init
    if base.is_dir():
        return base
    return None


def resolve_relative_module(source: Path, level: int, module: str | None) -> str:
    package_parts = list(source.relative_to(ROOT).with_suffix("").parts[:-1])
    if level > len(package_parts) + 1:
        return ""
    base = package_parts[: len(package_parts) - level + 1]
    if module:
        base.extend(module.split("."))
    return ".".join(base)


def imported_modules(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        fail(f"Python syntax error in {path}: {exc}")
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                modules.append(resolve_relative_module(path, node.level, node.module))
            elif node.module:
                modules.append(node.module)
    return modules


def check_dependency_edge(source_layer: str, target_layer: str, allowed: set[tuple[str, str]], forbidden: set[tuple[str, str]]) -> str:
    edge = (source_layer, target_layer)
    if edge in forbidden:
        return "forbidden"
    if edge not in allowed:
        return "undeclared"
    return "allowed"


def check_repository_dependencies(architecture: dict) -> None:
    path_roots = architecture["path_roots"]
    allowed = {tuple(edge.split(" -> ", 1)) for edge in architecture["dependency_direction"]}
    forbidden = {tuple(edge.split(" -> ", 1)) for edge in architecture["forbidden_dependencies"]}
    scanned = 0
    for path in sorted(ROOT.rglob("*.py")):
        if ".git" in path.parts or path.is_symlink():
            continue
        source_layer = layer_for_path(path, path_roots)
        if source_layer is None:
            continue
        scanned += 1
        for module in imported_modules(path):
            target = resolve_local_module(module) if local_module_exists(module) else None
            if target is None:
                continue
            target_layer = layer_for_path(target, path_roots)
            if target_layer is None or source_layer == target_layer:
                continue
            decision = check_dependency_edge(source_layer, target_layer, allowed, forbidden)
            if decision == "forbidden":
                fail(f"forbidden architecture dependency: {source_layer} -> {target_layer} ({path.relative_to(ROOT)} imports {module})")
            if decision == "undeclared":
                fail(f"undeclared architecture dependency: {source_layer} -> {target_layer} ({path.relative_to(ROOT)} imports {module}); add the edge to dependency_direction only if the dependency is architecturally intentional")
    print(f"repository dependency validation passed ({scanned} Python files scanned)")


def main() -> None:
    if not PROFILES.is_dir():
        fail("profiles directory is missing")
    architecture_dir = PROFILES / "architecture"
    policy_dir = PROFILES / "policies"
    architecture_paths = sorted(architecture_dir.glob("*.json")) if architecture_dir.is_dir() else []
    policy_paths = sorted(policy_dir.glob("*.json")) if policy_dir.is_dir() else []
    project_paths = sorted(PROFILES.glob("project*.json"))
    if not architecture_paths:
        fail("no architecture profiles found")
    if not policy_paths:
        fail("no policy profiles found")
    if not project_paths:
        fail("no project profiles found")
    architecture_ids: set[str] = set()
    architecture_values: list[dict] = []
    for path in architecture_paths:
        value = load(path)
        check_architecture(path, value)
        architecture_ids.add(value["id"])
        architecture_values.append(value)
        check_sensitive_text(path)
    policy_ids: set[str] = set()
    for path in policy_paths:
        value = load(path)
        check_policy(path, value)
        policy_ids.add(value["id"])
        check_sensitive_text(path)
    for path in project_paths:
        value = load(path)
        check_project(path, value, architecture_ids, policy_ids)
        check_sensitive_text(path)
    for architecture in architecture_values:
        check_repository_dependencies(architecture)
    print(f"architecture profile validation passed ({len(architecture_paths)} architecture, {len(policy_paths)} policy, {len(project_paths)} project)")


if __name__ == "__main__":
    main()
