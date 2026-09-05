# กฎทั่วไปสำหรับ AI Agent

1. อ่านและปฏิบัติตามคำแนะนำของ repository
2. เคารพสถาปัตยกรรมและนโยบายที่มีอยู่
3. ตรวจสอบโค้ดและ tests ที่เกี่ยวข้องก่อนเปลี่ยนพฤติกรรม
4. เพิ่มหรือปรับปรุง tests เมื่อพฤติกรรมเปลี่ยน
5. แยกรายละเอียดที่ขึ้นกับแพลตฟอร์มไว้หลัง abstraction
6. ห้าม commit secrets หรือ credentials
7. ใช้ network access เมื่อมีความจำเป็นอย่างชัดเจน
8. ใช้ execution environment จริงเป็น source of truth
9. ให้ความสำคัญกับ validation ที่ทำซ้ำได้
10. รัน validation หลังการเปลี่ยนแปลงและรายงานผล

## วงจรการทำงาน

```text
Inspect → Plan → Change → Validate → Review → Report
```

ตรวจสอบ memory และ runtime ก่อนตั้งสมมติฐานด้านฮาร์ดแวร์ สำหรับงานระยะยาวให้ตรวจสอบ early stopping และ checkpoint