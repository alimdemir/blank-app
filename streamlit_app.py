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
            return True
        else:
            return False

# Fiyat belirleme fonksiyonu (OVR ve yaşa göre)
def fiyat_belirle(overall, yas):
    yas_faktor = 1 - (yas - 20) * 0.05 if yas > 20 else 1  # Yaş faktörü
    base_fiyat = overall * 2_000_000  # Base fiyat overall'a göre belirlenir
    return max(500_000, base_fiyat * yas_faktor * 1.2)  # OVR'yi %20 daha etkili yap

# Oyuncu oluşturma fonksiyonu
def oyuncu_olustur(name, overall, yas):
    fiyat = fiyat_belirle(overall, yas)
    return FutbolOyuncusu(name, overall, yas, fiyat)

# Takımlar arası maç yapma fonksiyonu
def takimlar_arasi_mac(takim1, takim2):
    takim1_gucu = sum([oyuncu.overall for oyuncu in takim1.oyuncular]) / len(takim1.oyuncular)
    takim2_gucu = sum([oyuncu.overall for oyuncu in takim2.oyuncular]) / len(takim2.oyuncular)
    
    gol_sayisi1 = np.random.poisson(takim1_gucu / 20)
    gol_sayisi2 = np.random.poisson(takim2_gucu / 20)

    gol_atan_oyuncular1 = random.choices(takim1.oyuncular, weights=[oyuncu.overall for oyuncu in takim1.oyuncular], k=gol_sayisi1)
    gol_atan_oyuncular2 = random.choices(takim2.oyuncular, weights=[oyuncu.overall for oyuncu in takim2.oyuncular], k=gol_sayisi2)

    return gol_sayisi1, gol_sayisi2, gol_atan_oyuncular1, gol_atan_oyuncular2

# Transfermarkt'taki oyuncuları listeleme
def transfermarkt_listele(transfermarkt):
    if not transfermarkt:
        st.write("Transfermarkt'ta hiç oyuncu yok.")
    else:
        st.write("### Transfermarkt:")
        oyuncu_listesi = []
        for oyuncu in transfermarkt:
            fiyat_formatted = format(oyuncu.fiyat, ',.0f').replace(',', '.')  # Fiyatı formatla
            oyuncu_listesi.append([oyuncu.isim, oyuncu.overall, oyuncu.yas, f"{fiyat_formatted} €"])

        oyuncu_df = pd.DataFrame(oyuncu_listesi, columns=["İsim", "Overall", "Yaş", "Fiyat"])
        st.table(oyuncu_df)

# Takım bilgilerini gösterme fonksiyonu
def takim_bilgilerini_goster(takimlar):
    st.write("### Takım Bilgileri:")
    for takim in takimlar:
        st.write(f"**Takım İsmi:** {takim.isim}")
        st.write(f"**Bütçe:** {format(takim.para, ',.0f').replace(',', '.')} €")
        if takim.oyuncular:
            st.write("Oyuncular:")
            for oyuncu in takim.oyuncular:
                fiyat_formatted = format(oyuncu.fiyat, ',.0f').replace(',', '.')
                st.write(f"- {oyuncu.isim} (Overall: {oyuncu.overall}, Yaş: {oyuncu.yas}, Fiyat: {fiyat_formatted} €)")
        else:
            st.write("Bu takımda hiç oyuncu yok.")
        st.write("---")

# Veri setinden oyuncuları yükleyip transfermarkt'a ekleyen fonksiyon
def csvden_oyuncu_yukle(transfermarkt, dosya_adi):
    df = pd.read_csv(dosya_adi)
    for _, row in df.iterrows():
        isim = row['Name']
        overall = int(row['OVR'])
        yas = int(row['Age'])
        oyuncu = oyuncu_olustur(isim, overall, yas)
        transfermarkt.append(oyuncu)

