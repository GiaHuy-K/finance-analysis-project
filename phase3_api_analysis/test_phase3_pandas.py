import os
from vnstock import Vnstock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ===== PATH SETUP =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
os.chdir(DATASET_DIR)

# ===== FUNCTION 1: Lấy dữ liệu cổ phiếu và lưu CSV =====
def fetch_stock_data(symbol, start, end):
    """Lấy dữ liệu cổ phiếu từ API và lưu vào CSV."""
    api = Vnstock()
    stock = api.stock(symbol=symbol, source="TCBS")
    # Nếu source 'VCI' lỗi, có thể đổi sang 'TCBS'
    # stock = api.stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start, end=end, interval="1D")
    df.to_csv(f"{symbol}_history.csv", index=False, encoding="utf-8-sig", float_format='%.2f')
    return df

# ===== FUNCTION 2: Phân tích cơ bản (giá trung bình, lợi nhuận %) =====
def analyze_stock(df):
    """Tính giá đóng cửa trung bình và % lợi nhuận đơn."""
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

# ===== FUNCTION 5: Tính độ biến động cuộn (rolling volatility) ( Chưa sử dụng) =====
def compute_rolling_volatility(df, window=30):
    """
    Tính độ biến động cuộn (rolling volatility) dựa trên
    standard deviation của lợi nhuận ngày.
    """
    # 1. Tính lợi nhuận ngày
    daily_returns = df['close'].pct_change()
    
    # 2. Tính rolling standard deviation (dùng Pandas)
    # Nhân với 100 để ra %
    rolling_vol = daily_returns.rolling(window=window).std() * 100
    
    rolling_vol.name = f"rolling_vol_{window}d"
    return rolling_vol

# ===== FUNCTION 6: Tính độ biến động (volatility) =====
def compute_volatility(df):
    """Tính độ biến động (volatility %) dựa trên thay đổi ngày."""
    returns = df["close"].pct_change().dropna()
    
    volatility = np.std(returns) * 100 
    return volatility

# ===== FUNCTION 7: Lọc cổ phiếu tiềm năng =====
def filter_top_stocks(portfolio, min_profit=20, 
                      max_dd=-10, max_volatility=5):
    """Lọc các mã tăng trưởng tốt và rủi ro thấp."""
    return [
        s for s in portfolio
        if s["profit_pct"] >= min_profit
        and s["max_drawdown"] >= max_dd
        and s.get("volatility_pct", 999) <= max_volatility
    ]

# ===== FUNCTION 8: TÍNH CAGR( Tính tốc độ tăng trưởng kép hằng năm) =====
def compute_cagr(df):
    """Tính tốc độ tăng trưởng kép hàng năm (CAGR) (%)."""
    try:
        # Đảm bảo cột 'time' là kiểu datetime
        df['time'] = pd.to_datetime(df['time'])
        # Lấy giá trị đầu và cuối
        start_val = df['close'].iloc[0]
        end_val = df['close'].iloc[-1]
        # Lấy ngày đầu và cuối
        start_date = df['time'].iloc[0]
        end_date = df['time'].iloc[-1]
        # Tính số ngày 
        num_days = (end_date - start_date).days
        if num_days <= 0:
            return 0.0

        num_years = num_days / 365.25  # Dùng 365.25 để tính năm nhuận
        # Công thức CAGR
        cagr = ((end_val / start_val) ** (1 / num_years)) - 1
        
        return cagr * 100  
    except Exception as e:
        print(f"Lỗi khi tính CAGR: {e}")
        return 0.0

# ===== FUNCTION 9: Gói toàn bộ logic xử lý từng mã =====
def process_stock(symbol, start, end): 
    """Lấy, phân tích và tính drawdown cho 1 cổ phiếu."""
    df = fetch_stock_data(symbol, start, end)
    
    # Tính toán các chỉ số
    avg_close, profit_pct = analyze_stock(df)
    stock_list, stock_tuples = convert_to_structures(df)
    drawdowns, max_dd = compute_drawdowns(df["close"].tolist())
    volatility = compute_volatility(df)
    cagr_pct = compute_cagr(df) 

    print(f"{symbol}: Avg Close={avg_close:.2f}, Profit={profit_pct:.2f}%, CAGR={cagr_pct:.2f}%, MaxDD={max_dd:.2f}%, Vol={volatility:.2f}%")

    # Trả về dict kết quả
    return {
        "symbol": symbol,
        "average_close": avg_close,
        "profit_pct": profit_pct,
        "cagr_pct": cagr_pct,
        "max_drawdown": max_dd,
        "volatility_pct": volatility,
        "list_of_dicts": stock_list,
        "list_of_tuples": stock_tuples,
    } 
    
