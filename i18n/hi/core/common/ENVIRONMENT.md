# सामान्य Environment Contract

सभी domains वास्तविक execution environment को source of truth मानते हैं.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

CPU, system RAM, disk, accelerator/GPU, VRAM, framework capabilities और Python/runtime उपलब्ध होने पर मापें।

किसी नामित hardware profile को runtime requirement न मानें। OS, IDE और background processes के लिए memory headroom रखें और 100% utilization का लक्ष्य न रखें।

Workload validation में early stopping और checkpoint save/reload जैसे व्यवहारों को आवश्यकतानुसार सत्यापित करें।
