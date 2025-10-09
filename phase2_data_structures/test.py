import os
import pandas as pd
# DÒNG SỬA 1: Thêm 'stock_listing' vào đây
from vnstock import Vnstock, stock_listing
from datetime import datetime, timedelta

# ===== PATH SETUP (Không đổi) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)


class Stock:
    """
    Đại diện cho một mã cổ phiếu duy nhất.
    Class này chịu trách nhiệm lấy dữ liệu và tự tính toán các chỉ số cho chính nó.
    """
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = pd.DataFrame()
        self.average_close = 0
        self.profit_pct = 0
        self.max_drawdown = 0
        self.volatility_pct = 0

    def __str__(self):
        """Định dạng cách hiển thị đối tượng Stock khi được print()"""
        if self.data.empty:
            return f"[{self.symbol}] - Chưa có dữ liệu."
        return (
            f"[{self.symbol}] Lợi nhuận: {self.profit_pct:.2f}% | "
            f"Max Drawdown: {self.max_drawdown:.2f}% | "
            f"Biến động: {self.volatility_pct:.2f}%"
        )

    def fetch_data(self, start, end):
        """Lấy dữ liệu lịch sử giá và lưu vào thuộc tính 'data'."""
        try:
            print(f"   - Đang tải dữ liệu cho {self.symbol}...")
            # Sử dụng lại đối tượng api để tránh khởi tạo nhiều lần
            df = Vnstock().stock(symbol=self.symbol, source="VCI").quote.history(start=start, end=end, interval="1D")
            
            if df.empty:
                print(f"   ⚠️ Không tìm thấy dữ liệu cho mã {self.symbol} trong khoảng {start} -> {end}.")
                self.data = pd.DataFrame() # Đảm bảo data rỗng
                return False
            
            # Lưu file CSV
            file_path = os.path.join(DATASET_DIR, f"{self.symbol}_history.csv")
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            
            self.data = df
            return True
        except Exception as e:
            print(f"   ❌ Lỗi khi tải dữ liệu cho {self.symbol}: {e}")
            self.data = pd.DataFrame() # Đảm bảo data rỗng
            return False

    def analyze(self):
        """Thực hiện tất cả các phép tính phân tích cho cổ phiếu này."""
        if self.data.empty:
            print(f"   - Bỏ qua phân tích {self.symbol} do không có dữ liệu.")
            return

        self._calculate_basic_stats()
        self._calculate_max_drawdown()
        self._calculate_volatility()
        print(f"   ✓ Phân tích {self.symbol} hoàn tất.")

    def _calculate_basic_stats(self):
        self.average_close = self.data["close"].mean()
        first_price = self.data["close"].iloc[0]
        last_price = self.data["close"].iloc[-1]
        if first_price != 0:
            self.profit_pct = ((last_price - first_price) / first_price) * 100
        else:
            self.profit_pct = 0

    def _calculate_max_drawdown(self):
        prices = self.data["close"]
        peak = prices.iloc[0]
        max_dd = 0.0
        for p in prices:
            if p > peak:
                peak = p
            if peak != 0:
                dd = (p - peak) / peak * 100.0
                if dd < max_dd:
                    max_dd = dd
        self.max_drawdown = max_dd

    def _calculate_volatility(self):
        returns = self.data["close"].pct_change().dropna()
        if not returns.empty:
            self.volatility_pct = returns.std() * 100
        else:
            self.volatility_pct = 0

class PortfolioAnalyzer:
    """Quản lý và phân tích một danh mục gồm nhiều đối tượng Stock."""
    def __init__(self, symbols):
        # Tự động loại bỏ khoảng trắng và viết hoa
        self.symbols = [s.strip().upper() for s in symbols if s.strip()]
        self.portfolio = [Stock(s) for s in self.symbols]
        print(f"Đã khởi tạo danh mục với các mã: {', '.join(self.symbols)}")

    def run_analysis(self, start, end):
        print(f"\nBắt đầu quá trình phân tích danh mục từ {start} đến {end}...")
        for stock in self.portfolio:
            if stock.fetch_data(start, end):
                stock.analyze()
        print("--- Phân tích danh mục hoàn tất ---\n")
    
    def display_results(self):
        print("--- KẾT QUẢ PHÂN TÍCH DANH MỤC ---")
        for stock in self.portfolio:
            print(stock)
        print("------------------------------------")

    def get_best_performer(self):
        valid_stocks = [s for s in self.portfolio if not s.data.empty]
        if not valid_stocks: return None
        return max(valid_stocks, key=lambda stock: stock.profit_pct)

    def filter_potential_stocks(self, min_profit, max_dd, max_volatility):
        return [s for s in self.portfolio if not s.data.empty and s.profit_pct >= min_profit and s.max_drawdown >= max_dd and s.volatility_pct <= max_volatility]

