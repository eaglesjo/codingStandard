# Kontrak Environment Umum

Semua domain menggunakan execution environment nyata sebagai source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Ukur CPU, system RAM, disk, accelerator/GPU, VRAM, kemampuan framework, dan Python/runtime bila tersedia. Jangan jadikan profil hardware tertentu sebagai requirement. Sisakan headroom untuk OS, IDE, framework, dan proses latar belakang.

Dalam validation workload, verifikasi early stopping dan checkpoint save/reload bila relevan.