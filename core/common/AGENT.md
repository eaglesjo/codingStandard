# Common AI Agent Rules

These rules apply to every supported project domain.

1. Inspect the actual repository, runtime, dependencies, tests, and security constraints before changing code.
2. Detect and measure the real execution environment before choosing resource-sensitive settings.
3. Do not hard-code a specific machine, OS, CPU, RAM, GPU, accelerator, or IDE as a project prerequisite.
4. Keep reusable domain logic in modules and keep notebooks/scripts focused on orchestration.
5. Use explicit configuration, reproducibility metadata, and deterministic paths.
6. Preserve secrets outside source control.
7. Validate changes with the smallest meaningful test first, then run the broader test suite.
8. After environment validation, remove unused execution branches and obsolete code unless multi-platform support is intentional.
9. Long-running workloads should use validation, Early Stopping where meaningful, best Checkpoint, and Resume.
10. Experiments should define a baseline, controlled variants, seeds, metrics, and resource tracking.

## Standard execution lifecycle

```text
Discover → Detect → Measure → Resolve → Smoke Test → Lock → Implement → Validate → Record
```
