import socket

# --- KULLANICIDAN VERİ ALMA ---
# 1. Kullanıcıya hangi IP'yi taramak istediğini sor.
hedef_ip = input("Taranacak IP Adresi : ")

# 2. Port aralığını sor (Yeni ekledik!)
baslangic_port = int(input("Başlangıç Portu : "))
bitis_port = int(input("Bitiş Portu ): "))
# ---------------------------------

print(f"\n{hedef_ip} adresindeki {baslangic_port} - {bitis_port} arası portlar taranıyor...")

# 3. FOR DÖNGÜSÜ BURADA BAŞLIYOR
#    'port' adında bir değişken oluştur ve 'baslangic_port'tan 'bitis_port + 1'e kadar
#    (çünkü Python'da son sayı dahil edilmez) her sayıyı sırayla ona ata.
for port in range(baslangic_port, bitis_port + 1):

    # 4. AŞAĞIDAKİ KODUN TAMAMI, DÖNGÜNÜN "İÇİNDE" (GİRİNTİLİ)
    #    Bu kod, her port numarası için TEKRAR TEKRAR çalışacak.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 5. Zaman aşımı ekleyelim (Tarama çok yavaşlamasın diye)
        #    Eğer 1 saniye içinde cevap alamazsa, kapalı say.
        s.settimeout(1) 
        
        # 6. 'port' değişkenini kullan (artık 'hedef_port' değil)
        s.connect((hedef_ip, port))
        
        # 7. Sadece AÇIK olanları ekrana yazdır (Kapalılar sessiz kalsın)
        print(f"Port {port} AÇIK!")
        s.close()

    except:
        # 8. Hata verirse (Kapalı veya Zaman Aşımı) HİÇBİR ŞEY YAPMA,
        #    sadece döngüye devam et. (Buna 'pass' denir)
        pass

print("\nTarama tamamlandı.")