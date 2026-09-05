# สัญญา Environment ทั่วไป

ทุก domain ใช้ execution environment จริงเป็น source of truth

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

วัด CPU, system RAM, disk, accelerator/GPU, VRAM, ความสามารถของ framework และ Python/runtime เมื่อทำได้ อย่ากำหนด hardware profile ใดเป็น requirement และควรเหลือ memory headroom สำหรับ OS, IDE, framework และงานเบื้องหลัง

ในการ validation ของ workload ให้ตรวจสอบ early stopping และ checkpoint save/reload เมื่อเกี่ยวข้อง