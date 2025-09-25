import yfinance as yf
import pandas as pd

# ==============================
# 1. Lấy dữ liệu cổ phiếu
# ==============================
tickers = ["AAPL", "TSLA", "MSFT"]  # Apple, Tesla, Microsoft

print("Đang tải dữ liệu từ Yahoo Finance...")
data = yf.download(tickers, period="6mo", interval="1d")

# ==============================
# 2. Lưu dữ liệu ra CSV
# ==============================
data.to_csv("stock_data.csv")
print("Đã lưu dữ liệu vào stock_data.csv")

# ==============================
# 3. Phân tích nhanh với Pandas
# ==============================
# Lấy giá đóng cửa (Close)
close_prices = data["Close"]

print("\n Giá đóng cửa trung bình 6 tháng:")
print(close_prices.mean())

print("\n Giá thấp nhất trong 6 tháng:")
print(close_prices.min())

print("\n Giá cao nhất trong 6 tháng:")
print(close_prices.max())

# ==============================
# 4. Vẽ biểu đồ 
# ==============================
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
for ticker in tickers:
    plt.plot(close_prices[ticker], label=ticker)

plt.title("Stock Prices (6 months)")
plt.xlabel("Date")
plt.ylabel("Close Price (USD)")
plt.legend()
plt.grid(True)
plt.show()
