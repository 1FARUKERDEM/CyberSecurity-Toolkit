# Proje 7.2: Cross-Site Scripting (XSS) - Kalıcı (Stored) XSS Raporu

Bu rapor, PortSwigger Web Security Academy'deki "Stored XSS into HTML context with nothing encoded" (HTML içeriğine depolanan, hiçbir şeyin kodlanmadığı Stored XSS) laboratuvarının çözüm sürecini belgelemektedir.

**Platform:** PortSwigger Web Security Academy

---

## 1. Zafiyet Analizi (Vulnerability Analysis)

Bu laboratuvar, bir blog sitesindeki "Yorum Bölümü" (Comment) üzerinde Stored (Kalıcı) XSS açığı barındırmaktaydı.

Zafiyet, "Reflected XSS"ten (Proje 7.1) çok daha tehlikelidir.

* **Reflected XSS'te,** payload (saldırı kodu) sadece o linke tıklayan kurbana "yansır" ve kaybolur.
* **Stored XSS'te,** payload, sunucunun **veritabanına (database) kaydedilir.**

Bu zafiyet, sunucunun kullanıcıdan "Yorum" olarak aldığı girdiyi, veritabanına kaydetmeden önce **temizlememesinden (Input Sanitization)** kaynaklanmaktadır.

## 2. Saldırı Süreci (Attack Process)

**Hedef:** Sitenin veritabanına kalıcı bir XSS payload'u yerleştirmek. Bu sayede, o blog yazısını ziyaret eden *her kullanıcının* (veya adminin) tarayıcısında bu kodun otomatik olarak çalışmasını sağlamak.

**Adım 1: Açık Girdinin Bulunması**
Sitedeki blog yazılarından birine gidildi ve sayfanın altındaki "Leave a comment" (Yorum Bırak) formu bulundu. Bu form, veritabanına veri kaydeden "giriş noktamızdı".

**Adım 2: Payload Enjeksiyonu ve Depolama**
Formdaki "Comment" (Yorum) `<textarea>` kutusuna, standart XSS test payload'u girildi:

```html
<script>alert(1)</script>
(Diğer form alanları test, test@test.com gibi sahte verilerle dolduruldu.)

Adım 3: Saldırıyı Tetikleme "Post Comment" (Yorumu Gönder) butonuna tıklandığında, sayfa yenilendi ancak alert() pop-up'ı çalışmadı. Bu normaldi, çünkü kodumuz o an sadece veritabanına kaydedilmişti.

Blog yazısı sayfası tekrar ziyaret edildiğinde (veya yenilendiğinde), saldırı tetiklendi.

3. Payload Analizi (Stored XSS vs. Reflected XSS)
Bu saldırı, bir "etkileşimli" (dinamik) sitenin nasıl çalıştığını sömürür:

Hacker (Biz): Yorum kutusuna <script>alert(1)</script> yazar ve gönderir.

Sunucu (Açık Kapı): Bu tehlikeli girdiyi kontrol etmez (temizlemez) ve olduğu gibi veritabanına kaydeder.

Kurban (Normal Kullanıcı): Bir gün sonra aynı blog yazısını ziyaret eder.

Sunucu (Açık Kapı): Kurbana HTML sayfasını oluştururken, "Yorumları göster" komutuyla veritabanına gider.

Veritabanı: Sunucuya bizim zehirli yorumumuzu (<script>alert(1)</script>) geri verir.

Sunucu: Bu zehirli metni, olduğu gibi kurban için oluşturduğu HTML'e basar: ...<p>Harika bir yazı!</p><p><script>alert(1)</script></p>...

Kurbanın Tarayıcısı: Bu HTML'i okur, <script> etiketini görür ve alert(1) komutunu otomatik olarak çalıştırır.

4. Sonuç (Result)
Sayfa her ziyaret edildiğinde alert(1) pop-up'ı tetiklendi ve laboratuvar çözüldü. Bu, saldırının "kalıcı" (persistent) olduğunu ve o sayfayı ziyaret eden herkesi etkileyeceğini kanıtlar.

5. Düzeltme Yöntemi (Remediation)
Bu zafiyeti önlemek için, kullanıcıdan gelen veri veritabanına kaydedilmeden önce mutlaka "Input Sanitization" (Girdi Temizleme) işleminden geçirilmelidir. Sunucu, <script> veya onerror gibi tehlikeli HTML etiketlerini ve JavaScript olaylarını tamamen söküp atmalı veya (Proje 7.1'deki gibi) &lt;script&gt; olarak kodlamalıdır.