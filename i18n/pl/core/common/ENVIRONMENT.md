# Wspólny kontrakt Environment

Wszystkie domeny traktują rzeczywiste execution environment jako source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Mierz CPU, system RAM, disk, accelerator/GPU, VRAM, możliwości frameworka oraz Python/runtime, gdy są dostępne. Nie uznawaj określonego profilu sprzętowego za runtime requirement. Zachowaj memory headroom dla systemu, IDE, frameworka i procesów w tle.

W validation workload, gdy ma to zastosowanie, sprawdź early stopping oraz checkpoint save/reload.