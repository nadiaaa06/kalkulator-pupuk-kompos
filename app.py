import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Kalkulator Pupuk Kompos",
    page_icon="🌱",
    layout="centered"
)

# Data bahan dan propertinya (dari tabel terbaru)
BAHAN_DATA = {
    'Ampas teh segar': {'C/N': 30, 'kelembaban': 72.5},
    'Ampas kopi segar': {'C/N': 25, 'kelembaban': 77.5},
    'Kulit pisang baru dikupas': {'C/N': 35, 'kelembaban': 77.5},
    'Cangkang telur': {'C/N': 6, 'kelembaban': 12.5},
    'Kulit bawang merah': {'C/N': 40, 'kelembaban': 12.5},
    'Kangkung segar': {'C/N': 20, 'kelembaban': 92.5},
    'Bayam segar': {'C/N': 17, 'kelembaban': 92.5},
    'Nasi baru dimasak (<12 jam)': {'C/N': 20, 'kelembaban': 67.5},
    'Nasi semalam': {'C/N': 18, 'kelembaban': 62.5},
    'Kangkung busuk': {'C/N': 15, 'kelembaban': 72.5},
    'Bayam busuk': {'C/N': 13, 'kelembaban': 72.5},
    'Kulit pisang 1-2 hari setelah dikupas': {'C/N': 28, 'kelembaban': 67.5},
    'Ampas teh 1-2 hari setelah diseduh': {'C/N': 26, 'kelembaban': 67.5},
    'Ampas kopi 1-2 hari setelah diseduh': {'C/N': 22, 'kelembaban': 67.5}
}

# Mapping unsur dominan tiap bahan
UNSUR_BAHAN = {
    'Kangkung segar': 'N',
    'Bayam segar': 'N',
    'Kangkung busuk': 'N',
    'Bayam busuk': 'N',
    'Nasi semalam': 'N & P',
    'Nasi baru dimasak (<12 jam)': 'P',
    'Cangkang telur': 'P',
    'Kulit bawang merah': 'P',
    'Kulit pisang baru dikupas': 'K',
    'Kulit pisang 1-2 hari setelah dikupas': 'K',
    'Ampas teh segar': 'K',
    'Ampas teh 1-2 hari setelah diseduh': 'K',
    'Ampas kopi segar': 'K',
    'Ampas kopi 1-2 hari setelah diseduh': 'K',
}

# Mapping tanaman ke unsur dominan dan penjelasan
UNSUR_TANAMAN = {
    'Jahe': {'unsur': 'K', 'penjelasan': 'Mendorong pembentukan rimpang, meningkatkan ukuran dan kualitas'},
    'Kunyit': {'unsur': 'K', 'penjelasan': 'K penting untuk metabolisme & sintesis senyawa aktif'},
    'Sereh': {'unsur': 'N', 'penjelasan': 'Daun panjang butuh N untuk pertumbuhan vegetatif yang cepat'},
    'Lengkuas': {'unsur': 'K', 'penjelasan': 'Rhizome seperti jahe dan kunyit, sangat butuh K'},
    'Daun Salam': {'unsur': 'N', 'penjelasan': 'Daun sebagai hasil utama, butuh N untuk klorofil dan pertumbuhan daun'},
    'Cengkeh': {'unsur': 'K', 'penjelasan': 'Penting untuk pembungaan & perkembangan kuncup bunga'},
    'Kayu manis': {'unsur': 'N', 'penjelasan': 'Pertumbuhan batang & daun dominan, N sangat dibutuhkan'},
    'Lada': {'unsur': 'K', 'penjelasan': 'Pembungaan dan pembentukan buah perlu K tinggi'},
    'Cabai': {'unsur': 'K', 'penjelasan': 'Buah banyak, K penting untuk produksi buah dan kualitas rasa'},
    'Tomat': {'unsur': 'K', 'penjelasan': 'K dominan untuk pembentukan dan rasa buah'},
}

