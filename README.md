# 📊 Project Phân tích Dữ liệu Tài chính (PSD301M)

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-purple?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-1.2x-orange?style=for-the-badge&logo=numpy)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-blueviolet?style=for-the-badge&logo=seaborn)

Đây là project cuối kỳ cho môn PSD301M, áp dụng kiến thức Python từ cơ bản đến nâng cao (NumPy, Pandas) để xây dựng một quy trình phân tích dữ liệu tài chính hoàn chỉnh.

Project tập trung vào việc thu thập dữ liệu qua API (`vnstock`), xử lý, phân tích thống kê và trực quan hóa kết quả để tìm ra các insight (nhận định) đầu tư.


---

## 🌟 Các tính năng chính (Theo 3 Giai đoạn)

### 📚 Phase 1 – Python Basics

* **Mục tiêu:** Ôn tập cú pháp Python cơ bản.
* Viết các hàm cơ bản để xử lý dữ liệu:
    * Tính lợi nhuận/lỗ (%) khi mua – bán.
    * Phân loại hiệu suất cổ phiếu.
    * Tìm giá cao nhất & thấp nhất.

### 📦 Phase 2 – Data Structures

* **Mục tiêu:** Vận dụng các cấu trúc dữ liệu.
* Sử dụng **List / Dict / Set / Tuple** để quản lý và tổ chức dữ liệu tài chính.
* Chuẩn bị dữ liệu dạng `list of dict` (mô phỏng JSON) cho các phân tích phức tạp hơn.

### 🚀 Phase 3 – API, Pandas & NumPy Analysis

* **Mục tiêu:** Phân tích dữ liệu thực tế.
* **Thu thập dữ liệu (API):** Sử dụng thư viện `vnstock` để tải dữ liệu lịch sử (2023-2025) của 5 mã cổ phiếu: `FPT`, `CTR`, `BID`, `TCB`, `VIC`.
* **Xử lý (Pandas):** Dữ liệu được load vào Pandas DataFrame.
* **Phân tích (Pandas & NumPy):**
    * Tính toán các chỉ số hiệu suất: Lợi nhuận (`profit_pct`), Tăng trưởng kép hàng năm (`cagr_pct`).
    * Tính toán các chỉ số rủi ro: Sụt giảm tối đa (`max_drawdown`), Biến động (`volatility`).
    * Tính toán ma trận tương quan (`.corr()`) giữa các mã.
    * Sử dụng `.describe()` để thống kê mô tả toàn danh mục.
* **Trực quan hóa (Matplotlib & Seaborn):**
    * Xuất 3 biểu đồ phân tích ra file PNG.
* **Xuất kết quả:**
    * Lưu file `portfolio_analysis_summary.csv` chứa kết quả phân tích tổng hợp.
    * Lưu 3 file biểu đồ (`.png`) vào thư mục `dataset`.

---

## 📈 Kết quả đầu ra

Script chính (`test_phase3_pandas.py`) sẽ tự động tải dữ liệu và tạo ra các file phân tích trong thư mục `phase3_api_analysis/dataset/`:

1.  **File CSV tổng hợp:** `portfolio_analysis_summary.csv`
2.  **Biểu đồ 1:** `plot_1_heatmap.png` (Ma trận tương quan)
3.  **Biểu đồ 2:** `plot_2_price_line_graph.png` (So sánh tăng trưởng chuẩn hóa)
4.  **Biểu đồ 3:** `plot_3_profit_barplot.png` (So sánh % lợi nhuận)



---

## 🛠️ Cài đặt & Chạy dự án

### 1. Clone Repository

```bash
git clone [https://github.com/GiaHuy-K/finance-analysis-project.git](https://github.com/GiaHuy-K/finance-analysis-project.git)
cd finance-analysis-project
```
### 2. Tạo môi trường ảo và cài thư viện
(Khuyến khích) nên tạo môi trường ảo venv:
Kích hoạt môi trường ảo:

Trên Windows:

```Bash

.\venv\Scripts\activate
```
Cài đặt thư viện:

```Bash

pip install -r requirements.txt
```
### 3. Chạy phân tích Giai đoạn 3
Đây là phần quan trọng nhất. Script sẽ tự động chạy và xuất kết quả.
## Di chuyển vào thư mục Phase 3
```Bash
cd phase3_api_analysis
```
## Chạy file phân tích chính
```Bash
python test_phase3_pandas.py
```
