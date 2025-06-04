import pandas as pd
import streamlit as st
from io import BytesIO

def calculate_float_shares(df):
    df.columns = [col.strip() for col in df.columns]
    df['Sermaye_TL'] = df['Sermaye (mn TL)'] * 1_000_000
    df['Dolasimdaki_Lot'] = df['Sermaye_TL'] * (df['Halka Açıklık Oranı (%)'] / 100)
    df['Dolasimdaki_Lot'] = df['Dolasimdaki_Lot'].round().astype(int)
    output_df = df[['Hisse Adı', 'Dolasimdaki_Lot']]
    return output_df

st.title("Dolaşımdaki Lot Sayısı Hesaplayıcı (Adet)")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    result_df = calculate_float_shares(df)

    st.subheader("Hesaplanan Dolaşımdaki Lot Sayıları (adet)")
    st.dataframe(result_df)

    # Excel dosyasını bellek içine yaz
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False)
    output.seek(0)

    # İndirme butonu
    st.download_button(
        label="📥 Excel dosyasını indir",
        data=output,
        file_name="dolasimdaki_lotlar_adet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
