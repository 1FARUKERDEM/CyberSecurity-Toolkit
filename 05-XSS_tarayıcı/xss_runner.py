import requests
from bs4 import BeautifulSoup

url = "http://testphp.vulnweb.com/guestbook.php"

# 1. Payload'umuzu basit ve eşsiz tutalım
payload = "GEMINI_XSS_TEST_12345" 
# Not: <script> veya <b> etiketi koymadık. Sadece düz metin.
#      Sitenin bu metni yansıtıp yansıtmadığını görelim.

print(f"Saldırı Başlatılıyor: {url}")
print(f"Kullanılan Payload: {payload}")

try:
    # 2. YENİ ve DOĞRU Veri Sözlüğü
    #    HTML'de bulduğumuz 'name', 'text' ve 'submit' alanlarını kullanıyoruz.
    data_payload = {
        'name': payload,    # 'name' kutusuna payload'u koy
        'text': payload,    # 'text' (textarea) kutusuna payload'u koy
        'submit': 'add message' # 'submit' butonuna tıkla
    }

    print(f"\nForm bulundu... '{url}' adresine DOĞRU payload ile POST isteği gönderiliyor...")
    post_response = requests.post(url, data=data_payload)

    # 3. YANITI KONTROL ET
    if payload in post_response.text:
        print("\n-------------------------------------------")
        print(">>> AÇIK BULUNDU! (Reflected XSS) <<<")
        print(f">>> Gönderilen '{payload}' metni, sayfa kaynağında geri yansıdı.")
        print("-------------------------------------------")
    else:
        print("\nAçık bulunamadı. Payload kayboldu.")

except requests.exceptions.RequestException as e:
    print(f"Bağlantı hatası: {e}")