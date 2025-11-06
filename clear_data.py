import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DATASET_DIR = os.path.join(BASE_DIR, "phase3_api_analysis", "dataset")

def clear_output_files(): 
    count = 0
    
    # Đảm bảo thư mục dataset tồn tại
    if not os.path.exists(DATASET_DIR):
        print("Thư mục 'dataset' không tồn tại.")
        return

    # Chỉ đi tìm trong DATASET_DIR, không đi lung tung ra BASE_DIR
    for root, dirs, files in os.walk(DATASET_DIR):
        for file in files:
            if file.endswith(".csv") or file.endswith(".png"):
                # Chỉ xoá file, không xoá thư mục
                if os.path.isfile(os.path.join(root, file)): 
                    try:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        count += 1
                    except OSError as e:
                        print(f"Lỗi khi xoá file {file_path}: {e}")

    print(f"Đã xoá {count} file CSV và PNG trong thư mục 'dataset'.")

if __name__ == "__main__":
    clear_output_files()