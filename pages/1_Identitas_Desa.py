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
        st.title(":green[Identitas Desa]")
        st.warning(f"Sumber: https://portaldatadesa.jabarprov.go.id/index-profile-desa/Pemerintahan/Identitas-Desa")
        st.warning(f"Sumber: https://portaldatadesa.jabarprov.go.id/index-profile-desa/Lingkungan/Ekologi")
        st.warning(f"Sumber: https://portaldatadesa.jabarprov.go.id/index-profile-desa/Lingkungan/Geografi, Kondisi: {tanggal_hari_ini}")
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


# IDENTITAS
with st.expander('Identitas Desa'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Identitas%20Desa&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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

# DESA MODEL        
with st.expander('Desa Model'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Desa%20Model&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
# Wisata Budaya        
with st.expander('Wisata Budaya'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Wisata%20Budaya&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
# Wisata Alam        
with st.expander('Wisata Alam'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Wisata%20Alam&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
# Wisata Buatan     
with st.expander('Wisata Buatan'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Wisata%20Buatan&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
# Potensi Bencana     
with st.expander('Potensi Bencana'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Potensi%20Bencana&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
# Kondisi Lingkungan     
with st.expander('Kondisi Lingkungan'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Kondisi%20Linkungan&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
# Data Topografi     
with st.expander('Data Topografi'):    
    if kabterpilih and kecterpilih and tahunterpilih:
        url = f'https://portaldatadesa.jabarprov.go.id/api/idm/idmdataidentitas/v2?sub_name=Data%20Topografi&tahun={tahunterpilih}&page=1&limit=100&order=asc&orderby=id_desa&id_kabupaten={kabterpilih}&id_kecamatan={kecterpilih}'
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
        
