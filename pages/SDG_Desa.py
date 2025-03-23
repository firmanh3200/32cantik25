import streamlit as st
import pandas as pd
import requests  # Import the requests library for API calls

# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

# --- Functions ---

def fetch_data(api_url):
    """Fetches data from the API and returns it as a JSON object.
       Handles potential errors gracefully."""
    try:
        response = requests.get(api_url)  # Use requests library
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}") # Handle network errors
        return None
    except ValueError as e:
        st.error(f"Error parsing JSON: {e}") # Handle invalid JSON responses
        return None


def process_data(data):
    """Processes the fetched data into a pandas DataFrame.
       Handles missing or invalid data gracefully."""
    if data is None or not data.get('data'): # Check if data is valid and has 'data' key
        st.warning("No data available or data format is incorrect.")
        return None

    sdgs_data = data['data']
    try:
        df = pd.DataFrame(sdgs_data)
        # Ensure the columns exist and in the correct order.  Handle missing columns
        if not all(col in df.columns for col in ['goals', 'title', 'score']):
            st.warning("Missing required columns ('goals', 'title', 'score') in the data.")
            return None

        df = df[['goals', 'title', 'score']] # Ensure order
        return df
    except (KeyError, TypeError) as e:
        st.error(f"Error processing data: {e}. Check the data structure.") # Handle data type errors
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

mfd_2025_a = pd.merge(mfd_2025, mfd32_2025[['iddesa', 'stat_pem', 'nmdesa', 'nmkec', 'nmkab']], on='iddesa', how='left')
mfd_2025_cantik = pd.merge(mfd_2025_a, mendagri, on='idkec', how='left')

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.header("Indikator SDG's Desa")
        st.caption('Sumber: https://sid.kemendesa.go.id/sdgs')
        
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

        # --- API Configuration (Keep this configurable) ---
        api_url = f"https://sid.kemendesa.go.id/sdgs/searching/score-sdgs?location_code=&village_id={desaterpilih}"

        tampilkan = st.button('Tampilkan Data')
        
        if tampilkan:
            st.subheader(f":green[{infodesa['stat_pem'].iloc[0]} {infodesa['nmdesa'].iloc[0]}]")
            st.subheader(f"KECAMATAN :green[{infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
            
            # --- Data Fetching ---
            data = fetch_data(api_url)

            # --- Data Processing ---
            df = process_data(data)

            st.header("Data SDGs Desa")
            st.dataframe(df,  hide_index=True)  # Display DataFrame with Streamlit's table
        else:
            st.warning("Tidak tersedia.")

# BANSOS        
with st.expander('Bansos Desa'):
    url2 = f'https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tnp'

    response2 = requests.get(url2)
    data2 = response2.json()
    df2 = pd.DataFrame(data2['data'])
    
    st.subheader(f":green[{infodesa['stat_pem'].iloc[0]} {infodesa['nmdesa'].iloc[0]}]")
    st.subheader(f"KECAMATAN :green[{infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
    st.dataframe(df2, hide_index=True, use_container_width=True)
    
# PIRAMIDA PENDUDUK DESA        
with st.expander('Piramida Penduduk Desa'):
    url3 = f'https://sid.kemendesa.go.id/population-statistic/data?location_code=&village_id={desaterpilih}&on=population'

    response3 = requests.get(url3)
    data3 = response3.json()
    df3 = pd.DataFrame(data3['data'])
    
    st.subheader(f":green[{infodesa['stat_pem'].iloc[0]} {infodesa['nmdesa'].iloc[0]}]")
    st.subheader(f"KECAMATAN :green[{infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
    st.dataframe(df3, hide_index=True, use_container_width=True)