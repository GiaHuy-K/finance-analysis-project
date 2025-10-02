# import os
# from vnstock import Vnstock
# import pandas as pd

# # Thư mục dataset
# print("Current directory:", os.getcwd())
# os.chdir(r"C:\Users\Admin\Desktop\PDS301m_HuongNTC2\Project\finance-analysis-project\phase2_data_structures\dataset")

# symbols = ['FPT', 'MBB', 'VCB', 'VIC']
# api = Vnstock()

# portfolio = []

# for sym in symbols:
#     stock = api.stock(symbol=sym, source='VCI')  
#     df = stock.quote.history(start='2023-01-01', end='2024-01-01', interval='1D')
    
#     # Lưu CSV riêng từng cổ phiếu
#     filename = f"{sym}_history.csv"
#     df.to_csv(filename, index=False, encoding="utf-8-sig")
    
#     # Chuyển DataFrame thành list of dicts và list of tuples
#     stock_list = df.to_dict('records')  # List of dicts
#     stock_tuples = [(row['time'], row['close']) for row in stock_list]  # List of tuples
    
#     # Tính trung bình giá đóng cửa
#     avg_close = df['close'].mean()
    
#     # Tính lợi nhuận % = (giá cuối - giá đầu)/giá đầu * 100
#     profit_pct = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
    
#     portfolio.append({
#         "symbol": sym,
#         "list_of_dicts": stock_list,
#         "list_of_tuples": stock_tuples,
#         "average_close": avg_close,
#         "profit_pct": profit_pct
#     })
    
#     print(f"{sym}: Avg Close = {avg_close:.2f}, Profit % = {profit_pct:.2f}%")

# # Tìm cổ phiếu tăng trưởng tốt nhất
# best_stock = max(portfolio, key=lambda x: x['profit_pct'])
# print("\nCổ phiếu tăng trưởng tốt nhất:", best_stock['symbol'], f"({best_stock['profit_pct']:.2f}%)")

import os
from vnstock import Vnstock
import pandas as pd

# Thư mục dataset nằm cùng cấp file .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
os.chdir(DATASET_DIR)

# ---- Function 1: Lấy dữ liệu cổ phiếu và lưu CSV ----
def fetch_stock_data(symbol, start, end):
    api = Vnstock()
    stock = api.stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start, end=end, interval="1D")
    df.to_csv(f"{symbol}_history.csv", index=False, encoding="utf-8-sig")
    return df

# ---- Function 2: Tính trung bình & lợi nhuận % ----
def analyze_stock(df):
    avg_close = df['close'].mean()
    profit_pct = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
    return avg_close, profit_pct

# ---- Function 3: Chuyển sang list of dicts & tuples ----
def convert_to_structures(df):
    stock_list = df.to_dict('records')
    stock_tuples = [(row['time'], row['close']) for row in stock_list]
    return stock_list, stock_tuples

# ---- Main demo ----
if __name__ == "__main__":
    symbols = ['FPT', 'MBB', 'VCB', 'VIC']
    portfolio = []

    for sym in symbols:
        df = fetch_stock_data(sym, "2023-01-01", "2024-01-01")
        avg_close, profit_pct = analyze_stock(df)
        stock_list, stock_tuples = convert_to_structures(df)

        stock_data = {
            "symbol": sym,
            "list_of_dicts": stock_list,
            "list_of_tuples": stock_tuples,
            "average_close": avg_close,
            "profit_pct": profit_pct
        }
        portfolio.append(stock_data)

        print(f"{sym}: Avg Close = {avg_close:.2f}, Profit % = {profit_pct:.2f}%")

    best_stock = max(portfolio, key=lambda x: x['profit_pct'])
    print("\nCổ phiếu tăng trưởng tốt nhất:", best_stock['symbol'], f"({best_stock['profit_pct']:.2f}%)")

