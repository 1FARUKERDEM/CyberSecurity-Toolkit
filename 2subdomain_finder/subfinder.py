import requests

# 1. Kullanıcıdan ana domaini al
domain = input(" Taranacak Domain : ")

# 2. wordlist.txt dosyasını 'okuma' modunda (r) aç
try:
    with open("wordlist.txt", "r") as f:
        # 3. Dosyadaki her satır için bir FOR döngüsü başlat
        for satir in f:
            # 4. 'satir' değişkeni "admin\n" gibi sonunda bir boşluk/yeni satır karakteri (\n) içerir.
            #    .strip() fonksiyonu bu görünmez karakterleri temizler.
            subdomain = satir.strip()

            # 5. Tam URL'yi oluştur
            url = f"https://{subdomain}.{domain}"

            # 6. ÇEKİRDEK MANTIK (Aşama 3'ten aynen kopyaladık)
            try:
                requests.get(url, timeout=3)
                print(f"[+] Bulundu: {url}")
            except:
                # Hata verirse (Bulunamazsa) sessiz kal, hiçbir şey yazdırma
                pass 

    print("\nTarama tamamlandı.")

except FileNotFoundError:
    print("\nHATA: wordlist.txt dosyası bulunamadı.")
    print("Lütfen subfinder.py ile aynı klasörde olduğundan emin olun.")