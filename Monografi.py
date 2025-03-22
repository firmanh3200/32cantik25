import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import xlsxwriter
import lxml

# Function to fetch data from URL based on selected code
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_html(response.text)  # Read HTML tables from the response
        return data[0]  # Assuming the data is in the first table
    else:
        st.error("Gagal mengambil data. Status code: {}".format(response.status_code))
        return None

def kamus():
    mfd = pd.read_csv('data/mfd2023.csv', sep=',', 
                            dtype={'idkab':'str', 'idkec':'str', 'iddesa':'str'}, encoding='utf-8')
    
    mendagri = pd.read_csv('data/kdkec.csv', sep=',', 
                            dtype={'idkab':'str', 'idkec':'str', 'kodedapodik':'str'}, encoding='utf-8')
    
    mfd32 = pd.read_csv('data/mfd_23_1_32.csv', 
                            dtype={'kdkab':'str', 'kdkec':'str', 'kddesa':'str', 'iddesa':'str'}, encoding='utf-8')
    mfd32['idkec'] = mfd32['iddesa'].str[:7]
    
    return mfd, mendagri, mfd32
mfd, mendagri, mfd32 = kamus()

# Filter mfd berdasarkan idkec yang ada di mendagri
mfd_2025 = mfd[mfd['idkec'].isin(mendagri['idkec'])]
mfd32_2025 = mfd32[mfd32['idkec'].isin(mendagri['idkec'])]

# Gabungkan mfd_2025 dengan mfd32 berdasarkan iddesa untuk mendapatkan informasi tambahan
# st.dataframe(mfd_2025)
# st.dataframe(mfd32_2025)
# st.dataframe(mendagri)
mfd_2025_a = pd.merge(mfd_2025, mfd32_2025[['iddesa', 'stat_pem', 'nmdesa', 'nmkec', 'nmkab', 'latitude', 'longitude']], on='iddesa', how='left')
mfd_2025_cantik = pd.merge(mfd_2025_a, mendagri, on='idkec', how='left')

# st.dataframe(mfd_2025_a)
# st.dataframe(mfd_2025)

