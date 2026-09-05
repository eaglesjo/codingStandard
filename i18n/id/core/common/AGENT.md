# Aturan Umum untuk Agen AI

1. Baca dan ikuti instruksi repositori.
2. Hormati arsitektur dan kebijakan yang ada.
3. Periksa kode serta tests terkait sebelum mengubah perilaku.
4. Tambahkan atau perbarui tests untuk perubahan perilaku.
5. Abstraksikan detail yang spesifik platform.
6. Jangan commit secrets atau credentials.
7. Gunakan akses jaringan hanya bila diperlukan secara eksplisit.
8. Jadikan environment eksekusi nyata sebagai source of truth.
9. Utamakan validation yang reproducible.
10. Jalankan validation setelah perubahan dan laporkan hasilnya.

## Siklus kerja

```text
Inspect → Plan → Change → Validate → Review → Report
```

Periksa memory dan runtime sebelum membuat asumsi hardware. Untuk workload panjang, verifikasi early stopping dan checkpoint.