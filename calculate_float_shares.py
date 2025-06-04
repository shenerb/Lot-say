import pandas as pd
import streamlit as st
from io import BytesIO

def calculate_float_shares(df):
    df.columns = [col.strip() for col in df.columns]
    
    # Sermaye mn TL -> TL'ye çevir
    df['Sermaye_TL'] = df['Sermaye (mn TL)'] * 1_000_000
    
    # Doğru dolaşımdaki lot hesaplama
    df['Dolasimdaki_Lot'] = (df['Sermaye_TL'] * df['Halka Açıklık Oranı (%)'] / 100).round().astype(int)

    return df[['Hisse Adı', 'Dolasimdaki_Lot']]

st.title("📊 Halka Açık Lot Sayısı Hesaplama (adet)")

uploaded_file = st.file_uploader("Excel dosyasını yükle (.xlsx)", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    result_df = calculate_float_shares(df)

    st.dataframe(result_df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False)
    output.seek(0)

    st.download_button(
        label="📥 Excel dosyasını indir",
        data=output,
        file_name="dolasimdaki_lotlar_adet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
