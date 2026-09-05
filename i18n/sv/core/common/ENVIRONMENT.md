# Gemensamt Environment-kontrakt

Alla domäner använder den verkliga execution environment som source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Mät CPU, system RAM, disk, accelerator/GPU, VRAM, framework-funktioner och Python/runtime när det är möjligt. Gör inte en viss hårdvaruprofil till runtime requirement. Behåll memory headroom för OS, IDE, framework och bakgrundsprocesser.

Vid workload validation, verifiera early stopping och checkpoint save/reload när det är relevant.