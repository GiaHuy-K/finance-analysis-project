# Phase 1 - Finance domain (Stock/Crypto)

# 1. Tính lợi nhuận % từ giá mua và giá bán
def calc_profit_percent(buy_price, sell_price):
    return ((sell_price - buy_price) / buy_price) * 100

# 2. Phân loại hiệu suất cổ phiếu
def classify_stock_change(start_price, end_price):
    change_percent = ((end_price - start_price) / start_price) * 100
    if change_percent > 5:
        return "Tăng mạnh"
    elif change_percent < -5:
        return "Giảm mạnh"
    else:
        return "Ổn định"

# 3. Tính trung bình động (Moving Average)
def moving_average(prices, window):
    if len(prices) < window:
        return None  # không đủ dữ liệu thì ra None 
    return sum(prices[-window:]) / window
# 4. Tìm giá cao nhất & thấp nhất
def min_max_price(prices):
    return max(prices), min(prices)


# ---- Demo chạy thử ----

prices_week = [101, 105, 98, 110, 120, 115, 108]

print("1. Lợi nhuận % (mua 100, bán 120):", calc_profit_percent(100, 120), "%")
print("2. Hiệu suất tuần:", classify_stock_change(prices_week[0], prices_week[-1]))
print("3. Moving Average 3 ngày: {:<.2f}".format(moving_average(prices_week, 3)))
print("4. Giá cao nhất & thấp nhất:", min_max_price(prices_week))



# | API                           | Loại dữ liệu                                 | Ghi chú                                                   |
# | ----------------------------- | -------------------------------------------- | --------------------------------------------------------- |
# | Alpha Vantage                 | cổ phiếu, forex, crypto, indicators          | miễn phí, cần đăng ký key ([alphavantage.co][1])          |
# | Marketstack                   | real-time, lịch sử cổ phiếu                  | free tier với ~100 requests/tháng ([marketstack.com][2])  |
# | Finnhub                       | real-time & lịch sử stock, báo cáo tài chính | cung cấp gói miễn phí cho dev ([finnhub.io][3])           |
# | Financial Modeling Prep (FMP) | cổ phiếu, báo cáo tài chính, lịch sử         | có truy cập miễn phí với key ([FinancialModelingPrep][4]) |
# | Polygon.io                    | dữ liệu lịch sử & real-time                  | có free tier cho dev ([polygon.io][5])                    |
# | EODHD                         | dữ liệu lịch sử & real-time                  | có key miễn phí cho gói dùng thử ([eodhd.com][6])         |

# [1]: https://www.alphavantage.co/     "Alpha Vantage: Free Stock APIs in JSON & Excel"
# [2]: https://marketstack.com/         "Free Stock Market Data API for Real-Time & Historical Data"
# [3]: https://finnhub.io/              "Finnhub Stock APIs - Real-time stock prices, Company ..."
# [4]: https://site.financialmodelingprep.com/developer/docs "Free Stock Market API and Financial Statements API... | FMP"
# [5]: https://polygon.io/              "Polygon.io: Stock Market API"
# [6]: https://eodhd.com/ "             The Best API for Historical Stock Market Prices and ..."