# ===== FUNCTION 10: GỘP DỮ LIỆU GIÁ CÁC MÃ =====
def get_portfolio_prices(symbols):
    """
    Đọc từ CSV, gộp giá đóng cửa của các mã vào một DataFrame.
    Trả về 2 DataFrame: giá đóng cửa (prices) và lợi nhuận ngày (returns).
    """
    print("\nĐang gộp dữ liệu giá danh mục...")
    portfolio_prices = pd.DataFrame()

    for symbol in symbols:
        csv_file = f"{symbol}_history.csv"
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df_close = df[['time', 'close']].copy()
            df_close.rename(columns={'close': symbol}, inplace=True)
            df_close['time'] = pd.to_datetime(df_close['time'])
            df_close.set_index('time', inplace=True)

            if portfolio_prices.empty:
                portfolio_prices = df_close
            else:
                portfolio_prices = portfolio_prices.join(df_close, how='outer')
        else:
            print(f"Không tìm thấy file {csv_file}, vui lòng chạy lại Main.")
            return None, None

    # 1. Tính lợi nhuận ngày
    daily_returns = portfolio_prices.pct_change().dropna()

    # 2. Dùng ffill (forward fill) để lấp các ngày nghỉ
    portfolio_prices = portfolio_prices.ffill().dropna()

    return portfolio_prices, daily_returns
# ===== FUNCTION 11 : TÍNH TƯƠNG QUAN =====
def analyze_correlation(daily_returns):
    """
    Chỉ tính toán và in ma trận tương quan từ daily_returns.
    """
    print("Đang phân tích tương quan danh mục...")
    
    # Tính tương quan (Yêu cầu của Project)
    correlation_matrix = daily_returns.corr()
    
    print("Ma trận tương quan (Correlation Matrix):")
    print(correlation_matrix.to_string(float_format='%.2f'))

    return correlation_matrix 
# ===== FUNCTION 12: VẼ BIỂU ĐỒ =====
# ===== FUNCTION 12.1: VẼ HEATMAP TƯƠNG QUAN =====
def plot_correlation_heatmap(correlation_matrix):
    """Vẽ và lưu biểu đồ heatmap tương quan."""
    print("Đang vẽ biểu đồ 1: Heatmap tương quan...")
    try:
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Biểu đồ 1: Tương quan lợi nhuận giữa các mã")
        
        plot_file = os.path.join(DATASET_DIR, "plot_1_heatmap.png")
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.show()
        plt.close() 
        print(f"Đã lưu: {plot_file}")
    except Exception as e:
        print(f"Lỗi khi vẽ Heatmap: {e}")
    

# ===== FUNCTION 12.2: VẼ BIỂU ĐỒ GIÁ (LINE GRAPH) =====
def plot_price_line_graph(portfolio_prices, start_date, end_date):
    """Vẽ biểu đồ đường so sánh giá của các mã."""
    print("Đang vẽ biểu đồ 2: So sánh giá cổ phiếu (Line Graph)...")
    try:
        plt.figure(figsize=(12, 6))
        
        # Dùng seaborn để vẽ line plot cho DataFrame
        
        sns.lineplot(data=portfolio_prices) #, dashes=False) đường nét liền
        
        title_str = f"Biểu đồ 2: So sánh giá cổ phiếu (Từ {start_date} đến {end_date})"
        plt.title(title_str)
        plt.xlabel("Thời gian")
        plt.ylabel("Giá đóng cửa (Đã điều chỉnh)")
        plt.legend(title="Mã Cổ Phiếu")
        
        plot_file = os.path.join(DATASET_DIR, "plot_2_price_line_graph.png")
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.show()
        plt.close() # Đóng figure
        print(f"Đã lưu: {plot_file}")
    except Exception as e:
        print(f"Lỗi khi vẽ Line Graph: {e}")

