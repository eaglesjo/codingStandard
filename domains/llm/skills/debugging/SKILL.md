# Debugging Skill

Use for failures, exceptions, test regressions, and runtime issues.

First capture the exact error, command, environment profile, dependency versions, Git commit, and minimal reproduction.

For resource failures, record peak/available RAM and VRAM before changing settings. For OOM, use staged reduction of batch/input/workers and verify each change with a smoke test.

Prefer a minimal reproducible fix over broad rewrites. Add or update a regression test when practical. Remove temporary diagnostic code before completion.
