import os
from vnstock import Vnstock
import pandas as pd

# TODO: Thêm phần merge file, vài hàm phân tích và dùng pandas nhiều hơn, 
# TODO: Dùng thêm Numpy và vẽ biểu đồ (matplotlib/seaborn)

# ===== PATH SETUP =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
os.chdir(DATASET_DIR)


# ===== FUNCTION 1: Lấy dữ liệu cổ phiếu và lưu CSV =====
def fetch_stock_data(symbol, start, end):
    """Lấy dữ liệu cổ phiếu từ API và lưu vào CSV."""
    api = Vnstock()
    stock = api.stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start, end=end, interval="1D")
    df.to_csv(f"{symbol}_history.csv", index=False, encoding="utf-8-sig", float_format='%.2f')
    return df


# ===== FUNCTION 2: Phân tích cơ bản (giá trung bình, lợi nhuận %) =====
def analyze_stock(df):
    avg_close = df["close"].mean()
    profit_pct = ((df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0]) * 100
    return avg_close, profit_pct


# ===== FUNCTION 3: Chuyển đổi dữ liệu ===== (Mở rộng cho tương lai)
def convert_to_structures(df):
    """Chuyển DataFrame sang list of dicts và list of tuples."""
    stock_list = df.to_dict("records")
    stock_tuples = [(row["time"], row["close"]) for row in stock_list]
    return stock_list, stock_tuples


# ===== FUNCTION 4: Tính drawdown =====
def compute_drawdowns(prices):
    """Tính drawdown và max drawdown (%)."""
    peak = prices[0]
    drawdowns = []
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (p - peak) / peak * 100.0
        drawdowns.append(dd)
        if dd < max_dd:
            max_dd = dd
    return drawdowns, max_dd


# ===== FUNCTION 5: Tính độ biến động (volatility) =====
def compute_volatility(df):
    """Tính độ biến động (volatility %) dựa trên thay đổi ngày."""
    returns = df["close"].pct_change().dropna()
    volatility = returns.std() * 100
    return volatility


# ===== FUNCTION 6: Lọc cổ phiếu tiềm năng =====
def filter_top_stocks(portfolio, min_profit=20, 
                      max_dd=-10, max_volatility=5):
    """Lọc các mã tăng trưởng tốt và rủi ro thấp."""
    return [
        s for s in portfolio
        if s["profit_pct"] >= min_profit
        and s["max_drawdown"] >= max_dd
        and s.get("volatility_pct", 999) <= max_volatility
    ]


# ===== FUNCTION 7: Gói toàn bộ logic xử lý từng mã =====
def process_stock(symbol, start="2023-01-01", end="2025-01-01"):
    """Lấy, phân tích và tính drawdown cho 1 cổ phiếu."""
    df = fetch_stock_data(symbol, start, end)
    avg_close, profit_pct = analyze_stock(df)
    stock_list, stock_tuples = convert_to_structures(df)
    drawdowns, max_dd = compute_drawdowns(df["close"].tolist())
    volatility = compute_volatility(df)

    print(f"{symbol}: Avg Close={avg_close:.2f}, Profit={profit_pct:.2f}%, MaxDD={max_dd:.2f}%, Vol={volatility:.2f}%")
    print(f"   Max Drawdown (%): {max_dd:.2f}\n")


    return {
        "symbol": symbol,
        "average_close": avg_close,
        "profit_pct": profit_pct,
        "max_drawdown": max_dd,
        "volatility_pct": volatility,
        "list_of_dicts": stock_list,
        "list_of_tuples": stock_tuples,
    }   
# ===== MAIN =====
if __name__ == "__main__":
    symbols = ["FPT", "MBB", "VCB", "VIC"]
    portfolio = [process_stock(sym) for sym in symbols]

    best_stock = max(portfolio, key=lambda x: x["profit_pct"])
    print("🔥 Cổ phiếu tăng trưởng tốt nhất:", best_stock["symbol"], f"({best_stock['profit_pct']:.2f}%)")

    top_stocks = filter_top_stocks(portfolio)
    if top_stocks:
        print("\n Các cổ phiếu tiềm năng :")
        for s in top_stocks:
            print(f" - {s['symbol']} | Profit={s['profit_pct']:.2f}% | MaxDD={s['max_drawdown']:.2f}% | Vol={s['volatility_pct']:.2f}%")
    else:
        print("\nKhông có cổ phiếu nào tiềm năng.")
