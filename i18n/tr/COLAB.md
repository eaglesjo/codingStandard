# Google Colab Doğrulaması

Bu belge, `codingStandard` için Google Colab üzerinde çalıştırma ve doğrulama adımlarını açıklar.

## Colab'da açma

Depo README'sindeki Colab bağlantısını kullanın veya aşağıdaki Notebook'u doğrudan açın:

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

Bir fork veya taşınmış kopya kullanıyorsanız, bu kopyanın Notebook'unu Colab'da açın ve ilk hücrede depo URL'sini girin ya da `CODINGSTANDARD_REPO_URL` ortam değişkenini ayarlayın.

## Depo seçimi

Notebook belirli bir depo URL'sine sabitlenmez. Öncelik sırası şöyledir:

1. `CODINGSTANDARD_REPO_URL` ortam değişkeni.
2. Etkileşimli depo URL'si istemi.
3. Varsayılan olarak özgün `eaglesjo/codingStandard` URL'si.

## Genel ve özel depolarda kimlik doğrulama

Notebook önce kimlik doğrulama olmadan clone denemesi yapar.

- **Genel depo:** clone hemen devam eder ve token istemi gösterilmez.
- **Özel depo:** kimlik doğrulamasız clone reddedildikten sonra güvenli `getpass` istemiyle **GitHub Personal Access Token** istenir.
- Google Colab Secrets veya ortamda bulunan `GITHUB_TOKEN` varsa otomatik olarak kullanılır.

Token, geçici bir `GIT_ASKPASS` helper üzerinden Git'e aktarılır. Clone URL'sine, Notebook kaynak koduna, yazdırılan çıktıya veya kaydedilen sonuç JSON'una eklenmez. Testten sonra token'ı Colab oturumundan kaldırın.

## Neleri kontrol eder

1. Seçilen depoyu Colab runtime içine clone eder.
2. Python, PyTorch, CPU, RAM, accelerator, VRAM, CUDA/MPS capability ve runtime bilgilerini algılar.
3. Ortak LLM environment profiler'ı çalıştırır.
4. Checkpoint kaydetme/yeniden yükleme içeren küçük bir LLM training smoke test çalıştırır.
5. Görüntü tensor'ları kullanan küçük bir Vision training smoke test çalıştırır.
6. Repository validation çalıştırır.
7. Kaynak bilgilerini ve pass/fail durumunu JSON olarak kaydeder.
8. Notebook'un yerel geliştirici makinesine bağlı olmadan temiz bir runtime'da çalışabildiğini doğrular.

Başarısız veya kısmi bir clone nedeniyle `/content/codingStandard` mevcutsa Notebook eksik dizini kaldırır ve temiz şekilde yeniden dener.

Testler bilerek küçük tutulmuştur. Başarılı bir Colab smoke test'i geliştirme standardını ve minimum çalıştırma yolunu doğrular; herhangi bir production modelinin mevcut Colab runtime kaynaklarına sığacağını garanti etmez.

## Önerilen kullanım

Environment profiler, memory smoke test'leri, training configuration veya Colab ile ilgili instruction'larda değişiklik yaptıktan sonra bu Notebook'u çalıştırın.

## İlgili doğrulamalar

- Tam doğrulama: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
