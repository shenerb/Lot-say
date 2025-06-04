import pandas as pd
import streamlit as st
from io import BytesIO

def calculate_float_shares(df):
    df.columns = [col.strip() for col in df.columns]
    df['Sermaye_TL'] = df['Sermaye (mn TL)'] * 1_000_000
    df['Dolasimdaki_Lot'] = (df['Sermaye_TL'] / df['Kapanış (TL)']) * (df['Halka Açıklık Oranı (%)'] / 100)
    df['Dolasimdaki_Lot'] = df['Dolasimdaki_Lot'].round().astype(int)
    return df[['Kod', 'Hisse Adı', 'Dolasimdaki_Lot']]

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dolaşımdaki Lotlar')
    processed_data = output.getvalue()
    return processed_data

# Streamlit Arayüzü
st.title("Dolaşımdaki Lot Hesaplama")

uploaded_file = st.file_uploader("Excel dosyasını yükle (temelozet.xlsx)", type=["xlsx"])

if uploaded_file:
    df_input = pd.read_excel(uploaded_file)
    df_result = calculate_float_shares(df_input)

    st.dataframe(df_result)

    excel_data = to_excel(df_result)

    st.download_button(
        label="📥 Excel olarak indir",
        data=excel_data,
        file_name="dolasimdaki_lotlar.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