def tampilkan_petunjuk():
    st.title("Petunjuk Penggunaan")
    st.write("""
    ### Cara Menggunakan Kalkulator Pupuk Kompos:
    1. Pilih tanaman yang akan ditanam
    2. Perhatikan rekomendasi bahan yang ditampilkan
    3. Masukkan bahan-bahan yang tersedia beserta massanya
    4. Sistem akan menghitung komposisi C/N dan kelembaban
    5. Ikuti rekomendasi yang diberikan untuk mendapatkan komposisi ideal
    6. Setelah komposisi ideal, hancurkan semua bahan, dan tambahkan dekomposer
    7. Proses pengomposan dilakukan secara tertutup, dan lakukan pembalikan 1 kali seminggu. Suhu panas saat proses pengomposan menunjukan dekomposisi berjalan baik
    """)
    
    st.write("""
    ### Target Ideal:
    - Rasio C/N: 20-40
    - Kelembaban: 40%-65%
    """)

def hitung_komposisi(bahan_massa):
    total_massa = sum(bahan_massa.values())
    total_cn = 0
    total_kelembaban = 0
    
    for bahan, massa in bahan_massa.items():
        if bahan in BAHAN_DATA:
            proporsi = massa / total_massa
            total_cn += BAHAN_DATA[bahan]['C/N'] * proporsi
            total_kelembaban += BAHAN_DATA[bahan]['kelembaban'] * proporsi
    
    return {
        'C/N': total_cn,
        'kelembaban': total_kelembaban
    }

def berikan_rekomendasi(hasil):
    cn = hasil['C/N']
    kelembaban = hasil['kelembaban']
    rekom = []
    bahan_cn_tinggi = [b for b, v in BAHAN_DATA.items() if v['C/N'] > 25]
    bahan_basah = [b for b, v in BAHAN_DATA.items() if v['kelembaban'] > 70]

    if cn > 40 and kelembaban > 65:
        rekom.append(f"Kurangi bahan dengan rasio C/N tinggi (misal: {', '.join(bahan_cn_tinggi)}) dan bahan basah (misal: {', '.join(bahan_basah)})")
    elif cn > 40 and kelembaban < 40:
        rekom.append(f"Kurangi bahan dengan rasio C/N tinggi (misal: {', '.join(bahan_cn_tinggi)}) dan tambahkan bahan basah (misal: {', '.join(bahan_basah)})")
    elif cn < 20 and kelembaban > 65:
        rekom.append(f"Tambahkan bahan dengan rasio C/N tinggi (misal: {', '.join(bahan_cn_tinggi)}) dan kurangi bahan basah (misal: {', '.join(bahan_basah)})")
    elif cn < 20 and kelembaban < 40:
        rekom.append(f"Tambahkan bahan dengan rasio C/N tinggi (misal: {', '.join(bahan_cn_tinggi)}) dan tambahkan bahan basah (misal: {', '.join(bahan_basah)})")
    elif not (20 <= cn <= 40):
        if cn < 20:
            rekom.append(f"C/N terlalu rendah, tambahkan bahan dengan C/N tinggi (misal: {', '.join(bahan_cn_tinggi)})")
        else:
            rekom.append(f"C/N terlalu tinggi, kurangi bahan dengan C/N tinggi (misal: {', '.join(bahan_cn_tinggi)})")
    elif not (40 <= kelembaban <= 65):
        if kelembaban < 40:
            rekom.append(f"Kelembaban terlalu rendah, tambahkan bahan basah (misal: {', '.join(bahan_basah)})")
        else:
            rekom.append(f"Kelembaban terlalu tinggi, kurangi bahan basah (misal: {', '.join(bahan_basah)})")
    else:
        rekom.append("Komposisi sudah ideal!")
    return rekom

def analisis_graf_bahan(input_gram):
    # Ambil bahan yang dipilih user (massa > 0)
    bahan_dipilih = [b for b, g in input_gram.items() if g > 0]
    if not bahan_dipilih:
        return None, None
    
    # Klasifikasi bahan basah dan kering
    bahan_basah = [b for b in bahan_dipilih if BAHAN_DATA[b]['kelembaban'] > 70]
    bahan_kering = [b for b in bahan_dipilih if BAHAN_DATA[b]['kelembaban'] <= 70]

    pesan = None
    saran = None
    if len(bahan_basah) == len(bahan_dipilih):
        # Semua bahan basah
        pesan = "Semua bahan yang dipilih adalah bahan basah. Kombinasi ini tidak ideal."
        # Rekomendasikan bahan kering dari daftar
        bahan_kering_opsi = [b for b, v in BAHAN_DATA.items() if v['kelembaban'] <= 70 and b not in bahan_dipilih]
        if bahan_kering_opsi:
            saran = f"Tambahkan bahan penyeimbang (kering), misal: {', '.join(bahan_kering_opsi[:3])}"
    elif len(bahan_kering) == len(bahan_dipilih):
        # Semua bahan kering
        pesan = "Semua bahan yang dipilih adalah bahan kering. Kombinasi ini tidak ideal."
        # Rekomendasikan bahan basah dari daftar
        bahan_basah_opsi = [b for b, v in BAHAN_DATA.items() if v['kelembaban'] > 70 and b not in bahan_dipilih]
        if bahan_basah_opsi:
            saran = f"Tambahkan bahan penyeimbang (basah), misal: {', '.join(bahan_basah_opsi[:3])}"
    return pesan, saran

