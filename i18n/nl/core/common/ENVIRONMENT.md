# Algemeen Environment-contract

Alle domeinen gebruiken de echte execution environment als source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Meet CPU, system RAM, disk, accelerator/GPU, VRAM, frameworkmogelijkheden en Python/runtime wanneer beschikbaar. Beschouw geen vast hardwareprofiel als runtime requirement. Houd memory headroom voor OS, IDE, framework en achtergrondprocessen.

Controleer bij workload-validation indien relevant early stopping en checkpoint save/reload.