

### Önemli Özellikler:

- **Çoklu Giriş Modları:** Kullanıcılar GPT-4 ile metin yazarak, konuşarak veya ekran görüntüsü paylaşarak etkileşim kurabilirler.
- **Sesli Konuşma:** ElevenLabs API'si kullanılarak, GPT-4'ün yanıtları gerçekçi bir şekilde seslendirilir ve kullanıcıya dinletilir.
- **Whisper Entegrasyonu:** Konuşmadan metne dönüştürme işlemi için OpenAI'nin Whisper modeli kullanılır.
- **Ekran Görüntüsü Analizi:** Kullanıcılar ekran görüntülerini paylaşabilir ve GPT-4'ten içerik hakkında bilgi isteyebilirler.
- **Kolay Kullanım:** Basit bir komut satırı arayüzü ile kullanıcı dostu bir deneyim sunar.

## Gereksinimler

- Python 3.7+
- Gerekli Python Paketleri: Aşağıdaki komutla gerekli paketler yüklenebilir:
    ```bash
    pip install -r requirements.txt
    ```
- API Anahtarları:
  - **OpenAI API Anahtarı:** GPT-4 modeline erişmek için gereklidir.
  - **ElevenLabs API Anahtarı:** Metinden konuşmaya dönüştürme için gereklidir (isteğe bağlı).

## Kurulum

1. Projeyi klonlayın veya zip dosyasını indirin ve dosyaları çıkartın.
2. `requirements.txt` dosyasındaki paketleri yükleyin.
3. `.env` dosyasını oluşturun ve API anahtarlarınızı aşağıdaki gibi ekleyin:
    ```plaintext
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY"
    VOICE_ID="CHOOSEN_VOICE_ID"
    ```

## Kullanım

1. Bir terminal penceresi açın ve proje dizinine gidin.
2. Uygulamayı başlatmak için aşağıdaki komutu çalıştırın:
   bash
    python customgpt.py
    ```

## Uygulama Arayüzü

Uygulama başlatıldığında, kullanıcılara aşağıdaki giriş seçenekleri sunulur:
- **Yazı (1):** Metin girişi yapmak için bu seçeneği kullanın.
- **Konuşma (2):** Mikrofonunuzla konuşarak GPT-4 ile etkileşim kurmak için bu seçeneği kullanın.
- **Ekran Görüntüsü (3):** Ekran görüntüsü alıp GPT-4'ten analiz etmesini istemek için bu seçeneği kullanın.

## Fonksiyon Açıklamaları

- **get_user_choice():** Kullanıcının hangi giriş modunu kullanmak istediğini sorar (yazı, konuşma, ekran görüntüsü).
- **get_user_input():** Mikrofondan ses kaydı yapar ve Whisper modelini kullanarak metne dönüştürür.
- **text_to_speech_input_streaming():** ElevenLabs API'sini kullanarak metni sese dönüştürür ve yayınlar.
- **handle_speech_input():** Kullanıcıdan ses girişi alır, GPT-4 ile etkileşime geçer ve yanıtı seslendirir.
- **chat_completion():** Verilen metin girişi ve geçmiş mesajları kullanarak OpenAI GPT-4 API'sine istek gönderir ve yanıtı alır.
- **capture_screen():** Ekran görüntüsü alır ve base64 formatına dönüştürür.
- **text_chunker():** Uzun metinleri, cümleleri bölmeden daha küçük parçalara ayırır.
- **stream():** Ses verilerini mpv oynatıcı kullanarak yayınlar.
- **handle_text_input():** Kullanıcıdan metin girişi alır ve GPT-4 ile etkileşime geçer.
- **handle_screenshot_input():** Ekran görüntüsü alır, kullanıcıdan girdi ister ve GPT-4'ten analiz etmesini ister.
- **main():** Ana uygulama döngüsünü yönetir.

## Örnek Kullanım Senaryoları

- **Yaratıcı Yazma:** Hikaye fikirleri üretmek, şiir yazmak veya senaryo tasarlamak için GPT-4'ün yaratıcılığından yararlanın.
- **Kodlama Yardımcısı:** Kodlama sırasında takıldığınız noktalarda GPT-4'ten yardım alın, kod örnekleri isteyin veya hatalarınızı düzeltin.
- **Dil Öğrenme:** GPT-4 ile farklı dillerde konuşma pratiği yapın, gramer kurallarını öğrenin veya metin çevirileri yapın.
- **Oyun Geliştirme:** Oyunlar için diyaloglar, karakterler veya hikaye unsurları oluşturmak için GPT-4'ü kullanın.
- **Eğlence:** GPT-4 ile sohbet edin, şakalar yapın veya ilginç bilgiler edinin.

## Sınırlamalar

- **API Sınırlamaları:** Hem OpenAI hem de ElevenLabs API'lerinin kullanım sınırlamaları vardır.
- **Gerçek Zamanlı Performans:** Konuşma tanıma ve metinden konuşmaya dönüştürme işlemleri gerçek zamanlı olarak gerçekleşse de, internet bağlantınızın hızı ve API yanıt süreleri performansı etkileyebilir.
- **Doğruluk:** Whisper modeli ve GPT-4, etkileyici bir doğruluk sunsa da, her zaman mükemmel sonuçlar vermeyebilir.

## Gelecek Geliştirmeler

- **Bellek Yönetimi:** Önceki konuşmaları kaydetme ve GPT-4'ün daha tutarlı ve bağlamsal olarak alakalı yanıtlar vermesini sağlama.
- **Grafik Kullanıcı Arayüzü (GUI):** Daha kullanıcı dostu bir deneyim için grafik arayüz geliştirme.

## Katkıda Bulunma

Projeye katkıda bulunmak isterseniz, lütfen fork edin, değişikliklerinizi yapın ve bir pull request gönderin. Her türlü katkıya açığız!

     pip uninstall PyQt5-sip PyQt5-Qt5 PyQtWebEngine

     pip install PyQt5
