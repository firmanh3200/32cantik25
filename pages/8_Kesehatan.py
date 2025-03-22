import streamlit as st
import requests
import pandas as pd
import lxml
from datetime import datetime

# Ambil tanggal hari ini
tanggal_hari_ini = datetime.now().strftime("%d-%m-%Y")

st.set_page_config(layout="wide")
with st.container(border=True):
    with st.container(border=True):
        st.title(":green[Indikator Kesehatan di Desa]")
        st.warning(f"Sumber: https://portaldatadesa.jabarprov.go.id/index-profile-desa/Sosial/Kesehatan, Kondisi: {tanggal_hari_ini}")
        st.info("Hanya tersedia untuk Desa, Tidak tersedia untuk Kelurahan")
st.subheader("", divider='green')


mendagri = pd.read_csv('data/kdkec.csv', sep=',', 
                            dtype={'idkab':'str', 'idkec':'str', 'kodedapodik':'str'}, encoding='utf-8')    
pilihankab = mendagri['namakab'].unique()

with st.container(border=True):
    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        kabterpilih2 = st.selectbox("Pilih Kabupaten", pilihankab, key='kab')
        kabterpilih_series = mendagri[mendagri['namakab'] == kabterpilih2]['idkab']
        # Pastikan Series tidak kosong sebelum mengambil nilainya
        kabterpilih = kabterpilih_series.iloc[0] if not kabterpilih_series.empty else None

    with kol2:
        pilihankec = mendagri[mendagri['namakab'] == kabterpilih2]['namakec'].unique()
        kecterpilih2 = st.selectbox("Pilih Kecamatan", pilihankec, key='kec')
        kecterpilih_series = mendagri[mendagri['namakec'] == kecterpilih2]['kodekec']
        # Pastikan Series tidak kosong sebelum mengambil nilainya
        kecterpilih = kecterpilih_series.iloc[0] if not kecterpilih_series.empty else None

    with kol3:
        pilihantahun = ['2024', '2023', '2022', '2021', '2025']
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun, key='tahun')

# BPJS KESEHATAN
with st.expander('Kepesertaan BPJS Kesehatan'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Tingkat%20Kepesertaan%20BPJS/%20JKN/%20KIS&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")
        
# LAYANAN PUS
with st.expander('Layanan kepada Calon PUS'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Konvergensi%20Layanan%20untuk%20Kesejahteraan%20Calon%20Pengantin%20dan%20Pasangan%20Usia%20Subur&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")
        
# LAYANAN STUNTING
with st.expander('Layanan Stunting'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Konvergensi%20Layanan%20Stunting%20di%20Desa&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")
        
# POSKESDES POLINDES POSYANDU
with st.expander('Poskesdes / Polindes / Posyandu'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Akses%20Ke%20Poskesdes/%20Polindes%20dan%20Posyandu&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")
        
# RUMAH BERSALIN
with st.expander('Rumah Bersalin'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Rumah%20Bersalin&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# RUMAH SAKIT BERSALIN
with st.expander('Rumah Sakit Bersalin'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Rumah%20Sakit%20Bersalin&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# DOKTER
with st.expander('Ketersediaan Dokter'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Ketersediaan%20Tenaga%20Kesehatan%20Dokter&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# Keluarga Rentan Stunting
with st.expander('Keluarga Rentan Stunting'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Kondisi%20Keluarga%20Rentan%20terhadap%20Stunting&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# POLIKLINIK
with st.expander('Poliklinik/ Balai Pengobatan'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Poliklinik/Balai%20Pengobatan&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# BIDAN
with st.expander('Ketersediaan Bidan'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Ketersediaan%20Tenaga%20Kesehatan%20Bidan&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# RUMAH SAKIT
with st.expander('Ketersediaan Rumah Sakit'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Rumah%20Sakit&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# PUSTU
with st.expander('Ketersediaan Puskesmas Pembantu'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Puskesmas%20Pembantu&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# PUSKESMAS RAWAT INAP
with st.expander('Ketersediaan Puskesmas Rawat Inap'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Puskesmas%20Rawat%20inap&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# Keluarga Beresiko Stunting dan Rentan
with st.expander('Keluarga Berisiko Stunting dan Keluarga Rentan'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Keluarga%20Berisiko%20Stunting%20dan%20Rentan&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# Puskesmas Tanpa Rawat Inap
with st.expander('Ketersediaan Puskesmas Tanpa Rawat Inap'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Puskesmas%20Tanpa%20Rawat%20Inap&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

# Layanan Ibu Hamil
with st.expander('Layanan Ibu Hamil'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Cakupan%20Pelayanan%20Kesehatan%20Ibu%20Hamil&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
        response = requests.get(url)
        data = response.json()
        
        # Ekstrak data dan identifikasi ID
        extracted_data = []
        for item_list in data['data']:
            for item in item_list:
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

        # Proses data per item_list (desa)
        for item_list in data['data']:
            # Ekstrak ID Desa
            id_desa = None
            extracted_data = []
            for item in item_list:
                if item['indikator_db'] == 'id':  # Asumsikan 'id' adalah ID Desa
                    id_desa = item['value']
                extracted_data.append({
                    'indikator_db': item['indikator_db'],
                    'perangkat_indikator_2': item['perangkat_indikator_2'],
                    'value': item['value']
                })

            # Buat DataFrame untuk desa ini
            df_desa = pd.DataFrame(extracted_data)

            # Tampilkan DataFrame dengan judul ID Desa
            if id_desa is not None:
                st.subheader(f"Data untuk ID Desa: {id_desa}")
                st.dataframe(df_desa, hide_index=True, use_container_width=True)
                st.subheader("", divider='green')
            else:
                st.warning("ID Desa tidak ditemukan untuk item ini.")

    else:
        st.warning("Pilih Kabupaten, Kecamatan, dan Tahun terlebih dahulu.")

