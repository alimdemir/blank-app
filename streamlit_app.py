import random
import numpy as np
import streamlit as st

# Futbol oyuncusu sınıfı
class FutbolOyuncusu:
    def __init__(self, isim, overall, fiyat):
        self.isim = isim
        self.overall = overall
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

# Takımlar arasında maç yapma fonksiyonu
def takimlar_arasi_mac(takim1, takim2):
    # Takım gücünü hesapla
    takim1_gucu = sum([oyuncu.overall for oyuncu in takim1.oyuncular]) / len(takim1.oyuncular) if takim1.oyuncular else 0
    takim2_gucu = sum([oyuncu.overall for oyuncu in takim2.oyuncular]) / len(takim2.oyuncular) if takim2.oyuncular else 0

    # Gol sayısını belirle
    gol_sayisi1 = np.random.poisson(takim1_gucu / 20)
    gol_sayisi2 = np.random.poisson(takim2_gucu / 20)

    return gol_sayisi1, gol_sayisi2

# Streamlit arayüzü
def main():
    st.title("Futbol Takım Yönetimi")

    # Kullanıcı verilerini saklamak için session state kullanıyoruz
    if 'oyuncular' not in st.session_state:
        st.session_state.oyuncular = []
    if 'transfermarkt' not in st.session_state:
        st.session_state.transfermarkt = []
    if 'takimlar' not in st.session_state:
        st.session_state.takimlar = []

    menu_option = st.sidebar.selectbox("Seçenekler", ["Oyuncu Oluştur", "Transfermarkt'i Gör", "Takım Kur", "Oyuncu Satın Al", "Maç Yap"])

    if menu_option == "Oyuncu Oluştur":
        isim = st.text_input("Oyuncunun ismini girin:")
        overall = st.number_input("Oyuncunun overall gücünü (1-100 arası) girin:", min_value=1, max_value=100)

        if st.button("Oyuncu Oluştur"):
            fiyat = overall * 100_000
            oyuncu = FutbolOyuncusu(isim, overall, fiyat)
            st.session_state.oyuncular.append(oyuncu)
            st.session_state.transfermarkt.append(oyuncu)
            st.success(f"{oyuncu.isim} oyuncusu oluşturuldu ve Transfermarkt'a eklendi!")

    elif menu_option == "Transfermarkt'i Gör":
        if not st.session_state.transfermarkt:
            st.warning("Transfermarkt'ta hiç oyuncu yok.")
        else:
            st.write("Transfermarkt:")
            for i, oyuncu in enumerate(st.session_state.transfermarkt):
                st.write(f"{i + 1}. {oyuncu.isim} (Overall: {oyuncu.overall}, Fiyat: {oyuncu.fiyat} €)")

    elif menu_option == "Takım Kur":
        isim = st.text_input("Takımın ismini girin:")
        para = st.number_input("Takımın bütçesini girin (minimum 1 milyon €):", min_value=1_000_000)

        if st.button("Takım Kur"):
            takim = Takim(isim, para)
            st.session_state.takimlar.append(takim)
            st.success(f"{takim.isim} takımı kuruldu!")

    elif menu_option == "Oyuncu Satın Al":
        if not st.session_state.takimlar:
            st.warning("Oyuncu satın almak için önce bir takım kurmalısınız!")
        elif not st.session_state.transfermarkt:
            st.warning("Transfermarkt'ta satılık oyuncu yok!")
        else:
            takim_secimi = st.selectbox("Satın alacak takım:", [takim.isim for takim in st.session_state.takimlar])
            takim = next(t for t in st.session_state.takimlar if t.isim == takim_secimi)
            oyuncu_secimi = st.selectbox("Satın alınacak oyuncu:", [oyuncu.isim for oyuncu in st.session_state.transfermarkt])

            if st.button("Oyuncu Satın Al"):
                oyuncu = next(o for o in st.session_state.transfermarkt if o.isim == oyuncu_secimi)
                if takim.oyuncu_satinal(oyuncu):
                    st.session_state.transfermarkt.remove(oyuncu)
                    st.success(f"{oyuncu.isim} oyuncusu {takim.isim} takımına transfer edildi!")
                else:
                    st.error("Yeterli paranız yok!")

    elif menu_option == "Maç Yap":
        if len(st.session_state.takimlar) < 2:
            st.warning("Maç yapabilmek için en az iki takım oluşturmalısınız!")
        else:
            takim1_secimi = st.selectbox("Birinci takım:", [takim.isim for takim in st.session_state.takimlar])
            takim2_secimi = st.selectbox("İkinci takım:", [takim.isim for takim in st.session_state.takimlar if takim.isim != takim1_secimi])

            if st.button("Maç Yap"):
                takim1 = next(t for t in st.session_state.takimlar if t.isim == takim1_secimi)
                takim2 = next(t for t in st.session_state.takimlar if t.isim == takim2_secimi)
                gol1, gol2 = takimlar_arasi_mac(takim1, takim2)
                st.write(f"{takim1.isim} Skoru: {gol1} - {takim2.isim} Skoru: {gol2}")
                if gol1 > gol2:
                    st.success(f"Kazanan: {takim1.isim}!")
                elif gol1 < gol2:
                    st.success(f"Kazanan: {takim2.isim}!")
                else:
                    st.success("Maç Berabere!")

if __name__ == "__main__":
    main()