# Main Streamlit app
def main():
    with st.container(border=True):
        with st.container(border=True):
            st.subheader(":orange[MONOGRAFI DESA/ KELURAHAN CINTA STATISTIK]")
            st.subheader(":blue[DI PROVINSI JAWA BARAT TAHUN 2025]", divider='rainbow')
        
            kol1, kol2, kol3 = st.columns(3)
            with kol1:
                kabkot = mfd_2025['idkab'].unique().tolist()
                kabterpilih1 = st.selectbox("Filter IDKAB", kabkot, key='kabkot1')
            with kol2:
                kec = mfd_2025[mfd_2025['idkab'] == kabterpilih1]['idkec'].unique().tolist()
                kecterpilih1 = st.selectbox("Filter IDKEC", kec, key='kec1')
            with kol3:
                desa = mfd_2025[mfd_2025['idkec'] == kecterpilih1]['iddesa'].unique().tolist()
                desaterpilih = st.selectbox("Filter IDDESA", desa, key='desa1')    
                
            if kol1 and kol2 and kol3:
                infodesa = mfd_2025_cantik[mfd_2025_cantik['iddesa'] == desaterpilih]
                url = f"https://e-prodeskel.kemendagri.go.id/datapokok/data.php?kodesa={desaterpilih}"

                # Fetch data based on selected code
                tables = pd.read_html(url)

                df0 = tables[0]
                df1 = tables[1]
                df2 = tables[2]
                df3 = tables[3]
                #df4 = tables[4]

                tabel0 = pd.DataFrame(df0)
                tabel1 = pd.DataFrame(df1)
                tabel2 = pd.DataFrame(df2)
                tabel3 = pd.DataFrame(df3)
                #tabel4 = pd.DataFrame(df4)

                gabungan = pd.concat([tabel0, tabel1, tabel2, tabel3], axis=1)
    
    #st.subheader("", divider='green')
            
    with st.container(border=True):
        st.subheader(f":green[MONOGRAFI {infodesa['stat_pem'].iloc[0]} {infodesa['nmdesa'].iloc[0]}]")
        st.subheader(f":green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
        st.dataframe(tabel0, use_container_width=True, hide_index=True)
        st.dataframe(tabel1, use_container_width=True, hide_index=True)
        st.dataframe(tabel2, use_container_width=True, hide_index=True)
        st.dataframe(tabel3, use_container_width=True, hide_index=True)
        #st.dataframe(tabel4, use_container_width=True, hide_index=True)
    
        st.link_button("Sumber Data", url=f"https://e-prodeskel.kemendagri.go.id/datapokok/data.php?kodesa={desaterpilih}")
        
    st.subheader("", divider='green')
    st.subheader("", divider='orange')
    st.subheader("", divider='blue')
###############################################################    
###############################################################    
    with st.container(border=True):
        with st.container(border=True):
            st.subheader('Data Prodeskel Kemendagri Lainnya')
            st.subheader(f"{infodesa['stat_pem'].iloc[0]} {infodesa['nmdesa'].iloc[0]}, KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}", divider='orange')
            kolom1, kolom2 = st.columns(2)

            # Daftar tahun yang tersedia
            daftar_tahun = list(range(2019, 2026))

            # Pemilihan Tahun
            with kolom1:
                tahun_terpilih = st.selectbox("Pilih Tahun:", daftar_tahun)
                kodekecterpilih = mfd_2025_cantik[mfd_2025_cantik['idkec'] == kecterpilih1]['kodekec'].unique().tolist()[0]

            # Kategori Data Options
            kategori_data_options = {
                "Pendidikan": "2",
                "Kesejahteraan Keluarga": "6",
                "Perkembangan LKM": "7",
                "Musrenbangdes": "8",
                "Posyandu": "9",
                "PKK": "10",
                "Iklim": "11",
                "Lahan": "12",
                "Potensi Penduduk": "13",
                "Lahan Kehutanan": "14",
                "Lahan Perkebunan": "15",
                "Lahan Pertanian": "16",
                "Potensi LKM": "17",
                "Potensi Pemerintahan": "18",
                "Luas Wilayah": "19",
                "Keagamaan": "20",
                "Sarana Prasarana": "21",
                "Air Bersih": "22",
                "Kesehatan": "23",
                "Kominfo": "24",
                "Umur Tunggal": "25",
                "RT - RW": "34",
            }

            with kolom2:
                kategori_terpilih = st.selectbox(
                    "Pilih Kategori Data:",
                    options=list(kategori_data_options.keys()),
                )

            # Dapatkan kode kategori
            kodekategori = kategori_data_options[kategori_terpilih]

            # Tombol Tampilkan
            tampilkan = st.button("Tampilkan Data") #Ganti Tombol Download jadi Tampilkan
            if tampilkan: #Jika Tombol Tampilkan Ditekan
                if tahun_terpilih and kodekategori and kodekecterpilih:
                    url = f"https://e-prodeskel.kemendagri.go.id/api/d/{tahun_terpilih}/data-integrasi-level/{kodekategori}?kode_daerah={kodekecterpilih}"

                    # Fetch data based on selected code
                    try:
                        tables = pd.read_html(url)
                        df = tables[0]
                        tabel = pd.DataFrame(df)

                        if tabel is not None:
                            st.dataframe(tabel)  # Tampilkan DataFrame
                            st.caption(f'Sumber: {url}')
                    except ValueError as e:
                        st.error("Jika tabel tidak tampil, berarti ada Kemungkinan Situs e-prodeskel Kemendagri sedang mengalami Masalah.")
                        st.error(f"Anda bisa klik langsung alamat: {url} untuk melihat sumber data asli e-prodeskel.")
                        st.error("Sementara Menunggu Perbaikan oleh Tim e-prodeskel Kemendagri.")

if __name__ == '__main__':
    main()