def tampilkan_kalkulator():
    st.title("Kalkulator Pupuk Kompos")
    
    # Pilih tanaman
    tanaman = st.selectbox("Pilih Tanaman", list(UNSUR_TANAMAN.keys()))
    
    # Tampilkan rekomendasi bahan cocok dan penjelasan
    if tanaman in UNSUR_TANAMAN:
        unsur = UNSUR_TANAMAN[tanaman]['unsur']
        penjelasan = UNSUR_TANAMAN[tanaman]['penjelasan']
        # Cari bahan yang cocok
        bahan_cocok = [b for b, u in UNSUR_BAHAN.items() if unsur in u]
        st.info(f"Tanaman ini paling membutuhkan unsur **{unsur}**.\n\nBahan yang cocok: {', '.join(bahan_cocok)}\n\nPenjelasan: {penjelasan}")
    
    # Input bahan
    st.subheader("Masukkan Bahan-bahan")
    bahan_massa = {}
    
    bahan_list = list(BAHAN_DATA.keys())
    input_gram = {}
    
    cols = st.columns([2, 1, 1, 1])
    cols[0].markdown("**BAHAN**")
    cols[1].markdown("**KOMPOSISI (g)**")
    cols[2].markdown("**C/N**")
    cols[3].markdown("**Kelembaban (%)**")
    
    for bahan in bahan_list:
        cols = st.columns([2, 1, 1, 1])
        cols[0].write(bahan)
        gram = cols[1].number_input(" ", min_value=0, value=0, key=bahan)
        input_gram[bahan] = gram
        cols[2].write(f"{BAHAN_DATA[bahan]['C/N']}")
        cols[3].write(f"{BAHAN_DATA[bahan]['kelembaban']}")
    
    total_gram = sum(input_gram.values())
    
    # Tampilkan tabel rekap hanya jika ada input
    if total_gram > 0:
        st.markdown("**Rekap Bahan yang Dimasukkan**")
        rekap_data = []
        for bahan in bahan_list:
            gram = input_gram[bahan]
            if gram > 0:
                persen = gram / total_gram * 100
                rekap_data.append({
                    "Bahan": bahan,
                    "Gram": gram,
                    "Berat %": f"{persen:.1f}",
                    "C/N": BAHAN_DATA[bahan]['C/N'],
                    "Kelembaban (%)": BAHAN_DATA[bahan]['kelembaban']
                })
        st.dataframe(rekap_data, hide_index=True)
    
    # Tombol hitung
    hitung = st.button("Hitung")
    
    if hitung:
        # Hitung komposisi
        if total_gram == 0:
            st.warning("Masukkan minimal satu bahan!")
        else:
            hasil = hitung_komposisi(input_gram)
            
            # Tampilkan hasil
            st.subheader("Hasil Perhitungan")
            st.write(f"Rasio C/N: {hasil['C/N']:.2f}")
            st.write(f"Kelembaban: {hasil['kelembaban']:.2f}%")
            
            # Tampilkan rekomendasi
            st.subheader("Rekomendasi")
            rekomendasi = berikan_rekomendasi(hasil)
            for r in rekomendasi:
                st.write(f"- {r}")
            # Analisis graf bahan
            pesan, saran = analisis_graf_bahan(input_gram)
            if pesan:
                st.warning(pesan)
            if saran:
                st.info(saran)

def main():
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Pilih Menu", ["Petunjuk", "Kalkulator"])
    
    if menu == "Petunjuk":
        tampilkan_petunjuk()
    else:
        tampilkan_kalkulator()

if __name__ == "__main__":
    main()