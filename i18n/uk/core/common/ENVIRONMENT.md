# Спільний контракт Environment

Усі домени використовують реальне execution environment як source of truth.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Вимірюйте CPU, system RAM, disk, accelerator/GPU, VRAM, можливості framework і Python/runtime, якщо вони доступні. Не вважайте конкретний hardware profile вимогою runtime. Залишайте memory headroom для ОС, IDE, framework і фонових процесів.

Під час validation workload, коли це доречно, перевіряйте early stopping і checkpoint save/reload.