# Yapay Zekâ Ajanları için Ortak Kurallar

Bu kurallar desteklenen tüm alanlara uygulanır.

1. Kodda değişiklik yapmadan önce gerçek depoyu, çalışma ortamını, bağımlılıkları, testleri ve güvenlik gereksinimlerini inceleyin.
2. Kaynaklara duyarlı parametreleri seçmeden önce gerçek çalışma ortamını algılayın ve ölçün.
3. Belirli bir makine, işletim sistemi, CPU, RAM, GPU, hızlandırıcı veya IDE gerektiğini varsaymayın.
4. Yeniden kullanılabilir alan mantığını modüllerde tutun; notebook ve scriptleri orkestrasyonla sınırlayın.
5. Açık yapılandırma, yeniden üretilebilirlik metadatası ve belirleyici yollar kullanın.
6. Gizli bilgileri sürüm kontrolü dışında tutun.
7. Önce en küçük anlamlı testle doğrulayın, ardından daha kapsamlı test paketini çalıştırın.
8. Ortam doğrulandıktan sonra, çoklu platform desteği kasıtlı değilse kullanılmayan çalışma yollarını ve eski kodu kaldırın.
9. Uzun iş yüklerinde uygun olduğunda doğrulama, Early Stopping, en iyi Checkpoint ve Resume kullanın.
10. Deneyler baseline, kontrollü varyantlar, seed değerleri, metrikler ve kaynak takibi tanımlamalıdır.

## Standart yürütme döngüsü

```text
Keşfet → Algıla → Ölç → Çöz → Smoke Test → Düzelt → Uygula → Doğrula → Belgele
```
