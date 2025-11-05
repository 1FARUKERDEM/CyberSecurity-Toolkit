# Proje 7.1: Cross-Site Scripting (XSS) - Yansıyan (Reflected) XSS Raporu

Bu rapor, PortSwigger Web Security Academy'deki "Reflected XSS into HTML context with nothing encoded" (HTML içeriğine yansıyan, hiçbir şeyin kodlanmadığı Reflected XSS) laboratuvarının çözüm sürecini belgelemektedir.

**Platform:** PortSwigger Web Security Academy
**Araçlar:** Sadece Web Tarayıcısı

---

## 1. Zafiyet Analizi (Vulnerability Analysis)

Hedef laboratuvar, (muhtemelen bir blog veya e-ticaret sitesi) üzerinde bir "Search" (Arama) kutusu barındırmaktaydı.

Zafiyet, bu arama kutusuna girilen kullanıcı girdisinin, sunucu tarafından **hiçbir temizleme (sanitization) veya kodlama (encoding) işlemine tabi tutulmadan** doğrudan sayfanın HTML yanıtına geri "yansıtılmasından" kaynaklanmaktadır.

**Keşif Adımı:**
1.  Arama kutusuna `test123` gibi zararsız, eşsiz bir metin girildi.
2.  Sunucu, "0 results found for 'test123'" (test123 için 0 sonuç bulundu) şeklinde bir yanıt döndürdü.
3.  Sayfa kaynağı incelendiğinde, `test123` metninin HTML'e ham (raw) olarak yerleştirildiği görüldü.

Bu "yansıtma" (reflection) davranışı, tarayıcıya metin yerine çalıştırılabilir bir komut (JavaScript) göndermek için bir kapı açmaktadır.

## 2. Saldırı Süreci (Attack Process)

**Hedef:** Sitenin güvenlik açığını kanıtlamak için tarayıcıda basit bir `alert()` pop-up penceresi çalıştırmak.

**Adım 1: Payload Enjeksiyonu**
Arama kutusuna bu kez `test123` metni yerine, standart bir XSS test payload'u (saldırı yükü) girildi:

```html
<script>alert(1)</script>
Harika! VSCode'da o boş README.md dosyası (.../01-Reflected-XSS-Temel/README.md) şu an açık ve seni bekliyor.

İşte o "FBI pop-up" (<script>alert(1)</script>) saldırısını anlatan profesyonel rapor taslağı.

Aşama 1: Raporu Kopyala ve Yapıştır
Aşağıdaki kutunun içindeki metnin tamamını kopyala ve o boş README.md dosyana yapıştır.

Markdown

# Proje 7.1: Cross-Site Scripting (XSS) - Yansıyan (Reflected) XSS Raporu

Bu rapor, PortSwigger Web Security Academy'deki "Reflected XSS into HTML context with nothing encoded" (HTML içeriğine yansıyan, hiçbir şeyin kodlanmadığı Reflected XSS) laboratuvarının çözüm sürecini belgelemektedir.

**Platform:** PortSwigger Web Security Academy
**Araçlar:** Sadece Web Tarayıcısı

---

## 1. Zafiyet Analizi (Vulnerability Analysis)

Hedef laboratuvar, (muhtemelen bir blog veya e-ticaret sitesi) üzerinde bir "Search" (Arama) kutusu barındırmaktaydı.

Zafiyet, bu arama kutusuna girilen kullanıcı girdisinin, sunucu tarafından **hiçbir temizleme (sanitization) veya kodlama (encoding) işlemine tabi tutulmadan** doğrudan sayfanın HTML yanıtına geri "yansıtılmasından" kaynaklanmaktadır.

**Keşif Adımı:**
1.  Arama kutusuna `GEMINI123` gibi zararsız, eşsiz bir metin girildi.
2.  Sunucu, "0 results found for 'GEMINI123'" (GEMINI123 için 0 sonuç bulundu) şeklinde bir yanıt döndürdü.
3.  Sayfa kaynağı incelendiğinde, `GEMINI123` metninin HTML'e ham (raw) olarak yerleştirildiği görüldü.

Bu "yansıtma" (reflection) davranışı, tarayıcıya metin yerine çalıştırılabilir bir komut (JavaScript) göndermek için bir kapı açmaktadır.

## 2. Saldırı Süreci (Attack Process)

**Hedef:** Sitenin güvenlik açığını kanıtlamak için tarayıcıda basit bir `alert()` pop-up penceresi çalıştırmak.

**Adım 1: Payload Enjeksiyonu**
Arama kutusuna bu kez `GEMINI123` metni yerine, standart bir XSS test payload'u (saldırı yükü) girildi:

```html
<script>alert(1)</script>
Adım 2: Gramer Testi (Opsiyonel) Ayrıca, JavaScript gramerinin çalıştığını doğrulamak için alert("you hacked bro") gibi özel metinler de ' (tek tırnak) veya " (çift tırnak) içine alınarak test edildi ve başarıyla çalıştı.

3. Payload Analizi: <script>alert(1)</script>
Bu payload, sunucunun zafiyetini sömürmek için tasarlanmıştır:

Hacker (Biz): Arama kutusuna <script>alert(1)</script> yazar.

Sunucu (Açık Kapı): Bu girdiyi (hala bir metin sanarak) alır ve o an oluşturduğu HTML yanıtına ekler. Kurbana gönderilen HTML şöyle görünür: ...<p>0 results found for '<script>alert(1)</script>'</p>...

Tarayıcı (Kurban): Bu HTML'i okumaya başlar. <p> etiketini (metin) görür, ancak ardından gelen <script> etiketini gördüğü an durur.

Tarayıcı: "Bu bir metin değil! Bu, benim çalıştırmam gereken bir JavaScript komutu!" der.

Sonuç: Tarayıcı, komut olan alert(1)'i çalıştırır ve ekrana "1" yazan bir pop-up kutusu çıkarır.

4. Sonuç (Result)
Payload başarıyla enjekte edildi, tarayıcıda alert() pop-up'ı tetiklendi ve laboratuvar çözüldü.

(Opsiyonel: Buraya o "FBI" pop-up'ının ekran görüntüsünü ekleyebilirsin.)

5. Düzeltme Yöntemi (Remediation)
Bu zafiyeti önlemek için, kullanıcıdan gelen hiçbir veriye güvenilmemelidir. Sunucu tarafındaki kod, kullanıcı girdisini HTML'e basmadan önce mutlaka "Output Encoding" (Çıktı Kodlaması) işleminden geçirmelidir.

Örneğin, <script> girdisi şu hale getirilmelidir:

&lt;script&gt;

Bu "kodlanmış" metni gören tarayıcı, bunu "komut" olarak çalıştırmaz, ekrana sadece <script> yazısını basar ve saldırı etkisiz hale gelir.