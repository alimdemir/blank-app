import random
import numpy as np

# Futbol oyuncusu sinifi
class FutbolOyuncusu:
    def __init__(self, isim, overall, fiyat):
        self.isim = isim
        self.overall = overall
        self.fiyat = fiyat

# Takim sinifi
class Takim:
    def __init__(self, isim, para):
        self.isim = isim
        self.para = para
        self.oyuncular = []

    def oyuncu_satinal(self, oyuncu):
        if self.para >= oyuncu.fiyat:
            self.oyuncular.append(oyuncu)
            self.para -= oyuncu.fiyat
            print(f"{oyuncu.isim} oyuncusu {self.isim} takimina transfer edildi!")
        else:
            print("Yeterli paraniz yok!")

# Oyuncu olusturma fonksiyonu
def oyuncu_olustur():
    isim = input("Oyuncunun ismini girin: ")
    while True:
        try:
            overall = int(input("Oyuncunun overall gucunu (1-100 arasi) girin: "))
            if 1 <= overall <= 100:
                break
            else:
                print("Lutfen 1 ile 100 arasinda bir deger girin.")
        except ValueError:
            print("Lutfen gecerli bir sayi girin.")
    
    fiyat = overall * 100_000
    return FutbolOyuncusu(isim, overall, fiyat)

# Takimlar arasinda mac yapma fonksiyonu
def takimlar_arasi_mac(takim1, takim2):
    print(f"\nMac Basliyor: {takim1.isim} vs {takim2.isim}!")

    # Takim gücünü hesapla
    takim1_gucu = sum([oyuncu.overall for oyuncu in takim1.oyuncular]) / len(takim1.oyuncular)
    takim2_gucu = sum([oyuncu.overall for oyuncu in takim2.oyuncular]) / len(takim2.oyuncular)
    
    # Gol sayısını belirle
    gol_sayisi1 = np.random.poisson(takim1_gucu / 20)
    gol_sayisi2 = np.random.poisson(takim2_gucu / 20)

    # Gol atan oyuncuları belirleme
    gol_atan_oyuncular1 = []
    gol_atan_oyuncular2 = []

    for _ in range(gol_sayisi1):
        # Ağırlıklı seçim: overall değerine göre oyuncu seç
        oyuncu = random.choices(takim1.oyuncular, weights=[oyuncu.overall for oyuncu in takim1.oyuncular])[0]
        gol_atan_oyuncular1.append(oyuncu)

    for _ in range(gol_sayisi2):
        # Ağırlıklı seçim: overall değerine göre oyuncu seç
        oyuncu = random.choices(takim2.oyuncular, weights=[oyuncu.overall for oyuncu in takim2.oyuncular])[0]
        gol_atan_oyuncular2.append(oyuncu)

    # Sonuçları yazdır
    print(f"{takim1.isim} Skoru: {gol_sayisi1} - Gol atanlar: {[oyuncu.isim for oyuncu in gol_atan_oyuncular1]}")
    print(f"{takim2.isim} Skoru: {gol_sayisi2} - Gol atanlar: {[oyuncu.isim for oyuncu in gol_atan_oyuncular2]}")
    
    if gol_sayisi1 > gol_sayisi2:
        print(f"\nKazanan: {takim1.isim}!")
    elif gol_sayisi1 < gol_sayisi2:
        print(f"\nKazanan: {takim2.isim}!")
    else:
        print("\nMac Berabere!")

# Transfermarkt'tan oyuncu silme fonksiyonu
def transfermarkt_sil(oyuncu, transfermarkt):
    transfermarkt.remove(oyuncu)

# Transfermarkt'taki oyuncuları listeleme
def transfermarkt_listele(transfermarkt):
    if not transfermarkt:
        print("Transfermarkt'ta hic oyuncu yok.")
    else:
        print("\nTransfermarkt:")
        for i, oyuncu in enumerate(transfermarkt):
            print(f"{i+1}. {oyuncu.isim} (Overall: {oyuncu.overall}, Fiyat: {oyuncu.fiyat} €)")

# Takim kurma fonksiyonu
def takim_olustur():
    isim = input("Takimin ismini girin: ")
    while True:
        try:
            para = int(input("Takimin bütçesini girin (minimum 1 milyon €): "))
            if para >= 1_000_000:
                break
            else:
                print("Bütçe en az 1 milyon € olmalı.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
    
    return Takim(isim, para)

# Menu
def menu():
    oyuncular = []
    transfermarkt = []
    takimlar = []
    
    while True:
        print("\n1. Oyuncu Olustur")
        print("2. Transfermarkt'i Gor")
        print("3. Takim Kur")
        print("4. Oyuncu Satin Al")
        print("5. Mac Yap")
        print("6. Cikis")
        
        secim = input("Secenegi girin: ")
        
        if secim == "1":
            oyuncu = oyuncu_olustur()
            oyuncular.append(oyuncu)
            transfermarkt.append(oyuncu)
            print(f"{oyuncu.isim} oyuncusu olusturuldu ve Transfermarkt'a eklendi!")
        
        elif secim == "2":
            transfermarkt_listele(transfermarkt)
        
        elif secim == "3":
            takim = takim_olustur()
            takimlar.append(takim)
            print(f"{takim.isim} takimi kuruldu!")
        
        elif secim == "4":
            if not takimlar:
                print("Oyuncu satin almak icin oncelikle bir takim kurmalisiniz!")
            elif not transfermarkt:
                print("Transfermarkt'ta satilik oyuncu yok!")
            else:
                transfermarkt_listele(transfermarkt)
                takim_index = int(input("Hangi takim oyuncu satin alacak? (Takim numarasini girin): ")) - 1
                takim = takimlar[takim_index]
                
                oyuncu_index = int(input("Satin alinacak oyuncunun numarasini girin: ")) - 1
                oyuncu = transfermarkt[oyuncu_index]
                
                takim.oyuncu_satinal(oyuncu)
                if oyuncu in takim.oyuncular:
                    transfermarkt_sil(oyuncu, transfermarkt)
        
        elif secim == "5":
            if len(takimlar) < 2:
                print("Mac yapabilmek icin en az iki takim olusturmalisiniz!")
            else:
                print("Takimlar:")
                for i, takim in enumerate(takimlar):
                    print(f"{i+1}. {takim.isim} - Oyuncu Sayisi: {len(takim.oyuncular)}")
                
                takim1_index = int(input("Birinci takim numarasini secin: ")) - 1
                takim2_index = int(input("Ikinci takim numarasini secin: ")) - 1
                
                takim1 = takimlar[takim1_index]
                takim2 = takimlar[takim2_index]
                
                takimlar_arasi_mac(takim1, takim2)
        
        elif secim == "6":
            print("Cikis yapiliyor.")
            break
        
        else:
            print("Gecersiz secenek, lutfen tekrar deneyin.")

# Programi baslat
menu()
