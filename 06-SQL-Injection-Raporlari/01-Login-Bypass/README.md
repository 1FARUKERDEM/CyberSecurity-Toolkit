# Proje 6.1: SQL Injection (SQLi) - Login Bypass Raporu

Bu rapor, PortSwigger Web Security Academy'deki "SQL injection vulnerability allowing login bypass" (Giriş atlamaya izin veren SQL enjeksiyonu açığı) laboratuvarının çözüm sürecini belgelemektedir.

**Platform:** PortSwigger Web Security Academy
**Araçlar:** Burp Suite Community Edition

---

## 1. Zafiyet Analizi (Vulnerability Analysis)

Hedef laboratuvar, bir kullanıcı giriş (login) formu içermekteydi. Bu tür formlar, sunucu tarafında genellikle aşağıdaki gibi bir SQL sorgusu oluşturur:

```sql
SELECT * FROM users WHERE username = '[GİRİLEN_KULLANICI_ADI]' AND password = '[GİRİLEN_ŞİFRE]'
Zafiyet, sunucunun kullanıcıdan gelen [GİRİLEN_KULLANICI_ADI] girdisini doğrudan (temizlemeden veya doğrulamadan) bu SQL sorgusuna dahil etmesinden kaynaklanmaktadır. Bu, sorgunun yapısını manipüle etmemize olanak tanır.

2. Saldırı Süreci (Attack Process)
Hedef: administrator kullanıcısının şifresini bilmeden giriş yapmak.

Adım 1: Trafiği Yakalama Burp Suite'in dahili tarayıcısı kullanılarak laboratuvarın /login sayfası açıldı. Burp Proxy > Intercept (Yakalama) özelliği "on" (açık) konuma getirildi.

Adım 2: Form Verilerini Doldurma Giriş formuna aşağıdaki payload (saldırı yükü) girildi:

Username: administrator' OR 1=1--

Password: 123 (Girilen şifrenin bir önemi yoktur)

Adım 3: İsteği Manipüle Etme (Burp Suite) "Login" butonuna tıklandığında, giden POST isteği Burp Suite tarafından yakalandı. username parametresinin saldırı yükümüzü içerdiği doğrulandı.

3. Payload Analizi: ' OR 1=1--
Bu payload, sunucunun SQL sorgusunu şu şekilde bozmak için tasarlanmıştır:

SQL

/* Orijinal Sorgu (Sunucunun Planı): */
SELECT * FROM users WHERE username = 'administrator' OR 1=1--' AND password = '123'

/* Veritabanının Yorumladığı Sorgu: */
-- 1. ' (Tek Tırnak):
--    'administrator' metnini kapatır.
SELECT * FROM users WHERE username = 'administrator'

-- 2. OR 1=1 (Mantıksal Kandırmaca):
--    Yeni bir mantıksal koşul ekler. 1=1 her zaman DOĞRU (TRUE) olduğundan, WHERE koşulu her zaman başarılı olur.
OR 1=1

-- 3. -- (Yorum Satırı):
--    SQL'de "çift tire", satırın geri kalanını yorum olarak işaretler ve yok sayar.
--    Bu, sorgunun geri kalan (ve bizim için sorunlu olan) ' AND password = '123' kısmını çöpe atar.
--' AND password = '123'
Sonuç olarak, veritabanı "bana users tablosundaki, kullanıcı adı 'administrator' OLAN VEYA 1=1 (HER ZAMAN DOĞRU) OLAN ilk kullanıcıyı ver" emrini çalıştırdı ve administrator olarak giriş yapıldı.

4. Sonuç (Result)
Saldırı başarılı oldu, administrator kullanıcısı olarak giriş yapıldı ve laboratuvar çözüldü.

(Opsiyonel: Buraya "Congratulations, you solved the lab!" yazısının ekran görüntüsünü ekleyebilirsin.)

5. Düzeltme Yöntemi (Remediation)
Bu tür bir saldırıyı önlemenin en etkili yolu, kullanıcı girdisini doğrudan SQL sorgularına dahil etmekten kaçınmaktır. Bunun yerine Parameterized Queries (Hazırlanmış İfadeler) kullanılmalıdır. Bu yöntemde, sorgunun yapısı ve kullanıcının verisi veritabanına ayrı ayrı gönderilir, böylece kullanıcının girdiği ' veya -- gibi karakterler "komut" olarak değil, "metin" olarak algılanır.


---