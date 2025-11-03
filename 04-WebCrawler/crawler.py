import requests
from bs4 import BeautifulSoup 

url = "http://example.com"

print(f"Taranıyor: {url}")

try:
    response = requests.get(url, timeout=3)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        linkler = soup.find_all('a')

        print(f"\nBulunan Linkler ({len(linkler)} adet):")
        
        # 6. --- GÜNCELLENEN DÖNGÜ BURASI ---
        for link in linkler:
            # 'link' bir etiket nesnesidir. 
            # .get('href') ile içindeki 'href' özelliğinin (attribute) değerini alırız.
            href = link.get('href')
            
            # Bazen linkler boştur (href=None) veya javascript kodudur.
            # Şimdilik sadece 'None' olmayanları (boş olmayanları) yazdıralım.
            if href:
                print(href) # Artık tüm etiketi değil, SADECE 'href' değerini yazdır

    else:
        print(f"Hata: Sayfa bulunamadı (Durum Kodu: {response.status_code})")

except requests.exceptions.RequestException as e:
    print(f"Bağlantı hatası: {e}")