# ===== FUNCTION 12.3: VẼ BAR PLOT SO SÁNH LỢI NHUẬN =====
def plot_profit_barplot(portfolio_df, start_date, end_date): 
    """Vẽ biểu đồ cột so sánh % lợi nhuận."""
    print("Đang vẽ biểu đồ 3: So sánh lợi nhuận...")
    try:
        portfolio_df_sorted = portfolio_df.sort_values('profit_pct', ascending=False)

        plt.figure(figsize=(10, 4))
        sns.barplot(x='profit_pct', y='symbol', data=portfolio_df_sorted)
        
        # ===  TITLE ===
        title_str = f"Biểu đồ 3: So sánh % Lợi nhuận (Từ {start_date} đến {end_date})"
        plt.title(title_str)
        # ======================
        
        plt.xlabel("Lợi nhuận (%)")
        plt.ylabel("Mã Cổ Phiếu")

        plot_file = os.path.join(DATASET_DIR, "plot_3_profit_barplot.png")
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.show()
        plt.close() 
        print(f"Đã lưu: {plot_file}")
    except Exception as e:
        print(f"Lỗi khi vẽ Bar Plot: {e}")
    
        
# ===== FUNCTION 13 : XUẤT CSV TỔNG HỢP =====
def export_summary_csv(portfolio_list):
    """Chuyển list portfolio sang DataFrame và lưu CSV."""
    
    summary_data = []
    for s in portfolio_list:
        summary_data.append({
            "symbol": s["symbol"],
            "average_close": s["average_close"],
            "profit_pct": s["profit_pct"],
            "cagr_pct": s["cagr_pct"], 
            "max_drawdown": s["max_drawdown"],
            "volatility_pct": s["volatility_pct"],
        })
        
    df = pd.DataFrame(summary_data)
    
    # Dùng describe() của Pandas (Yêu cầu của Project)
    print("\nThống kê mô tả (describe) toàn danh mục:")
    print(df.describe().to_string(float_format='%.2f'))
    
    # Lưu file CSV (Deliverable 6.2)
    csv_path = os.path.join(DATASET_DIR, "portfolio_analysis_summary.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig", float_format='%.2f')
    print(f"\nĐã lưu file tổng kết phân tích tại: {csv_path}")
    
    return df

# ===== MAIN  =====
if __name__ == "__main__":
    print("=== Bắt đầu phân tích danh mục cổ phiếu ===")
    #2 Ngân hàng, 1 Bất động sản, 2 Công Nghệ thông tin
    symbols = ["TCB", "BID", "VIC", "FPT", "CTR"]
    #symbols = ["TCB", "BID", "VHM", "KBC", "GAS", "POW", "FPT", "CTR", "DHG", "TNH"]
    
    # Định nghĩa ngày ở đây để dùng chung
    start_date = "2023-01-01"
    end_date = "2025-01-01"
    
    # 1. Chạy phân tích từng mã
    portfolio_list = [process_stock(sym, start=start_date, end=end_date) for sym in symbols]

    best_stock = max(portfolio_list, key=lambda x: x["profit_pct"])
    print("🔥 Cổ phiếu tăng trưởng tốt nhất:", best_stock["symbol"], f"({best_stock['profit_pct']:.2f}%)")

    # 2. Lọc cổ phiếu (ví dụ)
    top_stocks = filter_top_stocks(portfolio_list, min_profit=10, max_dd=-25, max_volatility=5)
    if top_stocks:
        print("\n Các cổ phiếu tiềm năng (Profit > 10%, MaxDD > -25%, Vol < 5%):")
        for s in top_stocks:
            print(f" - {s['symbol']} | Profit={s['profit_pct']:.2f}% | MaxDD={s['max_drawdown']:.2f}% | Vol={s['volatility_pct']:.2f}%")
    else:
        print("\nKhông có cổ phiếu nào tiềm năng.")

    # 3. Xuất file CSV tổng hợp (Deliverable 6.2)
    portfolio_df = export_summary_csv(portfolio_list)

    # 4.  Lấy dữ liệu gộp giá đóng cửa và lợi nhuận ngày
    portfolio_prices, daily_returns = get_portfolio_prices(symbols)

    # 5. Vẽ 3 biểu đồ
    if portfolio_prices is not None and daily_returns is not None:
        
        # 5.1. Tính và vẽ Heatmap (Dùng daily_returns)
        corr_matrix = analyze_correlation(daily_returns)
        plot_correlation_heatmap(corr_matrix) 
        
        # 5.2. Vẽ Line Graph (Dùng portfolio_prices)
        plot_price_line_graph(portfolio_prices, start_date, end_date)
        
        # 5.3. Vẽ Bar Plot (Dùng portfolio_df)
        plot_profit_barplot(portfolio_df, start_date, end_date)