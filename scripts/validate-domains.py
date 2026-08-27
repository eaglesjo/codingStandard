from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['COMMON/AGENT.md','COMMON/SKILL.md','COMMON/ENVIRONMENT.md','LLM/AGENT.md','LLM/SKILL.md','VISION/AGENT.md','VISION/SKILL.md','VISION/ENVIRONMENT.md','VISION/memory_smoke_test.py']
for rel in REQUIRED:
    p=ROOT/rel
    if not p.is_file(): raise SystemExit(f'Missing: {rel}')
for p in ROOT.joinpath('VISION').rglob('*.py'): ast.parse(p.read_text(encoding='utf-8'))
print('domain validation passed')
