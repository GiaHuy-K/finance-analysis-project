# ---- Function 1: Tính trung bình & lợi nhuận % ----
def analyze_stock(prices):
    avg_close = sum(prices) / len(prices)
    profit_pct = ((prices[-1] - prices[0]) / prices[0]) * 100
    return avg_close, profit_pct


# ---- Function 2: Kiểm tra vốn hóa ----
def check_market_cap(stock_data):
    """Kiểm tra xem vốn hóa (tỷ USD) có lớn hơn hoặc bằng 10 tỷ USD không."""
    if stock_data["market_cap_billion_usd"] >= 10.0:
        return "Vốn hóa lớn hơn 10 tỷ USD"
    else:
        return "Vốn hóa vừa/nhỏ hơn 10 tỷ USD"


# ---- Function 3: Kiểm tra cổ phiếu top ----
def is_top_stock(ticker, top_tickers):
    """Kiểm tra mã cổ phiếu có nằm trong Tuple TOP_TICKERS không."""
    return ticker in top_tickers


# ---- Function 4: Chuyển sang list of dicts ----
def convert_to_list_of_dicts(symbol, prices, dates):
    stock_list = []
    for i in range(len(prices)):
        stock_list.append({"symbol": symbol, "date": dates[i], "close": prices[i]})
    return stock_list


# ---- Function 5: Chuyển sang list of tuples ----
def convert_to_list_of_tuples(prices, dates):
    stock_tuples = []
    for i in range(len(prices)):
        stock_tuples.append((dates[i], prices[i]))
    return stock_tuples


# ---- Function 6: Tính drawdown & max drawdown ----
def compute_drawdowns(prices):
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


# ---- Function 7: Tính độ biến động (volatility %) ----
def compute_volatility(prices):
    """Tính độ biến động dựa trên % thay đổi giữa các ngày."""
    returns = []
    for i in range(1, len(prices)):
        change = (prices[i] - prices[i - 1]) / prices[i - 1]
        returns.append(change)
    avg = sum(returns) / len(returns)
    variance = sum((r - avg) ** 2 for r in returns) / len(returns)
    volatility = (variance ** 0.5) * 100  # Độ lệch chuẩn * 100 (%)
    return volatility


# ---- Function 8: Lọc cổ phiếu tiềm năng ----
def filter_top_stocks(portfolio, min_profit=20, max_dd=-10, max_volatility=5):
    """Lọc cổ phiếu lợi nhuận cao, drawdown nhỏ và biến động thấp."""
    return [
        s for s in portfolio
        if s["profit_pct"] >= min_profit
        and s["max_drawdown"] >= max_dd
        and s.get("volatility_pct", 999) <= max_volatility
    ]


# ---- Demo ----
if __name__ == "__main__":
    # Hardcode dữ liệu 7 ngày
    week_dates = [
        "2023-01-01", "2023-01-02", "2023-01-03",
        "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07"
    ]

    stock_data_hardcode = {
        "FPT": {"prices": [85, 87, 86, 90, 92, 91, 93], "market_cap_billion_usd": 8.5},
        "VCB": {"prices": [70, 72, 71, 73, 75, 74, 76], "market_cap_billion_usd": 15.2},
        "MBB": {"prices": [20, 21, 22, 21, 23, 24, 25], "market_cap_billion_usd": 6.7},
        "VIC": {"prices": [55, 56, 57, 58, 60, 61, 62], "market_cap_billion_usd": 11.3},
    }

    TOP_TICKERS = ("VCB", "VIC", "FPT")
    portfolio = []

    for symbol, data in stock_data_hardcode.items():
        prices = data["prices"]
        avg, profit = analyze_stock(prices)
        stock_list = convert_to_list_of_dicts(symbol, prices, week_dates)
        stock_tuples = convert_to_list_of_tuples(prices, week_dates)
        dds, max_dd = compute_drawdowns(prices)
        volatility = compute_volatility(prices)
        cap_status = check_market_cap(data)
        top_status = "Có trong TOP" if is_top_stock(symbol, TOP_TICKERS) else "Không trong TOP"

        stock_info = {
            "symbol": symbol,
            "average_close": avg,
            "profit_pct": profit,
            "max_drawdown": max_dd,
            "volatility_pct": volatility,
            "market_cap_status": cap_status,
            "top_status": top_status,
            "list_of_dicts": stock_list,
            "list_of_tuples": stock_tuples
        }
        portfolio.append(stock_info)

        print(f"{symbol}: Avg Close = {avg:.2f}, Profit % = {profit:.2f}%, Volatility = {volatility:.2f}%")
        print(f"Drawdowns (%): {[round(x, 2) for x in dds]}")
        print(f"Max drawdown (%): {round(max_dd, 2)}")
        print(f"{cap_status} | {top_status}\n")

    # Cổ phiếu lời cao nhất
    best_stock = max(portfolio, key=lambda x: x["profit_pct"])
    print("🔥 Cổ phiếu tăng trưởng tốt nhất:", best_stock["symbol"], f"({best_stock['profit_pct']:.2f}%)")

    # Lọc cổ phiếu tiềm năng
    top_stocks = filter_top_stocks(portfolio)
    print("\n Các cổ phiếu tiềm năng:")
    if top_stocks:
        for s in top_stocks:
            print(f" - {s['symbol']} | Profit={s['profit_pct']:.2f}% | MaxDD={s['max_drawdown']:.2f}% | Vol={s['volatility_pct']:.2f}%")
    else:
        print("Không có cổ phiếu nào tiềm năng.")
