import requests

# 1. Kullanıcıdan ana domaini al
domain = input("Taranacak Ana Domain (örn: google.com): ")

# 2. Protokolü ekle (https://)
#    Proje 2'de bunu URL oluştururken yapıyorduk, şimdi başa aldık.
base_url = f"https://{domain}" 

try:
    # 3. 'common_dirs.txt' dosyasını 'okuma' modunda (r) aç
    with open("common_dirs.txt", "r") as f:
        # 4. Dosyadaki her satır için bir FOR döngüsü başlat
        for satir in f:
            # 5. Satır sonu boşluklarını temizle
            directory = satir.strip()

            # 6. !!!!!!! TEK FARK BURADA !!!!!!!
            #    Proje 2: url = f"https://{subdomain}.{domain}"
            #    Proje 3: url = f"{base_url}/{directory}"
            #    (Yani google.com/admin, google.com/login vs.)
            url = f"{base_url}/{directory}"

            # 7. ÇEKİRDEK MANTIK (Aşama 3'ten aynen kopyaladık)
            try:
                # 8. Not: allow_redirects=False ekledik.
                #    Eğer /admin adresi /login'e yönlendiriliyorsa,
                #    bunu "bulundu" saymamak için. Sadece direkt (200 OK)
                #    cevapları istiyoruz (şimdilik).
                response = requests.get(url, timeout=3, allow_redirects=False)
                
                # 9. HTTP Durum Kodunu kontrol et. 200 = "Başarılı/OK" demektir.
                if response.status_code == 200:
                    print(f"[+] Bulundu: {url} (Durum Kodu: 200)")
                
                # İsteğe bağlı: Diğer ilginç kodları da gösterebilirsin
                # elif response.status_code == 403:
                #    print(f"[!] Yasaklanmış: {url} (Durum Kodu: 403) - Var ama giriş izni yok.")

            except requests.exceptions.RequestException:
                # Hata verirse (Bulunamazsa, timeout vs.) sessiz kal
                pass 

    print("\nTarama tamamlandı.")

except FileNotFoundError:
    print(f"\nHATA: common_dirs.txt dosyası bulunamadı.")
    print("Lütfen dirbuster.py ile aynı klasörde olduğundan emin olun.")