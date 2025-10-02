# ---- Function 1: Tính trung bình & lợi nhuận % ----
def analyze_stock(prices):
    avg_close = sum(prices) / len(prices)
    profit_pct = ((prices[-1] - prices[0]) / prices[0]) * 100
    return avg_close, profit_pct


# ---- Function 2: Chuyển sang list of dicts ----
def convert_to_list_of_dicts(symbol, prices, dates):
    stock_list = []
    for i in range(len(prices)):
        stock_list.append({"symbol": symbol, "date": dates[i], "close": prices[i]})
    return stock_list


# ---- Function 3: Chuyển sang list of tuples ----
def convert_to_list_of_tuples(prices, dates):
    stock_tuples = []
    for i in range(len(prices)):
        stock_tuples.append((dates[i], prices[i]))
    return stock_tuples


# ---- Demo ----
if __name__ == "__main__":
    # Hardcode dữ liệu 7 ngày 
    week_dates = [
        "2023-01-01", "2023-01-02", "2023-01-03", 
        "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07"
    ]

    stock_data_hardcode = {
        "FPT": [85, 87, 86, 90, 92, 91, 93],
        "VCB": [70, 72, 71, 73, 75, 74, 76],
        "MBB": [20, 21, 22, 21, 23, 24, 25],
        "VIC": [55, 56, 57, 58, 60, 61, 62],
    }

    portfolio = []  # list of dicts (nhiều cổ phiếu)

    for symbol, prices in stock_data_hardcode.items():
        avg, profit = analyze_stock(prices)
        stock_list = convert_to_list_of_dicts(symbol, prices, week_dates)
        stock_tuples = convert_to_list_of_tuples(prices, week_dates)

        stock_info = {
            "symbol": symbol,
            "average_close": avg,
            "profit_pct": profit,
            "list_of_dicts": stock_list,
            "list_of_tuples": stock_tuples
        }
        portfolio.append(stock_info)

        print(f"{symbol}: Avg Close = {avg:.2f}, Profit % = {profit:.2f}%")

    # Tìm cổ phiếu lời nhiều nhất
    best_stock = max(portfolio, key=lambda x: x["profit_pct"])
    print("\nCổ phiếu tăng trưởng tốt nhất:", best_stock["symbol"], f"({best_stock['profit_pct']:.2f}%)")
