import csv
import os
from vnstock import Vnstock
import os

print("Current directory:", os.getcwd())
os.chdir(r"C:\Users\Admin\Desktop\PDS301m_HuongNTC2\Project\finance-analysis-project\phase3_api_analysis\dataset")

symbols = ['FPT', 'MBB', 'VCB', 'VIC']
api = Vnstock()

for sym in symbols:
    stock = api.stock(symbol=sym, source='VCI')   # tạo object cho từng mã
    df = stock.quote.history(
        start='2023-01-01',
        end='2025-01-01',
        interval='1D'
    )
    print(f"=== {sym} ===")
    print(df.head(), "\n")

    # Lưu từng DataFrame thành file CSV riêng
    filename = f"{sym}_history.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Đã lưu {filename}")

