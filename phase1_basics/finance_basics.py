# Phase 1 - Finance domain (Stock/Crypto)

# 1. Tính lợi nhuận % từ giá mua và giá bán
def calc_profit_percent(buy_price, sell_price):
    profit = ((sell_price - buy_price) / buy_price) * 100
    return profit

# 2. Check hôm nay tăng hay giảm
def check_trend(today_price, yesterday_price):
    if today_price > yesterday_price:
        return "Tăng"
    elif today_price < yesterday_price:
        return "Giảm"
    else:
        return "Không đổi"

# 3. Tính trung bình giá từ list
def average_price(prices):
    total = 0
    for p in prices:
        total += p
    return total / len(prices)

# 4. Tìm giá cao nhất & thấp nhất
def min_max_price(prices):
    highest = max(prices)
    lowest = min(prices)
    return highest, lowest


# ---- Demo chạy thử ----
prices_week = [101, 105, 98, 110, 120, 115, 108]

print("1. Lợi nhuận % (mua 100, bán 120):", calc_profit_percent(100, 120), "%")
print("2. Xu hướng hôm nay:", check_trend(108, 115))
print("3. Giá trung bình tuần:", average_price(prices_week))
print("4. Giá cao nhất & thấp nhất:", min_max_price(prices_week))