# Main Streamlit uygulaması
def main():
    st.title("Futbol Menajerlik Uygulaması")

    # Transfermarkt ve takım listesi
    transfermarkt = []
    takimlar = []

    # Oyuncuları players_game.csv dosyasından yükle
    csvden_oyuncu_yukle(transfermarkt, 'players_game.csv')

    # Menü
    menu_secim = st.sidebar.selectbox("Menü", ["Oyuncu Oluştur", "Transfermarkt'ı Gör", "Takım Kur", "Oyuncu Satın Al", "Maç Yap", "Takım Bilgilerini Gör", "Çıkış"])

    if menu_secim == "Oyuncu Oluştur":
        with st.form("oyuncu_form"):
            name = st.text_input("Oyuncunun İsmi")
            overall = st.slider("Oyuncunun Overall Gücü", 1, 100)
            yas = st.slider("Oyuncunun Yaşı", 18, 40)
            submitted = st.form_submit_button("Oyuncuyu Oluştur")

            if submitted and name:
                oyuncu = oyuncu_olustur(name, overall, yas)
                transfermarkt.append(oyuncu)
                st.success(f"{oyuncu.isim} oluşturuldu ve Transfermarkt'a eklendi!")

    elif menu_secim == "Transfermarkt'ı Gör":
        transfermarkt_listele(transfermarkt)

    elif menu_secim == "Takım Kur":
        takim_ismi = st.text_input("Takım İsmi")
        butce = st.number_input("Takım Bütçesi (Milyon €)", min_value=1_000_000, step=1_000_000)

        if st.button("Takımı Kur"):
            yeni_takim = Takim(takim_ismi, butce)
            takimlar.append(yeni_takim)
            st.success(f"{takim_ismi} takımı kuruldu!")

    elif menu_secim == "Oyuncu Satın Al":
        if not takimlar:
            st.warning("Oyuncu satın almak için önce bir takım kurmalısınız!")
        elif not transfermarkt:
            st.warning("Transfermarkt'ta hiç oyuncu yok!")
        else:
            takim_secim = st.selectbox("Oyuncu Satın Alacak Takım", takimlar, format_func=lambda x: x.isim)
            transfermarkt_listele(transfermarkt)
            oyuncu_secim = st.selectbox("Satın Alınacak Oyuncu", transfermarkt, format_func=lambda x: x.isim)

            if st.button("Oyuncuyu Satın Al"):
                if takim_secim.oyuncu_satinal(oyuncu_secim):
                    transfermarkt.remove(oyuncu_secim)
                    st.success(f"{oyuncu_secim.isim} {takim_secim.isim} takımına transfer edildi!")
                else:
                    st.error("Yeterli paranız yok!")

    elif menu_secim == "Maç Yap":
        if len(takimlar) < 2:
            st.warning("Maç yapmak için en az iki takım olmalı!")
        else:
            takim1_secim = st.selectbox("Birinci Takım", takimlar, format_func=lambda x: x.isim)
            takim2_secim = st.selectbox("İkinci Takım", takimlar, format_func=lambda x: x.isim)

            if st.button("Maçı Başlat"):
                if len(takim1_secim.oyuncular) > 0 and len(takim2_secim.oyuncular) > 0:
                    gol1, gol2, gol_atan_oyuncular1, gol_atan_oyuncular2 = takimlar_arasi_mac(takim1_secim, takim2_secim)

                    st.write(f"**Maç Sonucu:** {takim1_secim.isim} {gol1}-{gol2} {takim2_secim.isim}")
                    st.write("Gol Atanlar:")
                    for oyuncu in gol_atan_oyuncular1:
                        st.write(f"{takim1_secim.isim}: {oyuncu.isim} (Overall: {oyuncu.overall})")
                    for oyuncu in gol_atan_oyuncular2:
                        st.write(f"{takim2_secim.isim}: {oyuncu.isim} (Overall: {oyuncu.overall})")
                else:
                    st.warning("Her iki takımda da en az bir oyuncu olmalı!")

    elif menu_secim == "Takım Bilgilerini Gör":
        takim_bilgilerini_goster(takimlar)

    elif menu_secim == "Çıkış":
        st.write("Çıkış yapıldı.")

if __name__ == "__main__":
    main()
