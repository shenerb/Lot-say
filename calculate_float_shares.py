import pandas as pd
import streamlit as st
from io import StringIO

def calculate_float_shares(df):
    # Kolon adlarını temizle
    df.columns = [col.strip() for col in df.columns]

    # Sermayeyi tam TL'ye çevir
    df['Sermaye_TL'] = df['Sermaye (mn TL)'] * 1_000_000

    # Dolaşımdaki lot = Sermaye_TL * (halka açıklık oranı / 100)
    df['Dolasimdaki_Lot'] = (df['Sermaye_TL'] * df['Halka Açıklık Oranı (%)'] / 100).round().astype(int)

    # Çıktıya hisse kodunu da ekleyelim
    output_df = df[['Kod', 'Hisse Adı', 'Dolasimdaki_Lot']]
    return output_df

# Streamlit arayüzü
st.title("📊 Halka Açık Lot (Adet) Hesaplayıcı")
uploaded_file = st.file_uploader("Excel dosyasını yükleyin (.xlsx)", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    result_df = calculate_float_shares(df)

    st.dataframe(result_df)

    # CSV formatında çıktı oluştur
    csv = result_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 CSV dosyasını indir",
        data=csv,
        file_name="dolasimdaki_lotlar.csv",
        mime='text/csv'
    )
