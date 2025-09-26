# 📊 Finance Analysis Project

Phân tích dữ liệu tài chính bằng Python qua từng phase: từ cơ bản → data structures → phân tích nâng cao.

---

## 📚 Phase 1 – Python Basics
- Viết các hàm cơ bản để xử lý dữ liệu giá cổ phiếu:
  - Tính lợi nhuận/lỗ (%) khi mua – bán (`calc_profit_percent`)
  - Phân loại hiệu suất cổ phiếu theo % thay đổi (`classify_stock_change`)
  - Tính trung bình động (Moving Average) để quan sát xu hướng (`moving_average`)
  - Tìm giá cao nhất & thấp nhất trong danh sách giá (`min_max_price`)

---


## 📚 Phase 2 – Data Structures
- Dùng **list / dict / set / tuple** để quản lý dữ liệu tài chính.  
- Chuẩn bị dữ liệu dạng `list of dict` giống JSON.

---

## 🚀 Cách chạy project

```bash
# 1. Clone repo
git clone https://github.com/GiaHuy-K/finance-analysis-project.git 
cd finance-analysis-project

# 2. (Tuỳ chọn) Tạo môi trường ảo & cài thư viện
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt

# 3. Chạy thử Phase 1
python tên-file.py




