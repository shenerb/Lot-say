import pandas as pd

def calculate_float_shares(input_file, output_file):
    # Excel dosyasını oku
    df = pd.read_excel(input_file)

    # Kolon isimlerini temizleyelim (boşluk ve özel karakterler olabilir)
    df.columns = [col.strip() for col in df.columns]

    # Dolaşımdaki lot hesaplama:
    # (Sermaye (mn TL) * 1_000_000) / Kapanış fiyatı * Halka Açıklık Oranı / 100
    # Sermaye'nin mn TL olduğu varsayılıyor, önce tam TL'ye çevirelim
    df['Sermaye_TL'] = df['Sermaye (mn TL)'] * 1_000_000
    df['Dolasimdaki_Lot'] = (df['Sermaye_TL'] / df['Kapanış (TL)']) * (df['Halka Açıklık Oranı (%)'] / 100)

    # Dolaşımdaki lot sayısını tam sayıya yuvarlayalım
    df['Dolasimdaki_Lot'] = df['Dolasimdaki_Lot'].round().astype(int)

    # İstenirse sadece ilgili kolonları seçip kaydedebiliriz
    output_df = df[['Hisse Adı', 'Dolasimdaki_Lot']]

    output_df.to_csv(output_file, index=False)
    print(f"Dolaşımdaki lot sayıları '{output_file}' dosyasına kaydedildi.")

if __name__ == "__main__":
    input_excel = "temelozet.xlsx"
    output_csv = "dolasimdaki_lotlar.csv"
    calculate_float_shares(input_excel, output_csv)
