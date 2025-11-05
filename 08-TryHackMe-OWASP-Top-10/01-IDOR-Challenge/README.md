# Proje 8.1: TryHackMe OWASP Top 10 - IDOR Çözüm Raporu

Bu rapor, TryHackMe'deki "OWASP Top 10 2021" odasında yer alan **"Görev 3: Kırık Erişim Kontrolü (IDOR Challenge)"** bölümünün çözüm sürecini belgelemektedir.

Bu laboratuvar, temel keşif (reconnaissance) ve hata ayıklamanın (debugging) bir zafiyeti ortaya çıkarmada ne kadar kritik olduğunu göstermektedir.

**Platform:** TryHackMe (OWASP Top 10 2021 Odası)
**Araçlar:**  Web Tarayıcı, OpenVPN

---

## 1. İlk Analiz ve Keşif (Reconnaissance)
Görevin açıklamasında, hedef IP (`http://[IP_ADRESİ]`) üzerinde belirli kimlik bilgileriyle (`noot`/`test1234`) giriş yapılması isteniyordu.


noot/test1234 kimlik bilgileri bu yeni sayfada denendiğinde giriş başarılı oldu ve noot kullanıcısının not listesi ("lots of chocolate!") sayfası açıldı.


3. Zafiyeti Sömürme (IDOR Saldırısı)
noot olarak giriş yapıldığında, tarayıcının adres çubuğunda (URL), o notları tanımlayan bir ID parametresi görüldü (örn: .../notes.php?id=[SAYI]).

Görevin açıklamasındaki IDOR teorisine dayanarak, bu id parametresi manipüle edildi:

?id=2: Sophie'nin notları (Başarılı IDOR)

?id=3: "Doğru yoldasın!" ipucu.

?id=4: Mark'ın notları (Başarılı IDOR)

?id=5: Kritik İpucu: "Hint: Do note_ids start from 1? Maybe go lower ;)" (İpucu: ID'ler 1'den mi başlıyor? Belki daha da aşağıya inmelisin ;))

4. Sonuç (Bayrağı Alma)
id=5'teki "go lower" (daha aşağı in) ipucu takip edildi. 1'den daha düşük olan 0 (sıfır) denendi.

Final Payload: ?id=0

Sonuç: Bu payload, admin kullanıcısının notlarını ve flag{fivefourthree} bayrağını ortaya çıkardı.