# My CyberSecurity Toolkit

Bu repo, siber güvenlik ve etik hacker'lık öğrenme yolculuğumun bir parçası olarak geliştirdiğim temel araçları içermektedir.

Bu projelerin amacı, Nmap, ffuf veya Burp Suite gibi profesyonel araçların yerini almak **değildir**. Amaç, bu araçların *arkasında yatan temel mantığı* anlamaktır. Her proje, Python kütüphanelerini (Socket, Requests, BeautifulSoup) ve temel güvenlik konseptlerini öğrenmek için (rehberlik eşliğinde) sıfırdan yazılmıştır.

## Projeler

* **`01-PortTarayici`**: `socket` kütüphanesini ve `try...except` bloklarını kullanarak TCP bağlantı mantığını gösteren basit bir port tarayıcı.
* **`02-SubdomainFinder`**: Bir kelime listesi ve `requests` kütüphanesi kullanarak alt alan adlarını keşfeden bir araç.
* **`03-Dirbuster`**: `requests` ve `response.status_code` kontrolü ile gizli dizinleri bulan bir kaba kuvvet aracı.
* **`04-WebCrawler`**: `BeautifulSoup` kullanarak bir sayfanın HTML'ini ayrıştıran (parse) ve tüm `<a>` (link) etiketlerini çıkaran basit bir örümcek.
* **`05-XSS_tarayıcı`**: `requests.post` kullanarak bir formdaki temel yansıyan (reflected) XSS açıklarını test eden bir script.