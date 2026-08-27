# Common Environment Contract

All domains use the real execution environment as the source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Measure available CPU, system RAM, disk, accelerator/GPU, accelerator memory, framework capabilities, Python/runtime, and relevant IDE/kernel state when available.

Do not use a named hardware profile as a runtime requirement. Domain-specific workloads may add resource controls, but the common profile remains the measured source of truth.

Keep headroom for the OS, IDE/runtime, framework allocations, and background processes. Do not target 100% utilization.