# ===== CÁC HÀM TIỆN ÍCH CHO MENU =====

def display_menu():
    """Hiển thị menu cho người dùng."""
    print("\n===== MENU PHÂN TÍCH CỔ PHIẾU =====")
    print("1. Xem danh sách mã cổ phiếu (HOSE)")
    print("2. Phân tích danh mục")
    print("3. Tìm cổ phiếu tăng trưởng tốt nhất")
    print("4. Lọc cổ phiếu tiềm năng")
    print("5. Thoát")
    print("=====================================")

def get_date_range():
    """Hỏi người dùng và trả về khoảng thời gian phân tích."""
    print("\n--- Vui lòng chọn khoảng thời gian phân tích ---")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    start_date_default = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    start = input(f"Nhập ngày bắt đầu (YYYY-MM-DD) [mặc định: {start_date_default}]: ") or start_date_default
    end = input(f"Nhập ngày kết thúc (YYYY-MM-DD) [mặc định: {end_date_default}]: ") or end_date_default
    
    return start, end

def show_listed_companies():
    """Hiển thị 100 mã cổ phiếu đầu tiên trên sàn HOSE."""
    try:
        print("\nĐang tải danh sách các mã niêm yết...")
        # DÒNG SỬA 2: Thay đổi cách gọi hàm tại đây
        df = stock_listing() 
        print("--- 100 MÃ CỔ PHIẾU ĐẦU TIÊN TRÊN SÀN HOSE ---")
        # 'comGroupCode' đã được đổi tên thành 'exchange' trong các phiên bản mới
        hose_stocks = df[df['exchange'] == 'HOSE'][['ticker', 'company_name']].head(100)
        # Sử dụng to_string để hiển thị đẹp hơn trong console
        print(hose_stocks.to_string(index=False))
        print("-------------------------------------------------")
    except Exception as e:
        print(f"Lỗi khi tải danh sách công ty: {e}")

# ===== MAIN: Vòng lặp chính của chương trình =====
if __name__ == "__main__":
    analyzer = None

    while True:
        display_menu()
        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            show_listed_companies()

        elif choice == '2':
            symbols_input = input("\nNhập các mã cổ phiếu muốn phân tích, cách nhau bằng dấu phẩy (VD: FPT,VCB,MBB): ")
            if not symbols_input.strip():
                print("⚠️ Danh sách mã không được để trống.")
                continue
            
            symbols = symbols_input.split(',')
            start_date, end_date = get_date_range()
            analyzer = PortfolioAnalyzer(symbols)
            analyzer.run_analysis(start=start_date, end=end_date)
            analyzer.display_results()

        elif choice == '3':
            if not analyzer:
                print("⚠️ Vui lòng chạy 'Phân tích danh mục' (lựa chọn 2) trước.")
                continue
            
            start_date, end_date = get_date_range()
            analyzer.run_analysis(start=start_date, end=end_date) # Phân tích lại với ngày mới
            
            best_stock = analyzer.get_best_performer()
            if best_stock:
                print(f"\n🔥 Trong khoảng {start_date} -> {end_date}, cổ phiếu tăng trưởng tốt nhất là:")
                print(best_stock)
            else:
                print("Không có cổ phiếu nào hợp lệ để tìm kiếm.")

        elif choice == '4':
            if not analyzer:
                print("⚠️ Vui lòng chạy 'Phân tích danh mục' (lựa chọn 2) trước.")
                continue

            start_date, end_date = get_date_range()
            analyzer.run_analysis(start=start_date, end=end_date) # Phân tích lại với ngày mới
            
            try:
                print("\n--- Nhập tiêu chí để lọc cổ phiếu ---")
                min_p = float(input("Lợi nhuận tối thiểu (%): "))
                max_d = float(input("Sụt giảm tối đa chấp nhận được (%, nhập số âm, VD: -15): "))
                max_v = float(input("Độ biến động tối đa (%): "))
                
                top_stocks = analyzer.filter_potential_stocks(min_p, max_d, max_v)
                
                if top_stocks:
                    print(f"\n💎 Trong khoảng {start_date} -> {end_date}, các cổ phiếu tiềm năng tìm thấy:")
                    for stock in top_stocks:
                        print(f" - {stock}")
                else:
                    print("\nKhông tìm thấy cổ phiếu nào thỏa mãn tiêu chí.")
            except ValueError:
                print("⚠️ Vui lòng nhập đúng định dạng số.")

        elif choice == '5':
            print("👋 Tạm biệt!")
            break
        else:
            print("⚠️ Lựa chọn không hợp lệ, vui lòng nhập lại.")