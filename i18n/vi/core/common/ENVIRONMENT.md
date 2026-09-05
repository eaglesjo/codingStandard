# Hợp đồng Environment chung

Mọi domain dùng execution environment thực tế làm source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Đo CPU, system RAM, disk, accelerator/GPU, VRAM, khả năng framework và Python/runtime khi có thể. Không coi một hardware profile cố định là requirement. Luôn chừa memory headroom cho OS, IDE, framework và tiến trình nền.

Trong workload validation, xác minh early stopping và checkpoint save/reload khi cần.