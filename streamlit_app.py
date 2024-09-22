import streamlit as st
import pandas as pd
import random
import numpy as np

# Futbol oyuncusu sınıfı
class FutbolOyuncusu:
    def __init__(self, isim, overall, yas, fiyat):
        self.isim = isim
        self.overall = overall
        self.yas = yas
        self.fiyat = fiyat

# Takım sınıfı
class Takim:
    def __init__(self, isim, para):
        self.isim = isim
        self.para = para
        self.oyuncular = []

    def oyuncu_satinal(self, oyuncu):
        if self.para >= oyuncu.fiyat:
            self.oyuncular.append(oyuncu)
            self.para -= oyuncu.fiyat
            st.success(f"{oyuncu.isim} oyuncusu {self.isim} takımına transfer edildi!")
        else:
            st.error("Yeterli paranız yok!")

# Oyuncu fiyatlandırma fonksiyonu
def fiyat_belirle(overall, yas):
    if overall >= 90:
        fiyat = 200_000_000
    elif overall >= 80:
        fiyat = 100_000_000
    elif overall >= 70:
        fiyat = 50_000_000
    else:
        fiyat = 10_000_000
    
    if yas > 30:
        fiyat *= 0.8  # 30 yaş üstü oyuncular için %20 indirim
    
    return fiyat

# CSV'den oyuncu oluşturma fonksiyonu
def oyuncu_olustur(csv_data):
    oyuncular = []
    for _, row in csv_data.iterrows():
        isim = row['Name']
        overall = row['OVR']
        yas = row['Age']
        fiyat = fiyat_belirle(overall, yas)
        oyuncu = FutbolOyuncusu(isim, overall, yas, fiyat)
        oyuncular.append(oyuncu)
    return oyuncular

# Takımlar arası maç yapma fonksiyonu
def takimlar_arasi_mac(takim1, takim2):
    takim1_gucu = sum([oyuncu.overall for oyuncu in takim1.oyuncular]) / len(takim1.oyuncular)
    takim2_gucu = sum([oyuncu.overall for oyuncu in takim2.oyuncular]) / len(takim2.oyuncular)

    gol_sayisi1 = np.random.poisson(takim1_gucu / 20)
    gol_sayisi2 = np.random.poisson(takim2_gucu / 20)

    gol_atan_oyuncular1 = random.choices(takim1.oyuncular, weights=[oyuncu.overall for oyuncu in takim1.oyuncular], k=gol_sayisi1)
    gol_atan_oyuncular2 = random.choices(takim2.oyuncular, weights=[oyuncu.overall for oyuncu in takim2.oyuncular], k=gol_sayisi2)

    return gol_sayisi1, gol_sayisi2, gol_atan_oyuncular1, gol_atan_oyuncular2

# Streamlit uygulaması
def main():
    st.title("Futbol Menajerlik Oyunu")

    # CSV'den oyuncuları yükle
    csv_data = pd.read_csv('players_game.csv')
    oyuncular = oyuncu_olustur(csv_data)

    transfermarkt = oyuncular
    takimlar = []

    # Takım kurma
    if 'takimlar' not in st.session_state:
        st.session_state['takimlar'] = []

    st.sidebar.title("Menü")
    menu_secim = st.sidebar.selectbox("Seçenekler", ["Oyuncu Listesi", "Takım Kur", "Oyuncu Satın Al", "Maç Başlat"])

    if menu_secim == "Oyuncu Listesi":
        st.header("Transfermarkt'taki Oyuncular")
        if transfermarkt:
            for oyuncu in transfermarkt:
                st.write(f"{oyuncu.isim} - Overall: {oyuncu.overall}, Yaş: {oyuncu.yas}, Fiyat: {oyuncu.fiyat:.2f} €")
        else:
            st.write("Transfermarkt'ta oyuncu yok.")

    elif menu_secim == "Takım Kur":
        takim_ismi = st.text_input("Takımın ismi:")
        takim_butcesi = st.number_input("Takımın bütçesi (M €):", min_value=1, max_value=1000, value=50)
        
        if st.button("Takım Kur"):
            yeni_takim = Takim(takim_ismi, takim_butcesi * 1_000_000)
            st.session_state['takimlar'].append(yeni_takim)
            st.success(f"{takim_ismi} takımı başarıyla kuruldu!")

    elif menu_secim == "Oyuncu Satın Al":
        if not st.session_state['takimlar']:
            st.write("Önce bir takım kurmalısınız!")
        else:
            takim_secim = st.selectbox("Takım Seç", st.session_state['takimlar'], format_func=lambda x: x.isim)
            transfermarkt_listele = st.selectbox("Oyuncu Seç", transfermarkt, format_func=lambda x: f"{x.isim} - Overall: {x.overall}, Fiyat: {x.fiyat:.2f} €")
            
            if st.button("Oyuncu Satın Al"):
                takim_secim.oyuncu_satinal(transfermarkt_listele)
                transfermarkt.remove(transfermarkt_listele)

    elif menu_secim == "Maç Başlat":
        if len(st.session_state['takimlar']) < 2:
            st.write("Maç yapabilmek için en az 2 takım olmalı.")
        else:
            takim1 = st.selectbox("Birinci Takım", st.session_state['takimlar'], format_func=lambda x: x.isim)
            takim2 = st.selectbox("İkinci Takım", st.session_state['takimlar'], format_func=lambda x: x.isim)

            if st.button("Maç Başlat"):
                gol_sayisi1, gol_sayisi2, gol_atanlar1, gol_atanlar2 = takimlar_arasi_mac(takim1, takim2)
                st.write(f"Maç Skoru: {takim1.isim} {gol_sayisi1} - {gol_sayisi2} {takim2.isim}")

                st.write(f"{takim1.isim} Gol Atanlar: {[oyuncu.isim for oyuncu in gol_atanlar1]}")
                st.write(f"{takim2.isim} Gol Atanlar: {[oyuncu.isim for oyuncu in gol_atanlar2]}")

if __name__ == "__main__":
    main()
