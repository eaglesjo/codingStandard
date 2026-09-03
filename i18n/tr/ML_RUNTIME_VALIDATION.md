# ML/DL Runtime Doğrulaması

Bu kılavuz, `codingStandard` kurulumundan sonra gerçek çalıştırma sözleşmesini doğrular.

## Agent yönlendirme

Depo kök dizininden çalıştırın:

```bash
python scripts/validation/validate_agent_routing.py
```

Test dört temsili isteği kapsar:

- genel PyTorch eğitimi → common + ML yaşam döngüsü
- LLM QLoRA → common + ML + LLM fine-tuning/PEFT/quantization
- Vision detection → common + ML + Vision detection/evaluation
- Colab LLM training → common + ML + LLM + Colab checkpoint/resume politikası

Test ayrıca bu minimum senaryolara ilgisiz alanların yanlışlıkla dahil edilmediğini kontrol eder.

## Colab runtime

Yeni bir Colab runtime'da `examples/colab/clean_runtime_validation.ipynb` dosyasını açın. Tüm hücreleri yukarıdan aşağıya çalıştırın.

Notebook şunları yapmalıdır:

1. etkin Python kernel'ini ve çalışma ortamını belirlemek;
2. kullanılabiliyorsa accelerator, RAM ve disk özelliklerini raporlamak;
3. agent-routing sözleşme testini çalıştırmak;
4. PyTorch mevcutsa küçük bir forward/backward smoke test çalıştırmak;
5. seçilen kalıcı dizinde checkpoint yazmak ve geri yüklemek;
6. makine tarafından okunabilir bir runtime report üretmek.

Checkpoint'lerin Colab sıfırlamasından sonra da korunması gerekiyorsa bağlı bir kalıcı konum kullanın. Notebook VM dosya sistemi geçici kabul edilmelidir.

## Yorumlama

Başarılı doğrulama; kurulu politikanın keşfedilebildiği, seçilen runtime'ın ölçülebildiği, temsili bir workload'un güvenli şekilde başlatılabildiği ve kurtarma artifact'lerinin geri yüklenebildiği anlamına gelir. Tüm Colab accelerator türlerinin veya tüm model boyutlarının test edildiği anlamına gelmez.
